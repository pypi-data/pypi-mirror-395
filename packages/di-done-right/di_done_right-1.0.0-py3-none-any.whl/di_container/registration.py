"""
Service registration and configuration classes.
"""

from typing import Any, Callable, Optional, Type, TypeVar

from .enums import RegistrationStrategy, ServiceLifetime

T = TypeVar("T")


class ServiceRegistration:
    """Represents a service registration in the DI container."""

    def __init__(
        self,
        service_type: Type[T],
        implementation_type: Optional[Type[T]] = None,
        instance: Optional[T] = None,
        factory: Optional[Callable[..., T]] = None,
        lifetime: ServiceLifetime = ServiceLifetime.TRANSIENT,
        key: Optional[Any] = None,
    ):
        self.service_type = service_type
        self.implementation_type = implementation_type
        self.instance = instance
        self.factory = factory
        self.lifetime = lifetime
        self.key = key

        # Determine registration strategy
        if instance is not None:
            self.strategy = RegistrationStrategy.TYPE_TO_INSTANCE
        elif factory is not None:
            self.strategy = RegistrationStrategy.TYPE_TO_FACTORY
        elif implementation_type is not None:
            self.strategy = RegistrationStrategy.TYPE_TO_TYPE
        else:
            # Default: register type to itself
            self.implementation_type = service_type
            self.strategy = RegistrationStrategy.TYPE_TO_TYPE

    def __repr__(self) -> str:
        key_str = f", key={self.key}" if self.key is not None else ""
        return (
            f"ServiceRegistration("
            f"service_type={self.service_type}, "
            f"implementation_type={self.implementation_type}, "
            f"lifetime={self.lifetime}, "
            f"strategy={self.strategy}{key_str})"
        )


class ServiceRegistry:
    """Manages service registrations."""

    def __init__(self) -> None:
        # Store registrations by (Type, Optional[Key]) tuple
        self._registrations: dict[tuple[Type, Any], ServiceRegistration] = {}

    def register(self, registration: ServiceRegistration) -> None:
        """Register a service."""
        key = (registration.service_type, registration.key)
        self._registrations[key] = registration

    def get_registration(
        self, service_type: Type[T], key: Optional[Any] = None
    ) -> Optional[ServiceRegistration]:
        """Get a service registration by type and optional key."""
        lookup_key = (service_type, key)
        return self._registrations.get(lookup_key)

    def is_registered(self, service_type: Type[T], key: Optional[Any] = None) -> bool:
        """Check if a service type is registered with optional key."""
        lookup_key = (service_type, key)
        return lookup_key in self._registrations

    def get_all_registrations(self) -> dict[tuple[Type, Any], ServiceRegistration]:
        """Get all registrations."""
        return self._registrations.copy()

    def get_registrations_for_type(
        self, service_type: Type[T]
    ) -> list[ServiceRegistration]:
        """Get all registrations for a specific type (regardless of key)."""
        return [
            registration
            for (reg_type, _), registration in self._registrations.items()
            if reg_type == service_type
        ]

    def clear(self) -> None:
        """Clear all registrations."""
        self._registrations.clear()
