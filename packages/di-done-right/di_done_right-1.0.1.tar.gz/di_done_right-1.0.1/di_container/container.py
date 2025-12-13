"""
Main DI container implementation.
"""

import inspect
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar

from .enums import RegistrationStrategy, ServiceLifetime
from .exceptions import (
    CircularDependencyException,
    InvalidRegistrationException,
    ScopeException,
    ServiceNotRegisteredException,
)
from .registration import ServiceRegistration, ServiceRegistry

T = TypeVar("T")


class DIScope:
    """Represents a scope for scoped services."""

    def __init__(self) -> None:
        self._scoped_instances: Dict[tuple[Type, Any], Any] = {}

    def get_scoped_instance(
        self, service_type: Type[T], key: Optional[Any] = None
    ) -> Optional[T]:
        """Get a scoped instance if it exists."""
        scope_key = (service_type, key)
        return self._scoped_instances.get(scope_key)

    def set_scoped_instance(
        self, service_type: Type[T], key: Optional[Any], instance: T
    ) -> None:
        """Set a scoped instance."""
        scope_key = (service_type, key)
        self._scoped_instances[scope_key] = instance

    def dispose(self) -> None:
        """Dispose of all scoped instances."""
        for instance in self._scoped_instances.values():
            if hasattr(instance, "dispose"):
                instance.dispose()
        self._scoped_instances.clear()


