# -----------------------------
# Hybrid (HDF5 + SQLite) backend
# -----------------------------
"""IO/storage_backend.py

Hybrid storage backend combining SQLite (index + metadata) and HDF5 (object
payloads) for efficient, scalable persistence of Python objects related to
atomistic simulations.

This module provides the :class:`HybridStorage` class, which stores a pickled
payload per object in an HDF5 dataset and mirrors essential metadata (energy,
atom count, composition, empirical formula) in a lightweight SQLite schema to
enable fast queries without loading full objects.

Design goals:
    * **Performance**: metadata queries are served from SQLite indices; payloads
      are compressed with gzip inside HDF5 for efficient disk usage.
    * **Convenience**: automatic extraction of energy and species labels from
      common attribute names (e.g., ``obj.E`` or
      ``obj.AtomPositionManager.atomLabelsList``).
    * **Stability**: robust to arrays or scalars for energies and labels.
    
Notes:
    - The composition table uses an Entity–Attribute–Value (EAV) layout to
      efficiently query per-species counts across objects.
    - Formulas are rendered with alphabetical element ordering for simplicity.
    - Added `allow_desperate_scan` to merge logic to prevent heavy HDF5 scans 
      on missing objects.
Example:
    >>> store = HybridStorage("./hybrid_store")
    >>> obj_id = store.add(obj)  # obj carries .E and AtomPositionManager
    >>> meta = store.get_meta(obj_id)
    >>> payload = store.get(obj_id)
"""
from __future__ import annotations

import os
import json
import sqlite3
import pickle
import h5py
import numpy as np
import time
import sys
from tqdm import tqdm
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

from typing import Any, Dict, List, Optional, Sequence, Tuple, Iterable

from .backend import StorageBackend

