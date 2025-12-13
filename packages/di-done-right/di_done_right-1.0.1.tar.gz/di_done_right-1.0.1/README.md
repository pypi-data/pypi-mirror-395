# Python Dependency Injection Framework

A dependency injection framework for Python inspired by .NET's DI container system. This framework provides a clean and intuitive way to manage dependencies in your Python applications.

## Features

- Service registration with multiple lifetime scopes (Singleton, Transient, Scoped)
- Interface-based and concrete type registration
- **Keyed services** - Register multiple implementations of the same interface with keys
- **Static container management** - Global ServiceProvider for easy application-wide access
- **FastAPI integration** - Built-in support for FastAPI dependency injection
- Constructor injection with automatic dependency resolution
- Interface-based dependency resolution
- Circular dependency detection
- Type-safe service resolution
- Easy-to-use registration API
- Factory function support
- Thread-safe operations

## Quick Start

```python
from di_container import ServiceProvider, ServiceLifetime

# Configure services once at application startup
def configure_services(container):
    container.register(IUserService, UserService, ServiceLifetime.SINGLETON)
    container.register(IRepository, DatabaseRepository, ServiceLifetime.SCOPED)
    container.register(Logger, lifetime=ServiceLifetime.SINGLETON)

ServiceProvider.configure(configure_services)

# Use services anywhere in your application
user_service = ServiceProvider.resolve(IUserService)
logger = ServiceProvider.resolve(Logger)

# Or use convenience functions
from di_container import get_service
user_service = get_service(IUserService)
```

## Installation

```bash
pip install di-done-right

# For FastAPI integration support
pip install di-done-right[fastapi]

# For development
pip install di-done-right[dev]
```

## Usage Examples

### Basic Registration

```python
from di_container import DIContainer, ServiceLifetime

container = DIContainer()

# Interface to implementation
container.register(IUserService, UserService, ServiceLifetime.SINGLETON)

# Concrete type to itself
container.register(DatabaseService, lifetime=ServiceLifetime.SINGLETON)
container.register(Logger)  # Default TRANSIENT lifetime

# Instance registration
config = Configuration("connection_string")
container.register_instance(IConfiguration, config)

# Factory registration
container.register_factory(IEmailService, create_email_service)

# Keyed registrations
container.register_keyed(IPaymentService, "paypal", PayPalService)
container.register_keyed_instance(IConfig, "dev", dev_config)
container.register_keyed_factory(ICache, "redis", create_redis_cache)
```

### Service Resolution

```python
# Resolve services with automatic dependency injection
user_service = container.resolve(IUserService)
logger = container.resolve(Logger)

# Resolve keyed services
paypal_service = container.resolve_keyed(IPaymentService, "paypal")
stripe_service = container.resolve_keyed(IPaymentService, "stripe")

# Optional resolution (returns None if not found)
apple_pay = container.try_resolve_keyed(IPaymentService, "applepay")
```

### Static Container Setup

```python
from di_container import ServiceProvider, get_service

# Configure services once at startup
def configure_services(container):
    container.register(ILogger, ConsoleLogger, ServiceLifetime.SINGLETON)
    container.register(IUserService, UserService, ServiceLifetime.TRANSIENT)

ServiceProvider.configure(configure_services)

# Use anywhere in your application
logger = ServiceProvider.resolve(ILogger)
user_service = get_service(IUserService)  # Convenience function
```

### FastAPI Integration

```python
from fastapi import FastAPI, Depends
from di_container.fastapi_integration import FastAPIIntegration, inject

# Configure services
def configure_services(container):
    container.register(IUserService, UserService, ServiceLifetime.SINGLETON)

app = FastAPI(lifespan=FastAPIIntegration.create_lifespan_manager(configure_services))

# Use dependency injection in routes
@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    user_service: IUserService = Depends(inject(IUserService))
):
    return user_service.get_user(user_id)
```

### Keyed Services

```python
# Register multiple implementations with keys
container.register_keyed(IPaymentService, "paypal", PayPalService)
container.register_keyed(IPaymentService, "stripe", StripeService)
container.register_keyed(IPaymentService, "crypto", CryptoService)

# Resolve by key
payment_service = container.resolve_keyed(IPaymentService, "paypal")
# Or with ServiceProvider
payment_service = ServiceProvider.resolve_keyed(IPaymentService, "paypal")

# Get all services for a type
all_payment_services = container.get_all_services(IPaymentService)
```

### Scoped Services

```python
container.register(IEmailService, EmailService, ServiceLifetime.SCOPED)

scope = container.begin_scope()
try:
    email_service1 = container.resolve(IEmailService)
    email_service2 = container.resolve(IEmailService)
    # email_service1 is email_service2 -> True (same instance in scope)
finally:
    container.end_scope()
```

## Documentation and Examples

### Getting Started

See the [Quick Reference Guide](./QUICK_REFERENCE.md) for common patterns and immediate usage.

### Comprehensive Documentation

The [Complete User Documentation](./DOCUMENTATION.md) includes:

- Detailed API reference
- Advanced usage patterns
- FastAPI integration guide
- Real-world examples
- Best practices and troubleshooting

### Example Applications

Check the `examples/` directory for working demonstrations:

- `basic_usage.py` - Basic container usage
- `advanced_usage.py` - Advanced features like factories and instances
- `concrete_types_usage.py` - Working with concrete types without interfaces
- `keyed_services_usage.py` - Multiple implementations with keys
- `static_container_usage.py` - Global container management
- `fastapi_example.py` - FastAPI integration
- `comprehensive_example.py` - Complete e-commerce system example

## Structure

- `di_container/` - Core DI framework
  - `container.py` - Main DI container implementation
  - `registration.py` - Service registration and configuration
  - `exceptions.py` - Custom exceptions
  - `enums.py` - Enumerations and constants
- `examples/` - Usage examples
- `tests/` - Unit tests

## Contributing

This project follows Python best practices and includes comprehensive testing.
