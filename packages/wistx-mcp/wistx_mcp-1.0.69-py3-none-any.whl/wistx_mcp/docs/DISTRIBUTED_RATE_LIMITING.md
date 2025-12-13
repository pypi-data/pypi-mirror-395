# Distributed Rate Limiting with Google Cloud Memorystore

## Overview

The WISTX MCP server supports **distributed rate limiting** using Google Cloud Memorystore (Redis) for horizontal scaling on Cloud Run. This ensures rate limits are enforced globally across all server instances.

## Architecture

### Without Distributed Rate Limiting (In-Memory)
```
Instance 1: User A has made 50 requests (in-memory counter)
Instance 2: User A has made 0 requests (separate counter)
Instance 3: User A has made 0 requests (separate counter)
```
**Problem:** User can bypass rate limits by hitting different instances.

### With Distributed Rate Limiting (Redis)
```
Instance 1: Checks Redis → User A has 50 requests (shared counter)
Instance 2: Checks Redis → User A has 50 requests (shared counter)
Instance 3: Checks Redis → User A has 50 requests (shared counter)
```
**Solution:** All instances share the same rate limit counters via Redis.

## Implementation

The rate limiter automatically detects Redis/Memorystore configuration and uses distributed rate limiting when available, falling back to in-memory rate limiting if Redis is not configured.

### Redis Sorted Sets

We use Redis sorted sets (ZSET) for efficient time-window queries:

```python
# Key: rate_limit:user123:tool_hash
# Value: Sorted set with timestamps as scores
# Operations:
# 1. Remove old entries (outside time window)
# 2. Count current entries
# 3. Add new entry with current timestamp
# 4. Set TTL for automatic cleanup
```

## Configuration

### Option 1: Google Cloud Memorystore (Recommended for Cloud Run)

Set these environment variables:

```bash
MEMORYSTORE_ENABLED=true
MEMORYSTORE_HOST=<your-memorystore-instance-ip>
MEMORYSTORE_PORT=6379
```

**Example:**
```bash
MEMORYSTORE_ENABLED=true
MEMORYSTORE_HOST=10.0.0.3
MEMORYSTORE_PORT=6379
```

### Option 2: Redis URL

Alternatively, use a Redis URL:

```bash
REDIS_URL=redis://host:port
# Or with authentication:
REDIS_URL=redis://user:password@host:port/0
```

**Example:**
```bash
REDIS_URL=redis://10.0.0.3:6379
```

### Option 3: In-Memory (Development/Testing)

If neither `MEMORYSTORE_ENABLED` nor `REDIS_URL` is set, the server automatically falls back to in-memory rate limiting.

## Google Cloud Run Setup

### 1. Create Memorystore Instance

```bash
gcloud redis instances create wistx-rate-limit \
  --size=1 \
  --region=us-central1 \
  --redis-version=redis_7_0 \
  --tier=basic
```

### 2. Get Instance IP

```bash
gcloud redis instances describe wistx-rate-limit \
  --region=us-central1 \
  --format="value(host)"
```

### 3. Configure Cloud Run Service

Set environment variables in Cloud Run:

```bash
gcloud run services update wistx-mcp \
  --set-env-vars="MEMORYSTORE_ENABLED=true,MEMORYSTORE_HOST=<instance-ip>,MEMORYSTORE_PORT=6379" \
  --region=us-central1
```

### 4. Configure VPC Connector (Required)

Memorystore requires VPC connectivity. Configure a VPC connector:

```bash
# Create VPC connector
gcloud compute networks vpc-access connectors create wistx-connector \
  --region=us-central1 \
  --network=default \
  --range=10.8.0.0/28

# Attach to Cloud Run service
gcloud run services update wistx-mcp \
  --vpc-connector=wistx-connector \
  --vpc-egress=all-traffic \
  --region=us-central1
```

## Rate Limit Configuration

Rate limits are configured in `wistx_mcp/tools/lib/constants.py`:

```python
MAX_RATE_LIMIT_CALLS = 100  # Maximum calls per window
RATE_LIMIT_WINDOW_SECONDS = 60  # Time window in seconds
```

This means: **100 calls per 60 seconds per user per tool**.

## Monitoring

### Check Redis Connection

The server logs connection status on startup:

```
INFO: Successfully connected to Redis/Memorystore for distributed rate limiting
```

If Redis is unavailable, it falls back to in-memory:

