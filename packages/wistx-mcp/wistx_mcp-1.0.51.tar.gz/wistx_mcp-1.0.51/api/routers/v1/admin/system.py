"""Admin system operations endpoints."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies.auth import require_admin, require_permission_factory
from api.models.admin.system import (
    RateLimitConfigResponse,
    RedisMetricsResponse,
    SystemHealthResponse,
    SystemStatsResponse,
)
from api.services.admin.system_service import admin_system_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/system", tags=["admin"])


@router.get("/health", response_model=SystemHealthResponse, summary="Get system health")
async def get_system_health(
    current_user: dict[str, Any] = Depends(require_permission_factory("system.view")),
) -> SystemHealthResponse:
    """Get system health status.

    Args:
        current_user: Current admin user

    Returns:
        System health response
    """
    try:
        return await admin_system_service.get_system_health()
    except Exception as e:
        logger.error("Error getting system health: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get system health",
        ) from e


@router.get("/rate-limits", response_model=RateLimitConfigResponse, summary="Get rate limit configuration")
async def get_rate_limits(
    current_user: dict[str, Any] = Depends(require_permission_factory("system.view")),
) -> RateLimitConfigResponse:
    """Get rate limit configuration for all plans.

    Args:
        current_user: Current admin user

    Returns:
        Rate limit configuration response
    """
    try:
        return await admin_system_service.get_rate_limits()
    except Exception as e:
        logger.error("Error getting rate limits: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get rate limits",
        ) from e


@router.get("/stats", response_model=SystemStatsResponse, summary="Get system statistics")
async def get_system_stats(
    current_user: dict[str, Any] = Depends(require_permission_factory("system.view")),
) -> SystemStatsResponse:
    """Get system statistics.

    Args:
        current_user: Current admin user

    Returns:
        System statistics response
    """
    try:
        return await admin_system_service.get_system_stats()
    except Exception as e:
        logger.error("Error getting system stats: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get system stats",
        ) from e


@router.get("/redis/metrics", response_model=RedisMetricsResponse, summary="Get Redis metrics")
async def get_redis_metrics(
    current_user: dict[str, Any] = Depends(require_permission_factory("system.view")),
) -> RedisMetricsResponse:
    """Get detailed Redis/Memorystore metrics and statistics.

    Args:
        current_user: Current admin user

    Returns:
        Redis metrics response with circuit breaker state, operation metrics, and configuration

    Example response:
        {
            "healthy": true,
            "circuit_state": "closed",
            "failure_count": 0,
            "success_count": 0,
            "last_failure_time": null,
            "last_health_check": 1704067200.0,
            "client_initialized": true,
            "metrics": {
                "total_operations": 1234,
                "successful_operations": 1230,
                "failed_operations": 4,
                "circuit_breaker_opens": 0,
                "retries": 8,
                "health_checks": 120,
                "health_check_failures": 0
            },
            "configuration": {
                "failure_threshold": 5,
                "recovery_timeout": 60,
                "health_check_interval": 30,
                "max_retries": 3,
                "connection_pool_size": 50
            }
        }
    """
    try:
        from api.database.redis_client import get_redis_manager

        redis_manager = await get_redis_manager()
        if not redis_manager:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Redis/Memorystore not configured",
            )

        stats = redis_manager.get_stats()
        health_status = redis_manager.get_health_status()

        return RedisMetricsResponse(
            healthy=health_status.get("healthy", False),
            circuit_state=stats.get("circuit_state", "unknown"),
            failure_count=stats.get("failure_count", 0),
            success_count=stats.get("success_count", 0),
            last_failure_time=stats.get("last_failure_time"),
            last_health_check=stats.get("last_health_check"),
            client_initialized=stats.get("client_initialized", False),
            metrics=stats.get("metrics", {}),
            configuration=stats.get("configuration", {}),
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting Redis metrics: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get Redis metrics",
        ) from e

