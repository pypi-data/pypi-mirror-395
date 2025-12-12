"""CORS middleware for FastAPI."""

import logging

from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp

from api.config import settings

logger = logging.getLogger(__name__)


def setup_cors_middleware(app: ASGIApp) -> None:
    """Setup CORS middleware.

    Args:
        app: FastAPI application
    """
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
        "https://app.wistx.ai",
        "https://wistx.ai",
    ]

    if settings.debug:
        allowed_origins.extend([
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3001",
            "http://127.0.0.1:8000",
        ])

    allowed_origins = list(set(allowed_origins))

    logger.info("Setting up CORS middleware with allowed origins: %s", allowed_origins)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "X-CSRF-Token",
            "X-Requested-With",
            "Accept",
            "Origin",
            "Access-Control-Request-Method",
            "Access-Control-Request-Headers",
        ],
        expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Window"],
        max_age=86400,
    )
