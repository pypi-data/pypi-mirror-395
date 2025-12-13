"""
Example showing concrete type registration without interfaces.
"""

from di_container import DIContainer, ServiceLifetime


# Concrete classes without interfaces
class DatabaseConnection:
    def __init__(self):
        self.connection_string = "Server=localhost;Database=MyApp;"

    def connect(self) -> str:
        return f"Connected to {self.connection_string}"


class Logger:
    def __init__(self):
        pass

    def log(self, message: str) -> None:
        print(f"[LOG] {message}")


class UserRepository:
    def __init__(self, db_connection: DatabaseConnection, logger: Logger):
        self.db_connection = db_connection
        self.logger = logger

    def get_user(self, user_id: int) -> dict:
        self.logger.log(f"Getting user {user_id}")
        connection_info = self.db_connection.connect()
        self.logger.log(f"Using connection: {connection_info}")
        return {"id": user_id, "name": f"User {user_id}"}


class UserService:
    def __init__(self, user_repository: UserRepository, logger: Logger):
        self.user_repository = user_repository
        self.logger = logger

    def get_user_info(self, user_id: int) -> str:
        self.logger.log(f"UserService: Getting info for user {user_id}")
        user = self.user_repository.get_user(user_id)
        return f"User Info: {user['name']} (ID: {user['id']})"


def main():
    """Demonstrate concrete type registration."""
    container = DIContainer()

    # Register concrete types directly (no interfaces needed)
    container.register(DatabaseConnection, lifetime=ServiceLifetime.SINGLETON)
    container.register(Logger, lifetime=ServiceLifetime.SINGLETON)
    container.register(UserRepository, lifetime=ServiceLifetime.TRANSIENT)
    container.register(UserService, lifetime=ServiceLifetime.TRANSIENT)

    # Resolve and use services
    user_service = container.resolve(UserService)
    result = user_service.get_user_info(42)
    print(f"\nResult: {result}")

    # Demonstrate singleton behavior
    logger1 = container.resolve(Logger)
    logger2 = container.resolve(Logger)
    print(f"\nSame logger instance: {logger1 is logger2}")  # Should be True

    # Demonstrate transient behavior
    repo1 = container.resolve(UserRepository)
    repo2 = container.resolve(UserRepository)
    print(f"Different repository instances: {repo1 is not repo2}")  # Should be True

    # But they share the same singleton dependencies
    print(
        f"Same DB connection: {repo1.db_connection is repo2.db_connection}"
    )  # Should be True
    print(f"Same logger: {repo1.logger is repo2.logger}")  # Should be True


if __name__ == "__main__":
    main()
