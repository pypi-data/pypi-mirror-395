# LLM Cache Examples

This directory contains examples demonstrating how to use llm-caching.

## Phase 1: Core Cache Examples

### test_cache_basic.py
Demonstrates the core caching functionality:
- Cache key generation
- Storing and retrieving responses
- LRU eviction behavior
- Statistics tracking

```bash
uv run python examples/test_cache_basic.py
```

### simulate_llm_calls.py
Simulates a realistic development workflow:
- Multiple LLM calls with repeated prompts
- Shows time savings from caching
- Demonstrates cache hit/miss patterns

```bash
uv run python examples/simulate_llm_calls.py
```

### config_example.py
Shows configuration management:
- Default vs custom configuration
- Environment variable usage
- Storage backend selection
- Statistics monitoring

```bash
uv run python examples/config_example.py
```

## Phase 2: HTTP Proxy Examples

### proxy_example_simulated.py
Guide and tutorial for using the HTTP proxy:
- How to start the proxy server
- How to configure LLM SDKs to use the proxy
- Monitoring and management
- Configuration options

```bash
uv run python examples/proxy_example_simulated.py
```

## Starting the Proxy Server

To start the HTTP proxy server:

```bash
# Start with default settings (SQLite, port 8000)
uv run llm-caching-proxy

# Or start manually
uv run python -m llm_cache.proxy.server
```

The proxy will be available at `http://localhost:8000`

## Quick Start with OpenAI

```python
import openai

# Point OpenAI to the cache proxy
openai.api_base = "http://localhost:8000/v1"
openai.api_key = "your-real-openai-key"

# Make calls as normal - they'll be cached!
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Second identical call is instant (cache hit)
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Configuration

Create a `.env` file:

```bash
# Backend type
LLM_CACHE_BACKEND=sqlite  # or 'redis'

# Cache size
LLM_CACHE_MAX_SIZE=1000

# SQLite settings
LLM_CACHE_SQLITE_PATH=./llm_cache.db

# Proxy settings
LLM_CACHE_PROXY_PORT=8000
LLM_CACHE_PROXY_HOST=0.0.0.0
```

## Monitoring

### View cache statistics
```bash
curl http://localhost:8000/cache/stats
```

### Check health
```bash
curl http://localhost:8000/health
```

### Clear cache
```bash
curl -X DELETE http://localhost:8000/cache/clear
```

## Next Steps

- Check out the [main README](../README.md) for full documentation
- Run the unit tests: `uv run pytest tests/`
- Explore the source code in `llm_cache/`
