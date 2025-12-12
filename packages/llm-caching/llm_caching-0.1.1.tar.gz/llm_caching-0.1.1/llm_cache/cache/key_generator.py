"""
Cache key generation for LLM requests.

Generates deterministic SHA256 hashes from request parameters to use as cache keys.
"""

import hashlib
import json
from typing import Any, Dict, List, Optional, Union


def generate_cache_key(
    provider: str,
    model: str,
    messages: Union[List[Dict[str, Any]], str],
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    **kwargs: Any,
) -> str:
    """
    Generate deterministic cache key from request parameters.

    The cache key includes all parameters that affect the LLM output:
    - Provider (openai, anthropic, etc.)
    - Model name
    - Messages/prompt (full conversation history)
    - Temperature (affects randomness)
    - Max tokens
    - Other sampling parameters (top_p, frequency_penalty, presence_penalty, stop)

    Parameters excluded from cache key:
    - API keys (security)
    - User identifiers
    - Timestamps
    - Stream flags (cache works for both streaming and non-streaming)
    - n parameter (number of completions) - we cache the first completion

    Args:
        provider: LLM provider name (e.g., "openai", "anthropic")
        model: Model identifier (e.g., "gpt-4", "claude-sonnet-4.5")
        messages: List of message dicts or a string prompt
        temperature: Sampling temperature (default: None, treated as provider default)
        max_tokens: Maximum tokens to generate
        **kwargs: Additional parameters (top_p, frequency_penalty, etc.)

    Returns:
        SHA256 hash string (64 hex characters)

    Examples:
        >>> key1 = generate_cache_key(
        ...     provider="openai",
        ...     model="gpt-4",
        ...     messages=[{"role": "user", "content": "Hello"}],
        ...     temperature=0.7
        ... )
        >>> key2 = generate_cache_key(
        ...     provider="openai",
        ...     model="gpt-4",
        ...     messages=[{"role": "user", "content": "Hello"}],
        ...     temperature=0.7
        ... )
        >>> key1 == key2  # Deterministic
        True
    """
    # Normalize provider to lowercase
    provider = provider.lower().strip()

    # Normalize messages format
    if isinstance(messages, str):
        # Convert string prompt to message format
        normalized_messages = [{"role": "user", "content": messages}]
    else:
        normalized_messages = messages

    # Build the key data structure with only relevant parameters
    key_data = {
        "provider": provider,
        "model": model,
        "messages": normalized_messages,
    }

    # Add optional parameters only if provided
    if temperature is not None:
        key_data["temperature"] = temperature

    if max_tokens is not None:
        key_data["max_tokens"] = max_tokens

    # Include other sampling parameters that affect output
    relevant_params = [
        "top_p",
        "top_k",
        "frequency_penalty",
        "presence_penalty",
        "stop",
        "response_format",
        "seed",  # Important for deterministic outputs
    ]

    for param in relevant_params:
        if param in kwargs and kwargs[param] is not None:
            key_data[param] = kwargs[param]

    # Sort keys for deterministic JSON serialization
    # Use separators without spaces for compact representation
    canonical_json = json.dumps(
        key_data, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    )

    # Generate SHA256 hash
    hash_bytes = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

    return hash_bytes


def normalize_request_params(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize request parameters for cache key generation.

    This helper function extracts and normalizes parameters from a raw
    API request dictionary, making it easier to generate cache keys.

    Args:
        request_data: Raw API request data

    Returns:
        Normalized parameters dict for generate_cache_key

    Example:
        >>> request = {
        ...     "model": "gpt-4",
        ...     "messages": [{"role": "user", "content": "Hi"}],
        ...     "temperature": 0.7,
        ...     "api_key": "secret"  # Will be excluded
        ... }
        >>> params = normalize_request_params(request)
        >>> "api_key" in params
        False
    """
    # Parameters to exclude from cache key
    excluded_params = {
        "api_key",
        "authorization",
        "user",
        "stream",
        "n",  # Number of completions - we cache the first one
        "logprobs",
        "echo",
        "best_of",
        "logit_bias",
        "user_id",
        "request_id",
        "metadata",
    }

    # Extract relevant parameters
    normalized = {}
    for key, value in request_data.items():
        if key not in excluded_params and value is not None:
            normalized[key] = value

    return normalized
