"""
Basic example demonstrating the cache layer functionality.

This script shows:
1. Cache key generation
2. Storing and retrieving cached responses
3. LRU eviction behavior
4. Statistics tracking
"""

from llm_cache.cache.key_generator import generate_cache_key
from llm_cache.cache.sqlite_storage import SQLiteStorage
from llm_cache.config import Config

print("=" * 60)
print("LLM Cache - Basic Functionality Test")
print("=" * 60)

# Initialize storage with small max_size for demonstration
print("\n1. Initializing SQLite storage (max_size=3)...")
storage = SQLiteStorage(db_path="demo_cache.db", max_size=3)
print(f"   Storage initialized: {storage.get_size()} entries")

# Generate cache keys for different requests
print("\n2. Generating cache keys for different LLM requests...")

key1 = generate_cache_key(
    provider="openai",
    model="gpt-4",
    messages=[{"role": "user", "content": "What is Python?"}],
    temperature=0.7,
)
print(f"   Key 1: {key1[:16]}... (for 'What is Python?')")

key2 = generate_cache_key(
    provider="openai",
    model="gpt-4",
    messages=[{"role": "user", "content": "What is JavaScript?"}],
    temperature=0.7,
)
print(f"   Key 2: {key2[:16]}... (for 'What is JavaScript?')")

key3 = generate_cache_key(
    provider="openai",
    model="gpt-4",
    messages=[{"role": "user", "content": "What is Python?"}],
    temperature=0.7,
)
print(f"   Key 3: {key3[:16]}... (for 'What is Python?' again)")
print(f"   Key 1 == Key 3: {key1 == key3} (deterministic!)")

# Store mock responses
print("\n3. Storing mock LLM responses...")

response1 = {
    "id": "chatcmpl-1",
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "Python is a high-level programming language...",
            }
        }
    ],
}

response2 = {
    "id": "chatcmpl-2",
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "JavaScript is a programming language for web development...",
            }
        }
    ],
}

storage.set(key1, response1, metadata={"provider": "openai", "model": "gpt-4"})
print(f"   Stored response 1")

storage.set(key2, response2, metadata={"provider": "openai", "model": "gpt-4"})
print(f"   Stored response 2")

print(f"   Cache size: {storage.get_size()} entries")

# Retrieve from cache
print("\n4. Retrieving from cache...")

cached1 = storage.get(key1)
print(f"   Retrieved key1: {cached1['choices'][0]['message']['content'][:50]}...")

cached2 = storage.get(key2)
print(f"   Retrieved key2: {cached2['choices'][0]['message']['content'][:50]}...")

# Test cache miss
print("\n5. Testing cache miss...")
nonexistent_key = generate_cache_key(
    provider="openai",
    model="gpt-4",
    messages=[{"role": "user", "content": "Something not cached"}],
    temperature=0.7,
)
result = storage.get(nonexistent_key)
print(f"   Cache miss result: {result}")

# Show statistics
print("\n6. Cache statistics...")
stats = storage.get_stats()
print(f"   Size: {stats['size']}/{stats['max_size']}")
print(f"   Hits: {stats['hits']}")
print(f"   Misses: {stats['misses']}")
print(f"   Hit rate: {stats['hit_rate']}%")

# Test LRU eviction
print("\n7. Testing LRU eviction (max_size=3)...")
print(f"   Current size: {storage.get_size()}")

# Add a third entry
key4 = generate_cache_key(
    provider="openai",
    model="gpt-4",
    messages=[{"role": "user", "content": "What is Rust?"}],
    temperature=0.7,
)
response4 = {
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "Rust is a systems programming language...",
            }
        }
    ]
}
storage.set(key4, response4)
print(f"   Added entry 3, size: {storage.get_size()}")

# Access key1 to make it recently used
storage.get(key1)
print(f"   Accessed key1 to make it recently used")

# Add fourth entry - should evict key2 (least recently used)
key5 = generate_cache_key(
    provider="openai",
    model="gpt-4",
    messages=[{"role": "user", "content": "What is Go?"}],
    temperature=0.7,
)
response5 = {
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "Go is a programming language by Google...",
            }
        }
    ]
}
storage.set(key5, response5)
print(f"   Added entry 4 (should evict LRU), size: {storage.get_size()}")

print(f"\n   Checking which entries remain:")
print(f"   Key1 (Python): {'✓' if storage.get(key1) else '✗'}")
print(f"   Key2 (JavaScript): {'✓' if storage.get(key2) else '✗ (evicted!)'}")
print(f"   Key4 (Rust): {'✓' if storage.get(key4) else '✗'}")
print(f"   Key5 (Go): {'✓' if storage.get(key5) else '✗'}")

# Final statistics
print("\n8. Final statistics...")
stats = storage.get_stats()
print(f"   Total requests: {stats['total_requests']}")
print(f"   Hit rate: {stats['hit_rate']}%")
print(f"   Cache entries: {stats['size']}/{stats['max_size']}")

# Clean up
print("\n9. Cleaning up...")
storage.clear()
print(f"   Cache cleared, size: {storage.get_size()}")

print("\n" + "=" * 60)
print("Test complete!")
print("=" * 60)

# Clean up demo database
import os

if os.path.exists("demo_cache.db"):
    os.remove("demo_cache.db")
    print("Demo database removed")
