"""Search endpoints for v1 API."""

import logging
import time
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status

from api.models.v1_requests import (
    CodebaseSearchRequest,
    PackageSearchRequest,
    RegexSearchRequest,
    WebSearchRequest,
    ReadPackageFileRequest,
)
from api.models.v1_responses import APIResponse, ErrorResponse
from api.services.search_service import SearchService
from api.services.exceptions import QuotaExceededError
from api.services.quota_service import quota_service
from api.database.exceptions import MongoDBConnectionError
from api.dependencies import get_current_user
from api.dependencies.plan_enforcement import require_query_quota

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/search", tags=["search"])

search_service = SearchService()


@router.post(
    "/codebase",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Search codebase",
    description="Search user's indexed repositories, documentation, and documents",
)
async def search_codebase(
    request: CodebaseSearchRequest,
    http_request: Request,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Search user's indexed codebase.

    Args:
        request: Codebase search request
        http_request: FastAPI request object for accessing request ID

    Returns:
        API response with search results
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
        response = await search_service.search_codebase(
            request,
            user_id=user_id,
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
            "Invalid request for codebase search: %s | Request-ID: %s",
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
            "MongoDB connection error searching codebase: %s | Request-ID: %s",
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
            "Error searching codebase: %s | Request-ID: %s",
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
    "/packages",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Search packages",
    description="Search DevOps/infrastructure packages across registries",
)
async def search_packages(
    request: PackageSearchRequest,
    http_request: Request,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Search DevOps/infrastructure packages.

    Args:
        request: Package search request
        http_request: FastAPI request object for accessing request ID

    Returns:
        API response with package search results
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
        response = await search_service.search_packages(
            request,
            user_id=user_id,
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
            "Invalid request for package search: %s | Request-ID: %s",
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
            "MongoDB connection error searching packages: %s | Request-ID: %s",
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
            "Invalid request for package search: %s | Request-ID: %s",
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
    except Exception as e:
        logger.error(
            "Error searching packages: %s | Request-ID: %s",
            e,
            request_id,
            exc_info=True,
        )
        error_response = ErrorResponse(
            error={
                "code": "INTERNAL_ERROR",
                "message": f"An unexpected error occurred: {str(e)}",
                "details": str(e),
                "error_type": type(e).__name__,
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
    "/regex",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Regex search codebase",
    description="Search user's indexed codebase using regex patterns",
)
async def regex_search(
    request: RegexSearchRequest,
    http_request: Request,
    current_user: dict[str, Any] = Depends(require_query_quota),
) -> APIResponse:
    """Search codebase using regex patterns."""
    request_id = getattr(http_request.state, "request_id", "")
    start_time = time.time()

    user_id = current_user.get("user_id")
    authorization = http_request.headers.get("Authorization", "")
    api_key = authorization.replace("Bearer ", "").strip() if authorization.startswith("Bearer ") else ""

    try:
        from wistx_mcp.tools.regex_search import regex_search_codebase

        response = await regex_search_codebase(
            pattern=request.pattern,
            api_key=api_key,
            repositories=request.repositories,
            resource_ids=request.resource_ids,
            resource_types=request.resource_types,
            file_types=request.file_types,
            code_type=request.code_type,
            cloud_provider=request.cloud_provider,
            template=request.template,
            case_sensitive=request.case_sensitive,
            multiline=request.multiline,
            dotall=request.dotall,
            include_context=request.include_context,
            context_lines=request.context_lines,
            limit=request.limit,
            timeout=request.timeout,
        )
        query_time_ms = int((time.time() - start_time) * 1000)

        return APIResponse(
            data=response,
            metadata={
                "request_id": request_id,
                "timestamp": time.time(),
                "query_time_ms": query_time_ms,
            },
        )
    except ValueError as e:
        logger.warning("Invalid request for regex search: %s | Request-ID: %s", e, request_id)
        error_response = ErrorResponse(
            error={"code": "VALIDATION_ERROR", "message": "Invalid request parameters", "details": str(e)},
            metadata={"request_id": request_id, "timestamp": time.time()},
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_response.model_dump()) from e
    except Exception as e:
        logger.error("Error in regex search: %s | Request-ID: %s", e, request_id, exc_info=True)
        error_response = ErrorResponse(
            error={"code": "INTERNAL_ERROR", "message": "An unexpected error occurred", "details": str(e)},
            metadata={"request_id": request_id, "timestamp": time.time()},
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_response.model_dump()) from e


@router.post(
    "/web",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Web search",
    description="Search the web for DevOps/infrastructure/compliance/FinOps/SRE information",
)
async def web_search(
    request: WebSearchRequest,
    http_request: Request,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Search the web for DevOps/infrastructure information."""
    request_id = getattr(http_request.state, "request_id", "")
    start_time = time.time()

    user_id = current_user.get("user_id")
    plan = current_user.get("plan", "professional")
    authorization = http_request.headers.get("Authorization", "")
    api_key = authorization.replace("Bearer ", "").strip() if authorization.startswith("Bearer ") else ""

    try:
        await quota_service.check_query_quota(user_id, plan)
    except QuotaExceededError as e:
        logger.warning("Query quota exceeded for user %s: %s | Request-ID: %s", user_id, e, request_id)
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
            metadata={"request_id": request_id, "timestamp": time.time()},
        )
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=error_response.model_dump()) from e

    try:
        from wistx_mcp.tools.web_search import web_search

        response = await web_search(
            query=request.query,
            search_type=request.search_type,
            resource_type=request.resource_type,
            cloud_provider=request.cloud_provider,
            severity=request.severity,
            include_cves=request.include_cves,
            include_advisories=request.include_advisories,
            limit=request.limit,
            api_key=api_key,
        )
        query_time_ms = int((time.time() - start_time) * 1000)

        return APIResponse(
            data=response,
            metadata={
                "request_id": request_id,
                "timestamp": time.time(),
                "query_time_ms": query_time_ms,
            },
        )
    except ValueError as e:
        logger.warning("Invalid request for web search: %s | Request-ID: %s", e, request_id)
        error_response = ErrorResponse(
            error={"code": "VALIDATION_ERROR", "message": "Invalid request parameters", "details": str(e)},
            metadata={"request_id": request_id, "timestamp": time.time()},
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_response.model_dump()) from e
    except Exception as e:
        logger.error("Error in web search: %s | Request-ID: %s", e, request_id, exc_info=True)
        error_response = ErrorResponse(
            error={"code": "INTERNAL_ERROR", "message": "An unexpected error occurred", "details": str(e)},
            metadata={"request_id": request_id, "timestamp": time.time()},
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_response.model_dump()) from e


@router.post(
    "/packages/read-file",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Read package file",
    description="Read specific file sections from package source code using SHA256 hash",
)
async def read_package_file(
    request: ReadPackageFileRequest,
    http_request: Request,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Read specific file sections from package source code."""
    request_id = getattr(http_request.state, "request_id", "")
    start_time = time.time()

    try:
        from wistx_mcp.tools.lib.package_read_file import read_package_file

        response = await read_package_file(
            registry=request.registry,
            package_name=request.package_name,
            filename_sha256=request.filename_sha256,
            start_line=request.start_line,
            end_line=request.end_line,
            version=request.version,
        )
        query_time_ms = int((time.time() - start_time) * 1000)

        return APIResponse(
            data=response,
            metadata={
                "request_id": request_id,
                "timestamp": time.time(),
                "query_time_ms": query_time_ms,
            },
        )
    except ValueError as e:
        logger.warning("Invalid request for read package file: %s | Request-ID: %s", e, request_id)
        error_response = ErrorResponse(
            error={"code": "VALIDATION_ERROR", "message": "Invalid request parameters", "details": str(e)},
            metadata={"request_id": request_id, "timestamp": time.time()},
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_response.model_dump()) from e
    except Exception as e:
        logger.error("Error reading package file: %s | Request-ID: %s", e, request_id, exc_info=True)
        error_response = ErrorResponse(
            error={"code": "INTERNAL_ERROR", "message": "An unexpected error occurred", "details": str(e)},
            metadata={"request_id": request_id, "timestamp": time.time()},
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_response.model_dump()) from e
