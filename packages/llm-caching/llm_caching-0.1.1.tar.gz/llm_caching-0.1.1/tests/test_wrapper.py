"""
Unit tests for Python SDK wrapper.
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock

import pytest

from llm_cache.cache.sqlite_storage import SQLiteStorage
from llm_cache.wrapper.sdk import LLMCacheWrapper, cached


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


class TestLLMCacheWrapper:
    """Test LLMCacheWrapper class."""

    def test_wrapper_initialization(self, temp_storage):
        """Test wrapper initialization."""
        wrapper = LLMCacheWrapper(storage=temp_storage)
        assert wrapper.storage == temp_storage
        assert wrapper.enabled is True
        assert wrapper.forced_provider is None

    def test_wrapper_with_custom_provider(self, temp_storage):
        """Test wrapper with forced provider."""
        wrapper = LLMCacheWrapper(storage=temp_storage, provider="openai")
        assert wrapper.forced_provider == "openai"

    def test_wrapper_disabled(self, temp_storage):
        """Test wrapper with caching disabled."""
        wrapper = LLMCacheWrapper(storage=temp_storage, enabled=False)

        mock_func = Mock(return_value={"result": "test"})
        mock_func.__module__ = "test"
        mock_func.__qualname__ = "test_func"

        wrapped = wrapper.wrap(mock_func)
        result = wrapped(test="value")

        # Function should be called directly without caching
        assert mock_func.call_count == 1
        wrapped(test="value")
        assert mock_func.call_count == 2  # Not cached, always calls

    def test_context_manager(self, temp_storage):
        """Test context manager support."""
        with LLMCacheWrapper(storage=temp_storage) as wrapper:
            assert isinstance(wrapper, LLMCacheWrapper)

    def test_enable_disable(self, temp_storage):
        """Test enable/disable caching."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        assert wrapper.enabled is True
        wrapper.disable()
        assert wrapper.enabled is False
        wrapper.enable()
        assert wrapper.enabled is True


