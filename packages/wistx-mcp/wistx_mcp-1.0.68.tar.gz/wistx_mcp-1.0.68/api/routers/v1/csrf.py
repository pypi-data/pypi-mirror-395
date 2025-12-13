"""CSRF token endpoint for Double Submit Cookie pattern."""

import logging

from fastapi import APIRouter, Request, Response
from pydantic import BaseModel, Field

from api.utils.csrf import (
    generate_csrf_token,
    CSRF_COOKIE_NAME,
    CSRF_COOKIE_MAX_AGE,
    CSRF_COOKIE_PATH,
)
from api.utils.domain_config import get_cookie_domain
from api.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


class CSRFTokenResponse(BaseModel):
    """Response model for CSRF token."""

    token: str = Field(..., description="CSRF token (also set in cookie)")


@router.get("/csrf-token", response_model=CSRFTokenResponse)
async def get_csrf_token(
    request: Request, 
    response: Response,
    force: bool = False,
) -> CSRFTokenResponse:
    """Get CSRF token for Double Submit Cookie pattern.
    
    Returns existing token from cookie if present and force=False, otherwise generates a new one.
    This ensures token consistency and prevents mismatches.
    
    Frontend should:
    1. Read token from response body
    2. Send token in X-CSRF-Token header with state-changing requests
    3. Backend validates header matches cookie
    
    Cookie settings:
    - Development: Domain=localhost (cross-port), secure=False, sameSite=Lax
    - Production: Domain=.wistx.ai (cross-subdomain), secure=True, sameSite=None (for cross-subdomain support)
    
    Args:
        request: FastAPI Request object to read existing cookie
        response: FastAPI Response object for setting cookie
        force: If True, always generate a new token (useful for recovery from mismatches)
        
    Returns:
        CSRF token in JSON response
    """
    if not force:
        existing_token = request.cookies.get(CSRF_COOKIE_NAME)
        if existing_token and len(existing_token) >= 32:
            logger.debug("Returning existing CSRF token from cookie")
            return CSRFTokenResponse(token=existing_token)
    else:
        logger.debug("Force flag set, generating new CSRF token")
    
    token = generate_csrf_token()
    domain = get_cookie_domain()
    
    if settings.debug:
        cookie_kwargs = {
            "key": CSRF_COOKIE_NAME,
            "value": token,
            "max_age": CSRF_COOKIE_MAX_AGE,
            "httponly": True,
            "secure": False,
            "samesite": "lax",  # Use Lax for development - works for same-origin, requires proxy for cross-origin
            "path": CSRF_COOKIE_PATH,
        }
        if not domain:
            cookie_kwargs["domain"] = None
        else:
            cookie_kwargs["domain"] = domain
        logger.debug(
            "Setting CSRF cookie for development: domain=%s, samesite=lax, secure=false. "
            "Note: For cross-origin requests (localhost:3000 → localhost:8000), use Next.js proxy or HTTPS with Secure=True.",
            domain or "same-domain",
        )
    else:
        cookie_kwargs = {
            "key": CSRF_COOKIE_NAME,
            "value": token,
            "max_age": CSRF_COOKIE_MAX_AGE,
            "httponly": True,
            "secure": True,
            "samesite": "none" if domain else "lax",
            "path": CSRF_COOKIE_PATH,
        }
        if domain:
            cookie_kwargs["domain"] = domain
    
    response.set_cookie(**cookie_kwargs)
    
    set_cookie_header = response.headers.get("set-cookie")
    logger.info(
        "CSRF token generated and set in cookie: domain=%s, httponly=%s, secure=%s, samesite=%s, path=%s",
        domain or "same-domain",
        cookie_kwargs["httponly"],
        cookie_kwargs["secure"],
        cookie_kwargs["samesite"],
        cookie_kwargs["path"],
    )
    if set_cookie_header:
        logger.debug("Set-Cookie header: %s", set_cookie_header)
    else:
        logger.warning("Set-Cookie header not found in response headers")
    
    return CSRFTokenResponse(token=token)

