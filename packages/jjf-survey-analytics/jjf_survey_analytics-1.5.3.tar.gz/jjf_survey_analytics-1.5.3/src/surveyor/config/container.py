"""
Dependency Injection Container for the Surveyor application.

This module provides a simple DI container to manage service dependencies
and configuration throughout the application.
"""

import inspect
from functools import wraps
from typing import Any, Callable, Dict, Type, TypeVar

T = TypeVar("T")


class DIContainer:
    """Simple dependency injection container."""

    def __init__(self):
        self._services: Dict[Type, Any] = {}
        self._singletons: Dict[Type, Any] = {}
        self._factories: Dict[Type, Callable] = {}

    def register_singleton(self, interface: Type[T], implementation: Type[T]) -> None:
        """Register a service as a singleton."""
        self._services[interface] = implementation

    def register_transient(self, interface: Type[T], implementation: Type[T]) -> None:
        """Register a service as transient (new instance each time)."""
        self._factories[interface] = implementation

    def register_instance(self, interface: Type[T], instance: T) -> None:
        """Register a specific instance."""
        self._singletons[interface] = instance

    def get(self, interface: Type[T]) -> T:
        """Get an instance of the requested service."""
        # Check if we have a specific instance registered
        if interface in self._singletons:
            return self._singletons[interface]

        # Check if it's a singleton service
        if interface in self._services:
            if interface not in self._singletons:
                implementation = self._services[interface]
                instance = self._create_instance(implementation)
                self._singletons[interface] = instance
            return self._singletons[interface]

        # Check if it's a transient service
        if interface in self._factories:
            implementation = self._factories[interface]
            return self._create_instance(implementation)

        # Try to create instance directly if it's a concrete class
        if inspect.isclass(interface):
            return self._create_instance(interface)

        raise ValueError(f"Service {interface} not registered")

    def _create_instance(self, cls: Type[T]) -> T:
        """Create an instance with dependency injection."""
        # Get constructor signature
        sig = inspect.signature(cls.__init__)
        kwargs = {}

        # Resolve dependencies
        for param_name, param in sig.parameters.items():
            if param_name == "sel":
                continue

            if param.annotation != inspect.Parameter.empty:
                # Try to resolve the dependency
                try:
                    kwargs[param_name] = self.get(param.annotation)
                except ValueError:
                    # If we can't resolve it and there's no default, raise error
                    if param.default == inspect.Parameter.empty:
                        raise ValueError(f"Cannot resolve dependency {param.annotation} for {cls}")

        return cls(**kwargs)


# Global container instance
container = DIContainer()


def inject(func: Callable) -> Callable:
    """Decorator to inject dependencies into function parameters."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound_args = sig.bind_partial(*args, **kwargs)

        # Inject missing dependencies
        for param_name, param in sig.parameters.items():
            if (
                param_name not in bound_args.arguments
                and param.annotation != inspect.Parameter.empty
            ):
                try:
                    bound_args.arguments[param_name] = container.get(param.annotation)
                except ValueError:
                    if param.default == inspect.Parameter.empty:
                        raise

        return func(*bound_args.args, **bound_args.kwargs)

    return wrapper
