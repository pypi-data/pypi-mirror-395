"""Health check for MongoDB connection."""

import time
import logging
from typing import Any
from datetime import datetime

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure

from api.database.exceptions import MongoDBConnectionError

logger = logging.getLogger(__name__)


class MongoDBHealthCheck:
    """Health check for MongoDB connection."""

    def __init__(self, client: MongoClient):
        """Initialize health check.

        Args:
            client: MongoDB client instance
        """
        self.client = client
        self.last_check: datetime | None = None
        self.last_status: dict[str, Any] | None = None

    def check(self) -> dict[str, Any]:
        """Perform health check.

        Returns:
            Dictionary with health status information

        Raises:
            MongoDBConnectionError: If health check fails
        """
        start_time = time.time()

        try:
            self.client.admin.command("ping")

            server_status = self.client.admin.command("serverStatus")

            server_info = self.client.server_info()

            latency_ms = (time.time() - start_time) * 1000

            connections = server_status.get("connections", {})
            current_connections = connections.get("current", 0)
            available_connections = connections.get("available", 0)

            op_latencies = server_status.get("opLatencies", {})
            read_latency = (
                op_latencies.get("reads", {}).get("latency", 0) if op_latencies else 0
            )
            write_latency = (
                op_latencies.get("writes", {}).get("latency", 0) if op_latencies else 0
            )

            health_status = {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "latency_ms": round(latency_ms, 2),
                "connections": {
                    "current": current_connections,
                    "available": available_connections,
                    "max": connections.get("max", 0),
                },
                "server": {
                    "version": server_info.get("version", "unknown"),
                    "uptime_seconds": server_status.get("uptime", 0),
                    "read_latency_ms": read_latency,
                    "write_latency_ms": write_latency,
                },
                "replica_set": {
                    "is_master": server_status.get("repl", {}).get("ismaster", False),
                    "primary": server_status.get("repl", {}).get("primary", None),
                },
            }

            self.last_check = datetime.utcnow()
            self.last_status = health_status

            logger.debug("MongoDB health check passed: %s", health_status)

            return health_status

        except ServerSelectionTimeoutError as e:
            error_status = {
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "error": "Server selection timeout",
                "error_type": type(e).__name__,
                "error_message": str(e),
            }

            self.last_check = datetime.utcnow()
            self.last_status = error_status

            logger.error("MongoDB health check failed: %s", error_status)

            raise MongoDBConnectionError("MongoDB server selection timeout") from e

        except OperationFailure as e:
            error_status = {
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "error": "Operation failure",
                "error_type": type(e).__name__,
                "error_message": str(e),
            }

            self.last_check = datetime.utcnow()
            self.last_status = error_status

            logger.error("MongoDB health check failed: %s", error_status)

            raise MongoDBConnectionError(f"MongoDB operation failed: {e}") from e

        except Exception as e:
            error_status = {
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "error": "Unknown error",
                "error_type": type(e).__name__,
                "error_message": str(e),
            }

            self.last_check = datetime.utcnow()
            self.last_status = error_status

            logger.error("MongoDB health check failed: %s", error_status)

            raise MongoDBConnectionError(f"Health check failed: {e}") from e

    def get_last_status(self) -> dict[str, Any] | None:
        """Get last health check status.

        Returns:
            Last health check status or None if never checked
        """
        return self.last_status

    def is_healthy(self) -> bool:
        """Check if MongoDB is healthy based on last check.

        Returns:
            True if healthy, False otherwise
        """
        if not self.last_status:
            return False

        return self.last_status.get("status") == "healthy"

