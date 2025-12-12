"""
Abstract storage interface for cache backends.

This module defines the base interface that all storage backends must implement,
enabling pluggable storage (SQLite, Redis, etc.) with consistent behavior.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class CacheStorage(ABC):
    """
    Abstract base class for cache storage backends.

    All storage backends (SQLite, Redis, etc.) must implement this interface
    to ensure consistent cache behavior and enable easy backend switching.

    The storage layer is responsible for:
    - Storing and retrieving cached LLM responses
    - Tracking access times for LRU eviction
    - Managing cache size limits
    - Providing statistics and monitoring data
    """

    def __init__(self, max_size: int = 1000):
        """
        Initialize storage backend.

        Args:
            max_size: Maximum number of cache entries before eviction starts
        """
        self.max_size = max_size

    @abstractmethod
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached response by key.

        This method should automatically update the access time for LRU tracking.

        Args:
            key: Cache key (SHA256 hash from key_generator)

        Returns:
            Cached response dict if found, None if cache miss

        Example:
            >>> storage = SQLiteStorage()
            >>> response = storage.get("abc123...")
            >>> if response:
            ...     print(response["choices"][0]["message"])
        """
        pass

    @abstractmethod
    def set(
        self, key: str, value: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Store response with key.

        Should handle LRU eviction automatically if cache is at max_size.
        Stores both the response value and optional metadata.

        Args:
            key: Cache key (SHA256 hash)
            value: Response data to cache (full API response)
            metadata: Optional metadata (provider, model, timestamps, etc.)

        Example:
            >>> storage.set(
            ...     "abc123...",
            ...     {"choices": [{"message": {"content": "Hello"}}]},
            ...     {"provider": "openai", "model": "gpt-4"}
            ... )
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """
        Remove entry from cache.

        Args:
            key: Cache key to delete

        Returns:
            True if entry was deleted, False if key didn't exist

        Example:
            >>> storage.delete("abc123...")
            True
        """
        pass

    @abstractmethod
    def update_access_time(self, key: str) -> None:
        """
        Update last access time for LRU tracking.

        Called automatically by get() method. Can also be called manually
        to mark an entry as recently used without retrieving it.

        Args:
            key: Cache key to update

        Example:
            >>> storage.update_access_time("abc123...")
        """
        pass

    @abstractmethod
    def get_lru_key(self) -> Optional[str]:
        """
        Get least recently used key for eviction.

        Returns the cache key that was accessed longest ago.
        Used during eviction to determine which entry to remove.

        Returns:
            Cache key of LRU entry, or None if cache is empty

        Example:
            >>> lru_key = storage.get_lru_key()
            >>> if lru_key:
            ...     storage.delete(lru_key)
        """
        pass

    @abstractmethod
    def get_size(self) -> int:
        """
        Get current number of cached entries.

        Returns:
            Number of entries currently in cache

        Example:
            >>> storage.get_size()
            42
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Clear all cache entries.

        Removes all cached responses and resets the cache to empty state.

        Example:
            >>> storage.clear()
            >>> storage.get_size()
            0
        """
        pass

    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns various statistics about cache usage, hit rates, etc.

        Returns:
            Dict containing statistics:
            - size: Current number of entries
            - max_size: Maximum capacity
            - hits: Number of cache hits (if tracked)
            - misses: Number of cache misses (if tracked)
            - hit_rate: Cache hit rate percentage (if tracked)
            - oldest_entry: Timestamp of oldest entry (if available)
            - newest_entry: Timestamp of newest entry (if available)

        Example:
            >>> stats = storage.get_stats()
            >>> print(f"Cache hit rate: {stats.get('hit_rate', 0):.1f}%")
        """
        pass

    def evict_lru(self) -> bool:
        """
        Evict the least recently used entry.

        Helper method that combines get_lru_key() and delete().
        Called automatically by set() when cache is full.

        Returns:
            True if an entry was evicted, False if cache was empty

        Example:
            >>> storage.evict_lru()
            True
        """
        lru_key = self.get_lru_key()
        if lru_key:
            return self.delete(lru_key)
        return False

    def is_full(self) -> bool:
        """
        Check if cache is at capacity.

        Returns:
            True if cache size >= max_size, False otherwise

        Example:
            >>> if storage.is_full():
            ...     storage.evict_lru()
        """
        return self.get_size() >= self.max_size
