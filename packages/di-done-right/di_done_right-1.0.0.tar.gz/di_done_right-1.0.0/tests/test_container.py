"""
Unit tests for the DI container.
"""

from typing import Protocol

import pytest

from di_container import (
    CircularDependencyException,
    DIContainer,
    ScopeException,
    ServiceLifetime,
    ServiceNotRegisteredException,
)


# Test interfaces and classes
class ITestService(Protocol):
    def get_value(self) -> str: ...


class TestService:
    def __init__(self):
        pass

    def get_value(self) -> str:
        return "test"


class TestServiceWithDependency:
    def __init__(self, dependency: ITestService):
        self.dependency = dependency

    def get_value(self) -> str:
        return f"dependent: {self.dependency.get_value()}"


class ICircularA(Protocol):
    pass


class ICircularB(Protocol):
    pass


class CircularA:
    def __init__(self, b: ICircularB):
        self.b = b


class CircularB:
    def __init__(self, a: ICircularA):
        self.a = a


class ConcreteService:
    def __init__(self):
        pass

    def do_work(self) -> str:
        return "concrete work"


class ServiceWithConcreteDependency:
    def __init__(self, concrete_service: ConcreteService):
        self.concrete_service = concrete_service

    def get_result(self) -> str:
        return f"result: {self.concrete_service.do_work()}"


class IPaymentService(Protocol):
    def process_payment(self, amount: float) -> str: ...


class PayPalService:
    def __init__(self):
        pass

    def process_payment(self, amount: float) -> str:
        return f"PayPal: ${amount}"


class StripeService:
    def __init__(self):
        pass

    def process_payment(self, amount: float) -> str:
        return f"Stripe: ${amount}"


class PaymentProcessor:
    def __init__(self, payment_service: IPaymentService):
        self.payment_service = payment_service

    def process(self, amount: float) -> str:
        return self.payment_service.process_payment(amount)


