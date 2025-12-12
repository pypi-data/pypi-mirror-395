"""Knowledge research endpoints for v1 API."""

import logging
import time

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status

from api.models.v1_requests import KnowledgeResearchRequest
from api.models.v1_responses import APIResponse, ErrorResponse
from api.services.knowledge_service import KnowledgeService
from api.services.exceptions import QuotaExceededError
from api.services.quota_service import quota_service
from api.database.exceptions import MongoDBConnectionError
from api.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

knowledge_service = KnowledgeService()


@router.post(
    "/research",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Research knowledge base",
    description="Deep research tool for DevOps, infrastructure, compliance, FinOps, and platform engineering knowledge",
)
async def research_knowledge_base(
    request: KnowledgeResearchRequest,
    http_request: Request,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Research knowledge base across all domains.

    Args:
        request: Knowledge research request
        http_request: FastAPI request object for accessing request ID

    Returns:
        API response with research results and summary
    """
    request_id = getattr(http_request.state, "request_id", "")
    start_time = time.time()

    user_id = current_user.get("user_id")
    plan = current_user.get("plan", "professional")
    organization_id = current_user.get("organization_id")

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
        response = await knowledge_service.research_knowledge_base(
            request,
            user_id=user_id,
            organization_id=organization_id,
        )
        query_time_ms = int((time.time() - start_time) * 1000)

        response.metadata["query_time_ms"] = query_time_ms

        return APIResponse(
            data=response.model_dump(),
            metadata={
                "request_id": request_id,
                "timestamp": time.time(),
                "query_time_ms": query_time_ms,
            },
        )
    except MongoDBConnectionError as e:
        logger.error(
            "MongoDB connection error researching knowledge base: %s | Request-ID: %s",
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
    except ValueError as e:
        logger.warning(
            "Invalid request for knowledge research: %s | Request-ID: %s",
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
    except RuntimeError as e:
        error_msg = str(e)
        if "vector search is not available" in error_msg.lower() or "gemini" in error_msg.lower() or "pinecone" in error_msg.lower():
            logger.warning(
                "Vector search not available for knowledge research: %s | Request-ID: %s",
                e,
                request_id,
            )
            error_response = ErrorResponse(
                error={
                    "code": "SERVICE_UNAVAILABLE",
                    "message": "Knowledge search service is not available",
                    "details": "Vector search requires Gemini API key and Pinecone API key to be configured. Please configure these settings to enable knowledge base search.",
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
        logger.error(
            "Runtime error researching knowledge base: %s | Request-ID: %s",
            e,
            request_id,
            exc_info=True,
        )
        error_response = ErrorResponse(
            error={
                "code": "RUNTIME_ERROR",
                "message": "An error occurred while researching knowledge base",
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
    except Exception as e:
        logger.error(
            "Error researching knowledge base: %s | Request-ID: %s",
            e,
            request_id,
            exc_info=True,
        )
        error_response = ErrorResponse(
            error={
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
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

