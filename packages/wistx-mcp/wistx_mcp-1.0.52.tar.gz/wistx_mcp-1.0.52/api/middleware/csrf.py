"""CSRF protection middleware using Double Submit Cookie pattern."""

import logging
from typing import Callable

from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from api.utils.csrf import (
    validate_csrf_token,
    is_state_changing_method,
    CSRF_COOKIE_NAME,
    CSRF_HEADER_NAME,
)
from api.config import settings

logger = logging.getLogger(__name__)


class CSRFProtectionMiddleware(BaseHTTPMiddleware):
    """CSRF protection middleware using Double Submit Cookie pattern.

    Validates CSRF tokens for state-changing HTTP methods (POST, PUT, PATCH, DELETE).
    Compares X-CSRF-Token header to csrf_token cookie value.

    Exemptions:
    - Safe methods (GET, HEAD, OPTIONS)
    - Health check endpoints
    - CSRF token endpoint itself
    - OAuth callback endpoints (handled separately)
    - Waitlist signup endpoint (public, unauthenticated)
    - API key authenticated requests (API keys use Authorization headers, not cookies, so not vulnerable to CSRF)
    """

    def __init__(self, app):
        """Initialize CSRF protection middleware.

        Args:
            app: ASGI application
        """
        super().__init__(app)
        self.excluded_paths = {
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/v1/csrf-token",
            "/v1/auth/sync",
            "/v1/auth/refresh",  # Token refresh endpoint
            "/auth/",
            "/v1/waitlist/signup",  # Public waitlist signup (no auth required)
        }

    def _is_excluded_path(self, path: str) -> bool:
        """Check if path is excluded from CSRF protection.
        
        Args:
            path: Request path
            
        Returns:
            True if path is excluded, False otherwise
        """
        return any(path.startswith(excluded) for excluded in self.excluded_paths)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and validate CSRF token.

        Args:
            request: FastAPI request object
            call_next: Next middleware/handler

        Returns:
            Response object

        Raises:
            HTTPException: If CSRF token is missing or invalid
        """
        # Skip CSRF protection only if explicitly disabled via DISABLE_CSRF_PROTECTION env var
        # Note: This is decoupled from DEBUG mode to ensure CSRF protection stays enabled
        # in production even if DEBUG is accidentally left on
        if settings.disable_csrf_protection:
            logger.debug("CSRF protection explicitly disabled via DISABLE_CSRF_PROTECTION")
            return await call_next(request)

        if request.method == "OPTIONS":
            return await call_next(request)

        if self._is_excluded_path(request.url.path):
            return await call_next(request)

        if not is_state_changing_method(request.method):
            return await call_next(request)
        
        authorization = request.headers.get("authorization", "")
        if authorization and authorization.startswith("Bearer "):
            api_key_value = authorization.replace("Bearer ", "").strip()
            if api_key_value:
                user_info = getattr(request.state, "user_info", None)
                if user_info:
                    logger.debug(
                        "Skipping CSRF validation for API key authenticated request: path=%s, user_id=%s",
                        request.url.path,
                        user_info.get("user_id"),
                    )
                    return await call_next(request)
                elif api_key_value.startswith("wistx_") or len(api_key_value) > 20:
                    logger.debug(
                        "Skipping CSRF validation for API key request (format detected): path=%s",
                        request.url.path,
                    )
                    return await call_next(request)
        
        header_token = request.headers.get(CSRF_HEADER_NAME) or request.headers.get(
            CSRF_HEADER_NAME.lower()
        )
        cookie_token = request.cookies.get(CSRF_COOKIE_NAME)
        
        logger.info(
            "CSRF validation check: method=%s, path=%s, has_header=%s, has_cookie=%s",
            request.method,
            request.url.path,
            bool(header_token),
            bool(cookie_token),
        )
        
        if not validate_csrf_token(header_token, cookie_token):
            from api.models.audit_log import AuditEventType, AuditLogSeverity
            from api.services.audit_log_service import audit_log_service
            
            ip_address = request.client.host if request.client else None
            user_agent = request.headers.get("user-agent")
            request_id = getattr(request.state, "request_id", None)
            
            audit_log_service.log_event(
                event_type=AuditEventType.AUTHENTICATION_FAILURE,
                severity=AuditLogSeverity.HIGH,
                message="CSRF token validation failed",
                success=False,
                ip_address=ip_address,
                user_agent=user_agent,
                request_id=request_id,
                endpoint=request.url.path,
                method=request.method,
                details={
                    "reason": "CSRF token missing or invalid",
                    "has_header": bool(header_token),
                    "has_cookie": bool(cookie_token),
                    "path": request.url.path,
                },
                compliance_tags=["PCI-DSS-10", "SOC2"],
            )
            
            logger.warning(
                "CSRF validation failed: method=%s, path=%s, has_header=%s, has_cookie=%s",
                request.method,
                request.url.path,
                bool(header_token),
                bool(cookie_token),
            )
            
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF token missing or invalid",
                headers={"X-CSRF-Required": "true"},
            )
        
        logger.info(
            "CSRF validation successful: method=%s, path=%s",
            request.method,
            request.url.path,
        )
        
        return await call_next(request)

