"""Production-ready MongoDB connection manager."""

import logging
import atexit
from typing import Any, Optional
from contextlib import contextmanager

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import (
    ServerSelectionTimeoutError,
    NetworkTimeout,
    ConnectionFailure,
    AutoReconnect,
    NotPrimaryError,
    ExecutionTimeout,
)
from pymongo import monitoring

from api.config import settings
from api.database.exceptions import (
    MongoDBConnectionError,
    MongoDBCircuitBreakerOpenError,
)
from api.database.circuit_breaker import CircuitBreaker
from api.database.retry_handler import retry_mongodb_operation
from api.database.health_check import MongoDBHealthCheck

logger = logging.getLogger(__name__)

_pymongo_logger = logging.getLogger("pymongo")
_pymongo_logger.setLevel(logging.WARNING)


class MongoDBSSLErrorFilter(logging.Filter):
    """Filter out non-critical MongoDB SSL handshake errors from background tasks.
    
    These errors occur during connection pool maintenance (remove_stale_sockets)
    and are non-critical - MongoDB handles them gracefully with auto-reconnect.
    Suppressing them reduces log pollution while maintaining visibility of actual errors.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter out SSL handshake errors from background tasks."""
        message = record.getMessage()
        
        if "SSL handshake failed" in message:
            if "background task" in message or "_process_periodic_tasks" in str(record.pathname):
                return False
        
        if "AutoReconnect" in message and "SSL handshake failed" in message:
            if "remove_stale_sockets" in str(record.pathname) or "background task" in message:
                return False
        
        return True


_pymongo_logger.addFilter(MongoDBSSLErrorFilter())


class MongoDBBackgroundTaskErrorHandler(monitoring.ServerHeartbeatListener):
    """Handle MongoDB background task errors gracefully."""

    def started(self, event: monitoring.ServerHeartbeatStartedEvent) -> None:
        """Called when a server heartbeat is started."""
        pass

    def succeeded(self, event: monitoring.ServerHeartbeatSucceededEvent) -> None:
        """Called when a server heartbeat succeeds."""
        pass

    def failed(self, event: monitoring.ServerHeartbeatFailedEvent) -> None:
        """Called when a server heartbeat fails.

        This handles background task errors gracefully without raising exceptions.
        Suppresses non-critical errors like DNS resolution failures for replica set members.
        """
        try:
            error = event.reply
            if error:
                error_type = type(error).__name__
                error_str = str(error).lower()
                
                connection_id = getattr(event, "connection_id", None)
                server_info = f"connection_id={connection_id}" if connection_id else "unknown"
                
                if error_type in ("_OperationCancelled", "OperationCancelled"):
                    logger.debug(
                        "MongoDB background task cancelled (non-critical): %s",
                        error,
                    )
                elif error_type == "AutoReconnect":
                    if "nodename nor servname" in error_str or "gaierror" in error_str:
                        logger.debug(
                            "MongoDB replica set member unreachable (non-critical): %s",
                            server_info,
                        )
                    elif "ssl handshake failed" in error_str or "tlsv1 alert" in error_str:
                        logger.debug(
                            "MongoDB SSL handshake error during background task (non-critical): %s",
                            server_info,
                        )
                    else:
                        logger.debug(
                            "MongoDB background reconnection attempt (non-critical): %s",
                            error,
                        )
                else:
                    logger.debug(
                        "MongoDB background task failed (non-critical): %s (type: %s)",
                        error,
                        error_type,
                    )
        except AttributeError as e:
            logger.debug(
                "MongoDB heartbeat failed event handling error (non-critical): %s",
                e,
            )
        except Exception as e:
            logger.debug(
                "MongoDB heartbeat failed event handling error (non-critical): %s",
                e,
            )


