"""Early request logging middleware - logs ALL requests before CORS middleware."""

import logging
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("api.middleware.early_logging")


class EarlyLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs all incoming requests before any other processing.
    
    This is placed BEFORE CORS middleware to catch requests that might be blocked.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Log request before any processing.
        
        Args:
            request: FastAPI request object
            call_next: Next middleware/handler
            
        Returns:
            Response object
        """
        logger.info(
            "EARLY LOG: Request received: %s %s | Origin: %s | Cookie: %s | Headers: %s",
            request.method,
            request.url.path,
            request.headers.get("origin", "none"),
            "present" if request.cookies.get("auth_token") else "none",
            list(request.headers.keys())[:5],
        )
        
        try:
            response = await call_next(request)
            logger.info(
                "EARLY LOG: Request processed: %s %s | Status: %s",
                request.method,
                request.url.path,
                response.status_code,
            )
            return response
        except Exception as e:
            logger.error(
                "EARLY LOG: Request failed: %s %s | Error: %s",
                request.method,
                request.url.path,
                str(e),
                exc_info=True,
            )
            raise

