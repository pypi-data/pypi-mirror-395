"""
Configuration management for llm-caching.

Loads configuration from environment variables and provides a centralized
Config class for accessing all settings.
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()


class Config:
    """
    Central configuration management for llm-caching.

    Loads settings from environment variables with sensible defaults.
    All configuration is read-only after initialization.

    Environment Variables:
        LLM_CACHE_BACKEND: Storage backend ('sqlite' or 'redis', default: 'sqlite')
        LLM_CACHE_SQLITE_PATH: SQLite database path (default: './llm_cache.db')
        LLM_CACHE_REDIS_HOST: Redis host (default: 'localhost')
        LLM_CACHE_REDIS_PORT: Redis port (default: 6379)
        LLM_CACHE_REDIS_DB: Redis database number (default: 0)
        LLM_CACHE_REDIS_PASSWORD: Redis password (optional)
        LLM_CACHE_MAX_SIZE: Maximum cache entries (default: 1000)
        LLM_CACHE_PROXY_PORT: Proxy server port (default: 8000)
        LLM_CACHE_PROXY_HOST: Proxy server host (default: '0.0.0.0')

    Example:
        >>> config = Config()
        >>> print(config.backend)  # 'sqlite'
        >>> storage = config.get_storage()
        >>> print(config.proxy_port)  # 8000
    """

    def __init__(self):
        """Initialize configuration from environment variables."""
        # Storage backend selection
        self.backend = os.getenv("LLM_CACHE_BACKEND", "sqlite").lower()

        if self.backend not in ["sqlite", "redis"]:
            raise ValueError(
                f"Invalid LLM_CACHE_BACKEND: '{self.backend}'. "
                "Must be 'sqlite' or 'redis'"
            )

        # Cache size limit
        self.max_size = int(os.getenv("LLM_CACHE_MAX_SIZE", "1000"))

        if self.max_size <= 0:
            raise ValueError(
                f"LLM_CACHE_MAX_SIZE must be positive, got {self.max_size}"
            )

        # SQLite configuration
        self.sqlite_path = os.getenv("LLM_CACHE_SQLITE_PATH", "./llm_cache.db")

        # Redis configuration
        self.redis_host = os.getenv("LLM_CACHE_REDIS_HOST", "localhost")
        self.redis_port = int(os.getenv("LLM_CACHE_REDIS_PORT", "6379"))
        self.redis_db = int(os.getenv("LLM_CACHE_REDIS_DB", "0"))
        self.redis_password = os.getenv("LLM_CACHE_REDIS_PASSWORD")

        # Proxy server configuration
        self.proxy_port = int(os.getenv("LLM_CACHE_PROXY_PORT", "8000"))
        self.proxy_host = os.getenv("LLM_CACHE_PROXY_HOST", "0.0.0.0")

        # Validate proxy configuration
        if not (1 <= self.proxy_port <= 65535):
            raise ValueError(
                f"Invalid LLM_CACHE_PROXY_PORT: {self.proxy_port}. "
                "Must be between 1 and 65535"
            )

    def get_storage(self):
        """
        Factory method to create storage backend based on configuration.

        Returns:
            CacheStorage instance (SQLiteStorage or RedisStorage)

        Raises:
            ImportError: If Redis backend is selected but redis package not available
            ConnectionError: If Redis backend can't connect to server

        Example:
            >>> config = Config()
            >>> storage = config.get_storage()
            >>> storage.set("key", {"data": "value"})
        """
        if self.backend == "redis":
            try:
                from llm_cache.cache.redis_storage import RedisStorage
            except ImportError as e:
                raise ImportError(
                    "Redis backend requires 'redis' package. "
                    "Install with: pip install redis"
                ) from e

            return RedisStorage(
                host=self.redis_host,
                port=self.redis_port,
                db=self.redis_db,
                password=self.redis_password,
                max_size=self.max_size,
            )
        else:  # Default to SQLite
            from llm_cache.cache.sqlite_storage import SQLiteStorage

            return SQLiteStorage(db_path=self.sqlite_path, max_size=self.max_size)

    def __repr__(self) -> str:
        """String representation of configuration."""
        return (
            f"Config(backend='{self.backend}', "
            f"max_size={self.max_size}, "
            f"proxy={self.proxy_host}:{self.proxy_port})"
        )

    def to_dict(self) -> dict:
        """
        Export configuration as dictionary.

        Returns:
            Dict with all configuration values (passwords masked)

        Example:
            >>> config = Config()
            >>> print(config.to_dict())
        """
        return {
            "backend": self.backend,
            "max_size": self.max_size,
            "sqlite": {
                "path": self.sqlite_path,
            },
            "redis": {
                "host": self.redis_host,
                "port": self.redis_port,
                "db": self.redis_db,
                "password": "***" if self.redis_password else None,
            },
            "proxy": {
                "host": self.proxy_host,
                "port": self.proxy_port,
            },
        }