```
WARNING: Failed to connect to Redis/Memorystore: ... Falling back to in-memory rate limiting.
```

### Check Rate Limit Keys

You can inspect rate limit keys in Redis:

```bash
redis-cli -h <memorystore-ip> -p 6379

# List all rate limit keys
KEYS rate_limit:*

# Check specific user's rate limit
ZRANGE rate_limit:user123:tool_hash 0 -1 WITHSCORES

# Check count
ZCARD rate_limit:user123:tool_hash
```

## Performance Considerations

### Redis Operations

Each rate limit check performs:
1. `ZREMRANGEBYSCORE` - Remove old entries (O(log N + M))
2. `ZCARD` - Count current entries (O(1))
3. `ZADD` - Add new entry (O(log N))
4. `EXPIRE` - Set TTL (O(1))

**Total:** O(log N + M) where N = entries in set, M = entries removed

### Pipeline Optimization

We use Redis pipelines to batch operations and reduce round-trips:

```python
pipe = redis_client.pipeline()
pipe.zremrangebyscore(key, 0, window_start)
pipe.zcard(key)
pipe.zadd(key, {str(now): now})
pipe.expire(key, self.window_seconds + 10)
results = await pipe.execute()
```

### Memory Usage

Each rate limit entry uses minimal memory:
- Key: ~50 bytes (identifier)
- Value: ~8 bytes per timestamp entry
- TTL: Automatic cleanup after window expires

**Example:** 10,000 active users × 10 tools = 100,000 keys × ~100 bytes = ~10MB

## Error Handling

### Fail-Open Strategy

If Redis is unavailable, the rate limiter:
1. Logs a warning
2. **Allows the request** (fail-open)
3. Falls back to in-memory rate limiting if available

This ensures service availability even if Redis is down.

### Connection Retry

Redis client automatically retries on connection failures with exponential backoff.

## Security Considerations

### Network Security

- Memorystore instances are only accessible within your VPC
- Use VPC connectors for Cloud Run to Memorystore connectivity
- No public IP addresses required

### Authentication

Memorystore supports:
- AUTH password (if configured)
- IAM authentication (recommended for production)

### Data Isolation

Rate limit keys are namespaced:
```
rate_limit:{user_id}:{tool_hash}
```

This prevents key collisions and allows per-user/tool rate limiting.

## Troubleshooting

### Issue: Rate limits not enforced across instances

**Solution:** Ensure `MEMORYSTORE_ENABLED=true` and Memorystore is accessible.

### Issue: High latency on rate limit checks

**Solution:** 
- Check Memorystore instance size (upgrade if needed)
- Verify VPC connector is properly configured
- Monitor Redis connection pool

### Issue: Redis connection failures

**Solution:**
- Verify Memorystore instance is running
- Check VPC connector configuration
- Verify network connectivity from Cloud Run to Memorystore
- Check firewall rules

## Testing

### Test Distributed Rate Limiting Locally

1. Start local Redis:
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

2. Set environment variables:
```bash
export MEMORYSTORE_ENABLED=true
export MEMORYSTORE_HOST=localhost
export MEMORYSTORE_PORT=6379
```

3. Run MCP server:
```bash
python -m wistx_mcp.server
```

4. Verify Redis connection in logs:
```
INFO: Successfully connected to Redis/Memorystore for distributed rate limiting
```

## Migration Guide

### From In-Memory to Distributed

1. **No code changes required** - automatic detection
2. Set `MEMORYSTORE_ENABLED=true` and configure Memorystore
3. Deploy to Cloud Run
4. Verify logs show Redis connection

### Backward Compatibility

The implementation is fully backward compatible:
- If Redis is not configured → uses in-memory rate limiting
- If Redis fails → falls back to in-memory rate limiting
- Same API interface for both modes

## Best Practices

1. **Always use distributed rate limiting in production** (Cloud Run with multiple instances)
2. **Monitor Redis connection health** via Cloud Monitoring
3. **Set appropriate Memorystore instance size** based on expected load
4. **Use VPC connectors** for secure connectivity
5. **Enable Redis persistence** for production workloads
6. **Monitor rate limit hit rates** to adjust limits if needed

## References

- [Google Cloud Memorystore Documentation](https://cloud.google.com/memorystore/docs/redis)
- [Redis Sorted Sets Documentation](https://redis.io/docs/data-types/sorted-sets/)
- [Cloud Run VPC Connector](https://cloud.google.com/run/docs/configuring/connecting-vpc)




