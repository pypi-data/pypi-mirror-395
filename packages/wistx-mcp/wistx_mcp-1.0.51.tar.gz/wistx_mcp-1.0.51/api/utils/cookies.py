"""Cookie utilities for authentication tokens."""

import logging
from fastapi import Response

from api.config import settings
from api.utils.domain_config import get_cookie_domain

logger = logging.getLogger(__name__)

COOKIE_NAME = "auth_token"
REFRESH_COOKIE_NAME = "refresh_token"
COOKIE_MAX_AGE = 60 * 60 * 24 * 7
COOKIE_PATH = "/"
MAX_TOKEN_SIZE = 3500


def validate_token_size(token: str) -> None:
    """Validate token size fits in cookie.
    
    Args:
        token: JWT token string
        
    Raises:
        ValueError: If token is too large for cookie
    """
    token_size = len(token)
    if token_size > MAX_TOKEN_SIZE:
        logger.error(
            "Token size (%d bytes) exceeds cookie limit (%d bytes)",
            token_size,
            MAX_TOKEN_SIZE,
        )
        raise ValueError(
            f"Token size ({token_size} bytes) exceeds cookie limit ({MAX_TOKEN_SIZE} bytes). "
            "Consider reducing token payload or using token references."
        )
    
    if token_size > 3000:
        logger.warning(
            "Token size (%d bytes) is approaching cookie limit. Monitor closely.",
            token_size,
        )


def set_auth_cookie(
    response: Response,
    token: str,
    max_age: int = COOKIE_MAX_AGE,
    domain: str | None = None,
    cookie_name: str = COOKIE_NAME,
) -> None:
    """Set authentication token as httpOnly cookie.
    
    In development (localhost), sets cookie without domain so it's accessible
    to the frontend after redirect. In production, uses proper domain configuration.
    
    Args:
        response: FastAPI Response object
        token: JWT token string
        max_age: Cookie max age in seconds (default: 7 days)
        domain: Cookie domain (None for same-domain, '.wistx.ai' for subdomains).
                If None, will auto-detect from settings.
        cookie_name: Name of the cookie (default: 'auth_token')
    """
    validate_token_size(token)
    
    if domain is None:
        domain = get_cookie_domain()
    
    if settings.debug:
        # In development, use 'lax' instead of 'none' because 'none' requires secure=True
        # 'lax' works fine for same-site requests (localhost:3000 -> localhost:3000/api/proxy)
        cookie_kwargs = {
            "key": cookie_name,
            "value": token,
            "max_age": max_age,
            "httponly": True,
            "secure": False,
            "samesite": "lax",  # Changed from "none" to "lax" for development
            "path": COOKIE_PATH,
        }
        if domain:
            cookie_kwargs["domain"] = domain
    else:
        cookie_kwargs = {
            "key": cookie_name,
            "value": token,
            "max_age": max_age,
            "httponly": True,
            "secure": True,
            "samesite": "lax",
            "path": COOKIE_PATH,
        }
        if domain:
            cookie_kwargs["domain"] = domain
    
    response.set_cookie(**cookie_kwargs)
    
    logger.info(
        "Set auth cookie: name=%s, domain=%s, max_age=%d, samesite=%s, secure=%s, httponly=%s",
        cookie_name,
        domain or "same-domain",
        max_age,
        cookie_kwargs["samesite"],
        cookie_kwargs["secure"],
        cookie_kwargs["httponly"],
    )
    
    set_cookie_header = response.headers.get("set-cookie")
    if set_cookie_header:
        logger.debug("Set-Cookie header value: %s", set_cookie_header)
    else:
        logger.warning("Set-Cookie header not found in response headers")


