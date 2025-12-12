"""
Example demonstrating Python SDK wrapper usage.

This shows how to use the LLMCacheWrapper for direct integration
without needing an HTTP proxy.
"""

from llm_cache import LLMCacheWrapper

print("=" * 70)
print("Python SDK Wrapper Examples")
print("=" * 70)

# Example 1: Simple wrapper usage
print("\n" + "=" * 70)
print("Example 1: Basic Wrapper Usage")
print("=" * 70)

print(
    """
from llm_cache import LLMCacheWrapper

# Create wrapper
cache = LLMCacheWrapper()

# Mock LLM function for demonstration
def mock_openai_call(model, messages):
    # This would normally call openai.ChatCompletion.create()
    return {
        "id": "chatcmpl-123",
        "choices": [{
            "message": {"role": "assistant", "content": "Hello!"}
        }]
    }

mock_openai_call.__module__ = "openai"

# Wrap the function
cached_call = cache.wrap(mock_openai_call)

# First call - hits API
response1 = cached_call(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)

# Second call - instant cache hit!
response2 = cached_call(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)
"""
)

# Example 2: Decorator pattern
print("\n" + "=" * 70)
print("Example 2: Decorator Pattern")
print("=" * 70)

print(
    """
from llm_cache import cached

# Simple decorator (no arguments)
@cached
def ask_openai(prompt):
    # This would normally call the OpenAI API
    return openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

# With arguments
@cached(provider="openai")
def ask_gpt(prompt):
    return openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

# Usage
response = ask_openai("What is caching?")  # First call: API
response = ask_openai("What is caching?")  # Second call: cached!
"""
)

# Example 3: Context manager
print("\n" + "=" * 70)
print("Example 3: Context Manager")
print("=" * 70)

print(
    """
from llm_cache import LLMCacheWrapper

# Use as context manager
with LLMCacheWrapper() as cache:
    cached_func = cache.wrap(openai.ChatCompletion.create)

    response = cached_func(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )

    # Check statistics
    stats = cache.get_stats()
    print(f"Cache hits: {stats['hits']}")
    print(f"Cache misses: {stats['misses']}")
"""
)

# Example 4: Real usage with mock
print("\n" + "=" * 70)
print("Example 4: Working Demo with Mock Functions")
print("=" * 70)

# Create cache
cache = LLMCacheWrapper()

# Mock LLM function
call_count = 0


def mock_llm_api(model, messages, temperature=0.7):
    global call_count
    call_count += 1
    return {
        "id": f"response-{call_count}",
        "model": model,
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": f"Mock response #{call_count} to: {messages[0]['content']}",
                }
            }
        ],
    }


# Make it look like OpenAI for auto-detection
mock_llm_api.__module__ = "openai.api_resources"
mock_llm_api.__qualname__ = "ChatCompletion.create"

# Wrap it
cached_llm = cache.wrap(mock_llm_api)

print("\nMaking LLM calls...")

# First call
print("\n1. First call (should hit API):")
response1 = cached_llm(
    model="gpt-4", messages=[{"role": "user", "content": "What is Python?"}]
)
print(f"   Response ID: {response1['id']}")
print(f"   Content: {response1['choices'][0]['message']['content']}")
print(f"   Total API calls: {call_count}")

# Second call with same parameters (should hit cache)
print("\n2. Second call with same params (should hit cache):")
response2 = cached_llm(
    model="gpt-4", messages=[{"role": "user", "content": "What is Python?"}]
)
print(f"   Response ID: {response2['id']}")
print(f"   Content: {response2['choices'][0]['message']['content']}")
print(f"   Total API calls: {call_count}  # Should still be 1!")

# Third call with different parameters (should hit API)
print("\n3. Third call with different params (should hit API):")
response3 = cached_llm(
    model="gpt-4", messages=[{"role": "user", "content": "What is JavaScript?"}]
)
print(f"   Response ID: {response3['id']}")
print(f"   Content: {response3['choices'][0]['message']['content']}")
print(f"   Total API calls: {call_count}")

