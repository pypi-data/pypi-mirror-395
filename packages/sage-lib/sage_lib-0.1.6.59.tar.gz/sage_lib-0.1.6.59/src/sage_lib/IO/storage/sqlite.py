# ============================
# sqlite.py — SQLite (pickle BLOB) backend
# ============================
from __future__ import annotations

import os
import sqlite3
import pickle
from typing import Any, Dict, Iterator, List, Optional

from .backend import StorageBackend

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

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

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