class MongoDBManager:
    """Production-ready MongoDB connection manager.

    Features:
    - Connection pooling
    - Automatic reconnection
    - Retry logic with exponential backoff
    - Circuit breaker pattern
    - Health checks
    - Graceful shutdown
    - Context manager support
    """

    _instance: Optional["MongoDBManager"] = None
    _client: Optional[MongoClient] = None

    def __new__(cls) -> "MongoDBManager":
        """Singleton pattern - ensure only one instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize MongoDB manager."""
        if self._client is not None:
            return

        self._client: Optional[MongoClient] = None
        self._database: Optional[Database] = None
        self._circuit_breaker = CircuitBreaker(
            failure_threshold=settings.mongodb_circuit_breaker_failure_threshold,
            recovery_timeout=settings.mongodb_circuit_breaker_recovery_timeout,
            expected_exception=(
                ServerSelectionTimeoutError,
                NetworkTimeout,
                ConnectionFailure,
                AutoReconnect,
                NotPrimaryError,
                ExecutionTimeout,
            ),
            name="mongodb",
        )
        self._health_check: Optional[MongoDBHealthCheck] = None

        atexit.register(self.close)

    def connect(self) -> MongoClient:
        """Connect to MongoDB with production-ready configuration.

        Returns:
            MongoDB client instance

        Raises:
            MongoDBConnectionError: If connection fails
        """
        if self._client is not None:
            return self._client

        connection_string = self._build_connection_string()
        options = settings.get_mongodb_connection_options()

        max_attempts = 3
        last_error = None

        for attempt in range(1, max_attempts + 1):
            try:
                logger.info("Connecting to MongoDB (attempt %d/%d)...", attempt, max_attempts)

                event_listeners = [MongoDBBackgroundTaskErrorHandler()]

                self._client = MongoClient(
                    connection_string,
                    event_listeners=event_listeners,
                    **options,
                )

                self._test_connection()

                self._database = self._client[settings.mongodb_database]

                self._health_check = MongoDBHealthCheck(self._client)

                logger.info(
                    "Successfully connected to MongoDB: %s (pool size: %s)",
                    settings.mongodb_database,
                    options["maxPoolSize"],
                )

                return self._client

            except (ServerSelectionTimeoutError, NetworkTimeout, ConnectionFailure) as e:
                last_error = e
                error_str = str(e).lower()
                
                if attempt < max_attempts:
                    wait_time = attempt * 2
                    logger.warning(
                        "MongoDB connection attempt %d/%d failed: %s. Retrying in %d seconds...",
                        attempt,
                        max_attempts,
                        str(e)[:200],
                        wait_time,
                    )
                    
                    if "ssl handshake failed" in error_str or "tlsv1 alert" in error_str:
                        logger.warning(
                            "SSL handshake error detected. Common causes: "
                            "1) IP address not whitelisted in MongoDB Atlas Network Access, "
                            "2) Firewall blocking connection, "
                            "3) Certificate validation issues. "
                            "Check MongoDB Atlas Network Access settings."
                        )
                    
                    import time
                    time.sleep(wait_time)
                else:
                    logger.error("Failed to connect to MongoDB after %d attempts: %s", max_attempts, e)
                    if "ssl handshake failed" in error_str or "tlsv1 alert" in error_str:
                        logger.error(
                            "SSL handshake failure. Troubleshooting steps: "
                            "1) Verify your IP address is whitelisted in MongoDB Atlas (Network Access), "
                            "2) Check firewall rules allow outbound connections to MongoDB Atlas, "
                            "3) Ensure connection string is correct and password is URL-encoded if needed."
                        )
            except Exception as e:
                last_error = e
                logger.error("Failed to connect to MongoDB: %s", e, exc_info=True)
                break

        raise MongoDBConnectionError(f"Failed to connect to MongoDB after {max_attempts} attempts: {last_error}") from last_error

    def _build_connection_string(self) -> str:
        """Build MongoDB connection string with all options.

        Returns:
            Complete connection string (without database name - handled separately)
        """
        connection_url = str(settings.mongodb_url).strip()

        connection_url = connection_url.rstrip("/")


        return connection_url

    @retry_mongodb_operation(
        max_attempts=settings.mongodb_retry_max_attempts,
        initial_delay=settings.mongodb_retry_initial_delay,
        max_delay=settings.mongodb_retry_max_delay,
    )
    def _test_connection(self) -> None:
        """Test MongoDB connection.

        Raises:
            MongoDBConnectionError: If connection test fails
        """
        if self._client is None:
            raise MongoDBConnectionError("Client not initialized")

        self._client.admin.command("ping")

    def get_client(self) -> MongoClient:
        """Get MongoDB client instance.

        Returns:
            MongoDB client

        Raises:
            MongoDBConnectionError: If not connected
        """
        if self._client is None:
            self.connect()

        if self._client is None:
            raise MongoDBConnectionError("Failed to initialize MongoDB client")

        return self._client

    def get_database(self) -> Database:
        """Get MongoDB database instance.

        Returns:
            MongoDB database

        Raises:
            MongoDBConnectionError: If not connected
        """
        if self._database is None:
            self.connect()

        if self._database is None:
            raise MongoDBConnectionError("Failed to initialize MongoDB database")

        return self._database

    @contextmanager
    def safe_operation(self):
        """Context manager for safe MongoDB operations with circuit breaker.

        Usage:
            with mongodb_manager.safe_operation():
                db.collection.find_one(...)
        """
        try:
            if self._circuit_breaker.get_state().value == "open":
                raise MongoDBCircuitBreakerOpenError()

            yield self._circuit_breaker

        except (
            ServerSelectionTimeoutError,
            NetworkTimeout,
            ConnectionFailure,
            AutoReconnect,
            NotPrimaryError,
            ExecutionTimeout,
        ) as e:
            self._circuit_breaker.call(lambda: None)
            raise MongoDBConnectionError(f"MongoDB operation failed: {e}") from e

    def health_check(self) -> dict[str, Any]:
        """Perform health check.

        Returns:
            Health status dictionary

        Raises:
            MongoDBConnectionError: If health check fails
        """
        if self._health_check is None:
            self.connect()

        if self._health_check is None:
            raise MongoDBConnectionError("Health check not initialized")

        return self._circuit_breaker.call(self._health_check.check)

    def is_healthy(self) -> bool:
        """Check if MongoDB is healthy.

        Returns:
            True if healthy, False otherwise
        """
        try:
            status = self.health_check()
            return status.get("status") == "healthy"
        except (MongoDBConnectionError, MongoDBCircuitBreakerOpenError):
            return False

    def get_circuit_breaker_stats(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Circuit breaker statistics
        """
        return self._circuit_breaker.get_stats()

    def reset_circuit_breaker(self) -> None:
        """Manually reset circuit breaker."""
        self._circuit_breaker.reset()

    def get_connection_pool_stats(self) -> dict[str, Any]:
        """Get MongoDB connection pool statistics.

        Returns:
            Dictionary with connection pool statistics:
            {
                "max_pool_size": int,
                "min_pool_size": int,
                "active_connections": int,
                "idle_connections": int,
                "total_connections": int,
                "pool_utilization_percent": float,
                "waiting_for_connection": int,
            }
        """
        if self._client is None:
            return {
                "status": "not_connected",
                "max_pool_size": 0,
                "min_pool_size": 0,
                "active_connections": 0,
                "idle_connections": 0,
                "total_connections": 0,
                "pool_utilization_percent": 0.0,
                "waiting_for_connection": 0,
            }

        try:
            options = settings.get_mongodb_connection_options()
            max_pool_size = options.get("maxPoolSize", 100)
            min_pool_size = options.get("minPoolSize", 0)

            total_connections = 0
            active_connections = 0
            idle_connections = 0

            try:
                topology = self._client._topology
                if topology and hasattr(topology, "_servers"):
                    for server_address, server in topology._servers.items():
                        if server and hasattr(server, "pool") and server.pool:
                            pool = server.pool
                            
                            if hasattr(pool, "_sockets"):
                                sockets = pool._sockets
                                if sockets:
                                    socket_count = len(sockets)
                                    total_connections += socket_count
                                    
                                    active_count = 0
                                    for socket in sockets:
                                        if hasattr(socket, "in_use") and socket.in_use:
                                            active_count += 1
                                    active_connections += active_count
                                    idle_connections += socket_count - active_count
                            
                            elif hasattr(pool, "opts"):
                                pool_opts = pool.opts
                                if hasattr(pool_opts, "max_pool_size"):
                                    pool_max = pool_opts.max_pool_size
                                    if pool_max and pool_max != max_pool_size:
                                        max_pool_size = max(max_pool_size, pool_max)
            except (AttributeError, TypeError, KeyError) as e:
                logger.debug("Could not access detailed pool stats (non-critical): %s", e)

            pool_utilization = (total_connections / max_pool_size * 100) if max_pool_size > 0 else 0.0

            return {
                "status": "connected",
                "max_pool_size": max_pool_size,
                "min_pool_size": min_pool_size,
                "active_connections": active_connections,
                "idle_connections": idle_connections,
                "total_connections": total_connections if total_connections > 0 else "unknown",
                "pool_utilization_percent": round(pool_utilization, 2) if total_connections > 0 else 0.0,
                "waiting_for_connection": 0,
            }
        except Exception as e:
            logger.warning("Failed to get connection pool stats: %s", e)
            options = settings.get_mongodb_connection_options() if self._client else {}
            return {
                "status": "error",
                "error": str(e),
                "max_pool_size": options.get("maxPoolSize", 100) if self._client else 0,
                "min_pool_size": options.get("minPoolSize", 0) if self._client else 0,
            }

    def monitor_connection_pool(self) -> dict[str, Any]:
        """Monitor connection pool health and log warnings if utilization is high.

        Returns:
            Connection pool statistics with health status
        """
        stats = self.get_connection_pool_stats()
        
        if stats.get("status") != "connected":
            return stats

        utilization = stats.get("pool_utilization_percent", 0.0)
        max_pool_size = stats.get("max_pool_size", 100)
        total_connections = stats.get("total_connections", 0)

        if utilization >= 90:
            logger.warning(
                "MongoDB connection pool utilization is CRITICAL: %.1f%% (%d/%d connections). "
                "Consider increasing maxPoolSize or reducing concurrent operations.",
                utilization,
                total_connections,
                max_pool_size,
            )
        elif utilization >= 75:
            logger.warning(
                "MongoDB connection pool utilization is HIGH: %.1f%% (%d/%d connections). "
                "Monitor closely and consider increasing maxPoolSize if this persists.",
                utilization,
                total_connections,
                max_pool_size,
            )
        elif utilization >= 50:
            logger.info(
                "MongoDB connection pool utilization: %.1f%% (%d/%d connections)",
                utilization,
                total_connections,
                max_pool_size,
            )

        stats["health_status"] = (
            "critical" if utilization >= 90
            else "warning" if utilization >= 75
            else "healthy" if utilization < 50
            else "moderate"
        )

        return stats

    def close(self) -> None:
        """Close MongoDB connection gracefully."""
        if self._client is not None:
            logger.info("Closing MongoDB connection...")
            try:
                self._client.close()
                logger.info("MongoDB connection closed")
            except Exception as e:
                logger.warning("Error closing MongoDB connection (non-critical): %s", e)
            finally:
                self._client = None
                self._database = None
                self._health_check = None

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""


mongodb_manager = MongoDBManager()


def get_database() -> Database:
    """Get MongoDB database instance (dependency injection helper).

    Returns:
        MongoDB database instance
    """
    return mongodb_manager.get_database()


def get_client() -> MongoClient:
    """Get MongoDB client instance (dependency injection helper).

    Returns:
        MongoDB client instance
    """
    return mongodb_manager.get_client()
