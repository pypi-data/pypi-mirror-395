"""
Example demonstrating configuration and storage backend usage.
"""

import os

from llm_cache.cache.sqlite_storage import SQLiteStorage
from llm_cache.config import Config

print("=" * 70)
print("LLM Cache - Configuration Example")
print("=" * 70)

# Example 1: Using default configuration
print("\n1. Default Configuration")
print("-" * 70)

config = Config()
print(f"Backend: {config.backend}")
print(f"Max size: {config.max_size}")
print(f"SQLite path: {config.sqlite_path}")
print(f"Proxy: {config.proxy_host}:{config.proxy_port}")

# Example 2: Get storage from config
print("\n2. Creating Storage from Config")
print("-" * 70)

storage = config.get_storage()
print(f"Storage type: {type(storage).__name__}")
print(f"Max size: {storage.max_size}")

# Test the storage
storage.set("test_key", {"data": "test_value"})
result = storage.get("test_key")
print(f"Stored and retrieved: {result}")

# Example 3: Configuration to dict
print("\n3. Configuration as Dictionary")
print("-" * 70)

config_dict = config.to_dict()
import json

print(json.dumps(config_dict, indent=2))

# Example 4: Demonstrate environment variable override
print("\n4. Environment Variable Override")
print("-" * 70)

print("\nTo customize configuration, set environment variables:")
print("  export LLM_CACHE_BACKEND=redis")
print("  export LLM_CACHE_MAX_SIZE=5000")
print("  export LLM_CACHE_SQLITE_PATH=/path/to/cache.db")
print("  export LLM_CACHE_PROXY_PORT=9000")

print("\nOr create a .env file:")
print("  cp .env.example .env")
print("  # Edit .env with your settings")

# Example 5: Direct storage usage
print("\n5. Direct Storage Usage (without Config)")
print("-" * 70)

# You can also create storage directly
custom_storage = SQLiteStorage(db_path="custom_cache.db", max_size=500)

print(f"Created custom storage:")
print(f"  Path: custom_cache.db")
print(f"  Max size: {custom_storage.max_size}")

# Example 6: Cache statistics
print("\n6. Cache Statistics")
print("-" * 70)

# Add some test data
for i in range(5):
    custom_storage.set(f"key_{i}", {"index": i, "data": f"value_{i}"})

# Some cache hits
custom_storage.get("key_0")
custom_storage.get("key_1")
custom_storage.get("key_0")  # Hit again

# Some cache misses
custom_storage.get("nonexistent_1")
custom_storage.get("nonexistent_2")

stats = custom_storage.get_stats()
print(f"Size: {stats['size']}/{stats['max_size']}")
print(f"Hits: {stats['hits']}")
print(f"Misses: {stats['misses']}")
print(f"Hit rate: {stats['hit_rate']}%")

print("\n" + "=" * 70)
print("Configuration Tips")
print("=" * 70)
print(
    """
Development (Local):
  - Use SQLite (default)
  - Small max_size (100-1000 entries)
  - Local file path

Production:
  - Use Redis for scalability
  - Larger max_size (5000-10000 entries)
  - Shared Redis instance for team caching

Example .env for production:
  LLM_CACHE_BACKEND=redis
  LLM_CACHE_REDIS_HOST=redis.example.com
  LLM_CACHE_REDIS_PASSWORD=your_password
  LLM_CACHE_MAX_SIZE=10000
  LLM_CACHE_PROXY_PORT=8000
"""
)

# Clean up
storage.clear()
custom_storage.clear()

import os

if os.path.exists("llm_cache.db"):
    os.remove("llm_cache.db")
if os.path.exists("custom_cache.db"):
    os.remove("custom_cache.db")

print("\nDemo databases cleaned up")
