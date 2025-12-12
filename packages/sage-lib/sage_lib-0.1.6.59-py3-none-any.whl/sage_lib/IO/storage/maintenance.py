import json
import sqlite3
from typing import Optional, Tuple, List
from tqdm import tqdm  # Recommended for progress visualization

def backfill_metadata_indices(storage_backend, batch_size: int = 5000) -> dict:
    """
    Repairs and populates the 'metadata_kv' SQLite table by extracting data 
    from the existing 'meta_json' column in the 'objects' table.

    This function is necessary when migrating from an older version of the 
    HybridStorage backend where 'metadata_kv' was not automatically populated 
    during object insertion.

    Args:
        storage_backend (HybridStorage): An instance of the HybridStorage class 
                                         opened in 'rw' (read-write) mode.
        batch_size (int, optional): The number of rows to insert per SQL transaction. 
                                    Defaults to 5000.

    Returns:
        dict: A summary report containing keys:
              - 'objects_scanned': Total objects processed.
              - 'keys_inserted': Total metadata keys inserted into the index.
              - 'errors': Number of JSON parsing errors encountered.
    """
    
    # 1. Verification: Ensure the backend is writable
    if getattr(storage_backend, "read_only", False):
        raise PermissionError("Storage backend must be opened in 'rw' (read-write) mode.")

    print("Starting metadata index backfill...")
    
    conn = storage_backend._conn
    cursor = conn.cursor()
    
    # 2. Extract raw JSON payloads from the master table
    # We only need the ID and the JSON blob.
    try:
        cursor.execute("SELECT id, meta_json FROM objects ORDER BY id ASC")
    except sqlite3.Error as e:
        print(f"Critical Database Error: {e}")
        return {}

    # Fetch all rows (generators could be used for massive DBs, but fetchall is usually safe for SQLite metadata)
    rows = cursor.fetchall()
    total_objects = len(rows)
    
    kv_buffer: List[Tuple[int, str, str]] = []
    keys_inserted_count = 0
    error_count = 0
    
    print(f"Scanning {total_objects} objects for metadata...")

    # 3. Iterate through objects and parse JSON
    # We use tqdm for a progress bar, or a simple range if tqdm is not installed
    iterator = tqdm(rows, unit="obj") if 'tqdm' in globals() else rows

    for obj_id, meta_json_str in iterator:
        if not meta_json_str:
            continue

        try:
            # Parse the stored JSON blob
            meta_payload = json.loads(meta_json_str)
            
            # The 'add' method stores custom metadata under the key 'apm_metadata'
            apm_metadata = meta_payload.get("apm_metadata")

            if isinstance(apm_metadata, dict):
                # Prepare rows for the key-value table: (object_id, key, value_json)
                for key, value in apm_metadata.items():
                    # We verify the value is serializable or already a primitive
                    # The table expects the value to be a JSON string
                    serialized_val = json.dumps(value)
                    kv_buffer.append((obj_id, str(key), serialized_val))

        except (json.JSONDecodeError, TypeError):
            error_count += 1
            continue

        # 4. Batch Insertion Strategy
        # Insert in chunks to keep memory usage low and transactions atomic
        if len(kv_buffer) >= batch_size:
            _flush_buffer(cursor, kv_buffer)
            keys_inserted_count += len(kv_buffer)
            kv_buffer.clear()
            conn.commit()

    # 5. Final Flush
    if kv_buffer:
        _flush_buffer(cursor, kv_buffer)
        keys_inserted_count += len(kv_buffer)
        kv_buffer.clear()
        conn.commit()

    # 6. Final Report
    report = {
        "objects_scanned": total_objects,
        "keys_inserted": keys_inserted_count,
        "errors": error_count
    }
    
    print("\n--- Backfill Complete ---")
    print(f"Objects scanned: {report['objects_scanned']}")
    print(f"Index entries created: {report['keys_inserted']}")
    if error_count > 0:
        print(f"Parsing errors skipped: {report['errors']}")
        
    return report

def _flush_buffer(cursor: sqlite3.Cursor, data: List[Tuple[int, str, str]]) -> None:
    """
    Helper function to execute bulk inserts safely.
    Uses INSERT OR REPLACE to update existing keys if run multiple times.
    """
    try:
        cursor.executemany(
            """
            INSERT OR REPLACE INTO metadata_kv (object_id, key, value_json) 
            VALUES (?, ?, ?)
            """, 
            data
        )
    except sqlite3.Error as e:
        print(f"Warning: Batch insert failed: {e}")