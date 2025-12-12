from __future__ import annotations

from functools import wraps
from typing import Awaitable, Callable, ParamSpec, TypeVar

from fastmcp.exceptions import ToolError

P = ParamSpec("P")
R = TypeVar("R")


def wrap_tool_exceptions(message_prefix: str) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """
    Decorator that converts unhandled exceptions into ToolError instances so FastMCP
    clients receive structured failures without duplicating try/except blocks.
    """

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return await func(*args, **kwargs)
            except ToolError:
                raise
            except Exception as exc:
                raise ToolError(f"{message_prefix}: {exc}") from exc

        return wrapper

    return decorator

