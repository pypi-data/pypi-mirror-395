"""Agent improvement metrics endpoints."""

import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies import get_current_user
from api.models.task_tracking import AgentImprovementReport
from api.services.agent_metrics import agent_metrics_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/agent-improvement", response_model=AgentImprovementReport)
async def get_agent_improvement(
    start_date: Optional[datetime] = Query(
        default=None, description="Start date (ISO format)"
    ),
    end_date: Optional[datetime] = Query(default=None, description="End date (ISO format)"),
    days: int = Query(
        default=30, ge=1, le=365, description="Number of days to retrieve (if dates not provided)"
    ),
    current_user: dict = Depends(get_current_user),
) -> AgentImprovementReport:
    """Get agent improvement metrics report.

    Args:
        start_date: Start date for report period
        end_date: End date for report period
        days: Number of days to retrieve (default: 30)
        current_user: Current authenticated user

    Returns:
        Agent improvement report
    """
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

    try:
        report = await agent_metrics_service.generate_improvement_report(start_date, end_date)
        return report
    except Exception as e:
        logger.error("Error generating improvement report: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate improvement report",
        ) from e


@router.get("/task-success")
async def get_task_success_metrics(
    start_date: Optional[datetime] = Query(
        default=None, description="Start date (ISO format)"
    ),
    end_date: Optional[datetime] = Query(default=None, description="End date (ISO format)"),
    days: int = Query(
        default=30, ge=1, le=365, description="Number of days to retrieve (if dates not provided)"
    ),
    task_type: Optional[str] = Query(
        default=None, description="Filter by task type"
    ),
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Get task success rate metrics.

    Args:
        start_date: Start date for metrics period
        end_date: End date for metrics period
        days: Number of days to retrieve (default: 30)
        task_type: Filter by task type
        current_user: Current authenticated user

    Returns:
        Task success metrics
    """
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

    try:
        without_wistx = await agent_metrics_service.calculate_task_success_rate(
            start_date, end_date, wistx_enabled=False, task_type=task_type
        )
        with_wistx = await agent_metrics_service.calculate_task_success_rate(
            start_date, end_date, wistx_enabled=True, task_type=task_type
        )

        improvement = 0.0
        if without_wistx["success_rate"] > 0:
            improvement = (
                (with_wistx["success_rate"] - without_wistx["success_rate"])
                / without_wistx["success_rate"]
                * 100
            )

        return {
            "without_wistx": without_wistx,
            "with_wistx": with_wistx,
            "improvement_percentage": round(improvement, 2),
        }
    except Exception as e:
        logger.error("Error retrieving task success metrics: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve task success metrics",
        ) from e


@router.get("/compliance")
async def get_compliance_metrics(
    start_date: Optional[datetime] = Query(
        default=None, description="Start date (ISO format)"
    ),
    end_date: Optional[datetime] = Query(default=None, description="End date (ISO format)"),
    days: int = Query(
        default=30, ge=1, le=365, description="Number of days to retrieve (if dates not provided)"
    ),
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Get compliance adherence metrics.

    Args:
        start_date: Start date for metrics period
        end_date: End date for metrics period
        days: Number of days to retrieve (default: 30)
        current_user: Current authenticated user

    Returns:
        Compliance metrics
    """
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

    try:
        without_wistx = await agent_metrics_service.calculate_compliance_score(
            start_date, end_date, wistx_enabled=False
        )
        with_wistx = await agent_metrics_service.calculate_compliance_score(
            start_date, end_date, wistx_enabled=True
        )

        improvement = 0.0
        if (
            without_wistx.get("average_score") is not None
            and with_wistx.get("average_score") is not None
        ):
            without_score = without_wistx["average_score"]
            with_score = with_wistx["average_score"]
            if without_score > 0:
                improvement = ((with_score - without_score) / without_score) * 100

        return {
            "without_wistx": without_wistx,
            "with_wistx": with_wistx,
            "improvement_percentage": round(improvement, 2),
        }
    except Exception as e:
        logger.error("Error retrieving compliance metrics: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve compliance metrics",
        ) from e


@router.get("/cost-accuracy")
async def get_cost_accuracy_metrics(
    start_date: Optional[datetime] = Query(
        default=None, description="Start date (ISO format)"
    ),
    end_date: Optional[datetime] = Query(default=None, description="End date (ISO format)"),
    days: int = Query(
        default=30, ge=1, le=365, description="Number of days to retrieve (if dates not provided)"
    ),
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Get cost estimation accuracy metrics.

    Args:
        start_date: Start date for metrics period
        end_date: End date for metrics period
        days: Number of days to retrieve (default: 30)
        current_user: Current authenticated user

    Returns:
        Cost accuracy metrics
    """
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

    try:
        without_wistx = await agent_metrics_service.calculate_cost_accuracy(
            start_date, end_date, wistx_enabled=False
        )
        with_wistx = await agent_metrics_service.calculate_cost_accuracy(
            start_date, end_date, wistx_enabled=True
        )

        improvement = 0.0
        if (
            without_wistx.get("average_accuracy") is not None
            and with_wistx.get("average_accuracy") is not None
        ):
            without_accuracy = without_wistx["average_accuracy"]
            with_accuracy = with_wistx["average_accuracy"]
            if without_accuracy > 0:
                improvement = ((with_accuracy - without_accuracy) / without_accuracy) * 100

        return {
            "without_wistx": without_wistx,
            "with_wistx": with_wistx,
            "improvement_percentage": round(improvement, 2),
        }
    except Exception as e:
        logger.error("Error retrieving cost accuracy metrics: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve cost accuracy metrics",
        ) from e


@router.get("/comparison")
async def get_comparison_metrics(
    start_date: Optional[datetime] = Query(
        default=None, description="Start date (ISO format)"
    ),
    end_date: Optional[datetime] = Query(default=None, description="End date (ISO format)"),
    days: int = Query(
        default=30, ge=1, le=365, description="Number of days to retrieve (if dates not provided)"
    ),
    task_type: Optional[str] = Query(
        default=None, description="Filter by task type"
    ),
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Get comparison metrics (with vs without WISTX).

    Args:
        start_date: Start date for metrics period
        end_date: End date for metrics period
        days: Number of days to retrieve (default: 30)
        task_type: Filter by task type
        current_user: Current authenticated user

    Returns:
        Comparison metrics
    """
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

    try:
        comparisons = await agent_metrics_service.compare_with_baseline(
            start_date, end_date, task_type=task_type
        )

        return {
            "comparisons": [c.model_dump() for c in comparisons],
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
        }
    except Exception as e:
        logger.error("Error retrieving comparison metrics: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve comparison metrics",
        ) from e

