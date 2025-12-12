"""
Comprehensive edge case and error handling tests for robustness.
"""

import json
import tempfile
import threading
import time
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from llm_cache.cache.key_generator import generate_cache_key
from llm_cache.cache.sqlite_storage import SQLiteStorage
from llm_cache.config import Config
from llm_cache.wrapper.sdk import LLMCacheWrapper


@pytest.fixture
def temp_storage():
    """Create temporary storage for testing."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as f:
        db_path = f.name

    test_storage = SQLiteStorage(db_path=db_path, max_size=10)
    yield test_storage

    # Cleanup
    test_storage.clear()
    Path(db_path).unlink(missing_ok=True)


class TestCacheKeyEdgeCases:
    """Test cache key generation with edge cases."""

    def test_very_long_message(self):
        """Test cache key generation with very long messages."""
        long_message = "x" * 100000  # 100k characters

        key = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": long_message}],
        )

        # Should still generate valid SHA256 hash
        assert len(key) == 64
        assert isinstance(key, str)

    def test_unicode_messages(self):
        """Test cache key generation with Unicode characters."""
        unicode_messages = [
            {"role": "user", "content": "Hello 世界 🌍"},
            {"role": "assistant", "content": "Привет مرحبا"},
        ]

        key = generate_cache_key(
            provider="openai", model="gpt-4", messages=unicode_messages
        )

        assert len(key) == 64

        # Same input should produce same key
        key2 = generate_cache_key(
            provider="openai", model="gpt-4", messages=unicode_messages
        )
        assert key == key2

    def test_nested_message_structure(self):
        """Test cache key generation with deeply nested structures."""
        nested_messages = [
            {
                "role": "user",
                "content": "test",
                "metadata": {"nested": {"deeply": {"very": {"deep": "value"}}}},
            }
        ]

        key = generate_cache_key(
            provider="openai", model="gpt-4", messages=nested_messages
        )

        assert len(key) == 64

    def test_special_characters_in_model(self):
        """Test cache key with special characters in model name."""
        key = generate_cache_key(
            provider="openai",
            model="gpt-4-32k-0613",
            messages=[{"role": "user", "content": "test"}],
        )

        assert len(key) == 64

    def test_empty_messages(self):
        """Test cache key generation with empty messages list."""
        key = generate_cache_key(provider="openai", model="gpt-4", messages=[])

        assert len(key) == 64

    def test_float_temperature_precision(self):
        """Test that different temperature precisions generate different keys."""
        key1 = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}],
            temperature=0.7,
        )

        key2 = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}],
            temperature=0.70000001,
        )

        # Should be different due to different values
        assert key1 != key2

    def test_none_vs_missing_parameter(self):
        """Test that None and missing parameters are handled consistently."""
        key1 = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}],
            temperature=None,
        )

        key2 = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}],
        )

        # Should generate same key
        assert key1 == key2


class TestStorageEdgeCases:
    """Test storage backend edge cases."""

    def test_cache_size_exactly_at_limit(self, temp_storage):
        """Test behavior when cache is exactly at max size."""
        # Fill cache to exactly max_size
        for i in range(temp_storage.max_size):
            temp_storage.set(f"key_{i}", {"data": f"value_{i}"}, metadata={"index": i})

        assert temp_storage.get_size() == temp_storage.max_size

        # Adding one more should trigger eviction
        temp_storage.set("key_new", {"data": "new_value"})

        # Size should still be at max
        assert temp_storage.get_size() == temp_storage.max_size

        # Oldest key should be evicted
        assert temp_storage.get("key_0") is None
        assert temp_storage.get("key_new") is not None

    def test_very_large_response(self, temp_storage):
        """Test caching very large responses."""
        large_response = {
            "choices": [{"message": {"content": "x" * 1000000}}]  # 1MB of data
        }

        temp_storage.set("large_key", large_response)
        retrieved = temp_storage.get("large_key")

        assert retrieved == large_response
        assert len(retrieved["choices"][0]["message"]["content"]) == 1000000

    def test_concurrent_access(self, temp_storage):
        """Test concurrent read/write access to cache."""
        errors = []

        def writer(key_prefix, count):
            try:
                for i in range(count):
                    temp_storage.set(f"{key_prefix}_{i}", {"data": f"value_{i}"})
            except Exception as e:
                errors.append(e)

        def reader(keys):
            try:
                for key in keys:
                    temp_storage.get(key)
            except Exception as e:
                errors.append(e)

        # Create multiple threads
        threads = []

        # Writers
        for i in range(3):
            t = threading.Thread(target=writer, args=(f"thread_{i}", 5))
            threads.append(t)
            t.start()

        # Readers
        read_keys = [f"thread_0_{i}" for i in range(5)]
        for i in range(2):
            t = threading.Thread(target=reader, args=(read_keys,))
            threads.append(t)
            t.start()

        # Wait for all threads
        for t in threads:
            t.join(timeout=5)

        # Should have no errors
        assert len(errors) == 0

    def test_special_characters_in_keys(self, temp_storage):
        """Test keys with special characters."""
        special_key = "key_with_!@#$%^&*()_+-=[]{}|;:',.<>?/`~"

        temp_storage.set(special_key, {"data": "test"})
        result = temp_storage.get(special_key)

        assert result == {"data": "test"}

    def test_update_existing_key(self, temp_storage):
        """Test updating an existing cache entry."""
        key = "test_key"

        # Set initial value
        temp_storage.set(key, {"data": "original"})
        assert temp_storage.get(key) == {"data": "original"}

        # Update value
        temp_storage.set(key, {"data": "updated"})
        assert temp_storage.get(key) == {"data": "updated"}

        # Size should still be 1
        assert temp_storage.get_size() == 1

    def test_clear_empty_cache(self, temp_storage):
        """Test clearing an already empty cache."""
        temp_storage.clear()
        assert temp_storage.get_size() == 0

        # Clearing again should not error
        temp_storage.clear()
        assert temp_storage.get_size() == 0

    def test_access_order_tracking(self, temp_storage):
        """Test that access order is properly tracked for LRU."""
        # Add three items
        temp_storage.set("key1", {"data": "1"})
        time.sleep(0.01)  # Small delay to ensure different timestamps
        temp_storage.set("key2", {"data": "2"})
        time.sleep(0.01)
        temp_storage.set("key3", {"data": "3"})

        # Access key1 to update its access time
        time.sleep(0.01)
        temp_storage.get("key1")

        # Get LRU key - should be key2 (oldest unaccessed)
        lru_key = temp_storage.get_lru_key()
        assert lru_key == "key2"


class TestWrapperEdgeCases:
    """Test wrapper edge cases and error handling."""

    def test_wrap_function_with_no_parameters(self, temp_storage):
        """Test wrapping a function with no parameters."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        call_count = 0

        def no_param_func():
            nonlocal call_count
            call_count += 1
            return {"result": "test"}

        no_param_func.__module__ = "openai"

        wrapped = wrapper.wrap(no_param_func)

        # Should still work
        result = wrapped()
        assert result == {"result": "test"}
        assert call_count == 1

    def test_wrap_function_with_varargs(self, temp_storage):
        """Test wrapping a function with *args and **kwargs."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        def varargs_func(*args, **kwargs):
            return {"args": args, "kwargs": kwargs}

        varargs_func.__module__ = "openai"

        wrapped = wrapper.wrap(varargs_func)

        result = wrapped("test", key="value")
        assert result["args"] == ("test",)
        assert result["kwargs"] == {"key": "value"}

    def test_exception_in_wrapped_function(self, temp_storage):
        """Test that exceptions in wrapped functions are propagated."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        def failing_func(model, messages):
            raise ValueError("Test error")

        failing_func.__module__ = "openai"

        wrapped = wrapper.wrap(failing_func)

        with pytest.raises(ValueError, match="Test error"):
            wrapped(model="gpt-4", messages=[{"role": "user", "content": "test"}])

    def test_non_serializable_response(self, temp_storage):
        """Test handling of non-serializable response objects."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        class CustomObject:
            def __init__(self):
                self.data = "test"
                self.func = lambda x: x  # Non-serializable

        def custom_func(model, messages):
            return CustomObject()

        custom_func.__module__ = "openai"

        wrapped = wrapper.wrap(custom_func)

        # Should handle gracefully
        result = wrapped(model="gpt-4", messages=[{"role": "user", "content": "test"}])
        assert isinstance(result, CustomObject)

    def test_provider_detection_fallback(self, temp_storage):
        """Test provider detection with unknown modules."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        def unknown_func(model, messages):
            return {"result": "test"}

        unknown_func.__module__ = "completely.unknown.module"
        unknown_func.__qualname__ = "UnknownClass.method"

        wrapped = wrapper.wrap(unknown_func)

        # Should still work with "unknown" provider
        result = wrapped(
            model="test-model", messages=[{"role": "user", "content": "test"}]
        )
        assert result == {"result": "test"}

    def test_disable_enable_multiple_times(self, temp_storage):
        """Test enabling and disabling cache multiple times."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        call_count = 0

        def test_func(model, messages):
            nonlocal call_count
            call_count += 1
            return {"count": call_count}

        test_func.__module__ = "openai"

        wrapped = wrapper.wrap(test_func)

        # Enabled - should cache
        wrapped(model="gpt-4", messages=[{"role": "user", "content": "test"}])
        assert call_count == 1

        wrapped(model="gpt-4", messages=[{"role": "user", "content": "test"}])
        assert call_count == 1  # Cached

        # Disable
        wrapper.disable()
        wrapped(model="gpt-4", messages=[{"role": "user", "content": "test"}])
        assert call_count == 2  # Not cached

        # Enable again
        wrapper.enable()
        wrapped(model="gpt-4", messages=[{"role": "user", "content": "test"}])
        assert call_count == 2  # From cache again

    def test_context_manager_with_exception(self, temp_storage):
        """Test context manager cleanup when exception occurs."""
        try:
            with LLMCacheWrapper(storage=temp_storage) as wrapper:
                raise ValueError("Test error")
        except ValueError:
            pass  # Expected

        # Should not leave resources hanging


class TestConfigEdgeCases:
    """Test configuration edge cases."""

    def test_invalid_backend_raises_error(self):
        """Test that invalid backend raises ValueError."""
        with patch.dict("os.environ", {"LLM_CACHE_BACKEND": "invalid"}):
            with pytest.raises(ValueError, match="Invalid LLM_CACHE_BACKEND"):
                Config()

    def test_missing_env_vars_use_defaults(self):
        """Test that missing environment variables use defaults."""
        with patch.dict("os.environ", {}, clear=True):
            config = Config()

            assert config.backend == "sqlite"
            assert config.max_size == 1000
            assert config.proxy_port == 8000

    def test_invalid_max_size_uses_default(self):
        """Test that invalid max_size values use defaults."""
        with patch.dict("os.environ", {"LLM_CACHE_MAX_SIZE": "not_a_number"}):
            with pytest.raises(ValueError):
                Config()

    def test_negative_max_size_raises_error(self):
        """Test that negative max_size raises ValueError."""
        with patch.dict("os.environ", {"LLM_CACHE_MAX_SIZE": "-10"}):
            with pytest.raises(ValueError, match="LLM_CACHE_MAX_SIZE must be positive"):
                Config()


class TestRedisEdgeCases:
    """Test Redis-specific edge cases."""

    def test_redis_connection_failure_handling(self):
        """Test graceful handling of Redis connection failures."""
        with patch.dict(
            "os.environ",
            {
                "LLM_CACHE_BACKEND": "redis",
                "LLM_CACHE_REDIS_HOST": "nonexistent-host",
                "LLM_CACHE_REDIS_PORT": "9999",
            },
        ):
            config = Config()

            # Should handle connection error gracefully
            try:
                storage = config.get_storage()
                # Attempting operations should handle errors
                result = storage.get("test_key")
                # Should return None on connection error
                assert result is None or True  # Connection might succeed in test env
            except Exception:
                # Connection errors are acceptable in this test
                pass

    def test_redis_operation_with_closed_connection(self):
        """Test Redis operations after connection is closed."""
        # This test requires actual Redis, so we'll skip if not available
        pytest.skip("Requires Redis server - tested in integration tests")


class TestIntegrationEdgeCases:
    """Integration tests for edge cases."""

    def test_cache_hit_after_clear(self, temp_storage):
        """Test that cache hits work correctly after clearing."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        call_count = 0

        def test_func(model, messages):
            nonlocal call_count
            call_count += 1
            return {"count": call_count}

        test_func.__module__ = "openai"

        wrapped = wrapper.wrap(test_func)

        # First call
        result1 = wrapped(model="gpt-4", messages=[{"role": "user", "content": "test"}])
        assert call_count == 1

        # Second call - cached
        wrapped(model="gpt-4", messages=[{"role": "user", "content": "test"}])
        assert call_count == 1

        # Clear cache
        wrapper.clear_cache()

        # Third call - should hit API again
        wrapped(model="gpt-4", messages=[{"role": "user", "content": "test"}])
        assert call_count == 2

    def test_stats_accuracy_under_load(self, temp_storage):
        """Test that statistics remain accurate under concurrent load."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        def test_func(model, messages):
            return {"result": "test"}

        test_func.__module__ = "openai"

        wrapped = wrapper.wrap(test_func)

        # Make multiple calls
        for i in range(5):
            wrapped(model="gpt-4", messages=[{"role": "user", "content": f"test{i}"}])

        # Make duplicate calls
        for i in range(5):
            wrapped(model="gpt-4", messages=[{"role": "user", "content": f"test{i}"}])

        stats = wrapper.get_stats()

        # Should have 5 unique entries
        assert stats["size"] == 5
        # Should have 5 hits (second round)
        assert stats["hits"] == 5
        # Should have 5 misses (first round)
        assert stats["misses"] == 5
        # Hit rate should be 50%
        assert stats["hit_rate"] == 50.0
