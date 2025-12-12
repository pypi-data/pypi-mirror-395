"""Organization quota service with caching for team-wide quota enforcement."""

import logging
from datetime import datetime, timedelta
from typing import Any

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.database.redis_client import get_redis_client
from api.services.exceptions import OrganizationQuotaExceededError, QuotaExceededError
from api.services.plan_service import plan_service
from api.services.usage_aggregator import usage_aggregator
from api.exceptions import NotFoundError

logger = logging.getLogger(__name__)

CACHE_TTL_SECONDS = 300
USAGE_CACHE_TTL_SECONDS = 300


class OrganizationQuotaService:
    """Service for enforcing organization-level quotas with caching."""

    def __init__(self):
        """Initialize organization quota service."""
        self._db = None
        self._redis_client = None

    @property
    def db(self):
        """Get database connection."""
        if self._db is None:
            mongodb_manager.connect()
            self._db = mongodb_manager.get_database()
        return self._db

    async def _get_redis_client(self):
        """Get Redis client for caching.

        Returns:
            Redis client or None if not configured
        """
        if self._redis_client is None:
            try:
                from api.database.redis_client import get_redis_client

                self._redis_client = await get_redis_client()
            except Exception as e:
                logger.debug("Redis not available for caching: %s", e)
                self._redis_client = None
        return self._redis_client

    def _get_cache_key(self, organization_id: str, metric: str, period: str) -> str:
        """Get Redis cache key for organization usage.

        Args:
            organization_id: Organization ID
            metric: Usage metric (queries, indexes, storage)
            period: Time period (month, day)

        Returns:
            Cache key string
        """
        now = datetime.utcnow()
        if period == "month":
            period_key = f"{now.year}-{now.month:02d}"
        else:
            period_key = now.date().isoformat()
        return f"org_usage:{organization_id}:{metric}:{period_key}"

    async def _get_cached_usage(
        self,
        organization_id: str,
        metric: str,
    ) -> int | float | None:
        """Get cached organization usage.

        Args:
            organization_id: Organization ID
            metric: Usage metric

        Returns:
            Cached usage value or None
        """
        redis_client = await self._get_redis_client()
        if not redis_client:
            return None

        try:
            cache_key = self._get_cache_key(organization_id, metric, "month")
            cached = await redis_client.get(cache_key)
            if cached:
                return float(cached) if "." in cached else int(cached)
        except Exception as e:
            logger.warning("Failed to get cached usage: %s", e)
        return None

    async def _set_cached_usage(
        self,
        organization_id: str,
        metric: str,
        value: int | float,
        ttl: int = USAGE_CACHE_TTL_SECONDS,
    ) -> None:
        """Cache organization usage.

        Args:
            organization_id: Organization ID
            metric: Usage metric
            value: Usage value
            ttl: Cache TTL in seconds (default: 5 minutes)
        """
        redis_client = await self._get_redis_client()
        if not redis_client:
            return

        try:
            cache_key = self._get_cache_key(organization_id, metric, "month")
            await redis_client.setex(cache_key, ttl, str(value))
        except Exception as e:
            logger.warning("Failed to cache usage: %s", e)

    async def _get_member_usage_breakdown(
        self,
        organization_id: str,
        metric: str,
    ) -> list[dict[str, Any]]:
        """Get per-member usage breakdown for quota exceeded errors.

        Args:
            organization_id: Organization ID
            metric: Usage metric

        Returns:
            List of member usage breakdowns
        """
        now = datetime.utcnow()
        start_of_month = datetime(now.year, now.month, 1)
        end_of_month = start_of_month + timedelta(days=32)
        end_of_month = end_of_month.replace(day=1) - timedelta(seconds=1)

        members = list(
            self.db.organization_members.find(
                {"organization_id": ObjectId(organization_id), "status": "active"},
                {"user_id": 1},
            )
        )

        if not members:
            return []

        member_breakdown = []
        for member in members:
            user_id = str(member["user_id"])
            user = self.db.users.find_one({"_id": member["user_id"]}, {"email": 1, "full_name": 1})

            user_usage = await usage_aggregator.aggregate_user_usage(
                user_id, start_of_month, end_of_month
            )

            if metric == "queries":
                usage_value = user_usage.get("total_queries", 0)
            elif metric == "indexes":
                usage_value = user_usage.get("total_indexes", 0)
            elif metric == "storage":
                usage_value = user_usage.get("total_storage_mb", 0.0)
            else:
                usage_value = 0

            member_breakdown.append(
                {
                    "user_id": user_id,
                    "email": user.get("email", "unknown") if user else "unknown",
                    "full_name": user.get("full_name") if user else None,
                    "usage": usage_value,
                }
            )

        return sorted(member_breakdown, key=lambda x: x["usage"], reverse=True)

    async def check_organization_query_quota(
        self,
        organization_id: str,
        plan_id: str,
    ) -> None:
        """Check organization query quota (team-wide) with caching.

        Args:
            organization_id: Organization ID
            plan_id: Plan ID

        Raises:
            OrganizationQuotaExceededError: If quota exceeded
        """
        plan_limits = plan_service.get_plan_limits(plan_id)
        if not plan_limits:
            raise NotFoundError(
                message=f"Plan {plan_id} not found",
                user_message=f"Plan {plan_id} not found",
                error_code="PLAN_NOT_FOUND",
                details={"plan_id": plan_id}
            )

        if plan_limits.queries_per_month == -1:
            return

        cached_queries = await self._get_cached_usage(organization_id, "queries")

        if cached_queries is not None:
            current_queries = int(cached_queries)
        else:
            now = datetime.utcnow()
            start_of_month = datetime(now.year, now.month, 1)
            end_of_month = start_of_month + timedelta(days=32)
            end_of_month = end_of_month.replace(day=1) - timedelta(seconds=1)

            usage = await usage_aggregator.aggregate_organization_usage(
                organization_id, start_of_month, end_of_month
            )
            current_queries = usage.get("total_queries", 0)

            await self._set_cached_usage(organization_id, "queries", current_queries)

        if current_queries >= plan_limits.queries_per_month:
            member_breakdown = await self._get_member_usage_breakdown(organization_id, "queries")
            raise OrganizationQuotaExceededError(
                message=f"Team quota exceeded: {current_queries}/{plan_limits.queries_per_month} queries used this month",
                limit_type="queries_per_month",
                current=current_queries,
                limit=plan_limits.queries_per_month,
                organization_id=organization_id,
                member_breakdown=member_breakdown,
            )

    async def check_organization_indexing_quota(
        self,
        organization_id: str,
        plan_id: str,
        estimated_storage_mb: float = 0.0,
    ) -> None:
        """Check organization indexing quota (team-wide) with caching.

        Args:
            organization_id: Organization ID
            plan_id: Plan ID
            estimated_storage_mb: Estimated storage for this operation

        Raises:
            OrganizationQuotaExceededError: If quota exceeded
        """
        plan_limits = plan_service.get_plan_limits(plan_id)
        if not plan_limits:
            raise NotFoundError(
                message=f"Plan {plan_id} not found",
                user_message=f"Plan {plan_id} not found",
                error_code="PLAN_NOT_FOUND",
                details={"plan_id": plan_id}
            )

        if plan_limits.indexes_per_month == -1 and plan_limits.storage_mb == -1:
            return

        now = datetime.utcnow()
        start_of_month = datetime(now.year, now.month, 1)
        end_of_month = start_of_month + timedelta(days=32)
        end_of_month = end_of_month.replace(day=1) - timedelta(seconds=1)

        cached_indexes = await self._get_cached_usage(organization_id, "indexes")
        cached_storage = await self._get_cached_usage(organization_id, "storage")

        if cached_indexes is not None and cached_storage is not None:
            current_indexes = int(cached_indexes)
            current_storage = float(cached_storage)
        else:
            usage = await usage_aggregator.aggregate_organization_usage(
                organization_id, start_of_month, end_of_month
            )
            current_indexes = usage.get("total_indexes", 0)
            current_storage = usage.get("total_storage_mb", 0.0)

            await self._set_cached_usage(organization_id, "indexes", current_indexes)
            await self._set_cached_usage(organization_id, "storage", current_storage)

        if plan_limits.indexes_per_month != -1 and current_indexes >= plan_limits.indexes_per_month:
            member_breakdown = await self._get_member_usage_breakdown(organization_id, "indexes")
            raise OrganizationQuotaExceededError(
                message=f"Team indexing quota exceeded: {current_indexes}/{plan_limits.indexes_per_month} indexes used this month",
                limit_type="indexes_per_month",
                current=current_indexes,
                limit=plan_limits.indexes_per_month,
                organization_id=organization_id,
                member_breakdown=member_breakdown,
            )

        if plan_limits.storage_mb != -1 and (current_storage + estimated_storage_mb) > plan_limits.storage_mb:
            member_breakdown = await self._get_member_usage_breakdown(organization_id, "storage")
            raise OrganizationQuotaExceededError(
                message=f"Team storage quota exceeded: {current_storage + estimated_storage_mb:.2f}/{plan_limits.storage_mb} MB used",
                limit_type="storage_mb",
                current=current_storage + estimated_storage_mb,
                limit=plan_limits.storage_mb,
                organization_id=organization_id,
                member_breakdown=member_breakdown,
            )

    async def get_organization_usage_summary(
        self,
        organization_id: str,
        start_date: datetime,
        end_date: datetime,
    ) -> dict[str, Any]:
        """Get aggregated usage for organization (with caching).

        Args:
            organization_id: Organization ID
            start_date: Start date
            end_date: End date

        Returns:
            Usage summary with per-member breakdown
        """
        usage = await usage_aggregator.aggregate_organization_usage(
            organization_id, start_date, end_date
        )

        members = list(
            self.db.organization_members.find(
                {"organization_id": ObjectId(organization_id), "status": "active"},
                {"user_id": 1},
            )
        )

        member_breakdown = []
        for member in members:
            user_id = str(member["user_id"])
            user = self.db.users.find_one({"_id": member["user_id"]}, {"email": 1, "full_name": 1})

            member_usage = await usage_aggregator.aggregate_user_usage(user_id, start_date, end_date)
            member_breakdown.append(
                {
                    "user_id": user_id,
                    "email": user.get("email", "unknown") if user else "unknown",
                    "full_name": user.get("full_name") if user else None,
                    "queries": member_usage.get("total_queries", 0),
                    "indexes": member_usage.get("total_indexes", 0),
                    "storage_mb": member_usage.get("total_storage_mb", 0.0),
                }
            )

        return {
            **usage,
            "member_breakdown": member_breakdown,
        }

    async def invalidate_cache(self, organization_id: str) -> None:
        """Invalidate cached usage for organization.

        Args:
            organization_id: Organization ID
        """
        redis_client = await self._get_redis_client()
        if not redis_client:
            return

        try:
            now = datetime.utcnow()
            period_key = f"{now.year}-{now.month:02d}"
            keys = [
                f"org_usage:{organization_id}:queries:{period_key}",
                f"org_usage:{organization_id}:indexes:{period_key}",
                f"org_usage:{organization_id}:storage:{period_key}",
            ]

            for key in keys:
                await redis_client.delete(key)
        except Exception as e:
            logger.warning("Failed to invalidate cache: %s", e)

    async def update_cache_after_usage(
        self,
        organization_id: str,
        metric: str,
        increment: int | float = 1,
    ) -> None:
        """Update cache after usage is tracked.

        Args:
            organization_id: Organization ID
            metric: Usage metric (queries, indexes, storage)
            increment: Amount to increment (default: 1)
        """
        redis_client = await self._get_redis_client()
        if not redis_client:
            return

        try:
            cache_key = self._get_cache_key(organization_id, metric, "month")
            await redis_client.incrbyfloat(cache_key, float(increment))
            await redis_client.expire(cache_key, USAGE_CACHE_TTL_SECONDS)
        except Exception as e:
            logger.warning("Failed to update cache: %s", e)


organization_quota_service = OrganizationQuotaService()

