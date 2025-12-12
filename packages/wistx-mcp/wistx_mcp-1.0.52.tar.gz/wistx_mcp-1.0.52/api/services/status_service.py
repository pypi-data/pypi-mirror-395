"""Status service for comprehensive health checks."""

import time
import logging
from typing import Any
from datetime import datetime

from api.config import settings
from api.database.mongodb import mongodb_manager
from api.database.redis_client import get_redis_manager

logger = logging.getLogger(__name__)


class StatusService:
    """Service for checking status of all WISTX components."""

    def __init__(self):
        """Initialize status service."""
        self._start_time = time.time()

    async def check_all_services(self) -> dict[str, Any]:
        """Check status of all services.

        Returns:
            Dictionary with status of all services
        """
        start_time = time.time()

        services_status = {
            "api": await self._check_api(),
            "database": await self._check_database(),
            "redis": await self._check_redis(),
            "vector_search": await self._check_vector_search(),
            "indexing": await self._check_indexing(),
            "authentication": await self._check_authentication(),
        }

        overall_status = self._determine_overall_status(services_status)
        check_duration_ms = (time.time() - start_time) * 1000

        return {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "check_duration_ms": round(check_duration_ms, 2),
            "services": services_status,
        }

    async def _check_api(self) -> dict[str, Any]:
        """Check API service status.

        Returns:
            API service status
        """
        try:
            return {
                "status": "operational",
                "version": settings.api_version,
                "title": settings.api_title,
                "uptime_seconds": int(time.time() - self._start_time),
            }
        except Exception as e:
            logger.error("API health check failed: %s", e, exc_info=True)
            return {
                "status": "degraded",
                "error": str(e),
            }

    async def _check_database(self) -> dict[str, Any]:
        """Check database service status.

        Returns:
            Database service status
        """
        try:
            db_health = mongodb_manager.health_check()
            return {
                "status": "operational" if db_health.get("status") == "healthy" else "degraded",
                "latency_ms": db_health.get("latency_ms"),
                "connections": db_health.get("connections", {}),
                "server_version": db_health.get("server", {}).get("version", "unknown"),
            }
        except Exception as e:
            logger.error("Database health check failed: %s", e, exc_info=True)
            return {
                "status": "down",
                "error": str(e),
            }

    async def _check_redis(self) -> dict[str, Any]:
        """Check Redis/Memorystore service status.

        Returns:
            Redis service status
        """
        redis_manager = await get_redis_manager()
        if not redis_manager:
            return {
                "status": "not_configured",
                "message": "Redis/Memorystore not configured",
            }

        try:
            health_status = redis_manager.get_health_status()
            metrics = health_status.get("metrics", {})

            if health_status.get("healthy"):
                return {
                    "status": "operational",
                    "circuit_state": health_status.get("circuit_state"),
                    "last_health_check": health_status.get("last_health_check"),
                    "metrics": {
                        "total_operations": metrics.get("total_operations", 0),
                        "successful_operations": metrics.get("successful_operations", 0),
                        "failed_operations": metrics.get("failed_operations", 0),
                        "health_checks": metrics.get("health_checks", 0),
                    },
                }
            else:
                return {
                    "status": "degraded" if health_status.get("circuit_state") != "open" else "down",
                    "circuit_state": health_status.get("circuit_state"),
                    "failure_count": health_status.get("failure_count", 0),
                    "last_failure_time": health_status.get("last_failure_time"),
                    "last_health_check": health_status.get("last_health_check"),
                }
        except Exception as e:
            logger.error("Redis health check failed: %s", e, exc_info=True)
            return {
                "status": "down",
                "error": str(e),
            }

    async def _check_vector_search(self) -> dict[str, Any]:
        """Check vector search (Pinecone) service status.

        Returns:
            Vector search service status
        """
        if not settings.pinecone_api_key:
            return {
                "status": "not_configured",
                "message": "Pinecone API key not configured",
            }

        try:
            from pinecone import Pinecone
            from pinecone.exceptions import NotFoundException

            pc = Pinecone(api_key=settings.pinecone_api_key)
            index = pc.Index(settings.pinecone_index_name)
            stats = index.describe_index_stats()

            return {
                "status": "operational",
                "index_name": settings.pinecone_index_name,
                "total_vectors": stats.get("total_vector_count", 0),
                "indexes": stats.get("indexes", {}),
            }
        except NotFoundException:
            return {
                "status": "degraded",
                "error": f"Index '{settings.pinecone_index_name}' not found",
            }
        except Exception as e:
            logger.error("Vector search health check failed: %s", e, exc_info=True)
            return {
                "status": "down",
                "error": str(e),
            }

    async def _check_indexing(self) -> dict[str, Any]:
        """Check indexing service status.

        Returns:
            Indexing service status
        """
        try:
            db = mongodb_manager.get_database()
            indexing_collection = db["indexed_resources"]

            recent_jobs = indexing_collection.count_documents(
                {"created_at": {"$gte": datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)}}
            )

            active_jobs = indexing_collection.count_documents({"status": {"$in": ["indexing", "pending"]}})

            return {
                "status": "operational",
                "recent_jobs_today": recent_jobs,
                "active_jobs": active_jobs,
            }
        except Exception as e:
            logger.error("Indexing service health check failed: %s", e, exc_info=True)
            return {
                "status": "degraded",
                "error": str(e),
            }

    async def _check_authentication(self) -> dict[str, Any]:
        """Check authentication service status.

        Returns:
            Authentication service status
        """
        try:
            db = mongodb_manager.get_database()
            users_collection = db["users"]

            total_users = users_collection.count_documents({})
            active_users = users_collection.count_documents({"is_active": True})

            return {
                "status": "operational",
                "total_users": total_users,
                "active_users": active_users,
            }
        except Exception as e:
            logger.error("Authentication service health check failed: %s", e, exc_info=True)
            return {
                "status": "degraded",
                "error": str(e),
            }

    def _determine_overall_status(self, services_status: dict[str, Any]) -> str:
        """Determine overall status from individual service statuses.

        Args:
            services_status: Dictionary of service statuses

        Returns:
            Overall status (operational, degraded, down)
        """
        statuses = [service.get("status") for service in services_status.values()]

        if "down" in statuses:
            return "down"
        if any(status in ["degraded", "not_configured"] for status in statuses):
            return "degraded"
        return "operational"

    async def get_uptime_stats(self, days: int = 30) -> dict[str, Any]:
        """Get uptime statistics for services.

        Args:
            days: Number of days to calculate uptime for

        Returns:
            Uptime statistics

        Note:
            Historical uptime statistics require periodic status checks to be stored
            in the 'service_status' collection. If no historical data exists, this
            will return an error indicating that historical data collection is needed.
        """
        try:
            db = mongodb_manager.get_database()
            status_collection = db.get_collection("service_status")

            from datetime import timedelta

            cutoff_date = datetime.utcnow() - timedelta(days=days)

            total_checks = status_collection.count_documents({"timestamp": {"$gte": cutoff_date}})
            
            if total_checks == 0:
                return {
                    "period_days": days,
                    "total_checks": 0,
                    "operational_checks": 0,
                    "uptime_percentage": 0.0,
                    "message": "No historical status data available. Historical uptime statistics require periodic status checks to be stored.",
                }

            operational_checks = status_collection.count_documents(
                {"timestamp": {"$gte": cutoff_date}, "status": "operational"}
            )

            uptime_percentage = (operational_checks / total_checks * 100) if total_checks > 0 else 100.0

            return {
                "period_days": days,
                "total_checks": total_checks,
                "operational_checks": operational_checks,
                "uptime_percentage": round(uptime_percentage, 2),
            }
        except Exception as e:
            logger.error("Failed to get uptime stats: %s", e, exc_info=True)
            return {
                "period_days": days,
                "total_checks": 0,
                "operational_checks": 0,
                "uptime_percentage": 0.0,
                "error": str(e),
                "message": "Failed to retrieve uptime statistics. Historical data collection may not be configured.",
            }


status_service = StatusService()

