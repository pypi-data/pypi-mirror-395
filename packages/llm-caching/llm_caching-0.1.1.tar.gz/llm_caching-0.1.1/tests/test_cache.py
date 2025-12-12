"""
Unit tests for cache layer (key generation, SQLite storage, configuration).
"""

import os
import tempfile
from pathlib import Path

import pytest

from llm_cache.cache.key_generator import generate_cache_key, normalize_request_params
from llm_cache.cache.sqlite_storage import SQLiteStorage
from llm_cache.config import Config


class TestKeyGenerator:
    """Test cache key generation."""

    def test_deterministic_key_generation(self):
        """Same inputs should always generate the same key."""
        key1 = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
            temperature=0.7,
        )
        key2 = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
            temperature=0.7,
        )
        assert key1 == key2
        assert len(key1) == 64  # SHA256 produces 64 hex characters

    def test_different_prompts_different_keys(self):
        """Different prompts should generate different keys."""
        key1 = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
        )
        key2 = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "Goodbye"}],
        )
        assert key1 != key2

    def test_different_temperature_different_keys(self):
        """Different temperatures should generate different keys."""
        key1 = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
            temperature=0.7,
        )
        key2 = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
            temperature=0.8,
        )
        assert key1 != key2

    def test_different_model_different_keys(self):
        """Different models should generate different keys."""
        key1 = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
        )
        key2 = generate_cache_key(
            provider="openai",
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
        )
        assert key1 != key2

    def test_provider_case_insensitive(self):
        """Provider names should be case-insensitive."""
        key1 = generate_cache_key(
            provider="OpenAI",
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
        )
        key2 = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
        )
        assert key1 == key2

    def test_string_prompt_conversion(self):
        """String prompts should be converted to message format."""
        key1 = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages="Hello",
        )
        key2 = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
        )
        assert key1 == key2

    def test_sampling_parameters_affect_key(self):
        """Sampling parameters should affect cache key."""
        key1 = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
            top_p=0.9,
        )
        key2 = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
            top_p=0.95,
        )
        assert key1 != key2

    def test_normalize_request_params(self):
        """normalize_request_params should exclude sensitive data."""
        request = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "Hi"}],
            "temperature": 0.7,
            "api_key": "secret-key",
            "user": "user123",
            "stream": True,
        }
        normalized = normalize_request_params(request)

        assert "api_key" not in normalized
        assert "user" not in normalized
        assert "stream" not in normalized
        assert normalized["model"] == "gpt-4"
        assert normalized["temperature"] == 0.7


