"""
Static container manager for global DI container access.
"""

import threading
from typing import Any, Callable, Optional, Type, TypeVar

from .container import DIContainer, DIScope
from .exceptions import DIException

T = TypeVar("T")


class ContainerNotConfiguredException(DIException):
    """Raised when trying to use the container before it's configured."""

    pass


class ServiceProvider:
    """
    Static service provider for global container access.
    Thread-safe singleton pattern for managing DI container.
    """

    _instance: Optional["ServiceProvider"] = None
    _lock = threading.Lock()
    _container: Optional[DIContainer] = None
    _is_configured = False

    def __new__(cls) -> "ServiceProvider":
        """Ensure singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def configure(cls, configuration_func: Callable[[DIContainer], None]) -> None:
        """
        Configure the global container with services.

        Args:
            configuration_func: Function that receives a DIContainer and configures it

        Example:
            def configure_services(container: DIContainer):
                container.register(
                    IUserService, UserService, ServiceLifetime.SINGLETON
                )
                container.register(
                    IRepository, DatabaseRepository, ServiceLifetime.SCOPED
                )

            ServiceProvider.configure(configure_services)
        """
        with cls._lock:
            if cls._is_configured:
                raise DIException("ServiceProvider is already configured")

            cls._container = DIContainer()
            configuration_func(cls._container)
            cls._is_configured = True

    @classmethod
    def get_container(cls) -> DIContainer:
        """Get the configured container."""
        if not cls._is_configured or cls._container is None:
            raise ContainerNotConfiguredException(
                "ServiceProvider not configured. Call "
                "ServiceProvider.configure() first."
            )
        return cls._container

    @classmethod
    def resolve(cls, service_type: Type[T]) -> T:
        """Resolve a service from the global container."""
        return cls.get_container().resolve(service_type)

    @classmethod
    def resolve_keyed(cls, service_type: Type[T], key: Any) -> T:
        """Resolve a keyed service from the global container."""
        return cls.get_container().resolve_keyed(service_type, key)

    @classmethod
    def try_resolve(cls, service_type: Type[T]) -> Optional[T]:
        """Try to resolve a service from the global container."""
        return cls.get_container().try_resolve(service_type)

    @classmethod
    def try_resolve_keyed(cls, service_type: Type[T], key: Any) -> Optional[T]:
        """Try to resolve a keyed service from the global container."""
        return cls.get_container().try_resolve_keyed(service_type, key)

    @classmethod
    def create_scope(cls) -> DIScope:
        """Create a new scope from the global container."""
        return cls.get_container().create_scope()

    @classmethod
    def begin_scope(cls, scope: Optional[DIScope] = None) -> DIScope:
        """Begin a scope in the global container."""
        return cls.get_container().begin_scope(scope)

    @classmethod
    def end_scope(cls) -> None:
        """End the current scope in the global container."""
        cls.get_container().end_scope()

    @classmethod
    def is_configured(cls) -> bool:
        """Check if the service provider is configured."""
        return cls._is_configured

    @classmethod
    def reset(cls) -> None:
        """Reset the service provider (mainly for testing)."""
        with cls._lock:
            cls._container = None
            cls._is_configured = False
            cls._instance = None


# Convenience functions for common operations
def get_service(service_type: Type[T]) -> T:
    """Convenience function to resolve a service."""
    return ServiceProvider.resolve(service_type)


def get_keyed_service(service_type: Type[T], key: Any) -> T:
    """Convenience function to resolve a keyed service."""
    return ServiceProvider.resolve_keyed(service_type, key)


def try_get_service(service_type: Type[T]) -> Optional[T]:
    """Convenience function to try resolving a service."""
    return ServiceProvider.try_resolve(service_type)
