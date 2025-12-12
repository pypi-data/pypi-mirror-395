"""
HTTP Proxy Server for LLM caching.

This FastAPI server provides transparent caching for LLM API calls.
Point your LLM SDK to this server and all requests will be cached automatically.
"""

import asyncio
import json
import logging
from typing import AsyncGenerator

import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse, StreamingResponse

from llm_cache.cache.key_generator import generate_cache_key, normalize_request_params
from llm_cache.cache.storage import CacheStorage
from llm_cache.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="LLM Cache Proxy",
    description="Transparent caching proxy for LLM API calls",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Initialize configuration and storage
config = Config()
storage: CacheStorage = config.get_storage()

# Provider endpoint mappings
PROVIDER_ENDPOINTS = {
    "openai": "https://api.openai.com",
    "anthropic": "https://api.anthropic.com",
}

# Default provider (can be overridden with X-LLM-Provider header)
DEFAULT_PROVIDER = "openai"


async def replay_cached_stream(cached_response: dict) -> AsyncGenerator[str, None]:
    """
    Replay a cached response as a Server-Sent Events stream.

    Converts a cached non-streaming response into SSE format to simulate
    streaming behavior for cache hits.
    """
    # For OpenAI-style responses, simulate streaming
    if "choices" in cached_response:
        for choice in cached_response.get("choices", []):
            # Send the full message as a single chunk (could be enhanced to split by words/tokens)
            chunk = {
                "id": cached_response.get("id", "cached"),
                "object": "chat.completion.chunk",
                "created": cached_response.get("created", 0),
                "model": cached_response.get("model", ""),
                "choices": [
                    {
                        "index": choice.get("index", 0),
                        "delta": choice.get("message", {}),
                        "finish_reason": choice.get("finish_reason"),
                    }
                ],
            }
            yield f"data: {json.dumps(chunk)}\n\n"
            await asyncio.sleep(0.01)  # Small delay to simulate streaming

    # Send [DONE] marker
    yield "data: [DONE]\n\n"


async def collect_and_forward_stream(
    response: httpx.Response, cache_key: str, provider: str, model: str
) -> AsyncGenerator[bytes, None]:
    """
    Collect streaming response while forwarding it to the client.

    This allows us to cache the full response while still providing
    real-time streaming to the client.
    """
    collected_chunks = []
    full_content = ""

    async for chunk in response.aiter_bytes():
        # Forward chunk to client
        yield chunk

        # Collect for caching
        collected_chunks.append(chunk)

    # After stream completes, parse and cache the response
    try:
        # Combine all chunks
        full_response = b"".join(collected_chunks).decode("utf-8")

        # Parse SSE events to reconstruct the response
        # For now, we cache the raw stream data
        # In production, you might want to reconstruct the full response object
        cache_data = {
            "stream_data": full_response,
            "type": "stream",
        }

        storage.set(
            cache_key,
            cache_data,
            metadata={"provider": provider, "model": model, "streamed": True},
        )
        logger.info(f"Cached streaming response: {cache_key[:16]}...")
    except Exception as e:
        logger.error(f"Failed to cache streaming response: {e}")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "LLM Cache Proxy",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "openai_chat": "/v1/chat/completions",
            "anthropic_messages": "/v1/messages",
            "stats": "/cache/stats",
            "clear": "/cache/clear",
            "health": "/health",
            "docs": "/docs",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        size = storage.get_size()
        return {
            "status": "healthy",
            "cache_size": size,
            "cache_max_size": storage.max_size,
            "backend": config.backend,
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503, content={"status": "unhealthy", "error": str(e)}
        )


