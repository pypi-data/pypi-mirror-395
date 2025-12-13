"""CSRF token utilities for Double Submit Cookie pattern."""

import hmac
import logging
import secrets

logger = logging.getLogger(__name__)

CSRF_TOKEN_LENGTH = 32
CSRF_COOKIE_NAME = "csrf_token"
CSRF_HEADER_NAME = "X-CSRF-Token"
CSRF_COOKIE_MAX_AGE = 60 * 60 * 24
CSRF_COOKIE_PATH = "/"


def generate_csrf_token() -> str:
    """Generate cryptographically secure CSRF token.
    
    Uses secrets.token_urlsafe() for cryptographically secure random generation.
    Token length: 32 bytes = 43 characters base64-encoded.
    
    Returns:
        CSRF token string (URL-safe base64)
    """
    token = secrets.token_urlsafe(CSRF_TOKEN_LENGTH)
    logger.debug("Generated CSRF token: length=%d", len(token))
    return token


def validate_csrf_token(header_token: str | None, cookie_token: str | None) -> bool:
    """Validate CSRF token using Double Submit Cookie pattern.
    
    Compares token from header to token from cookie. Both must match exactly.
    
    Args:
        header_token: CSRF token from X-CSRF-Token header
        cookie_token: CSRF token from csrf_token cookie
        
    Returns:
        True if tokens match and are valid, False otherwise
    """
    if not header_token or not cookie_token:
        logger.debug(
            "CSRF validation failed: missing token (header=%s, cookie=%s)",
            bool(header_token),
            bool(cookie_token),
        )
        return False
    
    # Use constant-time comparison to prevent timing attacks
    # hmac.compare_digest prevents attackers from inferring token characters
    # by measuring response time differences
    if not hmac.compare_digest(header_token, cookie_token):
        logger.warning(
            "CSRF validation failed: token mismatch (header_length=%d, cookie_length=%d)",
            len(header_token),
            len(cookie_token),
        )
        return False
    
    if len(header_token) < 32:
        logger.warning(
            "CSRF validation failed: token too short (length=%d)",
            len(header_token),
        )
        return False
    
    logger.debug("CSRF validation successful")
    return True


def is_state_changing_method(method: str) -> bool:
    """Check if HTTP method is state-changing (requires CSRF protection).
    
    Args:
        method: HTTP method string
        
    Returns:
        True if method requires CSRF protection, False otherwise
    """
    return method.upper() in ("POST", "PUT", "PATCH", "DELETE")

