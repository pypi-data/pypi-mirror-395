"""Distributed tracing utilities with correlation IDs."""

import uuid
import contextvars
import logging
from typing import Optional

logger = logging.getLogger(__name__)

correlation_id: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar('correlation_id', default=None)


def get_correlation_id() -> str:
    """Get or create correlation ID.

    Returns:
        Correlation ID string
    """
    cid = correlation_id.get()
    if not cid:
        cid = str(uuid.uuid4())
        correlation_id.set(cid)
    return cid


def set_correlation_id(cid: str):
    """Set correlation ID.

    Args:
        cid: Correlation ID string
    """
    correlation_id.set(cid)


class TracingContext:
    """Context manager for tracing operations."""

    def __init__(self, operation_name: str, **kwargs):
        """Initialize tracing context.

        Args:
            operation_name: Name of the operation
            **kwargs: Additional attributes to log
        """
        self.operation_name = operation_name
        self.correlation_id = get_correlation_id()
        self.attributes = kwargs

    def __enter__(self):
        """Enter context."""
        logger.info(
            "Starting operation: %s [correlation_id=%s]",
            self.operation_name,
            self.correlation_id,
            extra={"correlation_id": self.correlation_id, **self.attributes}
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context."""
        if exc_type:
            logger.error(
                "Operation failed: %s [correlation_id=%s]",
                self.operation_name,
                self.correlation_id,
                exc_info=True,
                extra={"correlation_id": self.correlation_id}
            )
        else:
            logger.info(
                "Operation completed: %s [correlation_id=%s]",
                self.operation_name,
                self.correlation_id,
                extra={"correlation_id": self.correlation_id}
            )

