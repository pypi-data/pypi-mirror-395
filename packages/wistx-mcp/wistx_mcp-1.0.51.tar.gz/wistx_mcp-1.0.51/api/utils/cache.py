"""Caching service using Google Memorystore (Redis-compatible)."""

import hashlib
import json
import logging
from typing import Any, Callable, TypeVar

from api.config import settings
from api.database.redis_client import get_redis_manager, RedisCircuitBreakerOpenError

logger = logging.getLogger(__name__)

T = TypeVar("T")


def _make_cache_key(prefix: str, *args: Any, **kwargs: Any) -> str:
    """Generate cache key from arguments.

    Args:
        prefix: Cache key prefix
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        Cache key string
    """
    key_parts = [prefix]

    if args:
        key_parts.extend(str(arg) for arg in args)

    if kwargs:
        sorted_kwargs = sorted(kwargs.items())
        key_parts.extend(f"{k}={v}" for k, v in sorted_kwargs)

    key_string = ":".join(key_parts)
    key_hash = hashlib.sha256(key_string.encode()).hexdigest()[:16]

    return f"{prefix}:{key_hash}"


async def get_cached(
    key_prefix: str,
    ttl_seconds: int = 3600,
    *args: Any,
    **kwargs: Any,
) -> Any | None:
    """Get value from cache.

    Args:
        key_prefix: Cache key prefix
        ttl_seconds: Time-to-live in seconds
        *args: Positional arguments for key generation
        **kwargs: Keyword arguments for key generation

    Returns:
        Cached value or None if not found
    """
    redis_manager = await get_redis_manager()
    if not redis_manager:
        return None

    try:
        cache_key = _make_cache_key(key_prefix, *args, **kwargs)

        async def _get_value(client: Any) -> Any | None:
            cached_value = await client.get(cache_key)
            if cached_value:
                return json.loads(cached_value)
            return None

        return await redis_manager.execute(_get_value)
    except RedisCircuitBreakerOpenError:
        logger.debug("Redis circuit breaker open, cache get skipped")
        return None
    except Exception as e:
        logger.debug("Cache get failed: %s", e)
        return None


async def set_cached(
    key_prefix: str,
    value: Any,
    ttl_seconds: int = 3600,
    *args: Any,
    **kwargs: Any,
) -> bool:
    """Set value in cache.

    Args:
        key_prefix: Cache key prefix
        value: Value to cache (must be JSON-serializable)
        ttl_seconds: Time-to-live in seconds
        *args: Positional arguments for key generation
        **kwargs: Keyword arguments for key generation

    Returns:
        True if cached successfully, False otherwise
    """
    redis_manager = await get_redis_manager()
    if not redis_manager:
        return False

    try:
        cache_key = _make_cache_key(key_prefix, *args, **kwargs)
        serialized_value = json.dumps(value)

        async def _set_value(client: Any) -> bool:
            await client.setex(cache_key, ttl_seconds, serialized_value)
            return True

        await redis_manager.execute(_set_value)
        return True
    except RedisCircuitBreakerOpenError:
        logger.debug("Redis circuit breaker open, cache set skipped")
        return False
    except Exception as e:
        logger.debug("Cache set failed: %s", e)
        return False


async def delete_cached(
    key_prefix: str,
    *args: Any,
    **kwargs: Any,
) -> bool:
    """Delete value from cache.

    Args:
        key_prefix: Cache key prefix
        *args: Positional arguments for key generation
        **kwargs: Keyword arguments for key generation

    Returns:
        True if deleted successfully, False otherwise
    """
    redis_manager = await get_redis_manager()
    if not redis_manager:
        return False

    try:
        cache_key = _make_cache_key(key_prefix, *args, **kwargs)

        async def _delete_value(client: Any) -> bool:
            await client.delete(cache_key)
            return True

        await redis_manager.execute(_delete_value)
        return True
    except RedisCircuitBreakerOpenError:
        logger.debug("Redis circuit breaker open, cache delete skipped")
        return False
    except Exception as e:
        logger.debug("Cache delete failed: %s", e)
        return False


def cached(
    key_prefix: str,
    ttl_seconds: int = 3600,
    key_func: Callable[..., tuple[Any, ...]] | None = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to cache function results.

    Args:
        key_prefix: Cache key prefix
        ttl_seconds: Time-to-live in seconds
        key_func: Optional function to extract cache key from arguments

    Returns:
        Decorator function
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            if key_func:
                cache_key_args = key_func(*args, **kwargs)
            else:
                cache_key_args = (args, kwargs)

            cached_value = await get_cached(key_prefix, ttl_seconds, *cache_key_args)
            if cached_value is not None:
                return cached_value

            result = await func(*args, **kwargs)

            await set_cached(key_prefix, result, ttl_seconds, *cache_key_args)

            return result

        return wrapper

    return decorator

