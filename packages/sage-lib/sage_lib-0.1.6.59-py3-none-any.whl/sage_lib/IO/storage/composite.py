# ============================
# composite.py — CompositeHybridStorage
# ============================
from __future__ import annotations

import os
from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple

import numpy as np

from .backend import StorageBackend
from .hybrid import HybridStorage

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
