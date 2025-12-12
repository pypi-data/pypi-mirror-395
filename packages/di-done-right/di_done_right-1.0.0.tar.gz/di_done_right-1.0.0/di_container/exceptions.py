"""
Custom exceptions for the DI container.
"""

from typing import Optional


class DIException(Exception):
    """Base exception for DI container errors."""

    pass


class ServiceNotRegisteredException(DIException):
    """Raised when trying to resolve a service that hasn't been registered."""

    def __init__(self, service_type: type, message: Optional[str] = None) -> None:
        self.service_type = service_type
        if message:
            super().__init__(message)
        else:
            super().__init__(f"Service of type {service_type} is not registered.")


class CircularDependencyException(DIException):
    """Raised when a circular dependency is detected."""

    def __init__(self, dependency_chain: list) -> None:
        self.dependency_chain = dependency_chain
        chain_str = " -> ".join(str(t) for t in dependency_chain)
        super().__init__(f"Circular dependency detected: {chain_str}")


class InvalidRegistrationException(DIException):
    """Raised when a service registration is invalid."""

    pass


class ScopeException(DIException):
    """Raised when there are issues with service scoping."""

    pass
