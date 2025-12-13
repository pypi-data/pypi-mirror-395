"""Enhanced Redis client manager with health checks, circuit breaker, retry logic, and metrics.

Supports both Redis URL and Google Memorystore (GCP).
"""

import asyncio
import logging
import time
from enum import Enum
from typing import Any, Callable, Optional, TypeVar

from api.config import settings

logger = logging.getLogger(__name__)

T = TypeVar("T")


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class RedisCircuitBreakerOpenError(Exception):
    """Raised when Redis circuit breaker is open."""

    pass


class RedisClientManager:
    """Enhanced Redis client manager with production-grade features.

    Features:
    - Health checks with periodic ping
    - Circuit breaker pattern
    - Retry logic with exponential backoff
    - Connection pooling
    - Metrics tracking
    - Graceful degradation
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        health_check_interval: int = 30,
        max_retries: int = 3,
        retry_initial_delay: float = 1.0,
        retry_max_delay: float = 10.0,
        connection_pool_size: int = 50,
        socket_connect_timeout: int = 5,
        socket_timeout: int = 5,
    ):
        """Initialize Redis client manager.

        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before attempting recovery
            health_check_interval: Seconds between health checks
            max_retries: Maximum retry attempts for operations
            retry_initial_delay: Initial delay between retries in seconds
            retry_max_delay: Maximum delay between retries in seconds
            connection_pool_size: Maximum connection pool size
            socket_connect_timeout: Socket connection timeout in seconds
            socket_timeout: Socket timeout in seconds
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.health_check_interval = health_check_interval
        self.max_retries = max_retries
        self.retry_initial_delay = retry_initial_delay
        self.retry_max_delay = retry_max_delay
        self.connection_pool_size = connection_pool_size
        self.socket_connect_timeout = socket_connect_timeout
        self.socket_timeout = socket_timeout

        self._client: Optional[Any] = None
        self._lock = asyncio.Lock()
        self._circuit_state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time: Optional[float] = None
        self._last_health_check: Optional[float] = None
        self._health_check_task: Optional[asyncio.Task] = None

        self._metrics = {
            "total_operations": 0,
            "successful_operations": 0,
            "failed_operations": 0,
            "circuit_breaker_opens": 0,
            "retries": 0,
            "health_checks": 0,
            "health_check_failures": 0,
        }

    async def _initialize_client(self) -> Optional[Any]:
        """Initialize Redis client.

        Returns:
            Redis client instance or None if not configured
        """
        if self._client is not None:
            return self._client

        async with self._lock:
            if self._client is not None:
                return self._client

            if not settings.redis_url and not (
                settings.memorystore_enabled and settings.memorystore_host
            ):
                logger.debug("Redis not configured, skipping initialization")
                return None

            try:
                import redis.asyncio as redis

                socket_connect_timeout = self.socket_connect_timeout
                socket_timeout = self.socket_timeout

                if settings.redis_url:
                    self._client = redis.from_url(
                        settings.redis_url,
                        encoding="utf-8",
                        decode_responses=True,
                        socket_connect_timeout=socket_connect_timeout,
                        socket_timeout=socket_timeout,
                        max_connections=self.connection_pool_size,
                    )
                    logger.info("Redis client initialized from REDIS_URL")
                elif settings.memorystore_host:
                    socket_connect_timeout = max(self.socket_connect_timeout, 10)
                    socket_timeout = max(self.socket_timeout, 10)
                    
                    redis_kwargs = {
                        "host": settings.memorystore_host,
                        "port": settings.memorystore_port,
                        "encoding": "utf-8",
                        "decode_responses": True,
                        "socket_connect_timeout": socket_connect_timeout,
                        "socket_timeout": socket_timeout,
                        "socket_keepalive": True,
                        "socket_keepalive_options": {
                            1: 1,
                            3: 10,
                            4: 1,
                        },
                        "health_check_interval": 30,
                        "retry_on_timeout": True,
                        "max_connections": self.connection_pool_size,
                        "single_connection_client": False,
                    }
                    
                    if settings.redis_password:
                        redis_kwargs["password"] = settings.redis_password
                        logger.debug("Redis authentication enabled via REDIS_PASSWORD")
                    
                    self._client = redis.Redis(**redis_kwargs)
                    logger.info(
                        "Redis client initialized for Memorystore at %s:%d (connect_timeout=%d, socket_timeout=%d)",
                        settings.memorystore_host,
                        settings.memorystore_port,
                        socket_connect_timeout,
                        socket_timeout,
                    )

                max_connect_retries = 3
                connect_retry_delay = 2.0
                last_error = None
                
                for attempt in range(max_connect_retries):
                    try:
                        await asyncio.wait_for(
                            self._client.ping(),
                            timeout=socket_connect_timeout + 5,
                        )
                        break
                    except Exception as e:
                        last_error = e
                        if attempt < max_connect_retries - 1:
                            logger.debug(
                                "Redis connection attempt %d/%d failed, retrying in %.1fs: %s",
                                attempt + 1,
                                max_connect_retries,
                                connect_retry_delay,
                                e,
                            )
                            await asyncio.sleep(connect_retry_delay)
                            connect_retry_delay *= 1.5
                        else:
                            raise
                logger.info("Successfully connected to Redis/Memorystore")
                self._circuit_state = CircuitState.CLOSED
                self._failure_count = 0
                self._last_health_check = time.time()

                self._start_health_check_task()
                
                asyncio.create_task(self._perform_health_check())

                return self._client

            except ImportError:
                logger.warning(
                    "redis package not installed. Install with: pip install redis. "
                    "Falling back to in-memory operations."
                )
                return None
            except Exception as e:
                error_type = type(e).__name__
                if "Timeout" in error_type or "timeout" in str(e).lower():
                    logger.warning(
                        "Redis connection timeout (network unreachable or server unavailable). "
                        "Falling back to in-memory mode. Error: %s",
                        e,
                    )
                else:
                    logger.error("Failed to initialize Redis client: %s", e, exc_info=True)
                self._on_failure()
                return None

    def _start_health_check_task(self) -> None:
        """Start background health check task."""
        if self._health_check_task is None or self._health_check_task.done():
            self._health_check_task = asyncio.create_task(self._health_check_loop())

    async def _health_check_loop(self) -> None:
        """Background health check loop."""
        while True:
            try:
                await asyncio.sleep(self.health_check_interval)
                await self._perform_health_check()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.debug("Health check loop error: %s", e)

    async def _perform_health_check(self) -> bool:
        """Perform health check on Redis connection.

        Returns:
            True if healthy, False otherwise
        """
        if self._client is None:
            return False

        try:
            await self._client.ping()
            self._metrics["health_checks"] += 1
            self._last_health_check = time.time()

            if self._circuit_state == CircuitState.HALF_OPEN:
                self._success_count += 1
                if self._success_count >= 2:
                    logger.info("Redis circuit breaker: Recovered (CLOSED)")
                    self._circuit_state = CircuitState.CLOSED
                    self._failure_count = 0
                    self._success_count = 0

            return True
        except Exception as e:
            self._metrics["health_check_failures"] += 1
            logger.warning("Redis health check failed: %s", e)
            self._on_failure()
            return False

    def _on_failure(self) -> None:
        """Handle failure event."""
        self._failure_count += 1
        self._last_failure_time = time.time()
        self._metrics["failed_operations"] += 1

        if self._failure_count >= self.failure_threshold:
            if self._circuit_state != CircuitState.OPEN:
                logger.error(
                    "Redis circuit breaker: Opening circuit (OPEN) after %d failures",
                    self._failure_count,
                )
                self._circuit_state = CircuitState.OPEN
                self._metrics["circuit_breaker_opens"] += 1

    def _on_success(self) -> None:
        """Handle success event."""
        self._metrics["successful_operations"] += 1

        if self._circuit_state == CircuitState.HALF_OPEN:
            self._success_count += 1
            if self._success_count >= 2:
                logger.info("Redis circuit breaker: Recovered (CLOSED)")
                self._circuit_state = CircuitState.CLOSED
                self._failure_count = 0
                self._success_count = 0
        elif self._circuit_state == CircuitState.CLOSED:
            self._failure_count = 0

    async def _check_circuit_breaker(self) -> None:
        """Check circuit breaker state and raise if open."""
        if self._circuit_state == CircuitState.OPEN:
            if (
                self._last_failure_time
                and time.time() - self._last_failure_time > self.recovery_timeout
            ):
                logger.info("Redis circuit breaker: Attempting recovery (HALF_OPEN)")
                self._circuit_state = CircuitState.HALF_OPEN
                self._success_count = 0
            else:
                raise RedisCircuitBreakerOpenError(
                    f"Redis circuit breaker is OPEN. "
                    f"Last failure: {self._last_failure_time}"
                )

    async def _retry_with_backoff(
        self, func: Callable[..., T], *args: Any, **kwargs: Any
    ) -> T:
        """Execute function with retry and exponential backoff.

        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result

        Raises:
            Exception: If all retries fail
        """
        delay = self.retry_initial_delay
        last_exception: Optional[Exception] = None

        for attempt in range(self.max_retries):
            try:
                await self._check_circuit_breaker()
                result = await func(*args, **kwargs)
                self._on_success()
                return result
            except RedisCircuitBreakerOpenError:
                raise
            except Exception as e:
                last_exception = e
                self._metrics["retries"] += 1

                if attempt < self.max_retries - 1:
                    logger.debug(
                        "Redis operation failed (attempt %d/%d), retrying in %.2fs: %s",
                        attempt + 1,
                        self.max_retries,
                        delay,
                        e,
                    )
                    await asyncio.sleep(delay)
                    delay = min(delay * 2, self.retry_max_delay)
                else:
                    logger.warning(
                        "Redis operation failed after %d attempts: %s",
                        self.max_retries,
                        e,
                    )

        self._on_failure()
        if last_exception:
            raise last_exception
        raise RuntimeError("Redis operation failed after retries")

    async def get_client(self) -> Optional[Any]:
        """Get Redis client instance.

        Returns:
            Redis client or None if not configured
        """
        if self._client is None:
            await self._initialize_client()
        return self._client

    async def execute(
        self, operation: Callable[..., T], *args: Any, **kwargs: Any
    ) -> T:
        """Execute Redis operation with circuit breaker and retry logic.

        Args:
            operation: Redis operation to execute
            *args: Operation arguments
            **kwargs: Operation keyword arguments

        Returns:
            Operation result

        Raises:
            RedisCircuitBreakerOpenError: If circuit breaker is open
            Exception: If operation fails after retries
        """
        self._metrics["total_operations"] += 1

        client = await self.get_client()
        if client is None:
            raise RuntimeError("Redis client not available")

        async def _execute_operation() -> T:
            return await operation(client, *args, **kwargs)

        return await self._retry_with_backoff(_execute_operation)

    async def ping(self) -> bool:
        """Check Redis connection health.

        Returns:
            True if healthy, False otherwise
        """
        try:
            client = await self.get_client()
            if client is None:
                return False

            await client.ping()
            return True
        except Exception:
            return False

    def get_health_status(self) -> dict[str, Any]:
        """Get Redis health status.

        Returns:
            Health status dictionary
        """
        if self._client is None:
            is_healthy = False
        elif self._circuit_state == CircuitState.OPEN:
            is_healthy = False
        elif self._last_health_check is None:
            is_healthy = False
        else:
            time_since_last_check = time.time() - self._last_health_check
            max_stale_time = self.health_check_interval * 3
            is_healthy = (
                time_since_last_check < max_stale_time
                and self._circuit_state == CircuitState.CLOSED
            )

        return {
            "healthy": is_healthy,
            "circuit_state": self._circuit_state.value,
            "failure_count": self._failure_count,
            "last_failure_time": self._last_failure_time,
            "last_health_check": self._last_health_check,
            "client_initialized": self._client is not None,
            "metrics": self._metrics.copy(),
        }

    def get_stats(self) -> dict[str, Any]:
        """Get Redis client statistics.

        Returns:
            Statistics dictionary
        """
        return {
            "circuit_state": self._circuit_state.value,
            "failure_count": self._failure_count,
            "success_count": self._success_count,
            "last_failure_time": self._last_failure_time,
            "last_health_check": self._last_health_check,
            "client_initialized": self._client is not None,
            "metrics": self._metrics.copy(),
            "configuration": {
                "failure_threshold": self.failure_threshold,
                "recovery_timeout": self.recovery_timeout,
                "health_check_interval": self.health_check_interval,
                "max_retries": self.max_retries,
                "connection_pool_size": self.connection_pool_size,
            },
        }

    async def close(self) -> None:
        """Close Redis client connection."""
        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass

        if self._client:
            try:
                await self._client.aclose()
            except Exception as e:
                logger.warning("Error closing Redis client: %s", e)
            finally:
                self._client = None


