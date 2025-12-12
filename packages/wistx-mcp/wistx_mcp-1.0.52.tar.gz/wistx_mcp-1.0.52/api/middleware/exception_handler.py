"""Global exception handler."""

import logging
import uuid
from typing import Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from api.exceptions import (
    WISTXError,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    RateLimitError,
)

logger = logging.getLogger(__name__)


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to handle exceptions globally."""

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

        except WISTXError as e:
            logger.error(
                "WISTX error [correlation_id=%s]: %s",
                e.correlation_id,
                e,
                exc_info=True
            )

            status_code = self._get_status_code(e)
            return JSONResponse(
                status_code=status_code,
                content=e.to_dict(),
                headers={"X-Correlation-ID": e.correlation_id}
            )

        except Exception as e:
            correlation_id = str(uuid.uuid4())
            logger.error(
                "Unexpected error [correlation_id=%s]: %s",
                correlation_id,
                e,
                exc_info=True
            )

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "InternalServerError",
                    "message": "An internal error occurred",
                    "correlation_id": correlation_id,
                    "details": {},
                },
                headers={"X-Correlation-ID": correlation_id}
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
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

