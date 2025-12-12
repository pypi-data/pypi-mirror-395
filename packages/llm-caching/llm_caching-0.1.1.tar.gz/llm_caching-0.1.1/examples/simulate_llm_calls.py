"""
Realistic simulation of LLM caching during development.

This script simulates a typical development workflow where you're testing
an LLM application and making repeated calls with the same prompts.
"""

import time

from llm_cache.cache.key_generator import generate_cache_key
from llm_cache.cache.sqlite_storage import SQLiteStorage

print("=" * 70)
print("Simulating LLM Development with Caching")
print("=" * 70)

# Initialize cache
storage = SQLiteStorage(db_path="dev_cache.db", max_size=100)
print(f"\nCache initialized (max_size=100)")


# Simulate LLM API call (with artificial delay)
def mock_llm_api_call(prompt: str, model: str = "gpt-4", temperature: float = 0.7):
    """Simulate an LLM API call with 1 second delay."""
    time.sleep(1.0)  # Simulate network latency
    return {
        "id": f"chatcmpl-{hash(prompt) % 1000}",
        "model": model,
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": f"This is a mock response to: {prompt[:30]}...",
                }
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
    }


def cached_llm_call(prompt: str, model: str = "gpt-4", temperature: float = 0.7):
    """LLM call with caching."""
    # Generate cache key
    key = generate_cache_key(
        provider="openai",
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )

    # Check cache
    cached_response = storage.get(key)
    if cached_response:
        return cached_response, True  # Cache hit

    # Cache miss - call API
    response = mock_llm_api_call(prompt, model, temperature)

    # Store in cache
    storage.set(
        key,
        response,
        metadata={"provider": "openai", "model": model, "timestamp": time.time()},
    )

    return response, False  # Cache miss


# Simulate development workflow
print("\n" + "=" * 70)
print("Scenario: Testing a chatbot feature during development")
print("=" * 70)

test_prompts = [
    "Explain what Python is",
    "How do I use decorators in Python?",
    "What are the benefits of using TypeScript?",
    "Explain what Python is",  # Repeat
    "How do I use decorators in Python?",  # Repeat
    "What is the difference between REST and GraphQL?",
    "Explain what Python is",  # Repeat again
]

print("\nMaking LLM calls (1 second delay for API calls, instant for cache hits):\n")

total_time = 0
cache_hits = 0
cache_misses = 0

for i, prompt in enumerate(test_prompts, 1):
    start = time.time()
    response, hit = cached_llm_call(prompt)
    elapsed = time.time() - start
    total_time += elapsed

    if hit:
        cache_hits += 1
        status = "✓ CACHE HIT"
        time_str = f"{elapsed*1000:.0f}ms"
    else:
        cache_misses += 1
        status = "✗ CACHE MISS (API call)"
        time_str = f"{elapsed:.2f}s"

    print(f"{i}. {status:30} | {time_str:8} | {prompt[:45]}")

# Show results
print("\n" + "=" * 70)
print("Results")
print("=" * 70)

print(f"\nTime saved by caching:")
print(f"  Total time: {total_time:.2f}s")
print(f"  Without cache (all API calls): {len(test_prompts):.2f}s")
print(
    f"  Time saved: {len(test_prompts) - total_time:.2f}s ({((len(test_prompts) - total_time) / len(test_prompts) * 100):.0f}% faster)"
)

print(f"\nCache statistics:")
stats = storage.get_stats()
print(f"  Total requests: {stats['total_requests']}")
print(f"  Cache hits: {cache_hits}")
print(f"  Cache misses: {cache_misses}")
print(f"  Hit rate: {stats['hit_rate']}%")
print(f"  Entries cached: {stats['size']}")

print("\n" + "=" * 70)
print("Key Insight")
print("=" * 70)
print(
    """
During development, you often test the same prompts repeatedly.
With caching:
  - First run: 1 second per call (API latency)
  - Subsequent runs: < 1ms per call (cache hit)

This dramatically speeds up your development iteration cycle!
"""
)

# Clean up
storage.clear()
import os

if os.path.exists("dev_cache.db"):
    os.remove("dev_cache.db")
    print("Demo database cleaned up")
