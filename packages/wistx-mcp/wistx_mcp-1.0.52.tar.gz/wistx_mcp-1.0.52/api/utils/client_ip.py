"""Utility functions for extracting real client IP addresses from requests.

Handles Cloudflare, load balancers, and other proxy scenarios.
"""

import logging
from fastapi import Request

logger = logging.getLogger(__name__)


def get_real_client_ip(request: Request) -> str:
    """Get real client IP address from request headers.

    Priority order:
    1. CF-Connecting-IP (Cloudflare)
    2. X-Forwarded-For (load balancers, proxies)
    3. X-Real-IP (nginx, other proxies)
    4. request.client.host (direct connection)

    Args:
        request: FastAPI request object

    Returns:
        Client IP address string, or "unknown" if not found
    """
    cf_ip = request.headers.get("CF-Connecting-IP")
    if cf_ip:
        return cf_ip.strip()

    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
        if ip:
            return ip

    x_real_ip = request.headers.get("X-Real-IP")
    if x_real_ip:
        return x_real_ip.strip()

    if request.client:
        return request.client.host

    return "unknown"


def is_cloudflare_request(request: Request) -> bool:
    """Check if request is coming through Cloudflare.

    Args:
        request: FastAPI request object

    Returns:
        True if request is proxied through Cloudflare, False otherwise
    """
    return "CF-Connecting-IP" in request.headers or "CF-Ray" in request.headers


def get_cloudflare_ray(request: Request) -> str | None:
    """Get Cloudflare Ray ID from request headers.

    Args:
        request: FastAPI request object

    Returns:
        Cloudflare Ray ID string, or None if not present
    """
    return request.headers.get("CF-Ray")

