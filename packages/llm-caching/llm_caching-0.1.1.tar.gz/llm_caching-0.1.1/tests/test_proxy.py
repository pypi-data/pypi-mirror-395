"""
Integration tests for HTTP proxy server.
"""

import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from llm_cache.cache.sqlite_storage import SQLiteStorage
from llm_cache.proxy.server import app, storage


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


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


@pytest.fixture(autouse=True)
def clear_cache():
    """Clear cache before each test."""
    storage.clear()
    yield
    storage.clear()


class TestRootEndpoints:
    """Test root and utility endpoints."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "LLM Cache Proxy"
        assert "endpoints" in data

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "cache_size" in data
        assert "backend" in data


class TestCacheManagement:
    """Test cache management endpoints."""

    def test_get_stats_empty_cache(self, client):
        """Test stats endpoint with empty cache."""
        response = client.get("/cache/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["stats"]["size"] == 0

    def test_clear_cache(self, client):
        """Test clearing the cache."""
        # Add some test data first
        from llm_cache.cache.key_generator import generate_cache_key

        key = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}],
        )
        storage.set(key, {"test": "data"})

        assert storage.get_size() > 0

        # Clear cache
        response = client.delete("/cache/clear")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert storage.get_size() == 0

    def test_delete_specific_entry(self, client):
        """Test deleting a specific cache entry."""
        from llm_cache.cache.key_generator import generate_cache_key

        key = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}],
        )
        storage.set(key, {"test": "data"})

        # Delete the entry
        response = client.post(f"/cache/delete/{key}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert storage.get(key) is None

    def test_delete_nonexistent_entry(self, client):
        """Test deleting a nonexistent entry returns 404."""
        fake_key = "a" * 64
        response = client.post(f"/cache/delete/{fake_key}")
        assert response.status_code == 404


class TestChatCompletionsEndpoint:
    """Test OpenAI chat completions endpoint."""

    def test_chat_completions_cache_miss(self, client):
        """Test cache miss - should forward to API."""
        from unittest.mock import MagicMock

        import httpx

        mock_response_data = {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "model": "gpt-4",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "Hello! How can I help you?",
                    },
                    "finish_reason": "stop",
                }
            ],
        }

        request_body = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "Hello"}],
            "temperature": 0.7,
        }

        # Mock the httpx client with proper async context manager support
        async def mock_post(*args, **kwargs):
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json = lambda: mock_response_data
            mock_resp.headers = {}
            return mock_resp

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client_instance = MagicMock()
            mock_client_instance.post = mock_post
            mock_client_instance.__aenter__ = AsyncMock(
                return_value=mock_client_instance
            )
            mock_client_instance.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client_instance

            response = client.post(
                "/v1/chat/completions",
                json=request_body,
                headers={"Authorization": "Bearer test-key"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "chatcmpl-123"
            assert response.headers["X-Cache-Hit"] == "false"

    def test_chat_completions_cache_hit(self, client):
        """Test cache hit - should return from cache."""
        from llm_cache.cache.key_generator import generate_cache_key

        # Pre-populate cache
        request_body = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "Hello"}],
            "temperature": 0.7,
        }

        key = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
            temperature=0.7,
        )

        cached_response = {
            "id": "cached-123",
            "choices": [{"message": {"content": "Cached response"}}],
        }
        storage.set(key, cached_response)

        # Make request
        response = client.post(
            "/v1/chat/completions",
            json=request_body,
            headers={"Authorization": "Bearer test-key"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "cached-123"
        assert response.headers["X-Cache-Hit"] == "true"

    def test_chat_completions_bypass_cache(self, client):
        """Test bypassing cache with X-Cache-Bypass header."""
        from unittest.mock import MagicMock

        from llm_cache.cache.key_generator import generate_cache_key

        # Pre-populate cache
        key = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
            temperature=0.7,
        )
        storage.set(key, {"id": "cached-123"})

        mock_response_data = {
            "id": "fresh-123",
            "choices": [{"message": {"content": "Fresh response"}}],
        }

        request_body = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "Hello"}],
            "temperature": 0.7,
        }

        async def mock_post(*args, **kwargs):
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json = lambda: mock_response_data
            mock_resp.headers = {}
            return mock_resp

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client_instance = MagicMock()
            mock_client_instance.post = mock_post
            mock_client_instance.__aenter__ = AsyncMock(
                return_value=mock_client_instance
            )
            mock_client_instance.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client_instance

            response = client.post(
                "/v1/chat/completions",
                json=request_body,
                headers={"Authorization": "Bearer test-key", "X-Cache-Bypass": "true"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "fresh-123"  # Got fresh response, not cached

    def test_chat_completions_invalid_json(self, client):
        """Test invalid JSON returns 400."""
        response = client.post(
            "/v1/chat/completions",
            content="invalid json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 400

    def test_chat_completions_custom_provider(self, client):
        """Test custom provider via X-LLM-Provider header."""
        from unittest.mock import MagicMock

        request_body = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "Hello"}],
        }

        mock_response_data = {"id": "test-123", "choices": []}

        async def mock_post(*args, **kwargs):
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json = lambda: mock_response_data
            mock_resp.headers = {}
            return mock_resp

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client_instance = MagicMock()
            mock_client_instance.post = mock_post
            mock_client_instance.__aenter__ = AsyncMock(
                return_value=mock_client_instance
            )
            mock_client_instance.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client_instance

            response = client.post(
                "/v1/chat/completions",
                json=request_body,
                headers={
                    "Authorization": "Bearer test-key",
                    "X-LLM-Provider": "openai",
                },
            )

            assert response.status_code == 200
            assert response.headers["X-Cache-Hit"] == "false"


class TestAnthropicEndpoint:
    """Test Anthropic messages endpoint."""

    def test_messages_cache_miss(self, client):
        """Test Anthropic endpoint cache miss."""
        from unittest.mock import MagicMock

        mock_response_data = {
            "id": "msg_123",
            "type": "message",
            "role": "assistant",
            "content": [{"type": "text", "text": "Hello from Claude!"}],
        }

        request_body = {
            "model": "claude-sonnet-4.5",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 1024,
        }

        async def mock_post(*args, **kwargs):
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json = lambda: mock_response_data
            mock_resp.headers = {}
            return mock_resp

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client_instance = MagicMock()
            mock_client_instance.post = mock_post
            mock_client_instance.__aenter__ = AsyncMock(
                return_value=mock_client_instance
            )
            mock_client_instance.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client_instance

            response = client.post(
                "/v1/messages",
                json=request_body,
                headers={"x-api-key": "test-key", "anthropic-version": "2023-06-01"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "msg_123"
            assert response.headers["X-Cache-Hit"] == "false"

    def test_messages_cache_hit(self, client):
        """Test Anthropic endpoint cache hit."""
        from llm_cache.cache.key_generator import generate_cache_key

        # Pre-populate cache
        request_body = {
            "model": "claude-sonnet-4.5",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 1024,
        }

        key = generate_cache_key(
            provider="anthropic",
            model="claude-sonnet-4.5",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=1024,
        )

        cached_response = {
            "id": "cached-msg-123",
            "content": [{"text": "Cached Claude response"}],
        }
        storage.set(key, cached_response)

        response = client.post(
            "/v1/messages", json=request_body, headers={"x-api-key": "test-key"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "cached-msg-123"
        assert response.headers["X-Cache-Hit"] == "true"


class TestCacheStatistics:
    """Test cache statistics tracking through proxy."""

    def test_stats_update_after_requests(self, client):
        """Test that stats are updated after requests."""
        from llm_cache.cache.key_generator import generate_cache_key

        # Pre-populate cache
        key = generate_cache_key(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}],
        )
        storage.set(key, {"response": "cached"})

        # Make a cache hit request
        request_body = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "test"}],
        }
        client.post("/v1/chat/completions", json=request_body)

        # Check stats
        response = client.get("/cache/stats")
        data = response.json()
        stats = data["stats"]

        assert stats["hits"] >= 1
        assert stats["size"] >= 1