_redis_manager: Optional[RedisClientManager] = None
_manager_lock = asyncio.Lock()


async def get_redis_manager() -> Optional[RedisClientManager]:
    """Get global Redis client manager instance.

    Returns:
        RedisClientManager instance or None if Redis not configured
    """
    global _redis_manager

    if _redis_manager is not None:
        return _redis_manager

    async with _manager_lock:
        if _redis_manager is not None:
            return _redis_manager

        redis_failure_threshold = getattr(
            settings, "redis_circuit_breaker_failure_threshold", 5
        )
        redis_recovery_timeout = getattr(
            settings, "redis_circuit_breaker_recovery_timeout", 60
        )
        redis_health_check_interval = getattr(
            settings, "redis_health_check_interval", 30
        )
        redis_max_retries = getattr(settings, "redis_max_retries", 3)
        redis_retry_initial_delay = getattr(settings, "redis_retry_initial_delay", 1.0)
        redis_retry_max_delay = getattr(settings, "redis_retry_max_delay", 10.0)
        redis_connection_pool_size = getattr(
            settings, "redis_connection_pool_size", 50
        )
        redis_socket_connect_timeout = getattr(
            settings, "redis_socket_connect_timeout", 5
        )
        redis_socket_timeout = getattr(settings, "redis_socket_timeout", 5)

        _redis_manager = RedisClientManager(
            failure_threshold=redis_failure_threshold,
            recovery_timeout=redis_recovery_timeout,
            health_check_interval=redis_health_check_interval,
            max_retries=redis_max_retries,
            retry_initial_delay=redis_retry_initial_delay,
            retry_max_delay=redis_retry_max_delay,
            connection_pool_size=redis_connection_pool_size,
            socket_connect_timeout=redis_socket_connect_timeout,
            socket_timeout=redis_socket_timeout,
        )

        return _redis_manager


async def get_redis_client() -> Optional[Any]:
    """Get Redis client instance (convenience function).

    Returns:
        Redis client or None if not configured
    """
    manager = await get_redis_manager()
    if manager:
        return await manager.get_client()
    return None

