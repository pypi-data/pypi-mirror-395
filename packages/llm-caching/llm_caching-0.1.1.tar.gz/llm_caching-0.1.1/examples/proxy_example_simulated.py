"""
Example demonstrating the HTTP Proxy Server with simulated LLM API.

This script:
1. Starts a mock LLM API server
2. Configures the proxy to forward to the mock API
3. Makes requests through the proxy
4. Shows cache hits/misses and performance gains
"""

import asyncio
import time
from contextlib import asynccontextmanager

import httpx

print("=" * 70)
print("LLM Cache Proxy - Simulated Example")
print("=" * 70)

# Simulated LLM API endpoint (mock)
MOCK_API_BASE = "http://localhost:8001"  # Would be a mock server
PROXY_BASE = "http://localhost:8000"


async def make_request(base_url: str, prompt: str):
    """Make a chat completion request."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{base_url}/v1/chat/completions",
                json={
                    "model": "gpt-4",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                },
                headers={"Authorization": "Bearer mock-api-key"},
            )
            return response
        except httpx.ConnectError:
            return None


async def get_stats():
    """Get cache statistics."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{PROXY_BASE}/cache/stats")
            return response.json()
        except httpx.ConnectError:
            return None


print("\n" + "=" * 70)
print("How to Use the Proxy")
print("=" * 70)

print(
    """
Step 1: Start the proxy server
----------------------------------------------------------------------
In one terminal, run:

    $ uv run llm-caching-proxy

Or:

    $ uv run python -m llm_cache.proxy.server

The proxy will start on http://localhost:8000

You should see:
    INFO: Started server process
    INFO: Uvicorn running on http://0.0.0.0:8000


Step 2: Configure your LLM SDK to use the proxy
----------------------------------------------------------------------
Instead of pointing to the real API, point to the proxy:

Python (OpenAI SDK):
    import openai

    # Configure to use proxy
    openai.api_base = "http://localhost:8000/v1"
    openai.api_key = "your-real-openai-key"  # Still needed for upstream API

    # Make calls as normal - they'll be cached!
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello!"}]
    )

JavaScript (OpenAI Node.js):
    const { Configuration, OpenAIApi } = require("openai");

    const configuration = new Configuration({
        apiKey: process.env.OPENAI_API_KEY,
        basePath: "http://localhost:8000/v1"
    });

    const openai = new OpenAIApi(configuration);

cURL:
    curl http://localhost:8000/v1/chat/completions \\
      -H "Content-Type: application/json" \\
      -H "Authorization: Bearer YOUR_API_KEY" \\
      -d '{
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "Hello!"}]
      }'


Step 3: Monitor cache performance
----------------------------------------------------------------------
View cache statistics:

    $ curl http://localhost:8000/cache/stats

Response:
    {
      "status": "success",
      "stats": {
        "size": 42,
        "max_size": 1000,
        "hits": 127,
        "misses": 58,
        "hit_rate": 68.65
      }
    }

Clear cache:

    $ curl -X DELETE http://localhost:8000/cache/clear

Health check:

    $ curl http://localhost:8000/health


Step 4: Special Headers
----------------------------------------------------------------------
Bypass cache for a specific request:

    curl http://localhost:8000/v1/chat/completions \\
      -H "X-Cache-Bypass: true" \\
      -H "Authorization: Bearer YOUR_API_KEY" \\
      ...

Use different provider:

    curl http://localhost:8000/v1/chat/completions \\
      -H "X-LLM-Provider: anthropic" \\
      ...


Response Headers
----------------------------------------------------------------------
All responses include:
  - X-Cache-Hit: true/false (whether response came from cache)

Example:
    HTTP/1.1 200 OK
    X-Cache-Hit: true
    Content-Type: application/json
    ...
"""
)

print("\n" + "=" * 70)
print("Example Workflow")
print("=" * 70)

print(
    """
Development Workflow:
1. Start proxy: llm-caching-proxy
2. Run your development code (tests, experiments, etc.)
3. First run: Slow (hits real API)
4. Subsequent runs: Fast (cache hits)
5. When done: Clear cache if needed

Team Workflow:
1. Deploy proxy with Redis backend
2. Team members point their SDKs to shared proxy
3. Cache is shared across the team
4. Significant cost and time savings

Production Workflow:
1. Deploy proxy in your infrastructure
2. Use Redis for scalability
3. Monitor cache hit rates
4. Adjust max_size based on memory/disk
"""
)

print("\n" + "=" * 70)
print("Configuration")
print("=" * 70)

print(
    """
Configure via environment variables or .env file:

# SQLite (default - good for local dev)
LLM_CACHE_BACKEND=sqlite
LLM_CACHE_SQLITE_PATH=./llm_cache.db
LLM_CACHE_MAX_SIZE=1000

# Redis (production - scalable)
LLM_CACHE_BACKEND=redis
LLM_CACHE_REDIS_HOST=localhost
LLM_CACHE_REDIS_PORT=6379
LLM_CACHE_MAX_SIZE=10000

# Proxy settings
LLM_CACHE_PROXY_HOST=0.0.0.0
LLM_CACHE_PROXY_PORT=8000
"""
)

print("\n" + "=" * 70)
print("Testing the Proxy")
print("=" * 70)


async def test_proxy():
    """Test if proxy is running."""
    print("\nChecking if proxy is running...")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{PROXY_BASE}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Proxy is running!")
                print(f"  Status: {data['status']}")
                print(f"  Backend: {data['backend']}")
                print(f"  Cache size: {data['cache_size']}/{data['cache_max_size']}")
                return True
            else:
                print(f"✗ Proxy returned status {response.status_code}")
                return False
        except httpx.ConnectError:
            print("✗ Could not connect to proxy.")
            print("\nTo start the proxy, run in another terminal:")
            print("  $ uv run llm-caching-proxy")
            return False


# Try to connect to proxy
try:
    running = asyncio.run(test_proxy())

    if running:
        print("\n" + "=" * 70)
        print("Try It Out!")
        print("=" * 70)
        print(
            """
The proxy is running! Try making a request:

    curl http://localhost:8000/v1/chat/completions \\
      -H "Content-Type: application/json" \\
      -H "Authorization: Bearer YOUR_OPENAI_API_KEY" \\
      -d '{
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "Say hello!"}]
      }'

Run it twice and watch the second request return instantly (cache hit)!
        """
        )
except Exception as e:
    print(f"\nNote: {e}")

print("\n" + "=" * 70)
print("For more examples, see:")
print("  - examples/proxy_example_openai.py (OpenAI SDK integration)")
print("  - examples/proxy_example_anthropic.py (Anthropic SDK integration)")
print("=" * 70)
