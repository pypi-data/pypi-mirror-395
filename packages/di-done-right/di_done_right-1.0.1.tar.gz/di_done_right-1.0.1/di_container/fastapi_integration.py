"""
FastAPI integration utilities for the DI container.
"""

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Callable, Type, TypeVar

from fastapi import Depends, Request

from .service_provider import ServiceProvider

T = TypeVar("T")


class FastAPIIntegration:
    """FastAPI integration utilities for DI container."""

    _scope_key = "_di_scope"

    @staticmethod
    def configure_services(configuration_func: Callable) -> Callable:
        """
        Decorator to configure services for FastAPI application.

        Usage:
            @FastAPIIntegration.configure_services
            def configure(container):
                container.register(IUserService, UserService)
        """
        ServiceProvider.configure(configuration_func)
        return configuration_func

    @staticmethod
    def get_service(service_type: Type[T]) -> Callable[[], T]:
        """
        Create a FastAPI dependency for resolving a service.

        Usage:
            @app.get("/users")
            def get_users(
                user_service: IUserService = Depends(
                    FastAPIIntegration.get_service(IUserService)
                )
            ):
                return user_service.get_all_users()
        """

        def dependency() -> T:
            return ServiceProvider.resolve(service_type)

        return dependency

    @staticmethod
    def get_keyed_service(service_type: Type[T], key: Any) -> Callable[[], T]:
        """
        Create a FastAPI dependency for resolving a keyed service.

        Usage:
            @app.get("/payment")
            def process_payment(
                paypal_service: IPaymentService = Depends(
                    FastAPIIntegration.get_keyed_service(
                        IPaymentService, "paypal"
                    )
                )
            ):
                return paypal_service.process_payment(100.0)
        """

        def dependency() -> T:
            return ServiceProvider.resolve_keyed(service_type, key)

        return dependency

    @staticmethod
    def get_scoped_service(service_type: Type[T]) -> Callable[[Request], T]:
        """
        Create a FastAPI dependency for resolving a scoped service.
        Automatically manages scope lifecycle per request.

        Usage:
            @app.get("/data")
            def get_data(
                repository: IRepository = Depends(
                    FastAPIIntegration.get_scoped_service(IRepository)
                )
            ):
                return repository.get_data()
        """

        def dependency(request: Request) -> T:
            # Get or create scope for this request
            if not hasattr(request.state, FastAPIIntegration._scope_key):
                scope = ServiceProvider.create_scope()
                setattr(request.state, FastAPIIntegration._scope_key, scope)
                ServiceProvider.begin_scope(scope)

            try:
                return ServiceProvider.resolve(service_type)
            except Exception as e:
                # End scope on error
                if hasattr(request.state, FastAPIIntegration._scope_key):
                    ServiceProvider.end_scope()
                    delattr(request.state, FastAPIIntegration._scope_key)
                raise e

        return dependency

    @staticmethod
    def get_keyed_scoped_service(
        service_type: Type[T], key: Any
    ) -> Callable[[Request], T]:
        """
        Create a FastAPI dependency for resolving a keyed scoped service.

        Usage:
            @app.get("/cache")
            def get_cache_data(
                redis_cache: ICache = Depends(
                    FastAPIIntegration.get_keyed_scoped_service(
                        ICache, "redis"
                    )
                )
            ):
                return redis_cache.get("data")
        """

        def dependency(request: Request) -> T:
            # Get or create scope for this request
            if not hasattr(request.state, FastAPIIntegration._scope_key):
                scope = ServiceProvider.create_scope()
                setattr(request.state, FastAPIIntegration._scope_key, scope)
                ServiceProvider.begin_scope(scope)

            try:
                return ServiceProvider.resolve_keyed(service_type, key)
            except Exception as e:
                # End scope on error
                if hasattr(request.state, FastAPIIntegration._scope_key):
                    ServiceProvider.end_scope()
                    delattr(request.state, FastAPIIntegration._scope_key)
                raise e

        return dependency

    @staticmethod
    def create_lifespan_manager(configuration_func: Callable) -> Callable:
        """
        Create a lifespan manager for FastAPI that configures services on startup.

        Usage:
            def configure_services(container):
                container.register(IUserService, UserService)

            app = FastAPI(
                lifespan=FastAPIIntegration.create_lifespan_manager(
                    configure_services
                )
            )
        """

        @asynccontextmanager
        async def lifespan(app: Any) -> AsyncGenerator[None, None]:
            # Startup
            ServiceProvider.configure(configuration_func)
            yield
            # Shutdown - could add cleanup logic here
            pass

        return lifespan


# Middleware to handle scope cleanup
class ScopeCleanupMiddleware:
    """Middleware to ensure scoped services are properly cleaned up after requests."""

    def __init__(self, app: Any) -> None:
        self.app = app

    async def __call__(self, scope: dict, receive: Any, send: Any) -> None:
        if scope["type"] == "http":
            # Create a custom send function to clean up after response
            async def cleanup_send(message: dict) -> None:
                await send(message)
                # Clean up scope after response is sent
                if message["type"] == "http.response.body" and not message.get(
                    "more_body", False
                ):
                    try:
                        ServiceProvider.end_scope()
                    except Exception:
                        pass  # Ignore errors during cleanup

            await self.app(scope, receive, cleanup_send)
        else:
            await self.app(scope, receive, send)


# Convenience dependency functions
def inject(service_type: Type[T]) -> T:
    """
    Convenience function for injecting services in FastAPI.

    Usage:
        @app.get("/users")
        def get_users(user_service: IUserService = Depends(inject)):
            return user_service.get_all_users()
    """
    result: T = Depends(FastAPIIntegration.get_service(service_type))
    return result


def inject_keyed(service_type: Type[T], key: Any) -> T:
    """
    Convenience function for injecting keyed services in FastAPI.

    Usage:
        @app.get("/payment")
        def process_payment(
            paypal: IPaymentService = Depends(
                lambda: inject_keyed(IPaymentService, "paypal")
            )
        ):
            return paypal.process_payment(100.0)
    """
    result: T = Depends(FastAPIIntegration.get_keyed_service(service_type, key))
    return result


def inject_scoped(service_type: Type[T]) -> T:
    """
    Convenience function for injecting scoped services in FastAPI.

    Usage:
        @app.get("/data")
        def get_data(repository: IRepository = Depends(inject_scoped)):
            return repository.get_data()
    """
    result: T = Depends(FastAPIIntegration.get_scoped_service(service_type))
    return result
