"""Budget management API endpoints."""

import logging
from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from api.models.budget import BudgetScopeType, BudgetStatus, EnforcementMode
from api.models.v1_requests import CreateBudgetRequest, UpdateBudgetRequest, RecordManualSpendingRequest
from api.models.v1_responses import (
    BudgetResponse,
    BudgetStatusResponse,
    ErrorResponse,
    SpendingSummaryResponse,
)
from api.services.budget_service import budget_service
from api.services.spending_tracker import spending_tracker
from api.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.post(
    "",
    response_model=BudgetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create infrastructure budget",
    description="Create a new infrastructure budget for tracking spending.",
)
async def create_budget(
    request: CreateBudgetRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> BudgetResponse:
    """Create a new infrastructure budget.

    Args:
        request: Budget creation request
        current_user: Current authenticated user

    Returns:
        Created budget

    Raises:
        HTTPException: If validation fails
    """
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in authentication token",
            )
        user_id = str(user_id)

        # Map frontend enforcement_mode to backend EnforcementMode
        enforcement_mode_str = request.enforcement_mode or "alert"
        if enforcement_mode_str == "enforce":
            enforcement_mode = EnforcementMode.BLOCK
        elif enforcement_mode_str == "warn":
            enforcement_mode = EnforcementMode.WARN
        else:
            enforcement_mode = EnforcementMode.ALERT
        
        budget = await budget_service.create_budget(
            user_id=user_id,
            name=request.name,
            scope=request.scope,
            monthly_limit_usd=request.monthly_limit_usd,
            alert_threshold_percent=request.alert_threshold_percent,
            critical_threshold_percent=request.critical_threshold_percent,
            organization_id=request.organization_id,
            description=request.description,
            enforcement_mode=enforcement_mode,
        )

        return BudgetResponse(
            budget_id=budget.budget_id,
            name=budget.name,
            description=budget.description,
            scope=budget.scope.model_dump(),
            monthly_limit_usd=budget.monthly_limit_usd,
            alert_threshold_percent=budget.alert_threshold_percent,
            critical_threshold_percent=budget.critical_threshold_percent,
            status=budget.status.value,
            enforcement_mode=budget.enforcement_mode.value,
            current_period_start=budget.current_period_start.isoformat(),
            current_period_end=budget.current_period_end.isoformat(),
            created_at=budget.created_at.isoformat(),
            updated_at=budget.updated_at.isoformat(),
        )

    except ValueError as e:
        logger.warning("Invalid budget creation request: %s", e)
        error_response = ErrorResponse(
            error={
                "code": "VALIDATION_ERROR",
                "message": str(e),
                "details": None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response.model_dump(),
        ) from e
    except Exception as e:
        logger.error("Error creating budget: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "BUDGET_CREATION_ERROR",
                "message": "Failed to create budget",
                "details": {"error": str(e)} if logger.isEnabledFor(logging.DEBUG) else None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.get(
    "",
    response_model=list[BudgetResponse],
    summary="List budgets",
    description="List all infrastructure budgets for the user/organization.",
)
async def list_budgets(
    scope_type: str | None = None,
    status_filter: str | None = None,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> list[BudgetResponse]:
    """List budgets for user/org.

    Args:
        scope_type: Filter by scope type (overall, cloud_provider, environment)
        status_filter: Filter by status (active, paused, exceeded)
        current_user: Current authenticated user

    Returns:
        List of budgets
    """
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in authentication token",
            )
        user_id = str(user_id)
        organization_id = current_user.get("organization_id")
        org_id_str = str(organization_id) if organization_id else None

        scope_type_enum = BudgetScopeType(scope_type) if scope_type else None
        status_enum = BudgetStatus(status_filter) if status_filter else None

        budgets = await budget_service.get_budgets(
            user_id=user_id,
            organization_id=org_id_str,
            scope_type=scope_type_enum,
            status=status_enum,
        )

        return [
            BudgetResponse(
                budget_id=budget.budget_id,
                name=budget.name,
                description=budget.description,
                scope=budget.scope.model_dump(),
                monthly_limit_usd=budget.monthly_limit_usd,
                alert_threshold_percent=budget.alert_threshold_percent,
                critical_threshold_percent=budget.critical_threshold_percent,
                status=budget.status.value,
                enforcement_mode=budget.enforcement_mode.value,
                current_period_start=budget.current_period_start.isoformat(),
                current_period_end=budget.current_period_end.isoformat(),
                created_at=budget.created_at.isoformat(),
                updated_at=budget.updated_at.isoformat(),
            )
            for budget in budgets
        ]

    except ValueError as e:
        logger.warning("Invalid filter: %s", e)
        error_response = ErrorResponse(
            error={
                "code": "VALIDATION_ERROR",
                "message": str(e),
                "details": None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response.model_dump(),
        ) from e
    except Exception as e:
        logger.error("Error listing budgets: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "BUDGET_LIST_ERROR",
                "message": "Failed to list budgets",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.get(
    "/{budget_id}",
    response_model=BudgetResponse,
    summary="Get budget",
    description="Get budget details by ID.",
)
async def get_budget(
    budget_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> BudgetResponse:
    """Get budget by ID.

    Args:
        budget_id: Budget ID
        current_user: Current authenticated user

    Returns:
        Budget details

    Raises:
        HTTPException: If budget not found
    """
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in authentication token",
            )
        user_id = str(user_id)
        
        budget = await budget_service.get_budget(budget_id, user_id)
        if not budget:
            error_response = ErrorResponse(
                error={
                    "code": "BUDGET_NOT_FOUND",
                    "message": f"Budget not found: {budget_id}",
                    "details": None,
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response.model_dump(),
            )

        return BudgetResponse(
            budget_id=budget.budget_id,
            name=budget.name,
            description=budget.description,
            scope=budget.scope.model_dump(),
            monthly_limit_usd=budget.monthly_limit_usd,
            alert_threshold_percent=budget.alert_threshold_percent,
            critical_threshold_percent=budget.critical_threshold_percent,
            status=budget.status.value,
            enforcement_mode=budget.enforcement_mode.value,
            current_period_start=budget.current_period_start.isoformat(),
            current_period_end=budget.current_period_end.isoformat(),
            created_at=budget.created_at.isoformat(),
            updated_at=budget.updated_at.isoformat(),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting budget: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "BUDGET_GET_ERROR",
                "message": "Failed to get budget",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.put(
    "/{budget_id}",
    response_model=BudgetResponse,
    summary="Update budget",
    description="Update budget details.",
)
async def update_budget(
    budget_id: str,
    request: UpdateBudgetRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> BudgetResponse:
    """Update budget.

    Args:
        budget_id: Budget ID
        request: Update request
        current_user: Current authenticated user

    Returns:
        Updated budget

    Raises:
        HTTPException: If budget not found or validation fails
    """
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in authentication token",
            )
        user_id = str(user_id)
        
        updates = {}
        if request.name is not None:
            updates["name"] = request.name
        if request.description is not None:
            updates["description"] = request.description
        if request.monthly_limit_usd is not None:
            updates["monthly_limit_usd"] = request.monthly_limit_usd
        if request.alert_threshold_percent is not None:
            updates["alert_threshold_percent"] = request.alert_threshold_percent
        if request.critical_threshold_percent is not None:
            updates["critical_threshold_percent"] = request.critical_threshold_percent
        if request.enforcement_mode is not None:
            updates["enforcement_mode"] = EnforcementMode(request.enforcement_mode).value
        if request.status is not None:
            updates["status"] = BudgetStatus(request.status).value

        if not updates:
            error_response = ErrorResponse(
                error={
                    "code": "VALIDATION_ERROR",
                    "message": "No fields to update",
                    "details": None,
                }
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_response.model_dump(),
            )

        budget = await budget_service.update_budget(budget_id, user_id, updates)

        return BudgetResponse(
            budget_id=budget.budget_id,
            name=budget.name,
            description=budget.description,
            scope=budget.scope.model_dump(),
            monthly_limit_usd=budget.monthly_limit_usd,
            alert_threshold_percent=budget.alert_threshold_percent,
            critical_threshold_percent=budget.critical_threshold_percent,
            status=budget.status.value,
            enforcement_mode=budget.enforcement_mode.value,
            current_period_start=budget.current_period_start.isoformat(),
            current_period_end=budget.current_period_end.isoformat(),
            created_at=budget.created_at.isoformat(),
            updated_at=budget.updated_at.isoformat(),
        )

    except ValueError as e:
        logger.warning("Invalid budget update: %s", e)
        error_response = ErrorResponse(
            error={
                "code": "VALIDATION_ERROR",
                "message": str(e),
                "details": None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response.model_dump(),
        ) from e
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error updating budget: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "BUDGET_UPDATE_ERROR",
                "message": "Failed to update budget",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.delete(
    "/{budget_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete budget",
    description="Delete infrastructure budget.",
)
async def delete_budget(
    budget_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> None:
    """Delete budget.

    Args:
        budget_id: Budget ID
        current_user: Current authenticated user

    Raises:
        HTTPException: If budget not found
    """
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in authentication token",
            )
        user_id = str(user_id)
        
        await budget_service.delete_budget(budget_id, user_id)

    except ValueError as e:
        logger.warning("Budget not found for deletion: %s", e)
        error_response = ErrorResponse(
            error={
                "code": "BUDGET_NOT_FOUND",
                "message": str(e),
                "details": None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response.model_dump(),
        ) from e
    except Exception as e:
        logger.error("Error deleting budget: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "BUDGET_DELETE_ERROR",
                "message": "Failed to delete budget",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.get(
    "/{budget_id}/status",
    response_model=BudgetStatusResponse,
    summary="Get budget status",
    description="Get current budget status and spending.",
)
async def get_budget_status(
    budget_id: str,
    period: str | None = None,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> BudgetStatusResponse:
    """Get budget status.

    Args:
        budget_id: Budget ID
        period: Period string (YYYY-MM), defaults to current month
        current_user: Current authenticated user

    Returns:
        Budget status

    Raises:
        HTTPException: If budget not found
    """
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in authentication token",
            )
        user_id = str(user_id)
        
        budget = await budget_service.get_budget(budget_id, user_id)
        if not budget:
            error_response = ErrorResponse(
                error={
                    "code": "BUDGET_NOT_FOUND",
                    "message": f"Budget not found: {budget_id}",
                    "details": None,
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response.model_dump(),
            )

        status_obj = await budget_service.get_budget_status(budget_id, period)
        if not status_obj:
            error_response = ErrorResponse(
                error={
                    "code": "STATUS_NOT_FOUND",
                    "message": f"Budget status not found for period: {period or 'current'}",
                    "details": None,
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response.model_dump(),
            )

        return BudgetStatusResponse(
            budget_id=status_obj.budget_id,
            period=status_obj.period,
            total_spent_usd=status_obj.total_spent_usd,
            budget_limit_usd=status_obj.budget_limit_usd,
            remaining_usd=status_obj.remaining_usd,
            utilization_percent=status_obj.utilization_percent,
            status=status_obj.status,
            by_cloud_provider=status_obj.by_cloud_provider,
            by_service=status_obj.by_service,
            projected_monthly_spend=status_obj.projected_monthly_spend,
            projected_exceed=status_obj.projected_exceed,
            days_until_exceed=status_obj.days_until_exceed,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting budget status: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "STATUS_GET_ERROR",
                "message": "Failed to get budget status",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.get(
    "/{budget_id}/spending",
    response_model=dict[str, Any],
    summary="Get budget spending breakdown",
    description="Get detailed spending breakdown for budget.",
)
async def get_budget_spending(
    budget_id: str,
    period: str | None = None,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Get budget spending breakdown.

    Args:
        budget_id: Budget ID
        period: Period string (YYYY-MM), defaults to current month
        current_user: Current authenticated user

    Returns:
        Spending breakdown

    Raises:
        HTTPException: If budget not found
    """
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in authentication token",
            )
        user_id = str(user_id)
        
        budget = await budget_service.get_budget(budget_id, user_id)
        if not budget:
            error_response = ErrorResponse(
                error={
                    "code": "BUDGET_NOT_FOUND",
                    "message": f"Budget not found: {budget_id}",
                    "details": None,
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response.model_dump(),
            )

        status_obj = await budget_service.get_budget_status(budget_id, period)
        if not status_obj:
            return {
                "budget_id": budget_id,
                "period": period or "current",
                "total_spent_usd": 0.0,
                "breakdown": {},
            }

        return {
            "budget_id": budget_id,
            "period": status_obj.period,
            "total_spent_usd": status_obj.total_spent_usd,
            "breakdown": {
                "by_cloud_provider": status_obj.by_cloud_provider,
                "by_service": status_obj.by_service,
                "by_resource_type": status_obj.by_resource_type,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting budget spending: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "SPENDING_GET_ERROR",
                "message": "Failed to get spending breakdown",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.get(
    "/spending/summary",
    response_model=SpendingSummaryResponse,
    summary="Get spending summary",
    description="Get spending summary for user/organization.",
)
async def get_spending_summary(
    period: str | None = None,
    environment_id: str | None = None,
    cloud_provider: str | None = None,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> SpendingSummaryResponse:
    """Get spending summary.

    Args:
        period: Period string (YYYY-MM), defaults to current month
        environment_id: Filter by environment ID (optional)
        cloud_provider: Filter by cloud provider (optional)
        current_user: Current authenticated user

    Returns:
        Spending summary
    """
    try:
        from api.models.budget import get_month_period
        
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in authentication token",
            )
        user_id = str(user_id)
        
        if period:
            period_start = datetime.strptime(period, "%Y-%m")
            period_start = datetime(period_start.year, period_start.month, 1)
            period_end = period_start + timedelta(days=32)
            period_end = period_end.replace(day=1) - timedelta(seconds=1)
        else:
            period_start, period_end = get_month_period()

        spending = await budget_service.aggregate_spending_from_analysis(
            user_id=user_id,
            period_start=period_start,
            period_end=period_end,
        )

        period_str = period or period_start.strftime("%Y-%m")

        return SpendingSummaryResponse(
            period=period_str,
            total_spent_usd=spending["total_spent_usd"],
            by_cloud_provider=spending["by_cloud_provider"],
            by_service=spending["by_service"],
            by_environment={},
            component_count=spending["component_count"],
        )

    except ValueError as e:
        logger.warning("Invalid period format: %s", e)
        error_response = ErrorResponse(
            error={
                "code": "VALIDATION_ERROR",
                "message": f"Invalid period format: {e}",
                "details": None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response.model_dump(),
        ) from e
    except Exception as e:
        logger.error("Error getting spending summary: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "SPENDING_SUMMARY_ERROR",
                "message": "Failed to get spending summary",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e



@router.post(
    "/spending/manual",
    status_code=status.HTTP_201_CREATED,
    summary="Record manual spending",
    description="Record spending for manually created or existing infrastructure that was created before WISTX.",
)
async def record_manual_spending(
    request: RecordManualSpendingRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Record spending for manually created or existing infrastructure.

    Use this endpoint to record spending for infrastructure that was:
    - Created manually (not through coding agents)
    - Created before WISTX was implemented
    - Created outside the system
    - Needs to be tracked retroactively

    Args:
        request: Manual spending record request
        current_user: Current authenticated user

    Returns:
        Dictionary with recording results

    Raises:
        HTTPException: If recording fails
    """
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in authentication token",
            )
        user_id = str(user_id)

        result = await spending_tracker.record_manual_spending(
            user_id=user_id,
            amount_usd=request.amount_usd,
            cloud_provider=request.cloud_provider,
            environment_name=request.environment_name,
            service=request.service,
            resource_type=request.resource_type,
            description=request.description,
            source_id=request.source_id,
        )

        if not result.get("spending_recorded"):
            error_response = ErrorResponse(
                error={
                    "code": "SPENDING_RECORD_ERROR",
                    "message": result.get("error", "Failed to record spending"),
                    "details": None,
                }
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_response.model_dump(),
            )

        return {
            "success": True,
            "message": "Manual spending recorded successfully",
            "data": result,
        }

    except HTTPException:
        raise
    except ValueError as e:
        logger.warning("Invalid manual spending request: %s", e)
        error_response = ErrorResponse(
            error={
                "code": "VALIDATION_ERROR",
                "message": str(e),
                "details": None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response.model_dump(),
        ) from e
    except Exception as e:
        logger.error("Error recording manual spending: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "SPENDING_RECORD_ERROR",
                "message": "Failed to record manual spending",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e