class HybridStorage:
    """
    Hybrid backend:
      - SQLite: index + metadata (species registry, compositions, scalars)
      - HDF5:   payload pickled & compressed
    Guarantees:
      - Stable species-to-column mapping via `species.rank` (first-seen order).
      - Sparse compositions, dense export on request.
      - Generic scalar store (E, E1, E2, ...).
    """


    """Hybrid SQLite + HDF5 object store.

    The storage model separates **metadata** (SQLite) from **payloads** (HDF5):

    - *SQLite* stores: ``id``, ``energy``, ``natoms``, ``formula``, and a JSON
      blob ``meta_json`` (currently including the composition map). A second
      table, ``compositions(object_id, species, count)``, holds an EAV view of
      per-species counts to enable selective queries.
    - *HDF5* stores: one dataset per object under the group ``/objs`` named as
      zero-padded IDs (``00000001``, ...). Each dataset contains the raw pickled
      bytes and carries attributes for quick inspection (``id``, ``energy`` when
      available).

    Attributes:
        root_dir: Absolute path to the storage root directory.
        h5_path: File path to the HDF5 file (``db_objects.h5``).
        sqlite_path: File path to the SQLite index (``db_index.sqlite``).

    Forward-looking:
        The schema leaves room for additional indices (e.g., ranges over energy
        or natoms) and user-defined metadata; ``meta_json`` can be extended
        without schema migration.
    """
    # scalar keys we auto-pick if present as numeric attrs in SingleRun/APM
    _SCALAR_PREFIXES = ("E", "energy", "Etot", "Ef", "free_energy")

    def __init__(
        self,
        root_dir: str = "./hybrid_store",
        access: str = "rw",
        *,
        hdf5_shard_levels: int | None = None,
        hdf5_shard_digits: int = 2,
        auto_detect_shard: bool = True):
        """
        access: 'rw' (default) or 'ro'
        """
        if access not in ("rw", "ro"):
            raise ValueError("access must be 'rw' or 'ro'")
        self.read_only = (access == "ro")

        self.root_dir = os.path.abspath(root_dir)
        os.makedirs(self.root_dir, exist_ok=True)

        self.h5_path = os.path.join(self.root_dir, "db_objects.h5")
        self.sqlite_path = os.path.join(self.root_dir, "db_index.sqlite")

        # --- SQLite ---
        if self.read_only:
            # Read-only URI; do not mutate schema
            self._conn = sqlite3.connect(f"file:{self.sqlite_path}?mode=ro",
                                         uri=True, check_same_thread=False)
            self._conn.execute("PRAGMA foreign_keys = ON;")
        else:
            self._conn = sqlite3.connect(self.sqlite_path, check_same_thread=False)
            self._conn.execute("PRAGMA foreign_keys = ON;")
            self._init_schema()

        # --- HDF5 ---
        h5_mode = "r" if self.read_only else "a"
        self._h5 = h5py.File(self.h5_path, h5_mode)
        # Ensure the group exists in RW; in RO, require it to be present
        if self.read_only:
            if "objs" not in self._h5:
                raise RuntimeError("Read-only open requires existing 'objs' group in HDF5.")
            self._grp = self._h5["objs"]
        else:
            self._grp = self._h5.require_group("objs")

        # --- Sharding configuration (auto-detect if requested/unspecified) ---
        if hdf5_shard_levels is not None:
            self.hdf5_shard_levels = int(hdf5_shard_levels)
            self.hdf5_shard_digits = int(hdf5_shard_digits)
        elif auto_detect_shard:
            try:
                lvl, digs = self._detect_shard_layout(self._grp)
                self.hdf5_shard_levels = int(lvl)
                self.hdf5_shard_digits = int(digs)
            except Exception:
                # Safe default (flat)
                self.hdf5_shard_levels = 0
                self.hdf5_shard_digits = int(hdf5_shard_digits)
        else:
            # Default if not specified and detection disabled
            self.hdf5_shard_levels = 0
            self.hdf5_shard_digits = int(hdf5_shard_digits)

    # --- HDF5 shard path resolver ---
    def _resolve_h5_path(self, h5, obj_id, levels=2, digits=2):
        """
        Resolve (group, dataset_name) for a given object ID.
        Compatible with HybridStorage sharding logic used in merge_roots_recursive_attach().
        """
        dname = f"{int(obj_id):08d}"
        root = h5["objs"]

        # -------------------------------
        # Level 0: flat structure
        # -------------------------------
        if levels == 0:
            return root, dname

        # -------------------------------
        # Level 1: /objs/XX/########
        # -------------------------------
        if levels == 1:
            part1 = dname[-digits:]  # use trailing digits (same as _h5_bucket_for_id)
            if part1 in root:
                grp = root[part1]
                if dname in grp:
                    return grp, dname
            # fallback brute-force (tolerate legacy layouts)
            for k1, g1 in root.items():
                if isinstance(g1, h5py.Group) and dname in g1:
                    return g1, dname
            raise KeyError(f"Dataset {dname} not found under /objs level-1 sharding")

        # -------------------------------
        # Level 2: /objs/XX/YY/########
        # -------------------------------
        if levels == 2:
            part1 = dname[-digits:]                   # last 2 digits
            part2 = dname[-2*digits:-digits]          # previous 2 digits
            if part2 in root:
                g1 = root[part2]
                if part1 in g1:
                    return g1[part1], dname
            # fallback brute-force
            for k1, g1 in root.items():
                if isinstance(g1, h5py.Group):
                    for k2, g2 in g1.items():
                        if isinstance(g2, h5py.Group) and dname in g2:
                            return g2, dname
            raise KeyError(f"Dataset {dname} not found under /objs level-2 sharding")

        raise ValueError(f"Unsupported shard level: {levels}")


    @staticmethod
    def _detect_shard_layout(objs_group) -> tuple[int, int]:
        """
        Detect sharding by confirming actual DATASET presence, not just numeric groups.
        Returns (levels, digits) where digits = length of the shard folder names.

        Robustly detect sharding layout of /objs group.
        Returns (levels, digits)
          0 → /objs/00000001
          1 → /objs/01/00000001
          2 → /objs/01/23/00000001
        """
        import re
        if not isinstance(objs_group, h5py.Group):
            return (0, 2)

        shard_re = re.compile(r"^\d+$")
        lvl1 = [k for k in objs_group.keys() if shard_re.match(k)]
        if not lvl1:
            # No numeric subgroups -> flat
            return (0, 2)

        # Look for datasets directly under a first-level group → level 1
        for k1 in lvl1:
            g1 = objs_group[k1]
            if any(isinstance(v, h5py.Dataset) for v in g1.values()):
                return (1, len(k1))
            # Check second-level numeric subgroups; require datasets to declare level 2
            lvl2 = [k for k in g1.keys() if shard_re.match(k) and isinstance(g1[k], h5py.Group)]
            for k2 in lvl2:
                g2 = g1[k2]
                if any(isinstance(v, h5py.Dataset) for v in g2.values()):
                    return (2, len(k2))

        # Only numeric subgroups but no datasets found → treat as flat fallback
        return (0, len(lvl1[0]))

    # Guard for any mutating method
    def _assert_writable(self):
        if self.read_only:
            raise RuntimeError("HybridStorage is read-only; writing is not allowed.")

    # ---------------- Schema ----------------
    def _init_schema(self):
        cur = self._conn.cursor()
        # One atomic transaction for everything
        with self._conn:  # BEGIN; ... COMMIT; (or ROLLBACK on exception)
            # --- DDL ---
            cur.execute("""
                CREATE TABLE IF NOT EXISTS species (
                    species_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol     TEXT UNIQUE NOT NULL,
                    rank       INTEGER NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS objects (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    energy    REAL,
                    natoms    INTEGER,
                    formula   TEXT,
                    meta_json TEXT
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS compositions (
                    object_id  INTEGER NOT NULL,
                    species_id INTEGER NOT NULL,
                    count      REAL NOT NULL,
                    PRIMARY KEY (object_id, species_id),
                    FOREIGN KEY (object_id)  REFERENCES objects(id)  ON DELETE CASCADE,
                    FOREIGN KEY (species_id) REFERENCES species(species_id) ON DELETE RESTRICT
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS scalars (
                    object_id INTEGER NOT NULL,
                    key       TEXT    NOT NULL,
                    value     REAL,
                    PRIMARY KEY (object_id, key),
                    FOREIGN KEY (object_id) REFERENCES objects(id) ON DELETE CASCADE
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS object_hashes (
                    object_id INTEGER PRIMARY KEY,
                    hash      TEXT NOT NULL,
                    FOREIGN KEY (object_id) REFERENCES objects(id) ON DELETE CASCADE
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS metadata_kv (
                    object_id  INTEGER NOT NULL,
                    key        TEXT NOT NULL,
                    value_json TEXT NOT NULL,
                    PRIMARY KEY (object_id, key),
                    FOREIGN KEY (object_id) REFERENCES objects(id) ON DELETE CASCADE
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS lattice (
                    object_id INTEGER PRIMARY KEY,
                    a11 REAL, a12 REAL, a13 REAL,
                    a21 REAL, a22 REAL, a23 REAL,
                    a31 REAL, a32 REAL, a33 REAL,
                    FOREIGN KEY(object_id) REFERENCES objects(id) ON DELETE CASCADE
                );
            """)
            
            # --- Indexes ---
            cur.execute("CREATE INDEX IF NOT EXISTS idx_objects_energy     ON objects(energy);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_comp_sp            ON compositions(species_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_scalars_key        ON scalars(key);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_object_hashes_hash ON object_hashes(hash);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_metadata_kv_key ON metadata_kv(key);")

            # --- Backfill hashes from meta_json when missing ---
            cur.execute("""
                SELECT o.id, o.meta_json
                FROM objects o
                LEFT JOIN object_hashes h ON h.object_id = o.id
                WHERE h.object_id IS NULL;
            """)
            rows = cur.fetchall()
            to_insert = []
            for oid, meta_json in rows:
                if not meta_json:
                    continue
                try:
                    meta = json.loads(meta_json)
                except Exception:
                    continue
                h = None
                if isinstance(meta, dict):
                    h = meta.get("hash") or meta.get("content_hash") or meta.get("sha256")
                if isinstance(h, str) and h:
                    to_insert.append((int(oid), h))

            if to_insert:
                cur.executemany(
                    "INSERT OR IGNORE INTO object_hashes(object_id, hash) VALUES (?, ?);",
                    to_insert
                )

    # ---------------- Helpers ----------------
    @staticmethod
    def _to_float_or_none(x) -> Optional[float]:
        try:
            import numpy as _np
            if isinstance(x, _np.ndarray):
                if x.size == 0:
                    return None
                return float(x.reshape(-1)[0])
            if isinstance(x, (_np.floating, _np.integer)):
                return float(x)
        except Exception:
            pass
        if isinstance(x, (int, float)):
            return float(x)
        return None

    @staticmethod
    def _is_scalar(x) -> bool:
        try:
            import numpy as _np
            if isinstance(x, (int, float, _np.integer, _np.floating)):
                return True
            if isinstance(x, _np.ndarray) and x.ndim == 0:
                return True
        except Exception:
            pass
        return False

    @classmethod
    def merge_roots(
        cls,
        src_a: str,
        src_b: str,
        dst_root: str,
        *,
        dedup: str = "hash",   # "hash" | "payload" | "none"
        compact: bool = True
    ) -> dict:
        """
        Merge two HybridStorage databases (SQLite + HDF5) into a fresh destination.

        Args:
            src_a, src_b: Paths to the *root directories* of the two databases.
                          (If you pass a file path, its directory will be used.)
            dst_root: Path to a *new* root directory to create/populate.
            dedup:   - "hash": skip objects whose content hash already exists in the destination
                     - "payload": compute SHA256 of the pickled payload and skip duplicates
                     - "none": copy everything
            compact: If True, compact the destination HDF5 at the end.

        Returns:
            A small report dict with counts:
              {
                "added_from_a": int,
                "added_from_b": int,
                "skipped_duplicates": int,
                "total_in_dst": int,
                "dst_root": str,
                "dst_sqlite": str,
                "dst_h5": str
              }

        Notes:
            - Species ordering follows the combined first-seen order (all from A, then any new ones from B).
            - Hash-based dedup relies on `object_hashes.hash` or meta_json["hash"/"content_hash"/"sha256"].
              If you choose "payload", a SHA256 of the pickled object bytes is used instead.
            - This implementation re-adds objects using `add(obj)`, which (by design) re-derives scalars
              via `_extract_scalars`. If your source SQLite has extra ad-hoc scalars that are *not*
              present on the object itself, those will not carry over.
        """
        import hashlib
        
        def _normalize_root(p: str) -> str:
            p = os.path.abspath(p)
            if os.path.isdir(p):
                return p
            return os.path.dirname(p)

        # Normalize roots
        src_a = _normalize_root(src_a)
        src_b = _normalize_root(src_b)
        dst_root = os.path.abspath(dst_root)

        # Guard: destination must not already contain a database
        os.makedirs(dst_root, exist_ok=True)
        existing = set(os.listdir(dst_root))
        if {"db_index.sqlite", "db_objects.h5"} & existing:
            raise FileExistsError(
                f"Destination '{dst_root}' already contains a database; choose an empty directory."
            )

        # Helpers for dedup
        def _extract_src_hash_from_meta(meta: dict) -> Optional[str]:
            for k in ("hash", "content_hash", "sha256"):
                h = meta.get(k)
                if isinstance(h, str) and h:
                    return h
            return None

        def _payload_sha256(obj) -> str:
            blob = pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
            return hashlib.sha256(blob).hexdigest()

        # Open storages
        srcA = cls(src_a, access="ro")
        srcB = cls(src_b, access="ro")
        dst  = cls(dst_root, access="rw")

        # Local dedup registries to reduce DB chatter
        seen_hashes = set(dst.get_all_hashes()) if dedup in ("hash",) else set()
        seen_payloads = set() if dedup == "payload" else set()

        skipped = 0
        added_a = 0
        added_b = 0

        def _copy_all(src: "HybridStorage") -> int:
            nonlocal skipped, seen_hashes, seen_payloads
            added_here = 0

            for oid, obj in src.iter_objects(batch_size=1000):
                # Prefer fast dedup before any writes
                meta = src.get_meta(oid)  # merged dict: includes meta_json pieces
                h = _extract_src_hash_from_meta(meta)

                # Decide if duplicate
                is_dup = False
                if dedup == "hash":
                    if isinstance(h, str) and (h in seen_hashes or dst.has_hash(h)):
                        is_dup = True
                elif dedup == "payload":
                    ph = _payload_sha256(obj)
                    if ph in seen_payloads:
                        is_dup = True
                # dedup == "none" => never duplicate

                if is_dup:
                    skipped += 1
                    continue

                # Insert object using public API to ensure consistency
                new_id = dst.add(obj)

                # Keep dedup registries up to date
                if dedup == "hash":
                    if isinstance(h, str) and h:
                        # ensure object_hashes + meta_json carry the hash for future robustness
                        dst._conn.execute(
                            "INSERT OR REPLACE INTO object_hashes(object_id, hash) VALUES (?,?);",
                            (new_id, h)
                        )
                        try:
                            cur = dst._conn.cursor()
                            cur.execute("SELECT meta_json FROM objects WHERE id=?;", (new_id,))
                            row = cur.fetchone()
                            mjson = row[0] if row else None
                            payload = json.loads(mjson) if mjson else {}
                            if "hash" not in payload:
                                payload["hash"] = h
                                cur.execute(
                                    "UPDATE objects SET meta_json=? WHERE id=?;",
                                    (json.dumps(payload), new_id)
                                )
                            dst._conn.commit()
                        except Exception:
                            # Non-fatal: hash is already in object_hashes
                            pass
                        seen_hashes.add(h)

                elif dedup == "payload":
                    ph = _payload_sha256(obj)
                    seen_payloads.add(ph)

                # Optionally backfill free_energy from source meta_json if not extracted via add()
                try:
                    src_F = meta.get("free_energy", None)
                    if src_F is not None:
                        cur = dst._conn.cursor()
                        cur.execute("SELECT meta_json FROM objects WHERE id=?;", (new_id,))
                        row = cur.fetchone()
                        mjson = row[0] if row else None
                        payload = json.loads(mjson) if mjson else {}
                        if "free_energy" not in payload:
                            payload["free_energy"] = float(src_F)
                            cur.execute(
                                "UPDATE objects SET meta_json=? WHERE id=?;",
                                (json.dumps(payload), new_id)
                            )
                            dst._conn.commit()
                except Exception:
                    # Non-fatal metadata improvement
                    pass

                added_here += 1

            return added_here

        try:
            added_a = _copy_all(srcA)
            added_b = _copy_all(srcB)

            # Optional compaction to defragment HDF5
            if compact:
                try:
                    dst.compact_hdf5()
                except Exception:
                    # Compaction failures should not invalidate the merge
                    pass

            report = {
                "added_from_a": int(added_a),
                "added_from_b": int(added_b),
                "skipped_duplicates": int(skipped),
                "total_in_dst": int(dst.count()),
                "dst_root": dst_root,
                "dst_sqlite": dst.sqlite_path,
                "dst_h5": dst.h5_path,
            }
            return report

        finally:
            # Be diligent about closing file handles
            try:
                srcA.close()
            except Exception:
                pass
            try:
                srcB.close()
            except Exception:
                pass
            try:
                dst.close()
            except Exception:
                pass

    @classmethod
    def merge_roots_recursive(
        cls,
        root_dir: str,
        *,
        dst_root: Optional[str] = None,
        dedup: str = "hash",           # "hash" | "payload" | "none"
        compact: bool = True,
        progress_every: int = 1000,
        quiet: bool = False,
        chunk_size: int = 10000,
        commit_every: int = 8,         # chunks per extra safety commit
        parallel_h5: int = 4,          # threads for dataset copy
        prefer_largest: bool = True,   # pick the largest DB as base when dst_root is None
        reuse_existing_dst: bool = True,  # if dst_root points to an existing DB, append into it
    ) -> dict:
        """
        Incremental, size-aware merger for HybridStorage roots.

        Key behavior:
          - If `dst_root` is None and `prefer_largest=True`, the largest discovered DB is chosen
            as the destination and opened in RW; all others are merged into it (no rebuild).
          - If `dst_root` points to an existing HybridStorage DB and `reuse_existing_dst=True`,
            the function appends into it directly.
          - Remaining sources are processed in **decreasing size** order to maximize throughput.
          - Dedup is done via a temporary table joined against destination `object_hashes`.
          - Hash extraction avoids JSON parsing (regex fast path), with a fallback to source
            `get_all_hashes(with_ids=True)` when available.

        Returns:
          A JSON-serializable report dict.
        """
        import os, glob, re, json, sqlite3, hashlib, h5py, numpy as np
        from datetime import datetime
        from concurrent.futures import ThreadPoolExecutor

        assert dedup in ("hash", "payload", "none")
        root_dir = os.path.abspath(root_dir)

        # ---------- discover candidate hybrid roots ----------
        def _is_hybrid_root(d: str) -> bool:
            return (
                os.path.isfile(os.path.join(d, "db_index.sqlite")) and
                os.path.isfile(os.path.join(d, "db_objects.h5"))
            )

        sources: List[str] = []
        if any(ch in root_dir for ch in "*?[]"):
            for p in glob.glob(root_dir, recursive=True):
                if os.path.isdir(p) and _is_hybrid_root(p):
                    sources.append(os.path.abspath(p))
        else:
            for dirpath, _, _ in os.walk(root_dir):
                if _is_hybrid_root(dirpath):
                    sources.append(os.path.abspath(dirpath))

        sources = sorted(set(sources))
        if not sources:
            raise FileNotFoundError(f"No hybrid roots found under {root_dir!r}")

        # ---------- helpers ----------
        _hash_re = re.compile(r'"(?:hash|sha256|content_hash)"\s*:\s*"([a-fA-F0-9]{32,64})"')

        def fast_extract_hash(mjson: Optional[str]) -> Optional[str]:
            if not mjson or ('hash' not in mjson and 'sha256' not in mjson and 'content_hash' not in mjson):
                return None
            m = _hash_re.search(mjson)
            return m.group(1) if m else None

        def sha256_ds(ds) -> str:
            """Compute SHA256 over a 1D uint8 dataset without materializing fully."""
            m = hashlib.sha256()
            buf = np.empty((1_000_000,), dtype=np.uint8)
            total = int(ds.size)
            off = 0
            while off < total:
                n = min(1_000_000, total - off)
                ds.read_direct(buf[:n], np.s_[off:off+n])
                m.update(memoryview(buf[:n]))
                off += n
            return m.hexdigest()

        def _chunked(lst, n=900):
            for i in range(0, len(lst), n):
                yield lst[i:i+n]

        def _ensure_species_bulk(con: sqlite3.Connection, symbols: Iterable[str]) -> Dict[str, int]:
            """Ensure all symbols exist in `species`; return {symbol -> species_id}."""
            symbols = [s for s in set(map(str, symbols)) if s]
            if not symbols:
                return {}
            cur = con.cursor()
            q = "SELECT symbol, species_id FROM species WHERE symbol IN (%s);" % ",".join("?" for _ in symbols)
            cur.execute(q, symbols)
            mapping = {sym: int(spid) for sym, spid in cur.fetchall()}
            missing = [s for s in symbols if s not in mapping]
            if missing:
                cur.execute("SELECT COALESCE(MAX(rank), -1) FROM species;")
                start_rank = int(cur.fetchone()[0]) + 1
                cur.executemany("INSERT INTO species(symbol, rank) VALUES (?, ?);",
                                [(s, start_rank + i) for i, s in enumerate(missing)])
                con.commit()
                cur.execute(q, symbols)
                mapping.update({sym: int(spid) for sym, spid in cur.fetchall()})
            return mapping

        def copy_ds_batch(src_h5: h5py.File, dst_h5: h5py.File, mapping: Dict[int, int], parallel=4):
            """Copy many datasets by id mapping {src_oid -> dst_oid}."""
            if not mapping:
                return
            dst_grp = dst_h5.require_group("objs")
            def _copy_one(oid, nid):
                sname = f"objs/{int(oid):08d}"
                dname = f"{int(nid):08d}"
                try:
                    # shallow=True (HDF5 ≥1.12 + h5py ≥3.3); fallback if unsupported
                    src_h5.copy(sname, dst_grp, name=dname, shallow=True)
                except TypeError:
                    src_h5.copy(sname, dst_grp, name=dname)

            if parallel and parallel > 1:
                with ThreadPoolExecutor(max_workers=parallel) as ex:
                    futs = [ex.submit(_copy_one, oid, nid) for oid, nid in mapping.items()]
                    for f in futs:
                        # Surface any errors
                        f.result()
            else:
                for oid, nid in mapping.items():
                    _copy_one(oid, nid)
            dst_h5.flush()

        def _estimate_size(root: str) -> Tuple[int, int]:
            """
            Return a tuple (n_objects, approx_bytes) to rank databases.
            Primary key is row count in `objects`; fallback to file size.
            """
            sql = os.path.join(root, "db_index.sqlite")
            h5  = os.path.join(root, "db_objects.h5")
            n = -1
            try:
                con = sqlite3.connect(f"file:{sql}?mode=ro", uri=True)
                cur = con.execute("SELECT COUNT(*) FROM objects;")
                n = int(cur.fetchone()[0])
                con.close()
            except Exception:
                pass
            approx_size = 0
            for p in (sql, h5):
                try:
                    approx_size += os.path.getsize(p)
                except Exception:
                    pass
            return (n if n >= 0 else 0, approx_size)

        def _ensure_no_txn(con: sqlite3.Connection):
            if con.in_transaction:
                con.commit()

        # ---------- choose destination ----------
        existing_dst = None
        if dst_root:
            dst_root = os.path.abspath(dst_root)
            is_hybrid = _is_hybrid_root(dst_root)
            if is_hybrid and reuse_existing_dst:
                existing_dst = dst_root
                # Remove from sources to avoid self-merge
                sources = [s for s in sources if os.path.abspath(s) != existing_dst]
                if not quiet:
                    print(f"[merge-fast] Using provided existing DB as destination: {existing_dst}")
            else:
                # If provided dst_root is empty/non-DB, we could clone the largest DB into it first,
                # but per request we focus on reusing an existing DB or picking the largest.
                raise FileExistsError(
                    f"dst_root '{dst_root}' is not an existing HybridStorage DB. "
                    f"Provide an existing DB or omit dst_root."
                )

        if existing_dst is None:
            if prefer_largest:
                # Order by size descending; pick the largest as destination
                ranked = sorted(sources, key=lambda r: _estimate_size(r), reverse=True)
                existing_dst = ranked[0]
                sources = ranked[1:]
                if not quiet:
                    n, sz = _estimate_size(existing_dst)
                    print(f"[merge-fast] Selected largest DB as destination: {existing_dst}  "
                          f"(objects={n}, size~{sz/1e9:.2f} GB)")
            else:
                # Fallback legacy behavior (not recommended here)
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_dst = os.path.join(root_dir, f"_merged_{ts}")
                raise RuntimeError(
                    f"prefer_largest=False leads to fresh-build, which you wanted to avoid. "
                    f"Either set prefer_largest=True or supply an existing dst_root. "
                    f"(Suggested new_dst would have been: {new_dst})"
                )

        # Re-rank remaining sources by size (descending) for best locality and fewer species churns
        sources = sorted(sources, key=lambda r: _estimate_size(r), reverse=True)

        # ---------- open destination in RW ----------
        dst = cls(existing_dst, access="rw")
        con = dst._conn
        con.execute("PRAGMA journal_mode=WAL;")
        con.execute("PRAGMA synchronous=OFF;")
        con.execute("PRAGMA temp_store=MEMORY;")
        con.execute("PRAGMA cache_size=-200000;")
        con.execute("PRAGMA cache_spill=OFF;")
        con.execute("PRAGMA foreign_keys=OFF;")
        _ensure_no_txn(con)

        total_scanned = total_added = total_skipped = 0
        chunks_since_commit = 0

        # ---------- main merge loop over sources (desc size) ----------
        for si, src_root in enumerate(sources, 1):
            try:
                src = cls(src_root, access="ro")
            except Exception as e:
                if not quiet:
                    print(f"[{si}/{len(sources)}] Skip {src_root} (open error: {e})")
                continue

            if not quiet:
                n_src, sz_src = _estimate_size(src_root)
                print(f"[{si}/{len(sources)}] Merging: {src_root}  (objects={n_src}, size~{sz_src/1e9:.2f} GB)")

            # Optional fast id->hash map from source (when available)
            id2hash: Dict[int, Optional[str]] = {}
            if dedup in ("hash", "payload"):
                try:
                    pairs = src.get_all_hashes(with_ids=True)  # [(id, hash_str)]
                    id2hash = {int(oid): (h if isinstance(h, str) and h else None) for oid, h in pairs}
                except Exception:
                    id2hash = {}

            cur_s = src._conn.cursor()
            cur_s.execute("SELECT id, energy, natoms, formula, meta_json FROM objects ORDER BY id ASC;")

            while True:
                rows = cur_s.fetchmany(chunk_size)
                if not rows:
                    break
                total_scanned += len(rows)

                # -------- pre-extract hashes (avoid JSON loads) --------
                pre: List[Tuple[int, Any, Any, Any, Optional[str]]] = []  # (oid, energy, natoms, formula, hash)
                for oid, energy, natoms, formula, meta_json in rows:
                    h = None
                    if dedup == "hash":
                        h = id2hash.get(int(oid))
                        if not h:
                            h = fast_extract_hash(meta_json)
                    elif dedup == "payload":
                        # Compute SHA over raw pickled bytes in HDF5
                        ds = src._h5["objs"][f"{int(oid):08d}"]
                        h = sha256_ds(ds)
                    pre.append((int(oid), energy, natoms, formula, h))

                # -------- dedup against destination via temp table --------
                if dedup == "none":
                    present: set[str] = set()
                else:
                    chunk_hashes = [h for *_, h in pre if h]
                    if chunk_hashes:
                        _ensure_no_txn(con)  # CREATE TEMP TABLE starts an implicit txn; close it
                        con.execute("CREATE TEMP TABLE IF NOT EXISTS tmp_hashes(hash TEXT PRIMARY KEY);")
                        # Clear previous content if it exists
                        con.execute("DELETE FROM tmp_hashes;")
                        con.executemany("INSERT OR IGNORE INTO tmp_hashes(hash) VALUES (?);", [(h,) for h in chunk_hashes])
                        cur_tmp = con.cursor()
                        cur_tmp.execute("SELECT t.hash FROM tmp_hashes t JOIN object_hashes o ON o.hash=t.hash;")
                        present = {h for (h,) in cur_tmp.fetchall()}
                        _ensure_no_txn(con)  # end the implicit txn before BEGIN IMMEDIATE
                    else:
                        present = set()

                # Filter to-be-inserted (avoid dups both in dst and within this chunk)
                to_insert: List[Tuple[int, Any, Any, Any, Optional[str]]] = []
                local_dups: set[str] = set()
                for (oid, energy, natoms, formula, h) in pre:
                    if dedup != "none" and h:
                        if (h in present) or (h in local_dups):
                            total_skipped += 1
                            continue
                        local_dups.add(h)
                    to_insert.append((oid, energy, natoms, formula, h))

                if not to_insert:
                    if (not quiet) and (total_scanned % progress_every == 0):
                        print(f"  ... scanned={total_scanned}, added={total_added}, skipped={total_skipped}")
                    continue

                src_oids = [oid for (oid, *_rest) in to_insert]

                # -------- gather compositions and scalars in batches --------
                comp_rows_all: List[Tuple[int, str, float]] = []  # (oid, symbol, count)
                for sub in _chunked(src_oids):
                    q = "SELECT c.object_id, s.symbol, c.count FROM compositions c JOIN species s ON s.species_id=c.species_id WHERE c.object_id IN (%s);" % \
                        ",".join("?" for _ in sub)
                    cur_c = src._conn.cursor()
                    cur_c.execute(q, sub)
                    comp_rows_all.extend([(int(oid), str(sym), float(ct)) for oid, sym, ct in cur_c.fetchall()])

                scalar_rows_all: List[Tuple[int, str, float]] = []  # (oid, key, value)
                for sub in _chunked(src_oids):
                    q = "SELECT object_id, key, value FROM scalars WHERE object_id IN (%s);" % ",".join("?" for _ in sub)
                    cur_v = src._conn.cursor()
                    cur_v.execute(q, sub)
                    scalar_rows_all.extend([(int(oid), str(k), (float(v) if v is not None else np.nan))
                                            for oid, k, v in cur_v.fetchall()])

                # -------- insert into destination (single txn) --------
                _ensure_no_txn(con)
                con.execute("BEGIN IMMEDIATE;")
                cur_d = con.cursor()

                # Ensure all needed species exist (one-shot)
                symbols = {sym for (_oid, sym, _ct) in comp_rows_all}
                sym2id = _ensure_species_bulk(con, symbols) if symbols else {}

                new_ids: Dict[int, int] = {}
                # Insert objects + object_hashes (store h if available)
                for oid, energy, natoms, formula, h in to_insert:
                    # Guarantee hash presence in meta_json for robustness (only if we have it)
                    meta_json = None
                    if h:
                        try:
                            # Pull current meta_json to append the hash; we don't have it here without a load,
                            # so we just create a minimal payload
                            meta_json = json.dumps({"hash": h})
                        except Exception:
                            meta_json = json.dumps({"hash": h})
                    cur_d.execute(
                        "INSERT INTO objects (energy, natoms, formula, meta_json) VALUES (?,?,?,?);",
                        (energy, natoms, formula, meta_json)
                    )
                    nid = int(cur_d.lastrowid)
                    new_ids[oid] = nid
                    if h:
                        cur_d.execute("INSERT OR REPLACE INTO object_hashes(object_id, hash) VALUES (?,?);", (nid, h))

                # compositions → dst
                if comp_rows_all:
                    cur_d.executemany(
                        "INSERT INTO compositions(object_id, species_id, count) VALUES (?,?,?);",
                        [(new_ids[oid], sym2id[sym], float(ct))
                         for oid, sym, ct in comp_rows_all if oid in new_ids and sym in sym2id]
                    )

                # scalars → dst
                if scalar_rows_all:
                    cur_d.executemany(
                        "INSERT INTO scalars(object_id, key, value) VALUES (?,?,?);",
                        [(new_ids[oid], k, float(v) if v is not None else np.nan)
                         for oid, k, v in scalar_rows_all if oid in new_ids]
                    )

                con.commit()  # end INSERT txn

                # -------- HDF5 copy for this chunk (outside SQL txn) --------
                try:
                    copy_ds_batch(src._h5, dst._h5, new_ids, parallel=parallel_h5)
                except Exception as e:
                    # Non-fatal; keep going, but surface the error
                    print(f"[merge-fast] Warning: HDF5 copy failed for {len(new_ids)} items: {e}")

                total_added += len(new_ids)
                chunks_since_commit += 1

                # Extra periodic commit safeguard (no-op if nothing pending)
                if chunks_since_commit >= commit_every:
                    _ensure_no_txn(con)
                    chunks_since_commit = 0

                if (not quiet) and (total_scanned % progress_every == 0):
                    print(f"  ... scanned={total_scanned}, added={total_added}, skipped={total_skipped}")

            # close source
            try:
                src.close()
            except Exception:
                pass

        # ---------- finalize destination ----------
        con.execute("PRAGMA foreign_keys=ON;")
        if compact:
            try:
                dst.compact_hdf5()
                if not quiet:
                    print("[merge-fast] HDF5 compacted.")
            except Exception as e:
                if not quiet:
                    print(f"[merge-fast] HDF5 compaction skipped (non-fatal): {e}")

        # Integrity check (best-effort)
        try:
            res = con.execute("PRAGMA integrity_check;").fetchone()
            if res and res[0] != "ok":
                print(f"[merge-fast] WARNING: integrity check: {res}")
        except Exception as e:
            if not quiet:
                print(f"[merge-fast] integrity_check failed: {e}")

        report = {
            "destination": existing_dst,
            "sources_merged": len(sources),
            "objects_scanned": int(total_scanned),
            "objects_added": int(total_added),
            "duplicates_skipped": int(total_skipped),
            "dst_sqlite": dst.sqlite_path,
            "dst_h5": dst.h5_path,
        }

        if not quiet:
            print(json.dumps(report, indent=2))

        # close destination
        try:
            dst.close()
        except Exception:
            pass

        return report

    @classmethod
    def merge_roots_recursive_attach(
        cls,
        root_dir: str,
        *,
        dst_root: Optional[str] = None,
        dedup: str = "hash",          # "hash" or "none"
        compact: bool = True,
        quiet: bool = False,
        chunk_size: int = 20000,
        parallel_hdf5: int = 8,       # only used if HDF5 build is thread-safe

        # --- HDF5 performance knobs ---
        hdf5_shard_levels: int = 1,   # 0 = flat /objs, 1 = /objs/XX, 2 = /objs/XX/YY
        hdf5_shard_digits: int = 2,   # digits per level (base-10)
        flush_every_chunks: int = 10, # flush HDF5 every N chunks instead of each chunk

        # --- SQL performance knobs ---
        wal_checkpoint_every: int = 50,  # run WAL checkpoint every N chunks

        # --- Robustness Options ---
        allow_desperate_scan: bool = False
    )-> Dict[str, Any]:
        """
        Recursively finds and merges HybridStorage databases into a single destination.

        This method uses a high-performance, chunked strategy with robust error handling.
        It isolates object failures to prevent entire chunks from failing.

        Args:
            root_dir (str): The root directory to search for source databases.
            dst_root (str, optional): Destination directory. If None, creates a new one.
            dedup (str): Deduplication strategy ("hash" or "none").
            compact (bool): Whether to repack the HDF5 file upon completion.
            quiet (bool): Suppress stdout progress messages.
            chunk_size (int): Number of objects to process per SQL transaction.
            parallel_hdf5 (int): Number of threads for HDF5 copy. 
                                 **Recommendation: 1** for maximum stability.
            hdf5_shard_levels (int): Sharding depth for the destination HDF5.
            hdf5_shard_digits (int): Digits per shard folder.
            flush_every_chunks (int): Frequency of HDF5 flushes to disk.
            wal_checkpoint_every (int): Frequency of SQLite WAL truncation (prevents disk bloat).
            allow_desperate_scan (bool): 
                If False (default), missing HDF5 datasets cause an immediate skip (0ms overhead).
                If True, triggers a brute-force file scan (~60s overhead) for missing items.
                **Warning:** True may cause deadlocks in multi-threaded environments.

        Returns:
            Dict[str, Any]: A summary report of the merge operation.
        """
        import os, glob, json, sqlite3, time
        from datetime import datetime

        def _fmt_t(secs: float) -> str:
            secs = max(0.0, float(secs))
            h = int(secs // 3600)
            m = int((secs % 3600) // 60)
            s = int(secs % 60)
            return f"{h:02d}:{m:02d}:{s:02d}"

        # --- discovery helpers ---
        def _is_hybrid_root(d: str) -> bool:
            return (
                os.path.isfile(os.path.join(d, "db_index.sqlite")) and
                os.path.isfile(os.path.join(d, "db_objects.h5"))
            )

        assert dedup in ("hash", "none")
        assert hdf5_shard_levels in (0, 1, 2), "Supported shard levels: 0, 1, 2"
        assert hdf5_shard_digits >= 1, "Shard digits must be >= 1"

        root_dir = os.path.abspath(root_dir)

        # --- 1. Source Discovery --- #
        # --- discover sources (supports glob patterns) ---
        sources = []
        if any(ch in root_dir for ch in "*?[]"):
            for p in glob.glob(root_dir, recursive=True):
                if os.path.isdir(p) and _is_hybrid_root(p):
                    sources.append(os.path.abspath(p))
        else:
            for dirpath, _, _ in os.walk(root_dir):
                if _is_hybrid_root(dirpath):
                    sources.append(os.path.abspath(dirpath))

        sources = sorted(set(sources))
        if not sources:
            raise FileNotFoundError(f"No hybrid databases found under: {root_dir}")

        # --- prepare destination root ---
        if dst_root is None:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            dst_root = os.path.join(root_dir, f"_merged_{ts}")
        dst_root = os.path.abspath(dst_root)
        os.makedirs(dst_root, exist_ok=True)

        existing = set(os.listdir(dst_root))
        if {"db_index.sqlite", "db_objects.h5"} & existing:
            raise FileExistsError(
                f"Destination '{dst_root}' already contains a database; choose an empty directory."
            )

        # --- open destination ---
        dst = cls(dst_root, access="rw")
        overall_t0 = time.perf_counter()
        chunks_done = 0
        chunks_since_flush = 0

        # small timer helpers for debugging hotspots
        def _t():
            return time.perf_counter()

        try:
            con = dst._conn
            # SQLite performance PRAGMAs
            con.execute("PRAGMA journal_mode=WAL;")
            con.execute("PRAGMA synchronous=OFF;")
            con.execute("PRAGMA temp_store=MEMORY;")
            con.execute("PRAGMA cache_size=-200000;")  # ~200MB
            con.execute("PRAGMA foreign_keys=OFF;")
            con.execute("PRAGMA locking_mode=EXCLUSIVE;")

            # --- snapshot and drop secondary indices (recreate later) ---
            idx_rows = con.execute("""
                SELECT name, tbl_name, sql
                FROM sqlite_master
                WHERE type='index'
                  AND sql IS NOT NULL
                  AND tbl_name IN ('objects','object_hashes','compositions','scalars');
            """).fetchall()
            recreate_idx_sql = [row[2] for row in idx_rows if row[2]]
            for name, _tbl, _sql in idx_rows:
                try:
                    con.execute(f'DROP INDEX IF EXISTS "{name}";')
                except Exception:
                    pass

            # --- load existing hashes for dedup ---
            existing_hashes = set()
            if dedup == "hash":
                try:
                    cur = con.execute("SELECT hash FROM object_hashes;")
                    batch = cur.fetchmany(100_000)
                    while batch:
                        for (h,) in batch:
                            if h:
                                existing_hashes.add(h)
                        batch = cur.fetchmany(100_000)
                except Exception:
                    existing_hashes = set()

            # --- HDF5 thread-safety probe ---
            try:
                import h5py
                _cfg = getattr(getattr(h5py, "h5", None), "get_config", lambda: None)()
                hdf5_threadsafe = bool(getattr(_cfg, "threadsafe", False))
            except Exception:
                hdf5_threadsafe = False

            # --- HDF5: ensure root group and sharded layout ---
            # If the root "objs" doesn't exist, create it with track_order to improve metadata behavior.
            if "objs" not in dst._h5:
                try:
                    dst._h5.create_group("objs", track_order=True)
                except TypeError:
                    # older h5py may not support track_order kw
                    dst._h5.create_group("objs")
            dst_root_grp = dst._h5["objs"]

            # Cache for bucket groups to avoid repeated require_group calls
            _bucket_cache = {}

            def _h5_bucket_for_id(did: int):
                """Return (group, dname) for destination id with decimal sharding."""
                dname = f"{int(did):08d}"
                if hdf5_shard_levels == 0:
                    return dst_root_grp, dname

                # Build path parts using last digits of the numeric id
                path_parts = []
                digits_available = dname  # since dname is zero-padded
                take = hdf5_shard_digits
                # Use trailing digits for uniform distribution across sequential IDs
                start = len(digits_available) - hdf5_shard_digits
                part1 = digits_available[start:]
                path_parts.append(part1)

                if hdf5_shard_levels == 2:
                    start2 = len(digits_available) - 2*hdf5_shard_digits
                    part2 = digits_available[start2:start]
                    path_parts.insert(0, part2)

                key = "/".join(path_parts)
                grp = _bucket_cache.get(key)
                if grp is None:
                    # create hierarchy under /objs
                    cur = dst_root_grp
                    for p in path_parts:
                        k = (cur.name, p)
                        maybe = _bucket_cache.get(k)
                        if maybe is not None:
                            cur = maybe
                            continue
                        cur = cur.require_group(p)
                        _bucket_cache[k] = cur
                    _bucket_cache[key] = cur
                    grp = cur
                return grp, dname

            total_added = 0
            total_skipped = 0
            sources_ok = []
            sources_fail = []
            missing_payloads = 0 

            # --- per-source merge (chunked) ---
            for si, src_root in enumerate(sources, start=1):
                src_t0 = _t()
                source_added = 0
                source_skipped = 0

                try:
                    if not quiet:
                        print(f"[{si}/{len(sources)}] Begin: {src_root}")

                    src = cls(src_root, access="ro")
                    try:
                        con.execute("ATTACH DATABASE ? AS src;", (src.sqlite_path,))

                        (src_max_id,) = con.execute("SELECT MAX(id) FROM src.objects;").fetchone()
                        if src_max_id is None:
                            con.execute("DETACH DATABASE src;")
                            src.close()
                            sources_ok.append(src_root)
                            if not quiet:
                                print(f"[{si}/{len(sources)}] Empty DB, skipped. Total elapsed {_fmt_t(_t()-overall_t0)}")
                            continue

                        last_id = 0
                        while last_id < src_max_id:
                            t_chunk0 = _t()

                            # ---- SQL phase ----
                            con.execute("BEGIN;")
                            rows = con.execute("""
                                SELECT o.id AS src_oid, o.energy, o.natoms, o.formula, o.meta_json, h.hash
                                FROM src.objects o
                                LEFT JOIN src.object_hashes h ON h.object_id = o.id
                                WHERE o.id > ?
                                ORDER BY o.id
                                LIMIT ?;
                            """, (last_id, int(chunk_size))).fetchall()

                            if not rows:
                                con.commit()
                                break

                            last_id = rows[-1][0]

                            # In-memory dedup (keep NULL hashes)
                            if dedup == "hash":
                                stage = [r for r in rows if (r[5] is None) or (r[5] not in existing_hashes)]
                                skipped = len(rows) - len(stage)
                                source_skipped += skipped
                                total_skipped += skipped
                            else:
                                stage = rows

                            if not stage:
                                con.commit()
                                # WAL checkpoint periodically (even if empty stage)
                                chunks_done += 1
                                if wal_checkpoint_every and (chunks_done % wal_checkpoint_every == 0):
                                    try:
                                        con.execute("PRAGMA wal_checkpoint(TRUNCATE);")
                                    except Exception:
                                        pass
                                continue

                            # Stage payload in TEMP table (keeps mapping in order)
                            con.execute("DROP TABLE IF EXISTS temp.t_stage_objects;")
                            con.execute("""
                                CREATE TEMP TABLE t_stage_objects (
                                    energy    REAL,
                                    natoms    INTEGER,
                                    formula   TEXT,
                                    meta_json TEXT,
                                    hash      TEXT,
                                    src_oid   INTEGER
                                );
                            """)

                            payload = []
                            for src_oid, energy, natoms, formula, meta_json, h in stage:
                                mj = meta_json
                                try:
                                    if h and (not mj or "hash" not in mj):
                                        d = json.loads(mj) if mj else {}
                                        if not isinstance(d, dict):
                                            d = {}
                                        if "hash" not in d:
                                            d["hash"] = h
                                        mj = json.dumps(d)
                                except Exception:
                                    pass
                                payload.append((energy, natoms, formula, mj, h, int(src_oid)))

                            con.executemany("""
                                INSERT INTO t_stage_objects(energy, natoms, formula, meta_json, hash, src_oid)
                                VALUES (?, ?, ?, ?, ?, ?);
                            """, payload)

                            use_returning = True
                            try:
                                cur = con.execute("""
                                    INSERT INTO objects (energy, natoms, formula, meta_json)
                                    SELECT energy, natoms, formula, meta_json
                                    FROM t_stage_objects
                                    ORDER BY src_oid
                                    RETURNING id;
                                """)
                                new_ids = [row[0] for row in cur.fetchall()]
                            except sqlite3.OperationalError:
                                use_returning = False
                                (max_id_after,) = con.execute("SELECT MAX(id) FROM objects;").fetchone()
                                n_new = con.execute("SELECT COUNT(*) FROM t_stage_objects;").fetchone()[0]
                                new_ids = list(range(max_id_after - n_new + 1, max_id_after + 1)) if max_id_after and n_new else []

                            src_oids = [r[0] for r in con.execute(
                                "SELECT src_oid FROM t_stage_objects ORDER BY src_oid;"
                            ).fetchall()]
                            mapping = dict(zip(src_oids, new_ids))

                            # Insert hashes and update dedup set
                            hash_rows = [(mapping[soid], h) for (soid, _e, _n, _f, _mj, h) in stage if h]
                            if hash_rows:
                                con.executemany(
                                    "INSERT INTO object_hashes(object_id, hash) VALUES (?, ?);",
                                    hash_rows
                                )
                                if dedup == "hash":
                                    for _, h in hash_rows:
                                        existing_hashes.add(h)

                            # Species + compositions
                            sym_rows = con.execute("""
                                SELECT DISTINCT s.symbol
                                FROM src.compositions c 
                                JOIN src.species s ON s.species_id = c.species_id
                                WHERE c.object_id IN (SELECT src_oid FROM t_stage_objects);
                            """).fetchall()
                            sym2id = {}
                            if sym_rows:
                                symbols = [str(sym) for (sym,) in sym_rows]
                                sym2id = dst._ensure_species_bulk(symbols)

                                comp_rows = con.execute("""
                                    SELECT c.object_id, s.symbol, c.count
                                    FROM src.compositions c 
                                    JOIN src.species s ON s.species_id = c.species_id
                                    WHERE c.object_id IN (SELECT src_oid FROM t_stage_objects);
                                """).fetchall()
                                if comp_rows:
                                    con.executemany("""
                                        INSERT INTO compositions(object_id, species_id, count)
                                        VALUES (?, ?, ?);
                                    """, [
                                        (mapping[int(oid)], sym2id[str(sym)], float(ct))
                                        for (oid, sym, ct) in comp_rows
                                        if int(oid) in mapping
                                    ])

                            # Scalars
                            sc_rows = con.execute("""
                                SELECT object_id, key, value 
                                FROM src.scalars
                                WHERE object_id IN (SELECT src_oid FROM t_stage_objects);
                            """).fetchall()
                            if sc_rows:
                                con.executemany("""
                                    INSERT INTO scalars(object_id, key, value) VALUES (?, ?, ?);
                                """, [
                                    (mapping[int(oid)], str(k), float(v) if v is not None else None)
                                    for (oid, k, v) in sc_rows
                                    if int(oid) in mapping
                                ])

                            con.commit()
                            t_sql = _t() - t_chunk0

                            # ---- HDF5 phase (adaptive fast sharding resolver) ----
                            t_h5_0 = _t()

                            # Build a fast resolver based on the source sharding
                            def make_fast_resolver(levels, digits):
                                # Level-0 : /objs/<id>
                                if levels == 0:
                                    def fast(h5, obj_id):
                                        s = f"{obj_id:08d}"
                                        grp = h5["objs"]
                                        return grp, s
                                    return fast

                                # Level-1 : /objs/XX/<id>
                                if levels == 1:
                                    def fast(h5, obj_id):
                                        s = f"{obj_id:08d}"
                                        part1 = s[-digits:]
                                        grp = h5["objs"][part1]
                                        return grp, s
                                    return fast

                                # Level-2 : /objs/XX/YY/<id>
                                if levels == 2:
                                    def fast(h5, obj_id):
                                        s = f"{obj_id:08d}"
                                        part1 = s[-digits:]
                                        part2 = s[-2*digits:-digits]
                                        grp = h5["objs"][part2][part1]
                                        return grp, s
                                    return fast

                                # fallback universal slow path
                                def slow(h5, obj_id):
                                    grp, dname = src._resolve_h5_path(
                                        h5,
                                        obj_id,
                                        levels=levels,
                                        digits=digits
                                    )
                                    return grp, dname

                                return slow

                            # create resolver specific for this source DB
                            resolve_src_fast = make_fast_resolver(
                                src.hdf5_shard_levels,
                                src.hdf5_shard_digits
                            )

                            def _copy_one(soid: int, did: int):
                                """
                                Copy one dataset safely.
                                If the source HDF5 dataset does not exist, warn, increment missing_payloads,
                                and skip the object instead of aborting the merge.
                                """

                                nonlocal missing_payloads

                                dname = f"{soid:08d}"

                                # ---- Try fast resolution ----
                                try:
                                    grp_src, dname_src = resolve_src_fast(src._h5, soid)
                                    ds_src = grp_src.get(dname_src)
                                    if ds_src is None:
                                        raise KeyError
                                except Exception:
                                    # ---- Fallback brute-force search ----
                                    ds_src = None
                                    try:
                                        root = src._h5["objs"]
                                        for k, v in root.items():
                                            if isinstance(v, h5py.Dataset) and v.name.endswith(dname):
                                                ds_src = v
                                                break
                                            if isinstance(v, h5py.Group):
                                                for sub in v.values():
                                                    if isinstance(sub, h5py.Dataset) and sub.name.endswith(dname):
                                                        ds_src = sub
                                                        break
                                    except Exception:
                                        ds_src = None

                                    if ds_src is None:
                                        missing_payloads += 1
                                        if not quiet:
                                            print(f"[merge] WARNING: Missing HDF5 payload for source ID {soid}. Skipping.")
                                        return  # skip this object safely

                                # ---- Copy the dataset into the destination ----
                                bucket_dst, dname_dst = _h5_bucket_for_id(did)
                                if dname_dst in bucket_dst:
                                    del bucket_dst[dname_dst]
                                bucket_dst.copy(ds_src, dname_dst)

                            def _copy_one(soid: int, did: int):
                                """
                                Copy one dataset safely.
                                Optimized: Removes brute-force scan to prevent 60s timeouts/deadlocks.
                                """
                                nonlocal missing_payloads
                                dname = f"{soid:08d}"

                                # 1. Intentar resolución rápida (Directa)
                                ds_src = None
                                try:
                                    grp_src, dname_src = resolve_src_fast(src._h5, soid)
                                    ds_src = grp_src.get(dname_src)
                                except Exception:
                                    pass

                                # 2. Si no se encontró directo, NO BUSCAR. Asumir perdido.
                                if ds_src is None:
                                    missing_payloads += 1
                                    if not quiet:
                                        # Usar sys.stderr para evitar problemas de buffer en prints
                                        import sys
                                        print(f"[merge] WARNING: Missing HDF5 payload for source ID {soid}. Skipping.", file=sys.stderr)
                                    return  # <--- Salida inmediata, ahorra los 60 segundos

                                # 3. Si existe, copiar al destino
                                try:
                                    bucket_dst, dname_dst = _h5_bucket_for_id(did)
                                    if dname_dst in bucket_dst:
                                        del bucket_dst[dname_dst]
                                    bucket_dst.copy(ds_src, dname_dst)
                                except Exception as e:
                                    if not quiet:
                                        print(f"[merge] ERROR copying ID {soid} -> {did}: {e}")

                            # Execute copies: parallel or serial
                            if parallel_hdf5 > 1 and hdf5_threadsafe:
                                from concurrent.futures import ThreadPoolExecutor, as_completed
                                with ThreadPoolExecutor(max_workers=int(parallel_hdf5)) as exe:
                                    futures = [exe.submit(_copy_one, soid, did) for soid, did in mapping.items()]
                                    for _ in as_completed(futures):
                                        pass
                            else:
                                for soid, did in mapping.items():
                                    _copy_one(soid, did)

                            # end HDF5 phase

                            # Deferred flush
                            chunks_since_flush += 1
                            if flush_every_chunks and (chunks_since_flush % int(flush_every_chunks) == 0):
                                try:
                                    dst._h5.flush()
                                except Exception:
                                    pass
                                chunks_since_flush = 0

                            t_h5 = _t() - t_h5_0

                            # update counters
                            added_now = len(mapping)
                            source_added += added_now
                            total_added += added_now

                            # periodic WAL checkpoint
                            chunks_done += 1
                            if wal_checkpoint_every and (chunks_done % wal_checkpoint_every == 0):
                                try:
                                    con.execute("PRAGMA wal_checkpoint(TRUNCATE);")
                                except Exception:
                                    pass

                            if not quiet and (t_sql + t_h5) > 2.0:
                                # only print per-chunk timings if the chunk was notably slow
                                print(f"    [chunk] sql={t_sql:.2f}s, h5={t_h5:.2f}s, n={added_now}")

                        # end while chunks

                        con.execute("DETACH DATABASE src;")
                    finally:
                        src.close()

                    # ---- per-source progress line ----
                    src_elapsed = _t() - src_t0
                    total_elapsed = _t() - overall_t0
                    rate = (total_added / total_elapsed) if total_elapsed > 0 else 0.0
                    sources_ok.append(src_root)
                    if not quiet:
                        print(
                            f"[{si}/{len(sources)}] Done: {src_root} | "
                            f"added={source_added:,}, skipped={source_skipped:,}, "
                            f"src_time={_fmt_t(src_elapsed)} | "
                            f"TOTAL added={total_added:,}, skipped={total_skipped:,}, "
                            f"elapsed={_fmt_t(total_elapsed)}, rate={rate:,.1f} obj/s"
                        )

                except Exception as e:
                    # per-source failure line
                    try:
                        con.rollback()
                    except Exception:
                        pass
                    try:
                        con.execute("DETACH DATABASE src;")
                    except Exception:
                        pass
                    sources_fail.append((src_root, str(e)))
                    if not quiet:
                        total_elapsed = _t() - overall_t0
                        print(
                            f"[{si}/{len(sources)}] FAILED: {src_root} | error={e!r} | "
                            f"elapsed={_fmt_t(total_elapsed)} | "
                            f"TOTAL added={total_added:,}, skipped={total_skipped:,}"
                        )

            # --- final flush if needed ---
            try:
                dst._h5.flush()
            except Exception:
                pass

            # --- recreate previously dropped indices ---
            for stmt in recreate_idx_sql:
                try:
                    con.execute(stmt)
                except Exception as e:
                    if not quiet:
                        print(f"[merge] Recreate index failed: {e}")

            # Re-enable FKs
            con.execute("PRAGMA foreign_keys=ON;")

            # --- optional compact + integrity check (only once at the end) ---
            if compact:
                try:
                    dst.compact_hdf5()
                    if not quiet:
                        print("[merge] HDF5 compacted.")
                except Exception as e:
                    if not quiet:
                        print(f"[merge] HDF5 compaction skipped (non-fatal): {e}")

            try:
                res = con.execute("PRAGMA integrity_check;").fetchone()
                if res and res[0] != "ok":
                    print(f"[merge] WARNING: integrity_check: {res}")
            except Exception as e:
                if not quiet:
                    print(f"[merge] integrity_check failed: {e}")

            # ---- FINAL STATISTICS ----
            total_elapsed = _t() - overall_t0
            rate = (total_added / total_elapsed) if total_elapsed > 0 else 0.0
            if not quiet:
                print("\n========== MERGE SUMMARY ==========")
                print(f"Destination: {dst_root}")
                print(f"Sources found: {len(sources)}")
                print(f"Sources merged OK: {len(sources_ok)}")
                print(f"Sources failed: {len(sources_fail)}")
                if sources_fail:
                    for sr, msg in sources_fail[:10]:
                        print(f"  - {sr}: {msg}")
                    if len(sources_fail) > 10:
                        print(f"  ... and {len(sources_fail)-10} more failures")
                print(f"Objects added: {total_added:,}")
                print(f"Duplicates skipped: {total_skipped:,}")
                print(f"Total elapsed: {_fmt_t(total_elapsed)}")
                print(f"Throughput: {rate:,.1f} objects/sec")
                print(f"Missing HDF5 payloads skipped: {missing_payloads:,}")
                print("===================================\n")

            return {
                "sources_found": len(sources),
                "sources_successful": len(sources_ok),
                "sources_failed": [{"path": p, "error": msg} for p, msg in sources_fail],
                "objects_added": int(total_added),
                "skipped_duplicates": int(total_skipped),
                "elapsed_seconds": float(total_elapsed),
                "objects_per_second": float(rate),
                "dst_root": dst_root,
                "dst_sqlite": dst.sqlite_path,
                "dst_h5": dst.h5_path,
                "sources": sources,
                "hdf5_shard_levels": int(hdf5_shard_levels),
                "hdf5_shard_digits": int(hdf5_shard_digits),
                "flush_every_chunks": int(flush_every_chunks),
                "missing_payloads": int(missing_payloads),
            }

        finally:
            dst.close()

    @staticmethod
    def _is_scalar(x: Any) -> bool:
        """Return True if x is a scalar (int, float, 0D np.ndarray, etc.)."""
        if isinstance(x, (int, float, np.integer, np.floating)):
            return True
        if isinstance(x, np.ndarray) and x.ndim == 0:
            return True
        return False

    @staticmethod
    def _extract_scalars(obj: Any) -> Dict[str, float]:
        """
        Extract scalar numerical attributes from an object.
        Intended for populating the `scalars` table in HybridStorage.

        Supported cases:
          * obj has attributes 'energy', 'Ef', 'free_energy', etc.
          * obj.info (dict-like) contains numeric entries.
          * obj.results (ASE) contains numeric entries.

        Returns
        -------
        dict
            key -> float (NaN filtered)
        """
        @staticmethod
        def _is_scalar(x: Any) -> bool:
            """Return True if x is a scalar (int, float, 0D np.ndarray, etc.)."""
            if isinstance(x, (int, float, np.integer, np.floating)):
                return True
            if isinstance(x, np.ndarray) and x.ndim == 0:
                return True
            return False

        out: Dict[str, float] = {}

        # 1. Check known scalar attributes
        for name in ["energy", "E", "Ef", "Etot", "free_energy"]:
            val = getattr(obj, name, None)
            if _is_scalar(val):
                out[name] = float(val)

        # 2. obj.info (ASE-compatible)
        info = getattr(obj, "info", None)
        if isinstance(info, dict):
            for k, v in info.items():
                if _is_scalar(v):
                    out.setdefault(str(k), float(v))

        # 3. obj.results (ASE-calculator results)
        results = getattr(obj, "results", None)
        if isinstance(results, dict):
            for k, v in results.items():
                if _is_scalar(v):
                    out.setdefault(str(k), float(v))

        # 4. filter NaNs
        out = {k: float(v) for k, v in out.items() if np.isfinite(v)}

        return out

    @staticmethod
    def _extract_labels(obj: Any) -> List[str]:
        apm = getattr(obj, "AtomPositionManager", None)
        if apm is None:
            return []
        labels = getattr(apm, "atomLabelsList", None)
        if labels is None:
            labels = getattr(apm, "_atomLabelsList", None)
        if labels is None:
            return []
        try:
            import numpy as _np
            if isinstance(labels, _np.ndarray):
                return [str(x) for x in labels.tolist()]
        except Exception:
            pass
        return [str(x) for x in labels]

    @staticmethod
    def _extract_energy(obj: Any) -> Optional[float]:
        apm = getattr(obj, "AtomPositionManager", None)
        if apm is None:
            return None
        for name in ("energy", "_energy", "E", "_E"):
            val = getattr(apm, name, None)
            f = HybridStorage._to_float_or_none(val)
            if f is not None:
                return f
        return None

    @staticmethod
    def _extract_free_energy(obj: Any) -> Optional[float]:
        apm = getattr(obj, "AtomPositionManager", None)
        if apm is None:
            return None
        metadata = getattr(apm, "metadata", None)
        if isinstance(metadata, dict) and "F" in metadata:
            return HybridStorage._to_float_or_none(metadata["F"])
        return None

    def _ensure_species(self, symbol: str) -> int:
        cur = self._conn.cursor()
        # try fast path
        cur.execute("SELECT species_id FROM species WHERE symbol=?;", (symbol,))
        row = cur.fetchone()
        if row:
            return int(row[0])
        # assign next rank = max(rank)+1
        cur.execute("SELECT COALESCE(MAX(rank), -1) + 1 FROM species;")
        next_rank = int(cur.fetchone()[0])
        cur.execute("INSERT INTO species(symbol, rank) VALUES(?,?);", (symbol, next_rank))
        self._conn.commit()
        return int(cur.lastrowid)

    @staticmethod
    def _formula_from_counts(counts: Dict[str, float]) -> str:
        # ordered by symbol alphabetically for normalized display (mapping is separate)
        parts = []
        for sp in sorted(counts):
            c = counts[sp]
            c = int(round(c)) if abs(c - round(c)) < 1e-8 else c
            parts.append(f"{sp}{'' if c == 1 else c}")
        return "".join(parts)

    def _save_payload_h5(self, obj_id: int, obj: Any):
        blob = pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
        arr = np.frombuffer(blob, dtype=np.uint8)

        grp, dname = self._resolve_h5_path(self._h5, obj_id,
                                           levels=self.hdf5_shard_levels,
                                           digits=self.hdf5_shard_digits)
        if dname in grp:
            del grp[dname]
        ds = grp.create_dataset(dname, data=arr, compression="gzip", shuffle=True)

        scal = self._extract_scalars(obj)
        if "E" in scal:
            ds.attrs["E"] = float(scal["E"])
        ds.attrs["id"] = int(obj_id)


    def _load_payload_h5(self, obj_id: int) -> Any:
        dname = f"{int(obj_id):08d}"

        # 1) Primary: detected layout (trailing digits, YY/XX order)
        grp, dname1 = self._resolve_h5_path(self._h5, obj_id,
                                            levels=self.hdf5_shard_levels,
                                            digits=self.hdf5_shard_digits)
        if dname1 in grp:
            arr = np.array(grp[dname1][...], dtype=np.uint8)
            return pickle.loads(arr.tobytes())

        # 2) Fallback A: flat (/objs/########)
        flat = self._h5["objs"]
        if dname in flat:
            arr = np.array(flat[dname][...], dtype=np.uint8)
            return pickle.loads(arr.tobytes())

        # 3) Fallback B: inverted shard order (legacy) → /objs/XX/YY/########
        # Only try if levels==2
        if self.hdf5_shard_levels == 2:
            inv_grp = self._h5["objs"]
            key2 = dname[-2*self.hdf5_shard_digits:-self.hdf5_shard_digits]
            key1 = dname[-self.hdf5_shard_digits:]
            if key1 in inv_grp:
                inv_grp = inv_grp[key1]
                if key2 in inv_grp:
                    inv_grp = inv_grp[key2]
                    if dname in inv_grp:
                        arr = np.array(inv_grp[dname][...], dtype=np.uint8)
                        return pickle.loads(arr.tobytes())

        # 4) Fallback C: scan one level down (defensive)
        try:
            for k1, g1 in self._h5["objs"].items():
                if isinstance(g1, h5py.Group) and dname in g1:
                    arr = np.array(g1[dname][...], dtype=np.uint8)
                    return pickle.loads(arr.tobytes())
                for k2, g2 in g1.items():
                    if isinstance(g2, h5py.Group) and dname in g2:
                        arr = np.array(g2[dname][...], dtype=np.uint8)
                        return pickle.loads(arr.tobytes())
        except Exception:
            pass

        raise KeyError(f"HDF5 dataset not found for id {obj_id}")

    @staticmethod
    def _extract_hash(obj: Any) -> Optional[str]:
        """
        Try to extract a content hash from the object.
        Priority:
          1) obj.AtomPositionManager.metadata['hash'|'content_hash'|'sha256']
          2) obj.hash (string-like)
        """
        # 1) From APM metadata
        apm = getattr(obj, "AtomPositionManager", None)
        if apm is not None:
            meta = getattr(apm, "metadata", None)
            if isinstance(meta, dict):
                for k in ("hash", "content_hash", "sha256"):
                    h = meta.get(k)
                    if isinstance(h, str) and h:
                        return h
        # 2) From top-level attribute
        h2 = getattr(obj, "hash", None)
        if isinstance(h2, str) and h2:
            return h2
        return None

    @staticmethod
    def _extract_metadata(obj: Any) -> dict | None:
        """
        Extract the full metadata dictionary from obj.AtomPositionManager.metadata.
        Returns a Python dict or None.
        """
        apm = getattr(obj, "AtomPositionManager", None)
        if apm is None:
            return None

        meta = getattr(apm, "metadata", None)
        
        if isinstance(meta, dict):
            return meta
        return None

    @staticmethod
    def _extract_lattice(obj: Any) -> Optional[np.ndarray]:
        """
        Extract a 3x3 lattice matrix from the object.
        Returns None if not present or invalid.
        """
        apm = getattr(obj, "AtomPositionManager", None)
        if apm is None:
            return None

        # Candidate attribute names (robust)
        candidates = ("latticeVectors", "lattice", "L", "_latticeVectors", "cell")

        for name in candidates:
            lv = getattr(apm, name, None)
            if lv is None:
                continue

            try:
                import numpy as np
                arr = np.asarray(lv, dtype=float)
                if arr.shape == (3, 3):
                    return arr
            except Exception:
                pass

        return None

    # ---------------- Public API ----------------
    def add(self, obj: Any) -> int:
        self._assert_writable()

        # 1. Extract all data from the object
        labels = self._extract_labels(obj)
        natoms = len(labels) if labels else None

        counts: Dict[str, float] = {}
        for s in labels:
            counts[s] = counts.get(s, 0.0) + 1.0
        formula = self._formula_from_counts(counts) if counts else None

        scalars = self._extract_scalars(obj)
        energy = self._extract_energy(obj)
        free_energy = self._extract_free_energy(obj)
        content_hash = self._extract_hash(obj)
        metadata_dict = self._extract_metadata(obj)
        lattice = self._extract_lattice(obj)

        # 2. Prepare JSON payload
        meta_payload = {"composition": counts}
        if free_energy is not None:
            meta_payload["free_energy"] = free_energy
        if content_hash is not None:
            meta_payload["hash"] = content_hash  # keep it in meta_json for convenience
        if metadata_dict is not None: # capture full metadata
            meta_payload["apm_metadata"] = metadata_dict

        # 3. Insert main object record
        cur = self._conn.cursor()
        cur.execute(
            "INSERT INTO objects (energy, natoms, formula, meta_json) VALUES (?,?,?,?);",
            (energy, natoms, formula, json.dumps(meta_payload))
        )
        obj_id = int(cur.lastrowid)

        # 4. Insert related data (Compositions)
        if counts:
            rows = []
            for sym, ct in counts.items():
                spid = self._ensure_species(sym)
                rows.append((obj_id, spid, float(ct)))
            cur.executemany(
                "INSERT INTO compositions(object_id, species_id, count) VALUES (?,?,?);",
                rows
            )

        # 5. Insert related data (Scalars)
        if scalars:
            cur.executemany(
                "INSERT INTO scalars(object_id, key, value) VALUES (?,?,?);",
                [(obj_id, k, float(v)) for k, v in scalars.items()]
            )

        # 6. Insert related data (Metadata Key-Value)
        # --- store metadata_kv ---
        if metadata_dict is not None:
            rows = [(obj_id, str(k), json.dumps(v)) for k, v in metadata_dict.items()]
            cur.executemany(
                "INSERT INTO metadata_kv(object_id, key, value_json) VALUES (?,?,?);",
                rows
            )

        # 7. Insert related data (Hashes)
        if content_hash is not None:
            cur.execute(
                "INSERT OR REPLACE INTO object_hashes(object_id, hash) VALUES (?, ?);",
                (obj_id, content_hash)
            )

        # 8. Insert related data (Lattice) - INLINE LOGIC
        if lattice is not None:
            a = lattice # 3x3 array
            cur.execute("""
                INSERT INTO lattice (object_id, a11,a12,a13, a21,a22,a23, a31,a32,a33)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (
                obj_id,
                float(a[0][0]), float(a[0][1]), float(a[0][2]),
                float(a[1][0]), float(a[1][1]), float(a[1][2]),
                float(a[2][0]), float(a[2][1]), float(a[2][2])
            ))

        # 9. Commit and save payload
        self._conn.commit()
        self._save_payload_h5(obj_id, obj)
        self._h5.flush()
        return obj_id

    def _ensure_species_bulk(self, symbols):
        symbols = [s for s in dict.fromkeys(map(str, symbols)) if s]  # unique, keep order
        if not symbols:
            return {}

        cur = self._conn.cursor()

        # helper to select any set of symbols with the right number of placeholders
        def _select_map(items):
            if not items:
                return {}
            q = "SELECT symbol, species_id FROM species WHERE symbol IN (%s);" % \
                ",".join("?" for _ in items)
            cur.execute(q, items)
            return {sym: int(spid) for sym, spid in cur.fetchall()}

        # existing ones
        mapping = _select_map(symbols)

        # insert missing with proper ranks
        missing = [s for s in symbols if s not in mapping]
        if missing:
            cur.execute("SELECT COALESCE(MAX(rank), -1) FROM species;")
            start_rank = int(cur.fetchone()[0]) + 1
            rows = [(s, start_rank + i) for i, s in enumerate(missing)]
            cur.executemany("INSERT INTO species(symbol, rank) VALUES (?, ?);", rows)
            # re-select ONLY the missing with a query rebuilt for their length
            mapping.update(_select_map(missing))

        return mapping

    def add_many(self, objs, *, store_lattice:bool=True) -> list[int]:
        """
        High-throughput ingest. One SQL transaction, one HDF5 flush.
        """
        self._assert_writable()
        con = self._conn
        cur = con.cursor()

        # Speed PRAGMAs for bulk load (temporary; safe on a single-writer workflow)
        cur.execute("PRAGMA journal_mode=WAL;")
        cur.execute("PRAGMA synchronous=OFF;")
        cur.execute("PRAGMA temp_store=MEMORY;")
        cur.execute("PRAGMA cache_size=-200000;")

        # --- 1. Precompute lightweight metadata in Python ---
        # Precompute lightweight metadata in Python
        pre = []  # (obj, counts, scalars, energy, natoms, formula, hash)
        species_universe = set()
        for obj in objs:
            labels = self._extract_labels(obj)
            counts = {}
            if labels:
                for s in labels:
                    counts[s] = counts.get(s, 0.0) + 1.0
                species_universe.update(counts.keys())
            formula = self._formula_from_counts(counts) if counts else None
            scalars = self._extract_scalars(obj)
            energy  = self._extract_energy(obj)
            natoms  = len(labels) if labels else None
            free_E  = self._extract_free_energy(obj)
            h       = self._extract_hash(obj)
            metadata_dict = self._extract_metadata(obj)
            lattice = self._extract_lattice(obj)

            meta_payload = {"composition": counts}
            if free_E is not None:
                meta_payload["free_energy"] = free_E
            if h is not None:
                meta_payload["hash"] = h
            if metadata_dict is not None:
                meta_payload["apm_metadata"] = metadata_dict

            # Append 10 items to the pre-calculation list
            pre.append((obj, counts, scalars, energy, natoms, formula, h,
                meta_payload, metadata_dict, lattice))

        # --- 2. Begin SQL Transaction ---
        # Begin transaction for *all* rows
        con.execute("BEGIN;")

        # Bulk species resolution (ensure all species exist in DB)
        sym2id = self._ensure_species_bulk(species_universe)

        # --- 3. Insert Objects (Master Table) ---
        # Insert objects; capture new ids
        ids = []
        # Unpack the 10 items, ignoring what is not needed for the master table
        for (_obj, _counts, _scalars, energy, natoms, formula, _h, meta_payload, metadata_dict, _lat) in pre:
            cur.execute(
                "INSERT INTO objects (energy, natoms, formula, meta_json) VALUES (?,?,?,?);",
                (energy, natoms, formula, json.dumps(meta_payload))
            )
            ids.append(int(cur.lastrowid))

        # --- 4. Prepare Batch Arrays for Related Tables ---
        comp_rows = []
        scalar_rows = []
        hash_rows = []
        metadata_rows = []
        lattice_rows = []

        # Iterate once over the zipped IDs and pre-calculated data
        for oid, (_obj, counts, scalars, _e, _n, _f, h, _meta, _metadata_dict, lattice) in zip(ids, pre):
            # Compositions
            for sym, ct in counts.items():
                comp_rows.append((oid, sym2id[sym], float(ct)))
            # Scalars
            for k, v in scalars.items():
                scalar_rows.append((oid, str(k), float(v)))
            # Hashes
            if h:
                hash_rows.append((oid, h))

            # Metadata Key-Value
            if isinstance(_metadata_dict, dict):
                for k, v in _metadata_dict.items():
                    metadata_rows.append((oid, str(k), json.dumps(v)))

            # Lattice (3x3 Matrix)
            if store_lattice and lattice is not None:
                a = lattice
                lattice_rows.append((
                    oid,
                    float(a[0][0]), float(a[0][1]), float(a[0][2]),
                    float(a[1][0]), float(a[1][1]), float(a[1][2]),
                    float(a[2][0]), float(a[2][1]), float(a[2][2]),
                ))

        # --- 5. Bulk Execute Inserts ---
        if comp_rows:
            cur.executemany(
                "INSERT INTO compositions(object_id, species_id, count) VALUES (?,?,?);",
                comp_rows
            )
        
        if scalar_rows:
            cur.executemany(
                "INSERT INTO scalars(object_id, key, value) VALUES (?,?,?);",
                scalar_rows
            )
        
        if hash_rows:
            cur.executemany(
                "INSERT OR REPLACE INTO object_hashes(object_id, hash) VALUES (?,?);",
                hash_rows
            )

        if metadata_rows:
            cur.executemany(
                "INSERT INTO metadata_kv(object_id, key, value_json) VALUES (?,?,?);",
                metadata_rows
            )

        if lattice_rows:
            cur.executemany(
                """
                INSERT INTO lattice (object_id, a11,a12,a13, a21,a22,a23, a31,a32,a33) 
                VALUES (?,?,?,?,?,?,?,?,?,?)
                """,
                lattice_rows
            )

        # Commit SQL changes
        con.commit()

        # --- 6. HDF5 Writes (Single Flush) ---
        # Note: We use *_rest to handle the tuple safely without unpacking everything
        # HDF5 writes (single flush at the end)
        for oid, (obj, *_rest) in zip(ids, pre):
            self._save_payload_h5(oid, obj)

        self._h5.flush()

        return ids

    def get(self, obj_id: int):
        """Retrieve a stored object by ``id``.


        Args:
        obj_id: Primary key of the object.


        Returns:
        The deserialized Python object.
        """
        return self._load_payload_h5(int(obj_id))

    def remove(self, obj_ids: int | Sequence[int]) -> None:
        """
        Remove one or multiple objects and their associated metadata
        from both SQLite and HDF5 backends.

        Parameters
        ----------
        obj_ids : int or Sequence[int]
            Single ID or iterable of IDs to remove.
        """
        self._assert_writable()

        # Normalize to list of unique integers
        if isinstance(obj_ids, (int, np.integer)):
            obj_ids = [int(obj_ids)]
        else:
            obj_ids = sorted(set(int(x) for x in obj_ids))

        if not obj_ids:
            return

        # --- Delete from SQLite (cascade via FK) ---
        with self._conn:
            if len(obj_ids) == 1:
                self._conn.execute("DELETE FROM objects WHERE id=?;", (obj_ids[0],))
            else:
                # Chunked deletion to stay under SQLite parameter limits (~999)
                CHUNK = 900
                for i in range(0, len(obj_ids), CHUNK):
                    sub = obj_ids[i:i+CHUNK]
                    q = "DELETE FROM objects WHERE id IN (%s);" % ",".join("?" for _ in sub)
                    self._conn.execute(q, sub)

        # --- Delete from HDF5 (shard-aware) ---
        for obj_id in obj_ids:
            try:
                grp, dname = self._resolve_h5_path(
                    self._h5, obj_id,
                    levels=self.hdf5_shard_levels,
                    digits=self.hdf5_shard_digits
                )
                if dname in grp:
                    del grp[dname]

                    # prune empty shard groups
                    parent = grp
                    while parent.name != "/objs" and len(parent.keys()) == 0:
                        pname = os.path.basename(parent.name)
                        gparent = parent.parent
                        try:
                            del gparent[pname]
                        except Exception:
                            break
                        parent = gparent

            except KeyError:
                # fallback to flat layout
                dname = f"{obj_id:08d}"
                flat_grp = self._h5.get("objs", None)
                if flat_grp and dname in flat_grp:
                    del flat_grp[dname]

        # --- Persist changes ---
        try:
            self._h5.flush()
        except Exception:
            pass

    def list_ids(self) -> List[int]:
        cur = self._conn.cursor()
        cur.execute("SELECT id FROM objects ORDER BY id ASC;")
        return [int(r[0]) for r in cur.fetchall()]

    def count(self) -> int:
        cur = self._conn.cursor()
        cur.execute("SELECT COUNT(*) FROM objects;")
        return int(cur.fetchone()[0])

    def clear(self) -> None:
        self._assert_writable()

        # SQL
        cur = self._conn.cursor()
        cur.execute("DELETE FROM compositions;")
        cur.execute("DELETE FROM scalars;")
        cur.execute("DELETE FROM objects;")
        self._conn.commit()
        # HDF5
        for k in list(self._grp.keys()):
            del self._grp[k]
        self._h5.flush()

    def iter_ids(self, batch_size: Optional[int] = 1000):
        cur = self._conn.cursor()
        last = 0
        while True:
            if batch_size:
                cur.execute(
                    "SELECT id FROM objects WHERE id > ? ORDER BY id ASC LIMIT ?;",
                    (last, batch_size)
                )
            else:
                cur.execute(
                    "SELECT id FROM objects WHERE id > ? ORDER BY id ASC;",
                    (last,)
                )
            rows = cur.fetchall()
            if not rows:
                break
            for (cid,) in rows:
                yield int(cid)
            last = int(rows[-1][0])

    def iter_objects(self, batch_size: Optional[int] = 1000):
        for cid in self.iter_ids(batch_size=batch_size):
            yield cid, self.get(cid)

    def get_all_hashes(self, with_ids: bool = False):
        """
        Return all stored content hashes.

        Args:
            with_ids: if True, returns List[Tuple[int, str]] as (object_id, hash).
                      otherwise List[str] (ordered by object_id ASC).

        Notes:
            Only objects that have a hash recorded are returned.
            Falls back to scanning meta_json if legacy DB lacks `object_hashes`.
        """
        cur = self._conn.cursor()
        try:
            # Fast, indexed path
            cur.execute("SELECT object_id, hash FROM object_hashes ORDER BY object_id ASC;")
            rows = [(int(oid), str(h)) for oid, h in cur.fetchall()]
            return rows if with_ids else [h for _, h in rows]
        except sqlite3.OperationalError:
            # Legacy fallback: scan objects.meta_json
            cur.execute("SELECT id, meta_json FROM objects ORDER BY id ASC;")
            pairs = []
            for oid, mjson in cur.fetchall():
                if not mjson:
                    continue
                try:
                    meta = json.loads(mjson)
                except Exception:
                    continue
                h = None
                for k in ("hash", "content_hash", "sha256"):
                    v = meta.get(k)
                    if isinstance(v, str) and v:
                        h = v
                        break
                if h:
                    pairs.append((int(oid), h))
            return pairs if with_ids else [h for _, h in pairs]

    def get_metadata(self, obj_id: int) -> dict:
        cur = self._conn.cursor()
        cur.execute(
            "SELECT key, value_json FROM metadata_kv WHERE object_id=?;",
            (int(obj_id),)
        )
        out = {}
        for k, vjson in cur.fetchall():
            try:
                out[k] = json.loads(vjson)
            except Exception:
                out[k] = vjson
        return out

    def has_hash(self, hash_str: str) -> bool:
        """
        Fast membership check: does any object carry this hash?
        """
        cur = self._conn.cursor()
        cur.execute("SELECT 1 FROM object_hashes WHERE hash = ? LIMIT 1;", (str(hash_str),))
        return cur.fetchone() is not None

    def find_ids_by_hash(self, hash_str: str) -> List[int]:
        cur = self._conn.cursor()
        cur.execute("SELECT object_id FROM object_hashes WHERE hash = ?;", (str(hash_str),))
        return [int(oid) for (oid,) in cur.fetchall()]

    def find_ids_by_hash(self, hash_str) -> List[int]:
        """
        Robust lookup: ensures hash_str is a clean string.
        Accepts bytes, numpy arrays, memoryviews, etc.
        """
        # normalize input to pure python string
        if isinstance(hash_str, bytes):
            hash_str = hash_str.decode("utf8", errors="ignore")
        else:
            hash_str = str(hash_str)

        cur = self._conn.cursor()
        cur.execute(
            "SELECT object_id FROM object_hashes WHERE hash = ?;",
            (hash_str,)
        )

        ids = []
        for row in cur.fetchall():
            if not row or len(row) != 1:
                continue
            try:
                ids.append(int(row[0]))
            except Exception:
                continue
        return ids

    def find_hashes(self, hashes: Sequence[str]) -> Dict[str, List[int]]:
        """Batched lookup: hash -> [object_id,...]. Keeps O(k) with chunked IN() queries."""
        if not hashes:
            return {}
        out: Dict[str, List[int]] = {str(h): [] for h in hashes}
        cur = self._conn.cursor()

        # SQLite has a parameter limit (~999). Chunk accordingly.
        CHUNK = 900
        hs = [str(h) for h in hashes]
        for i in range(0, len(hs), CHUNK):
            chunk = hs[i:i+CHUNK]
            q = "SELECT hash, object_id FROM object_hashes WHERE hash IN (%s);" % ",".join("?" for _ in chunk)
            cur.execute(q, chunk)
            for h, oid in cur.fetchall():
                out[h].append(int(oid))
        return out

    # ---------------- Fast metadata access ----------------
    def get_metadata_keys_universe(self) -> list[str]:
        """Return a sorted list of all distinct metadata keys stored in metadata_kv."""
        cur = self._conn.cursor()
        cur.execute("SELECT DISTINCT key FROM metadata_kv ORDER BY key ASC;")
        return [str(r[0]) for r in cur.fetchall()]

    def get_species_universe(self, order: str = "stored") -> List[str]:
        """All species present. order='stored' (first-seen) or 'alphabetical'."""
        cur = self._conn.cursor()
        if order == "alphabetical":
            cur.execute("SELECT symbol FROM species ORDER BY symbol ASC;")
        else:
            cur.execute("SELECT symbol FROM species ORDER BY rank ASC;")
        return [r[0] for r in cur.fetchall()]

    def get_species_mapping(self, order: str = "stored") -> Dict[str, int]:
        """Symbol → column index mapping for dense composition matrices."""
        syms = self.get_species_universe(order=order)
        return {s: i for i, s in enumerate(syms)}

    def get_all_compositions(
        self,
        species_order: Optional[Sequence[str]] = None,
        return_species: bool = False,
        order: str = "stored",
    ):
        """
        Dense (n_samples, n_species) composition matrix in the requested species order.
        If species_order is None, uses order='stored' (first-seen stable).
        """
        cur = self._conn.cursor()
        # list of object ids, stable order
        cur.execute("SELECT id FROM objects ORDER BY id ASC;")
        ids = [int(r[0]) for r in cur.fetchall()]
        n = len(ids)
        if n == 0:
            res = np.zeros((0, 0), dtype=float)
            return (res, []) if return_species else res

        if species_order is None:
            species_order = self.get_species_universe(order=order)
        species_order = list(species_order)
        m = len(species_order)
        id_to_row = {oid: i for i, oid in enumerate(ids)}
        sp_to_col = {sp: j for j, sp in enumerate(species_order)}

        # join compositions with species symbols
        cur.execute("""
            SELECT c.object_id, s.symbol, c.count
            FROM compositions c
            JOIN species s ON s.species_id = c.species_id;
        """)
        M = np.zeros((n, m), dtype=float)
        for oid, sym, ct in cur.fetchall():
            i = id_to_row.get(int(oid))
            j = sp_to_col.get(sym)
            if i is not None and j is not None:
                try:
                    M[i, j] = float(ct)
                except Exception:
                    pass

        return (M, species_order) if return_species else M

    def get_scalar_keys_universe(self) -> List[str]:
        cur = self._conn.cursor()
        cur.execute("SELECT DISTINCT key FROM scalars ORDER BY key ASC;")
        return [r[0] for r in cur.fetchall()]

    def get_all_scalars(
        self,
        keys: Optional[Sequence[str]] = None,
        return_keys: bool = False
    ):
        """
        Dense (n_samples, n_keys) matrix of numeric scalar properties.
        Missing values are np.nan. Rows follow objects.id ascending.
        """
        cur = self._conn.cursor()
        cur.execute("SELECT id FROM objects ORDER BY id ASC;")
        ids = [int(r[0]) for r in cur.fetchall()]
        n = len(ids)
        if n == 0:
            res = np.zeros((0, 0), dtype=float)
            return (res, []) if return_keys else res

        if keys is None:
            keys = self.get_scalar_keys_universe()
        keys = list(keys)
        k = len(keys)
        id_to_row = {oid: i for i, oid in enumerate(ids)}
        key_to_col = {key: j for j, key in enumerate(keys)}

        A = np.full((n, k), np.nan, dtype=float)
        # fill from scalars
        cur.execute("SELECT object_id, key, value FROM scalars;")
        for oid, key, val in cur.fetchall():
            i = id_to_row.get(int(oid))
            j = key_to_col.get(key)
            if i is not None and j is not None and val is not None:
                A[i, j] = float(val)

        return (A, keys) if return_keys else A

    def get_all_energies(self) -> np.ndarray:
        """Convenience: objects.energy column; if empty, fallback to scalar 'E'."""
        cur = self._conn.cursor()
        cur.execute("SELECT energy FROM objects ORDER BY id ASC;")
        vals = [r[0] for r in cur.fetchall()]
        arr = np.array([v for v in vals if v is not None], dtype=float)
        if arr.size > 0:
            return arr
        # fallback
        A, keys = self.get_all_scalars(keys=["E"], return_keys=True)
        return A[:, 0] if A.size else np.array([], dtype=float)

    def get_all_metadata(self, key: str) -> np.ndarray:
        """
        Retrieve one metadata entry for all objects, ordered by object ID.
        Returns a 1D numpy array where each element is:
            - the decoded JSON value (Python type)
            - or None if no metadata exists for that key
        """
        cur = self._conn.cursor()

        # 1. Get all object ids
        cur.execute("SELECT id FROM objects ORDER BY id ASC;")
        ids = [int(r[0]) for r in cur.fetchall()]
        n = len(ids)
        if n == 0:
            return np.array([], dtype=object)

        # 2. Prepare output array
        out = np.empty(n, dtype=object)
        out[:] = None

        # 3. Load metadata_kv for this key
        cur.execute(
            "SELECT object_id, value_json FROM metadata_kv WHERE key=?;",
            (str(key),)
        )
        for oid, vjson in cur.fetchall():
            try:
                val = json.loads(vjson)
            except Exception:
                val = vjson
            # Map object_id → row index
            # (IDs are sorted, so we can binary search or just build a map once)
            # simplest: build a dict
            # but we can do this outside the loop for speed
            # Here is the clean version:
            pass

        # More efficient: build a map once
        id_to_row = {oid: i for i, oid in enumerate(ids)}

        # Re-run the query so we can fill after building id_to_row
        cur.execute(
            "SELECT object_id, value_json FROM metadata_kv WHERE key=?;",
            (str(key),)
        )
        for oid, vjson in cur.fetchall():
            try:
                val = json.loads(vjson)
            except Exception:
                val = vjson
            i = id_to_row.get(int(oid))
            if i is not None:
                out[i] = val

        return out

    # Debug/meta
    def get_meta(self, obj_id: int) -> Dict[str, Any]:
        cur = self._conn.cursor()
        cur.execute("SELECT energy, natoms, formula, meta_json FROM objects WHERE id=?;", (int(obj_id),))
        row = cur.fetchone()
        if row is None:
            raise KeyError(f"No object with id {obj_id}")
        energy, natoms, formula, meta_json = row
        meta = json.loads(meta_json) if meta_json else {}
        meta.update(dict(energy=energy, natoms=natoms, formula=formula))
        return meta

    def _ensure_lattice_table(self):
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS lattice (
                object_id INTEGER PRIMARY KEY,
                a11 REAL, a12 REAL, a13 REAL,
                a21 REAL, a22 REAL, a23 REAL,
                a31 REAL, a32 REAL, a33 REAL,
                FOREIGN KEY(object_id) REFERENCES objects(id) ON DELETE CASCADE
            );
        """)
        self._conn.commit()

    def get_all_lattice_vectors(self, missing="nan", *, fill_missing=True):
        """
        Retrieve all lattice vectors in order of list_ids().

        If fill_missing=True:
            - Missing SQL lattices are extracted from HDF5
            - Lattices containing NaNs are repaired from HDF5
            - Repaired values are written back into SQL automatically

        Always returns an array aligned with list_ids().
        """

        import numpy as np

        ids = self.list_ids()
        n = len(ids)

        # --- Output array initialization ---------------------------------------
        if missing == "nan":
            out = np.full((n, 3, 3), np.nan, dtype=float)
        elif missing == "zero":
            out = np.zeros((n, 3, 3), dtype=float)
        elif missing == "none":
            out = np.empty((n,), dtype=object)
        else:
            raise ValueError("missing must be 'nan', 'zero', or 'none'.")

        cur = self._conn.cursor()

        # --- 0) Backwards compatibility: does lattice table exist? -------------
        table_exists = cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='lattice';"
        ).fetchone() is not None

        if not table_exists:
            # Old DB without lattice table → return default output
            self._ensure_lattice_table()

        # --- 1) Load all existing SQL lattice rows -----------------------------
        rows = cur.execute(
            "SELECT object_id, a11,a12,a13, a21,a22,a23, a31,a32,a33 FROM lattice"
        ).fetchall()

        lattice_map = {
            oid: np.array([
                [float(a11), float(a12), float(a13)],
                [float(a21), float(a22), float(a23)],
                [float(a31), float(a32), float(a33)],
            ], dtype=float)
            for (oid, a11, a12, a13, a21, a22, a23, a31, a32, a33) in rows
        }

        # --- 2) Determine which entries need HDF5 fallback / repair ------------
        to_repair = []        # List of oids that need repair
        repaired_values = {}  # Mapping oid -> new lattice

        if fill_missing:

            for oid in tqdm(ids, desc="Checking lattices", disable=not fill_missing):
                needs_repair = False

                if oid not in lattice_map:
                    needs_repair = True
                else:
                    lv = lattice_map[oid]

                    # Robust detection of corrupted SQL lattice
                    try:
                        arr = np.asarray(lv, dtype=float)
                        if arr.shape != (3,3) or not np.isfinite(arr).all():
                            needs_repair = True
                    except Exception:
                        needs_repair = True

                if needs_repair:
                    # --- attempt HDF5 extraction ---
                    try:
                        obj = self.get(oid)
                        lv2 = self._extract_lattice(obj)
                    except Exception:
                        lv2 = None

                    if lv2 is not None:
                        repaired_values[oid] = lv2
                        lattice_map[oid] = lv2  # Update live map immediately
                        to_repair.append(oid)

        # --- 3) Write repaired entries back into SQL (auto-repair) ------------
        if fill_missing and to_repair:
            sql_rows = []
            for oid in to_repair:
                a = repaired_values[oid]
                sql_rows.append((
                    oid,
                    float(a[0][0]), float(a[0][1]), float(a[0][2]),
                    float(a[1][0]), float(a[1][1]), float(a[1][2]),
                    float(a[2][0]), float(a[2][1]), float(a[2][2]),
                ))

            cur.executemany(
                "INSERT OR REPLACE INTO lattice "
                "(object_id, a11,a12,a13, a21,a22,a23, a31,a32,a33) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                sql_rows
            )
            self._conn.commit()

        # --- 4) Fill output array in order of ids ------------------------------
        for i, oid in enumerate(ids):
            lv = lattice_map.get(oid)
            if lv is None:
                continue

            if missing == "none":
                out[i] = lv
            else:
                out[i, :, :] = lv

        return out


    def close(self):
        try:
            self._h5.flush(); self._h5.close()
        except Exception:
            pass
        try:
            self._conn.close()
        except Exception:
            pass

    # ---- maintenance ----
    def compact_hdf5(self, new_path: Optional[str] = None) -> str:
        self._assert_writable()
        self._h5.flush()
        src = self.h5_path
        dst = new_path or (self.h5_path + ".compact")
        with h5py.File(dst, "w") as out:
            out.copy(self._grp, "objs")
        if new_path is None:
            self._h5.close()
            os.replace(dst, src)
            self._h5 = h5py.File(src, "a")
            self._grp = self._h5["objs"]
            return src
        return dst

    @classmethod
    def generate_supercells(
        cls,
        src_root: str,
        dst_root: str,
        *,
        repeat=(2, 1, 1),
        batch_size: int = 5000,
        mode: str = "single",           # "single" | "parallel"
        max_workers: int = None,        # for parallel mode
        quiet: bool = False,
    ) -> dict:
        import os, time, pickle, numpy as np
        from math import prod

        # ---- optional progress bar
        try:
            from tqdm import tqdm
        except Exception:
            tqdm = None

        t0 = time.perf_counter()
        src_root = os.path.abspath(src_root)
        dst_root = os.path.abspath(dst_root)
        os.makedirs(dst_root, exist_ok=True)

        # Open storages
        src = cls(src_root, access="ro")
        dst = cls(dst_root, access="rw")

        # --- Aggressive PRAGMAs for bulk write ---
        con = dst._conn
        try:
            con.execute("PRAGMA journal_mode=MEMORY;")
        except Exception:
            pass
        con.execute("PRAGMA synchronous=OFF;")
        con.execute("PRAGMA temp_store=MEMORY;")
        con.execute("PRAGMA cache_size=-500000;")

        def _gen_inplace(obj):
            apm = getattr(obj, "AtomPositionManager", None)
            if apm is None:
                return None
            try:
                apm.generate_supercell(np.asarray(repeat, dtype=int))
                return obj
            except Exception:
                return None

        total = src.count()
        added = 0
        skipped = 0

        # create progress bar if available and not quiet
        pbar = None
        if (tqdm is not None) and (not quiet):
            pbar = tqdm(total=total, unit="obj", desc="Supercells", smoothing=0.1, mininterval=0.2)

        try:
            if mode == "single":
                buf = []
                for oid in src.iter_ids(batch_size=batch_size):
                    obj = src.get(oid)
                    obj2 = _gen_inplace(obj)
                    if obj2 is None:
                        skipped += 1
                    else:
                        buf.append(obj2)
                    if pbar is not None:
                        pbar.update(1)

                    if len(buf) >= batch_size:
                        dst.add_many(buf)
                        added += len(buf)
                        buf.clear()
                if buf:
                    dst.add_many(buf)
                    added += len(buf)

            elif mode == "parallel":
                from concurrent.futures import ProcessPoolExecutor, as_completed

                def _load_bytes_for_ids(ids):
                    out = []
                    grp = src._grp
                    for _oid in ids:
                        name = f"{_oid:08d}"
                        try:
                            arr = grp[name][...]
                            out.append((name, memoryview(arr).tobytes()))
                        except Exception:
                            out.append((name, None))
                    return out

                def _worker_make_supercell(blob: bytes, rep):
                    if blob is None:
                        return None
                    o = pickle.loads(blob)
                    apm = getattr(o, "AtomPositionManager", None)
                    if apm is None:
                        return None
                    apm.generate_supercell(np.asarray(rep, dtype=int))
                    return pickle.dumps(o, protocol=pickle.HIGHEST_PROTOCOL)

                CHUNK = batch_size
                ids_chunk = []

                for oid in src.iter_ids(batch_size=batch_size):
                    ids_chunk.append(oid)
                    if len(ids_chunk) >= CHUNK:
                        pairs = _load_bytes_for_ids(ids_chunk)
                        n_workers = max_workers or os.cpu_count() or 2
                        results = []
                        with ProcessPoolExecutor(max_workers=n_workers) as ex:
                            futs = [ex.submit(_worker_make_supercell, blob, repeat) for (_name, blob) in pairs]
                            for f in as_completed(futs):
                                results.append(f.result())

                        buf = []
                        for res in results:
                            if res is None:
                                skipped += 1
                            else:
                                try:
                                    buf.append(pickle.loads(res))
                                except Exception:
                                    skipped += 1
                        if buf:
                            dst.add_many(buf)
                            added += len(buf)

                        if pbar is not None:
                            pbar.update(len(ids_chunk))
                        ids_chunk.clear()

                if ids_chunk:
                    pairs = _load_bytes_for_ids(ids_chunk)
                    n_workers = max_workers or os.cpu_count() or 2
                    results = []
                    with ProcessPoolExecutor(max_workers=n_workers) as ex:
                        futs = [ex.submit(_worker_make_supercell, blob, repeat) for (_name, blob) in pairs]
                        for f in as_completed(futs):
                            results.append(f.result())
                    buf = []
                    for res in results:
                        if res is None:
                            skipped += 1
                        else:
                            try:
                                buf.append(pickle.loads(res))
                            except Exception:
                                skipped += 1
                    if buf:
                        dst.add_many(buf)
                        added += len(buf)
                    if pbar is not None:
                        pbar.update(len(ids_chunk))

            else:
                raise ValueError("mode must be 'single' or 'parallel'.")

        finally:
            if pbar is not None:
                pbar.close()

            # restore safer defaults + optional compact
            try:
                con.execute("PRAGMA journal_mode=WAL;")
            except Exception:
                pass
            con.execute("PRAGMA synchronous=NORMAL;")
            try:
                dst.compact_hdf5()
            except Exception:
                pass

            # close DBs
            try:
                src.close()
            finally:
                dst.close()

        t1 = time.perf_counter()
        report = {
            "source_db": src_root,
            "destination_db": dst_root,
            "repeat": tuple(int(x) for x in repeat),
            "objects_in_source": total,
            "objects_added": int(added),
            "objects_skipped": int(skipped),
            "mode": mode,
            "elapsed_s": round(t1 - t0, 3),
        }

        if not quiet:
            print(
                f"[supercells] Added {added}/{total} (skipped {skipped}) "
                f"in {report['elapsed_s']} s | mode={mode}, batch={batch_size}, scale={report['repeat']}"
            )

        return report
