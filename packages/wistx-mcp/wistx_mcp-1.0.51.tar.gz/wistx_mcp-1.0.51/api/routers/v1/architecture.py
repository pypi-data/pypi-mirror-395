"""Architecture endpoints for v1 API."""

import logging
import time
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status

from api.models.v1_requests import ArchitectureDesignRequest
from api.models.v1_responses import APIResponse, ErrorResponse
from api.services.architecture_service import ArchitectureService
from api.services.exceptions import QuotaExceededError
from api.services.quota_service import quota_service
from api.database.exceptions import MongoDBConnectionError
from api.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/architecture", tags=["architecture"])

architecture_service = ArchitectureService()


@router.post(
    "/design",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Design architecture",
    description="Design and initialize DevOps/infrastructure/SRE/platform engineering projects",
)
async def design_architecture(
    request: ArchitectureDesignRequest,
    http_request: Request,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Design architecture for DevOps/infrastructure projects.

    Args:
        request: Architecture design request
        http_request: FastAPI request object for accessing request ID

    Returns:
        API response with architecture design
    """
    request_id = getattr(http_request.state, "request_id", "")
    start_time = time.time()

    user_id = current_user.get("user_id")
    plan = current_user.get("plan", "professional")
    authorization = http_request.headers.get("Authorization", "")
    api_key = authorization.replace("Bearer ", "").strip() if authorization.startswith("Bearer ") else ""

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
        organization_id = current_user.get("organization_id")
        response = await architecture_service.design_architecture(
            request,
            api_key=api_key,
            user_id=user_id,
            organization_id=organization_id,
            use_cache=True,
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
        logger.warning(
            "Invalid request for architecture design: %s | Request-ID: %s",
            e,
            request_id,
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
            "MongoDB connection error designing architecture: %s | Request-ID: %s",
            e,
            request_id,
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
        import traceback
        error_traceback = traceback.format_exc()
        logger.error(
            "Error designing architecture: %s | Request-ID: %s | Traceback: %s",
            e,
            request_id,
            error_traceback,
            exc_info=True,
        )
        error_response = ErrorResponse(
            error={
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
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

