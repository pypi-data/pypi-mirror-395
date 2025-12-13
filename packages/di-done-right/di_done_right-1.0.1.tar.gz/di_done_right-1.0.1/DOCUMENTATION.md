# Python Dependency Injection Framework - User Documentation

## Table of Contents

1. [Quick Start](#quick-start)
2. [Core Concepts](#core-concepts)
3. [Service Registration](#service-registration)
4. [Service Lifetimes](#service-lifetimes)
5. [Keyed Services](#keyed-services)
6. [Static Container Management](#static-container-management)
7. [FastAPI Integration](#fastapi-integration)
8. [Advanced Scenarios](#advanced-scenarios)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Installation

```bash
pip install di-done-right
```

### Basic Setup

```python
from di_container import ServiceProvider, ServiceLifetime
from abc import ABC, abstractmethod

# 1. Define your interfaces
class ILogger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass

class IUserService(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> dict:
        pass

# 2. Implement your services
class ConsoleLogger(ILogger):
    def log(self, message: str) -> None:
        print(f"[LOG] {message}")

class UserService(IUserService):
    def __init__(self, logger: ILogger):
        self.logger = logger
    
    def get_user(self, user_id: int) -> dict:
        self.logger.log(f"Getting user {user_id}")
        return {"id": user_id, "name": f"User {user_id}"}

# 3. Configure services
def configure_services(container):
    container.register(ILogger, ConsoleLogger, ServiceLifetime.SINGLETON)
    container.register(IUserService, UserService, ServiceLifetime.TRANSIENT)

# 4. Setup container
ServiceProvider.configure(configure_services)

# 5. Use services
user_service = ServiceProvider.resolve(IUserService)
user = user_service.get_user(123)
print(user)  # Output: {'id': 123, 'name': 'User 123'}
```

---

## Core Concepts

### Dependency Injection Container (DIContainer)

The `DIContainer` is the core class that manages service registrations and resolutions. It supports:

- Constructor injection
- Multiple service lifetimes
- Keyed services
- Circular dependency detection

### Service Provider (Static Container)

The `ServiceProvider` provides a global, thread-safe way to access services throughout your application without passing the container around.

### Service Registration

Services can be registered in three ways:

1. **Type to Type**: Interface to implementation mapping
2. **Type to Instance**: Pre-created instance
3. **Type to Factory**: Factory function that creates the service

---

## Service Registration Details

### Interface to Implementation

```python
from di_container import DIContainer, ServiceLifetime

container = DIContainer()

# Register interface to implementation
container.register(IUserService, UserService, ServiceLifetime.SINGLETON)

# Register concrete type to itself
container.register(DatabaseConnection, lifetime=ServiceLifetime.SINGLETON)
```

### Instance Registration

Use this for pre-configured objects or third-party services:

```python
# Create a configured instance
database_config = DatabaseConfig(
    connection_string="<YourConnectionStringHere>",
    timeout=30
)

# Register the instance
container.register_instance(IDatabaseConfig, database_config)

# All resolutions will return this same instance
config = container.resolve(IDatabaseConfig)
```

### Factory Registration

Useful for complex object creation or when you need access to other services:

```python
def create_email_service(logger: ILogger, config: IConfig) -> IEmailService:
    smtp_host = config.get_value("smtp_host")
    return SmtpEmailService(smtp_host, logger)

container.register_factory(
    IEmailService, 
    create_email_service, 
    ServiceLifetime.SINGLETON
)
```

### Concrete Type Registration

Register classes without interfaces:

```python
# No interface needed
container.register(Logger, lifetime=ServiceLifetime.SINGLETON)
container.register(DatabaseService, lifetime=ServiceLifetime.SCOPED)

# Use directly
logger = container.resolve(Logger)
db_service = container.resolve(DatabaseService)
```

---

## Service Lifetimes

### Singleton

One instance for the entire application lifetime:

```python
container.register(ILogger, FileLogger, ServiceLifetime.SINGLETON)

logger1 = container.resolve(ILogger)
logger2 = container.resolve(ILogger)
assert logger1 is logger2  # Same instance
```

**Use cases:**

- Loggers
- Configuration services
- Cache managers
- Connection pools

### Transient

New instance every time:

```python
container.register(IEmailService, EmailService, ServiceLifetime.TRANSIENT)

email1 = container.resolve(IEmailService)
email2 = container.resolve(IEmailService)
assert email1 is not email2  # Different instances
```

**Use cases:**

- Stateless services
- Command handlers
- Request processors

### Scoped

One instance per scope (typically per request in web applications):

```python
container.register(IRepository, DatabaseRepository, ServiceLifetime.SCOPED)

# Create scope
scope = container.begin_scope()
try:
    repo1 = container.resolve(IRepository)
    repo2 = container.resolve(IRepository)
    assert repo1 is repo2  # Same instance within scope
finally:
    container.end_scope()
```

**Use cases:**

- Database contexts
- Unit of Work patterns
- Request-specific services

---

## Keyed Services

Register multiple implementations of the same interface with different keys:

### Basic Keyed Registration

```python
# Register multiple payment providers
container.register_keyed(IPaymentService, "paypal", PayPalService, ServiceLifetime.SINGLETON)
container.register_keyed(IPaymentService, "stripe", StripeService, ServiceLifetime.SINGLETON)
container.register_keyed(IPaymentService, "crypto", CryptoService, ServiceLifetime.TRANSIENT)

# Resolve by key
paypal = container.resolve_keyed(IPaymentService, "paypal")
stripe = container.resolve_keyed(IPaymentService, "stripe")
```

### Keyed Instance Registration

```python
# Register pre-configured instances
dev_config = DatabaseConfig("dev_connection_string")
prod_config = DatabaseConfig("prod_connection_string")

container.register_keyed_instance(IDatabaseConfig, "development", dev_config)
container.register_keyed_instance(IDatabaseConfig, "production", prod_config)

# Use based on environment
environment = "development"
config = container.resolve_keyed(IDatabaseConfig, environment)
```

### Keyed Factory Registration

```python
def create_redis_cache(config: IConfig) -> ICache:
    redis_url = config.get_value("redis_url")
    return RedisCache(redis_url)

def create_memory_cache() -> ICache:
    return MemoryCache()

container.register_keyed_factory(ICache, "redis", create_redis_cache)
container.register_keyed_factory(ICache, "memory", create_memory_cache)

# Choose cache implementation
cache = container.resolve_keyed(ICache, "redis")
```

### Working with All Services

```python
# Get all registered implementations
all_payment_services = container.get_all_services(IPaymentService)

for service in all_payment_services:
    result = service.process_payment(100.0)
    print(f"Payment result: {result}")
```

### Real-World Keyed Services Example

```python
class PaymentProcessor:
    def __init__(self, logger: ILogger):
        self.logger = logger
        self.container = ServiceProvider.get_container()
    
    def process_payment(self, method: str, amount: float) -> str:
        self.logger.log(f"Processing {method} payment for ${amount}")
        
        # Resolve payment service by method
        payment_service = self.container.resolve_keyed(IPaymentService, method)
        return payment_service.process_payment(amount)
    
    def get_available_methods(self) -> list[str]:
        # This could be dynamic based on registered services
        return ["paypal", "stripe", "crypto"]

# Usage
processor = PaymentProcessor(logger)
result = processor.process_payment("paypal", 99.99)
```

---

## Static Container Management

The `ServiceProvider` class provides a global, thread-safe way to manage your DI container.

### Configuration

```python
from di_container import ServiceProvider, get_service

def configure_services(container):
    # Register all your services here
    container.register(ILogger, ConsoleLogger, ServiceLifetime.SINGLETON)
    container.register(IUserService, UserService, ServiceLifetime.TRANSIENT)
    container.register(IRepository, DatabaseRepository, ServiceLifetime.SCOPED)
    
    # Keyed services
    container.register_keyed(IPaymentService, "paypal", PayPalService)
    container.register_keyed(IPaymentService, "stripe", StripeService)

# Configure once at application startup
ServiceProvider.configure(configure_services)
```

### Using Services

```python
# Direct resolution
user_service = ServiceProvider.resolve(IUserService)
payment_service = ServiceProvider.resolve_keyed(IPaymentService, "paypal")

# Convenience functions
logger = get_service(ILogger)
repository = get_service(IRepository)

# Safe resolution (returns None if not found)
optional_service = ServiceProvider.try_resolve(IOptionalService)
if optional_service:
    optional_service.do_something()
```

### Scope Management

```python
# Manual scope management
scope = ServiceProvider.create_scope()
ServiceProvider.begin_scope(scope)
try:
    # Use scoped services
    repository = ServiceProvider.resolve(IRepository)
    repository.save_data()
finally:
    ServiceProvider.end_scope()
```

### Application Structure Example

```python
# config.py
def configure_application_services(container):
    # Infrastructure
    container.register(ILogger, FileLogger, ServiceLifetime.SINGLETON)
    container.register(IConfiguration, AppConfiguration, ServiceLifetime.SINGLETON)
    
    # Data Access
    container.register(IUserRepository, SqlUserRepository, ServiceLifetime.SCOPED)
    container.register(IOrderRepository, SqlOrderRepository, ServiceLifetime.SCOPED)
    
    # Business Services
    container.register(IUserService, UserService, ServiceLifetime.TRANSIENT)
    container.register(IOrderService, OrderService, ServiceLifetime.TRANSIENT)
    
    # External Services
    container.register_keyed(IPaymentService, "default", StripePaymentService)
    container.register_keyed(IPaymentService, "backup", PayPalPaymentService)

# main.py
from config import configure_application_services

def main():
    # Setup DI container
    ServiceProvider.configure(configure_application_services)
    
    # Application logic
    user_service = get_service(IUserService)
    users = user_service.get_all_users()
    
if __name__ == "__main__":
    main()

# controllers/user_controller.py
class UserController:
    def __init__(self):
        self.user_service = get_service(IUserService)
        self.logger = get_service(ILogger)
    
    def get_user(self, user_id: int):
        self.logger.log(f"Getting user {user_id}")
        return self.user_service.get_user(user_id)
```

---

## FastAPI Integration

The framework provides seamless integration with FastAPI for automatic dependency injection.

### FastAPI Application Setup

```python
from fastapi import FastAPI, Depends
from di_container.fastapi_integration import FastAPIIntegration, inject

def configure_services(container):
    container.register(IUserService, UserService, ServiceLifetime.SINGLETON)
    container.register(IRepository, DatabaseRepository, ServiceLifetime.SCOPED)

# Create app with DI configuration
app = FastAPI(
    title="My API",
    lifespan=FastAPIIntegration.create_lifespan_manager(configure_services)
)

# Add middleware for scope cleanup
from di_container.fastapi_integration import ScopeCleanupMiddleware
app.add_middleware(ScopeCleanupMiddleware)
```

### Route Injection

```python
from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

# Inject singleton/transient services
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user_service: IUserService = Depends(inject(IUserService)),
    logger: ILogger = Depends(inject(ILogger))
):
    logger.log(f"API: Getting user {user_id}")
    user = user_service.get_user(user_id)
    return UserResponse(**user)

# Inject scoped services (automatically managed per request)
@app.post("/users", response_model=UserResponse)
async def create_user(
    request: CreateUserRequest,
    repository: IUserRepository = Depends(inject_scoped(IUserRepository)),
    logger: ILogger = Depends(inject(ILogger))
):
    logger.log(f"API: Creating user {request.name}")
    user = repository.create_user(request.name, request.email)
    return UserResponse(**user.to_dict())
```

### Keyed Services in FastAPI

```python
# Register keyed services
def configure_services(container):
    container.register_keyed(IPaymentService, "paypal", PayPalService)
    container.register_keyed(IPaymentService, "stripe", StripeService)
    container.register_keyed(INotificationService, "email", EmailNotificationService)
    container.register_keyed(INotificationService, "sms", SmsNotificationService)

# Use in routes
@app.post("/payments/{method}")
async def process_payment(
    method: str,
    amount: float,
    payment_service: IPaymentService = Depends(lambda: inject_keyed(IPaymentService, method)()),
    email_service: INotificationService = Depends(lambda: inject_keyed(INotificationService, "email")())
):
    result = payment_service.process_payment(amount)
    email_service.send_notification(f"Payment processed: {result}")
    return {"result": result}
```

### Advanced FastAPI Integration

```python
from fastapi import HTTPException, Request

# Custom dependency for user context
def get_current_user(
    request: Request,
    user_service: IUserService = Depends(inject(IUserService))
):
    user_id = request.headers.get("X-User-ID")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID required")
    
    user = user_service.get_user(int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

# Use custom dependency with DI
@app.get("/profile")
async def get_profile(
    current_user: dict = Depends(get_current_user),
    logger: ILogger = Depends(inject(ILogger))
):
    logger.log(f"Getting profile for user {current_user['id']}")
    return current_user

# Background tasks with DI
from fastapi import BackgroundTasks

@app.post("/send-email")
async def send_email(
    email: str,
    subject: str,
    body: str,
    background_tasks: BackgroundTasks,
    email_service: IEmailService = Depends(inject(IEmailService)),
    logger: ILogger = Depends(inject(ILogger))
):
    def send_email_task():
        logger.log(f"Sending email to {email}")
        email_service.send_email(email, subject, body)
    
    background_tasks.add_task(send_email_task)
    return {"message": "Email queued for sending"}
```

### Error Handling

```python
from fastapi import HTTPException

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger = get_service(ILogger)
    logger.log(f"Unhandled exception: {str(exc)}")
    
    # Ensure scope cleanup on error
    try:
        ServiceProvider.end_scope()
    except:
        pass
    
    return {"error": "Internal server error"}
```

---

## Advanced Scenarios

### Complex Object Graphs

```python
class OrderService:
    def __init__(
        self, 
        user_repository: IUserRepository,
        product_repository: IProductRepository,
        payment_service: IPaymentService,
        email_service: IEmailService,
        logger: ILogger
    ):
        self.user_repository = user_repository
        self.product_repository = product_repository
        self.payment_service = payment_service
        self.email_service = email_service
        self.logger = logger
    
    def process_order(self, order_data: dict) -> dict:
        # Complex business logic using all dependencies
        self.logger.log("Processing order")
        # ... implementation
        return {"order_id": 123, "status": "processed"}

# All dependencies are automatically resolved
container.register(IOrderService, OrderService, ServiceLifetime.TRANSIENT)
order_service = container.resolve(IOrderService)
```

### Conditional Registration

```python
import os

def configure_services(container):
    # Conditional registration based on environment
    environment = os.getenv("ENVIRONMENT", "development")
    
    if environment == "production":
        container.register(ILogger, FileLogger, ServiceLifetime.SINGLETON)
        container.register(IEmailService, SmtpEmailService, ServiceLifetime.TRANSIENT)
    else:
        container.register(ILogger, ConsoleLogger, ServiceLifetime.SINGLETON)
        container.register(IEmailService, MockEmailService, ServiceLifetime.TRANSIENT)
    
    # Database configuration
    if environment == "testing":
        container.register(IRepository, InMemoryRepository, ServiceLifetime.TRANSIENT)
    else:
        container.register(IRepository, SqlRepository, ServiceLifetime.SCOPED)
```

### Decorator Pattern with DI

```python
class CachedUserService:
    def __init__(self, user_service: IUserService, cache: ICache, logger: ILogger):
        self.user_service = user_service
        self.cache = cache
        self.logger = logger
    
    def get_user(self, user_id: int) -> dict:
        cache_key = f"user:{user_id}"
        
        # Try cache first
        cached_user = self.cache.get(cache_key)
        if cached_user:
            self.logger.log(f"Cache hit for user {user_id}")
            return cached_user
        
        # Fallback to actual service
        self.logger.log(f"Cache miss for user {user_id}")
        user = self.user_service.get_user(user_id)
        self.cache.set(cache_key, user, ttl=300)
        return user

# Register the decorator instead of the original service
container.register(IUserService, CachedUserService, ServiceLifetime.SINGLETON)
```

### Plugin Architecture

```python
class PluginManager:
    def __init__(self):
        self.plugins = []
    
    def register_plugin(self, plugin: IPlugin):
        self.plugins.append(plugin)
    
    def execute_plugins(self, context: dict):
        for plugin in self.plugins:
            plugin.execute(context)

def configure_plugins(container):
    # Register plugin manager
    container.register(PluginManager, lifetime=ServiceLifetime.SINGLETON)
    
    # Register individual plugins
    container.register_keyed(IPlugin, "auth", AuthenticationPlugin)
    container.register_keyed(IPlugin, "logging", LoggingPlugin)
    container.register_keyed(IPlugin, "validation", ValidationPlugin)

# Initialize plugins
plugin_manager = get_service(PluginManager)
auth_plugin = ServiceProvider.resolve_keyed(IPlugin, "auth")
logging_plugin = ServiceProvider.resolve_keyed(IPlugin, "logging")

plugin_manager.register_plugin(auth_plugin)
plugin_manager.register_plugin(logging_plugin)
```

---

## Best Practices

### 1. Interface Design

```python
# Good: Clear, focused interfaces
class IUserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def save_user(self, user: User) -> None:
        pass

# Avoid: Large, unfocused interfaces
class IBadRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_product(self, product_id: int) -> Optional[Product]:
        pass
    
    @abstractmethod
    def send_email(self, email: str) -> None:  # Doesn't belong here
        pass
```

### 2. Service Lifetime Selection

```python
# Singleton: Stateless, expensive to create
container.register(ILogger, FileLogger, ServiceLifetime.SINGLETON)
container.register(IConfiguration, AppConfiguration, ServiceLifetime.SINGLETON)

# Scoped: Stateful within a request/operation
container.register(IDbContext, DatabaseContext, ServiceLifetime.SCOPED)
container.register(IUserRepository, UserRepository, ServiceLifetime.SCOPED)

# Transient: Lightweight, stateless operations
container.register(IEmailService, EmailService, ServiceLifetime.TRANSIENT)
container.register(IValidator, UserValidator, ServiceLifetime.TRANSIENT)
```

### 3. Error Handling

```python
def configure_services(container):
    try:
        # Service registrations
        container.register(IUserService, UserService)
    except Exception as e:
        logger.error(f"Failed to configure services: {e}")
        raise

# Graceful degradation
def get_service_safely(service_type):
    try:
        return ServiceProvider.resolve(service_type)
    except ServiceNotRegisteredException:
        logger.warning(f"Service {service_type} not registered, using fallback")
        return FallbackService()
```

### 4. Testing

```python
import pytest

class TestUserService:
    def setup_method(self):
        # Reset container for each test
        ServiceProvider.reset()
        
        def configure_test_services(container):
            container.register(ILogger, MockLogger, ServiceLifetime.SINGLETON)
            container.register(IRepository, MockRepository, ServiceLifetime.TRANSIENT)
            container.register(IUserService, UserService, ServiceLifetime.TRANSIENT)
        
        ServiceProvider.configure(configure_test_services)
    
    def test_get_user(self):
        user_service = ServiceProvider.resolve(IUserService)
        user = user_service.get_user(1)
        assert user is not None
    
    def teardown_method(self):
        ServiceProvider.reset()
```

---

## Troubleshooting

### Common Issues

#### 1. ServiceNotRegisteredException

```python
# Problem: Service not registered
user_service = container.resolve(IUserService)  # Throws exception

# Solution: Register the service
container.register(IUserService, UserService)

# Or use safe resolution
user_service = container.try_resolve(IUserService)
if user_service is None:
    print("Service not available")
```

#### 2. CircularDependencyException

```python
# Problem: Services depend on each other
class ServiceA:
    def __init__(self, service_b: IServiceB):
        self.service_b = service_b

class ServiceB:
    def __init__(self, service_a: IServiceA):
        self.service_a = service_a

# Solution: Refactor to remove circular dependency
class ServiceA:
    def __init__(self, service_b: IServiceB):
        self.service_b = service_b

class ServiceB:
    def __init__(self, common_service: ICommonService):
        self.common_service = common_service
```

#### 3. Missing Type Annotations

```python
# Problem: Missing type hints
class BadService:
    def __init__(self, logger):  # No type annotation
        self.logger = logger

# Solution: Add proper type annotations
class GoodService:
    def __init__(self, logger: ILogger):
        self.logger = logger
```

#### 4. Scope Issues

```python
# Problem: Using scoped service without scope
container.register(IRepository, Repository, ServiceLifetime.SCOPED)
repo = container.resolve(IRepository)  # Throws ScopeException

# Solution: Use within a scope
scope = container.begin_scope()
try:
    repo = container.resolve(IRepository)
    # Use repository
finally:
    container.end_scope()
```

### Debugging Tips

#### 1. Check Registration

```python
# Verify service is registered
if container.is_registered(IUserService):
    print("Service is registered")
else:
    print("Service not found")

# Check keyed service
if container.is_registered(IPaymentService, "paypal"):
    print("Keyed service is registered")
```

#### 2. Inspect Dependencies

```python
# Get all registrations
registrations = container._registry.get_all_registrations()
for (service_type, key), registration in registrations.items():
    print(f"Registered: {service_type} (key: {key}) -> {registration.implementation_type}")
```

#### 3. Enable Logging

```python
class VerboseLogger(ILogger):
    def log(self, message: str) -> None:
        print(f"[{datetime.now()}] {message}")

# Use in DI configuration for debugging
container.register(ILogger, VerboseLogger, ServiceLifetime.SINGLETON)
```

---

This documentation covers all the major features and usage patterns of the Python Dependency Injection Framework. For more examples, check the `examples/` directory in the repository.
