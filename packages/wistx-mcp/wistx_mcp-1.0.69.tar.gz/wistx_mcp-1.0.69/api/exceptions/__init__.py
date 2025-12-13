"""Custom exception hierarchy for WISTX API."""

import uuid
from typing import Any, Optional


class WISTXError(Exception):
    """Base exception for all WISTX errors.

    Attributes:
        correlation_id: Unique identifier for error tracking
        error_code: Machine-readable error code
        user_message: User-friendly error message
        details: Additional error details
    """

    def __init__(
        self,
        message: str,
        correlation_id: Optional[str] = None,
        error_code: Optional[str] = None,
        user_message: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ):
        """Initialize WISTX error.

        Args:
            message: Technical error message
            correlation_id: Correlation ID for tracking
            error_code: Machine-readable error code
            user_message: User-friendly message
            details: Additional error details
        """
        super().__init__(message)
        self.correlation_id = correlation_id or str(uuid.uuid4())
        self.error_code = error_code or self.__class__.__name__
        self.user_message = user_message or message
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON response.

        Returns:
            Error dictionary
        """
        return {
            "error": self.error_code,
            "message": self.user_message,
            "correlation_id": self.correlation_id,
            "details": self.details,
        }


class ValidationError(WISTXError):
    """Validation error."""
    pass


class AuthenticationError(WISTXError):
    """Authentication error."""
    pass


class AuthorizationError(WISTXError):
    """Authorization error."""
    pass


class DatabaseError(WISTXError):
    """Database operation error."""
    pass


class RateLimitError(WISTXError):
    """Rate limit exceeded error."""
    pass


class NotFoundError(WISTXError):
    """Resource not found error."""
    pass


class ExternalServiceError(WISTXError):
    """External service error."""
    pass

