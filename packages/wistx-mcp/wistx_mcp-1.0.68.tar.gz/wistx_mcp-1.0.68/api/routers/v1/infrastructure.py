"""Infrastructure endpoints for v1 API."""

import logging
import time
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status

from api.models.v1_requests import InfrastructureInventoryRequest, InfrastructureManageRequest
from api.models.v1_responses import APIResponse, ErrorResponse
from api.services.infrastructure_service import InfrastructureService
from api.services.exceptions import QuotaExceededError
from api.services.quota_service import quota_service
from api.database.exceptions import MongoDBConnectionError
from api.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/infrastructure", tags=["infrastructure"])

infrastructure_service = InfrastructureService()


@router.get(
    "/inventory",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Get infrastructure inventory",
    description="Get existing infrastructure context for coding agents",
)
async def get_infrastructure_inventory(
    http_request: Request,
    repository_url: str | None = None,
    environment_name: str | None = None,
    inventory_id: str | None = None,
    include_compliance: bool = True,
    include_costs: bool = True,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Get infrastructure inventory.

    Args:
        repository_url: GitHub repository URL
        environment_name: Environment name (dev, stage, prod, etc.)
        inventory_id: Inventory ID
        include_compliance: Include compliance status
        include_costs: Include cost information
        http_request: FastAPI request object for accessing request ID

    Returns:
        API response with infrastructure inventory
    """
    request_id = getattr(http_request.state, "request_id", "") if http_request else ""
    start_time = time.time()

    user_id = current_user.get("user_id")
    plan = current_user.get("plan", "professional")
    authorization = http_request.headers.get("Authorization", "")
    api_key = authorization.replace("Bearer ", "").strip() if authorization.startswith("Bearer ") else ""

    if not repository_url and not inventory_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "repository_url or inventory_id is required",
                },
            },
        )

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
        request = InfrastructureInventoryRequest(
            repository_url=repository_url,
            environment_name=environment_name,
            inventory_id=inventory_id,
            include_compliance=include_compliance,
            include_costs=include_costs,
        )
        response = await infrastructure_service.get_inventory(
            request,
            api_key=api_key,
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
            "Invalid request for infrastructure inventory: %s | Request-ID: %s",
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
            "MongoDB connection error getting infrastructure inventory: %s | Request-ID: %s",
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
        logger.error(
            "Error getting infrastructure inventory: %s | Request-ID: %s",
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


@router.post(
    "/manage",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Manage infrastructure",
    description="Manage infrastructure lifecycle (create, update, upgrade, backup, restore, monitor, optimize)",
)
async def manage_infrastructure(
    request: InfrastructureManageRequest,
    http_request: Request,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Manage infrastructure lifecycle.

    Args:
        request: Infrastructure management request
        http_request: FastAPI request object for accessing request ID

    Returns:
        API response with infrastructure management result
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
        response = await infrastructure_service.manage_infrastructure(
            request,
            api_key=api_key,
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
            "Invalid request for infrastructure management: %s | Request-ID: %s",
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
            "MongoDB connection error managing infrastructure: %s | Request-ID: %s",
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
        logger.error(
            "Error managing infrastructure: %s | Request-ID: %s",
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

