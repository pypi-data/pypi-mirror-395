"""Error alerting middleware for critical errors."""

import logging
from typing import Callable

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from api.services.alerting_service import AlertingService, AlertLevel, AlertType

logger = logging.getLogger(__name__)

alerting_service = AlertingService()


class ErrorAlertingMiddleware(BaseHTTPMiddleware):
    """Middleware to alert on critical errors."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and alert on critical errors.

        Args:
            request: FastAPI request object
            call_next: Next middleware/handler

        Returns:
            Response object
        """
        try:
            response = await call_next(request)

            if response.status_code >= 500:
                await self._alert_server_error(request, response)

            return response

        except Exception as e:
            await self._alert_exception(request, e)
            raise

    async def _alert_server_error(self, request: Request, response: Response) -> None:
        """Alert on server errors (5xx).

        Args:
            request: Request object
            response: Response object
        """
        try:
            await alerting_service.create_alert(
                alert_type=AlertType.ERROR,
                level=AlertLevel.HIGH,
                title=f"Server Error: {response.status_code}",
                message=f"Server error on {request.method} {request.url.path}",
                metadata={
                    "status_code": response.status_code,
                    "method": request.method,
                    "path": str(request.url.path),
                    "query_params": str(request.url.query),
                },
            )
        except Exception as e:
            logger.error("Failed to create error alert: %s", e)

    async def _alert_exception(self, request: Request, exception: Exception) -> None:
        """Alert on unhandled exceptions.

        Args:
            request: Request object
            exception: Exception instance
        """
        try:
            await alerting_service.create_alert(
                alert_type=AlertType.ERROR,
                level=AlertLevel.CRITICAL,
                title="Unhandled Exception",
                message=f"Unhandled exception: {type(exception).__name__}: {str(exception)}",
                metadata={
                    "exception_type": type(exception).__name__,
                    "exception_message": str(exception),
                    "method": request.method,
                    "path": str(request.url.path),
                },
            )
        except Exception as e:
            logger.error("Failed to create exception alert: %s", e)

