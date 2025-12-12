"""
LLM Cache - Cache LLM API calls to speed up development.

A caching system for LLM API calls that provides:
- HTTP proxy server for transparent caching
- Python SDK wrapper for direct integration
- SQLite and Redis storage backends
- LRU eviction with configurable size limits
"""

__version__ = "0.1.0"

from llm_cache.config import Config
from llm_cache.wrapper.sdk import LLMCacheWrapper, cached

__all__ = ["LLMCacheWrapper", "cached", "Config"]
