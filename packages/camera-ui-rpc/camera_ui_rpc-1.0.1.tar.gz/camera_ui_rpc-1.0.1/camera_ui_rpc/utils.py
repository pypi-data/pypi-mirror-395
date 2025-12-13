"""Utility functions for the RPC library."""

import time
from collections.abc import AsyncGenerator
from random import randint
from typing import TYPE_CHECKING, Any, TypeVar

from nats.micro.service import ServiceInfo

if TYPE_CHECKING:
    from .client import RPCClient

T = TypeVar("T")


def generate_id() -> str:
    """Generate a unique ID for requests."""
    return f"{int(time.time() * 1000)}-{randint(100000, 999999)}"


def is_generator(func: Any) -> bool:
    """Check if a function returns a generator."""
    if not callable(func):
        return False

    # Check if it's a generator function
    return is_sync_generator(func) or is_async_generator(func)


def is_sync_generator(func: Any) -> bool:
    """Check if a function returns a synchronous generator."""
    if not callable(func):
        return False

    # Check if it's a generator function
    import inspect

    return inspect.isgeneratorfunction(func) or inspect.isgenerator(func)


def is_async_generator(func: Any) -> bool:
    """Check if a function returns an async generator."""
    if not callable(func):
        return False

    # Check if it's a coroutine function that might return an async generator
    import inspect

    if inspect.isasyncgenfunction(func):
        return True

    # Check return annotation
    if hasattr(func, "__annotations__"):
        return_annotation = func.__annotations__.get("return")
        if return_annotation:
            # Check if it's AsyncGenerator type
            origin = getattr(return_annotation, "__origin__", None)
            if origin is AsyncGenerator:
                return True

    return False


def is_async_function(func: Any) -> bool:
    """Check if a function is an async function."""
    if not callable(func):
        return False

    # Check if it's a coroutine function
    import inspect

    return inspect.iscoroutinefunction(func) or inspect.iscoroutine(func) or inspect.isawaitable(func)


def create_proxy(client: "RPCClient", namespace: str, path: list[str] | None = None) -> Any:
    """
    Create a proxy for RPC calls with support for nested objects.

    Args:
        client: RPC client with call and call_stream methods
        namespace: RPC namespace
        path: Current path in proxy hierarchy

    Returns:
        Proxy that intercepts attribute access and method calls
    """
    if path is None:
        path = []

    _path: list[str] = path.copy()

    class RPCProxy:
        def __getattr__(self, name: str) -> Any:
            # Build the full path
            full_path = _path + [name]

            # Return a callable proxy that can also be awaited directly
            class CallableProxy:
                def __call__(self, *args: Any, **kwargs: Any) -> Any:
                    method = ".".join(full_path)

                    # Check if this is a streaming method
                    is_generator = "generate" in name.lower()
                    is_pull_iterator = "pull" in name.lower()

                    if is_generator:
                        return client.call_stream(f"rpc.{namespace}.{method}", *args)
                    elif is_pull_iterator:
                        return client.call_pull_iterator(f"rpc.{namespace}.{method}", *args)
                    else:
                        return client.call(f"rpc.{namespace}.{method}", *args)

                def __getattr__(self, nested_name: str) -> Any:
                    # Handle nested property access
                    return create_proxy(client, namespace, full_path).__getattribute__(nested_name)

                def __await__(self) -> Any:
                    # Make this proxy awaitable - call with no arguments
                    return self().__await__()

            return CallableProxy()

        def __repr__(self) -> str:
            path_str = ".".join(_path) if _path else ""
            return f"<RPCProxy {namespace}{('.' + path_str) if path_str else ''}>"

    return RPCProxy()


def create_service_proxy(
    client: "RPCClient", service_info: ServiceInfo, timeout: int | None = None, path: list[str] | None = None
) -> Any:
    """
    Create a service proxy with proper streaming support.

    Args:
        client: RPC client instance
        service_info: Service information from discovery
        timeout: Optional timeout for requests
        path: Current path in proxy hierarchy

    Returns:
        Proxy that intercepts attribute access and method calls
    """
    if path is None:
        path = []

    _path: list[str] = path.copy()

    class ServiceProxy:
        def __getattr__(self, name: str) -> Any:
            full_path = _path + [name]
            full_path_str = ".".join(full_path)

            # Check if this is an endpoint
            endpoint = None
            for ep in service_info.endpoints:
                # Match exact path or last segment
                if ep.subject == full_path_str:
                    endpoint = ep
                    break
                parts = ep.subject.split(".")
                if parts[-1] == name and ".".join(parts[:-1]) == ".".join(_path):
                    endpoint = ep
                    break

            if endpoint:
                _endpoint = endpoint

                # Return a callable proxy similar to create_proxy
                class CallableProxy:
                    def __call__(self, *args: Any, **kwargs: Any) -> Any:
                        # Check if this is a streaming endpoint
                        is_generator = "generate" in name.lower()
                        is_pull_iterator = "pull" in name.lower()

                        if is_generator:
                            return client.call_stream(_endpoint.subject, *args)
                        elif is_pull_iterator:
                            return client.call_pull_iterator(_endpoint.subject, *args)
                        else:
                            return client.call(_endpoint.subject, *args)

                return CallableProxy()

            # Check if this is a nested namespace
            prefix = full_path_str + "."
            has_nested = any(ep.subject.startswith(prefix) for ep in service_info.endpoints)

            if has_nested:
                return create_service_proxy(client, service_info, timeout, full_path)

            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        def __repr__(self) -> str:
            path_str = ".".join(_path) if _path else ""
            return f"<ServiceProxy {service_info.name}{('.' + path_str) if path_str else ''}>"

    return ServiceProxy()
