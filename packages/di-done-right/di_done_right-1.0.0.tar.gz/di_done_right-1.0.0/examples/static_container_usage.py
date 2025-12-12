"""
Example demonstrating static container setup and configuration.
"""

from abc import ABC, abstractmethod

from di_container import DIContainer, ServiceLifetime, ServiceProvider, get_service


# Define interfaces and services
class ILogger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass


class IUserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> dict:
        pass

    @abstractmethod
    def save_user(self, user: dict) -> None:
        pass


class IEmailService(ABC):
    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> None:
        pass


class IUserService(ABC):
    @abstractmethod
    def get_user_profile(self, user_id: int) -> dict:
        pass

    @abstractmethod
    def update_user_email(self, user_id: int, new_email: str) -> None:
        pass


# Implementations
class ConsoleLogger(ILogger):
    def log(self, message: str) -> None:
        print(f"[LOG] {message}")


class DatabaseUserRepository(IUserRepository):
    def __init__(self, logger: ILogger):
        self.logger = logger
        self._users = {
            1: {"id": 1, "name": "John Doe", "email": "john@example.com"},
            2: {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
        }

    def get_user(self, user_id: int) -> dict:
        self.logger.log(f"Fetching user {user_id} from database")
        return self._users.get(user_id, {})

    def save_user(self, user: dict) -> None:
        self.logger.log(f"Saving user {user['id']} to database")
        self._users[user["id"]] = user


class EmailService(IEmailService):
    def __init__(self, logger: ILogger):
        self.logger = logger

    def send_email(self, to: str, subject: str, body: str) -> None:
        self.logger.log(f"Sending email to {to}: {subject}")


class UserService(IUserService):
    def __init__(
        self,
        user_repository: IUserRepository,
        email_service: IEmailService,
        logger: ILogger,
    ):
        self.user_repository = user_repository
        self.email_service = email_service
        self.logger = logger

    def get_user_profile(self, user_id: int) -> dict:
        self.logger.log(f"Getting profile for user {user_id}")
        return self.user_repository.get_user(user_id)

    def update_user_email(self, user_id: int, new_email: str) -> None:
        self.logger.log(f"Updating email for user {user_id}")
        user = self.user_repository.get_user(user_id)
        if user:
            old_email = user.get("email", "")
            user["email"] = new_email
            self.user_repository.save_user(user)

            # Send notification email
            self.email_service.send_email(
                new_email,
                "Email Updated",
                f"Your email has been changed from {old_email} to {new_email}",
            )


# Configuration function
def configure_services(container: DIContainer) -> None:
    """Configure all services in the DI container."""
    print("Configuring services...")

    # Register core services
    container.register(ILogger, ConsoleLogger, ServiceLifetime.SINGLETON)
    container.register(
        IUserRepository, DatabaseUserRepository, ServiceLifetime.SINGLETON
    )
    container.register(IEmailService, EmailService, ServiceLifetime.TRANSIENT)
    container.register(IUserService, UserService, ServiceLifetime.TRANSIENT)

    print("Services configured successfully!")


def main():
    """Demonstrate static container setup."""
    print("=== Static Container Setup Demo ===\n")

    # Check if container is configured
    print(f"Container configured: {ServiceProvider.is_configured()}")

    # Configure the global container
    ServiceProvider.configure(configure_services)
    print(f"Container configured: {ServiceProvider.is_configured()}\n")

    # Use services through static provider
    print("=== Using ServiceProvider directly ===")
    user_service = ServiceProvider.resolve(IUserService)
    logger = ServiceProvider.resolve(ILogger)

    logger.log("Application started")

    # Get user profile
    profile = user_service.get_user_profile(1)
    print(f"User profile: {profile}")

    # Update user email
    user_service.update_user_email(1, "john.doe.new@example.com")

    # Get updated profile
    updated_profile = user_service.get_user_profile(1)
    print(f"Updated profile: {updated_profile}")

    print("\n=== Using convenience functions ===")
    # Use convenience functions
    logger2 = get_service(ILogger)
    logger2.log("Using convenience function")

    # Verify singleton behavior
    print(f"Same logger instance: {logger is logger2}")

    print("\n=== Demonstrating multiple service resolution ===")
    # Resolve multiple services
    user_service2 = ServiceProvider.resolve(IUserService)
    user_service3 = ServiceProvider.resolve(IUserService)

    # Check if they're different instances (transient)
    print(f"Different UserService instances: {user_service2 is not user_service3}")

    # But they share the same singleton dependencies
    print(
        f"Same logger in both services: {user_service2.logger is user_service3.logger}"
    )

    print("\n=== Testing error handling ===")
    # Test trying to resolve unregistered service
    try:
        unregistered = ServiceProvider.try_resolve(str)
        print(f"Unregistered service result: {unregistered}")
    except Exception as e:
        print(f"Error resolving unregistered service: {e}")


# Business logic classes that use the static container
class UserController:
    """Example controller that uses static DI."""

    def __init__(self):
        # Services are resolved from the static container
        self.user_service = get_service(IUserService)
        self.logger = get_service(ILogger)

    def handle_get_user(self, user_id: int) -> dict:
        """Handle GET /users/{user_id} request."""
        self.logger.log(f"UserController: Handling get user request for {user_id}")
        return self.user_service.get_user_profile(user_id)

    def handle_update_email(self, user_id: int, new_email: str) -> dict:
        """Handle PUT /users/{user_id}/email request."""
        self.logger.log(f"UserController: Updating email for user {user_id}")
        self.user_service.update_user_email(user_id, new_email)
        return {"message": "Email updated successfully"}


def demonstrate_controller_usage():
    """Demonstrate using static DI in controllers."""
    print("\n=== Controller Usage Demo ===")

    controller = UserController()

    # Simulate API requests
    user_data = controller.handle_get_user(2)
    print(f"API Response: {user_data}")

    update_result = controller.handle_update_email(2, "jane.smith.updated@example.com")
    print(f"Update Response: {update_result}")


if __name__ == "__main__":
    main()
    demonstrate_controller_usage()
