"""Usage tracking middleware for API requests."""

import logging
import secrets
import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from api.models.usage import APIUsageRequest, PerformanceMetrics
from api.services.usage_tracker import usage_tracker

logger = logging.getLogger(__name__)


class UsageTrackingMiddleware(BaseHTTPMiddleware):
    """Middleware to track API usage (queries, indexes, etc.)."""

    def _get_operation_type(self, endpoint: str, method: str) -> str:
        """Determine operation type from endpoint.

        Args:
            endpoint: API endpoint
            method: HTTP method

        Returns:
            Operation type: query, index, or other
        """
        query_endpoints = [
            "/v1/compliance",
            "/v1/knowledge",
            "/v1/pricing",
            "/v1/code-examples",
            "/v1/search",
            "/v1/troubleshoot",
            "/v1/architecture",
            "/v1/infrastructure",
            "/v1/reports/generate",
        ]

        if any(endpoint.startswith(ep) for ep in query_endpoints):
            return "query"
        elif endpoint.startswith("/v1/indexing"):
            indexing_endpoints = [
                "/v1/indexing/repositories",
                "/v1/indexing/documentation",
                "/v1/indexing/documents",
            ]
            reindex_pattern = "/v1/indexing/resources/"
            if method == "POST" and (
                endpoint in indexing_endpoints
                or (endpoint.startswith(reindex_pattern) and endpoint.endswith("/reindex"))
            ):
                return "index"
            return "other"
        return "other"

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Track usage for request/response.

        Args:
            request: FastAPI request object
            call_next: Next middleware/handler

        Returns:
            Response object
        """
        if request.url.path.startswith("/health") or request.url.path.startswith("/docs"):
            return await call_next(request)

        start_time = time.time()
        request_id = f"req_{secrets.token_hex(12)}"

        authorization = request.headers.get("authorization", "")
        if not authorization or not authorization.startswith("Bearer "):
            return await call_next(request)

        from api.auth.api_keys import get_user_from_api_key

        api_key_value = authorization.replace("Bearer ", "").strip()
        user_info = await get_user_from_api_key(api_key_value)

        if not user_info:
            return await call_next(request)

        request.state.user_info = user_info

        response = await call_next(request)

        try:
            total_time_ms = int((time.time() - start_time) * 1000)
            performance = PerformanceMetrics(total_time_ms=total_time_ms)

            operation_type = self._get_operation_type(request.url.path, request.method)

            operation_details = {}
            if operation_type == "query":
                operation_details = {
                    "endpoint": request.url.path,
                    "query_params": str(request.query_params) if request.query_params else None,
                }
            elif operation_type == "index":
                try:
                    if hasattr(response, "body") and response.body:
                        import json
                        body = json.loads(response.body.decode("utf-8"))
                        if isinstance(body, dict) and "data" in body:
                            data = body["data"]
                            operation_details = {
                                "resource_id": data.get("resource_id"),
                                "index_type": data.get("index_type"),
                                "documents_count": data.get("documents_count", 0),
                                "storage_mb": data.get("storage_mb", 0.0),
                            }
                except Exception:
                    pass

            usage_request = APIUsageRequest(
                request_id=request_id,
                user_id=user_info.get("user_id", ""),
                api_key_id=user_info.get("api_key_id", ""),
                organization_id=user_info.get("organization_id"),
                plan=user_info.get("plan", "professional"),
                endpoint=request.url.path,
                method=request.method,
                operation_type=operation_type,
                operation_details=operation_details,
                performance=performance,
                status_code=response.status_code,
                success=200 <= response.status_code < 400,
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent"),
            )

            await usage_tracker.track_request(usage_request)

        except Exception as e:
            logger.error("Failed to track usage: %s", e, exc_info=True)

        return response
