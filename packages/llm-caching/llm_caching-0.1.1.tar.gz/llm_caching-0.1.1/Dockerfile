# Multi-stage build for smaller final image
FROM python:3.13-slim as builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN uv sync --no-dev --no-install-project

# Final stage
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy uv and dependencies from builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY llm_cache ./llm_cache
COPY pyproject.toml ./
COPY README.md ./

# Install the package
RUN uv pip install --system -e .

# Create non-root user
RUN useradd -m -u 1000 llmcache && \
    chown -R llmcache:llmcache /app

USER llmcache

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')" || exit 1

# Run the proxy server
CMD ["python", "-m", "llm_cache.proxy.server"]