class DIContainer:
    """Main dependency injection container."""

    def __init__(self) -> None:
        self._registry = ServiceRegistry()
        self._singleton_instances: Dict[tuple[Type, Any], Any] = {}
        self._current_scope: Optional[DIScope] = None
        self._resolution_stack: List[tuple[Type, Any]] = []

    def register(
        self,
        service_type: Type[T],
        implementation_type: Optional[Type[T]] = None,
        lifetime: ServiceLifetime = ServiceLifetime.TRANSIENT,
    ) -> "DIContainer":
        """
        Register a service type with an implementation type.

        Args:
            service_type: The service type to register (interface or concrete type)
            implementation_type: The implementation type.
            If None, service_type will be registered to itself
            lifetime: The service lifetime (default: TRANSIENT)

        Examples:
            # Register interface to implementation
            container.register(IUserService, UserService, ServiceLifetime.SINGLETON)

            # Register concrete type to itself
            container.register(UserService, lifetime=ServiceLifetime.SINGLETON)
            container.register(DatabaseContext)  # Uses default TRANSIENT lifetime
        """
        registration = ServiceRegistration(
            service_type=service_type,
            implementation_type=implementation_type,
            lifetime=lifetime,
        )
        self._registry.register(registration)
        return self

    def register_keyed(
        self,
        service_type: Type[T],
        key: Any,
        implementation_type: Optional[Type[T]] = None,
        lifetime: ServiceLifetime = ServiceLifetime.TRANSIENT,
    ) -> "DIContainer":
        """
        Register a keyed service type with an implementation type.

        Args:
            service_type: The service type to register
            key: The key to associate with this registration
            implementation_type: The implementation type. If None,
                service_type will be registered to itself
            lifetime: The service lifetime (default: TRANSIENT)

        Examples:
            # Register multiple implementations of the same interface
            container.register_keyed(IPaymentService, "paypal", PayPalService)
            container.register_keyed(IPaymentService, "stripe", StripeService)

            # Register keyed concrete types
            container.register_keyed(DatabaseService, "primary", PrimaryDbService)
            container.register_keyed(DatabaseService, "secondary", SecondaryDbService)
        """
        registration = ServiceRegistration(
            service_type=service_type,
            implementation_type=implementation_type,
            lifetime=lifetime,
            key=key,
        )
        self._registry.register(registration)
        return self

    def register_instance(self, service_type: Type[T], instance: T) -> "DIContainer":
        """Register a service type with a specific instance."""
        registration = ServiceRegistration(
            service_type=service_type,
            instance=instance,
            lifetime=ServiceLifetime.SINGLETON,
        )
        self._registry.register(registration)
        return self

    def register_keyed_instance(
        self, service_type: Type[T], key: Any, instance: T
    ) -> "DIContainer":
        """Register a keyed service type with a specific instance."""
        registration = ServiceRegistration(
            service_type=service_type,
            instance=instance,
            lifetime=ServiceLifetime.SINGLETON,
            key=key,
        )
        self._registry.register(registration)
        return self

    def register_factory(
        self,
        service_type: Type[T],
        factory: Callable[..., T],
        lifetime: ServiceLifetime = ServiceLifetime.TRANSIENT,
    ) -> "DIContainer":
        """Register a service type with a factory function."""
        registration = ServiceRegistration(
            service_type=service_type, factory=factory, lifetime=lifetime
        )
        self._registry.register(registration)
        return self

    def register_keyed_factory(
        self,
        service_type: Type[T],
        key: Any,
        factory: Callable[..., T],
        lifetime: ServiceLifetime = ServiceLifetime.TRANSIENT,
    ) -> "DIContainer":
        """Register a keyed service type with a factory function."""
        registration = ServiceRegistration(
            service_type=service_type, factory=factory, lifetime=lifetime, key=key
        )
        self._registry.register(registration)
        return self

    def resolve(self, service_type: Type[T]) -> T:
        """Resolve a service instance."""
        try:
            return self._resolve_internal(service_type)
        finally:
            self._resolution_stack.clear()

    def resolve_keyed(self, service_type: Type[T], key: Any) -> T:
        """Resolve a keyed service instance."""
        try:
            return self._resolve_keyed_internal(service_type, key)
        finally:
            self._resolution_stack.clear()

    def try_resolve(self, service_type: Type[T]) -> Optional[T]:
        """Try to resolve a service instance, return None if not registered."""
        try:
            return self._resolve_internal(service_type)
        except ServiceNotRegisteredException:
            return None
        finally:
            self._resolution_stack.clear()

    def try_resolve_keyed(self, service_type: Type[T], key: Any) -> Optional[T]:
        """Try to resolve a keyed service instance, return None if not registered."""
        try:
            return self._resolve_keyed_internal(service_type, key)
        except ServiceNotRegisteredException:
            return None
        finally:
            self._resolution_stack.clear()

    def _resolve_internal(self, service_type: Type[T]) -> T:
        """Internal resolution method with circular dependency detection."""
        return self._resolve_keyed_internal(service_type, None)

    def _resolve_keyed_internal(self, service_type: Type[T], key: Optional[Any]) -> T:
        """Internal keyed resolution method with circular dependency detection."""
        # Create a unique identifier for this service+key combination
        service_key = (service_type, key)

        # Check for circular dependency
        if service_key in self._resolution_stack:
            self._resolution_stack.append(service_key)
            raise CircularDependencyException(
                [str(sk) for sk in self._resolution_stack]
            )

        self._resolution_stack.append(service_key)

        try:
            registration = self._registry.get_registration(service_type, key)
            if registration is None:
                if key is None:
                    raise ServiceNotRegisteredException(service_type)
                else:
                    raise ServiceNotRegisteredException(
                        service_type,
                        f"Service of type {service_type} with key "
                        f"'{key}' is not registered.",
                    )

            result: T = self._create_instance(registration)
            return result
        finally:
            if self._resolution_stack and self._resolution_stack[-1] == service_key:
                self._resolution_stack.pop()

    def _create_instance(self, registration: ServiceRegistration) -> Any:
        """Create an instance based on the registration."""
        # Create unique key for singleton storage
        singleton_key = (registration.service_type, registration.key)

        # Handle singleton lifetime
        if registration.lifetime == ServiceLifetime.SINGLETON:
            if singleton_key in self._singleton_instances:
                return self._singleton_instances[singleton_key]

            instance = self._create_new_instance(registration)
            self._singleton_instances[singleton_key] = instance
            return instance

        # Handle scoped lifetime
        elif registration.lifetime == ServiceLifetime.SCOPED:
            if self._current_scope is None:
                raise ScopeException("No active scope for scoped service resolution")

            instance = self._current_scope.get_scoped_instance(
                registration.service_type, registration.key
            )
            if instance is None:
                instance = self._create_new_instance(registration)
                self._current_scope.set_scoped_instance(
                    registration.service_type, registration.key, instance
                )
            return instance

        # Handle transient lifetime
        else:
            return self._create_new_instance(registration)

    def _create_new_instance(self, registration: ServiceRegistration) -> Any:
        """Create a new instance based on registration strategy."""
        if registration.strategy == RegistrationStrategy.TYPE_TO_INSTANCE:
            return registration.instance

        elif registration.strategy == RegistrationStrategy.TYPE_TO_FACTORY:
            if registration.factory is None:
                raise InvalidRegistrationException(
                    "Factory cannot be None for TYPE_TO_FACTORY strategy"
                )
            return self._invoke_factory(registration.factory)

        elif registration.strategy == RegistrationStrategy.TYPE_TO_TYPE:
            if registration.implementation_type is None:
                raise InvalidRegistrationException(
                    "Implementation type cannot be None for TYPE_TO_TYPE"
                )
            return self._create_type_instance(registration.implementation_type)

        else:
            raise InvalidRegistrationException(
                f"Unknown registration strategy: {registration.strategy}"
            )

    def _create_type_instance(self, implementation_type: Type) -> Any:
        """Create an instance of a type using constructor injection."""
        # Get constructor signature
        signature = inspect.signature(implementation_type.__init__)
        parameters = signature.parameters

        # Skip 'self' parameter and filter out *args/**kwargs
        param_names = [
            name
            for name, param in parameters.items()
            if name != "self"
            and param.kind
            not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
        ]

        if not param_names:
            # No dependencies, create instance directly
            return implementation_type()

        # Resolve dependencies
        dependencies = []
        for param_name in param_names:
            param = parameters[param_name]
            param_type = param.annotation

            if param_type == inspect.Parameter.empty:
                raise InvalidRegistrationException(
                    f"Parameter '{param_name}' in "
                    f"{implementation_type} has no type annotation"
                )

            # Handle optional parameters
            if param.default != inspect.Parameter.empty:
                if self._registry.is_registered(param_type):
                    dependencies.append(self._resolve_internal(param_type))
                else:
                    dependencies.append(param.default)
            else:
                dependencies.append(self._resolve_internal(param_type))

        return implementation_type(*dependencies)

    def _invoke_factory(self, factory: Callable) -> Any:
        """Invoke a factory function with dependency injection."""
        signature = inspect.signature(factory)
        parameters = signature.parameters

        if not parameters:
            return factory()

        # Resolve factory dependencies
        dependencies = []
        for param_name, param in parameters.items():
            param_type = param.annotation

            if param_type == inspect.Parameter.empty:
                raise InvalidRegistrationException(
                    f"Factory parameter '{param_name}' has no type annotation"
                )

            dependencies.append(self._resolve_internal(param_type))

        return factory(*dependencies)

    def create_scope(self) -> DIScope:
        """Create a new scope."""
        return DIScope()

    def begin_scope(self, scope: Optional[DIScope] = None) -> DIScope:
        """Begin a new scope or use the provided scope."""
        if scope is None:
            scope = self.create_scope()
        self._current_scope = scope
        return scope

    def end_scope(self) -> None:
        """End the current scope."""
        if self._current_scope:
            self._current_scope.dispose()
            self._current_scope = None

    def is_registered(self, service_type: Type[T], key: Optional[Any] = None) -> bool:
        """Check if a service type is registered with optional key."""
        result: bool = self._registry.is_registered(service_type, key)
        return result

    def get_all_services(self, service_type: Type[T]) -> List[T]:
        """Get all registered services for a given type (including keyed services)."""
        registrations = self._registry.get_registrations_for_type(service_type)
        services = []

        for registration in registrations:
            try:
                service = self._create_instance(registration)
                services.append(service)
            except Exception:
                # Skip services that can't be resolved
                continue

        return services

    def clear(self) -> None:
        """Clear all registrations and instances."""
        self._registry.clear()
        self._singleton_instances.clear()
        if self._current_scope:
            self._current_scope.dispose()
            self._current_scope = None
