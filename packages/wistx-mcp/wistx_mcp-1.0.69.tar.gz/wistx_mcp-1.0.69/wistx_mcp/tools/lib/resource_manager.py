"""Resource manager for tracking and cleaning up MCP server resources."""

import asyncio
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class ResourceManager:
    """Manages server resources and provides cleanup on shutdown."""

    def __init__(self) -> None:
        """Initialize resource manager."""
        self._mongodb_clients: list[Any] = []
        self._http_clients: list[Any] = []
        self._redis_clients: list[Any] = []
        self._shutdown_event: Optional[asyncio.Event] = None
        self._cleanup_lock = asyncio.Lock()
        self._subscriptions: dict[str, set[str]] = {}
        self._subscription_lock = asyncio.Lock()

    def register_mongodb_client(self, client: Any) -> None:
        """Register a MongoDB client for cleanup.

        Args:
            client: MongoDB client instance
        """
        if client not in self._mongodb_clients:
            self._mongodb_clients.append(client)
            logger.debug("Registered MongoDB client for cleanup")

    def register_http_client(self, client: Any) -> None:
        """Register an HTTP client for cleanup.

        Args:
            client: HTTP client instance
        """
        if client not in self._http_clients:
            self._http_clients.append(client)
            logger.debug("Registered HTTP client for cleanup")

    def register_redis_client(self, client: Any) -> None:
        """Register a Redis client for cleanup.

        Args:
            client: Redis client instance
        """
        if not hasattr(self, "_redis_clients"):
            self._redis_clients: list[Any] = []
        if client not in self._redis_clients:
            self._redis_clients.append(client)
            logger.debug("Registered Redis client for cleanup")

    def get_shutdown_event(self) -> asyncio.Event:
        """Get or create shutdown event.

        Returns:
            Shutdown event
        """
        if self._shutdown_event is None:
            self._shutdown_event = asyncio.Event()
        return self._shutdown_event

    async def _cleanup_mongodb_client(self, client: Any) -> None:
        """Clean up a single MongoDB client.

        Args:
            client: MongoDB client instance
        """
        try:
            if hasattr(client, "disconnect"):
                await client.disconnect()
            elif hasattr(client, "close"):
                if asyncio.iscoroutinefunction(client.close):
                    await client.close()
                else:
                    client.close()
            logger.debug("Closed MongoDB client")
        except Exception as e:
            logger.warning("Error closing MongoDB client: %s", e)
            raise

    async def _cleanup_http_client(self, client: Any) -> None:
        """Clean up a single HTTP client.

        Args:
            client: HTTP client instance
        """
        try:
            if hasattr(client, "close"):
                if asyncio.iscoroutinefunction(client.close):
                    await client.close()
                else:
                    client.close()
            elif hasattr(client, "aclose"):
                await client.aclose()
            logger.debug("Closed HTTP client")
        except Exception as e:
            logger.warning("Error closing HTTP client: %s", e)
            raise

    async def _cleanup_redis_client(self, client: Any) -> None:
        """Clean up a single Redis client.

        Args:
            client: Redis client instance
        """
        try:
            if hasattr(client, "aclose"):
                if asyncio.iscoroutinefunction(client.aclose):
                    await client.aclose()
                else:
                    client.aclose()
            elif hasattr(client, "close"):
                if asyncio.iscoroutinefunction(client.close):
                    await client.close()
                else:
                    client.close()
            logger.debug("Closed Redis client")
        except Exception as e:
            logger.warning("Error closing Redis client: %s", e)
            raise

    async def cleanup_all(self) -> None:
        """Clean up all registered resources atomically with proper error handling.

        This method is idempotent and can be called multiple times safely.
        All cleanup operations are executed concurrently, and failures are collected.
        """
        async with self._cleanup_lock:
            if not self._mongodb_clients and not self._http_clients and not self._redis_clients:
                logger.debug("No resources to clean up")
                if self._shutdown_event:
                    self._shutdown_event.set()
                return

            logger.info("Starting resource cleanup...")

            cleanup_tasks = []
            cleanup_metadata = []

            for client in self._mongodb_clients:
                cleanup_tasks.append(self._cleanup_mongodb_client(client))
                cleanup_metadata.append(("mongodb", client))

            for client in self._http_clients:
                cleanup_tasks.append(self._cleanup_http_client(client))
                cleanup_metadata.append(("http", client))

            for client in self._redis_clients:
                cleanup_tasks.append(self._cleanup_redis_client(client))
                cleanup_metadata.append(("redis", client))

            if cleanup_tasks:
                results = await asyncio.gather(*cleanup_tasks, return_exceptions=True)

                errors = []
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        client_type, client = cleanup_metadata[i]
                        errors.append((client_type, client, result))

                if errors:
                    logger.warning(
                        "Some resources had errors during cleanup: %d errors",
                        len(errors),
                    )
                    for client_type, client, error in errors[:5]:
                        logger.debug(
                            "Cleanup error for %s client: %s",
                            client_type,
                            error,
                        )

            self._mongodb_clients.clear()
            self._http_clients.clear()
            self._redis_clients.clear()

            if self._shutdown_event:
                self._shutdown_event.set()

            logger.info("Resource cleanup completed")

    async def subscribe(self, uri: str, user_id: str) -> None:
        """Subscribe user to resource change notifications.

        Args:
            uri: Resource URI
            user_id: User identifier
        """
        async with self._subscription_lock:
            if uri not in self._subscriptions:
                self._subscriptions[uri] = set()
            self._subscriptions[uri].add(user_id)
            logger.debug("User %s subscribed to resource %s", user_id[:8] if len(user_id) > 8 else user_id, uri)

    async def unsubscribe(self, uri: str, user_id: str) -> None:
        """Unsubscribe user from resource change notifications.

        Args:
            uri: Resource URI
            user_id: User identifier
        """
        async with self._subscription_lock:
            if uri in self._subscriptions:
                self._subscriptions[uri].discard(user_id)
                if not self._subscriptions[uri]:
                    del self._subscriptions[uri]
            logger.debug("User %s unsubscribed from resource %s", user_id[:8] if len(user_id) > 8 else user_id, uri)

    async def notify_subscribers(self, uri: str) -> None:
        """Notify all subscribers of resource changes.

        Args:
            uri: Resource URI that changed
        """
        async with self._subscription_lock:
            subscribers = self._subscriptions.get(uri, set()).copy()

        if subscribers:
            logger.info("Notifying %d subscribers of change to %s", len(subscribers), uri)


_resource_manager: Optional[ResourceManager] = None
_resource_manager_lock = asyncio.Lock()


async def get_resource_manager() -> ResourceManager:
    """Get or create global resource manager instance.

    Returns:
        Resource manager instance
    """
    global _resource_manager
    async with _resource_manager_lock:
        if _resource_manager is None:
            _resource_manager = ResourceManager()
        return _resource_manager