@app.post("/v1/chat/completions")
async def proxy_chat_completions(request: Request):
    """
    OpenAI-compatible chat completions endpoint.

    Supports both streaming and non-streaming requests.
    Caches responses and returns from cache on hit.
    Compatible with OpenAI SDK and any OpenAI-compatible API.

    Headers:
        - Authorization: Bearer token for the upstream API
        - X-LLM-Provider: Provider name (default: openai)
        - X-Cache-Bypass: Set to 'true' to bypass cache

    Response Headers:
        - X-Cache-Hit: 'true' if served from cache, 'false' otherwise
    """
    try:
        # Parse request body
        body = await request.json()

        # Get provider from header or default
        provider = request.headers.get("X-LLM-Provider", DEFAULT_PROVIDER).lower()

        # Check if this is a streaming request
        is_streaming = body.get("stream", False)

        # Check if cache should be bypassed
        bypass_cache = request.headers.get("X-Cache-Bypass", "false").lower() == "true"

        # Normalize request parameters for cache key
        normalized = normalize_request_params(body)

        # Generate cache key
        cache_key = generate_cache_key(provider=provider, **normalized)

        logger.info(
            f"Request: model={body.get('model')}, provider={provider}, "
            f"stream={is_streaming}, cache_key={cache_key[:16]}..."
        )

        # Check cache (unless bypassed)
        if not bypass_cache:
            cached_response = storage.get(cache_key)
            if cached_response:
                logger.info(f"Cache hit: {cache_key[:16]}...")

                # If client requested streaming, replay cache as stream
                if is_streaming:
                    return StreamingResponse(
                        replay_cached_stream(cached_response),
                        media_type="text/event-stream",
                        headers={"X-Cache-Hit": "true"},
                    )
                else:
                    return JSONResponse(
                        content=cached_response, headers={"X-Cache-Hit": "true"}
                    )

        # Cache miss - forward to actual LLM API
        logger.info(f"Cache miss: {cache_key[:16]}... - forwarding to {provider}")

        # Get target URL
        if provider not in PROVIDER_ENDPOINTS:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown provider: {provider}. Supported: {list(PROVIDER_ENDPOINTS.keys())}",
            )

        target_url = f"{PROVIDER_ENDPOINTS[provider]}/v1/chat/completions"

        # Forward request with original headers
        async with httpx.AsyncClient(timeout=120.0) as client:
            # Prepare headers (exclude some proxy-specific headers)
            headers = dict(request.headers)
            excluded_headers = {
                "host",
                "x-llm-provider",
                "x-cache-bypass",
                "content-length",
            }
            headers = {
                k: v for k, v in headers.items() if k.lower() not in excluded_headers
            }

            try:
                if is_streaming:
                    # For streaming, we need to handle it differently
                    response = await client.post(
                        target_url, json=body, headers=headers, timeout=120.0
                    )

                    if response.status_code == 200:
                        # Return streaming response while collecting for cache
                        return StreamingResponse(
                            collect_and_forward_stream(
                                response, cache_key, provider, body.get("model", "")
                            ),
                            media_type="text/event-stream",
                            headers={"X-Cache-Hit": "false"},
                        )
                    else:
                        logger.warning(f"API error: {response.status_code}")
                        return Response(
                            content=response.content,
                            status_code=response.status_code,
                            headers=dict(response.headers),
                        )
                else:
                    # Non-streaming request
                    response = await client.post(target_url, json=body, headers=headers)

                    if response.status_code == 200:
                        response_data = response.json()

                        # Cache the response
                        storage.set(
                            cache_key,
                            response_data,
                            metadata={
                                "provider": provider,
                                "model": body.get("model"),
                                "status_code": response.status_code,
                            },
                        )
                        logger.info(f"Cached response: {cache_key[:16]}...")

                        return JSONResponse(
                            content=response_data, headers={"X-Cache-Hit": "false"}
                        )
                    else:
                        # Return error response without caching
                        logger.warning(f"API error: {response.status_code}")
                        return Response(
                            content=response.content,
                            status_code=response.status_code,
                            headers=dict(response.headers),
                        )

            except httpx.RequestError as e:
                logger.error(f"Request to {provider} failed: {e}")
                raise HTTPException(
                    status_code=502, detail=f"Failed to connect to {provider}: {str(e)}"
                )

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in request body")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/messages")
async def proxy_anthropic_messages(request: Request):
    """
    Anthropic-compatible messages endpoint.

    Caches Claude API responses.
    Compatible with Anthropic SDK.

    Headers:
        - x-api-key: API key for Anthropic
        - anthropic-version: API version (e.g., 2023-06-01)
        - X-Cache-Bypass: Set to 'true' to bypass cache

    Response Headers:
        - X-Cache-Hit: 'true' if served from cache, 'false' otherwise
    """
    try:
        # Parse request body
        body = await request.json()

        # Check if cache should be bypassed
        bypass_cache = request.headers.get("X-Cache-Bypass", "false").lower() == "true"

        # Normalize and generate cache key
        normalized = normalize_request_params(body)
        cache_key = generate_cache_key(provider="anthropic", **normalized)

        logger.info(
            f"Anthropic request: model={body.get('model')}, cache_key={cache_key[:16]}..."
        )

        # Check cache
        if not bypass_cache:
            cached_response = storage.get(cache_key)
            if cached_response:
                logger.info(f"Cache hit: {cache_key[:16]}...")
                return JSONResponse(
                    content=cached_response, headers={"X-Cache-Hit": "true"}
                )

        # Cache miss - forward to Anthropic API
        logger.info(f"Cache miss: {cache_key[:16]}... - forwarding to Anthropic")

        target_url = f"{PROVIDER_ENDPOINTS['anthropic']}/v1/messages"

        # Forward request
        async with httpx.AsyncClient(timeout=120.0) as client:
            headers = dict(request.headers)
            excluded_headers = {"host", "x-cache-bypass", "content-length"}
            headers = {
                k: v for k, v in headers.items() if k.lower() not in excluded_headers
            }

            try:
                response = await client.post(target_url, json=body, headers=headers)
            except httpx.RequestError as e:
                logger.error(f"Request to Anthropic failed: {e}")
                raise HTTPException(
                    status_code=502, detail=f"Failed to connect to Anthropic: {str(e)}"
                )

        # Cache successful responses
        if response.status_code == 200:
            response_data = response.json()

            storage.set(
                cache_key,
                response_data,
                metadata={
                    "provider": "anthropic",
                    "model": body.get("model"),
                    "status_code": response.status_code,
                },
            )
            logger.info(f"Cached response: {cache_key[:16]}...")

            return JSONResponse(content=response_data, headers={"X-Cache-Hit": "false"})
        else:
            logger.warning(f"Anthropic API error: {response.status_code}")
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
            )

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in request body")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cache/stats")
async def get_cache_stats():
    """
    Get cache statistics.

    Returns hit/miss rates, cache size, and other metrics.
    """
    try:
        stats = storage.get_stats()
        return {
            "status": "success",
            "stats": stats,
            "config": {"backend": config.backend, "max_size": config.max_size},
        }
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/cache/clear")
async def clear_cache():
    """
    Clear all cache entries.

    Use with caution - this will remove all cached responses.
    """
    try:
        stats_before = storage.get_stats()
        storage.clear()
        logger.info("Cache cleared")

        return {
            "status": "success",
            "message": "Cache cleared successfully",
            "entries_removed": stats_before["size"],
        }
    except Exception as e:
        logger.error(f"Failed to clear cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cache/delete/{key}")
async def delete_cache_entry(key: str):
    """
    Delete a specific cache entry by key.

    Args:
        key: Cache key to delete
    """
    try:
        deleted = storage.delete(key)
        if deleted:
            logger.info(f"Deleted cache entry: {key[:16]}...")
            return {"status": "success", "message": "Cache entry deleted", "key": key}
        else:
            raise HTTPException(status_code=404, detail="Cache entry not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete cache entry: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def main():
    """Run the proxy server."""
    import uvicorn

    logger.info("Starting LLM Cache Proxy Server")
    logger.info(f"Backend: {config.backend}")
    logger.info(f"Max cache size: {config.max_size}")
    logger.info(f"Listening on {config.proxy_host}:{config.proxy_port}")

    uvicorn.run(app, host=config.proxy_host, port=config.proxy_port, log_level="info")


if __name__ == "__main__":
    main()
