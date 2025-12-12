"""Admin system service."""

import logging
import time
from datetime import date, datetime
from typing import Any

from api.database.mongodb import mongodb_manager
from api.models.admin.system import (
    RateLimitConfig,
    RateLimitConfigResponse,
    SystemHealthResponse,
    SystemStatsResponse,
)
from api.services.plan_service import plan_service
from api.services.status_service import status_service

logger = logging.getLogger(__name__)

_start_time = time.time()


def _sanitize_for_json(obj: Any) -> Any:
    """Recursively convert date/datetime objects to strings for JSON serialization.

    Args:
        obj: Object to sanitize

    Returns:
        Sanitized object
    """
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {key: _sanitize_for_json(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [_sanitize_for_json(item) for item in obj]
    return obj


class AdminSystemService:
    """Service for admin system operations."""

    async def get_system_health(self) -> SystemHealthResponse:
        """Get system health status.

        Returns:
            System health response
        """
        try:
            status_data = await status_service.check_all_services()
            uptime_seconds = time.time() - _start_time

            services = status_data.get("services", {})

            return SystemHealthResponse(
                status=status_data.get("status", "unknown"),
                api=_sanitize_for_json(services.get("api", {})),
                database=_sanitize_for_json(services.get("database", {})),
                redis=_sanitize_for_json(services.get("redis", {})),
                vector_search=_sanitize_for_json(services.get("vector_search", {})),
                uptime_seconds=uptime_seconds,
            )
        except Exception as e:
            logger.error("Error getting system health: %s", e, exc_info=True)
            return SystemHealthResponse(
                status="unknown",
                api={},
                database={},
                redis={},
                vector_search={},
                uptime_seconds=None,
            )

    async def get_rate_limits(self) -> RateLimitConfigResponse:
        """Get rate limit configuration for all plans.

        Returns:
            Rate limit configuration response
        """
        plans = plan_service.list_plans()
        rate_limit_configs = []

        for plan in plans:
            limits = plan.limits
            rate_limit_configs.append(
                RateLimitConfig(
                    plan=plan.plan_id,
                    requests_per_minute=limits.requests_per_minute,
                )
            )

        return RateLimitConfigResponse(plans=rate_limit_configs)

    async def get_system_stats(self) -> SystemStatsResponse:
        """Get system statistics.

        Returns:
            System statistics response
        """
        db = mongodb_manager.get_database()

        total_users = db.users.count_documents({})
        total_api_keys = db.api_keys.count_documents({})
        active_api_keys = db.api_keys.count_documents({"is_active": True})

        total_organizations = len(db.users.distinct("organization_id"))
        total_indexed_resources = db.indexed_resources.count_documents({})

        storage_pipeline = [
            {"$group": {"_id": None, "total": {"$sum": "$storage_mb"}}},
        ]
        storage_result = list(db.indexed_resources.aggregate(storage_pipeline))
        total_storage_mb = storage_result[0]["total"] if storage_result else 0.0

        try:
            db_stats = db.command("dbStats")
            database_size_mb = db_stats.get("dataSize", 0) / (1024 * 1024)
        except Exception:
            database_size_mb = None

        collections_count = len(db.list_collection_names())

        return SystemStatsResponse(
            total_users=total_users,
            total_api_keys=total_api_keys,
            active_api_keys=active_api_keys,
            total_organizations=total_organizations,
            total_indexed_resources=total_indexed_resources,
            total_storage_mb=round(total_storage_mb, 2),
            database_size_mb=round(database_size_mb, 2) if database_size_mb else None,
            collections_count=collections_count,
        )


admin_system_service = AdminSystemService()

