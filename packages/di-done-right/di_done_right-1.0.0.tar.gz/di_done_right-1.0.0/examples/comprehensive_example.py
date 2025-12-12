"""
Comprehensive Example: E-commerce Order Processing System

This example demonstrates all features of the dependency injection framework
in a realistic e-commerce scenario including FastAPI integration.
"""

import os
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

# Import our DI framework
from di_container import ServiceLifetime, ServiceProvider, get_service


# Domain Models
class OrderStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.id = user_id
        self.name = name
        self.email = email


class Product:
    def __init__(self, product_id: int, name: str, price: float, stock: int):
        self.id = product_id
        self.name = name
        self.price = price
        self.stock = stock


class OrderItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
        self.total_price = product.price * quantity


class Order:
    def __init__(self, order_id: int, user: User, items: List[OrderItem]):
        self.id = order_id
        self.user = user
        self.items = items
        self.status = OrderStatus.PENDING
        self.total_amount = sum(item.total_price for item in items)
        self.created_at = datetime.now()


# Interfaces
class ILogger(ABC):
    @abstractmethod
    def log(self, level: str, message: str) -> None:
        pass

    @abstractmethod
    def log_error(self, message: str, exception: Exception = None) -> None:
        pass


class IConfiguration(ABC):
    @abstractmethod
    def get_value(self, key: str, default: Any = None) -> Any:
        pass


class IUserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def save_user(self, user: User) -> None:
        pass


