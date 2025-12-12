"""MongoDB custom exceptions."""

from typing import Optional


class MongoDBError(Exception):
    """Base exception for MongoDB operations."""


class MongoDBConnectionError(MongoDBError):
    """Raised when connection to MongoDB fails."""

    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.original_error = original_error


class MongoDBOperationError(MongoDBError):
    """Raised when a MongoDB operation fails."""

    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.original_error = original_error


class MongoDBTimeoutError(MongoDBError):
    """Raised when a MongoDB operation times out."""


class MongoDBCircuitBreakerOpenError(MongoDBError):
    """Raised when circuit breaker is open."""

    def __init__(self, message: str = "Circuit breaker is OPEN. MongoDB appears to be down."):
        super().__init__(message)

