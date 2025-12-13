"""Middleware to enforce HTTPS for production domains and fix redirect URLs."""

import logging
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse

from api.config import settings

logger = logging.getLogger(__name__)


class HTTPSEnforcementMiddleware(BaseHTTPMiddleware):
    """Middleware to enforce HTTPS for production domains.

    Fixes FastAPI redirects that incorrectly use HTTP instead of HTTPS
    when behind a proxy (e.g., Cloudflare).
    """

    PRODUCTION_DOMAINS = [
        "api.wistx.ai",
        "api.wistx.com",
        "wistx.ai",
        "wistx.com",
    ]

    def is_production_domain(self, hostname: str) -> bool:
        """Check if hostname is a production domain."""
        return any(domain in hostname for domain in self.PRODUCTION_DOMAINS)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and enforce HTTPS for production domains."""
        hostname = request.url.hostname or ""
        is_production = self.is_production_domain(hostname)

        if is_production:
            forwarded_proto = request.headers.get("X-Forwarded-Proto", "").lower()
            cf_visitor = request.headers.get("CF-Visitor", "").lower()
            forwarded_header = request.headers.get("Forwarded", "").lower()
            
            is_behind_proxy = bool(forwarded_proto or cf_visitor or forwarded_header)
            is_https_via_proxy = (
                forwarded_proto == "https"
                or '"scheme":"https"' in cf_visitor
                or 'proto=https' in forwarded_header
            )
            
            if is_https_via_proxy or (is_behind_proxy and request.url.scheme == "http"):
                request.scope["scheme"] = "https"
                if hasattr(request, "_url"):
                    request._url = request.url.replace(scheme="https")
            elif request.url.scheme == "http" and not is_behind_proxy:
                https_url = request.url.replace(scheme="https")
                logger.warning(
                    "Redirecting HTTP to HTTPS for production domain",
                    extra={
                        "original_url": str(request.url),
                        "redirect_url": str(https_url),
                        "hostname": hostname,
                        "x_forwarded_proto": forwarded_proto or "none",
                        "cf_visitor": cf_visitor or "none",
                    },
                )
                return RedirectResponse(url=str(https_url), status_code=301)
            else:
                request.scope["scheme"] = "https"
                if hasattr(request, "_url"):
                    request._url = request.url.replace(scheme="https")

        response = await call_next(request)

        if isinstance(response, RedirectResponse) and is_production:
            redirect_url = response.headers.get("location", "")
            if redirect_url.startswith("http://"):
                https_redirect_url = redirect_url.replace("http://", "https://", 1)
                response.headers["location"] = https_redirect_url
                logger.debug(
                    "Fixed redirect URL to use HTTPS",
                    extra={
                        "original": redirect_url,
                        "fixed": https_redirect_url,
                    },
                )

        return response

