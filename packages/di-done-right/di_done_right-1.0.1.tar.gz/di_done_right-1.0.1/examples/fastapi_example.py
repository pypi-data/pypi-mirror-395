"""
Example FastAPI application using the DI container.
This example shows how to integrate the DI container with FastAPI.

To run this example:
1. Install FastAPI and Uvicorn: pip install fastapi uvicorn
2. Run the server: uvicorn fastapi_example:app --reload

Note: This file won't run without FastAPI installed, but shows the integration pattern.
"""

# Uncomment these imports when FastAPI is available:
# from fastapi import FastAPI, Depends, HTTPException
# from pydantic import BaseModel
# from di_container.fastapi_integration import FastAPIIntegration, inject, inject_scoped

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from di_container import DIContainer, ServiceLifetime


# Define your domain models and interfaces
class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "email": self.email}


class IUserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass

    @abstractmethod
    def create_user(self, name: str, email: str) -> User:
        pass


class ILogger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass


class IEmailService(ABC):
    @abstractmethod
    def send_welcome_email(self, user: User) -> None:
        pass


# Implementations
class InMemoryUserRepository(IUserRepository):
    def __init__(self, logger: ILogger):
        self.logger = logger
        self._users: Dict[int, User] = {
            1: User(1, "John Doe", "john@example.com"),
            2: User(2, "Jane Smith", "jane@example.com"),
        }
        self._next_id = 3

    def get_user(self, user_id: int) -> Optional[User]:
        self.logger.log(f"Repository: Getting user {user_id}")
        return self._users.get(user_id)

    def get_all_users(self) -> List[User]:
        self.logger.log("Repository: Getting all users")
        return list(self._users.values())

    def create_user(self, name: str, email: str) -> User:
        self.logger.log(f"Repository: Creating user {name}")
        user = User(self._next_id, name, email)
        self._users[self._next_id] = user
        self._next_id += 1
        return user


class ConsoleLogger(ILogger):
    def log(self, message: str) -> None:
        print(f"[LOG] {message}")


class EmailService(IEmailService):
    def __init__(self, logger: ILogger):
        self.logger = logger

    def send_welcome_email(self, user: User) -> None:
        self.logger.log(f"Sending welcome email to {user.email}")


# Configure services
def configure_services(container: DIContainer) -> None:
    """Configure all services for the FastAPI application."""
    container.register(ILogger, ConsoleLogger, ServiceLifetime.SINGLETON)
    container.register(IUserRepository, InMemoryUserRepository, ServiceLifetime.SCOPED)
    container.register(IEmailService, EmailService, ServiceLifetime.TRANSIENT)


# FastAPI application setup (commented out - requires FastAPI)
"""
# Create FastAPI app with DI configuration
app = FastAPI(
    title="DI Container FastAPI Example",
    description="Example showing DI container integration with FastAPI",
    version="1.0.0",
    lifespan=FastAPIIntegration.create_lifespan_manager(configure_services)
)

# Add scope cleanup middleware
app.add_middleware(ScopeCleanupMiddleware)

# Pydantic models for API
class CreateUserRequest(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

# API Routes using dependency injection

@app.get("/")
async def root():
    return {"message": "FastAPI DI Container Example"}

@app.get("/users", response_model=List[UserResponse])
async def get_users(
    user_repository: IUserRepository = Depends(inject_scoped(IUserRepository)),
    logger: ILogger = Depends(inject(ILogger))
):
    logger.log("API: Getting all users")
    users = user_repository.get_all_users()
    return [UserResponse(**user.to_dict()) for user in users]

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user_repository: IUserRepository = Depends(inject_scoped(IUserRepository)),
    logger: ILogger = Depends(inject(ILogger))
):
    logger.log(f"API: Getting user {user_id}")
    user = user_repository.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user.to_dict())

@app.post("/users", response_model=UserResponse)
async def create_user(
    request: CreateUserRequest,
    user_repository: IUserRepository = Depends(inject_scoped(IUserRepository)),
    email_service: IEmailService = Depends(inject(IEmailService)),
    logger: ILogger = Depends(inject(ILogger))
):
    logger.log(f"API: Creating user {request.name}")
    user = user_repository.create_user(request.name, request.email)
    email_service.send_welcome_email(user)
    return UserResponse(**user.to_dict())

# Alternative way using FastAPIIntegration methods directly
@app.get("/users-alt/{user_id}")
async def get_user_alternative(
    user_id: int,
    user_repository: IUserRepository = Depends(FastAPIIntegration.get_scoped_service(IUserRepository)),
    logger: ILogger = Depends(FastAPIIntegration.get_service(ILogger))
):
    logger.log(f"API (alternative): Getting user {user_id}")
    user = user_repository.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_dict()

# Health check endpoint
@app.get("/health")
async def health_check(logger: ILogger = Depends(inject(ILogger))):
    logger.log("Health check requested")
    return {"status": "healthy", "di_configured": ServiceProvider.is_configured()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""


def show_fastapi_example():
    """Show how the FastAPI integration would work."""
    print("=== FastAPI Integration Example ===")
    print("This example shows how to integrate the DI container with FastAPI.")
    print("\nKey features:")
    print("1. Global container configuration using ServiceProvider")
    print("2. Automatic dependency injection in route handlers")
    print("3. Scoped services per request")
    print("4. Middleware for proper cleanup")
    print("5. Integration with FastAPI's dependency system")

    print("\nTo use this with FastAPI:")
    print("1. Install FastAPI: pip install fastapi uvicorn")
    print("2. Uncomment the FastAPI code in this file")
    print("3. Run: uvicorn fastapi_example:app --reload")

    print("\nExample usage patterns:")
    print("- Use inject(ServiceType) for singleton/transient services")
    print("- Use inject_scoped(ServiceType) for scoped services")
    print("- Services are automatically injected into route parameters")
    print("- Scoped services are created per request and cleaned up automatically")


if __name__ == "__main__":
    show_fastapi_example()