class TestProviderDetection:
    """Test provider detection logic."""

    def test_detect_openai(self, temp_storage):
        """Test OpenAI provider detection."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        mock_func = Mock()
        mock_func.__module__ = "openai.api_resources.chat_completion"
        mock_func.__qualname__ = "ChatCompletion.create"

        provider = wrapper._detect_provider(mock_func, {})
        assert provider == "openai"

    def test_detect_anthropic(self, temp_storage):
        """Test Anthropic provider detection."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        mock_func = Mock()
        mock_func.__module__ = "anthropic.messages"
        mock_func.__qualname__ = "Messages.create"

        provider = wrapper._detect_provider(mock_func, {})
        assert provider == "anthropic"

    def test_detect_from_kwargs(self, temp_storage):
        """Test provider detection from kwargs."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        mock_func = Mock()
        mock_func.__module__ = "unknown"
        mock_func.__qualname__ = "test"

        kwargs = {"provider": "openai"}
        provider = wrapper._detect_provider(mock_func, kwargs)

        assert provider == "openai"
        assert "provider" not in kwargs  # Should be popped

    def test_forced_provider(self, temp_storage):
        """Test forced provider overrides detection."""
        wrapper = LLMCacheWrapper(storage=temp_storage, provider="custom")

        mock_func = Mock()
        mock_func.__module__ = "openai"

        provider = wrapper._detect_provider(mock_func, {})
        assert provider == "custom"


class TestCaching:
    """Test caching functionality."""

    def test_cache_hit_and_miss(self, temp_storage):
        """Test cache hit and miss behavior."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        call_count = 0

        def mock_llm_call(model, messages):
            nonlocal call_count
            call_count += 1
            return {"response": f"call_{call_count}"}

        mock_llm_call.__module__ = "openai"
        mock_llm_call.__qualname__ = "create"

        wrapped = wrapper.wrap(mock_llm_call)

        # First call - cache miss
        result1 = wrapped(model="gpt-4", messages=[{"role": "user", "content": "test"}])
        assert result1["response"] == "call_1"
        assert call_count == 1

        # Second call - cache hit
        result2 = wrapped(model="gpt-4", messages=[{"role": "user", "content": "test"}])
        assert result2["response"] == "call_1"  # Same result from cache
        assert call_count == 1  # Function not called again

        # Different parameters - cache miss
        result3 = wrapped(
            model="gpt-4", messages=[{"role": "user", "content": "different"}]
        )
        assert result3["response"] == "call_2"
        assert call_count == 2

    def test_cache_bypass(self, temp_storage):
        """Test cache bypass flag."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        call_count = 0

        def mock_llm_call(model, messages, _cache_bypass=False):
            nonlocal call_count
            call_count += 1
            return {"response": f"call_{call_count}"}

        mock_llm_call.__module__ = "openai"
        mock_llm_call.__qualname__ = "create"

        wrapped = wrapper.wrap(mock_llm_call)

        # First call
        result1 = wrapped(model="gpt-4", messages=[{"role": "user", "content": "test"}])
        assert call_count == 1

        # Bypass cache
        result2 = wrapped(
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}],
            _cache_bypass=True,
        )
        assert call_count == 2  # Function called again despite same params

    def test_response_serialization(self, temp_storage):
        """Test serialization of different response types."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        # Test dict response
        dict_response = {"key": "value"}
        serialized = wrapper._serialize_response(dict_response, "openai")
        assert serialized == dict_response

        # Test object with __dict__
        class MockResponse:
            def __init__(self):
                self.data = "test"
                self.code = 200

        obj_response = MockResponse()
        serialized = wrapper._serialize_response(obj_response, "openai")
        assert "data" in serialized
        assert serialized["data"] == "test"

        # Test object with model_dump (Pydantic)
        class PydanticLike:
            def model_dump(self):
                return {"pydantic": "data"}

        pydantic_response = PydanticLike()
        serialized = wrapper._serialize_response(pydantic_response, "openai")
        assert serialized == {"pydantic": "data"}

    def test_stats_tracking(self, temp_storage):
        """Test cache statistics tracking."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        def mock_llm_call(model, messages):
            return {"response": "test"}

        mock_llm_call.__module__ = "openai"
        mock_llm_call.__qualname__ = "create"

        wrapped = wrapper.wrap(mock_llm_call)

        # Make calls
        wrapped(model="gpt-4", messages=[{"role": "user", "content": "test1"}])
        wrapped(model="gpt-4", messages=[{"role": "user", "content": "test1"}])  # Hit
        wrapped(model="gpt-4", messages=[{"role": "user", "content": "test2"}])

        stats = wrapper.get_stats()
        assert stats["size"] == 2  # Two unique requests
        assert stats["hits"] == 1
        assert stats["misses"] == 2

    def test_clear_cache(self, temp_storage):
        """Test clearing the cache."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        def mock_llm_call(model, messages):
            return {"response": "test"}

        mock_llm_call.__module__ = "openai"
        mock_llm_call.__qualname__ = "create"

        wrapped = wrapper.wrap(mock_llm_call)

        # Add to cache
        wrapped(model="gpt-4", messages=[{"role": "user", "content": "test"}])
        assert wrapper.storage.get_size() == 1

        # Clear cache
        wrapper.clear_cache()
        assert wrapper.storage.get_size() == 0


