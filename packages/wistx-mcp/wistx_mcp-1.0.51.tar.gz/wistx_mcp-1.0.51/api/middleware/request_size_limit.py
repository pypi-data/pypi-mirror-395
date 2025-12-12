"""Request size limit middleware for FastAPI.

Prevents DoS attacks by limiting request body size.
"""

import logging
from typing import Callable

from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from api.config import settings

logger = logging.getLogger(__name__)


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to limit request body size.

    Prevents DoS attacks by rejecting requests that exceed size limits.
    """

    MAX_REQUEST_SIZE = getattr(settings, "max_request_size_mb", 10) * 1024 * 1024
    EXCLUDED_PATHS = {
        "/health",
        "/docs",
        "/redoc",
        "/openapi.json",
    }

    def __init__(self, app, max_request_size_mb: int = 10):
        """Initialize request size limit middleware.

        Args:
            app: ASGI application
            max_request_size_mb: Maximum request size in MB (default: 10)
        """
        super().__init__(app)
        self.max_request_size = max_request_size_mb * 1024 * 1024

    def _is_excluded_path(self, path: str) -> bool:
        """Check if path is excluded from size limits.

        Args:
            path: Request path

        Returns:
            True if path is excluded, False otherwise
        """
        return any(path.startswith(excluded) for excluded in self.EXCLUDED_PATHS)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and check size limits.

        Args:
            request: FastAPI request object
            call_next: Next middleware/handler

        Returns:
            Response object

        Raises:
            HTTPException: If request exceeds size limit
        """
        if self._is_excluded_path(request.url.path):
            return await call_next(request)

        content_length = request.headers.get("content-length")
        if content_length:
            try:
                size = int(content_length)
                if size > self.max_request_size:
                    logger.warning(
                        "Request rejected: size %d bytes exceeds limit %d bytes (path: %s)",
                        size,
                        self.max_request_size,
                        request.url.path,
                    )
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"Request too large: {size / 1024 / 1024:.2f} MB exceeds "
                               f"limit of {self.max_request_size / 1024 / 1024:.2f} MB",
                    )
            except ValueError:
                logger.warning("Invalid content-length header: %s", content_length)

        response = await call_next(request)
        return response

