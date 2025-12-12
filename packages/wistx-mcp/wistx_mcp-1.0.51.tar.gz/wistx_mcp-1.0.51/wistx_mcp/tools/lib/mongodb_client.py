"""MongoDB client for MCP tools."""

import asyncio
import logging
from typing import Any, Callable, Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from wistx_mcp.config import settings
from wistx_mcp.tools.lib.circuit_breaker import CircuitBreaker, CircuitBreakerError
from wistx_mcp.tools.lib.constants import (
    MONGODB_CIRCUIT_BREAKER_FAILURE_THRESHOLD,
    MONGODB_CIRCUIT_BREAKER_RECOVERY_TIMEOUT_SECONDS,
    MONGODB_HEALTH_CHECK_TIMEOUT_SECONDS,
    MONGODB_PING_TIMEOUT_SECONDS,
    MONGODB_MAX_RETRIES,
    MONGODB_RETRY_DELAY_SECONDS,
)

logger = logging.getLogger(__name__)

_global_mongodb_client: Optional["MongoDBClient"] = None
_mongodb_client_lock = asyncio.Lock()

_mongodb_circuit_breaker = CircuitBreaker(
    failure_threshold=MONGODB_CIRCUIT_BREAKER_FAILURE_THRESHOLD,
    recovery_timeout=MONGODB_CIRCUIT_BREAKER_RECOVERY_TIMEOUT_SECONDS,
    expected_exceptions=(RuntimeError, ConnectionError, TimeoutError),
    name="mongodb",
)


async def execute_mongodb_operation(
    operation: Callable[[], Any],
    timeout: float = 10.0,
    max_retries: int = 3,
) -> Any:
    """Execute MongoDB operation with circuit breaker and retry logic.

    Args:
        operation: Async operation coroutine to execute (callable that returns coroutine)
        timeout: Operation timeout in seconds
        max_retries: Maximum number of retry attempts

    Returns:
        Operation result

    Raises:
        CircuitBreakerError: If circuit breaker is open
        RuntimeError: If operation fails after retries
    """
    from wistx_mcp.tools.lib.retry_utils import with_timeout_and_retry

    async def _execute_with_circuit_breaker() -> Any:
        async def _call_operation() -> Any:
            if asyncio.iscoroutinefunction(operation):
                return await operation()
            elif asyncio.iscoroutine(operation):
                return await operation
            else:
                result = operation()
                if asyncio.iscoroutine(result):
                    return await result
                return result

        return await _mongodb_circuit_breaker.call(_call_operation)

    return await with_timeout_and_retry(
        _execute_with_circuit_breaker,
        timeout_seconds=timeout,
        max_attempts=max_retries,
        retryable_exceptions=(RuntimeError, ConnectionError, TimeoutError, CircuitBreakerError),
    )


