"""Admin activity monitoring endpoints."""

import logging
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies.auth import require_admin, require_permission_factory
from api.models.admin.analytics import ActivityFeedQuery, ActivityFeedResponse
from api.services.admin.activity_service import admin_activity_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/activity", tags=["admin"])


@router.get("/feed", response_model=ActivityFeedResponse, summary="Get activity feed")
async def get_activity_feed(
    user_id: str | None = Query(None, description="Filter by user ID"),
    endpoint: str | None = Query(None, description="Filter by endpoint"),
    operation_type: str | None = Query(None, description="Filter by operation type"),
    success: bool | None = Query(None, description="Filter by success status"),
    start_date: datetime | None = Query(None, description="Start date filter"),
    end_date: datetime | None = Query(None, description="End date filter"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
    current_user: dict[str, Any] = Depends(require_permission_factory("activity.read")),
) -> ActivityFeedResponse:
    """Get activity feed with filters.

    Args:
        user_id: User ID filter
        endpoint: Endpoint filter
        operation_type: Operation type filter
        success: Success status filter
        start_date: Start date filter
        end_date: End date filter
        limit: Result limit
        offset: Result offset
        current_user: Current admin user

    Returns:
        Activity feed response
    """
    query = ActivityFeedQuery(
        user_id=user_id,
        endpoint=endpoint,
        operation_type=operation_type,
        success=success,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset,
    )

    try:
        return await admin_activity_service.get_activity_feed(query)
    except Exception as e:
        logger.error("Error getting activity feed: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get activity feed",
        ) from e


@router.get("/user/{user_id}", summary="Get user activity timeline")
async def get_user_activity(
    user_id: str,
    start_date: datetime | None = Query(None, description="Start date filter"),
    end_date: datetime | None = Query(None, description="End date filter"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of results"),
    current_user: dict[str, Any] = Depends(require_permission_factory("activity.read")),
) -> dict[str, Any]:
    """Get user activity timeline.

    Args:
        user_id: User ID
        start_date: Start date filter
        end_date: End date filter
        limit: Result limit
        current_user: Current admin user

    Returns:
        User activity timeline
    """
    try:
        activities = await admin_activity_service.get_user_activity(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
        )
        return {
            "user_id": user_id,
            "activities": [activity.model_dump() for activity in activities],
            "count": len(activities),
        }
    except Exception as e:
        logger.error("Error getting user activity: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user activity",
        ) from e

