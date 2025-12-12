import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Optional, Tuple


class Cache:
    """Persistent SQLite cache for Sheets responses."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = Path(db_path or Path.home() / ".innosched_cache.db")
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                revision TEXT,
                ts REAL NOT NULL
            )
        """)
        self.conn.commit()

    def get_entry(self, key: str) -> Tuple[Optional[Any], Optional[str]]:
        row = self.conn.execute(
            "SELECT data, revision FROM cache WHERE key = ?", (key,)
        ).fetchone()

        if not row:
            return None, None

        data_json, cached_revision = row

        try:
            value = json.loads(data_json)
        except (json.JSONDecodeError, TypeError, ValueError):
            # Drop corrupted entry so we don't keep failing on subsequent reads.
            self.conn.execute("DELETE FROM cache WHERE key = ?", (key,))
            self.conn.commit()
            return None, None

        return value, cached_revision

    def get(self, key: str, revision: Optional[str] = None) -> Optional[Any]:
        value, cached_revision = self.get_entry(key)

        if value is None:
            return None

        if revision and cached_revision and cached_revision != revision:
            return None

        return value

    def set(self, key: str, value: Any, revision: Optional[str]):
        data_json = json.dumps(value, ensure_ascii=False)

        self.conn.execute(
            "REPLACE INTO cache (key, data, revision, ts) VALUES (?, ?, ?, ?)",
            (key, data_json, revision, time.time())
        )
        self.conn.commit()
