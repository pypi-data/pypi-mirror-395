"""Decorators for MCP tools."""

import inspect
import traceback
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from minitap.mcp.core.device import DeviceNotFoundError
from minitap.mcp.core.logging_config import get_logger

F = TypeVar("F", bound=Callable[..., Any])

logger = get_logger(__name__)


def handle_tool_errors[T: Callable[..., Any]](func: T) -> T:
    """
    Decorator that catches all exceptions in MCP tools and returns error messages.

    This prevents unhandled exceptions from causing infinite loops in the MCP server.
    Logs all errors with structured logging for better debugging.
    """

    @wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            logger.info(
                "tool_called",
                tool_name=func.__name__,
                args_count=len(args),
                kwargs_keys=list(kwargs.keys()),
            )
            result = await func(*args, **kwargs)
            logger.info("tool_completed", tool_name=func.__name__)
            return result
        except DeviceNotFoundError as e:
            logger.error(
                "device_not_found_error",
                tool_name=func.__name__,
                error=str(e),
                error_type=type(e).__name__,
            )
            return f"Error: {str(e)}"
        except Exception as e:
            logger.error(
                "tool_error",
                tool_name=func.__name__,
                error=str(e),
                error_type=type(e).__name__,
                traceback=traceback.format_exc(),
            )
            return f"Error in {func.__name__}: {type(e).__name__}: {str(e)}"

    @wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            logger.info(
                "tool_called",
                tool_name=func.__name__,
                args_count=len(args),
                kwargs_keys=list(kwargs.keys()),
            )
            result = func(*args, **kwargs)
            logger.info("tool_completed", tool_name=func.__name__)
            return result
        except DeviceNotFoundError as e:
            logger.error(
                "device_not_found_error",
                tool_name=func.__name__,
                error=str(e),
                error_type=type(e).__name__,
            )
            return f"Error: {str(e)}"
        except Exception as e:
            logger.error(
                "tool_error",
                tool_name=func.__name__,
                error=str(e),
                error_type=type(e).__name__,
                traceback=traceback.format_exc(),
            )
            return f"Error in {func.__name__}: {type(e).__name__}: {str(e)}"

    # Check if the function is async
    if inspect.iscoroutinefunction(func):
        return async_wrapper  # type: ignore
    else:
        return sync_wrapper  # type: ignore
