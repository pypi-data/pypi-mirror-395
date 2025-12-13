"""
Unit tests for service registration functionality.
"""

from di_container.enums import RegistrationStrategy, ServiceLifetime
from di_container.registration import ServiceRegistration, ServiceRegistry


class TestService:
    pass


class TestServiceImpl(TestService):
    pass


class TestServiceRegistration:
    """Test cases for ServiceRegistration."""

    def test_type_to_type_registration(self):
        """Test type-to-type registration."""
        registration = ServiceRegistration(
            service_type=TestService,
            implementation_type=TestServiceImpl,
            lifetime=ServiceLifetime.SINGLETON,
        )

        assert registration.service_type == TestService
        assert registration.implementation_type == TestServiceImpl
        assert registration.lifetime == ServiceLifetime.SINGLETON
        assert registration.strategy == RegistrationStrategy.TYPE_TO_TYPE

    def test_type_to_instance_registration(self):
        """Test type-to-instance registration."""
        instance = TestServiceImpl()
        registration = ServiceRegistration(service_type=TestService, instance=instance)

        assert registration.service_type == TestService
        assert registration.instance is instance
        assert registration.strategy == RegistrationStrategy.TYPE_TO_INSTANCE
        assert registration.lifetime == ServiceLifetime.TRANSIENT  # Default

    def test_type_to_factory_registration(self):
        """Test type-to-factory registration."""

        def factory():
            return TestServiceImpl()

        registration = ServiceRegistration(
            service_type=TestService,
            factory=factory,
            lifetime=ServiceLifetime.TRANSIENT,
        )

        assert registration.service_type == TestService
        assert registration.factory is factory
        assert registration.strategy == RegistrationStrategy.TYPE_TO_FACTORY
        assert registration.lifetime == ServiceLifetime.TRANSIENT

    def test_self_registration(self):
        """Test registering type to itself (default behavior)."""
        registration = ServiceRegistration(
            service_type=TestService, lifetime=ServiceLifetime.SINGLETON
        )

        assert registration.service_type == TestService
        assert registration.implementation_type == TestService
        assert registration.strategy == RegistrationStrategy.TYPE_TO_TYPE
        assert registration.lifetime == ServiceLifetime.SINGLETON


class TestServiceRegistry:
    """Test cases for ServiceRegistry."""

    def test_register_and_get_registration(self):
        """Test registering and retrieving registrations."""
        registry = ServiceRegistry()
        registration = ServiceRegistration(TestService, TestServiceImpl)

        registry.register(registration)

        retrieved = registry.get_registration(TestService)
        assert retrieved is registration

    def test_get_nonexistent_registration(self):
        """Test getting non-existent registration returns None."""
        registry = ServiceRegistry()

        registration = registry.get_registration(TestService)
        assert registration is None

    def test_is_registered(self):
        """Test checking if service is registered."""
        registry = ServiceRegistry()
        registration = ServiceRegistration(TestService, TestServiceImpl)

        assert not registry.is_registered(TestService)

        registry.register(registration)
        assert registry.is_registered(TestService)

    def test_get_all_registrations(self):
        """Test getting all registrations."""
        registry = ServiceRegistry()
        registration1 = ServiceRegistration(TestService, TestServiceImpl)
        registration2 = ServiceRegistration(str, str)

        registry.register(registration1)
        registry.register(registration2)

        all_registrations = registry.get_all_registrations()
        assert len(all_registrations) == 2
        # Keys are now tuples of (Type, Key)
        assert all_registrations[(TestService, None)] is registration1
        assert all_registrations[(str, None)] is registration2

    def test_clear(self):
        """Test clearing all registrations."""
        registry = ServiceRegistry()
        registration = ServiceRegistration(TestService, TestServiceImpl)

        registry.register(registration)
        assert registry.is_registered(TestService)

        registry.clear()
        assert not registry.is_registered(TestService)
        assert len(registry.get_all_registrations()) == 0
