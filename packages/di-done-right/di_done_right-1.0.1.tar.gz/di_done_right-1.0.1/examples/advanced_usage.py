"""
Advanced usage example showing factory registration and scoped services.
"""

from abc import ABC, abstractmethod

from di_container import DIContainer, ServiceLifetime


# Define interfaces
class IConfiguration(ABC):
    @abstractmethod
    def get_connection_string(self) -> str:
        pass


class IEmailService(ABC):
    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> None:
        pass


class INotificationService(ABC):
    @abstractmethod
    def notify_user(self, user_id: int, message: str) -> None:
        pass


# Implementations
class Configuration(IConfiguration):
    def __init__(self, connection_string: str):
        self._connection_string = connection_string

    def get_connection_string(self) -> str:
        return self._connection_string


class EmailService(IEmailService):
    def __init__(self, config: IConfiguration):
        self.config = config

    def send_email(self, to: str, subject: str, body: str) -> None:
        conn_str = self.config.get_connection_string()
        print(f"Sending email via {conn_str}: To={to}, Subject={subject}")


class NotificationService(INotificationService):
    def __init__(self, email_service: IEmailService):
        self.email_service = email_service

    def notify_user(self, user_id: int, message: str) -> None:
        self.email_service.send_email(
            f"user{user_id}@example.com", "Notification", message
        )


def create_configuration() -> IConfiguration:
    """Factory function to create configuration."""
    return Configuration("Server=localhost;Database=MyApp;")


def main():
    """Demonstrate advanced DI container features."""
    container = DIContainer()

    # Register using factory
    container.register_factory(
        IConfiguration, create_configuration, ServiceLifetime.SINGLETON
    )

    # Register scoped service
    container.register(IEmailService, EmailService, ServiceLifetime.SCOPED)
    container.register(
        INotificationService, NotificationService, ServiceLifetime.TRANSIENT
    )

    # Create scope and resolve services
    scope = container.begin_scope()
    try:
        notification_service1 = container.resolve(INotificationService)
        notification_service2 = container.resolve(INotificationService)

        # These should use the same EmailService instance (scoped)
        notification_service1.notify_user(1, "Hello from service 1")
        notification_service2.notify_user(2, "Hello from service 2")

        # Check if scoped services are the same
        email1 = notification_service1.email_service
        email2 = notification_service2.email_service
        print(f"Same scoped EmailService: {email1 is email2}")  # Should be True

    finally:
        container.end_scope()

    # Register instance example
    specific_config = Configuration("Server=prod;Database=Production;")
    container.register_instance(IConfiguration, specific_config)

    # Now resolve with the specific instance
    config = container.resolve(IConfiguration)
    print(f"Connection string: {config.get_connection_string()}")


if __name__ == "__main__":
    main()
