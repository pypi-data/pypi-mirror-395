"""Usage endpoints - GET /v1/usage."""

import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies import get_current_user
from api.models.usage import IndexMetrics, QueryMetrics, UsageSummary
from api.services.usage_aggregator import usage_aggregator
from api.services.usage_tracker import usage_tracker
from api.services.quota_service import quota_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/usage", tags=["usage"])


@router.get("", response_model=UsageSummary)
async def get_usage(
    start_date: Optional[datetime] = Query(default=None, description="Start date (ISO format)"),
    end_date: Optional[datetime] = Query(default=None, description="End date (ISO format)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to retrieve (if dates not provided)"),
    current_user: dict = Depends(get_current_user),
) -> UsageSummary:
    """Get usage statistics for current user.

    Args:
        start_date: Start date for usage period
        end_date: End date for usage period
        days: Number of days to retrieve (default: 30)
        current_user: Current authenticated user

    Returns:
        Usage summary
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    if not start_date:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
    elif not end_date:
        end_date = datetime.utcnow()

    if start_date >= end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date",
        )

    organization_id = current_user.get("organization_id")

    try:
        summary_data = await usage_tracker.get_usage_summary(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
                organization_id=organization_id,
            )

        return UsageSummary(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            total_requests=summary_data.get("total_requests", 0),
            queries=QueryMetrics(**summary_data.get("queries", {})),
            indexes=IndexMetrics(**summary_data.get("indexes", {})),
            requests_by_endpoint=summary_data.get("requests_by_endpoint", {}),
            requests_by_status=summary_data.get("requests_by_status", {}),
            average_response_time_ms=summary_data.get("average_response_time_ms"),
        )
    except (ValueError, RuntimeError, ConnectionError, TimeoutError) as e:
        logger.error("Error retrieving usage: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve usage statistics",
        ) from e
    except Exception as e:
        logger.error("Unexpected error retrieving usage: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve usage statistics",
        ) from e


@router.get("/daily")
async def get_daily_usage(
    days: int = Query(default=30, ge=1, le=365, description="Number of days to retrieve"),
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Get daily usage statistics for current user.

    Args:
        days: Number of days to retrieve
        current_user: Current authenticated user

    Returns:
        Daily usage statistics
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    organization_id = current_user.get("organization_id")

    try:
        daily_usage = await usage_tracker.get_daily_usage(
            user_id=user_id,
            days=days,
            organization_id=organization_id,
        )

        return {
            "daily_usage": daily_usage,
            "period_days": days,
        }
    except (ValueError, RuntimeError, ConnectionError, TimeoutError) as e:
        logger.error("Error retrieving daily usage: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve daily usage statistics",
        ) from e
    except Exception as e:
        logger.error("Unexpected error retrieving daily usage: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve daily usage statistics",
        ) from e


@router.get("/quota")
async def get_quota_status(
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Get current quota status for user.

    Args:
        current_user: Current authenticated user

    Returns:
        Quota status with usage and limits
    """
    user_id = current_user.get("user_id")
    plan = current_user.get("plan", "professional")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        quota_status = await quota_service.get_quota_status(user_id, plan)
        return quota_status
    except (ValueError, RuntimeError, ConnectionError, TimeoutError) as e:
        logger.error("Error retrieving quota status: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve quota status",
        ) from e
    except Exception as e:
        logger.error("Unexpected error retrieving quota status: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve quota status",
        ) from e
