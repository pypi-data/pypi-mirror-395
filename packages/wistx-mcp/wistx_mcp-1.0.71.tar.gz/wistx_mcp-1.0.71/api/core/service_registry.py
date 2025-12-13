"""Service registry for centralized service management.

This module provides a service registry pattern for advanced service lifecycle management.
It complements the dependency injection system by providing a centralized registry
for services that need more complex initialization or lifecycle management.
"""

import logging
from typing import Any, Dict, Optional, Type, TypeVar

from functools import lru_cache

logger = logging.getLogger(__name__)

T = TypeVar("T")


class ServiceRegistry:
    """Centralized service registry with lazy initialization and lifecycle management.
    
    This registry provides:
    - Lazy service initialization
    - Singleton pattern enforcement
    - Service lifecycle management
    - Service health monitoring
    - Graceful shutdown support
    """

    _services: Dict[Type, Any] = {}
    _initialized: Dict[Type, bool] = {}
    _shutdown_hooks: Dict[Type, callable] = {}

    @classmethod
    def register(
        cls,
        service_type: Type[T],
        factory: Optional[callable] = None,
        shutdown_hook: Optional[callable] = None,
    ) -> None:
        """Register a service type with optional factory and shutdown hook.
        
        Args:
            service_type: Service class type
            factory: Optional factory function to create service instance
            shutdown_hook: Optional cleanup function for service shutdown
        """
        if service_type not in cls._services:
            cls._services[service_type] = None
            cls._initialized[service_type] = False
            if factory:
                cls._services[service_type] = factory
            if shutdown_hook:
                cls._shutdown_hooks[service_type] = shutdown_hook
            logger.debug("Registered service type: %s", service_type.__name__)

    @classmethod
    @lru_cache()
    def get(cls, service_type: Type[T], *args, **kwargs) -> T:
        """Get or create service instance (singleton pattern).
        
        Args:
            service_type: Service class type
            *args: Optional arguments for service initialization
            **kwargs: Optional keyword arguments for service initialization
            
        Returns:
            Service instance (singleton)
        """
        if service_type not in cls._services:
            logger.warning(
                "Service type %s not registered, creating instance directly",
                service_type.__name__
            )
            instance = service_type(*args, **kwargs)
            cls._services[service_type] = instance
            cls._initialized[service_type] = True
            return instance

        if not cls._initialized[service_type]:
            factory = cls._services[service_type]
            if callable(factory) and not isinstance(factory, service_type):
                instance = factory(*args, **kwargs)
            else:
                instance = service_type(*args, **kwargs)
            cls._services[service_type] = instance
            cls._initialized[service_type] = True
            logger.debug("Initialized service: %s", service_type.__name__)

        return cls._services[service_type]

    @classmethod
    def is_initialized(cls, service_type: Type[T]) -> bool:
        """Check if service is initialized.
        
        Args:
            service_type: Service class type
            
        Returns:
            True if service is initialized, False otherwise
        """
        return cls._initialized.get(service_type, False)

    @classmethod
    async def shutdown(cls) -> None:
        """Shutdown all registered services.
        
        Calls shutdown hooks for all initialized services.
        """
        logger.info("Shutting down service registry...")
        for service_type, instance in cls._services.items():
            if cls._initialized.get(service_type, False) and instance:
                shutdown_hook = cls._shutdown_hooks.get(service_type)
                if shutdown_hook:
                    try:
                        if hasattr(shutdown_hook, "__call__"):
                            if hasattr(shutdown_hook, "__await__"):
                                await shutdown_hook(instance)
                            else:
                                shutdown_hook(instance)
                        logger.debug("Shutdown hook executed for: %s", service_type.__name__)
                    except Exception as e:
                        logger.error(
                            "Error executing shutdown hook for %s: %s",
                            service_type.__name__,
                            e,
                            exc_info=True
                        )
        logger.info("Service registry shutdown complete")

    @classmethod
    def get_all_services(cls) -> Dict[Type, Any]:
        """Get all registered services.
        
        Returns:
            Dictionary mapping service types to instances
        """
        return {
            service_type: instance
            for service_type, instance in cls._services.items()
            if cls._initialized.get(service_type, False)
        }

    @classmethod
    def reset(cls) -> None:
        """Reset registry (useful for testing).
        
        Clears all registered services and initialization state.
        """
        cls._services.clear()
        cls._initialized.clear()
        cls._shutdown_hooks.clear()
        logger.debug("Service registry reset")


# Global registry instance
service_registry = ServiceRegistry()

