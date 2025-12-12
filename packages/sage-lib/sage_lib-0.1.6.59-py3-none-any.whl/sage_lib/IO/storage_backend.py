# ============================
# storage_backend.py (updated)
# ============================
from __future__ import annotations

import os
import json
import glob
import pickle
import sqlite3
from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, Iterator, List, Optional, Sequence, Union, Tuple

import h5py
import numpy as np

StorageType = Union[List[Any], Dict[int, Any]]

class StorageBackend(ABC):
    """
    Abstract interface for container storage backends.

    Notes
    -----
    - `add` accepts an optional `metadata` mapping. Backends that do not use metadata
      may ignore it.
    - `get(obj_id=None)` may return a *lazy sequence* view (rather than a concrete list)
      when `obj_id` is None, to avoid loading everything into RAM. Code that needs a real
      list can call `list(...)` on that view.
    """

    @abstractmethod
    def add(self, obj: Any, metadata: Optional[Dict[str, Any]] = None) -> int:
        """Store object and return its integer ID."""
        raise NotImplementedError

    @abstractmethod
    def get(self, obj_id: Optional[int] = None):
        """
        Retrieve object by ID. If `obj_id` is None, return a *lazy* container view
        over all objects (implementing `__len__`, `__iter__`, and `__getitem__`).
        """
        raise NotImplementedError

    @abstractmethod
    def remove(self, obj_id: int) -> None:
        """Delete object by ID (no-op if already deleted)."""
        raise NotImplementedError

    @abstractmethod
    def list_ids(self) -> List[int]:
        """Return list of all object IDs (ascending)."""
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        """Return total number of stored objects."""
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        """Remove all objects from the store."""
        raise NotImplementedError

    # ---------- Optional (metadata-aware) API ----------
    def get_meta(self, obj_id: int) -> Dict[str, Any]:  # pragma: no cover (optional)
        raise NotImplementedError

    def set_meta(self, obj_id: int, meta: Dict[str, Any]) -> None:  # pragma: no cover
        raise NotImplementedError

    def query_ids(self, where: str, params: Sequence[Any] = ()) -> List[int]:  # pragma: no cover
        """SQL-like query support (if available)."""
        raise NotImplementedError

    # ---------- Convenience iteration (can be overridden) ----------
    def iter_ids(self, batch_size: Optional[int] = None) -> Iterator[int]:
        for cid in self.list_ids():
            yield cid

    def iter_objects(self, batch_size: Optional[int] = None) -> Iterator[tuple[int, Any]]:
        for cid in self.iter_ids(batch_size):
            yield cid, self.get(cid)


# -----------------------------
# In-memory (list/dict) backend
# -----------------------------
class MemoryStorage(StorageBackend):
    """
    Generic in-memory storage.

    The container can be either a list (sequential storage) or a dict that maps
    integer IDs to objects. IDs are always integers.
    """

    def __init__(self, initial: StorageType | None = None) -> None:
        self._data: StorageType = initial if initial is not None else []
        self._meta: Dict[int, Dict[str, Any]] = {}

    def add(self, obj: Any, metadata: Optional[Dict[str, Any]] = None) -> int:
        if isinstance(self._data, list):
            self._data.append(obj)
            idx = len(self._data) - 1
        else:
            idx = max(self._data.keys(), default=-1) + 1
            self._data[idx] = obj
        if metadata is not None:
            self._meta[idx] = metadata
        return idx

    def set(self, container: StorageType) -> int:
        if not isinstance(container, (list, dict)):
            raise TypeError("container must be a list or a dict[int, Any]")
        self._data = container
        self._meta.clear()
        return len(self._data) - 1 if isinstance(self._data, list) else (max(self._data.keys(), default=-1))

    def remove(self, obj_id: int) -> None:
        try:
            del self._data[obj_id]
        except (IndexError, KeyError):
            raise KeyError(f"No object found with id {obj_id}") from None
        self._meta.pop(obj_id, None)

    def get(self, obj_id: Optional[int] = None):
        if obj_id is None:
            return self._data
        try:
            return self._data[obj_id]
        except (IndexError, KeyError):
            raise KeyError(f"No object found with id {obj_id}") from None

    def list_ids(self) -> List[int]:
        return list(range(len(self._data))) if isinstance(self._data, list) else list(self._data.keys())

    def count(self) -> int:
        return len(self._data)

    def clear(self) -> None:
        if isinstance(self._data, list):
            self._data.clear()
        else:
            self._data = {}
        self._meta.clear()

    # Optional metadata helpers
    def get_meta(self, obj_id: int) -> Dict[str, Any]:
        return dict(self._meta.get(obj_id, {}))

    def set_meta(self, obj_id: int, meta: Dict[str, Any]) -> None:
        self._meta[obj_id] = dict(meta)

