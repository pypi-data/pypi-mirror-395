"""
Core enumerations and constants for the DI container.
"""

from enum import Enum


class ServiceLifetime(Enum):
    """Defines the lifetime of a service."""

    SINGLETON = "singleton"
    TRANSIENT = "transient"
    SCOPED = "scoped"


class RegistrationStrategy(Enum):
    """Defines how services are registered."""

    TYPE_TO_TYPE = "type_to_type"
    TYPE_TO_INSTANCE = "type_to_instance"
    TYPE_TO_FACTORY = "type_to_factory"
