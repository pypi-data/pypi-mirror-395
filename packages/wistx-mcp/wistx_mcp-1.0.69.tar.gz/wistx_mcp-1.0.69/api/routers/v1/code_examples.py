"""Code examples endpoints for v1 API."""

import logging
import time
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status

from api.models.v1_requests import CodeExamplesSearchRequest
from api.models.v1_responses import APIResponse, ErrorResponse, CodeExamplesSearchResponse
from api.services.code_examples_service import code_examples_service
from api.services.quota_service import quota_service, QuotaExceededError
from api.database.exceptions import MongoDBConnectionError
from api.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/code-examples", tags=["code-examples"])


@router.post(
    "/search",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Search code examples",
    description="Search infrastructure code examples from curated repositories. Supports filtering by code type, cloud provider, services, quality score, and compliance standards.",
)
async def search_code_examples(
    request: CodeExamplesSearchRequest,
    http_request: Request,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Search infrastructure code examples.

    Args:
        request: Code examples search request
        http_request: HTTP request object
        current_user: Current authenticated user

    Returns:
        API response with code examples search results

    Raises:
        HTTPException: If request is invalid, quota exceeded, or search fails
    """
    start_time = time.time()
    request_id = http_request.state.request_id if hasattr(http_request.state, "request_id") else None
    user_id = str(current_user["user_id"])
    plan = current_user.get("plan", "professional")

    logger.info(
        "Code examples search request: query=%s, user_id=%s [request_id=%s]",
        request.query[:50],
        user_id,
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
        response = await code_examples_service.search_code_examples(
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
        logger.warning(
            "Invalid request for code examples search: %s | Request-ID: %s",
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
            "MongoDB connection error searching code examples: %s | Request-ID: %s",
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
            "Unexpected error searching code examples: %s | Request-ID: %s",
            e,
            request_id or "unknown",
            exc_info=True,
        )
        error_response = ErrorResponse(
            error={
                "code": "INTERNAL_ERROR",
                "message": "Failed to search code examples",
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

