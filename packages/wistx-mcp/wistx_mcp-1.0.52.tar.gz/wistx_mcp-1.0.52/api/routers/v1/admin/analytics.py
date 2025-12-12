"""Admin analytics endpoints."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies.auth import require_admin
from api.models.admin.analytics import (
    TopEndpointsResponse,
    TopUsersResponse,
    UsageByPlanListResponse,
    UsageOverviewResponse,
    UsageTrendsQuery,
    UsageTrendsResponse,
)
from api.services.admin.analytics_service import admin_analytics_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analytics", tags=["admin"])


@router.get("/overview", response_model=UsageOverviewResponse, summary="Get usage overview")
async def get_usage_overview(
    current_user: dict[str, Any] = Depends(require_admin),
) -> UsageOverviewResponse:
    """Get usage overview statistics.

    Args:
        current_user: Current admin user

    Returns:
        Usage overview response
    """
    try:
        return await admin_analytics_service.get_usage_overview()
    except Exception as e:
        logger.error("Error getting usage overview: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get usage overview",
        ) from e


@router.get("/by-plan", response_model=UsageByPlanListResponse, summary="Get usage by plan")
async def get_usage_by_plan(
    current_user: dict[str, Any] = Depends(require_admin),
) -> UsageByPlanListResponse:
    """Get usage statistics by plan.

    Args:
        current_user: Current admin user

    Returns:
        Usage by plan response
    """
    try:
        return await admin_analytics_service.get_usage_by_plan()
    except Exception as e:
        logger.error("Error getting usage by plan: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get usage by plan",
        ) from e


@router.get("/trends", response_model=UsageTrendsResponse, summary="Get usage trends")
async def get_usage_trends(
    days: int = Query(default=30, ge=1, le=365, description="Number of days"),
    group_by: str = Query(default="day", description="Group by (day, week, month)"),
    current_user: dict[str, Any] = Depends(require_admin),
) -> UsageTrendsResponse:
    """Get usage trends.

    Args:
        days: Number of days
        group_by: Group by period
        current_user: Current admin user

    Returns:
        Usage trends response
    """
    query = UsageTrendsQuery(days=days, group_by=group_by)

    try:
        return await admin_analytics_service.get_usage_trends(query)
    except Exception as e:
        logger.error("Error getting usage trends: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get usage trends",
        ) from e


@router.get("/top-endpoints", response_model=TopEndpointsResponse, summary="Get top endpoints")
async def get_top_endpoints(
    days: int = Query(default=30, ge=1, le=365, description="Number of days"),
    limit: int = Query(default=10, ge=1, le=100, description="Maximum number of results"),
    current_user: dict[str, Any] = Depends(require_admin),
) -> TopEndpointsResponse:
    """Get top endpoints by usage.

    Args:
        days: Number of days to analyze
        limit: Maximum number of results
        current_user: Current admin user

    Returns:
        Top endpoints response
    """
    try:
        return await admin_analytics_service.get_top_endpoints(days=days, limit=limit)
    except Exception as e:
        logger.error("Error getting top endpoints: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get top endpoints",
        ) from e


@router.get("/top-users", response_model=TopUsersResponse, summary="Get top users")
async def get_top_users(
    days: int = Query(default=30, ge=1, le=365, description="Number of days"),
    limit: int = Query(default=10, ge=1, le=100, description="Maximum number of results"),
    current_user: dict[str, Any] = Depends(require_admin),
) -> TopUsersResponse:
    """Get top users by activity.

    Args:
        days: Number of days to analyze
        limit: Maximum number of results
        current_user: Current admin user

    Returns:
        Top users response
    """
    try:
        return await admin_analytics_service.get_top_users(days=days, limit=limit)
    except Exception as e:
        logger.error("Error getting top users: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get top users",
        ) from e

