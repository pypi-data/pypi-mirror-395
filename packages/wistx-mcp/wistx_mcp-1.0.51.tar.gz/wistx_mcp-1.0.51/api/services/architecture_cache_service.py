"""Architecture design cache service."""

import logging
from datetime import datetime
from typing import Any, Optional

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.models.architecture_cache import (
    ArchitectureDesignCache,
    generate_cache_key,
    get_cache_ttl,
)

logger = logging.getLogger(__name__)


class ArchitectureCacheService:
    """Service for managing architecture design cache."""

    def __init__(self):
        """Initialize architecture cache service."""
        self.collection_name = "architecture_design_cache"

    async def get_cached_design(
        self,
        cache_key: str,
        user_id: str,
    ) -> Optional[dict[str, Any]]:
        """Get cached architecture design.

        Args:
            cache_key: Cache key
            user_id: User ID

        Returns:
            Cached design result if found and not expired, None otherwise
        """
        db = mongodb_manager.get_database()
        collection = db[self.collection_name]

        try:
            cached_doc = collection.find_one({
                "_id": cache_key,
                "user_id": ObjectId(user_id),
            })

            if not cached_doc:
                return None

            cache_entry = ArchitectureDesignCache.from_dict(cached_doc)

            if cache_entry.is_expired():
                logger.info("Cache entry expired: %s", cache_key[:16])
                await self._delete_cache_entry(cache_key, user_id)
                return None

            cache_entry.record_hit()
            await self._update_cache_entry(cache_entry)

            logger.info(
                "Cache hit: key=%s, hits=%d",
                cache_key[:16],
                cache_entry.hit_count,
            )

            result = cache_entry.design_result.copy()
            result["cached"] = True
            result["cache_metadata"] = {
                "hit_count": cache_entry.hit_count,
                "created_at": cache_entry.created_at.isoformat(),
                "last_accessed_at": cache_entry.last_accessed_at.isoformat() if cache_entry.last_accessed_at else None,
            }
            return result

        except Exception as e:
            logger.warning("Error retrieving cache entry: %s", e, exc_info=True)
            return None

    async def cache_design(
        self,
        cache_key: str,
        user_id: str,
        organization_id: Optional[str],
        action: str,
        project_type: Optional[str],
        architecture_type: Optional[str],
        cloud_provider: Optional[str],
        compliance_standards: Optional[list[str]],
        requirements_hash: Optional[str],
        design_result: dict[str, Any],
        metadata: Optional[dict[str, Any]] = None,
    ) -> None:
        """Cache architecture design result.

        Args:
            cache_key: Cache key
            user_id: User ID
            organization_id: Organization ID
            action: Action type
            project_type: Project type
            architecture_type: Architecture pattern
            cloud_provider: Cloud provider
            compliance_standards: Compliance standards
            requirements_hash: Requirements hash
            design_result: Design result to cache
            metadata: Additional metadata
        """
        db = mongodb_manager.get_database()
        collection = db[self.collection_name]

        ttl = get_cache_ttl(action)
        expires_at = datetime.utcnow() + ttl

        cache_entry = ArchitectureDesignCache(
            cache_key=cache_key,
            user_id=user_id,
            organization_id=organization_id,
            action=action,
            project_type=project_type,
            architecture_type=architecture_type,
            cloud_provider=cloud_provider,
            compliance_standards=compliance_standards,
            requirements_hash=requirements_hash,
            design_result=design_result,
            metadata=metadata or {},
            expires_at=expires_at,
        )

        try:
            cache_dict = cache_entry.to_dict()
            collection.update_one(
                {"_id": cache_key},
                {"$set": cache_dict},
                upsert=True,
            )
            logger.info("Cached architecture design: key=%s, expires=%s", cache_key[:16], expires_at.isoformat())
        except Exception as e:
            logger.warning("Error caching design result: %s", e, exc_info=True)

    async def invalidate_cache(
        self,
        user_id: str,
        cache_key: Optional[str] = None,
        action: Optional[str] = None,
        project_type: Optional[str] = None,
    ) -> int:
        """Invalidate cache entries.

        Args:
            user_id: User ID
            cache_key: Specific cache key to invalidate (optional)
            action: Invalidate all entries for this action (optional)
            project_type: Invalidate all entries for this project type (optional)

        Returns:
            Number of entries invalidated
        """
        db = mongodb_manager.get_database()
        collection = db[self.collection_name]

        query: dict[str, Any] = {"user_id": ObjectId(user_id)}

        if cache_key:
            query["_id"] = cache_key
        elif action:
            query["action"] = action
            if project_type:
                query["project_type"] = project_type

        try:
            result = collection.delete_many(query)
            logger.info("Invalidated %d cache entries for user %s", result.deleted_count, user_id)
            return result.deleted_count
        except Exception as e:
            logger.warning("Error invalidating cache: %s", e, exc_info=True)
            return 0

    async def _update_cache_entry(self, cache_entry: ArchitectureDesignCache) -> None:
        """Update cache entry (for hit tracking).

        Args:
            cache_entry: Cache entry to update
        """
        db = mongodb_manager.get_database()
        collection = db[self.collection_name]

        try:
            collection.update_one(
                {"_id": cache_entry.cache_key},
                {
                    "$set": {
                        "hit_count": cache_entry.hit_count,
                        "last_accessed_at": cache_entry.last_accessed_at,
                    },
                },
            )
        except Exception as e:
            logger.warning("Error updating cache entry: %s", e, exc_info=True)

    async def _delete_cache_entry(self, cache_key: str, user_id: str) -> None:
        """Delete expired cache entry.

        Args:
            cache_key: Cache key
            user_id: User ID
        """
        db = mongodb_manager.get_database()
        collection = db[self.collection_name]

        try:
            collection.delete_one({
                "_id": cache_key,
                "user_id": ObjectId(user_id),
            })
        except Exception as e:
            logger.warning("Error deleting cache entry: %s", e, exc_info=True)

    async def cleanup_expired(self) -> int:
        """Clean up expired cache entries.

        Returns:
            Number of entries cleaned up
        """
        db = mongodb_manager.get_database()
        collection = db[self.collection_name]

        try:
            result = collection.delete_many({
                "expires_at": {"$lt": datetime.utcnow()},
            })
            logger.info("Cleaned up %d expired cache entries", result.deleted_count)
            return result.deleted_count
        except Exception as e:
            logger.warning("Error cleaning up expired cache: %s", e, exc_info=True)
            return 0


architecture_cache_service = ArchitectureCacheService()

