"""Retry handler for MongoDB operations."""

import time
import logging
from typing import Callable, TypeVar, Any
from functools import wraps

from pymongo.errors import (
    ServerSelectionTimeoutError,
    NetworkTimeout,
    ConnectionFailure,
    AutoReconnect,
    NotPrimaryError,
    ExecutionTimeout,
)

from api.database.exceptions import MongoDBConnectionError, MongoDBTimeoutError

logger = logging.getLogger(__name__)

T = TypeVar("T")

RETRYABLE_EXCEPTIONS = (
    ServerSelectionTimeoutError,
    NetworkTimeout,
    ConnectionFailure,
    AutoReconnect,
    NotPrimaryError,
    ExecutionTimeout,
)


def retry_mongodb_operation(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 10.0,
    exponential_base: float = 2.0,
    retryable_exceptions: tuple[type[Exception], ...] = RETRYABLE_EXCEPTIONS,
):
    """Decorator for retrying MongoDB operations with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff
        retryable_exceptions: Tuple of exception types to retry on
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception: Exception | None = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)

                except retryable_exceptions as e:
                    last_exception = e

                    if attempt == max_attempts:
                        logger.error(
                            "MongoDB operation failed after %s attempts: %s",
                            max_attempts,
                            e,
                        )
                        if isinstance(e, (NetworkTimeout, ExecutionTimeout)):
                            raise MongoDBTimeoutError(f"Operation timed out: {e}") from e
                        raise MongoDBConnectionError(f"Connection failed: {e}") from e

                    delay = min(initial_delay * (exponential_base ** (attempt - 1)), max_delay)

                    logger.warning(
                        "MongoDB operation failed (attempt %s/%s): %s. Retrying in %.2fs...",
                        attempt,
                        max_attempts,
                        e,
                        delay,
                    )

                    time.sleep(delay)

                except Exception as e:
                    logger.error("MongoDB operation failed with non-retryable error: %s", e)
                    raise

            if last_exception:
                raise MongoDBConnectionError(
                    f"Operation failed after {max_attempts} attempts"
                ) from last_exception

            raise RuntimeError("Unexpected error in retry logic")

        return wrapper

    return decorator
