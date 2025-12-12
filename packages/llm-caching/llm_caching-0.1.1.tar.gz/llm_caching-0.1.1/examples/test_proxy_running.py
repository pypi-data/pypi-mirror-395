"""
Quick test to verify the proxy server is working.

This script tests the proxy by:
1. Making a health check request
2. Getting cache statistics
3. Testing the root endpoint
"""

import sys

import httpx

PROXY_URL = "http://localhost:8000"

print("=" * 70)
print("Testing LLM Cache Proxy")
print("=" * 70)


def test_proxy():
    """Test proxy endpoints."""
    try:
        client = httpx.Client(timeout=5.0)

        # Test 1: Health check
        print("\n1. Testing health check endpoint...")
        response = client.get(f"{PROXY_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("   ✓ Health check passed")
            print(f"     Status: {data['status']}")
            print(f"     Backend: {data['backend']}")
            print(f"     Cache: {data['cache_size']}/{data['cache_max_size']}")
        else:
            print(f"   ✗ Health check failed with status {response.status_code}")
            return False

        # Test 2: Root endpoint
        print("\n2. Testing root endpoint...")
        response = client.get(f"{PROXY_URL}/")
        if response.status_code == 200:
            data = response.json()
            print("   ✓ Root endpoint working")
            print(f"     Name: {data['name']}")
            print(f"     Status: {data['status']}")
        else:
            print("   ✗ Root endpoint failed")
            return False

        # Test 3: Cache stats
        print("\n3. Testing cache stats endpoint...")
        response = client.get(f"{PROXY_URL}/cache/stats")
        if response.status_code == 200:
            data = response.json()
            stats = data["stats"]
            print("   ✓ Cache stats retrieved")
            print(f"     Size: {stats['size']}/{stats['max_size']}")
            print(f"     Hits: {stats['hits']}")
            print(f"     Misses: {stats['misses']}")
            print(f"     Hit rate: {stats['hit_rate']}%")
        else:
            print("   ✗ Stats endpoint failed")
            return False

        # Test 4: API documentation
        print("\n4. Testing API documentation...")
        response = client.get(f"{PROXY_URL}/docs")
        if response.status_code == 200:
            print("   ✓ API docs available at {PROXY_URL}/docs")
        else:
            print("   ✗ API docs not available")

        print("\n" + "=" * 70)
        print("All tests passed! ✓")
        print("=" * 70)
        print("\nThe proxy is ready to use. Try:")
        print(f"  - API docs: {PROXY_URL}/docs")
        print(f"  - Health: {PROXY_URL}/health")
        print(f"  - Stats: {PROXY_URL}/cache/stats")
        print("\nTo use with OpenAI SDK:")
        print("  openai.api_base = 'http://localhost:8000/v1'")

        return True

    except httpx.ConnectError:
        print("\n✗ Could not connect to proxy server")
        print("\nThe proxy is not running. Start it with:")
        print("  $ uv run llm-caching-proxy")
        print("\nOr:")
        print("  $ uv run python -m llm_cache.proxy.server")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False
    finally:
        client.close()


if __name__ == "__main__":
    success = test_proxy()
    sys.exit(0 if success else 1)
