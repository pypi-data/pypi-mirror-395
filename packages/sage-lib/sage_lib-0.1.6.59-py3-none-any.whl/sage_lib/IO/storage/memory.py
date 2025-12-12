# ============================
# memory.py — In-memory (list/dict) backend
# ============================
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from .backend import StorageBackend, StorageType

# -----------------------------
# In-memory (list/dict) backend
# -----------------------------
class MemoryStorage(StorageBackend):
    """
    Generic in-memory storage.

    Notes
    -----
    - The container can be either a list (sequential storage) or a dict mapping
      integer IDs to objects.
    - IDs are always integers, automatically assigned if using a list.
    """

    def __init__(self, initial: StorageType | None = None) -> None:
        self._data: StorageType = initial if initial is not None else []
        self._meta: Dict[int, Dict[str, Any]] = {}

    # ---------------------------------------
    # Core CRUD interface
    # ---------------------------------------
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

