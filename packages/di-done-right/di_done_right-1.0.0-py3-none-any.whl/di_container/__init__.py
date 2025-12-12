"""
Python Dependency Injection Framework

A dependency injection framework inspired by .NET's DI container system.
"""

from .container import DIContainer, DIScope
from .enums import RegistrationStrategy, ServiceLifetime
from .exceptions import (
    CircularDependencyException,
    DIException,
    InvalidRegistrationException,
    ScopeException,
    ServiceNotRegisteredException,
)
from .registration import ServiceRegistration, ServiceRegistry
from .service_provider import (
    ServiceProvider,
    get_keyed_service,
    get_service,
    try_get_service,
)

__version__ = "0.1.0"
__all__ = [
    "DIContainer",
    "DIScope",
    "ServiceRegistration",
    "ServiceRegistry",
    "ServiceLifetime",
    "RegistrationStrategy",
    "DIException",
    "ServiceNotRegisteredException",
    "CircularDependencyException",
    "InvalidRegistrationException",
    "ScopeException",
    "ServiceProvider",
    "get_service",
    "get_keyed_service",
    "try_get_service",
]
