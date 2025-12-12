import json
import sqlite3
import tempfile
from pathlib import Path

from core.cache import Cache


def test_cache_set_get():
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "cache.db"
        cache = Cache(db_path=db)

        cache.set("key1", {"a": 1}, revision="rev123")
        value = cache.get("key1", revision="rev123")

        assert value == {"a": 1}


def test_cache_revision_mismatch():
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "cache.db"
        cache = Cache(db_path=db)

        cache.set("k", {"x": 1}, revision="revA")

        v = cache.get("k", revision="revB")
        assert v is None


def test_cache_json_corruption():
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "cache.db"
        cache = Cache(db_path=db)

        conn = sqlite3.connect(db)
        conn.execute(
            "INSERT INTO cache (key, data, revision, ts) VALUES (?, ?, ?, ?)",
            ("bad", "{ invalid json", "rev", 0)
        )
        conn.commit()

        assert cache.get("bad", revision="rev") is None
