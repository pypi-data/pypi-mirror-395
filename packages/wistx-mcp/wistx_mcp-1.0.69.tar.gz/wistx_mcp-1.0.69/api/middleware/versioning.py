"""API versioning middleware for version negotiation and deprecation."""

import logging
from typing import Callable

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from api.config import settings
from api.services.version_tracking_service import version_tracking_service

logger = logging.getLogger(__name__)

SUPPORTED_VERSIONS = ["v1"]
CURRENT_VERSION = "v1"
DEPRECATED_VERSIONS: dict[str, dict[str, str]] = {}


class VersioningMiddleware(BaseHTTPMiddleware):
    """Middleware for API version negotiation and deprecation warnings."""

    def __init__(self, app):
        """Initialize versioning middleware.

        Args:
            app: ASGI application
        """
        super().__init__(app)
        self.supported_versions = SUPPORTED_VERSIONS
        self.current_version = CURRENT_VERSION
        self.deprecated_versions = DEPRECATED_VERSIONS

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and handle version negotiation.

        Args:
            request: FastAPI request object
            call_next: Next middleware/handler

        Returns:
            Response object with version headers
        """
        version = self._extract_version(request)

        if version and version not in self.supported_versions:
            return Response(
                content=f"API version '{version}' is not supported. Supported versions: {', '.join(self.supported_versions)}",
                status_code=status.HTTP_400_BAD_REQUEST,
                headers={
                    "X-API-Version": self.current_version,
                    "X-Supported-Versions": ", ".join(self.supported_versions),
                },
            )

        response = await call_next(request)

        api_version = version or self.current_version
        response.headers["X-API-Version"] = api_version
        response.headers["X-Current-Version"] = self.current_version
        response.headers["X-Supported-Versions"] = ", ".join(self.supported_versions)

        if version and version in self.deprecated_versions:
            deprecation_info = self.deprecated_versions[version]
            response.headers["X-API-Deprecated"] = "true"
            response.headers["X-API-Deprecation-Date"] = deprecation_info.get("deprecation_date", "")
            response.headers["X-API-Sunset-Date"] = deprecation_info.get("sunset_date", "")
            response.headers["X-API-Migration-Guide"] = deprecation_info.get("migration_guide", "")

            logger.warning(
                "Deprecated API version used: %s [path=%s, deprecation_date=%s]",
                version,
                request.url.path,
                deprecation_info.get("deprecation_date"),
            )

        user_info = getattr(request.state, "user_info", None)
        user_id = user_info.get("user_id") if user_info else None
        api_key_id = user_info.get("api_key_id") if user_info else None

        try:
            version_tracking_service.track_api_version_usage(
                version=api_version,
                endpoint=request.url.path,
                user_id=user_id,
                api_key_id=api_key_id,
            )
        except Exception as e:
            logger.debug("Failed to track API version usage: %s", e)

        return response

    def _extract_version(self, request: Request) -> str | None:
        """Extract API version from request.

        Checks in order:
        1. URL path (/v1/...)
        2. X-API-Version header
        3. Accept header (application/vnd.wistx.v1+json)

        Args:
            request: Request object

        Returns:
            Version string or None
        """
        path = request.url.path

        if path.startswith("/v"):
            parts = path.split("/")
            if len(parts) > 1 and parts[1].startswith("v"):
                return parts[1]

        version_header = request.headers.get("X-API-Version")
        if version_header:
            return version_header

        accept_header = request.headers.get("Accept", "")
        if "application/vnd.wistx." in accept_header:
            for version in self.supported_versions:
                if f"application/vnd.wistx.{version}+json" in accept_header:
                    return version

        return None

