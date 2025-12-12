# ============================
# storage_backend.py
# ============================
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator, List, Optional, Sequence, Union, Tuple


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