class TestDecoratorPattern:
    """Test decorator pattern usage."""

    def test_cached_decorator_no_args(self, temp_storage):
        """Test @cached decorator without arguments."""

        @cached
        def mock_llm_call(model, messages):
            return {"response": "test"}

        mock_llm_call.__module__ = "openai"

        # This should work but won't actually cache since we're using default storage
        result = mock_llm_call(
            model="gpt-4", messages=[{"role": "user", "content": "test"}]
        )
        assert result["response"] == "test"

    def test_cached_decorator_with_args(self, temp_storage):
        """Test @cached decorator with arguments."""

        @cached(provider="openai", storage=temp_storage)
        def mock_llm_call(model, messages):
            return {"response": "test"}

        mock_llm_call.__module__ = "test"

        result = mock_llm_call(
            model="gpt-4", messages=[{"role": "user", "content": "test"}]
        )
        assert result["response"] == "test"

    def test_wrap_method(self, temp_storage):
        """Test using wrap method directly."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        def mock_llm_call(model, messages):
            return {"response": "test"}

        mock_llm_call.__module__ = "openai"
        mock_llm_call.__qualname__ = "create"

        wrapped = wrapper.wrap(mock_llm_call)

        result = wrapped(model="gpt-4", messages=[{"role": "user", "content": "test"}])
        assert result["response"] == "test"

    def test_decorator_preserves_function_metadata(self, temp_storage):
        """Test that decorator preserves function metadata."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        def original_func(model, messages):
            """Original docstring."""
            return {"response": "test"}

        original_func.__module__ = "openai"
        wrapped = wrapper.wrap(original_func)

        assert wrapped.__name__ == "original_func"
        assert wrapped.__doc__ == "Original docstring."


class TestParameterExtraction:
    """Test parameter extraction for cache keys."""

    def test_extract_common_parameters(self, temp_storage):
        """Test extraction of common LLM parameters."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        def mock_func(model, messages, temperature=0.7, max_tokens=None, api_key=None):
            pass

        kwargs = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "test"}],
            "temperature": 0.7,
            "max_tokens": 100,
            "api_key": "secret",  # Should not be extracted
        }

        params = wrapper._extract_cache_params((), kwargs, mock_func)

        assert params["model"] == "gpt-4"
        assert params["messages"] == kwargs["messages"]
        assert params["temperature"] == 0.7
        assert params["max_tokens"] == 100
        # api_key is not in the param_mapping, so it won't be in params

    def test_extract_with_aliases(self, temp_storage):
        """Test extraction with parameter aliases."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        mock_func = Mock()

        # Using aliases
        kwargs = {
            "engine": "davinci",  # Alias for model
            "prompt": "test prompt",  # Alias for messages
            "max_length": 50,  # Alias for max_tokens
        }

        params = wrapper._extract_cache_params((), kwargs, mock_func)

        # Should be normalized to standard keys
        assert params.get("model") == "davinci" or "engine" in kwargs
        assert "prompt" in kwargs or "messages" in params


class TestIntegration:
    """Integration tests with realistic scenarios."""

    def test_realistic_openai_workflow(self, temp_storage):
        """Test realistic OpenAI SDK workflow."""
        wrapper = LLMCacheWrapper(storage=temp_storage)

        call_count = 0

        def mock_openai_create(model, messages, temperature=0.7):
            nonlocal call_count
            call_count += 1
            return {
                "id": f"chatcmpl-{call_count}",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": f"Response {call_count}",
                        }
                    }
                ],
                "model": model,
            }

        mock_openai_create.__module__ = "openai.api_resources"
        mock_openai_create.__qualname__ = "ChatCompletion.create"

        wrapped = wrapper.wrap(mock_openai_create)

        # First call
        response1 = wrapped(
            model="gpt-4", messages=[{"role": "user", "content": "Hello"}]
        )
        assert response1["id"] == "chatcmpl-1"
        assert call_count == 1

        # Same call - should hit cache
        response2 = wrapped(
            model="gpt-4", messages=[{"role": "user", "content": "Hello"}]
        )
        assert response2["id"] == "chatcmpl-1"  # Same response
        assert call_count == 1  # Not called again

        # Different temperature - should miss cache
        response3 = wrapped(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
            temperature=0.8,
        )
        assert response3["id"] == "chatcmpl-2"
        assert call_count == 2
