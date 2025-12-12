"""Health check and status endpoints."""

import logging
from typing import Any

from fastapi import APIRouter, Query, HTTPException, status

from api.models.v1_responses import StatusResponse, UptimeStatsResponse
from api.services.status_service import status_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    summary="Health check",
    description="Basic health check endpoint. Returns simple status.",
)
async def health() -> dict[str, str]:
    """Basic health check endpoint.

    Returns:
        Simple health status
    """
    return {"status": "healthy"}


@router.get(
    "/status",
    response_model=StatusResponse,
    summary="System status",
    description="Comprehensive status check for all WISTX services including API, Database, Vector Search, Indexing, and Authentication.",
)
async def get_status() -> StatusResponse:
    """Get comprehensive system status.

    Returns:
        Detailed status of all services

    Raises:
        HTTPException: If status check fails
    """
    try:
        status_data = await status_service.check_all_services()
        return StatusResponse(**status_data)
    except Exception as e:
        logger.error("Failed to get system status: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve system status: {str(e)}",
        ) from e


@router.get(
    "/status/uptime",
    response_model=UptimeStatsResponse,
    summary="Uptime statistics",
    description="Get uptime statistics for WISTX services over a specified period.",
)
async def get_uptime_stats(
    days: int = Query(
        default=30,
        ge=1,
        le=365,
        description="Number of days to calculate uptime for (1-365)",
    ),
) -> UptimeStatsResponse:
    """Get uptime statistics.

    Args:
        days: Number of days to calculate uptime for

    Returns:
        Uptime statistics

    Raises:
        HTTPException: If uptime calculation fails
    """
    try:
        uptime_data = await status_service.get_uptime_stats(days=days)
        return UptimeStatsResponse(**uptime_data)
    except Exception as e:
        logger.error("Failed to get uptime stats: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve uptime statistics: {str(e)}",
        ) from e
