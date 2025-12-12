"""Domain configuration utilities for cookie-based authentication."""

import logging
from urllib.parse import urlparse

from api.config import settings

logger = logging.getLogger(__name__)


def get_cookie_domain() -> str | None:
    """Get cookie domain based on environment.
    
    Architecture:
    - Development: localhost:3000 (frontend) ↔ localhost:8000 (backend) → None (no domain)
    - Production: wistx.ai (frontend) ↔ api.wistx.ai (backend) → .wistx.ai (cross-subdomain)
    
    Returns:
        Cookie domain string (e.g., '.wistx.ai') or None for same-domain.
        None means cookies will be set for the exact domain only (works for same-domain setup).
        '.wistx.ai' means cookies work across subdomains (e.g., wistx.ai ↔ api.wistx.ai).
    """
    if settings.debug:
        logger.debug("Development mode: Not setting cookie domain (browser will set for exact origin). Proxy will handle cross-port cookie forwarding.")
        return None

    frontend_url = settings.oauth_frontend_redirect_url_prod
    backend_url = settings.oauth_backend_callback_url_prod
    
    frontend_parsed = urlparse(frontend_url)
    backend_parsed = urlparse(backend_url)
    
    frontend_domain = frontend_parsed.netloc
    backend_domain = backend_parsed.netloc
    
    if frontend_domain == backend_domain:
        logger.debug(
            "Frontend and backend on same domain (%s). Using same-domain cookies (no domain specified).",
            frontend_domain,
        )
        return None
    
    frontend_base = ".".join(frontend_domain.split(".")[-2:])
    backend_base = ".".join(backend_domain.split(".")[-2:])
    
    if frontend_base != backend_base:
        logger.warning(
            "Frontend and backend are on different base domains: %s vs %s. "
            "Cookies may not work. Consider using subdomain cookies or same-domain setup.",
            frontend_base,
            backend_base,
        )
        return None
    
    if frontend_base == backend_base:
        logger.info(
            "Frontend (%s) and backend (%s) share base domain %s. "
            "Using cross-subdomain cookies (domain=.%s) to allow cookies across subdomains.",
            frontend_domain,
            backend_domain,
            frontend_base,
            frontend_base,
        )
        return f".{frontend_base}"
    
    return None


def should_use_subdomain_cookies() -> bool:
    """Check if subdomain cookies should be used.
    
    Returns:
        True if frontend and backend are on different subdomains of the same domain.
    """
    if settings.debug:
        return False
    
    frontend_url = settings.oauth_frontend_redirect_url_prod
    backend_url = settings.oauth_backend_callback_url_prod
    
    frontend_parsed = urlparse(frontend_url)
    backend_parsed = urlparse(backend_url)
    
    frontend_domain = frontend_parsed.netloc
    backend_domain = backend_parsed.netloc
    
    if frontend_domain == backend_domain:
        return False
    
    frontend_base = ".".join(frontend_domain.split(".")[-2:])
    backend_base = ".".join(backend_domain.split(".")[-2:])
    
    return frontend_base == backend_base


def get_frontend_domain() -> str:
    """Get frontend domain for cookie configuration.
    
    Returns:
        Frontend domain string
    """
    frontend_url = settings.oauth_frontend_redirect_url_prod
    parsed = urlparse(frontend_url)
    return parsed.netloc


def get_backend_domain() -> str:
    """Get backend domain for cookie configuration.
    
    Returns:
        Backend domain string
    """
    backend_url = settings.oauth_backend_callback_url_prod
    parsed = urlparse(backend_url)
    return parsed.netloc

