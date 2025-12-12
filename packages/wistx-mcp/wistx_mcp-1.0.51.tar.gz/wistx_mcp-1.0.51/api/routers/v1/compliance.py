"""Compliance endpoints for v1 API."""

import logging
import time

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status

from api.models.v1_requests import ComplianceRequirementsRequest
from api.models.v1_responses import APIResponse, ErrorResponse
from api.services.compliance_service import ComplianceService
from api.services.exceptions import QuotaExceededError
from api.services.quota_service import quota_service
from api.database.exceptions import MongoDBConnectionError
from api.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/compliance", tags=["compliance"])

compliance_service = ComplianceService()


@router.post(
    "/requirements",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Get compliance requirements",
    description="Get compliance requirements for infrastructure resources (PCI-DSS, HIPAA, CIS, SOC2, NIST, ISO 27001)",
)
async def get_compliance_requirements(
    request: ComplianceRequirementsRequest,
    http_request: Request,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Get compliance requirements for infrastructure resources.

    Args:
        request: Compliance requirements request
        http_request: FastAPI request object for accessing request ID

    Returns:
        API response with compliance controls and summary
    """
    request_id = getattr(http_request.state, "request_id", "")
    start_time = time.time()

    user_id = current_user.get("user_id")
    plan = current_user.get("plan", "professional")

    try:
        await quota_service.check_query_quota(user_id, plan)
    except QuotaExceededError as e:
        logger.warning(
            "Query quota exceeded for user %s: %s | Request-ID: %s",
            user_id,
            e,
            request_id,
        )
        error_response = ErrorResponse(
            error={
                "code": "QUOTA_EXCEEDED",
                "message": str(e),
                "details": {
                    "limit_type": e.limit_type,
                    "current": e.current,
                    "limit": e.limit,
                },
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
        response = await compliance_service.get_compliance_requirements(request, request_id=request_id)
        query_time_ms = int((time.time() - start_time) * 1000)

        response_metadata = response.metadata.copy()
        response_metadata["query_time_ms"] = query_time_ms
        response_metadata["request_id"] = request_id
        response_metadata["timestamp"] = time.time()

        return APIResponse(
            data=response.model_dump(),
            metadata=response_metadata,
        )
    except MongoDBConnectionError as e:
        logger.error(
            "MongoDB connection error getting compliance requirements: %s | Request-ID: %s",
            e,
            request_id,
            exc_info=True,
        )
        error_response = ErrorResponse(
            error={
                "code": "DATABASE_ERROR",
                "message": "Database connection failed",
                "details": {"error": str(e)},
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
    except ValueError as e:
        logger.warning(
            "Invalid request for compliance requirements: %s | Request-ID: %s",
            e,
            request_id,
        )
        error_response = ErrorResponse(
            error={
                "code": "VALIDATION_ERROR",
                "message": "Invalid request parameters",
                "details": {"error": str(e)},
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
    except Exception as e:
        logger.error(
            "Error getting compliance requirements: %s | Request-ID: %s",
            e,
            request_id,
            exc_info=True,
        )
        error_response = ErrorResponse(
            error={
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": {"error": str(e)} if logger.isEnabledFor(logging.DEBUG) else None,
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

