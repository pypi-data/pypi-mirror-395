"""
Basic usage example of the DI container.
"""

from abc import ABC, abstractmethod

from di_container import DIContainer, ServiceLifetime


# Define interfaces
class ILogger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass


class IUserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> dict:
        pass


class IUserService(ABC):
    @abstractmethod
    def get_user_details(self, user_id: int) -> str:
        pass


# Implement concrete classes
class ConsoleLogger(ILogger):
    def log(self, message: str) -> None:
        print(f"[LOG] {message}")


class DatabaseUserRepository(IUserRepository):
    def __init__(self, logger: ILogger):
        self.logger = logger

    def get_user(self, user_id: int) -> dict:
        self.logger.log(f"Fetching user {user_id} from database")
        return {
            "id": user_id,
            "name": f"User {user_id}",
            "email": f"user{user_id}@example.com",
        }


class UserService(IUserService):
    def __init__(self, user_repository: IUserRepository, logger: ILogger):
        self.user_repository = user_repository
        self.logger = logger

    def get_user_details(self, user_id: int) -> str:
        self.logger.log(f"Getting details for user {user_id}")
        user = self.user_repository.get_user(user_id)
        return f"User Details: {user['name']} ({user['email']})"


def main():
    """Demonstrate basic DI container usage."""
    # Create container
    container = DIContainer()

    # Register services
    container.register(ILogger, ConsoleLogger, ServiceLifetime.SINGLETON)
    container.register(
        IUserRepository, DatabaseUserRepository, ServiceLifetime.TRANSIENT
    )
    container.register(IUserService, UserService, ServiceLifetime.TRANSIENT)

    # Resolve and use services
    user_service = container.resolve(IUserService)
    result = user_service.get_user_details(123)
    print(result)

    # Demonstrate singleton behavior
    logger1 = container.resolve(ILogger)
    logger2 = container.resolve(ILogger)
    print(f"Same logger instance: {logger1 is logger2}")  # Should be True


if __name__ == "__main__":
    main()