def clear_auth_cookie(
    response: Response,
    domain: str | None = None,
    cookie_name: str = COOKIE_NAME,
) -> None:
    """Clear authentication cookie.
    
    In development (localhost), clears cookie for both possible domains
    (no domain and explicit localhost) to handle cross-origin scenarios.
    
    In production, clears cookie for both domain version (.wistx.ai) and
    no-domain version (wistx.ai) because the proxy may have set it without
    domain attribute.
    
    Args:
        response: FastAPI Response object
        domain: Cookie domain (must match domain used when setting).
                If None, will auto-detect from settings.
        cookie_name: Name of the cookie (default: 'auth_token')
    """
    if domain is None:
        domain = get_cookie_domain()
    
    if settings.debug:
        samesite_value = "lax"
        secure_value = False
    else:
        samesite_value = "lax"
        secure_value = True

    delete_kwargs = {
        "key": cookie_name,
        "path": COOKIE_PATH,
        "samesite": samesite_value,
        "secure": secure_value,
        "httponly": True,
    }

    if domain and not settings.debug:
        delete_kwargs_no_domain = {
            "key": cookie_name,
            "path": COOKIE_PATH,
            "samesite": samesite_value,
            "secure": secure_value,
            "httponly": True,
        }
        response.delete_cookie(**delete_kwargs_no_domain)
        logger.debug(
            "Cleared auth cookie (no-domain): name=%s, path=%s, samesite=%s, secure=%s",
            cookie_name,
            COOKIE_PATH,
            samesite_value,
            secure_value,
        )
        
        delete_kwargs_with_domain = {
            "key": cookie_name,
            "path": COOKIE_PATH,
            "domain": domain,
            "samesite": samesite_value,
            "secure": secure_value,
            "httponly": True,
        }
        response.delete_cookie(**delete_kwargs_with_domain)
        logger.debug(
            "Cleared auth cookie (with-domain): name=%s, domain=%s, path=%s, samesite=%s, secure=%s",
            cookie_name,
            domain,
            COOKIE_PATH,
            samesite_value,
            secure_value,
        )
    else:
        response.delete_cookie(**delete_kwargs)
        logger.debug(
            "Cleared auth cookie: name=%s, domain=%s",
            cookie_name,
            domain or "same-domain",
        )

    if settings.debug:
        delete_kwargs_no_domain = {
            "key": cookie_name,
            "path": COOKIE_PATH,
            "samesite": samesite_value,
            "secure": False,
            "httponly": True,
        }
        response.delete_cookie(**delete_kwargs_no_domain)

        delete_kwargs_localhost = {
            "key": cookie_name,
            "path": COOKIE_PATH,
            "domain": "localhost",
            "samesite": samesite_value,
            "secure": False,
            "httponly": True,
        }
        response.delete_cookie(**delete_kwargs_localhost)

        delete_kwargs_127 = {
            "key": cookie_name,
            "path": COOKIE_PATH,
            "domain": "127.0.0.1",
            "samesite": samesite_value,
            "secure": False,
            "httponly": True,
        }
        response.delete_cookie(**delete_kwargs_127)


def get_auth_token_from_cookie(request) -> str | None:
    """Get authentication token from cookie.
    
    Args:
        request: FastAPI Request object
        
    Returns:
        Token string or None if not found
    """
    return request.cookies.get(COOKIE_NAME)


def get_refresh_token_from_cookie(request) -> str | None:
    """Get refresh token from cookie.
    
    Args:
        request: FastAPI Request object
        
    Returns:
        Refresh token string or None if not found
    """
    return request.cookies.get(REFRESH_COOKIE_NAME)


def set_auth_cookie_safe(
    response: Response,
    token: str,
    max_age: int = COOKIE_MAX_AGE,
    domain: str | None = None,
    fallback_to_header: bool = True,
    cookie_name: str = COOKIE_NAME,
) -> tuple[bool, str | None]:
    """Safely set auth cookie with fallback.
    
    Args:
        response: FastAPI Response object
        token: JWT token string
        max_age: Cookie max age in seconds
        domain: Cookie domain
        fallback_to_header: If True, return token for header fallback on failure
        cookie_name: Name of the cookie
        
    Returns:
        Tuple of (success, fallback_token).
        If cookie setting fails and fallback_to_header=True, returns token for header.
    """
    try:
        set_auth_cookie(response, token, max_age, domain, cookie_name)
        return True, None
    except ValueError as e:
        logger.error("Failed to set auth cookie (token too large): %s", e)
        if fallback_to_header:
            return False, token
        raise
    except Exception as e:
        logger.warning("Failed to set auth cookie: %s", e, exc_info=True)
        if fallback_to_header:
            return False, token
        raise

