# Quick Reference Guide

## Basic Setup

```python
from di_container import ServiceProvider, ServiceLifetime

# 1. Configure services
def configure_services(container):
    container.register(ILogger, ConsoleLogger, ServiceLifetime.SINGLETON)
    container.register(IUserService, UserService, ServiceLifetime.TRANSIENT)

# 2. Setup container
ServiceProvider.configure(configure_services)

# 3. Use services
user_service = ServiceProvider.resolve(IUserService)
```

## Service Registration

| Method | Usage | Example |
|--------|-------|---------|
| `register()` | Interface to implementation | `container.register(IService, Service, ServiceLifetime.SINGLETON)` |
| `register_instance()` | Pre-created instance | `container.register_instance(IConfig, config_instance)` |
| `register_factory()` | Factory function | `container.register_factory(IService, factory_func)` |
| `register_keyed()` | Keyed services | `container.register_keyed(IService, "key", Service)` |

## Service Lifetimes

| Lifetime | Description | Use Cases |
|----------|-------------|-----------|
| `SINGLETON` | One instance for app lifetime | Loggers, configuration, caches |
| `TRANSIENT` | New instance every time | Stateless services, validators |
| `SCOPED` | One instance per scope | Database contexts, repositories |

## Resolution

| Method | Usage | Returns |
|--------|-------|---------|
| `resolve(type)` | Get service instance | Service or raises exception |
| `try_resolve(type)` | Safe resolution | Service or None |
| `resolve_keyed(type, key)` | Get keyed service | Service or raises exception |
| `get_all_services(type)` | Get all implementations | List of services |

## FastAPI Integration

```python
from di_container.fastapi_integration import FastAPIIntegration, inject

# Setup
app = FastAPI(lifespan=FastAPIIntegration.create_lifespan_manager(configure_services))

# Inject in routes
@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    user_service: IUserService = Depends(inject(IUserService))
):
    return user_service.get_user(user_id)
```

## Common Patterns

### Scoped Services

```python
scope = ServiceProvider.create_scope()
ServiceProvider.begin_scope(scope)
try:
    repository = ServiceProvider.resolve(IRepository)
    # Use scoped service
finally:
    ServiceProvider.end_scope()
```

### Keyed Services

```python
# Register multiple implementations
container.register_keyed(IPaymentService, "paypal", PayPalService)
container.register_keyed(IPaymentService, "stripe", StripeService)

# Resolve by key
payment_service = ServiceProvider.resolve_keyed(IPaymentService, "paypal")
```

### Conditional Registration

```python
def configure_services(container):
    if os.getenv("ENVIRONMENT") == "production":
        container.register(ILogger, FileLogger, ServiceLifetime.SINGLETON)
    else:
        container.register(ILogger, ConsoleLogger, ServiceLifetime.SINGLETON)
```

## Error Handling

| Exception | Cause | Solution |
|-----------|--------|----------|
| `ServiceNotRegisteredException` | Service not registered | Register the service or use `try_resolve()` |
| `CircularDependencyException` | Circular dependencies | Refactor to remove circular references |
| `ScopeException` | Scoped service used outside scope | Use within a scope |

## Best Practices

✅ **Do**

- Use interfaces for abstraction
- Choose appropriate lifetimes
- Handle exceptions gracefully
- Use keyed services for multiple implementations
- Test with mock services

❌ **Don't**

- Create circular dependencies
- Use scoped services outside of scopes
- Register services with missing type annotations
- Ignore dependency injection exceptions
- Mix singleton and transient inappropriately
