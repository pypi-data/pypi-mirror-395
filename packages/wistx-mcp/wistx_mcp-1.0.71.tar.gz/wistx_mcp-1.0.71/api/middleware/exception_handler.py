"""Global exception handler."""

import logging
import uuid
from typing import Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from api.exceptions import (
    WISTXError,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    RateLimitError,
    ExternalServiceError,
)
from api.config import settings

logger = logging.getLogger(__name__)


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to handle exceptions globally."""

    def _get_cors_headers(self, request: Request) -> dict[str, str]:
        """Get CORS headers for the request origin.

        Args:
            request: FastAPI request

        Returns:
            Dictionary of CORS headers
        """
        origin = request.headers.get("origin")
        if not origin:
            return {}

        allowed_origins = [
            "http://localhost:3000",
            "http://localhost:3001",
            "http://localhost:8000",
            "https://app.wistx.ai",
            "https://wistx.ai",
            "https://www.wistx.ai",
        ]

        if settings.debug:
            allowed_origins.extend([
                "http://127.0.0.1:3000",
                "http://127.0.0.1:3001",
                "http://127.0.0.1:8000",
            ])

        if origin in allowed_origins:
            return {
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Expose-Headers": "X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Window, X-Correlation-ID",
            }

        return {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and handle exceptions.

        Args:
            request: FastAPI request
            call_next: Next middleware/handler

        Returns:
            Response object
        """
        try:
            response = await call_next(request)
            return response

        except StarletteHTTPException as e:
            logger.debug(
                "HTTPException caught in middleware: status=%s, detail=%s",
                e.status_code,
                e.detail,
            )
            headers = dict(e.headers) if e.headers else {}
            cors_headers = self._get_cors_headers(request)
            headers.update(cors_headers)
            
            if cors_headers:
                logger.debug(
                    "Added CORS headers to HTTPException response: %s",
                    cors_headers,
                )
            else:
                logger.warning(
                    "No CORS headers added for HTTPException. Origin: %s",
                    request.headers.get("origin", "none"),
                )
            
            content = {"detail": e.detail}
            if e.status_code == 422:
                content = {"detail": e.detail, "body": getattr(e, "body", None)}
            
            return JSONResponse(
                status_code=e.status_code,
                content=content,
                headers=headers,
            )

        except WISTXError as e:
            logger.error(
                "WISTX error [correlation_id=%s]: %s",
                e.correlation_id,
                e,
                exc_info=True
            )

            status_code = self._get_status_code(e)
            headers = {"X-Correlation-ID": e.correlation_id}
            cors_headers = self._get_cors_headers(request)
            headers.update(cors_headers)
            
            if cors_headers:
                logger.debug(
                    "Added CORS headers to error response: %s",
                    cors_headers,
                )
            else:
                logger.warning(
                    "No CORS headers added for origin: %s",
                    request.headers.get("origin", "none"),
                )

            return JSONResponse(
                status_code=status_code,
                content=e.to_dict(),
                headers=headers
            )

        except Exception as e:
            correlation_id = str(uuid.uuid4())
            logger.error(
                "Unexpected error [correlation_id=%s]: %s",
                correlation_id,
                e,
                exc_info=True
            )

            headers = {"X-Correlation-ID": correlation_id}
            headers.update(self._get_cors_headers(request))

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "InternalServerError",
                    "message": "An internal error occurred",
                    "correlation_id": correlation_id,
                    "details": {},
                },
                headers=headers
            )

    def _get_status_code(self, error: WISTXError) -> int:
        """Get HTTP status code for error.

        Args:
            error: WISTX error

        Returns:
            HTTP status code
        """
        if isinstance(error, ValidationError):
            return status.HTTP_400_BAD_REQUEST
        elif isinstance(error, AuthenticationError):
            return status.HTTP_401_UNAUTHORIZED
        elif isinstance(error, AuthorizationError):
            return status.HTTP_403_FORBIDDEN
        elif isinstance(error, NotFoundError):
            return status.HTTP_404_NOT_FOUND
        elif isinstance(error, RateLimitError):
            return status.HTTP_429_TOO_MANY_REQUESTS
        elif isinstance(error, ExternalServiceError):
            return status.HTTP_502_BAD_GATEWAY
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

