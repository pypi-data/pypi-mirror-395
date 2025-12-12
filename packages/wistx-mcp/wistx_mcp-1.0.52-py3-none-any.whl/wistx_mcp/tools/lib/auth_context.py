"""Server-level authentication context for MCP tools."""

import logging
import time
from typing import Any, Optional

from contextvars import ContextVar

from wistx_mcp.tools.lib.api_client import WISTXAPIClient
from wistx_mcp.tools.lib.secure_storage import SecureString

logger = logging.getLogger(__name__)

auth_context: ContextVar[dict[str, Any]] = ContextVar("auth_context", default={})

_user_id_cache: dict[str, tuple[str, float]] = {}
_cache_ttl = 300.0


class AuthContext:
    """Server-level authentication context manager with proper isolation."""

    def __init__(self, api_key: Optional[str] = None, request_id: Optional[str] = None):
        """Initialize authentication context.

        Args:
            api_key: API key for authentication
            request_id: Request ID for tracing
        """
        self._api_key_secure: Optional[SecureString] = None
        if api_key:
            self._api_key_secure = SecureString(api_key)
        self.user_info: Optional[dict[str, Any]] = None
        self._api_client: Optional[WISTXAPIClient] = None
        self.request_id = request_id
        self._context_token = None
        self._entered = False

    async def __aenter__(self):
        """Enter async context manager."""
        if self._entered:
            raise RuntimeError("AuthContext already entered")
        
        self._context_token = auth_context.set({
            "auth_context": self,
            "request_id": self.request_id,
        })
        self._entered = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context manager with guaranteed cleanup."""
        if self._context_token is not None:
            try:
                auth_context.reset(self._context_token)
            except (ValueError, LookupError) as e:
                logger.warning("Failed to reset auth context token: %s", e)
            finally:
                self._context_token = None
                self._entered = False
        
        self._clear_sensitive_data()
        return False
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key value from secure storage.

        Returns:
            API key string or None if not set
        """
        if self._api_key_secure:
            return self._api_key_secure.get()
        return None

    @property
    def api_key(self) -> Optional[str]:
        """Get API key value from secure storage (public property).

        Returns:
            API key string or None if not set
        """
        return self._get_api_key()

    def _clear_sensitive_data(self) -> None:
        """Clear sensitive data from memory."""
        if self._api_key_secure:
            self._api_key_secure.clear()
            self._api_key_secure = None
        if self._api_client:
            self._api_client = None

    async def validate(self) -> dict[str, Any]:
        """Validate API key and get user information.

        Returns:
            Dictionary with user_id, organization_id, plan, etc.

        Raises:
            ValueError: If API key is invalid or missing
        """
        api_key = self._get_api_key()
        if not api_key:
            raise ValueError("API key is required. Set WISTX_API_KEY environment variable or provide via MCP initialization.")

        if not self._api_client:
            self._api_client = WISTXAPIClient(api_key=api_key)

        try:
            self.user_info = await self._api_client.get_current_user(api_key=api_key)
            user_id = self.user_info.get("user_id")

            if not user_id:
                raise ValueError("Invalid API key or user not found")

            return self.user_info
        except Exception as e:
            logger.error("Error validating API key: %s", e, exc_info=True)
            raise ValueError("Invalid API key or authentication failed") from e

    def get_api_client(self) -> WISTXAPIClient:
        """Get API client with authenticated context.

        Returns:
            WISTXAPIClient instance with API key set

        Raises:
            ValueError: If API key is not set
        """
        api_key = self._get_api_key()
        if not api_key:
            raise ValueError("API key is required")

        if not self._api_client:
            self._api_client = WISTXAPIClient(api_key=api_key)

        return self._api_client

    def get_user_id(self) -> Optional[str]:
        """Get current user ID.

        Returns:
            User ID string or None if not authenticated
        """
        if self.user_info:
            return str(self.user_info.get("user_id"))
        return None

    def get_api_key_id(self) -> Optional[str]:
        """Get current API key ID.

        Returns:
            API key ID string or None if not authenticated or not available
        """
        if self.user_info:
            api_key_id = self.user_info.get("api_key_id")
            return str(api_key_id) if api_key_id else None
        return None


def get_auth_context() -> Optional[AuthContext]:
    """Get current authentication context from context variable.

    Returns:
        AuthContext instance or None if not set
    """
    ctx = auth_context.get()
    if ctx and "auth_context" in ctx:
        return ctx["auth_context"]
    return None


def set_auth_context(context: AuthContext) -> None:
    """Set authentication context in context variable.

    Args:
        context: AuthContext instance to set
    """
    auth_context.set({"auth_context": context})


_api_key_context: ContextVar[str | None] = ContextVar("api_key_context", default=None)


def get_api_key_from_context() -> str | None:
    """Get API key from context variable.

    Returns:
        API key or None if not set
    """
    return _api_key_context.get()


def set_api_key_context(api_key: str | None) -> None:
    """Set API key in context variable.

    Args:
        api_key: API key to set, or None to clear
    """
    _api_key_context.set(api_key)


async def validate_api_key_and_get_user_id(api_key: str | None) -> str:
    """Validate API key and return user ID.

    Centralized API key validation function to reduce code duplication.
    Checks context variable first, then provided api_key parameter.

    Args:
        api_key: API key to validate (optional, checks context if not provided)

    Returns:
        User ID string

    Raises:
        ValueError: If API key is missing or invalid
        RuntimeError: If authentication service is unavailable
    """
    api_key = get_api_key_from_context() or api_key

    if not api_key:
        raise ValueError("API key is required. Set WISTX_API_KEY environment variable or provide via MCP initialization.")

    cache_key = api_key[:20] if api_key else None
    current_time = time.time()

    if cache_key and cache_key in _user_id_cache:
        cached_user_id, cache_time = _user_id_cache[cache_key]
        if current_time - cache_time < _cache_ttl:
            logger.debug("Using cached user_id for API key")
            return cached_user_id
        else:
            del _user_id_cache[cache_key]

    try:
        api_client = WISTXAPIClient(api_key=api_key)
        user_info = await api_client.get_current_user(api_key=api_key)
        user_id = user_info.get("user_id")

        if not user_id:
            raise ValueError("Invalid API key or user not found")

        user_id_str = str(user_id)
        if cache_key:
            _user_id_cache[cache_key] = (user_id_str, current_time)
            if len(_user_id_cache) > 1000:
                oldest_key = min(_user_id_cache.keys(), key=lambda k: _user_id_cache[k][1])
                del _user_id_cache[oldest_key]

        return user_id_str
    except ValueError:
        raise
    except (RuntimeError, ConnectionError, TimeoutError) as e:
        logger.warning("Error validating API key (using cache if available): %s", e)
        if cache_key and cache_key in _user_id_cache:
            cached_user_id, _ = _user_id_cache[cache_key]
            logger.info("Using cached user_id due to API unavailability")
            return cached_user_id
        raise RuntimeError("Authentication service temporarily unavailable") from e
    except Exception as e:
        logger.error("Error validating API key: %s", e, exc_info=True)
        if cache_key and cache_key in _user_id_cache:
            cached_user_id, _ = _user_id_cache[cache_key]
            logger.info("Using cached user_id due to unexpected error")
            return cached_user_id
        raise ValueError("Invalid API key or authentication failed") from e