# Fourth call with different temperature (should hit API)
print("\n4. Fourth call with different temperature (should hit API):")
response4 = cached_llm(
    model="gpt-4",
    messages=[{"role": "user", "content": "What is Python?"}],
    temperature=0.9,
)
print(f"   Response ID: {response4['id']}")
print(f"   Content: {response4['choices'][0]['message']['content']}")
print(f"   Total API calls: {call_count}")

# Show statistics
print("\n" + "=" * 70)
print("Cache Statistics")
print("=" * 70)

stats = cache.get_stats()
print(f"Cache size: {stats['size']}/{stats['max_size']}")
print(f"Hits: {stats['hits']}")
print(f"Misses: {stats['misses']}")
print(f"Hit rate: {stats['hit_rate']}%")

# Example 5: Cache bypass
print("\n" + "=" * 70)
print("Example 5: Cache Bypass")
print("=" * 70)

print("\nBypassing cache with _cache_bypass=True...")
response_bypass = cached_llm(
    model="gpt-4",
    messages=[{"role": "user", "content": "What is Python?"}],
    _cache_bypass=True,
)
print(f"Response ID: {response_bypass['id']}")
print(f"Total API calls: {call_count}  # Incremented even though params match!")

# Example 6: Disabling cache temporarily
print("\n" + "=" * 70)
print("Example 6: Temporarily Disable Caching")
print("=" * 70)

print("\nDisabling cache...")
cache.disable()

response_disabled = cached_llm(
    model="gpt-4", messages=[{"role": "user", "content": "What is Python?"}]
)
print(f"Response ID: {response_disabled['id']}")
print(f"Total API calls: {call_count}  # Not cached!")

print("\nRe-enabling cache...")
cache.enable()

# Example 7: Clearing cache
print("\n" + "=" * 70)
print("Example 7: Clear Cache")
print("=" * 70)

print(f"\nCache size before clear: {cache.storage.get_size()}")
cache.clear_cache()
print(f"Cache size after clear: {cache.storage.get_size()}")

print("\n" + "=" * 70)
print("Summary")
print("=" * 70)

print(
    """
The Python SDK wrapper provides:

1. ✓ Automatic provider detection (OpenAI, Anthropic, etc.)
2. ✓ Transparent caching with zero code changes
3. ✓ Decorator pattern (@cached)
4. ✓ Context manager support
5. ✓ Cache bypass option (_cache_bypass=True)
6. ✓ Enable/disable caching dynamically
7. ✓ Statistics tracking
8. ✓ Works with any LLM SDK

Usage Pattern Comparison:

┌─────────────────────────────────────────────────────────┐
│ Without Cache (Standard SDK Usage)                     │
├─────────────────────────────────────────────────────────┤
│ response = openai.ChatCompletion.create(               │
│     model="gpt-4",                                      │
│     messages=[...]                                      │
│ )                                                       │
│ # Every call hits the API: $$$                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ With Cache (Wrapper Method)                            │
├─────────────────────────────────────────────────────────┤
│ from llm_cache import cached                           │
│                                                         │
│ @cached                                                 │
│ def ask_llm(prompt):                                    │
│     return openai.ChatCompletion.create(               │
│         model="gpt-4",                                  │
│         messages=[{"role": "user", "content": prompt}] │
│     )                                                   │
│                                                         │
│ response = ask_llm("Hello")  # Cached automatically!   │
└─────────────────────────────────────────────────────────┘

Benefits:
- 10-1000x faster development iteration
- Significant cost savings during development
- No API rate limit issues
- Works offline after first call
- Easy to enable/disable
- Minimal code changes
"""
)

print("\n" + "=" * 70)
print("Next Steps")
print("=" * 70)

print(
    """
To use with real OpenAI:

    from llm_cache import cached
    import openai

    @cached
    def ask_gpt(question):
        return openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}]
        )

    # First call hits API
    answer = ask_gpt("What is machine learning?")

    # Subsequent calls are instant!
    answer = ask_gpt("What is machine learning?")

For Anthropic Claude:

    from llm_cache import cached
    import anthropic

    @cached
    def ask_claude(question):
        client = anthropic.Anthropic()
        return client.messages.create(
            model="claude-sonnet-4.5",
            max_tokens=1024,
            messages=[{"role": "user", "content": question}]
        )

See examples/proxy_example_simulated.py for HTTP proxy usage.
"""
)
