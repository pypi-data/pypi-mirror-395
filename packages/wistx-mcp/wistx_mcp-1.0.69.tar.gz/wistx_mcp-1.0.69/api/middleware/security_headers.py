"""Security headers middleware for production-grade HTTP security."""

import logging
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from api.config import settings

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add essential security headers to all responses.

    Implements OWASP recommended security headers:
    - Strict-Transport-Security (HSTS)
    - X-Content-Type-Options
    - X-Frame-Options
    - Content-Security-Policy
    - Referrer-Policy
    - Permissions-Policy
    - X-XSS-Protection (legacy, but still useful for older browsers)
    """

    def __init__(self, app):
        """Initialize security headers middleware.

        Args:
            app: ASGI application
        """
        super().__init__(app)
        
        # HSTS: Enforce HTTPS for 1 year, include subdomains
        # Only enable in production (when not in debug mode)
        self.hsts_value = "max-age=31536000; includeSubDomains; preload"
        
        # Prevent MIME type sniffing
        self.content_type_options = "nosniff"
        
        # Prevent clickjacking
        self.frame_options = "DENY"
        
        # XSS protection for legacy browsers
        self.xss_protection = "1; mode=block"
        
        # Referrer policy - send origin only for cross-origin requests
        self.referrer_policy = "strict-origin-when-cross-origin"
        
        # Permissions policy - disable unnecessary browser features
        self.permissions_policy = (
            "accelerometer=(), "
            "camera=(), "
            "geolocation=(), "
            "gyroscope=(), "
            "magnetometer=(), "
            "microphone=(), "
            "payment=(), "
            "usb=()"
        )
        
        # Content Security Policy
        # Restrictive by default, allows API responses
        self.csp_value = self._build_csp()

    def _build_csp(self) -> str:
        """Build Content-Security-Policy header value.

        Returns:
            CSP header value string
        """
        # For API backends, we primarily serve JSON responses
        # CSP is more relevant for HTML responses but still good practice
        directives = [
            "default-src 'none'",
            "frame-ancestors 'none'",
            "base-uri 'none'",
            "form-action 'none'",
        ]
        
        return "; ".join(directives)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Add security headers to response.

        Args:
            request: FastAPI request object
            call_next: Next middleware/handler

        Returns:
            Response with security headers
        """
        response = await call_next(request)
        
        # Add security headers
        # HSTS - only in production (non-debug mode) to avoid issues with local dev
        if not settings.debug:
            response.headers["Strict-Transport-Security"] = self.hsts_value
        
        response.headers["X-Content-Type-Options"] = self.content_type_options
        response.headers["X-Frame-Options"] = self.frame_options
        response.headers["X-XSS-Protection"] = self.xss_protection
        response.headers["Referrer-Policy"] = self.referrer_policy
        response.headers["Permissions-Policy"] = self.permissions_policy
        response.headers["Content-Security-Policy"] = self.csp_value
        
        # Cache control for API responses - prevent caching of sensitive data
        if "Cache-Control" not in response.headers:
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
        
        return response

