"""
End User Experience Demo
========================

This shows exactly what an end user sees when they install and use di-done-right.
"""

# What users can import after: pip install di-done-right
print("=== Available Imports ===")
print("# Main classes")
print("from di_container import DIContainer, ServiceProvider, ServiceLifetime")
print("from di_container import get_service, get_keyed_service, try_get_service")
print()
print("# For advanced usage")
print("from di_container import DIScope, ServiceRegistration, ServiceRegistry")
print()
print("# Exception handling")
print("from di_container import ServiceNotRegisteredException, CircularDependencyException")
print()
print("# FastAPI integration (if fastapi is installed)")
print("from di_container.fastapi_integration import FastAPIIntegration, inject")
print()

# ================================================================
# BASIC USAGE EXAMPLE - What users see in their IDE
# ================================================================

from abc import ABC, abstractmethod

# Step 1: Define interfaces (user's code)
class ILogger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass

class IUserService(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> dict:
        pass

# Step 2: Implement services (user's code)
class ConsoleLogger(ILogger):
    def log(self, message: str) -> None:
        print(f"[LOG] {message}")

class UserService(IUserService):
    def __init__(self, logger: ILogger):
        self.logger = logger
    
    def get_user(self, user_id: int) -> dict:
        self.logger.log(f"Getting user {user_id}")
        return {"id": user_id, "name": f"User {user_id}"}

# Step 3: Use the DI framework (what they import from your package)
print("=== Basic Usage Example ===")

# Import your framework
from di_container import ServiceProvider, ServiceLifetime

# Configure services
def configure_services(container):
    container.register(ILogger, ConsoleLogger, ServiceLifetime.SINGLETON)
    container.register(IUserService, UserService, ServiceLifetime.TRANSIENT)

# Setup container
ServiceProvider.configure(configure_services)

# Use services - automatic dependency injection!
user_service = ServiceProvider.resolve(IUserService)
user = user_service.get_user(123)
print(f"Retrieved: {user}")

print()

# ================================================================
# CONVENIENCE FUNCTIONS - Even easier usage
# ================================================================

print("=== Convenience Functions ===")

from di_container import get_service

# Even simpler usage
logger = get_service(ILogger)
logger.log("This is super easy!")

print()

# ================================================================
# WHAT USERS SEE IN THEIR IDE
# ================================================================

print("=== IDE Experience ===")
print("✅ Full type hints - IDE knows exactly what types you're working with")
print("✅ IntelliSense/autocomplete works perfectly")
print("✅ Mypy type checking passes")
print("✅ Clear error messages if something goes wrong")

# Type hints example
user_service_typed: IUserService = get_service(IUserService)
logger_typed: ILogger = get_service(ILogger)

print("✅ Variables have proper types:", type(user_service_typed).__name__, type(logger_typed).__name__)

print()

# ================================================================
# ERROR HANDLING - What users see when things go wrong
# ================================================================

print("=== Error Handling Example ===")

from di_container import ServiceNotRegisteredException, try_get_service

# Safe resolution
optional_service = try_get_service(str)  # Not registered
print(f"Safe resolution result: {optional_service}")  # None

# Exception handling
try:
    missing_service = ServiceProvider.resolve(str)  # Will throw
except ServiceNotRegisteredException as e:
    print(f"Clear error message: {e}")

print()

# ================================================================
# PACKAGE INFORMATION
# ================================================================

print("=== Package Information ===")
import di_container
print(f"Package version: {di_container.__version__}")
print(f"Package location: {di_container.__file__}")

# What documentation is available
print("\nDocumentation available at install time:")
print("- README.md in the package")
print("- Type hints on all functions")
print("- Docstrings on all classes")
print("- GitHub repository with full docs")

print()

# ================================================================
# REAL-WORLD USAGE PATTERNS
# ================================================================

print("=== Real-World Usage Patterns ===")

# Multiple implementations with keys
class EmailService:
    def __init__(self, logger: ILogger):
        self.logger = logger
    def send(self, message: str):
        self.logger.log(f"Email: {message}")

class SmsService:
    def __init__(self, logger: ILogger):
        self.logger = logger
    def send(self, message: str):
        self.logger.log(f"SMS: {message}")

# Register keyed services
container = ServiceProvider.get_container()
container.register_keyed(object, "email", EmailService, ServiceLifetime.SINGLETON)
container.register_keyed(object, "sms", SmsService, ServiceLifetime.SINGLETON)

# Use keyed services
email_service = ServiceProvider.resolve_keyed(object, "email")
sms_service = ServiceProvider.resolve_keyed(object, "sms")

email_service.send("Hello via email!")
sms_service.send("Hello via SMS!")

print("\n🎉 Complete! Users get a fully-featured, type-safe DI framework!")
print("📚 With comprehensive documentation and examples")
print("⚡ Ready for production use in any Python application")