class IProductRepository(ABC):
    @abstractmethod
    def get_product(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def update_stock(self, product_id: int, quantity: int) -> None:
        pass


class IOrderRepository(ABC):
    @abstractmethod
    def save_order(self, order: Order) -> int:
        pass

    @abstractmethod
    def get_order(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    def update_order_status(self, order_id: int, status: OrderStatus) -> None:
        pass


class IPaymentService(ABC):
    @abstractmethod
    def process_payment(self, amount: float, payment_method: str) -> Dict[str, Any]:
        pass


class INotificationService(ABC):
    @abstractmethod
    def send_notification(self, recipient: str, subject: str, message: str) -> bool:
        pass


class IOrderService(ABC):
    @abstractmethod
    def create_order(self, user_id: int, items: List[Dict[str, Any]]) -> Order:
        pass

    @abstractmethod
    def process_order(self, order_id: int, payment_method: str) -> bool:
        pass


# Implementations
class FileLogger(ILogger):
    def __init__(self, config: IConfiguration):
        self.log_file = config.get_value("log_file", "app.log")

    def log(self, level: str, message: str) -> None:
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {level.upper()}: {message}\n"
        print(log_entry.strip())  # For demo purposes

    def log_error(self, message: str, exception: Exception = None) -> None:
        error_msg = f"{message}"
        if exception:
            error_msg += f" - Exception: {str(exception)}"
        self.log("ERROR", error_msg)


class ConsoleLogger(ILogger):
    def log(self, level: str, message: str) -> None:
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] {level.upper()}: {message}")

    def log_error(self, message: str, exception: Exception = None) -> None:
        error_msg = f"{message}"
        if exception:
            error_msg += f" - Exception: {str(exception)}"
        self.log("ERROR", error_msg)


class AppConfiguration(IConfiguration):
    def __init__(self):
        self.config = {
            "log_file": "ecommerce.log",
            "database_url": "sqlite:///ecommerce.db",
            "payment_api_key": "test_key_123",
            "smtp_host": "smtp.example.com",
            "email_sender": "noreply@ecommerce.com",
        }

    def get_value(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)


class SqlUserRepository(IUserRepository):
    def __init__(self, config: IConfiguration, logger: ILogger):
        self.config = config
        self.logger = logger
        self.db_url = config.get_value("database_url")

        # Mock data for demo
        self.users = {
            1: User(1, "John Doe", "john@example.com"),
            2: User(2, "Jane Smith", "jane@example.com"),
        }

    def get_user(self, user_id: int) -> Optional[User]:
        self.logger.log("INFO", f"Fetching user {user_id} from database")
        return self.users.get(user_id)

    def save_user(self, user: User) -> None:
        self.logger.log("INFO", f"Saving user {user.id} to database")
        self.users[user.id] = user


class SqlProductRepository(IProductRepository):
    def __init__(self, config: IConfiguration, logger: ILogger):
        self.config = config
        self.logger = logger

        # Mock data for demo
        self.products = {
            1: Product(1, "Laptop", 999.99, 50),
            2: Product(2, "Mouse", 29.99, 200),
            3: Product(3, "Keyboard", 79.99, 150),
        }

    def get_product(self, product_id: int) -> Optional[Product]:
        self.logger.log("INFO", f"Fetching product {product_id} from database")
        return self.products.get(product_id)

    def update_stock(self, product_id: int, quantity: int) -> None:
        self.logger.log("INFO", f"Updating stock for product {product_id}: -{quantity}")
        if product_id in self.products:
            self.products[product_id].stock -= quantity


class SqlOrderRepository(IOrderRepository):
    def __init__(self, config: IConfiguration, logger: ILogger):
        self.config = config
        self.logger = logger
        self.orders = {}
        self.next_id = 1

    def save_order(self, order: Order) -> int:
        order.id = self.next_id
        self.orders[order.id] = order
        self.next_id += 1
        self.logger.log("INFO", f"Saved order {order.id} to database")
        return order.id

    def get_order(self, order_id: int) -> Optional[Order]:
        self.logger.log("INFO", f"Fetching order {order_id} from database")
        return self.orders.get(order_id)

    def update_order_status(self, order_id: int, status: OrderStatus) -> None:
        if order_id in self.orders:
            self.orders[order_id].status = status
            self.logger.log(
                "INFO", f"Updated order {order_id} status to {status.value}"
            )


# Keyed Service Implementations
class StripePaymentService(IPaymentService):
    def __init__(self, config: IConfiguration, logger: ILogger):
        self.config = config
        self.logger = logger
        self.api_key = config.get_value("stripe_api_key", "test_stripe_key")

    def process_payment(self, amount: float, payment_method: str) -> Dict[str, Any]:
        self.logger.log("INFO", f"Processing Stripe payment: ${amount}")
        # Mock payment processing
        return {
            "success": True,
            "transaction_id": f"stripe_tx_{int(datetime.now().timestamp())}",
            "amount": amount,
            "fee": amount * 0.029,  # 2.9% fee
        }


class PayPalPaymentService(IPaymentService):
    def __init__(self, config: IConfiguration, logger: ILogger):
        self.config = config
        self.logger = logger
        self.api_key = config.get_value("paypal_api_key", "test_paypal_key")

    def process_payment(self, amount: float, payment_method: str) -> Dict[str, Any]:
        self.logger.log("INFO", f"Processing PayPal payment: ${amount}")
        # Mock payment processing
        return {
            "success": True,
            "transaction_id": f"paypal_tx_{int(datetime.now().timestamp())}",
            "amount": amount,
            "fee": amount * 0.034,  # 3.4% fee
        }


class EmailNotificationService(INotificationService):
    def __init__(self, config: IConfiguration, logger: ILogger):
        self.config = config
        self.logger = logger
        self.smtp_host = config.get_value("smtp_host")
        self.sender = config.get_value("email_sender")

    def send_notification(self, recipient: str, subject: str, message: str) -> bool:
        self.logger.log("INFO", f"Sending email to {recipient}: {subject}")
        # Mock email sending
        return True


class SmsNotificationService(INotificationService):
    def __init__(self, config: IConfiguration, logger: ILogger):
        self.config = config
        self.logger = logger
        self.api_key = config.get_value("sms_api_key", "test_sms_key")

    def send_notification(self, recipient: str, subject: str, message: str) -> bool:
        self.logger.log("INFO", f"Sending SMS to {recipient}: {message}")
        # Mock SMS sending
        return True


# Main Business Service
class OrderService(IOrderService):
    def __init__(
        self,
        user_repository: IUserRepository,
        product_repository: IProductRepository,
        order_repository: IOrderRepository,
        logger: ILogger,
    ):
        self.user_repository = user_repository
        self.product_repository = product_repository
        self.order_repository = order_repository
        self.logger = logger

    def create_order(self, user_id: int, items: List[Dict[str, Any]]) -> Order:
        self.logger.log("INFO", f"Creating order for user {user_id}")

        # Get user
        user = self.user_repository.get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Process items
        order_items = []
        for item_data in items:
            product = self.product_repository.get_product(item_data["product_id"])
            if not product:
                raise ValueError(f"Product {item_data['product_id']} not found")

            quantity = item_data["quantity"]
            if product.stock < quantity:
                raise ValueError(f"Insufficient stock for product {product.name}")

            order_items.append(OrderItem(product, quantity))

        # Create order
        order = Order(0, user, order_items)  # ID will be set by repository
        order_id = self.order_repository.save_order(order)

        # Update stock
        for item in order_items:
            self.product_repository.update_stock(item.product.id, item.quantity)

        self.logger.log("INFO", f"Order {order_id} created successfully")
        return order

    def process_order(self, order_id: int, payment_method: str) -> bool:
        self.logger.log("INFO", f"Processing order {order_id} with {payment_method}")

        # Get order
        order = self.order_repository.get_order(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")

        # Get payment service (keyed service)
        container = ServiceProvider.get_container()
        payment_service = container.resolve_keyed(IPaymentService, payment_method)

        # Process payment
        payment_result = payment_service.process_payment(
            order.total_amount, payment_method
        )

        if payment_result["success"]:
            # Update order status
            self.order_repository.update_order_status(order_id, OrderStatus.PROCESSING)

            # Send notification (another keyed service)
            email_service = container.resolve_keyed(INotificationService, "email")
            email_service.send_notification(
                order.user.email,
                "Order Confirmation",
                f"Your order #{order_id} has been processed successfully!",
            )

            self.logger.log("INFO", f"Order {order_id} processed successfully")
            return True
        else:
            self.logger.log_error(f"Payment failed for order {order_id}")
            return False


# Configuration function
def configure_services(container):
    """Configure all services for the e-commerce application"""

    # Determine environment
    environment = os.getenv("ENVIRONMENT", "development")

    # Core services (Singleton)
    container.register(IConfiguration, AppConfiguration, ServiceLifetime.SINGLETON)

    # Logger based on environment
    if environment == "production":
        container.register(ILogger, FileLogger, ServiceLifetime.SINGLETON)
    else:
        container.register(ILogger, ConsoleLogger, ServiceLifetime.SINGLETON)

    # Repositories (Scoped - one per request/operation)
    container.register(IUserRepository, SqlUserRepository, ServiceLifetime.SCOPED)
    container.register(IProductRepository, SqlProductRepository, ServiceLifetime.SCOPED)
    container.register(IOrderRepository, SqlOrderRepository, ServiceLifetime.SCOPED)

    # Business services (Transient - new instance each time)
    container.register(IOrderService, OrderService, ServiceLifetime.TRANSIENT)

    # Payment services (Keyed - multiple implementations)
    container.register_keyed(
        IPaymentService, "stripe", StripePaymentService, ServiceLifetime.SINGLETON
    )
    container.register_keyed(
        IPaymentService, "paypal", PayPalPaymentService, ServiceLifetime.SINGLETON
    )

    # Notification services (Keyed - multiple implementations)
    container.register_keyed(
        INotificationService,
        "email",
        EmailNotificationService,
        ServiceLifetime.SINGLETON,
    )
    container.register_keyed(
        INotificationService, "sms", SmsNotificationService, ServiceLifetime.SINGLETON
    )


# Demo functions
def demo_basic_usage():
    """Demonstrate basic dependency injection usage"""
    print("=== Basic Usage Demo ===")

    # Configure the static container
    ServiceProvider.configure(configure_services)

    # Get services using the static container
    logger = get_service(ILogger)
    config = get_service(IConfiguration)

    logger.log("INFO", "Application started")
    db_url = config.get_value("database_url")
    logger.log("INFO", f"Database URL: {db_url}")

    print()


def demo_keyed_services():
    """Demonstrate keyed services usage"""
    print("=== Keyed Services Demo ===")

    logger = get_service(ILogger)

    # Test different payment providers
    for payment_method in ["stripe", "paypal"]:
        payment_service = ServiceProvider.resolve_keyed(IPaymentService, payment_method)
        result = payment_service.process_payment(100.0, "credit_card")
        logger.log("INFO", f"{payment_method.title()} result: {result}")

    # Test different notification services
    for notification_type in ["email", "sms"]:
        notification_service = ServiceProvider.resolve_keyed(
            INotificationService, notification_type
        )
        success = notification_service.send_notification(
            "user@example.com", "Test", "This is a test message"
        )
        logger.log("INFO", f"{notification_type.title()} sent: {success}")

    print()


def demo_scoped_services():
    """Demonstrate scoped services usage"""
    print("=== Scoped Services Demo ===")

    logger = get_service(ILogger)

    # Create and manage scope manually
    scope = ServiceProvider.create_scope()
    ServiceProvider.begin_scope(scope)

    try:
        # All scoped services will be the same instance within this scope
        user_repo1 = ServiceProvider.resolve(IUserRepository)
        user_repo2 = ServiceProvider.resolve(IUserRepository)

        logger.log("INFO", f"Same repository instance: {user_repo1 is user_repo2}")

        # Use the repository
        user = user_repo1.get_user(1)
        if user:
            logger.log("INFO", f"Found user: {user.name}")

    finally:
        # Always clean up scope
        ServiceProvider.end_scope()

    print()


def demo_complex_order_flow():
    """Demonstrate complex business flow with multiple dependencies"""
    print("=== Complex Order Flow Demo ===")

    logger = get_service(ILogger)

    # Create scope for this operation
    scope = ServiceProvider.create_scope()
    ServiceProvider.begin_scope(scope)

    try:
        # Get order service (with all its dependencies automatically injected)
        order_service = ServiceProvider.resolve(IOrderService)

        # Create an order
        order_items = [
            {"product_id": 1, "quantity": 1},  # Laptop
            {"product_id": 2, "quantity": 2},  # Mouse x2
        ]

        order = order_service.create_order(1, order_items)
        logger.log("INFO", f"Created order {order.id} for ${order.total_amount}")

        # Process the order with Stripe
        success = order_service.process_order(order.id, "stripe")
        logger.log("INFO", f"Order processing result: {success}")

    except Exception as e:
        logger.log_error("Order processing failed", e)
    finally:
        ServiceProvider.end_scope()

    print()


# FastAPI Integration Example
def create_fastapi_app():
    """Create FastAPI application with DI integration"""
    try:
        from fastapi import Depends, FastAPI, HTTPException
        from pydantic import BaseModel

        from di_container.fastapi_integration import (
            FastAPIIntegration,
            inject,
            inject_keyed,
        )

        # Create app with DI lifecycle management
        app = FastAPI(
            title="E-commerce API",
            description="E-commerce API with Dependency Injection",
            version="1.0.0",
            lifespan=FastAPIIntegration.create_lifespan_manager(configure_services),
        )

        # Request/Response models
        class CreateOrderRequest(BaseModel):
            user_id: int
            items: List[Dict[str, Any]]

        class ProcessPaymentRequest(BaseModel):
            payment_method: str

        class OrderResponse(BaseModel):
            id: int
            user_id: int
            total_amount: float
            status: str
            items_count: int

        # Routes with dependency injection
        @app.get("/users/{user_id}")
        async def get_user(
            user_id: int,
            user_repository: IUserRepository = Depends(inject(IUserRepository)),
            logger: ILogger = Depends(inject(ILogger)),
        ):
            logger.log("INFO", f"API: Getting user {user_id}")
            user = user_repository.get_user(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            return {"id": user.id, "name": user.name, "email": user.email}

        @app.post("/orders", response_model=OrderResponse)
        async def create_order(
            request: CreateOrderRequest,
            order_service: IOrderService = Depends(inject(IOrderService)),
            logger: ILogger = Depends(inject(ILogger)),
        ):
            logger.log("INFO", f"API: Creating order for user {request.user_id}")
            try:
                order = order_service.create_order(request.user_id, request.items)
                return OrderResponse(
                    id=order.id,
                    user_id=order.user.id,
                    total_amount=order.total_amount,
                    status=order.status.value,
                    items_count=len(order.items),
                )
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

        @app.post("/orders/{order_id}/process")
        async def process_order(
            order_id: int,
            request: ProcessPaymentRequest,
            order_service: IOrderService = Depends(inject(IOrderService)),
            logger: ILogger = Depends(inject(ILogger)),
        ):
            logger.log("INFO", f"API: Processing order {order_id}")
            try:
                success = order_service.process_order(order_id, request.payment_method)
                return {"success": success, "order_id": order_id}
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

        @app.get("/payment-methods")
        async def get_payment_methods(logger: ILogger = Depends(inject(ILogger))):
            logger.log("INFO", "API: Getting available payment methods")
            return {"methods": ["stripe", "paypal"], "default": "stripe"}

        return app

    except ImportError:
        print("FastAPI not installed. Skipping FastAPI demo.")
        return None


if __name__ == "__main__":
    # Run all demos
    demo_basic_usage()
    demo_keyed_services()
    demo_scoped_services()
    demo_complex_order_flow()

    # FastAPI demo (if available)
    app = create_fastapi_app()
    if app:
        print("=== FastAPI Integration ===")
        print("FastAPI app created successfully!")
        print("To run: uvicorn comprehensive_example:app --reload")
        print("API docs will be available at: http://localhost:8000/docs")

    print("\n=== Demo Complete ===")
    print("This example demonstrates:")
    print("✅ Interface-based dependency injection")
    print("✅ Multiple service lifetimes (Singleton, Transient, Scoped)")
    print("✅ Keyed services for multiple implementations")
    print("✅ Static container management")
    print("✅ Complex object graphs with automatic resolution")
    print("✅ FastAPI integration with automatic DI")
    print("✅ Proper scope management")
    print("✅ Real-world business logic patterns")
