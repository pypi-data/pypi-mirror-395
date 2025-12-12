"""
SQLite storage backend for LLM cache.

Provides file-based caching with LRU eviction, ideal for local development
and single-instance deployments.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from llm_cache.cache.storage import CacheStorage


class SQLiteStorage(CacheStorage):
    """
    SQLite-based cache storage with LRU eviction.

    Features:
    - File-based persistent storage
    - Indexed queries for fast LRU lookups
    - Automatic schema creation
    - Thread-safe operations
    - Access count tracking
    - Hit/miss statistics

    Storage Schema:
        key (TEXT PRIMARY KEY): Cache key (SHA256 hash)
        value (TEXT): JSON-serialized response data
        created_at (REAL): Unix timestamp of entry creation
        last_accessed (REAL): Unix timestamp of last access
        access_count (INTEGER): Number of times accessed
        metadata (TEXT): JSON-serialized metadata (provider, model, etc.)

    Example:
        >>> storage = SQLiteStorage("cache.db", max_size=1000)
        >>> storage.set("abc123", {"response": "data"})
        >>> cached = storage.get("abc123")
        >>> print(storage.get_stats())
    """

    def __init__(self, db_path: str = "llm_cache.db", max_size: int = 1000):
        """
        Initialize SQLite storage backend.

        Args:
            db_path: Path to SQLite database file
            max_size: Maximum number of cache entries
        """
        super().__init__(max_size)
        self.db_path = db_path

        # Ensure parent directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        # Statistics tracking
        self._hits = 0
        self._misses = 0

        # Initialize database schema
        self._init_db()

    def _init_db(self) -> None:
        """Initialize database schema with tables and indexes."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create main cache table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                created_at REAL NOT NULL,
                last_accessed REAL NOT NULL,
                access_count INTEGER DEFAULT 1,
                metadata TEXT
            )
        """
        )

        # Create index on last_accessed for efficient LRU queries
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_last_accessed
            ON cache(last_accessed)
        """
        )

        # Create statistics table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS stats (
                key TEXT PRIMARY KEY,
                value INTEGER DEFAULT 0
            )
        """
        )

        # Initialize stats if not exists
        cursor.execute(
            """
            INSERT OR IGNORE INTO stats (key, value)
            VALUES ('hits', 0), ('misses', 0)
        """
        )

        conn.commit()
        conn.close()

        # Load stats
        self._load_stats()

    def _load_stats(self) -> None:
        """Load statistics from database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT key, value FROM stats")
        stats = dict(cursor.fetchall())

        self._hits = stats.get("hits", 0)
        self._misses = stats.get("misses", 0)

        conn.close()

    def _update_stats(self, hit: bool) -> None:
        """Update hit/miss statistics."""
        if hit:
            self._hits += 1
            stat_key = "hits"
        else:
            self._misses += 1
            stat_key = "misses"

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE stats SET value = value + 1 WHERE key = ?", (stat_key,))
        conn.commit()
        conn.close()

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached response by key.

        Automatically updates access time and increments access count.

        Args:
            key: Cache key

        Returns:
            Cached response dict or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT value FROM cache WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()

        if row:
            self._update_stats(hit=True)
            self.update_access_time(key)
            return json.loads(row[0])

        self._update_stats(hit=False)
        return None

    def set(
        self, key: str, value: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Store response with key.

        Automatically handles LRU eviction if cache is full.

        Args:
            key: Cache key
            value: Response data to cache
            metadata: Optional metadata
        """
        # Evict LRU entry if cache is full
        if self.is_full():
            self.evict_lru()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.now().timestamp()
        value_json = json.dumps(value)
        metadata_json = json.dumps(metadata or {})

        cursor.execute(
            """
            INSERT OR REPLACE INTO cache
            (key, value, created_at, last_accessed, access_count, metadata)
            VALUES (?, ?, ?, ?, 1, ?)
        """,
            (key, value_json, now, now, metadata_json),
        )

        conn.commit()
        conn.close()

    def delete(self, key: str) -> bool:
        """
        Remove entry from cache.

        Args:
            key: Cache key

        Returns:
            True if deleted, False if key didn't exist
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM cache WHERE key = ?", (key,))
        deleted = cursor.rowcount > 0

        conn.commit()
        conn.close()

        return deleted

    def update_access_time(self, key: str) -> None:
        """
        Update last access time and increment access count.

        Args:
            key: Cache key
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.now().timestamp()
        cursor.execute(
            """
            UPDATE cache
            SET last_accessed = ?, access_count = access_count + 1
            WHERE key = ?
        """,
            (now, key),
        )

        conn.commit()
        conn.close()

    def get_lru_key(self) -> Optional[str]:
        """
        Get least recently used key.

        Returns:
            Cache key of LRU entry or None if cache is empty
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT key FROM cache
            ORDER BY last_accessed ASC
            LIMIT 1
        """
        )
        row = cursor.fetchone()
        conn.close()

        return row[0] if row else None

    def get_size(self) -> int:
        """
        Get current number of cached entries.

        Returns:
            Number of entries in cache
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM cache")
        size = cursor.fetchone()[0]

        conn.close()
        return size

    def clear(self) -> None:
        """Clear all cache entries."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM cache")

        conn.commit()
        conn.close()

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dict with cache statistics including hit rate, size, etc.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get basic stats
        size = self.get_size()

        # Get oldest and newest entries
        cursor.execute(
            """
            SELECT
                MIN(created_at) as oldest,
                MAX(created_at) as newest,
                MIN(last_accessed) as oldest_access,
                MAX(last_accessed) as newest_access
            FROM cache
        """
        )
        row = cursor.fetchone()

        oldest, newest, oldest_access, newest_access = (
            row if row else (None, None, None, None)
        )

        conn.close()

        # Calculate hit rate
        total_requests = self._hits + self._misses
        hit_rate = (self._hits / total_requests * 100) if total_requests > 0 else 0.0

        return {
            "size": size,
            "max_size": self.max_size,
            "hits": self._hits,
            "misses": self._misses,
            "total_requests": total_requests,
            "hit_rate": round(hit_rate, 2),
            "oldest_entry": (
                datetime.fromtimestamp(oldest).isoformat() if oldest else None
            ),
            "newest_entry": (
                datetime.fromtimestamp(newest).isoformat() if newest else None
            ),
            "oldest_access": (
                datetime.fromtimestamp(oldest_access).isoformat()
                if oldest_access
                else None
            ),
            "newest_access": (
                datetime.fromtimestamp(newest_access).isoformat()
                if newest_access
                else None
            ),
        }

    def get_all_keys(self) -> list[str]:
        """
        Get all cache keys (for debugging/testing).

        Returns:
            List of all cache keys
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT key FROM cache")
        keys = [row[0] for row in cursor.fetchall()]

        conn.close()
        return keys
