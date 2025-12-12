"""Database clients and connection management."""

from api.database.mongodb import (
    MongoDBManager,
    mongodb_manager,
    get_database,
    get_client,
)
from api.database.exceptions import (
    MongoDBError,
    MongoDBConnectionError,
    MongoDBOperationError,
    MongoDBTimeoutError,
    MongoDBCircuitBreakerOpenError,
)
from api.database.health_check import MongoDBHealthCheck
from api.database.circuit_breaker import CircuitBreaker, CircuitState

__all__ = [
    "MongoDBManager",
    "mongodb_manager",
    "get_database",
    "get_client",
    "MongoDBError",
    "MongoDBConnectionError",
    "MongoDBOperationError",
    "MongoDBTimeoutError",
    "MongoDBCircuitBreakerOpenError",
    "MongoDBHealthCheck",
    "CircuitBreaker",
    "CircuitState",
]

