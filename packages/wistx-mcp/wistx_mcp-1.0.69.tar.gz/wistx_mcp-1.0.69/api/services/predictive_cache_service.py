"""Predictive cache service for infrastructure-aware caching."""

import logging
import secrets
from datetime import datetime, timedelta
from typing import Any, Optional

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.models.predictive_cache import (
    CacheEntry,
    CacheEntryType,
    CacheStatus,
    DependencyEntry,
    DependencyType,
    UsagePattern,
)

logger = logging.getLogger(__name__)


def generate_cache_id() -> str:
    """Generate unique cache ID.

    Returns:
        Unique cache ID (e.g., 'cache_abc123')
    """
    random_part = secrets.token_urlsafe(8)[:8]
    return f"cache_{random_part}"


def generate_dependency_id() -> str:
    """Generate unique dependency ID.

    Returns:
        Unique dependency ID (e.g., 'dep_abc123')
    """
    random_part = secrets.token_urlsafe(8)[:8]
    return f"dep_{random_part}"


def generate_pattern_id() -> str:
    """Generate unique pattern ID.

    Returns:
        Unique pattern ID (e.g., 'pattern_abc123')
    """
    random_part = secrets.token_urlsafe(8)[:8]
    return f"pattern_{random_part}"


class PredictiveCacheService:
    """Service for predictive caching with infrastructure awareness."""

    def __init__(self):
        """Initialize predictive cache service."""
        self._db = None
        self.default_ttl_hours = 24

    def _get_db(self):
        """Get MongoDB database instance."""
        if self._db is None:
            self._db = mongodb_manager.get_database()
        return self._db

    async def get_cache(
        self,
        user_id: str,
        resource_id: str,
        key: str,
        entry_type: CacheEntryType,
    ) -> Optional[dict[str, Any]]:
        """Get cached value.

        Args:
            user_id: User ID
            resource_id: Resource ID
            key: Cache key
            entry_type: Entry type

        Returns:
            Cached value if found and valid, None otherwise
        """
        db = self._get_db()
        collection = db.cache_entries

        query = {
            "user_id": ObjectId(user_id),
            "resource_id": resource_id,
            "key": key,
            "entry_type": entry_type.value,
            "status": CacheStatus.ACTIVE.value,
        }

        doc = collection.find_one(query)
        if not doc:
            return None

        entry = CacheEntry.from_dict(doc)

        if entry.expires_at and entry.expires_at < datetime.utcnow():
            await self._invalidate_cache(entry.cache_id)
            return None

        collection.update_one(
            {"_id": entry.cache_id},
            {
                "$set": {
                    "last_accessed_at": datetime.utcnow(),
                },
                "$inc": {"access_count": 1},
            },
        )

        return entry.value

    async def set_cache(
        self,
        user_id: str,
        resource_id: str,
        key: str,
        value: dict[str, Any],
        entry_type: CacheEntryType,
        ttl_hours: Optional[int] = None,
        dependencies: Optional[list[str]] = None,
    ) -> CacheEntry:
        """Set cached value.

        Args:
            user_id: User ID
            resource_id: Resource ID
            key: Cache key
            value: Value to cache
            entry_type: Entry type
            ttl_hours: Time to live in hours
            dependencies: List of dependency keys

        Returns:
            Created CacheEntry
        """
        cache_id = generate_cache_id()
        expires_at = None
        if ttl_hours:
            expires_at = datetime.utcnow() + timedelta(hours=ttl_hours)
        elif self.default_ttl_hours:
            expires_at = datetime.utcnow() + timedelta(hours=self.default_ttl_hours)

        entry = CacheEntry(
            cache_id=cache_id,
            user_id=user_id,
            resource_id=resource_id,
            entry_type=entry_type,
            key=key,
            value=value,
            dependencies=dependencies or [],
            expires_at=expires_at,
        )

        db = self._get_db()
        collection = db.cache_entries
        entry_dict = entry.to_dict()
        collection.replace_one(
            {
                "user_id": ObjectId(user_id),
                "resource_id": resource_id,
                "key": key,
                "entry_type": entry_type.value,
            },
            entry_dict,
            upsert=True,
        )

        logger.info(
            "Cached entry: cache_id=%s, resource_id=%s, key=%s",
            cache_id,
            resource_id,
            key,
        )

        return entry

    async def predict_and_prefetch(
        self,
        user_id: str,
        resource_id: str,
        path: str,
        access_type: str,
    ) -> list[str]:
        """Predict likely next accesses and pre-cache.

        Args:
            user_id: User ID
            resource_id: Resource ID
            path: Current file path
            access_type: Access type (read, search, list)

        Returns:
            List of predicted paths that were pre-cached
        """
        dependencies = await self._analyze_dependencies(resource_id, path)
        usage_patterns = await self._get_usage_patterns(user_id, resource_id, path, access_type)

        predictions = []
        predictions.extend(dependencies.get("direct", [])[:5])
        predictions.extend(usage_patterns.get("next_accesses", [])[:5])

        prefetched = []
        for predicted_path in predictions[:10]:
            try:
                await self._prefetch_path(user_id, resource_id, predicted_path)
                prefetched.append(predicted_path)
            except Exception as e:
                logger.debug("Failed to prefetch %s: %s", predicted_path, e)

        return prefetched

    async def _analyze_dependencies(
        self, resource_id: str, path: str
    ) -> dict[str, list[str]]:
        """Analyze infrastructure dependencies.

        Args:
            resource_id: Resource ID
            path: File path

        Returns:
            Dictionary with direct, transitive, and reverse dependencies
        """
        db = self._get_db()
        dependencies_collection = db.dependencies

        direct = []
        transitive = []
        reverse = []

        source_deps = dependencies_collection.find({
            "resource_id": resource_id,
            "source_path": path,
            "dependency_type": {"$in": [DependencyType.DIRECT.value, DependencyType.RELATED.value]},
        })

        for dep_doc in source_deps:
            dep = DependencyEntry.from_dict(dep_doc)
            direct.append(dep.target_path)

        target_deps = dependencies_collection.find({
            "resource_id": resource_id,
            "target_path": path,
            "dependency_type": DependencyType.REVERSE.value,
        })

        for dep_doc in target_deps:
            dep = DependencyEntry.from_dict(dep_doc)
            reverse.append(dep.source_path)

        return {
            "direct": direct,
            "transitive": transitive,
            "reverse": reverse,
        }

    async def _get_usage_patterns(
        self, user_id: str, resource_id: str, path: str, access_type: str
    ) -> dict[str, Any]:
        """Get usage patterns for a file.

        Args:
            user_id: User ID
            resource_id: Resource ID
            path: File path
            access_type: Access type

        Returns:
            Dictionary with usage patterns
        """
        db = self._get_db()
        collection = db.usage_patterns

        doc = collection.find_one({
            "user_id": ObjectId(user_id),
            "resource_id": resource_id,
            "path": path,
            "access_type": access_type,
        })

        if not doc:
            return {"next_accesses": []}

        pattern = UsagePattern.from_dict(doc)
        return {
            "next_accesses": pattern.next_accesses,
            "time_patterns": pattern.time_patterns,
            "user_patterns": pattern.user_patterns,
        }

    async def _prefetch_path(
        self, user_id: str, resource_id: str, path: str
    ) -> None:
        """Prefetch a file path.

        Args:
            user_id: User ID
            resource_id: Resource ID
            path: File path to prefetch
        """
        from api.services.virtual_filesystem_service import virtual_filesystem_service

        try:
            entry = await virtual_filesystem_service.get_entry(
                resource_id=resource_id,
                path=path,
                user_id=user_id,
            )

            if entry:
                await self.set_cache(
                    user_id=user_id,
                    resource_id=resource_id,
                    key=path,
                    value={"path": path, "entry_id": entry.entry_id},
                    entry_type=CacheEntryType.FILE_CONTENT,
                    ttl_hours=1,
                )
        except Exception as e:
            logger.debug("Failed to prefetch path %s: %s", path, e)

    async def track_access(
        self,
        user_id: str,
        resource_id: str,
        path: str,
        access_type: str,
        next_path: Optional[str] = None,
    ) -> None:
        """Track file access pattern.

        Args:
            user_id: User ID
            resource_id: Resource ID
            path: File path accessed
            access_type: Access type (read, search, list)
            next_path: Next path accessed (if known)
        """
        db = self._get_db()
        collection = db.usage_patterns

        query = {
            "user_id": ObjectId(user_id),
            "resource_id": resource_id,
            "path": path,
            "access_type": access_type,
        }

        doc = collection.find_one(query)

        if doc:
            pattern = UsagePattern.from_dict(doc)
            pattern.access_count += 1
            pattern.last_accessed_at = datetime.utcnow()
            pattern.updated_at = datetime.utcnow()

            if next_path:
                next_accesses = {item["path"]: item for item in pattern.next_accesses}
                if next_path in next_accesses:
                    next_accesses[next_path]["count"] += 1
                else:
                    next_accesses[next_path] = {"path": next_path, "count": 1}
                pattern.next_accesses = list(next_accesses.values())
                pattern.next_accesses.sort(key=lambda x: x["count"], reverse=True)
                pattern.next_accesses = pattern.next_accesses[:10]

            collection.replace_one(query, pattern.to_dict())
        else:
            pattern_id = generate_pattern_id()
            next_accesses = []
            if next_path:
                next_accesses = [{"path": next_path, "count": 1}]

            pattern = UsagePattern(
                pattern_id=pattern_id,
                user_id=user_id,
                resource_id=resource_id,
                path=path,
                access_type=access_type,
                next_accesses=next_accesses,
                access_count=1,
            )

            collection.insert_one(pattern.to_dict())

    async def record_dependency(
        self,
        resource_id: str,
        source_path: str,
        target_path: str,
        dependency_type: DependencyType,
        strength: float = 1.0,
        metadata: Optional[dict[str, Any]] = None,
    ) -> DependencyEntry:
        """Record a dependency relationship.

        Args:
            resource_id: Resource ID
            source_path: Source file path
            target_path: Target file path
            dependency_type: Dependency type
            strength: Dependency strength (0.0-1.0)
            metadata: Additional metadata

        Returns:
            Created DependencyEntry
        """
        dependency_id = generate_dependency_id()

        entry = DependencyEntry(
            dependency_id=dependency_id,
            resource_id=resource_id,
            source_path=source_path,
            target_path=target_path,
            dependency_type=dependency_type,
            strength=strength,
            metadata=metadata or {},
        )

        db = self._get_db()
        collection = db.dependencies
        entry_dict = entry.to_dict()
        collection.replace_one(
            {
                "resource_id": resource_id,
                "source_path": source_path,
                "target_path": target_path,
            },
            entry_dict,
            upsert=True,
        )

        logger.info(
            "Recorded dependency: resource_id=%s, source=%s, target=%s, type=%s",
            resource_id,
            source_path,
            target_path,
            dependency_type.value,
        )

        return entry

    async def invalidate_cache(
        self,
        user_id: str,
        resource_id: Optional[str] = None,
        key: Optional[str] = None,
        entry_type: Optional[CacheEntryType] = None,
    ) -> int:
        """Invalidate cache entries.

        Args:
            user_id: User ID
            resource_id: Resource ID (optional, invalidates all for resource)
            key: Cache key (optional, invalidates specific key)
            entry_type: Entry type (optional, invalidates all of type)

        Returns:
            Number of entries invalidated
        """
        db = self._get_db()
        collection = db.cache_entries

        query: dict[str, Any] = {
            "user_id": ObjectId(user_id),
            "status": CacheStatus.ACTIVE.value,
        }

        if resource_id:
            query["resource_id"] = resource_id
        if key:
            query["key"] = key
        if entry_type:
            query["entry_type"] = entry_type.value

        result = collection.update_many(
            query,
            {
                "$set": {
                    "status": CacheStatus.INVALIDATED.value,
                    "expires_at": datetime.utcnow(),
                }
            },
        )

        logger.info(
            "Invalidated %d cache entries: user_id=%s, resource_id=%s, key=%s",
            result.modified_count,
            user_id,
            resource_id,
            key,
        )

        return result.modified_count

    async def _invalidate_cache(self, cache_id: str) -> None:
        """Invalidate a specific cache entry.

        Args:
            cache_id: Cache ID
        """
        db = self._get_db()
        collection = db.cache_entries

        collection.update_one(
            {"_id": cache_id},
            {
                "$set": {
                    "status": CacheStatus.INVALIDATED.value,
                    "expires_at": datetime.utcnow(),
                }
            },
        )

    async def get_cache_status(
        self,
        user_id: str,
        resource_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get cache status.

        Args:
            user_id: User ID
            resource_id: Resource ID (optional)

        Returns:
            Dictionary with cache statistics
        """
        db = self._get_db()
        collection = db.cache_entries

        query: dict[str, Any] = {"user_id": ObjectId(user_id)}
        if resource_id:
            query["resource_id"] = resource_id

        total = collection.count_documents(query)
        active = collection.count_documents({**query, "status": CacheStatus.ACTIVE.value})
        expired = collection.count_documents({**query, "status": CacheStatus.EXPIRED.value})
        invalidated = collection.count_documents({**query, "status": CacheStatus.INVALIDATED.value})

        return {
            "total": total,
            "active": active,
            "expired": expired,
            "invalidated": invalidated,
        }


predictive_cache_service = PredictiveCacheService()

