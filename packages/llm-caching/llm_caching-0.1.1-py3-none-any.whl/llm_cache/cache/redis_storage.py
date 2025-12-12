"""
Redis storage backend for LLM cache.

Provides distributed caching with LRU eviction, ideal for production
deployments and team sharing.
"""

import json
from datetime import datetime
from typing import Any, Dict, Optional

import redis

from llm_cache.cache.storage import CacheStorage


class RedisStorage(CacheStorage):
    """
    Redis-based cache storage with LRU eviction.

    Features:
    - Distributed caching across multiple instances
    - Persistent storage (with Redis persistence)
    - Sorted sets for efficient LRU operations
    - Atomic operations
    - Team collaboration (shared cache)
    - Hit/miss statistics

    Storage Strategy:
        - Main data: Redis hashes (llm_cache:{key})
        - LRU index: Redis sorted set (llm_cache:lru) with timestamps as scores
        - Statistics: Redis hash (llm_cache:stats)

    Example:
        >>> storage = RedisStorage(host="localhost", port=6379, max_size=10000)
        >>> storage.set("abc123", {"response": "data"})
        >>> cached = storage.get("abc123")
        >>> print(storage.get_stats())
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        max_size: int = 1000,
    ):
        """
        Initialize Redis storage backend.

        Args:
            host: Redis server host
            port: Redis server port
            db: Redis database number (0-15)
            password: Redis password (optional)
            max_size: Maximum number of cache entries
        """
        super().__init__(max_size)

        # Initialize Redis client
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True,  # Automatically decode bytes to strings
            socket_connect_timeout=5,
            socket_timeout=5,
        )

        # Test connection
        try:
            self.redis_client.ping()
        except redis.ConnectionError as e:
            raise ConnectionError(
                f"Failed to connect to Redis at {host}:{port}: {e}"
            ) from e

        # Key prefixes
        self.KEY_PREFIX = "llm_cache:"
        self.LRU_ZSET = "llm_cache:lru"
        self.STATS_KEY = "llm_cache:stats"

        # Initialize stats if not exists
        self._init_stats()

    def _init_stats(self) -> None:
        """Initialize statistics tracking."""
        if not self.redis_client.exists(self.STATS_KEY):
            self.redis_client.hset(self.STATS_KEY, mapping={"hits": 0, "misses": 0})

    def _update_stats(self, hit: bool) -> None:
        """Update hit/miss statistics."""
        stat_key = "hits" if hit else "misses"
        self.redis_client.hincrby(self.STATS_KEY, stat_key, 1)

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached response by key.

        Automatically updates access time and increments access count.

        Args:
            key: Cache key

        Returns:
            Cached response dict or None if not found
        """
        full_key = self.KEY_PREFIX + key

        # Get value from Redis
        value = self.redis_client.hget(full_key, "value")

        if value:
            self._update_stats(hit=True)
            self.update_access_time(key)
            return json.loads(value)

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

        full_key = self.KEY_PREFIX + key
        now = datetime.now().timestamp()

        # Store data in Redis hash
        self.redis_client.hset(
            full_key,
            mapping={
                "value": json.dumps(value),
                "created_at": now,
                "last_accessed": now,
                "access_count": 1,
                "metadata": json.dumps(metadata or {}),
            },
        )

        # Update LRU sorted set (score = timestamp)
        self.redis_client.zadd(self.LRU_ZSET, {key: now})

    def delete(self, key: str) -> bool:
        """
        Remove entry from cache.

        Args:
            key: Cache key

        Returns:
            True if deleted, False if key didn't exist
        """
        full_key = self.KEY_PREFIX + key

        # Use pipeline for atomic operations
        pipe = self.redis_client.pipeline()
        pipe.delete(full_key)
        pipe.zrem(self.LRU_ZSET, key)
        results = pipe.execute()

        # First result is number of keys deleted
        return results[0] > 0

    def update_access_time(self, key: str) -> None:
        """
        Update last access time and increment access count.

        Args:
            key: Cache key
        """
        full_key = self.KEY_PREFIX + key
        now = datetime.now().timestamp()

        # Use pipeline for atomic operations
        pipe = self.redis_client.pipeline()
        pipe.hset(full_key, "last_accessed", now)
        pipe.hincrby(full_key, "access_count", 1)
        pipe.zadd(self.LRU_ZSET, {key: now})
        pipe.execute()

    def get_lru_key(self) -> Optional[str]:
        """
        Get least recently used key.

        Returns:
            Cache key of LRU entry or None if cache is empty
        """
        # Get key with lowest score (oldest access time)
        keys = self.redis_client.zrange(self.LRU_ZSET, 0, 0)
        return keys[0] if keys else None

    def get_size(self) -> int:
        """
        Get current number of cached entries.

        Returns:
            Number of entries in cache
        """
        return self.redis_client.zcard(self.LRU_ZSET)

    def clear(self) -> None:
        """Clear all cache entries."""
        # Get all keys in LRU set
        keys = self.redis_client.zrange(self.LRU_ZSET, 0, -1)

        if keys:
            # Delete all cache entries
            pipe = self.redis_client.pipeline()
            for key in keys:
                pipe.delete(self.KEY_PREFIX + key)
            pipe.delete(self.LRU_ZSET)
            pipe.execute()

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dict with cache statistics including hit rate, size, etc.
        """
        # Get hits and misses
        stats = self.redis_client.hgetall(self.STATS_KEY)
        hits = int(stats.get("hits", 0))
        misses = int(stats.get("misses", 0))

        # Get size
        size = self.get_size()

        # Calculate hit rate
        total_requests = hits + misses
        hit_rate = (hits / total_requests * 100) if total_requests > 0 else 0.0

        # Get oldest and newest entries from LRU set
        oldest_entries = self.redis_client.zrange(self.LRU_ZSET, 0, 0, withscores=True)
        newest_entries = self.redis_client.zrange(
            self.LRU_ZSET, -1, -1, withscores=True
        )

        oldest_access = (
            datetime.fromtimestamp(oldest_entries[0][1]).isoformat()
            if oldest_entries
            else None
        )
        newest_access = (
            datetime.fromtimestamp(newest_entries[0][1]).isoformat()
            if newest_entries
            else None
        )

        return {
            "size": size,
            "max_size": self.max_size,
            "hits": hits,
            "misses": misses,
            "total_requests": total_requests,
            "hit_rate": round(hit_rate, 2),
            "oldest_access": oldest_access,
            "newest_access": newest_access,
            "oldest_entry": oldest_access,  # For compatibility
            "newest_entry": newest_access,  # For compatibility
        }

    def get_all_keys(self) -> list[str]:
        """
        Get all cache keys (for debugging/testing).

        Returns:
            List of all cache keys
        """
        return self.redis_client.zrange(self.LRU_ZSET, 0, -1)

    def ping(self) -> bool:
        """
        Test Redis connection.

        Returns:
            True if connected, False otherwise
        """
        try:
            return self.redis_client.ping()
        except redis.ConnectionError:
            return False
