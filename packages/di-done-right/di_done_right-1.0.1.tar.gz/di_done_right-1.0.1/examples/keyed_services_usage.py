"""
Example demonstrating keyed services functionality.
"""

from abc import ABC, abstractmethod

from di_container import DIContainer, ServiceLifetime


# Define interfaces
class IPaymentService(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> str:
        pass


class INotificationService(ABC):
    @abstractmethod
    def send_notification(self, message: str) -> None:
        pass


class ILogger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass


# Payment service implementations
class PayPalService(IPaymentService):
    def __init__(self, logger: ILogger):
        self.logger = logger

    def process_payment(self, amount: float) -> str:
        self.logger.log(f"Processing PayPal payment: ${amount}")
        return f"PayPal payment processed: ${amount}"


class StripeService(IPaymentService):
    def __init__(self, logger: ILogger):
        self.logger = logger

    def process_payment(self, amount: float) -> str:
        self.logger.log(f"Processing Stripe payment: ${amount}")
        return f"Stripe payment processed: ${amount}"


class CryptoService(IPaymentService):
    def __init__(self, logger: ILogger):
        self.logger = logger

    def process_payment(self, amount: float) -> str:
        self.logger.log(f"Processing crypto payment: ${amount}")
        return f"Crypto payment processed: ${amount}"


# Notification service implementations
class EmailNotificationService(INotificationService):
    def __init__(self, logger: ILogger):
        self.logger = logger

    def send_notification(self, message: str) -> None:
        self.logger.log(f"Sending email notification: {message}")


class SmsNotificationService(INotificationService):
    def __init__(self, logger: ILogger):
        self.logger = logger

    def send_notification(self, message: str) -> None:
        self.logger.log(f"Sending SMS notification: {message}")


# Logger implementations
class ConsoleLogger(ILogger):
    def log(self, message: str) -> None:
        print(f"[CONSOLE] {message}")


class FileLogger(ILogger):
    def __init__(self):
        self.filename = "app.log"

    def log(self, message: str) -> None:
        print(f"[FILE:{self.filename}] {message}")


# Business service that uses keyed services
class PaymentProcessor:
    def __init__(self, logger: ILogger):
        self.logger = logger
        self.container = None  # Will be injected

    def set_container(self, container: DIContainer):
        self.container = container

    def process_payment(self, payment_method: str, amount: float) -> str:
        """Process payment using the specified payment method."""
        payment_service = self.container.resolve_keyed(IPaymentService, payment_method)
        result = payment_service.process_payment(amount)

        # Send notification based on payment method
        if payment_method in ["paypal", "stripe"]:
            notification_service = self.container.resolve_keyed(
                INotificationService, "email"
            )
        else:
            notification_service = self.container.resolve_keyed(
                INotificationService, "sms"
            )

        notification_service.send_notification(f"Payment completed: {result}")
        return result

    def get_available_payment_methods(self) -> list[str]:
        """Get all available payment methods."""
        return ["paypal", "stripe", "crypto"]


def main():
    """Demonstrate keyed services usage."""
    container = DIContainer()

    # Register logger
    container.register(ILogger, ConsoleLogger, ServiceLifetime.SINGLETON)

    # Register payment services with keys
    container.register_keyed(
        IPaymentService, "paypal", PayPalService, ServiceLifetime.TRANSIENT
    )
    container.register_keyed(
        IPaymentService, "stripe", StripeService, ServiceLifetime.TRANSIENT
    )
    container.register_keyed(
        IPaymentService, "crypto", CryptoService, ServiceLifetime.TRANSIENT
    )

    # Register notification services with keys
    container.register_keyed(
        INotificationService,
        "email",
        EmailNotificationService,
        ServiceLifetime.TRANSIENT,
    )
    container.register_keyed(
        INotificationService, "sms", SmsNotificationService, ServiceLifetime.TRANSIENT
    )

    # Register and resolve payment processor
    container.register(PaymentProcessor, lifetime=ServiceLifetime.SINGLETON)
    processor = container.resolve(PaymentProcessor)
    processor.set_container(container)

    print("=== Keyed Services Demo ===\n")

    # Process payments using different methods
    methods = processor.get_available_payment_methods()
    amount = 99.99

    for method in methods:
        print(f"Processing {method} payment:")
        result = processor.process_payment(method, amount)
        print(f"Result: {result}\n")

    # Demonstrate resolving specific keyed services
    print("=== Direct Keyed Service Resolution ===")
    paypal = container.resolve_keyed(IPaymentService, "paypal")
    stripe = container.resolve_keyed(IPaymentService, "stripe")

    print(f"PayPal: {paypal.process_payment(50.0)}")
    print(f"Stripe: {stripe.process_payment(75.0)}")

    # Demonstrate try_resolve_keyed for optional services
    print("\n=== Optional Keyed Service Resolution ===")
    apple_pay = container.try_resolve_keyed(IPaymentService, "applepay")
    if apple_pay:
        print("Apple Pay is available")
    else:
        print("Apple Pay is not registered")

    # Demonstrate get_all_services
    print("\n=== All Payment Services ===")
    all_payment_services = container.get_all_services(IPaymentService)
    print(f"Total payment services registered: {len(all_payment_services)}")

    for i, service in enumerate(all_payment_services, 1):
        service_name = service.__class__.__name__
        print(f"{i}. {service_name}")


if __name__ == "__main__":
    main()