class TestSQLiteStorage:
    """Test SQLite storage backend."""

    @pytest.fixture
    def storage(self):
        """Create temporary SQLite storage for testing."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as f:
            db_path = f.name

        storage = SQLiteStorage(db_path=db_path, max_size=5)
        yield storage

        # Cleanup
        Path(db_path).unlink(missing_ok=True)

    def test_set_and_get(self, storage):
        """Test basic set and get operations."""
        key = "test_key"
        value = {"response": "Hello, world!"}

        storage.set(key, value)
        retrieved = storage.get(key)

        assert retrieved == value

    def test_get_nonexistent_key(self, storage):
        """Getting nonexistent key should return None."""
        result = storage.get("nonexistent")
        assert result is None

    def test_cache_size(self, storage):
        """Test get_size method."""
        assert storage.get_size() == 0

        storage.set("key1", {"data": "value1"})
        assert storage.get_size() == 1

        storage.set("key2", {"data": "value2"})
        assert storage.get_size() == 2

    def test_lru_eviction(self, storage):
        """Test LRU eviction when cache is full."""
        # Fill cache to max_size (5)
        for i in range(5):
            storage.set(f"key{i}", {"data": f"value{i}"})

        assert storage.get_size() == 5

        # Access key0 to make it recently used
        storage.get("key0")

        # Add new entry, should evict key1 (least recently used)
        storage.set("key5", {"data": "value5"})

        assert storage.get_size() == 5
        assert storage.get("key0") is not None  # Still in cache
        assert storage.get("key1") is None  # Evicted
        assert storage.get("key5") is not None  # New entry

    def test_update_access_time(self, storage):
        """Test that accessing updates LRU order."""
        storage.set("key1", {"data": "value1"})
        storage.set("key2", {"data": "value2"})
        storage.set("key3", {"data": "value3"})

        # Access key1 to make it recently used
        storage.get("key1")

        lru_key = storage.get_lru_key()
        assert lru_key == "key2"  # key2 is now LRU

    def test_delete(self, storage):
        """Test delete operation."""
        storage.set("key1", {"data": "value1"})
        assert storage.get("key1") is not None

        deleted = storage.delete("key1")
        assert deleted is True
        assert storage.get("key1") is None
        assert storage.get_size() == 0

    def test_delete_nonexistent(self, storage):
        """Deleting nonexistent key should return False."""
        deleted = storage.delete("nonexistent")
        assert deleted is False

    def test_clear(self, storage):
        """Test clear operation."""
        for i in range(3):
            storage.set(f"key{i}", {"data": f"value{i}"})

        assert storage.get_size() == 3

        storage.clear()

        assert storage.get_size() == 0
        assert storage.get("key0") is None

    def test_stats_tracking(self, storage):
        """Test statistics tracking."""
        storage.set("key1", {"data": "value1"})

        # Cache miss
        storage.get("nonexistent")
        # Cache hit
        storage.get("key1")
        # Cache hit
        storage.get("key1")

        stats = storage.get_stats()

        assert stats["size"] == 1
        assert stats["max_size"] == 5
        assert stats["hits"] == 2
        assert stats["misses"] == 1
        assert stats["total_requests"] == 3
        assert stats["hit_rate"] == 66.67

    def test_metadata_storage(self, storage):
        """Test storing metadata with cache entries."""
        key = "key1"
        value = {"response": "data"}
        metadata = {"provider": "openai", "model": "gpt-4"}

        storage.set(key, value, metadata=metadata)
        retrieved = storage.get(key)

        assert retrieved == value
        # Metadata is stored but not returned by get (could be added if needed)


class TestConfig:
    """Test configuration management."""

    def test_default_config(self):
        """Test default configuration values."""
        # Clear environment variables
        for key in os.environ.keys():
            if key.startswith("LLM_CACHE_"):
                del os.environ[key]

        config = Config()

        assert config.backend == "sqlite"
        assert config.max_size == 1000
        assert config.sqlite_path == "./llm_cache.db"
        assert config.redis_host == "localhost"
        assert config.redis_port == 6379
        assert config.proxy_port == 8000
        assert config.proxy_host == "0.0.0.0"

    def test_custom_config_from_env(self, monkeypatch):
        """Test loading configuration from environment variables."""
        monkeypatch.setenv("LLM_CACHE_BACKEND", "redis")
        monkeypatch.setenv("LLM_CACHE_MAX_SIZE", "2000")
        monkeypatch.setenv("LLM_CACHE_REDIS_HOST", "redis.example.com")
        monkeypatch.setenv("LLM_CACHE_PROXY_PORT", "9000")

        config = Config()

        assert config.backend == "redis"
        assert config.max_size == 2000
        assert config.redis_host == "redis.example.com"
        assert config.proxy_port == 9000

    def test_invalid_backend_raises_error(self, monkeypatch):
        """Test that invalid backend raises ValueError."""
        monkeypatch.setenv("LLM_CACHE_BACKEND", "invalid")

        with pytest.raises(ValueError, match="Invalid LLM_CACHE_BACKEND"):
            Config()

    def test_invalid_max_size_raises_error(self, monkeypatch):
        """Test that invalid max_size raises ValueError."""
        monkeypatch.setenv("LLM_CACHE_MAX_SIZE", "-100")

        with pytest.raises(ValueError, match="must be positive"):
            Config()

    def test_invalid_port_raises_error(self, monkeypatch):
        """Test that invalid port raises ValueError."""
        monkeypatch.setenv("LLM_CACHE_PROXY_PORT", "99999")

        with pytest.raises(ValueError, match="Invalid LLM_CACHE_PROXY_PORT"):
            Config()

    def test_get_storage_sqlite(self):
        """Test getting SQLite storage from config."""
        config = Config()
        storage = config.get_storage()

        assert isinstance(storage, SQLiteStorage)
        assert storage.max_size == config.max_size

    def test_config_to_dict(self):
        """Test config serialization to dict."""
        config = Config()
        config_dict = config.to_dict()

        assert config_dict["backend"] == "sqlite"
        assert config_dict["max_size"] == 1000
        assert config_dict["proxy"]["port"] == 8000

    def test_config_repr(self):
        """Test config string representation."""
        config = Config()
        repr_str = repr(config)

        assert "sqlite" in repr_str
        assert "1000" in repr_str
        assert "8000" in repr_str
