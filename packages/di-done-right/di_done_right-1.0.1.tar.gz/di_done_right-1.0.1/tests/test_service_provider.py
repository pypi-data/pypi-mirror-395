"""
Unit tests for the static service provider functionality.
"""

import threading
from typing import Protocol

import pytest

from di_container import DIContainer, ServiceLifetime
from di_container.service_provider import (
    ContainerNotConfiguredException,
    ServiceProvider,
    get_service,
)


class ITestService(Protocol):
    def get_value(self) -> str: ...


class TestService:
    def __init__(self):
        pass

    def get_value(self) -> str:
        return "test_value"


class TestServiceWithDependency:
    def __init__(self, dependency: ITestService):
        self.dependency = dependency

    def get_combined_value(self) -> str:
        return f"combined_{self.dependency.get_value()}"


class TestServiceProvider:
    """Test cases for ServiceProvider."""

    def setup_method(self):
        """Reset service provider before each test."""
        ServiceProvider.reset()

    def teardown_method(self):
        """Reset service provider after each test."""
        ServiceProvider.reset()

    def test_configure_and_resolve(self):
        """Test configuring and resolving services."""

        def configure(container: DIContainer):
            container.register(ITestService, TestService, ServiceLifetime.SINGLETON)

        ServiceProvider.configure(configure)

        service = ServiceProvider.resolve(ITestService)
        assert isinstance(service, TestService)
        assert service.get_value() == "test_value"

    def test_singleton_behavior_across_provider(self):
        """Test that singleton services maintain state across provider calls."""

        def configure(container: DIContainer):
            container.register(ITestService, TestService, ServiceLifetime.SINGLETON)

        ServiceProvider.configure(configure)

        service1 = ServiceProvider.resolve(ITestService)
        service2 = ServiceProvider.resolve(ITestService)

        assert service1 is service2

    def test_not_configured_exception(self):
        """Test exception when using provider before configuration."""
        with pytest.raises(ContainerNotConfiguredException):
            ServiceProvider.resolve(ITestService)

        with pytest.raises(ContainerNotConfiguredException):
            ServiceProvider.get_container()

    def test_already_configured_exception(self):
        """Test exception when trying to configure twice."""

        def configure1(container: DIContainer):
            container.register(ITestService, TestService)

        def configure2(container: DIContainer):
            container.register(ITestService, TestService)

        ServiceProvider.configure(configure1)

        with pytest.raises(
            Exception
        ):  # Should raise DIException about already configured
            ServiceProvider.configure(configure2)

    def test_dependency_injection_through_provider(self):
        """Test dependency injection works through provider."""

        def configure(container: DIContainer):
            container.register(ITestService, TestService, ServiceLifetime.SINGLETON)
            container.register(
                TestServiceWithDependency,
                TestServiceWithDependency,
                ServiceLifetime.TRANSIENT,
            )

        ServiceProvider.configure(configure)

        service = ServiceProvider.resolve(TestServiceWithDependency)
        assert isinstance(service, TestServiceWithDependency)
        assert service.get_combined_value() == "combined_test_value"

    def test_keyed_services_through_provider(self):
        """Test keyed services work through provider."""

        def configure(container: DIContainer):
            container.register_keyed(
                ITestService, "test1", TestService, ServiceLifetime.SINGLETON
            )
            container.register_keyed(
                ITestService, "test2", TestService, ServiceLifetime.TRANSIENT
            )

        ServiceProvider.configure(configure)

        service1 = ServiceProvider.resolve_keyed(ITestService, "test1")
        service2 = ServiceProvider.resolve_keyed(ITestService, "test2")

        assert isinstance(service1, TestService)
        assert isinstance(service2, TestService)
        assert service1 is not service2  # Different registrations

    def test_try_resolve_methods(self):
        """Test try_resolve methods."""

        def configure(container: DIContainer):
            container.register(ITestService, TestService)

        ServiceProvider.configure(configure)

        # Should return service
        service = ServiceProvider.try_resolve(ITestService)
        assert isinstance(service, TestService)

        # Should return None for unregistered
        unregistered = ServiceProvider.try_resolve(str)
        assert unregistered is None

        # Test keyed try_resolve
        keyed_service = ServiceProvider.try_resolve_keyed(ITestService, "nonexistent")
        assert keyed_service is None

    def test_scope_management_through_provider(self):
        """Test scope management through provider."""

        def configure(container: DIContainer):
            container.register(ITestService, TestService, ServiceLifetime.SCOPED)

        ServiceProvider.configure(configure)

        # Create and use scope
        scope = ServiceProvider.create_scope()
        ServiceProvider.begin_scope(scope)

        try:
            service1 = ServiceProvider.resolve(ITestService)
            service2 = ServiceProvider.resolve(ITestService)
            assert service1 is service2  # Same instance in scope
        finally:
            ServiceProvider.end_scope()

    def test_is_configured(self):
        """Test is_configured method."""
        assert not ServiceProvider.is_configured()

        def configure(container: DIContainer):
            container.register(ITestService, TestService)

        ServiceProvider.configure(configure)
        assert ServiceProvider.is_configured()

        ServiceProvider.reset()
        assert not ServiceProvider.is_configured()

    def test_thread_safety(self):
        """Test thread safety of service provider."""
        results = []
        errors = []

        def configure_and_resolve():
            try:

                def configure(container: DIContainer):
                    container.register(
                        ITestService, TestService, ServiceLifetime.SINGLETON
                    )

                # Only one thread should succeed in configuration
                ServiceProvider.configure(configure)
                service = ServiceProvider.resolve(ITestService)
                results.append(service)
            except Exception as e:
                errors.append(e)

        # Start multiple threads trying to configure
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=configure_and_resolve)
            threads.append(thread)
            thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join()

        # Only one should succeed in configuration, but all should be able to resolve
        # after configuration is done
        assert len(results) >= 1  # At least one success
        assert len(errors) >= 1  # At least one "already configured" error

        # All successful results should be the same instance (singleton)
        if len(results) > 1:
            first_service = results[0]
            for service in results[1:]:
                assert service is first_service


class TestConvenienceFunctions:
    """Test cases for convenience functions."""

    def setup_method(self):
        """Reset service provider before each test."""
        ServiceProvider.reset()

    def teardown_method(self):
        """Reset service provider after each test."""
        ServiceProvider.reset()

    def test_get_service_function(self):
        """Test get_service convenience function."""

        def configure(container: DIContainer):
            container.register(ITestService, TestService, ServiceLifetime.SINGLETON)

        ServiceProvider.configure(configure)

        service = get_service(ITestService)
        assert isinstance(service, TestService)
        assert service.get_value() == "test_value"
