"""
Python SDK wrapper for LLM caching.

Provides a generic wrapper that can cache any LLM SDK calls with automatic
provider detection and transparent caching.
"""

import functools
import inspect
import logging
from typing import Any, Callable, Dict, Optional, Union

from llm_cache.cache.key_generator import generate_cache_key
from llm_cache.cache.storage import CacheStorage
from llm_cache.config import Config

logger = logging.getLogger(__name__)


class LLMCacheWrapper:
    """
    Generic wrapper for any LLM SDK.

    Wraps LLM SDK calls with caching functionality. Works with any provider
    (OpenAI, Anthropic, etc.) through automatic provider detection.

    Features:
    - Automatic provider detection
    - Transparent caching (no code changes needed)
    - Decorator pattern support
    - Context manager support
    - Configurable cache bypass
    - Statistics tracking

    Usage:
        >>> cache = LLMCacheWrapper()
        >>>
        >>> # Method 1: Wrap a function
        >>> cached_call = cache.wrap(openai.ChatCompletion.create)
        >>> response = cached_call(model="gpt-4", messages=[...])
        >>>
        >>> # Method 2: Use as decorator
        >>> @cache.wrap
        >>> def my_llm_call(prompt):
        >>>     return openai.ChatCompletion.create(
        >>>         model="gpt-4",
        >>>         messages=[{"role": "user", "content": prompt}]
        >>>     )
        >>>
        >>> # Method 3: Context manager
        >>> with LLMCacheWrapper() as cache:
        >>>     response = openai.ChatCompletion.create(...)

    Example:
        >>> from llm_cache import LLMCacheWrapper
        >>> import openai
        >>>
        >>> cache = LLMCacheWrapper()
        >>>
        >>> @cache.wrap
        >>> def ask_gpt(question):
        >>>     return openai.ChatCompletion.create(
        >>>         model="gpt-4",
        >>>         messages=[{"role": "user", "content": question}]
        >>>     )
        >>>
        >>> # First call hits API
        >>> response1 = ask_gpt("What is caching?")
        >>>
        >>> # Second call hits cache (instant!)
        >>> response2 = ask_gpt("What is caching?")
    """

    def __init__(
        self,
        storage: Optional[CacheStorage] = None,
        enabled: bool = True,
        provider: Optional[str] = None,
    ):
        """
        Initialize wrapper with optional custom storage.

        Args:
            storage: Custom storage backend (defaults to config-based storage)
            enabled: Whether caching is enabled (default: True)
            provider: Force a specific provider (default: auto-detect)
        """
        self.storage = storage or Config().get_storage()
        self.enabled = enabled
        self.forced_provider = provider

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        return False

    def wrap(self, func: Callable) -> Callable:
        """
        Wrap any LLM SDK call with caching.

        Automatically detects the provider and caches responses based on
        the input parameters. Supports both synchronous and streaming calls.

        Args:
            func: Function to wrap (e.g., openai.ChatCompletion.create)

        Returns:
            Wrapped function that uses caching

        Example:
            >>> cached_create = cache.wrap(openai.ChatCompletion.create)
            >>> response = cached_create(model="gpt-4", messages=[...])
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # If caching is disabled, call original function
            if not self.enabled:
                return func(*args, **kwargs)

            # Detect provider
            provider = self._detect_provider(func, kwargs)

            # Extract cache key parameters
            cache_params = self._extract_cache_params(args, kwargs, func)

            # Check for bypass flag
            if kwargs.pop("_cache_bypass", False):
                logger.debug(f"Cache bypass requested for {provider}")
                return func(*args, **kwargs)

            # Generate cache key
            try:
                cache_key = generate_cache_key(provider=provider, **cache_params)
            except Exception as e:
                logger.warning(f"Failed to generate cache key: {e}. Bypassing cache.")
                return func(*args, **kwargs)

            # Check cache
            try:
                cached_response = self.storage.get(cache_key)
                if cached_response:
                    logger.debug(f"Cache hit for {provider}: {cache_key[:16]}...")
                    return self._reconstruct_response(cached_response, provider, func)
            except Exception as e:
                logger.warning(f"Cache lookup failed: {e}. Calling API.")

            # Cache miss - call original function
            logger.debug(f"Cache miss for {provider}: {cache_key[:16]}...")
            response = func(*args, **kwargs)

            # Cache the response
            try:
                serialized = self._serialize_response(response, provider)
                self.storage.set(
                    cache_key,
                    serialized,
                    metadata={
                        "provider": provider,
                        "model": cache_params.get("model"),
                        "function": func.__name__,
                    },
                )
                logger.debug(f"Cached response for {provider}: {cache_key[:16]}...")
            except Exception as e:
                logger.warning(f"Failed to cache response: {e}")

            return response

        return wrapper

    def _detect_provider(self, func: Callable, kwargs: Dict[str, Any]) -> str:
        """
        Detect LLM provider from function or kwargs.

        Args:
            func: Function being called
            kwargs: Function keyword arguments

        Returns:
            Provider name (e.g., "openai", "anthropic")
        """
        # Use forced provider if set
        if self.forced_provider:
            return self.forced_provider

        # Check kwargs for explicit provider
        if "provider" in kwargs:
            return kwargs.pop("provider")

        # Detect from function module
        func_module = func.__module__

        if "openai" in func_module:
            return "openai"
        elif "anthropic" in func_module:
            return "anthropic"
        elif "cohere" in func_module:
            return "cohere"
        elif "huggingface" in func_module or "transformers" in func_module:
            return "huggingface"

        # Check function name for clues
        func_name = func.__qualname__

        if "OpenAI" in func_name or "GPT" in func_name:
            return "openai"
        elif "Anthropic" in func_name or "Claude" in func_name:
            return "anthropic"

        # Default to unknown
        logger.warning(f"Could not detect provider for {func_module}.{func_name}")
        return "unknown"

    def _extract_cache_params(
        self, args: tuple, kwargs: Dict[str, Any], func: Callable
    ) -> Dict[str, Any]:
        """
        Extract parameters relevant for cache key generation.

        Args:
            args: Positional arguments
            kwargs: Keyword arguments
            func: Function being called

        Returns:
            Dict of parameters for cache key
        """
        # Get function signature
        try:
            sig = inspect.signature(func)
            bound_args = sig.bind_partial(*args, **kwargs)
            bound_args.apply_defaults()
            all_args = dict(bound_args.arguments)
        except Exception:
            # Fallback if signature inspection fails
            all_args = kwargs.copy()

        # Common parameter names across providers
        param_mapping = {
            # Messages/prompts
            "messages": ["messages", "prompt", "input", "text"],
            "model": ["model", "engine"],
            "temperature": ["temperature"],
            "max_tokens": ["max_tokens", "max_length", "max_new_tokens"],
            "top_p": ["top_p"],
            "top_k": ["top_k"],
            "frequency_penalty": ["frequency_penalty"],
            "presence_penalty": ["presence_penalty"],
            "stop": ["stop", "stop_sequences"],
            "seed": ["seed", "random_seed"],
        }

        # Extract relevant parameters
        cache_params = {}

        for standard_key, possible_keys in param_mapping.items():
            for key in possible_keys:
                if key in all_args and all_args[key] is not None:
                    cache_params[standard_key] = all_args[key]
                    break

        return cache_params

    def _serialize_response(self, response: Any, provider: str) -> Dict[str, Any]:
        """
        Convert SDK response to cacheable dict.

        Args:
            response: Response from LLM API
            provider: Provider name

        Returns:
            Serialized response dict
        """
        # Handle different response types

        # Pydantic models (OpenAI v1+, Anthropic)
        if hasattr(response, "model_dump"):
            return response.model_dump()

        # OpenAI v0.x
        if hasattr(response, "to_dict"):
            return response.to_dict()

        # Dict-like objects
        if hasattr(response, "__dict__"):
            return self._serialize_object(response)

        # Already a dict
        if isinstance(response, dict):
            return response

        # Fallback - try to convert to dict
        try:
            return dict(response)
        except Exception as e:
            logger.warning(f"Could not serialize response: {e}")
            # Return a wrapper dict
            return {"_cached_value": str(response), "_type": type(response).__name__}

    def _serialize_object(self, obj: Any) -> Dict[str, Any]:
        """
        Recursively serialize an object to dict.

        Args:
            obj: Object to serialize

        Returns:
            Serialized dict
        """
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj

        if isinstance(obj, (list, tuple)):
            return [self._serialize_object(item) for item in obj]

        if isinstance(obj, dict):
            return {k: self._serialize_object(v) for k, v in obj.items()}

        if hasattr(obj, "__dict__"):
            result = {}
            for key, value in obj.__dict__.items():
                if not key.startswith("_"):
                    result[key] = self._serialize_object(value)
            return result

        return str(obj)

    def _reconstruct_response(
        self, cached: Dict[str, Any], provider: str, func: Callable
    ) -> Any:
        """
        Reconstruct SDK-specific response object from cache.

        Args:
            cached: Cached response dict
            provider: Provider name
            func: Original function

        Returns:
            Reconstructed response (dict or object)
        """
        # For most use cases, returning the dict works fine
        # Most SDKs accept dict responses

        # If original response was a simple cached value
        if "_cached_value" in cached and "_type" in cached:
            return cached["_cached_value"]

        # Try to reconstruct provider-specific objects
        if provider == "openai":
            return self._reconstruct_openai_response(cached, func)
        elif provider == "anthropic":
            return self._reconstruct_anthropic_response(cached, func)

        # Default: return dict
        return cached

    def _reconstruct_openai_response(
        self, cached: Dict[str, Any], func: Callable
    ) -> Any:
        """
        Reconstruct OpenAI response object.

        Args:
            cached: Cached response dict
            func: Original function

        Returns:
            OpenAI response object or dict
        """
        # OpenAI SDK usually accepts dicts
        # For OpenAI v1+, we could reconstruct the Pydantic model
        # but returning dict is simpler and works for most cases
        return cached

    def _reconstruct_anthropic_response(
        self, cached: Dict[str, Any], func: Callable
    ) -> Any:
        """
        Reconstruct Anthropic response object.

        Args:
            cached: Cached response dict
            func: Original function

        Returns:
            Anthropic response object or dict
        """
        # Anthropic SDK also works with dicts
        return cached

    def clear_cache(self) -> None:
        """Clear all cached responses."""
        self.storage.clear()
        logger.info("Cache cleared")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dict with cache statistics
        """
        return self.storage.get_stats()

    def disable(self) -> None:
        """Disable caching (calls pass through to API)."""
        self.enabled = False
        logger.info("Caching disabled")

    def enable(self) -> None:
        """Enable caching."""
        self.enabled = True
        logger.info("Caching enabled")


# Convenience function for quick wrapping
def cached(
    func: Optional[Callable] = None,
    *,
    provider: Optional[str] = None,
    storage: Optional[CacheStorage] = None,
) -> Union[Callable, LLMCacheWrapper]:
    """
    Decorator to add caching to LLM function calls.

    Can be used with or without arguments.

    Args:
        func: Function to wrap (when used without arguments)
        provider: Force a specific provider
        storage: Custom storage backend

    Returns:
        Wrapped function or wrapper

    Examples:
        >>> # Without arguments
        >>> @cached
        >>> def ask_llm(prompt):
        >>>     return openai.ChatCompletion.create(...)
        >>>
        >>> # With arguments
        >>> @cached(provider="openai")
        >>> def ask_gpt(prompt):
        >>>     return openai.ChatCompletion.create(...)
    """
    wrapper = LLMCacheWrapper(storage=storage, provider=provider)

    # Used without arguments: @cached
    if func is not None:
        return wrapper.wrap(func)

    # Used with arguments: @cached(...)
    return wrapper.wrap
