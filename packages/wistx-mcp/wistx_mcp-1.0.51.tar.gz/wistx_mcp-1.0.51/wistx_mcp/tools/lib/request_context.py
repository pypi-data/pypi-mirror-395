"""Request context propagation for MCP tools."""

import logging
from contextvars import ContextVar
from typing import Any, Optional

logger = logging.getLogger(__name__)

_request_context_var: ContextVar[dict[str, Any]] = ContextVar("request_context", default={})


def get_request_context() -> dict[str, Any]:
    """Get current request context.

    Returns:
        Dictionary with request context (request_id, user_id, etc.)
    """
    return _request_context_var.get()


def set_request_context(context: dict[str, Any]) -> None:
    """Set request context.

    Args:
        context: Context dictionary with request_id, user_id, etc.
    """
    _request_context_var.set(context)


def update_request_context(**kwargs: Any) -> None:
    """Update request context with new values.

    Args:
        **kwargs: Key-value pairs to add/update in context
    """
    current = get_request_context()
    current.update(kwargs)
    set_request_context(current)


def get_request_id() -> Optional[str]:
    """Get current request ID from context.

    Returns:
        Request ID string or None
    """
    return get_request_context().get("request_id")


def get_user_id() -> Optional[str]:
    """Get current user ID from context.

    Returns:
        User ID string or None
    """
    return get_request_context().get("user_id")


def clear_request_context() -> None:
    """Clear request context."""
    _request_context_var.set({})