class TestDIContainer:
    """Test cases for DIContainer."""

    def test_register_and_resolve_transient(self):
        """Test basic registration and resolution."""
        container = DIContainer()
        container.register(ITestService, TestService, ServiceLifetime.TRANSIENT)

        service1 = container.resolve(ITestService)
        service2 = container.resolve(ITestService)

        assert isinstance(service1, TestService)
        assert isinstance(service2, TestService)
        assert service1 is not service2  # Different instances for transient

    def test_register_and_resolve_singleton(self):
        """Test singleton lifetime."""
        container = DIContainer()
        container.register(ITestService, TestService, ServiceLifetime.SINGLETON)

        service1 = container.resolve(ITestService)
        service2 = container.resolve(ITestService)

        assert isinstance(service1, TestService)
        assert service1 is service2  # Same instance for singleton

    def test_register_instance(self):
        """Test instance registration."""
        container = DIContainer()
        instance = TestService()
        container.register_instance(ITestService, instance)

        resolved = container.resolve(ITestService)
        assert resolved is instance

    def test_register_factory(self):
        """Test factory registration."""
        container = DIContainer()

        def create_service() -> ITestService:
            return TestService()

        container.register_factory(
            ITestService, create_service, ServiceLifetime.TRANSIENT
        )

        service = container.resolve(ITestService)
        assert isinstance(service, TestService)

    def test_dependency_injection(self):
        """Test constructor dependency injection."""
        container = DIContainer()
        container.register(ITestService, TestService, ServiceLifetime.SINGLETON)
        container.register(
            TestServiceWithDependency,
            TestServiceWithDependency,
            ServiceLifetime.TRANSIENT,
        )

        service = container.resolve(TestServiceWithDependency)
        assert isinstance(service, TestServiceWithDependency)
        assert service.get_value() == "dependent: test"

    def test_service_not_registered_exception(self):
        """Test exception when service is not registered."""
        container = DIContainer()

        with pytest.raises(ServiceNotRegisteredException):
            container.resolve(ITestService)

    def test_circular_dependency_detection(self):
        """Test circular dependency detection."""
        container = DIContainer()
        container.register(ICircularA, CircularA)
        container.register(ICircularB, CircularB)

        with pytest.raises(CircularDependencyException):
            container.resolve(ICircularA)

    def test_scoped_services(self):
        """Test scoped service lifetime."""
        container = DIContainer()
        container.register(ITestService, TestService, ServiceLifetime.SCOPED)

        # Test without scope should raise exception
        with pytest.raises(ScopeException):
            container.resolve(ITestService)

        # Test with scope
        scope = container.begin_scope()
        try:
            service1 = container.resolve(ITestService)
            service2 = container.resolve(ITestService)

            assert isinstance(service1, TestService)
            assert service1 is service2  # Same instance within scope
        finally:
            container.end_scope()

        # Test new scope creates new instance
        scope2 = container.begin_scope()
        try:
            service3 = container.resolve(ITestService)
            assert isinstance(service3, TestService)
            assert service3 is not service1  # Different instance in new scope
        finally:
            container.end_scope()

    def test_is_registered(self):
        """Test service registration check."""
        container = DIContainer()

        assert not container.is_registered(ITestService)

        container.register(ITestService, TestService)
        assert container.is_registered(ITestService)

    def test_clear(self):
        """Test clearing container."""
        container = DIContainer()
        container.register(ITestService, TestService, ServiceLifetime.SINGLETON)

        # Resolve to create singleton instance
        container.resolve(ITestService)

        container.clear()
        assert not container.is_registered(ITestService)

        # Should raise exception after clear
        with pytest.raises(ServiceNotRegisteredException):
            container.resolve(ITestService)

    def test_register_concrete_type_without_interface(self):
        """Test registering concrete types without interfaces."""
        container = DIContainer()

        # Register concrete type to itself
        container.register(ConcreteService, lifetime=ServiceLifetime.SINGLETON)

        service1 = container.resolve(ConcreteService)
        service2 = container.resolve(ConcreteService)

        assert isinstance(service1, ConcreteService)
        assert service1 is service2  # Same instance for singleton
        assert service1.do_work() == "concrete work"

    def test_concrete_type_dependency_injection(self):
        """Test dependency injection with concrete types."""
        container = DIContainer()

        # Register concrete types
        container.register(ConcreteService, lifetime=ServiceLifetime.TRANSIENT)
        container.register(
            ServiceWithConcreteDependency, lifetime=ServiceLifetime.TRANSIENT
        )

        service = container.resolve(ServiceWithConcreteDependency)

        assert isinstance(service, ServiceWithConcreteDependency)
        assert isinstance(service.concrete_service, ConcreteService)
        assert service.get_result() == "result: concrete work"

    def test_mixed_interface_and_concrete_registration(self):
        """Test mixing interface-based and concrete type registration."""
        container = DIContainer()

        # Register interface to implementation
        container.register(ITestService, TestService, ServiceLifetime.SINGLETON)

        # Register concrete type to itself
        container.register(ConcreteService, lifetime=ServiceLifetime.TRANSIENT)

        # Both should work
        test_service = container.resolve(ITestService)
        concrete_service = container.resolve(ConcreteService)

        assert isinstance(test_service, TestService)
        assert isinstance(concrete_service, ConcreteService)

    def test_register_keyed_services(self):
        """Test registering and resolving keyed services."""
        container = DIContainer()

        # Register multiple implementations with keys
        container.register_keyed(
            IPaymentService, "paypal", PayPalService, ServiceLifetime.SINGLETON
        )
        container.register_keyed(
            IPaymentService, "stripe", StripeService, ServiceLifetime.SINGLETON
        )

        # Resolve by key
        paypal_service = container.resolve_keyed(IPaymentService, "paypal")
        stripe_service = container.resolve_keyed(IPaymentService, "stripe")

        assert isinstance(paypal_service, PayPalService)
        assert isinstance(stripe_service, StripeService)
        assert paypal_service.process_payment(100.0) == "PayPal: $100.0"
        assert stripe_service.process_payment(100.0) == "Stripe: $100.0"

        # Test singleton behavior
        paypal_service2 = container.resolve_keyed(IPaymentService, "paypal")
        assert paypal_service is paypal_service2

    def test_keyed_service_not_found(self):
        """Test exception when keyed service is not found."""
        container = DIContainer()
        container.register_keyed(IPaymentService, "paypal", PayPalService)

        # Should work with correct key
        service = container.resolve_keyed(IPaymentService, "paypal")
        assert isinstance(service, PayPalService)

        # Should fail with wrong key
        with pytest.raises(ServiceNotRegisteredException):
            container.resolve_keyed(IPaymentService, "stripe")

    def test_try_resolve_keyed(self):
        """Test try_resolve_keyed method."""
        container = DIContainer()
        container.register_keyed(IPaymentService, "paypal", PayPalService)

        # Should return service for valid key
        service = container.try_resolve_keyed(IPaymentService, "paypal")
        assert isinstance(service, PayPalService)

        # Should return None for invalid key
        service = container.try_resolve_keyed(IPaymentService, "stripe")
        assert service is None

    def test_register_keyed_instance(self):
        """Test registering keyed instances."""
        container = DIContainer()

        paypal_instance = PayPalService()
        stripe_instance = StripeService()

        container.register_keyed_instance(IPaymentService, "paypal", paypal_instance)
        container.register_keyed_instance(IPaymentService, "stripe", stripe_instance)

        resolved_paypal = container.resolve_keyed(IPaymentService, "paypal")
        resolved_stripe = container.resolve_keyed(IPaymentService, "stripe")

        assert resolved_paypal is paypal_instance
        assert resolved_stripe is stripe_instance

    def test_register_keyed_factory(self):
        """Test registering keyed factories."""
        container = DIContainer()

        def create_paypal():
            return PayPalService()

        def create_stripe():
            return StripeService()

        container.register_keyed_factory(IPaymentService, "paypal", create_paypal)
        container.register_keyed_factory(IPaymentService, "stripe", create_stripe)

        paypal_service = container.resolve_keyed(IPaymentService, "paypal")
        stripe_service = container.resolve_keyed(IPaymentService, "stripe")

        assert isinstance(paypal_service, PayPalService)
        assert isinstance(stripe_service, StripeService)

    def test_mixed_keyed_and_unkeyed_services(self):
        """Test mixing keyed and unkeyed service registrations."""
        container = DIContainer()

        # Register default implementation
        container.register(IPaymentService, PayPalService, ServiceLifetime.SINGLETON)

        # Register keyed implementations
        container.register_keyed(
            IPaymentService, "stripe", StripeService, ServiceLifetime.SINGLETON
        )
        container.register_keyed(
            IPaymentService, "paypal", PayPalService, ServiceLifetime.SINGLETON
        )

        # Resolve default (unkeyed)
        default_service = container.resolve(IPaymentService)
        assert isinstance(default_service, PayPalService)

        # Resolve keyed
        stripe_service = container.resolve_keyed(IPaymentService, "stripe")
        paypal_service = container.resolve_keyed(IPaymentService, "paypal")

        assert isinstance(stripe_service, StripeService)
        assert isinstance(paypal_service, PayPalService)

        # Default and keyed paypal should be different instances
        # (different registrations)
        assert default_service is not paypal_service

    def test_get_all_services(self):
        """Test getting all services for a type."""
        container = DIContainer()

        # Register multiple implementations
        container.register(IPaymentService, PayPalService)
        container.register_keyed(IPaymentService, "stripe", StripeService)
        container.register_keyed(IPaymentService, "paypal2", PayPalService)

        all_services = container.get_all_services(IPaymentService)

        assert len(all_services) == 3
        service_types = [type(service) for service in all_services]
        assert PayPalService in service_types
        assert StripeService in service_types

    def test_keyed_services_with_scopes(self):
        """Test keyed services with scoped lifetimes."""
        container = DIContainer()

        container.register_keyed(
            IPaymentService, "paypal", PayPalService, ServiceLifetime.SCOPED
        )
        container.register_keyed(
            IPaymentService, "stripe", StripeService, ServiceLifetime.SCOPED
        )

        scope = container.begin_scope()
        try:
            paypal1 = container.resolve_keyed(IPaymentService, "paypal")
            paypal2 = container.resolve_keyed(IPaymentService, "paypal")
            stripe1 = container.resolve_keyed(IPaymentService, "stripe")

            # Same key should return same instance in scope
            assert paypal1 is paypal2
            # Different keys should return different instances
            assert paypal1 is not stripe1

        finally:
            container.end_scope()
