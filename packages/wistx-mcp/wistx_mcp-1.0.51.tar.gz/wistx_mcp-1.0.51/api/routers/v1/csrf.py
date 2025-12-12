"""CSRF token endpoint for Double Submit Cookie pattern."""

import logging

from fastapi import APIRouter, Response
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
async def get_csrf_token(response: Response) -> CSRFTokenResponse:
    """Get CSRF token for Double Submit Cookie pattern.
    
    Generates a cryptographically secure CSRF token, sets it in a cookie,
    and returns it in the response body. Frontend should:
    1. Read token from response body
    2. Send token in X-CSRF-Token header with state-changing requests
    3. Backend validates header matches cookie
    
    Cookie settings:
    - Development: Domain=localhost (cross-port), secure=False, sameSite=None
    - Production: Domain=.wistx.ai (cross-subdomain), secure=True, sameSite=Lax
    
    Args:
        response: FastAPI Response object for setting cookie
        
    Returns:
        CSRF token in JSON response
    """
    token = generate_csrf_token()
    domain = get_cookie_domain()
    
    if settings.debug:
        cookie_kwargs = {
            "key": CSRF_COOKIE_NAME,
            "value": token,
            "max_age": CSRF_COOKIE_MAX_AGE,
            "httponly": True,
            "secure": False,
            "samesite": "lax",  # Changed from "none" to "lax" for development
            "path": CSRF_COOKIE_PATH,
        }
        if domain:
            cookie_kwargs["domain"] = domain
    else:
        cookie_kwargs = {
            "key": CSRF_COOKIE_NAME,
            "value": token,
            "max_age": CSRF_COOKIE_MAX_AGE,
            "httponly": True,
            "secure": True,
            "samesite": "lax",
            "path": CSRF_COOKIE_PATH,
        }
        if domain:
            cookie_kwargs["domain"] = domain
    
    response.set_cookie(**cookie_kwargs)
    
    logger.info(
        "CSRF token generated and set in cookie: domain=%s, httponly=%s, secure=%s",
        domain or "same-domain",
        cookie_kwargs["httponly"],
        cookie_kwargs["secure"],
    )
    
    return CSRFTokenResponse(token=token)

