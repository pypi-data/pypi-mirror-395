"""Production-ready request logging middleware for FastAPI."""

import logging
import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from api.config import settings
from api.utils.client_ip import get_real_client_ip

logger = logging.getLogger("api.middleware.logging")

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses.

    Logs:
    - Request method, path, query params
    - Request ID for tracing
    - Response status code
    - Processing time
    - Client IP address
    - User agent
    """

    def __init__(self, app: ASGIApp):
        """Initialize request logging middleware.

        Args:
            app: ASGI application
        """
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log details.

        Args:
            request: FastAPI request object
            call_next: Next middleware/handler

        Returns:
            Response object
        """
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start_time = time.time()
        method = request.method
        path = request.url.path
        query_params = dict(request.query_params)
        client_ip = get_real_client_ip(request)
        user_agent = request.headers.get("user-agent", "unknown")

        logger.info(
            "Request started: %s %s | Request-ID: %s | IP: %s | Query: %s | Origin: %s | Cookie: %s",
            method,
            path,
            request_id,
            client_ip,
            query_params if query_params else "{}",
            request.headers.get("origin", "none"),
            "present" if request.cookies.get("auth_token") else "none",
        )

        if settings.debug:
            logger.debug(
                "Request headers: %s | User-Agent: %s",
                dict(request.headers),
                user_agent,
            )

        try:
            response = await call_next(request)

            process_time = time.time() - start_time

            logger.info(
                "Request completed: %s %s | Status: %s | Time: %.3fs | Request-ID: %s",
                method,
                path,
                response.status_code,
                process_time,
                request_id,
            )

            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{process_time:.3f}"

            cors_headers = {
                k: v for k, v in response.headers.items()
                if k.lower().startswith("access-control-")
            }
            if cors_headers:
                logger.debug(
                    "Response CORS headers: %s",
                    ", ".join(f"{k}={v}" for k, v in cors_headers.items()),
                )
            else:
                logger.warning(
                    "Response missing CORS headers for origin: %s",
                    request.headers.get("origin", "none"),
                )

            return response

        except Exception as e:
            process_time = time.time() - start_time

            logger.error(
                "Request failed: %s %s | Error: %s | Time: %.3fs | Request-ID: %s",
                method,
                path,
                str(e),
                process_time,
                request_id,
                exc_info=settings.debug,
            )

            raise


def setup_logging_middleware(app: ASGIApp) -> None:
    """Set up logging middleware on FastAPI app.

    Args:
        app: FastAPI application instance
    """
    app.add_middleware(RequestLoggingMiddleware)