class MongoDBClient:
    """MongoDB client wrapper for MCP tools with connection pooling and retry logic."""

    def __init__(self):
        """Initialize MongoDB client."""
        self.client: Optional[AsyncIOMotorClient] = None
        self.database: Optional[AsyncIOMotorDatabase] = None
        self._max_retries = MONGODB_MAX_RETRIES
        self._retry_delay = MONGODB_RETRY_DELAY_SECONDS
        self._registered = False

    async def __aenter__(self) -> "MongoDBClient":
        """Async context manager entry.

        Returns:
            MongoDBClient instance
        """
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit.

        Args:
            exc_type: Exception type
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        await self.disconnect()

    async def connect(self) -> None:
        """Connect to MongoDB with proper connection management.

        Includes:
        - Connection pooling (max 50, min 10)
        - Retry logic for transient failures
        - Health checks with timeout
        - Connection string validation

        Raises:
            RuntimeError: If connection fails after retries
        """
        if self.client is None:
            try:
                if not settings.mongodb_url:
                    raise ValueError("MongoDB connection string is required. Set MONGODB_URI environment variable.")
                
                connection_string = str(settings.mongodb_url).strip().rstrip("/")
                
                if not connection_string:
                    raise ValueError("MongoDB connection string is required")

                api_settings = None
                try:
                    import importlib.util
                    import sys
                    import logging
                    import io
                    import os
                    
                    spec = importlib.util.find_spec("api.config")
                    if spec is None:
                        raise ImportError("api.config module not found")
                    
                    module = importlib.util.module_from_spec(spec)
                    
                    api_config_logger = logging.getLogger("api.config")
                    root_logger = logging.getLogger()
                    original_api_level = api_config_logger.level
                    original_root_level = root_logger.level
                    
                    original_stderr = sys.stderr
                    stderr_buffer = io.StringIO()
                    
                    try:
                        api_config_logger.setLevel(logging.CRITICAL + 1)
                        root_logger.setLevel(logging.CRITICAL + 1)
                        sys.stderr = stderr_buffer
                        
                        try:
                            spec.loader.exec_module(module)
                            if hasattr(module, "settings"):
                                api_settings = module.settings
                        except SystemExit:
                            pass
                        except Exception:
                            pass
                    finally:
                        sys.stderr = original_stderr
                        api_config_logger.setLevel(original_api_level)
                        root_logger.setLevel(original_root_level)
                        
                except ImportError:
                    pass
                except Exception:
                    pass
                
                if api_settings is None:
                    logger.debug("API config not available, using default MongoDB connection options")

                if api_settings:
                    try:
                        motor_options = {
                            "maxPoolSize": api_settings.mongodb_max_pool_size,
                            "minPoolSize": api_settings.mongodb_min_pool_size,
                            "maxIdleTimeMS": api_settings.mongodb_max_idle_time_ms,
                            "serverSelectionTimeoutMS": api_settings.mongodb_server_selection_timeout_ms,
                            "connectTimeoutMS": api_settings.mongodb_connect_timeout_ms,
                            "socketTimeoutMS": api_settings.mongodb_socket_timeout_ms,
                            "retryWrites": api_settings.mongodb_retry_writes,
                            "retryReads": True,
                            "heartbeatFrequencyMS": api_settings.mongodb_heartbeat_frequency_ms,
                        }

                        read_pref_map = {
                            "primary": "primary",
                            "primarypreferred": "primaryPreferred",
                            "secondary": "secondary",
                            "secondarypreferred": "secondaryPreferred",
                            "nearest": "nearest",
                        }
                        read_pref_str = api_settings.mongodb_read_preference.lower()
                        motor_options["readPreference"] = read_pref_map.get(read_pref_str, "secondaryPreferred")

                        self.client = AsyncIOMotorClient(connection_string, **motor_options)
                        self.database = self.client[settings.mongodb_database]

                        if not self._registered:
                            try:
                                from wistx_mcp.tools.lib.resource_manager import get_resource_manager
                                resource_manager = await get_resource_manager()
                                resource_manager.register_mongodb_client(self)
                                self._registered = True
                                logger.debug("MongoDB client registered with resource manager")
                            except (ImportError, AttributeError, RuntimeError) as e:
                                logger.warning("Could not register MongoDB client with resource manager: %s", e)
                            except Exception as e:
                                logger.warning("Unexpected error registering MongoDB client: %s", e, exc_info=True)

                        for attempt in range(self._max_retries):
                            try:
                                await asyncio.wait_for(
                                    self.client.admin.command("ping"),
                                    timeout=MONGODB_PING_TIMEOUT_SECONDS,
                                )
                                logger.info("Connected to MongoDB: %s", settings.mongodb_database)
                                return
                            except asyncio.TimeoutError:
                                if attempt < self._max_retries - 1:
                                    logger.warning(
                                        "MongoDB ping timeout (attempt %d/%d), retrying...",
                                        attempt + 1,
                                        self._max_retries,
                                    )
                                    await asyncio.sleep(self._retry_delay * (attempt + 1))
                                else:
                                    raise RuntimeError("MongoDB connection timeout after retries")
                            except (asyncio.TimeoutError, ConnectionError, RuntimeError) as e:
                                if attempt < self._max_retries - 1:
                                    logger.warning(
                                        "MongoDB connection error (attempt %d/%d): %s, retrying...",
                                        attempt + 1,
                                        self._max_retries,
                                        e,
                                    )
                                    await asyncio.sleep(self._retry_delay * (attempt + 1))
                                else:
                                    raise RuntimeError(f"Failed to connect to MongoDB after retries: {e}") from e
                    except Exception as e:
                        logger.debug("Error using API config settings, falling back to defaults: %s", e)
                        api_settings = None

                if not api_settings:
                    logger.debug("Using default MongoDB connection options")
                    motor_options = {
                        "retryWrites": True,
                        "retryReads": True,
                    }
                    self.client = AsyncIOMotorClient(connection_string, **motor_options)
                    self.database = self.client[settings.mongodb_database]

                    if not self._registered:
                        try:
                            from wistx_mcp.tools.lib.resource_manager import get_resource_manager
                            resource_manager = await get_resource_manager()
                            resource_manager.register_mongodb_client(self)
                            self._registered = True
                            logger.debug("MongoDB client registered with resource manager")
                        except (ImportError, AttributeError, RuntimeError) as e:
                            logger.warning("Could not register MongoDB client with resource manager: %s", e)
                        except Exception as e:
                            logger.warning("Unexpected error registering MongoDB client: %s", e, exc_info=True)

                    for attempt in range(self._max_retries):
                        try:
                            await asyncio.wait_for(
                                self.client.admin.command("ping"),
                                timeout=MONGODB_PING_TIMEOUT_SECONDS,
                            )
                            logger.info("Connected to MongoDB: %s", settings.mongodb_database)
                            return
                        except asyncio.TimeoutError:
                            if attempt < self._max_retries - 1:
                                logger.warning(
                                    "MongoDB ping timeout (attempt %d/%d), retrying...",
                                    attempt + 1,
                                    self._max_retries,
                                )
                                await asyncio.sleep(self._retry_delay * (attempt + 1))
                            else:
                                raise RuntimeError("MongoDB connection timeout after retries")
                        except (asyncio.TimeoutError, ConnectionError, RuntimeError) as e:
                            if attempt < self._max_retries - 1:
                                logger.warning(
                                    "MongoDB connection error (attempt %d/%d): %s, retrying...",
                                    attempt + 1,
                                    self._max_retries,
                                    e,
                                )
                                await asyncio.sleep(self._retry_delay * (attempt + 1))
                            else:
                                raise RuntimeError(f"Failed to connect to MongoDB after retries: {e}") from e
            except (ValueError, RuntimeError, ConnectionError) as e:
                logger.error("Failed to initialize MongoDB client: %s", e, exc_info=True)
                if self.client is not None:
                    self.client.close()
                    self.client = None
                raise RuntimeError(f"Failed to initialize MongoDB client: {e}") from e

    async def disconnect(self) -> None:
        """Disconnect from MongoDB and clean up resources."""
        if self.client is not None:
            try:
                self.client.close()
                logger.debug("MongoDB client disconnected")
            except (RuntimeError, ConnectionError) as e:
                logger.warning("Error closing MongoDB client: %s", e)
            finally:
                self.client = None
                self.database = None

    async def health_check(self) -> bool:
        """Perform health check on MongoDB connection.

        Returns:
            True if connection is healthy, False otherwise
        """
        if self.client is None or self.database is None:
            return False

        async def _ping() -> bool:
            await asyncio.wait_for(
                self.client.admin.command("ping"),
                timeout=MONGODB_HEALTH_CHECK_TIMEOUT_SECONDS,
            )
            return True

        try:
            return await _mongodb_circuit_breaker.call(_ping)
        except CircuitBreakerError:
            logger.warning("MongoDB circuit breaker is open")
            return False
        except (asyncio.TimeoutError, ConnectionError, RuntimeError) as e:
            logger.warning("MongoDB health check failed: %s", e)
            return False

    async def _ensure_connected(self) -> None:
        """Ensure MongoDB connection is established.

        Raises:
            RuntimeError: If connection cannot be established
            CircuitBreakerError: If circuit breaker is open
        """
        async def _connect() -> None:
            if self.client is None or self.database is None:
                await self.connect()
            elif not await self.health_check():
                logger.warning("MongoDB connection unhealthy, reconnecting...")
                await self.connect()

        try:
            await _mongodb_circuit_breaker.call(_connect)
        except CircuitBreakerError as e:
            logger.error("MongoDB circuit breaker is open: %s", e)
            raise RuntimeError("MongoDB service temporarily unavailable") from e

    async def get_pricing(
        self,
        cloud: str,
        service: str,
        instance_type: str,
        region: str | None = None,
        pricing_category: str = "OnDemand",
        timeout: float = 10.0,
    ) -> dict[str, Any] | None:
        """Get pricing data for a resource from cost_data_focus collection.

        Args:
            cloud: Cloud provider (aws, gcp, azure, oracle, alibaba)
            service: Service name (rds, ec2, s3, etc.)
            instance_type: Instance/resource type (db.t3.medium, etc.)
            region: Optional region ID (us-east-1, us-central1, etc.)
            pricing_category: Pricing category (OnDemand, Reserved, Spot, etc.)
            timeout: Operation timeout in seconds (default: 10.0)

        Returns:
            Pricing data dictionary with monthly_cost, hourly_cost, etc., or None if not found

        Raises:
            CircuitBreakerError: If circuit breaker is open
        """
        async def _execute_query() -> dict[str, Any] | None:
            await self._ensure_connected()

            from wistx_mcp.tools.lib.mongodb_utils import escape_regex_for_mongodb

            collection = self.database.cost_data_focus

            escaped_service = escape_regex_for_mongodb(service)
            escaped_instance_type = escape_regex_for_mongodb(instance_type)

            query_filter: dict[str, Any] = {
                "provider": cloud.lower(),
                "service_name": {"$regex": escaped_service, "$options": "i"},
                "resource_type": {"$regex": escaped_instance_type, "$options": "i"},
                "pricing_category": pricing_category,
            }

            if region:
                query_filter["region_id"] = region

            cursor = collection.find(query_filter).sort("last_updated", -1).limit(1)
            record = await asyncio.wait_for(cursor.to_list(length=1), timeout=timeout)

            if not record:
                logger.warning(
                    "No pricing data found for %s:%s:%s in %s",
                    cloud,
                    service,
                    instance_type,
                    region or "any region",
                )
                return None

            cost_record = record[0]

            list_unit_price = float(cost_record.get("list_unit_price", 0))
            pricing_unit = cost_record.get("pricing_unit", "Hrs")
            effective_cost = float(cost_record.get("effective_cost", list_unit_price))

            monthly_cost = self._calculate_monthly_cost(
                list_unit_price, pricing_unit, effective_cost
            )

            return {
                "monthly_cost": monthly_cost,
                "hourly_cost": list_unit_price if pricing_unit == "Hrs" else monthly_cost / 730,
                "pricing_unit": pricing_unit,
                "list_unit_price": list_unit_price,
                "effective_cost": effective_cost,
                "region_id": cost_record.get("region_id"),
                "pricing_category": cost_record.get("pricing_category"),
                "service_name": cost_record.get("service_name"),
                "resource_type": cost_record.get("resource_type"),
                "billing_currency": cost_record.get("billing_currency", "USD"),
            }

        try:
            return await _mongodb_circuit_breaker.call(_execute_query)
        except CircuitBreakerError as e:
            logger.error("MongoDB circuit breaker is open: %s", e)
            raise RuntimeError("MongoDB service temporarily unavailable") from e
        except (RuntimeError, ConnectionError, TimeoutError) as e:
            logger.error(
                "Error querying pricing data: %s",
                e,
                exc_info=True,
            )
            raise
        except Exception as e:
            logger.error(
                "Unexpected error querying pricing data: %s",
                e,
                exc_info=True,
            )
            return None

    def _calculate_monthly_cost(
        self,
        list_unit_price: float,
        pricing_unit: str,
        effective_cost: float,
    ) -> float:
        """Calculate monthly cost from unit price and pricing unit.

        Args:
            list_unit_price: Unit price
            pricing_unit: Pricing unit (Hrs, GB-Mo, Requests, etc.)
            effective_cost: Effective cost (may differ from list_unit_price)

        Returns:
            Monthly cost in USD
        """
        unit_lower = pricing_unit.lower()

        if "hr" in unit_lower or "hour" in unit_lower:
            return effective_cost * 730
        elif "gb-mo" in unit_lower or "gb/month" in unit_lower:
            return effective_cost
        elif "mo" in unit_lower or "month" in unit_lower:
            return effective_cost
        elif "request" in unit_lower:
            return effective_cost * 1_000_000
        elif "one-time" in unit_lower or "one time" in unit_lower:
            return effective_cost / 12
        else:
            logger.warning("Unknown pricing unit: %s, assuming hourly", pricing_unit)
            return effective_cost * 730


async def get_mongodb_client() -> MongoDBClient:
    """Get or create global MongoDB client instance.

    Returns:
        MongoDBClient instance (singleton)
    """
    global _global_mongodb_client

    async with _mongodb_client_lock:
        if _global_mongodb_client is None:
            _global_mongodb_client = MongoDBClient()
            await _global_mongodb_client.connect()

            try:
                from wistx_mcp.tools.lib.resource_manager import get_resource_manager
                resource_manager = await get_resource_manager()
                resource_manager.register_mongodb_client(_global_mongodb_client)
            except Exception as e:
                logger.debug("Could not register MongoDB client with resource manager: %s", e)

        return _global_mongodb_client