# -----------------------------
# SQLite (pickle BLOB) backend
# -----------------------------
class SQLiteStorage(StorageBackend):
    """SQLite-based storage, pickling objects into a BLOB."""

    def __init__(self, db_path: str):
        dir_path = os.path.dirname(db_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_schema()

    def _init_schema(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS containers (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                data BLOB NOT NULL
            );
            """
        )
        self.conn.commit()

    def add(self, obj: Any, metadata: Optional[Dict[str, Any]] = None) -> int:
        blob = pickle.dumps(obj)
        cur = self.conn.cursor()
        cur.execute("INSERT INTO containers (data) VALUES (?);", (blob,))
        self.conn.commit()
        return int(cur.lastrowid)

    def get(self, obj_id: Optional[int] = None):
        if obj_id is None:
            # Return a lightweight proxy of all objects (loads on iteration)
            return _LazySQLiteView(self)
        cur = self.conn.cursor()
        cur.execute("SELECT data FROM containers WHERE id = ?;", (obj_id,))
        row = cur.fetchone()
        if row is None:
            raise KeyError(f"No container with id {obj_id}")
        return pickle.loads(row[0])

    def remove(self, obj_id: int) -> None:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM containers WHERE id = ?;", (obj_id,))
        if cur.rowcount == 0:
            raise KeyError(f"No container with id {obj_id}")
        self.conn.commit()

    def list_ids(self) -> List[int]:
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM containers ORDER BY id ASC;")
        return [int(row[0]) for row in cur.fetchall()]

    def count(self) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM containers;")
        return int(cur.fetchone()[0])

    def clear(self) -> None:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM containers;")
        self.conn.commit()

    def iter_ids(self, batch_size: Optional[int] = 1000) -> Iterator[int]:
        cur = self.conn.cursor()
        last = 0
        while True:
            if batch_size:
                cur.execute(
                    "SELECT id FROM containers WHERE id > ? ORDER BY id ASC LIMIT ?;",
                    (last, batch_size),
                )
            else:
                cur.execute(
                    "SELECT id FROM containers WHERE id > ? ORDER BY id ASC;",
                    (last,),
                )
            rows = cur.fetchall()
            if not rows:
                break
            for (cid,) in rows:
                yield int(cid)
            last = int(rows[-1][0])

class _LazySQLiteView:
    """Lazy sequence-like view over all objects in SQLiteStorage."""

    def __init__(self, store: SQLiteStorage):
        self._s = store

    def __len__(self) -> int:
        return self._s.count()

    def __iter__(self):
        for cid in self._s.iter_ids():
            yield self._s.get(cid)

    def __getitem__(self, i):
        if isinstance(i, slice):
            ids = self._s.list_ids()[i]
            return [self._s.get(cid) for cid in ids]
        else:
            cid = self._s.list_ids()[i]
            return self._s.get(cid)


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

Example:
    >>> store = HybridStorage("./hybrid_store")
    >>> obj_id = store.add(obj)  # obj carries .E and AtomPositionManager
    >>> meta = store.get_meta(obj_id)
    >>> payload = store.get(obj_id)

"""
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

        # Optional: log for debugging
        print(f"[HybridStorage] Detected sharding: levels={self.hdf5_shard_levels}, digits={self.hdf5_shard_digits}")

    # --- HDF5 shard path resolver ---
    @staticmethod
    def _resolve_h5_path(h5: "h5py.File", obj_id: int,
                         levels: int = 0, digits: int = 2):
        """
        Resolve (group, dataset_name) using the SAME convention as merge_roots_recursive_attach:
          levels=0  → /objs/########
          levels=1  → /objs/XX/########         (XX = last <digits> of zero-padded id)
          levels=2  → /objs/YY/XX/########      (YY = second-last <digits>)
        """
        dname = f"{int(obj_id):08d}"
        grp = h5["objs"]

        if levels >= 1:
            key1 = dname[-digits:]              # last digits
            grp = grp.require_group(key1) if isinstance(grp, h5py.Group) else grp[key1]
        if levels >= 2:
            key2 = dname[-2*digits:-digits]     # second-last digits
            grp = grp.require_group(key2) if isinstance(grp, h5py.Group) else grp[key2]

        return grp, dname



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

            # --- Indexes ---
            cur.execute("CREATE INDEX IF NOT EXISTS idx_objects_energy     ON objects(energy);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_comp_sp            ON compositions(species_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_scalars_key        ON scalars(key);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_object_hashes_hash ON object_hashes(hash);")

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

        # --- new performance knobs ---
        hdf5_shard_levels: int = 1,   # 0 = flat /objs, 1 = /objs/XX, 2 = /objs/XX/YY
        hdf5_shard_digits: int = 2,   # digits per level (base-10)
        flush_every_chunks: int = 10, # flush HDF5 every N chunks instead of each chunk
        wal_checkpoint_every: int = 50,  # run WAL checkpoint every N chunks
    ):
        """
        High-throughput merge of many 'hybrid roots' (db_index.sqlite + db_objects.h5) into a single destination.

        Key improvements vs the original:
          - HDF5 sharding: store objects under /objs/XX[/YY]/######## to cap per-group link counts.
          - Removed per-object "if dataset exists" membership checks in HDF5 (expensive at scale).
          - Less frequent HDF5 flush (every `flush_every_chunks` chunks).
          - Periodic SQLite WAL checkpoint to keep WAL bounded.
          - Keeps all previous safeguards (chunked SELECT, dedup set, index recreate).
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

                            # ---- HDF5 phase (sharded, no existence check) ----
                            t_h5_0 = _t()

                            dst_grp = dst_root_grp  # alias

                            def _copy_one(soid: int, did: int):
                                sname = f"{int(soid):08d}"
                                bucket, dname = _h5_bucket_for_id(did)
                                try:
                                    bucket.copy(src._h5["objs"][sname], dname)
                                except KeyError:
                                    if not quiet:
                                        print(f"[warn] Missing dataset {sname} in {src_root}")

                            if parallel_hdf5 > 1 and hdf5_threadsafe:
                                from concurrent.futures import ThreadPoolExecutor, as_completed
                                with ThreadPoolExecutor(max_workers=int(parallel_hdf5)) as exe:
                                    futs = [exe.submit(_copy_one, soid, did) for soid, did in mapping.items()]
                                    for _ in as_completed(futs):
                                        pass
                            else:
                                for soid, did in mapping.items():
                                    _copy_one(soid, did)

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
            }

        finally:
            dst.close()



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
        self.hdf5_shard_levels = 2
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

    # ---------------- Public API ----------------
    def add(self, obj: Any) -> int:
        self._assert_writable()

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

        meta_payload = {"composition": counts}
        if free_energy is not None:
            meta_payload["free_energy"] = free_energy
        if content_hash is not None:
            meta_payload["hash"] = content_hash  # keep it in meta_json for convenience


        cur = self._conn.cursor()
        cur.execute(
            "INSERT INTO objects (energy, natoms, formula, meta_json) VALUES (?,?,?,?);",
            (energy, natoms, formula, json.dumps(meta_payload))
        )
        obj_id = int(cur.lastrowid)

        if counts:
            rows = []
            for sym, ct in counts.items():
                spid = self._ensure_species(sym)
                rows.append((obj_id, spid, float(ct)))
            cur.executemany(
                "INSERT INTO compositions(object_id, species_id, count) VALUES (?,?,?);",
                rows
            )

        if scalars:
            cur.executemany(
                "INSERT INTO scalars(object_id, key, value) VALUES (?,?,?);",
                [(obj_id, k, float(v)) for k, v in scalars.items()]
            )

        if content_hash is not None:
            cur.execute(
                "INSERT OR REPLACE INTO object_hashes(object_id, hash) VALUES (?, ?);",
                (obj_id, content_hash)
            )

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

    def add_many(self, objs) -> list[int]:
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
            meta_payload = {"composition": counts}
            if free_E is not None:
                meta_payload["free_energy"] = free_E
            if h is not None:
                meta_payload["hash"] = h
            pre.append((obj, counts, scalars, energy, natoms, formula, h, meta_payload))

        # Begin transaction for *all* rows
        con.execute("BEGIN;")

        # Bulk species resolution
        sym2id = self._ensure_species_bulk(species_universe)

        # Insert objects; capture new ids
        ids = []
        for (_obj, _counts, _scalars, energy, natoms, formula, _h, meta_payload) in pre:
            cur.execute(
                "INSERT INTO objects (energy, natoms, formula, meta_json) VALUES (?,?,?,?);",
                (energy, natoms, formula, json.dumps(meta_payload))
            )
            ids.append(int(cur.lastrowid))

        # compositions/scalars/hash in batches
        comp_rows, scalar_rows, hash_rows = [], [], []
        for oid, (_obj, counts, scalars, _e, _n, _f, h, _meta) in zip(ids, pre):
            for sym, ct in counts.items():
                comp_rows.append((oid, sym2id[sym], float(ct)))
            for k, v in scalars.items():
                scalar_rows.append((oid, str(k), float(v)))
            if h:
                hash_rows.append((oid, h))

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

        con.commit()

        # HDF5 writes (single flush at the end)
        for oid, (obj, *_rest) in zip(ids, pre):
            self._save_payload_h5(oid, obj)
        self._h5.flush()

        return ids

    def get(self, obj_id: int):
        return self._load_payload_h5(int(obj_id))

    def remove(self, obj_id: int) -> None:
        self._assert_writable()

        obj_id = int(obj_id)
        # HDF5
        dname = f"{obj_id:08d}"
        if dname in self._grp:
            del self._grp[dname]
        # SQL
        cur = self._conn.cursor()
        cur.execute("DELETE FROM objects WHERE id=?;", (obj_id,))
        self._conn.commit()

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



class _LazyHybridView:
    """Lazy sequence-like view over all objects in HybridStorage."""

    def __init__(self, store: HybridStorage):
        self._s = store

    def __len__(self) -> int:
        return self._s.count()

    def __iter__(self):
        for cid in self._s.iter_ids():
            yield self._s.get(cid)

    def __getitem__(self, i):
        if isinstance(i, slice):
            ids = self._s.list_ids()[i]
            return [self._s.get(cid) for cid in ids]
        else:
            cid = self._s.list_ids()[i]
            return self._s.get(cid)

class CompositeHybridStorage(StorageBackend):
    """
    Unified, read/write *view* over two stores:
      - base: usually HybridStorage(opened 'ro'), immutable here
      - local: usually HybridStorage(opened 'rw'), all writes go here

    IDs exposed by this adapter are **composite indices**: 0..(N_base_active + N_local_active - 1)
    in the order [base_active, then local_active]. Internally we map each composite
    id to (part='base'|'local', backend_id). Removing a 'base' object sets a tombstone.
    """

    def __init__(self, base_store: StorageBackend, local_store: StorageBackend, allow_shadow_delete: bool = True):
        self.base = base_store
        self.local = local_store
        self.allow_shadow_delete = allow_shadow_delete

        # Tombstones hide items from 'base' (and optionally 'local' if you want soft deletes there too)
        self._base_tombs: set[int] = set()
        # For symmetry; not typically used because local deletes are hard-deletes
        self._local_tombs: set[int] = set()

    @classmethod
    def from_composite(cls, base_root: str, local_root: str, *args, **kwargs) -> "PartitionManager":
        kwargs = dict(kwargs)
        kwargs['base_root'] = base_root
        kwargs['local_root'] = local_root
        return cls(storage='composite', db_path=base_root, *args, **kwargs)

    # ---------- internal helpers ----------
    def _active_count(self, part: str) -> int:
        """
        Count ACTIVE items for a part ('base' or 'local'), i.e., excluding tombstones.
        """
        if part not in ("base", "local"):
            raise ValueError("part must be 'base' or 'local'")
        store = self.base if part == "base" else self.local
        tombs = self._base_tombs if part == "base" else self._local_tombs
        try:
            ids = store.list_ids()
        except Exception:
            return 0
        if not tombs:
            return len(ids)
        # Avoid materializing large sets when tombs is empty/small
        return sum(1 for i in ids if i not in tombs)

    def _active_count_fast(self, part: str) -> int:
        """
        O(1) active count using backend COUNT(*) and subtracting tombstones.
        Falls back to the slower path if a backend lacks count().
        """
        if part == "base":
            try:
                return int(self.base.count()) - len(self._base_tombs)
            except Exception:
                return self._active_count("base")
        elif part == "local":
            try:
                return int(self.local.count()) - len(self._local_tombs)
            except Exception:
                return self._active_count("local")
        else:
            raise ValueError("part must be 'base' or 'local'")

    def _compose_pairs(self) -> List[Tuple[str, int]]:
        """
        Returns a list of (part, backend_id) in composite order:
        all active base ids (ascending) then all active local ids (ascending).
        """
        pairs: List[Tuple[str, int]] = []
        # base (skip tombstoned)
        try:
            base_ids = self.base.list_ids()
        except Exception:
            base_ids = []
        for bid in base_ids:
            if bid not in self._base_tombs:
                pairs.append(("base", int(bid)))
        # local (skip tombstoned if you use them)
        try:
            local_ids = self.local.list_ids()
        except Exception:
            local_ids = []
        for lid in local_ids:
            if lid not in self._local_tombs:
                pairs.append(("local", int(lid)))
        return pairs

    def _resolve(self, composite_id: int) -> Tuple[str, int]:
        pairs = self._compose_pairs()
        if composite_id < 0 or composite_id >= len(pairs):
            raise KeyError(f"No object found with composite id {composite_id}")
        return pairs[composite_id]

    # ---------- mandatory API ----------
    def add(self, obj: Any) -> int:
        # All writes go to local
        self.local.add(obj)
        return self.count() - 1

    def add(self, obj: Any) -> int:
        # Compute composite index without scanning pairs
        base_active  = self._active_count_fast("base")
        local_active = self._active_count_fast("local")
        self.local.add(obj)
        return base_active + local_active


    def add_many(self, objs: Sequence[Any]) -> List[int]:
        """
        Add multiple objects at once to the *local* store (RW) using its bulk path if available.
        Returns the composite IDs of the newly added objects (in the same order as `objs`).

        Assumptions:
        - local.add_many returns backend IDs (ascending/new at end; SQLite AUTOINCREMENT).
        - Composite ordering: [active base asc] + [active local asc].
        """
        # Fast path: local backend supports bulk ingest
        bulk = getattr(self.local, "add_many", None)
        if callable(bulk):
            # Compute where the new block will appear in composite space
            base_active = self._active_count_fast("base")
            local_active_before = self._active_count_fast("local")

            new_local_ids = bulk(objs)  # backend IDs; may be needed by callers elsewhere
            # Composite IDs are contiguous at the end of the local-active block
            start = base_active + local_active_before
            return list(range(start, start + len(new_local_ids)))

        # Fallback: no bulk support; degrade gracefully while preserving IDs
        base_active = self._active_count_fast("base")
        local_active_before = self._active_count_fast("local")
        start = base_active + local_active_before
        comp_ids: List[int] = []
        for j, obj in enumerate(objs):
            # Route single adds directly to local (don’t call self.add to avoid O(N) count())
            self.local.add(obj)
            comp_ids.append(start + j)
        return comp_ids

    def get(self, obj_id: Optional[int] = None):
        if obj_id is None:
            # Return a lazy view over the composite
            return _LazyContainerView(self)
        part, bid = self._resolve(int(obj_id))
        return (self.base if part == "base" else self.local).get(bid)

    def remove(self, obj_id: int) -> None:
        part, bid = self._resolve(int(obj_id))
        if part == "base":
            if not self.allow_shadow_delete:
                raise RuntimeError("Cannot remove from base store in composite view (read-only).")
            # soft delete (tombstone)
            self._base_tombs.add(bid)
        else:
            # hard delete in local
            self.local.remove(bid)

    def list_ids(self) -> List[int]:
        return list(range(self.count()))

    def count(self) -> int:
        return self._active_count_fast("base") + self._active_count_fast("local")

    def clear(self) -> None:
        """
        Clear composite view:
          - base: shadow-delete (tombstone) everything,
          - local: hard-delete everything.
        """
        # tombstone all base
        try:
            self._base_tombs = set(self.base.list_ids())
        except Exception:
            self._base_tombs = set()
        # clear local
        try:
            self.local.clear()
        except Exception:
            # fallback: remove one by one
            for lid in getattr(self.local, "list_ids", lambda: [])():
                self.local.remove(lid)
        self._local_tombs.clear()

    def get_all_hashes(self, with_ids: bool = False):
        """
        Composite view of content hashes in composite order:
        [active base objects (ASC by base id), then active local objects (ASC by local id)].

        Args:
            with_ids: if True, returns List[Tuple[int, Optional[str]]] as (composite_id, hash_or_None).
                      If an item lacks a hash, the value is None.
                      If False, returns List[Optional[str]] aligned with composite indices.
        """
        # Fetch per-store (id -> hash) maps
        def _pairs_to_dict(store):
            f = getattr(store, "get_all_hashes", None)
            if f is None:
                return {}
            try:
                return dict(f(with_ids=True))
            except TypeError:
                # fallback if backend only supports without ids
                hs = f(with_ids=False)
                # cannot align without ids; return empty to avoid misreporting
                return {}

        base_map  = _pairs_to_dict(self.base)
        local_map = _pairs_to_dict(self.local)

        out = []
        pairs = self._compose_pairs()  # already excludes tombstoned base/local
        for comp_idx, (part, bid) in enumerate(pairs):
            h = base_map.get(bid) if part == "base" else local_map.get(bid)
            if with_ids:
                out.append((comp_idx, h if isinstance(h, str) and h else None))
            else:
                out.append(h if isinstance(h, str) and h else None)
        return out


    def has_hash(self, hash_str: str) -> bool:
        target = str(hash_str)

        # Base store fast path
        finder = getattr(self.base, "find_ids_by_hash", None)
        if callable(finder):
            for oid in finder(target):
                if oid not in self._base_tombs:
                    return True
        else:
            # Fallback to the (slower) legacy path only if necessary
            if self._has_hash_slow(self.base, target, self._active_ids("base")):
                return True

        # Local store fast path
        finder = getattr(self.local, "find_ids_by_hash", None)
        if callable(finder):
            for oid in finder(target):
                if oid not in self._local_tombs:
                    return True
        else:
            if self._has_hash_slow(self.local, target, self._active_ids("local")):
                return True

        return False

    def _has_hash_slow(self, store, target: str, active_ids: list[int]) -> bool:
        """Compatibility fallback; still avoids false positives on tombstoned items."""
        f = getattr(store, "get_all_hashes", None)
        if f is None:
            return False
        try:
            pairs = dict(f(with_ids=True))  # backend_id -> hash
        except TypeError:
            return False
        for oid in active_ids:
            h = pairs.get(oid)
            if isinstance(h, str) and h == target:
                return True
        return False


    def has_hashes(self, hashes: Sequence[str]) -> Dict[str, bool]:
        """
        Vectorized membership with tombstone awareness.
        Returns: {hash -> bool} for ACTIVE objects only.
        """
        hashes = [str(h) for h in hashes]
        result = {h: False for h in hashes}

        # Base
        finder = getattr(self.base, "find_hashes", None)
        if callable(finder):
            base_hits = finder(hashes)  # hash -> [backend_ids]
            for h, ids in base_hits.items():
                if ids and any(oid not in self._base_tombs for oid in ids):
                    result[h] = True
        else:
            # fallback: singletons via has_hash (still O(k) but not O(N))
            for h in hashes:
                if self.has_hash(h):
                    result[h] = True

        # Local (only fill remaining False)
        remaining = [h for h, ok in result.items() if not ok]
        if remaining:
            finder = getattr(self.local, "find_hashes", None)
            if callable(finder):
                loc_hits = finder(remaining)
                for h, ids in loc_hits.items():
                    if ids and any(oid not in self._local_tombs for oid in ids):
                        result[h] = True
            else:
                for h in remaining:
                    if self.has_hash(h):
                        result[h] = True

        return result
        
    # ---------- optional / metadata-aware ----------
    def get_meta(self, obj_id: int) -> Dict[str, Any]:
        part, bid = self._resolve(int(obj_id))
        getter = getattr(self.base if part == "base" else self.local, "get_meta", None)
        if getter is None:
            raise NotImplementedError("Underlying store does not implement get_meta")
        return getter(bid)

    # pass-through iterators using composite ids
    def iter_ids(self, batch_size: Optional[int] = None) -> Iterator[int]:
        # ignore batch_size; composite space is in-memory merged
        for i in range(self.count()):
            yield i

    def iter_objects(self, batch_size: Optional[int] = None) -> Iterator[tuple[int, Any]]:
        for i in self.iter_ids(batch_size):
            yield i, self.get(i)

    # ---------- fast metadata over the union ----------
    def get_species_universe(self, order: str = "stored") -> List[str]:
        # union of species; for 'stored', take base order then append locals not in base, preserving each store's order
        def _syms(store) -> List[str]:
            f = getattr(store, "get_species_universe", None)
            if f is not None:
                try:
                    return f(order="stored")
                except Exception:
                    pass
            # slow fallback
            syms = set()
            for _, obj in getattr(store, "iter_objects", lambda: [])():
                apm = getattr(obj, "AtomPositionManager", None)
                if apm is None: continue
                labels = getattr(apm, "atomLabelsList", None)
                if labels is None: continue
                lab_list = labels.tolist() if hasattr(labels, "tolist") else labels
                for s in lab_list:
                    syms.add(str(s))
            return sorted(syms)

        b = _syms(self.base)
        l = _syms(self.local)
        if order == "alphabetical":
            return sorted(set(b) | set(l))
        seen = set(b)
        tail = [s for s in l if s not in seen]
        return list(b) + tail

    def get_species_mapping(self, order: str = "stored") -> Dict[str, int]:
        syms = self.get_species_universe(order=order)
        return {s: i for i, s in enumerate(syms)}

    def _active_ids(self, part: str) -> List[int]:
        if part == "base":
            ids = getattr(self.base, "list_ids", lambda: [])()
            return [i for i in ids if i not in self._base_tombs]
        else:
            ids = getattr(self.local, "list_ids", lambda: [])()
            return [i for i in ids if i not in self._local_tombs]

    def get_all_compositions(
        self,
        species_order: Optional[Sequence[str]] = None,
        return_species: bool = False,
        order: str = "stored",
    ):
        import numpy as _np

        # combined species order
        if species_order is None:
            species_order = self.get_species_universe(order=order)
        species_order = list(species_order)
        m = len(species_order)
        sp2col = {sp: j for j, sp in enumerate(species_order)}

        def _fetch_align(store, tombs: set[int]):
            ids_all = getattr(store, "list_ids", lambda: [])()
            id2row = {oid: i for i, oid in enumerate(ids_all)}
            active = [oid for oid in ids_all if oid not in tombs]
            f = getattr(store, "get_all_compositions", None)
            if f is None:
                return np.zeros((0, m), dtype=float)
            M_store, sp_store = f(species_order=None, return_species=True, order=order)
            if M_store.size == 0 or len(ids_all) == 0 or len(sp_store) == 0:
                return np.zeros((0, m), dtype=float)
            rows = [id2row[oid] for oid in active]
            Ms = M_store[rows, :] if rows else np.zeros((0, len(sp_store)), dtype=float)
            out = np.zeros((Ms.shape[0], m), dtype=float)
            for j_old, sp in enumerate(sp_store):
                j_new = sp2col.get(sp)
                if j_new is not None:
                    out[:, j_new] = Ms[:, j_old]
            return out

        Mb = _fetch_align(self.base, self._base_tombs)
        Ml = _fetch_align(self.local, self._local_tombs)
        M = Ml if Mb.size == 0 else (Mb if Ml.size == 0 else np.vstack([Mb, Ml]))
        return (M, species_order) if return_species else M

    def get_scalar_keys_universe(self) -> List[str]:
        keys = set()
        for store in (self.base, self.local):
            f = getattr(store, "get_scalar_keys_universe", None)
            if f is not None:
                try:
                    keys.update(map(str, f()))
                except Exception:
                    pass
        return sorted(keys)

    def get_all_scalars(self, keys: Optional[Sequence[str]] = None, return_keys: bool = False):
        if keys is None:
            keys = self.get_scalar_keys_universe()
        keys = list(keys)
        m = len(keys)
        k2col = {k: j for j, k in enumerate(keys)}

        def _fetch_align(store, tombs: set[int]):
            ids_all = getattr(store, "list_ids", lambda: [])()
            id2row = {oid: i for i, oid in enumerate(ids_all)}
            active = [oid for oid in ids_all if oid not in tombs]
            f = getattr(store, "get_all_scalars", None)
            if f is None:
                return np.zeros((0, m), dtype=float)
            A_store, k_store = f(keys=None, return_keys=True)
            if A_store.size == 0 or len(ids_all) == 0:
                return np.zeros((0, m), dtype=float)
            rows = [id2row[oid] for oid in active]
            As = A_store[rows, :] if rows else np.zeros((0, A_store.shape[1]), dtype=float)
            out = np.full((As.shape[0], m), np.nan, dtype=float)
            kmap = {key: j for j, key in enumerate(k_store)}
            for key, j_new in k2col.items():
                j_old = kmap.get(key)
                if j_old is not None:
                    out[:, j_new] = As[:, j_old]
            return out

        Ab = _fetch_align(self.base, self._base_tombs)
        Al = _fetch_align(self.local, self._local_tombs)
        A = Al if Ab.size == 0 else (Ab if Al.size == 0 else np.vstack([Ab, Al]))
        return (A, keys) if return_keys else A

    def get_all_energies(self) -> np.ndarray:
        """
        Devuelve un vector 1D concatenando (base_activos, local_activos) con la energía por objeto.
        Prioridad de claves escalares: E > energy > Etot > Ef > free_energy.
        Si falta, cae a objects.energy del backend.
        """

        PRIORITY = ["E", "energy", "Etot", "Ef", "free_energy"]

        def _energies_from_store(store, tombs: set[int]) -> np.ndarray:
            # ids del store en orden estable (objects.id ASC)
            ids_all = getattr(store, "list_ids", lambda: [])()
            if not ids_all:
                return np.zeros((0,), dtype=float)

            # filas activas (no tombstoned)
            active_rows = [i for i, oid in enumerate(ids_all) if oid not in tombs]

            # 1) Intentar con get_all_scalars(keys=PRIORITY)
            g = getattr(store, "get_all_scalars", None)
            e = None
            if g is not None:
                A_store, k_store = g(keys=PRIORITY, return_keys=True)
                if A_store.size:
                    # seleccionar solo filas activas
                    As = A_store[active_rows, :] if active_rows else np.zeros((0, A_store.shape[1]), dtype=float)
                    e = np.full((As.shape[0],), np.nan, dtype=float)
                    # completar por prioridad
                    kpos = {k: j for j, k in enumerate(k_store)}
                    for key in PRIORITY:
                        j = kpos.get(key)
                        if j is None:  # esa columna no existe en este store
                            continue
                        mask = np.isnan(e) & ~np.isnan(As[:, j])
                        if mask.any():
                            e[mask] = As[mask, j]

            # 2) Fallback a objects.energy del backend
            if e is None or np.isnan(e).any():
                f = getattr(store, "get_all_energies", None)
                if f is not None:
                    v = np.asarray(f(), dtype=float)
                    # v viene ordenado por objects.id ASC (mismo orden que ids_all)
                    if v.size == len(ids_all):
                        v = v[active_rows]
                        if e is None:
                            e = v
                        else:
                            # rellenar NaNs con la columna de objects.energy
                            nan_mask = np.isnan(e) & ~np.isnan(v)
                            if nan_mask.any():
                                e[nan_mask] = v[nan_mask]

            if e is None:
                # nada disponible
                return np.zeros((0,), dtype=float)
            return e

        eb = _energies_from_store(self.base,  self._base_tombs)
        el = _energies_from_store(self.local, self._local_tombs)
        if eb.size == 0:
            return el
        if el.size == 0:
            return eb
        return np.concatenate([eb, el], axis=0)

    # optional passthroughs
    def set_meta(self, obj_id: int, meta: Dict[str, Any]) -> None:  # pragma: no cover
        part, bid = self._resolve(int(obj_id))
        setter = getattr(self.base if part == "base" else self.local, "set_meta", None)
        if setter is None:
            raise NotImplementedError("Underlying store does not implement set_meta")
        return setter(bid, meta)

    def query_ids(self, where: str, params: Sequence[Any] = ()) -> List[int]:  # pragma: no cover
        # Not implemented for composite; could be added by union over both stores
        raise NotImplementedError("query_ids is not supported on CompositeHybridStorage")



def merge_hybrid_stores(main_root: str, agent_roots: Sequence[str]) -> None:
    """
    One-shot consolidation of multiple HybridStorage roots into a single main root.
    - Copies rows in SQLite tables (objects, compositions, scalars).
    - Rewrites species references using the symbol (robust to different species_id mappings).
    - Copies HDF5 payloads (pickled objects) to new autoincremented IDs in main.
    - Commits per agent; safe to run once after all agents finish.

    Parameters
    ----------
    main_root : str
        Target HybridStorage root directory to consolidate into (must be writable).
    agent_roots : Sequence[str]
        List of source HybridStorage root directories produced by agents.

    Notes
    -----
    * This function does NOT deduplicate payloads. If you need de-dup, add a
      content hash (e.g., SHA-256 of the payload) to meta_json and skip repeats.
    * Do not run concurrently from multiple processes.
    """
    main_root_abs = os.path.abspath(main_root)
    main = HybridStorage(main_root_abs)  # opens RW in your current implementation
    try:
        cur_main = main._conn.cursor()

        for agent_root in agent_roots:
            if agent_root is None:
                continue
            agent_root_abs = os.path.abspath(agent_root)
            # Skip accidental self-merge
            if agent_root_abs == main_root_abs:
                continue
            # Skip non-existent or empty roots gracefully
            if not os.path.isdir(agent_root_abs):
                continue

            agent = None
            try:
                agent = HybridStorage(agent_root_abs)  # opens RW in current code; we'll only read
                cur_agent = agent._conn.cursor()

                # Iterate agent objects in stable order
                cur_agent.execute(
                    "SELECT id, energy, natoms, formula, meta_json "
                    "FROM objects ORDER BY id ASC;"
                )
                rows = cur_agent.fetchall()
                if not rows:
                    continue

                # Single transaction per agent for speed and atomicity
                cur_main.execute("BEGIN;")

                for oid, energy, natoms, formula, meta_json in rows:
                    # 1) Insert into main.objects
                    cur_main.execute(
                        "INSERT INTO objects (energy, natoms, formula, meta_json) VALUES (?,?,?,?);",
                        (energy, natoms, formula, meta_json),
                    )
                    new_id = int(cur_main.lastrowid)

                    # 2) compositions: remap by symbol → species_id in main
                    cur_agent.execute(
                        """
                        SELECT s.symbol, c.count
                        FROM compositions c
                        JOIN species s ON s.species_id = c.species_id
                        WHERE c.object_id = ?;
                        """,
                        (int(oid),),
                    )
                    comp_rows = cur_agent.fetchall()
                    if comp_rows:
                        rows_to_insert = []
                        for sym, ct in comp_rows:
                            spid = main._ensure_species(sym)  # creates if missing
                            rows_to_insert.append((new_id, spid, float(ct)))
                        cur_main.executemany(
                            "INSERT INTO compositions(object_id, species_id, count) VALUES (?,?,?);",
                            rows_to_insert,
                        )

                    # 3) scalars: straight copy
                    cur_agent.execute(
                        "SELECT key, value FROM scalars WHERE object_id = ?;",
                        (int(oid),),
                    )
                    scal_rows = cur_agent.fetchall()
                    if scal_rows:
                        cur_main.executemany(
                            "INSERT INTO scalars(object_id, key, value) VALUES (?,?,?);",
                            [(new_id, k, v) for (k, v) in scal_rows],
                        )

                    # 4) payload: load from agent HDF5, store in main HDF5
                    obj = agent.get(int(oid))
                    main._save_payload_h5(new_id, obj)

                # Commit per agent and flush datasets
                main._conn.commit()
                main._h5.flush()

            finally:
                if agent is not None:
                    agent.close()

    finally:
        main.close()
