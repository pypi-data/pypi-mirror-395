# Production Deployment Guide

This guide covers deploying LLM Cache in production with Redis for scalable, shared caching.

## Table of Contents

- [Quick Start with Docker Compose](#quick-start-with-docker-compose)
- [Manual Deployment](#manual-deployment)
- [Redis Configuration](#redis-configuration)
- [Security Best Practices](#security-best-practices)
- [Monitoring](#monitoring)
- [Scaling](#scaling)
- [Troubleshooting](#troubleshooting)

## Quick Start with Docker Compose

The fastest way to deploy LLM Cache with Redis in production:

### 1. Clone and Configure

```bash
# Clone the repository
git clone https://github.com/your-org/llm-caching.git
cd llm-caching

# Create environment file
cp .env.example .env

# Edit configuration
nano .env
```

### 2. Start Services

```bash
# Build and start
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f llm-caching
```

### 3. Verify Deployment

```bash
# Health check
curl http://localhost:8000/health

# Cache stats
curl http://localhost:8000/cache/stats
```

The proxy is now running on `http://localhost:8000` with Redis backing.

## Manual Deployment

For custom deployments without Docker:

### Prerequisites

- Python 3.9+
- Redis 6.0+
- uv (for dependency management)

### 1. Install Redis

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

**macOS:**
```bash
brew install redis
brew services start redis
```

**Docker:**
```bash
docker run -d \
  --name redis \
  -p 6379:6379 \
  -v redis-data:/data \
  redis:7-alpine \
  redis-server --maxmemory 2gb --maxmemory-policy allkeys-lru
```

### 2. Install LLM Cache

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone https://github.com/your-org/llm-caching.git
cd llm-caching

# Install dependencies
uv sync
```

### 3. Configure Environment

Create `.env` file:

```bash
# Backend
LLM_CACHE_BACKEND=redis

# Redis connection
LLM_CACHE_REDIS_HOST=localhost
LLM_CACHE_REDIS_PORT=6379
LLM_CACHE_REDIS_DB=0
LLM_CACHE_REDIS_PASSWORD=your_secure_password

# Cache settings
LLM_CACHE_MAX_SIZE=10000

# Proxy settings
LLM_CACHE_PROXY_HOST=0.0.0.0
LLM_CACHE_PROXY_PORT=8000
```

### 4. Run as Systemd Service

Create `/etc/systemd/system/llm-caching.service`:

```ini
[Unit]
Description=LLM Cache Proxy Server
After=network.target redis.service
Requires=redis.service

[Service]
Type=simple
User=llmcache
WorkingDirectory=/opt/llm-caching
EnvironmentFile=/opt/llm-caching/.env
ExecStart=/usr/local/bin/uv run llm-caching-proxy
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable llm-caching
sudo systemctl start llm-caching
sudo systemctl status llm-caching
```

## Redis Configuration

### Recommended Production Settings

Edit `/etc/redis/redis.conf`:

```conf
# Memory management
maxmemory 4gb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000
appendonly yes
appendfsync everysec

# Security
requirepass YOUR_STRONG_PASSWORD
bind 127.0.0.1
protected-mode yes

# Performance
tcp-backlog 511
timeout 0
tcp-keepalive 300
```

Restart Redis:

```bash
sudo systemctl restart redis
```

### Redis Cluster (High Availability)

For production workloads with multiple instances:

```bash
# redis-cluster.yml
version: '3.8'
services:
  redis-node-1:
    image: redis:7-alpine
    command: redis-server --cluster-enabled yes --cluster-config-file nodes.conf
    ports:
      - "6379:6379"

  redis-node-2:
    image: redis:7-alpine
    command: redis-server --cluster-enabled yes --cluster-config-file nodes.conf
    ports:
      - "6380:6379"

  redis-node-3:
    image: redis:7-alpine
    command: redis-server --cluster-enabled yes --cluster-config-file nodes.conf
    ports:
      - "6381:6379"
```

## Security Best Practices

### 1. Enable Authentication

**Redis:**
```bash
# Set Redis password
redis-cli
> CONFIG SET requirepass "strong_password_here"
> CONFIG REWRITE
```

**LLM Cache:**
```bash
LLM_CACHE_REDIS_PASSWORD=strong_password_here
```

### 2. Use TLS/SSL

For production, enable TLS between proxy and Redis:

```bash
# Generate certificates
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout redis.key -out redis.crt

# Configure Redis with TLS
redis-server \
  --tls-port 6380 \
  --port 0 \
  --tls-cert-file redis.crt \
  --tls-key-file redis.key \
  --tls-ca-cert-file ca.crt
```

### 3. Network Security

- Use firewall rules to restrict access
- Deploy in private network/VPC
- Use reverse proxy (nginx, Caddy) for HTTPS

**nginx Example:**

```nginx
server {
    listen 443 ssl http2;
    server_name cache.example.com;

    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. Rate Limiting

Protect your proxy with rate limiting:

```nginx
limit_req_zone $binary_remote_addr zone=llm_cache:10m rate=10r/s;

server {
    location / {
        limit_req zone=llm_cache burst=20 nodelay;
        proxy_pass http://localhost:8000;
    }
}
```

## Monitoring

### Health Checks

```bash
# Basic health
curl http://localhost:8000/health

# Cache statistics
curl http://localhost:8000/cache/stats | jq
```

### Prometheus Metrics (Future Enhancement)

Add to your monitoring stack:

```yaml
scrape_configs:
  - job_name: 'llm-caching'
    static_configs:
      - targets: ['localhost:8000']
```

### Redis Monitoring

```bash
# Monitor Redis
redis-cli INFO stats

# Key metrics
redis-cli INFO keyspace
redis-cli INFO memory
```

### Logging

Configure structured logging:

```python
# In production, use JSON logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}'
)
```

## Scaling

### Horizontal Scaling

Multiple proxy instances with shared Redis:

```yaml
# docker-compose-scaled.yml
services:
  llm-caching:
    build: .
    deploy:
      replicas: 3
    environment:
      LLM_CACHE_BACKEND: redis
      LLM_CACHE_REDIS_HOST: redis
    ports:
      - "8000-8002:8000"

  redis:
    image: redis:7-alpine
    ...

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

**Load Balancer Config (nginx.conf):**

```nginx
upstream llm_cache_backend {
    least_conn;
    server llm-caching-1:8000;
    server llm-caching-2:8000;
    server llm-caching-3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://llm_cache_backend;
    }
}
```

### Vertical Scaling

Increase Redis memory:

```bash
# docker-compose.yml
redis:
  command: >
    redis-server
    --maxmemory 8gb
    --maxmemory-policy allkeys-lru
```

Adjust cache size:

```bash
LLM_CACHE_MAX_SIZE=50000  # Increase cache capacity
```

## Troubleshooting

### Connection Issues

```bash
# Test Redis connection
redis-cli ping

# Check if Redis is accepting connections
redis-cli -h localhost -p 6379 INFO server

# Test proxy health
curl -v http://localhost:8000/health
```

### Performance Issues

```bash
# Check cache hit rate
curl http://localhost:8000/cache/stats | jq '.stats.hit_rate'

# Monitor Redis slowlog
redis-cli SLOWLOG GET 10

# Check memory usage
redis-cli INFO memory
```

### Cache Not Working

```bash
# Verify configuration
curl http://localhost:8000/health | jq

# Check logs
docker-compose logs llm-caching

# Test cache manually
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_KEY" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "test"}]
  }'
```

### Clear Cache

```bash
# Clear via API
curl -X DELETE http://localhost:8000/cache/clear

# Clear Redis directly
redis-cli FLUSHDB
```

## Performance Tuning

### Redis Optimization

```conf
# Disable persistence for maximum performance (if acceptable)
save ""
appendonly no

# Increase client connections
maxclients 10000

# Optimize memory
activedefrag yes
```

### Proxy Optimization

```bash
# Increase worker processes (for uvicorn)
uvicorn llm_cache.proxy.server:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --loop uvloop
```

## Backup and Recovery

### Backup Redis Data

```bash
# Automatic backups
redis-cli BGSAVE

# Copy RDB file
cp /var/lib/redis/dump.rdb /backup/dump-$(date +%Y%m%d).rdb

# Automated backup script
#!/bin/bash
redis-cli BGSAVE
sleep 10
cp /var/lib/redis/dump.rdb /backup/dump-$(date +%Y%m%d-%H%M%S).rdb
```

### Restore from Backup

```bash
# Stop Redis
sudo systemctl stop redis

# Replace data file
sudo cp /backup/dump-20240101.rdb /var/lib/redis/dump.rdb
sudo chown redis:redis /var/lib/redis/dump.rdb

# Start Redis
sudo systemctl start redis
```

## Cost Optimization

### Memory Management

```bash
# Monitor memory usage
redis-cli INFO memory | grep used_memory_human

# Adjust max size based on budget
LLM_CACHE_MAX_SIZE=5000  # Smaller cache = less memory
```

### Cache Eviction Tuning

```bash
# More aggressive eviction
redis-cli CONFIG SET maxmemory-policy volatile-lru

# TTL for entries (future feature)
LLM_CACHE_TTL=86400  # 24 hours
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/your-org/llm-caching/issues
- Documentation: https://github.com/your-org/llm-caching
- Email: support@example.com
