"""Pricing calculation API endpoints."""

import logging
import time
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status

from api.models.v1_requests import PricingCalculationRequest
from api.models.v1_responses import APIResponse, ErrorResponse, PricingCalculationResponse
from api.dependencies import get_current_user
from api.services.pricing_service import pricing_service
from api.services.quota_service import quota_service, QuotaExceededError
from api.database.exceptions import MongoDBConnectionError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/pricing", tags=["pricing"])


@router.post(
    "/calculate",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Calculate infrastructure costs",
    description="Calculate infrastructure costs from resource specifications. Includes budget checking and optimization suggestions.",
)
async def calculate_infrastructure_cost(
    request: PricingCalculationRequest,
    http_request: Request,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Calculate infrastructure costs from resource specifications.

    Args:
        request: Pricing calculation request with resource specifications
        http_request: HTTP request object
        current_user: Current authenticated user

    Returns:
        API response with cost calculation results

    Raises:
        HTTPException: If request is invalid, quota exceeded, or calculation fails
    """
    start_time = time.time()
    request_id = http_request.state.request_id if hasattr(http_request.state, "request_id") else None
    user_id = str(current_user["user_id"])
    plan = current_user.get("plan", "professional")

    logger.info(
        "Cost calculation request: resources=%d, user_id=%s, check_budgets=%s [request_id=%s]",
        len(request.resources),
        user_id,
        request.check_budgets,
        request_id or "unknown",
    )

    try:
        await quota_service.check_query_quota(user_id, plan)
    except QuotaExceededError as e:
        logger.warning(
            "Quota exceeded for user %s: %s | Request-ID: %s",
            user_id,
            e,
            request_id or "unknown",
        )
        error_response = ErrorResponse(
            error={
                "code": "QUOTA_EXCEEDED",
                "message": "Query quota exceeded",
                "details": str(e),
            },
            metadata={
                "request_id": request_id,
                "timestamp": time.time(),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=error_response.model_dump(),
        ) from e

    try:
        response = await pricing_service.calculate_infrastructure_cost(
            request=request,
            user_id=user_id,
            request_id=request_id,
        )
        query_time_ms = int((time.time() - start_time) * 1000)

        return APIResponse(
            data=response.model_dump(),
            metadata={
                "request_id": request_id,
                "timestamp": time.time(),
                "query_time_ms": query_time_ms,
            },
        )
    except ValueError as e:
        if "Budget exceeded" in str(e):
            logger.warning(
                "Budget exceeded for cost calculation: %s | Request-ID: %s",
                e,
                request_id or "unknown",
            )
            error_response = ErrorResponse(
                error={
                    "code": "BUDGET_EXCEEDED",
                    "message": "Budget exceeded - infrastructure creation blocked",
                    "details": str(e),
                },
                metadata={
                    "request_id": request_id,
                    "timestamp": time.time(),
                },
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=error_response.model_dump(),
            ) from e
        else:
            logger.warning(
                "Invalid request for cost calculation: %s | Request-ID: %s",
                e,
                request_id or "unknown",
            )
            error_response = ErrorResponse(
                error={
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid request parameters",
                    "details": str(e),
                },
                metadata={
                    "request_id": request_id,
                    "timestamp": time.time(),
                },
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_response.model_dump(),
            ) from e
    except MongoDBConnectionError as e:
        logger.error(
            "MongoDB connection error calculating costs: %s | Request-ID: %s",
            e,
            request_id or "unknown",
            exc_info=True,
        )
        error_response = ErrorResponse(
            error={
                "code": "DATABASE_ERROR",
                "message": "Database connection failed",
                "details": str(e),
            },
            metadata={
                "request_id": request_id,
                "timestamp": time.time(),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=error_response.model_dump(),
        ) from e
    except Exception as e:
        logger.error(
            "Unexpected error calculating costs: %s | Request-ID: %s",
            e,
            request_id or "unknown",
            exc_info=True,
        )
        error_response = ErrorResponse(
            error={
                "code": "INTERNAL_ERROR",
                "message": "Failed to calculate infrastructure costs",
                "details": str(e),
            },
            metadata={
                "request_id": request_id,
                "timestamp": time.time(),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e

