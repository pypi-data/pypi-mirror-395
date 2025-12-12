"""Decorators for YAMS plugin development."""

from typing import Callable, TypeVar

F = TypeVar("F", bound=Callable)


def rpc(method_name: str) -> Callable[[F], F]:
    """Decorator to mark a method as an RPC endpoint.

    Usage:
        @rpc("ghidra.analyze")
        def analyze(self, source: dict, opts: dict = None) -> dict:
            return {...}

    The decorated method will be automatically registered as an RPC handler
    when the plugin instance is created (if the plugin's __init__ scans for
    decorated methods).

    Args:
        method_name: The RPC method name (e.g., "ghidra.analyze")

    Returns:
        Decorated function with __rpc_name__ attribute set
    """

    def decorator(func: F) -> F:
        func.__rpc_name__ = method_name  # type: ignore
        return func

    return decorator
