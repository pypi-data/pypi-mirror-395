# LLM Cache

A high-performance caching system for LLM (Large Language Model) API calls that dramatically speeds up development iteration and reduces costs.

[![Tests](https://github.com/fred3105/llm-caching/workflows/CI/badge.svg)](https://github.com/fred3105/llm-caching/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why LLM Cache?

When developing applications that use LLM APIs (OpenAI, Anthropic, etc.), you often:

- **Wait unnecessarily** for the same API calls during development/testing
- **Hit rate limits** when iterating rapidly
- **Pay repeatedly** for identical API calls
- **Slow down** your development workflow

LLM Cache solves these problems by caching LLM responses locally, making repeated calls **instant** and **free**.

### Key Benefits

- **10-1000x faster** development iteration (instant cache hits vs. 1-10s API calls)
- **Significant cost savings** during development (no repeated charges for identical requests)
- **No rate limit issues** when testing and iterating
- **Works offline** after the first API call
- **Zero code changes** required (using HTTP proxy mode)
- **Production-ready** with Redis backend and Docker support

## Features

- **Dual Interface**: Choose between HTTP proxy server or Python SDK wrapper
- **Universal Provider Support**: Works with OpenAI, Anthropic, Cohere, HuggingFace, and more
- **Smart Caching**: Cache keys based on model, messages, temperature, and all sampling parameters
- **LRU Eviction**: Automatic cache size management with Least Recently Used eviction
- **Multiple Backends**: SQLite for local development, Redis for production
- **Streaming Support**: Full support for streaming LLM responses
- **Statistics Tracking**: Monitor cache hits, misses, and hit rates
- **Cache Management**: Clear cache, delete specific entries, bypass cache on demand
- **Production Ready**: Docker, docker-compose, CI/CD, comprehensive tests

## Quick Start

### Installation

Using [uv](https://github.com/astral-sh/uv) (recommended):

```bash
# Clone the repository
git clone https://github.com/fred3105/llm-caching.git
cd llm-caching

# Install dependencies with uv
uv sync

# Or install in editable mode
uv pip install -e .
```

Using pip:

```bash
pip install -e .
```

### Method 1: HTTP Proxy Server (Zero Code Changes)

Start the proxy server:

```bash
# Using uv
uv run python -m llm_cache.proxy.server

# Or directly
python -m llm_cache.proxy.server
```

Then point your LLM SDK to use the proxy:

```python
import openai

# Just change the base URL - that's it!
openai.api_base = "http://localhost:8000/v1"
openai.api_key = "your-real-api-key"  # Still needed for forwarding

# All calls are now automatically cached
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What is caching?"}]
)

# Second call with same params = instant cache hit!
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What is caching?"}]
)
```

**Works with Anthropic too:**

```python
import anthropic

# Point to the proxy
client = anthropic.Anthropic(
    api_key="your-real-api-key",
    base_url="http://localhost:8000"
)

# Automatically cached
response = client.messages.create(
    model="claude-sonnet-4.5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Method 2: Python SDK Wrapper (Direct Integration)

Use the Python wrapper for more control:

```python
from llm_cache import cached
import openai

# Option 1: Decorator pattern (simplest)
@cached
def ask_gpt(question):
    return openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": question}]
    )

# First call hits API
response = ask_gpt("What is machine learning?")

# Second call is instant - from cache!
response = ask_gpt("What is machine learning?")

# Option 2: Explicit wrapper
from llm_cache import LLMCacheWrapper

cache = LLMCacheWrapper()

@cache.wrap
def ask_claude(question):
    client = anthropic.Anthropic()
    return client.messages.create(
        model="claude-sonnet-4.5",
        max_tokens=1024,
        messages=[{"role": "user", "content": question}]
    )

# Usage is the same
answer = ask_claude("Explain caching")  # API call
answer = ask_claude("Explain caching")  # Cached!

# Option 3: Manual wrapping
cache = LLMCacheWrapper()
cached_create = cache.wrap(openai.ChatCompletion.create)

response = cached_create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Configuration

LLM Cache uses environment variables for configuration. Create a `.env` file in your project:

```bash
# Backend (sqlite or redis)
LLM_CACHE_BACKEND=sqlite

# SQLite Configuration (for local development)
LLM_CACHE_SQLITE_PATH=./llm_cache.db

# Redis Configuration (for production)
LLM_CACHE_REDIS_HOST=localhost
LLM_CACHE_REDIS_PORT=6379
LLM_CACHE_REDIS_DB=0
LLM_CACHE_REDIS_PASSWORD=

# Cache Settings
LLM_CACHE_MAX_SIZE=1000

# Proxy Server Settings
LLM_CACHE_PROXY_HOST=0.0.0.0
LLM_CACHE_PROXY_PORT=8000
```

### Configuration in Code

```python
from llm_cache.config import Config

config = Config()
print(config.to_dict())

# Get storage backend
storage = config.get_storage()  # Returns SQLiteStorage or RedisStorage
```

## Advanced Usage

### Cache Management

#### Using HTTP Proxy

```bash
# Check cache statistics
curl http://localhost:8000/cache/stats

# Clear entire cache
curl -X POST http://localhost:8000/cache/clear

# Delete specific entry
curl -X DELETE "http://localhost:8000/cache/entry?key=abc123..."

# Health check
curl http://localhost:8000/health
```

#### Using Python Wrapper

```python
from llm_cache import LLMCacheWrapper

cache = LLMCacheWrapper()

# Get statistics
stats = cache.get_stats()
print(f"Cache hits: {stats['hits']}")
print(f"Cache misses: {stats['misses']}")
print(f"Hit rate: {stats['hit_rate']}%")
print(f"Cache size: {stats['size']}/{stats['max_size']}")

# Clear cache
cache.clear_cache()

# Disable/enable caching
cache.disable()  # Bypass cache temporarily
result = wrapped_func()  # Goes to API
cache.enable()   # Re-enable caching
```

### Cache Bypass

Sometimes you want to force a fresh API call:

#### HTTP Proxy

```python
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}],
    extra_body={"_cache_bypass": True}  # Force fresh call
)
```

#### Python Wrapper

```python
response = cached_func(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}],
    _cache_bypass=True  # Force fresh call
)
```

### Custom Storage Backend

```python
from llm_cache import LLMCacheWrapper
from llm_cache.cache.sqlite_storage import SQLiteStorage

# Custom SQLite storage
storage = SQLiteStorage(db_path="./my_cache.db", max_size=5000)
cache = LLMCacheWrapper(storage=storage)

# Custom Redis storage
from llm_cache.cache.redis_storage import RedisStorage

storage = RedisStorage(
    host="redis.example.com",
    port=6379,
    db=0,
    password="secret",
    max_size=10000
)
cache = LLMCacheWrapper(storage=storage)
```

### Provider-Specific Configuration

```python
# Force a specific provider (useful for custom LLM APIs)
from llm_cache import LLMCacheWrapper

cache = LLMCacheWrapper(provider="custom-llm")

@cache.wrap
def my_custom_llm(prompt):
    # Your custom LLM API call
    return custom_api.generate(prompt)
```

### Streaming Support

The HTTP proxy automatically handles streaming responses:

```python
import openai

openai.api_base = "http://localhost:8000/v1"

# Streaming works automatically
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in response:
    print(chunk.choices[0].delta.get("content", ""), end="")
```

## Production Deployment

### Using Docker

Build and run:

```bash
# Build image
docker build -t llm-caching .

# Run with SQLite
docker run -p 8000:8000 \
  -v $(pwd)/cache:/app/cache \
  -e LLM_CACHE_BACKEND=sqlite \
  -e LLM_CACHE_SQLITE_PATH=/app/cache/llm_cache.db \
  llm-caching

# Run with Redis
docker run -p 8000:8000 \
  -e LLM_CACHE_BACKEND=redis \
  -e LLM_CACHE_REDIS_HOST=redis.example.com \
  -e LLM_CACHE_REDIS_PASSWORD=secret \
  llm-caching
```

### Using Docker Compose

The easiest way for production:

```bash
# Start both proxy and Redis
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Production Best Practices

See [PRODUCTION.md](PRODUCTION.md) for comprehensive production deployment guide including:

- Redis configuration and tuning
- Security considerations
- Scaling strategies
- Monitoring and observability
- Backup and recovery
- Performance optimization

## How It Works

### Cache Key Generation

LLM Cache generates deterministic cache keys from request parameters:

```python
# These parameters affect the cache key:
- provider (openai, anthropic, etc.)
- model (gpt-4, claude-sonnet-4.5, etc.)
- messages (the conversation/prompt)
- temperature
- max_tokens
- top_p, top_k
- frequency_penalty, presence_penalty
- stop sequences
- seed

# These do NOT affect the cache key:
- api_key (security)
- user_id (privacy)
- timestamps
- stream flag
```

Cache keys are SHA256 hashes of normalized, deterministically-serialized JSON, ensuring:
- Same inputs always generate the same key
- Different inputs always generate different keys
- Keys are cryptographically secure (no collisions)

### LRU Eviction

When the cache reaches max_size, the Least Recently Used (LRU) entry is evicted:

- **SQLite**: Uses indexed `last_accessed` timestamp for efficient LRU queries
- **Redis**: Uses sorted sets (ZSET) for O(log n) LRU operations

### Provider Auto-Detection

The Python wrapper automatically detects LLM providers:

```python
# Detected from function module and name
openai.ChatCompletion.create        → "openai"
anthropic.Messages.create           → "anthropic"
cohere.Client.generate              → "cohere"
transformers.pipeline()             → "huggingface"

# Or specify manually
@cached(provider="custom")
def my_llm(): ...
```

## API Reference

### HTTP Proxy Endpoints

#### Chat Completions (OpenAI-compatible)

```
POST /v1/chat/completions
```

Request body: Standard OpenAI chat completion request
Response: Standard OpenAI chat completion response
Headers: `X-Cache-Hit: true|false`

#### Messages (Anthropic-compatible)

```
POST /v1/messages
```

Request body: Standard Anthropic messages request
Response: Standard Anthropic messages response
Headers: `X-Cache-Hit: true|false`

#### Cache Statistics

```
GET /cache/stats
```

Response:
```json
{
  "size": 42,
  "max_size": 1000,
  "hits": 156,
  "misses": 42,
  "hit_rate": 78.79
}
```

#### Clear Cache

```
POST /cache/clear
```

Response:
```json
{
  "status": "success",
  "message": "Cache cleared"
}
```

#### Delete Entry

```
DELETE /cache/entry?key=<cache_key>
```

Response:
```json
{
  "status": "success",
  "message": "Entry deleted"
}
```

#### Health Check

```
GET /health
```

Response:
```json
{
  "status": "healthy",
  "backend": "sqlite",
  "cache_size": 42
}
```

### Python API

#### LLMCacheWrapper

```python
from llm_cache import LLMCacheWrapper

cache = LLMCacheWrapper(
    storage=None,      # Custom storage backend (default: from config)
    enabled=True,      # Enable/disable caching
    provider=None      # Force specific provider (default: auto-detect)
)

# Wrap a function
wrapped = cache.wrap(func)

# Context manager
with LLMCacheWrapper() as cache:
    wrapped = cache.wrap(func)
    result = wrapped()

# Cache management
cache.clear_cache()
cache.disable()
cache.enable()
stats = cache.get_stats()
```

#### Decorator

```python
from llm_cache import cached

# Simple usage
@cached
def my_llm_call(): ...

# With arguments
@cached(provider="openai", storage=custom_storage)
def my_llm_call(): ...
```

## Testing

LLM Cache has comprehensive test coverage (89 tests):

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=llm_cache --cov-report=html

# Run specific test file
uv run pytest tests/test_cache.py -v

# Run with different Python versions (requires tox)
tox
```

Test categories:
- **Cache layer tests** (26 tests): Key generation, storage, eviction, config
- **Proxy server tests** (14 tests): Endpoints, caching, streaming, error handling
- **Wrapper tests** (21 tests): Wrapping, decorators, providers, serialization
- **Edge case tests** (29 tests): Unicode, concurrency, large responses, error handling

## Examples

See the `examples/` directory for complete working examples:

- **[proxy_example_simulated.py](examples/proxy_example_simulated.py)**: HTTP proxy usage with simulated API
- **[wrapper_example.py](examples/wrapper_example.py)**: Python SDK wrapper usage with demos

Run examples:

```bash
# HTTP proxy example
uv run python examples/proxy_example_simulated.py

# Python wrapper example
uv run python examples/wrapper_example.py
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Client Application                   │
│         (OpenAI, Anthropic, or custom LLM SDK)          │
└────────────────┬────────────────────────────────────────┘
                 │
                 ├─────────────────┬───────────────────────┐
                 │                 │                       │
          ┌──────▼──────┐   ┌─────▼───────┐         ┌─────▼──────┐
          │ HTTP Proxy  │   │ SDK Wrapper │         │ Direct API │
          │   Server    │   │  (Decorator)│         │    Call    │
          └──────┬──────┘   └─────┬───────┘         └────────────┘
                 │                 │
                 └────────┬────────┘
                          │
                   ┌──────▼───────┐
                   │ Cache Layer  │
                   │ Key Generator│
                   └──────┬───────┘
                          │
                ┌─────────┴─────────┐
                │                   │
         ┌──────▼──────┐     ┌─────▼──────┐
         │   SQLite    │     │   Redis    │
         │  Storage    │     │  Storage   │
         │  (Dev/Test) │     │(Production)│
         └─────────────┘     └────────────┘
```

## Performance

Typical performance improvements:

| Scenario | Without Cache | With Cache (Hit) | Speedup |
|----------|--------------|------------------|---------|
| OpenAI GPT-4 | 2-5 seconds | 5-10 ms | **200-1000x** |
| Anthropic Claude | 1-3 seconds | 5-10 ms | **100-600x** |
| Local LLM (HF) | 100-500 ms | 5-10 ms | **10-100x** |

Cache overhead (miss): ~5-10ms additional latency for key generation and storage lookup.

## Limitations

- **Non-deterministic models**: If `temperature > 0` or random sampling is used, each API call is expected to be different. The cache respects this - different temperature values create different cache keys.
- **Streaming**: Streaming responses are fully cached, but the entire stream must complete before caching occurs.
- **Token limits**: Very large responses (>1MB) may impact SQLite performance. Use Redis for production with large responses.
- **Concurrent writes**: SQLite has limited concurrent write performance. Use Redis for high-concurrency scenarios.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`uv run pytest`)
6. Commit with clear messages (`git commit -m 'Add amazing feature'`)
7. Push to your fork (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Setup

```bash
# Clone repository
git clone https://github.com/fred3105/llm-caching.git
cd llm-caching

# Install development dependencies
uv sync --extra dev

# Install pre-commit hooks (optional)
pre-commit install

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=llm_cache

# Format code
uv run black llm_cache tests
uv run isort llm_cache tests
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the need to speed up LLM development workflows
- Built with [FastAPI](https://fastapi.tiangolo.com/), [Redis](https://redis.io/), and [SQLite](https://www.sqlite.org/)
- Developed with [uv](https://github.com/astral-sh/uv) for fast dependency management

## Support

- **Issues**: [GitHub Issues](https://github.com/fred3105/llm-caching/issues)
- **Discussions**: [GitHub Discussions](https://github.com/fred3105/llm-caching/discussions)

## Roadmap

- [ ] Semantic caching using embeddings (cache similar prompts)
- [ ] TTL (time-to-live) expiration for cache entries
- [ ] Multi-level cache hierarchy (memory + disk + Redis)
- [ ] Analytics dashboard for cache statistics
- [ ] Response compression for large cached responses
- [ ] Support for more LLM providers (Cohere, AI21, etc.)
- [ ] Automatic cache warming from production logs
- [ ] Cache export/import functionality

---

**Made with ❤️ to make LLM development faster and cheaper**
