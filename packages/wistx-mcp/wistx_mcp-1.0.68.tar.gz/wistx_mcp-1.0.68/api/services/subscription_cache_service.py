"""Subscription caching service with Redis fallback to MongoDB.

Uses Redis when available, falls back to MongoDB or in-memory cache.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional

from api.database.mongodb import mongodb_manager
from api.database.redis_client import get_redis_client

logger = logging.getLogger(__name__)


class SubscriptionCacheService:
    """Service for caching subscription data."""

    CACHE_TTL_SECONDS = 900
    CACHE_PREFIX = "subscription:"

    @staticmethod
    async def get_cached_subscription(user_id: str) -> Optional[dict]:
        """Get cached subscription data.

        Args:
            user_id: User ID

        Returns:
            Cached subscription data or None
        """
        cache_key = f"{SubscriptionCacheService.CACHE_PREFIX}{user_id}"

        redis_client = await get_redis_client()
        if redis_client:
            try:
                import json

                cached_data = await redis_client.get(cache_key)
                if cached_data:
                    return json.loads(cached_data)
            except Exception as e:
                logger.debug("Redis cache get failed, falling back to MongoDB: %s", e)

        db = mongodb_manager.get_database()
        cache_collection = db.subscription_cache

        cached = cache_collection.find_one({"cache_key": cache_key})

        if not cached:
            return None

        expires_at = cached.get("expires_at")
        if expires_at and expires_at < datetime.utcnow():
            cache_collection.delete_one({"cache_key": cache_key})
            return None

        return cached.get("data")

    @staticmethod
    async def set_cached_subscription(user_id: str, subscription_data: dict) -> None:
        """Cache subscription data.

        Args:
            user_id: User ID
            subscription_data: Subscription data to cache
        """
        cache_key = f"{SubscriptionCacheService.CACHE_PREFIX}{user_id}"
        expires_at = datetime.utcnow() + timedelta(
            seconds=SubscriptionCacheService.CACHE_TTL_SECONDS
        )

        redis_client = await get_redis_client()
        if redis_client:
            try:
                import json

                await redis_client.setex(
                    cache_key,
                    SubscriptionCacheService.CACHE_TTL_SECONDS,
                    json.dumps(subscription_data, default=str),
                )
                return
            except Exception as e:
                logger.debug("Redis cache set failed, falling back to MongoDB: %s", e)

        db = mongodb_manager.get_database()
        cache_collection = db.subscription_cache

        cache_collection.update_one(
            {"cache_key": cache_key},
            {
                "$set": {
                    "cache_key": cache_key,
                    "user_id": user_id,
                    "data": subscription_data,
                    "cached_at": datetime.utcnow(),
                    "expires_at": expires_at,
                }
            },
            upsert=True,
        )

    @staticmethod
    async def invalidate_cache(user_id: str) -> None:
        """Invalidate cached subscription data.

        Args:
            user_id: User ID
        """
        cache_key = f"{SubscriptionCacheService.CACHE_PREFIX}{user_id}"

        redis_client = await get_redis_client()
        if redis_client:
            try:
                await redis_client.delete(cache_key)
            except Exception as e:
                logger.debug("Redis cache delete failed: %s", e)

        db = mongodb_manager.get_database()
        cache_collection = db.subscription_cache

        cache_collection.delete_one({"cache_key": cache_key})

