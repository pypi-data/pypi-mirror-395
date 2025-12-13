"""Semantic Kernel integration for Blind AI.

Provides secure plugin and function wrappers for Microsoft Semantic Kernel.
"""

import json
import logging
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union

from ..sdk import ThreatBlockedError, ToolGuard
from ..sdk.async_client import AsyncToolGuard

# Set up logging
logger = logging.getLogger(__name__)

# Track sync guard usage in async context for performance warnings
_sync_guard_async_usage_count = 0
_SYNC_GUARD_WARNING_THRESHOLD = 10  # Warn after this many async calls with sync guard


def protect_kernel_function(
    guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
    block_on_threat: bool = True,
) -> Callable:
    """Decorator to protect a Semantic Kernel function with Blind AI.

    Works with both @kernel_function decorated functions and regular functions
    used as native functions in Semantic Kernel.

    Example:
        ```python
        from semantic_kernel.functions import kernel_function
        from blind_ai.integrations.semantic_kernel import protect_kernel_function

        guard = ToolGuard(base_url="http://localhost:8000")

        class DatabasePlugin:
            @kernel_function(
                name="query_database",
                description="Execute a database query"
            )
            @protect_kernel_function(guard=guard)
            def query_database(self, query: str) -> str:
                return db.execute(query)

            @kernel_function(
                name="send_email",
                description="Send an email"
            )
            @protect_kernel_function(guard=guard)
            def send_email(self, to: str, subject: str, body: str) -> str:
                return email_client.send(to, subject, body)

        # Register plugin with kernel
        kernel.add_plugin(DatabasePlugin(), plugin_name="database")
        ```

    Args:
        guard: Blind AI SDK client (creates default if not provided)
        block_on_threat: If True, raise exception. If False, return error message.

    Returns:
        Decorated function
    """
    if guard is None:
        guard = ToolGuard()

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Skip 'self' if present (for class methods)
            func_args = args[1:] if args and hasattr(args[0], '__class__') else args

            # Build structured input preserving parameter names
            extracted: Dict[str, Any] = {}
            for i, arg in enumerate(func_args):
                extracted[f"arg_{i}"] = arg if isinstance(arg, (str, int, float, bool)) else str(arg)
            for k, v in kwargs.items():
                extracted[k] = v if isinstance(v, (str, int, float, bool)) else str(v)
            tool_input = json.dumps(extracted, ensure_ascii=False) if extracted else ""

            # Check for threats
            try:
                guard.check(tool_input)
            except ThreatBlockedError as e:
                logger.warning(f"Blocked Semantic Kernel function {func.__name__}: {e}")
                if block_on_threat:
                    raise
                return f"Error: Request blocked due to security policy - {e}"
            except Exception as e:
                # Log infrastructure errors but don't block execution
                logger.error(f"Blind AI check failed for {func.__name__}: {e}", exc_info=True)
                # Fail open - allow the call to proceed

            # If safe (or check failed), run the function
            return func(*args, **kwargs)

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            # Skip 'self' if present
            func_args = args[1:] if args and hasattr(args[0], '__class__') else args

            # Build structured input preserving parameter names
            extracted: Dict[str, Any] = {}
            for i, arg in enumerate(func_args):
                extracted[f"arg_{i}"] = arg if isinstance(arg, (str, int, float, bool)) else str(arg)
            for k, v in kwargs.items():
                extracted[k] = v if isinstance(v, (str, int, float, bool)) else str(v)
            tool_input = json.dumps(extracted, ensure_ascii=False) if extracted else ""

            # Check for threats
            global _sync_guard_async_usage_count
            try:
                if isinstance(guard, AsyncToolGuard):
                    # Truly async - no blocking, no thread pool overhead
                    await guard.check(tool_input)
                else:
                    # Sync guard in async context - warn if used frequently
                    _sync_guard_async_usage_count += 1
                    if _sync_guard_async_usage_count == _SYNC_GUARD_WARNING_THRESHOLD:
                        logger.warning(
                            f"Sync ToolGuard used {_SYNC_GUARD_WARNING_THRESHOLD} times in async context. "
                            "For better performance in async applications, consider using AsyncToolGuard: "
                            "from blind_ai.sdk.async_client import AsyncToolGuard"
                        )
                    # Run sync guard in thread pool to avoid blocking
                    import asyncio as aio
                    await aio.to_thread(guard.check, tool_input)
            except ThreatBlockedError as e:
                logger.warning(f"Blocked Semantic Kernel function {func.__name__}: {e}")
                if block_on_threat:
                    raise
                return f"Error: Request blocked due to security policy - {e}"
            except Exception as e:
                # Log infrastructure errors but don't block execution
                logger.error(f"Blind AI async check failed for {func.__name__}: {e}", exc_info=True)
                # Fail open - allow the call to proceed

            # If safe (or check failed), run the function
            import asyncio
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)

        # Return async wrapper if function is async
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return wrapper

    return decorator


class BlindAIKernelFilter:
    """Filter for Semantic Kernel to intercept and check all function calls.

    Can be registered with a Kernel to automatically protect all function invocations.

    Example:
        ```python
        from semantic_kernel import Kernel
        from blind_ai.integrations.semantic_kernel import BlindAIKernelFilter

        kernel = Kernel()
        blind_ai_filter = BlindAIKernelFilter(guard=ToolGuard())

        # Register as a function invocation filter
        kernel.add_filter("function_invocation", blind_ai_filter)
        ```
    """

    def __init__(
        self,
        guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
        block_on_threat: bool = True,
        log_invocations: bool = True,
    ):
        """Initialize the filter.

        Args:
            guard: Blind AI SDK client
            block_on_threat: If True, raise exception on threat
            log_invocations: Whether to log all function invocations
        """
        self.guard = guard or ToolGuard()
        self.block_on_threat = block_on_threat
        self.log_invocations = log_invocations
        self.invocation_history: List[Dict[str, Any]] = []
        self.blocked_count = 0
        self.allowed_count = 0

    async def on_function_invocation(
        self,
        context: Any,
        next_handler: Callable,
    ) -> Any:
        """Filter handler called before each function invocation.

        Args:
            context: Function invocation context
            next_handler: Next handler in the filter chain

        Returns:
            Function result or error
        """
        # Extract function info from context
        function_name = getattr(context, 'function_name', 'unknown')
        arguments = getattr(context, 'arguments', {})

        # Build input string
        arg_str = " ".join(f"{k}={v}" for k, v in arguments.items())
        tool_input = f"{function_name}: {arg_str}"

        # Log if enabled
        if self.log_invocations:
            self.invocation_history.append({
                "function": function_name,
                "arguments": dict(arguments) if arguments else {},
                "blocked": False,
            })

        # Check for threats
        try:
            if isinstance(self.guard, AsyncToolGuard):
                await self.guard.check(tool_input)
            else:
                self.guard.check(tool_input)
            self.allowed_count += 1
        except ThreatBlockedError as e:
            logger.warning(f"Blocked Semantic Kernel function {function_name}: {e}")
            self.blocked_count += 1
            if self.log_invocations and self.invocation_history:
                self.invocation_history[-1]["blocked"] = True

            if self.block_on_threat:
                raise
            # Return error result
            context.result = f"Error: Request blocked due to security policy - {e}"
            return context

        # Continue to next handler (execute the function)
        return await next_handler(context)

    def get_stats(self) -> Dict[str, int]:
        """Get filter statistics.

        Returns:
            Dictionary with allowed and blocked counts
        """
        return {
            "allowed": self.allowed_count,
            "blocked": self.blocked_count,
            "total": self.allowed_count + self.blocked_count,
        }

    def get_invocation_history(self) -> List[Dict[str, Any]]:
        """Get the invocation history.

        Returns:
            List of invocation records
        """
        return self.invocation_history.copy()

    def clear_history(self) -> None:
        """Clear invocation history and reset stats."""
        self.invocation_history.clear()
        self.blocked_count = 0
        self.allowed_count = 0


def create_protected_plugin(
    plugin_class: type,
    guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
    **init_kwargs: Any,
) -> Any:
    """Create a Semantic Kernel plugin with all functions protected.

    This wraps all @kernel_function decorated methods with Blind AI protection.

    Example:
        ```python
        from blind_ai.integrations.semantic_kernel import create_protected_plugin

        class EmailPlugin:
            @kernel_function(name="send_email", description="Send email")
            def send_email(self, to: str, body: str) -> str:
                return email_client.send(to, body)

            @kernel_function(name="read_inbox", description="Read inbox")
            def read_inbox(self) -> str:
                return email_client.get_inbox()

        # Create protected instance
        protected_email = create_protected_plugin(
            EmailPlugin,
            guard=ToolGuard()
        )

        kernel.add_plugin(protected_email, plugin_name="email")
        ```

    Args:
        plugin_class: Plugin class to instantiate
        guard: Blind AI SDK client
        **init_kwargs: Arguments to pass to plugin constructor

    Returns:
        Plugin instance with protected functions
    """
    if guard is None:
        guard = ToolGuard()

    # Create instance
    instance = plugin_class(**init_kwargs)

    # Find and wrap all kernel functions
    for attr_name in dir(instance):
        if attr_name.startswith('_'):
            continue

        attr = getattr(instance, attr_name)
        if callable(attr) and hasattr(attr, '__kernel_function__'):
            # Wrap the method
            protected = protect_kernel_function(guard=guard)(attr)
            setattr(instance, attr_name, protected)

    return instance


def wrap_kernel_functions(
    functions: Dict[str, Callable],
    guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
) -> Dict[str, Callable]:
    """Wrap multiple functions for use with Semantic Kernel.

    Example:
        ```python
        from blind_ai.integrations.semantic_kernel import wrap_kernel_functions

        functions = {
            "search": search_function,
            "calculate": calculate_function,
        }

        protected = wrap_kernel_functions(functions, guard=ToolGuard())
        ```

    Args:
        functions: Dictionary of function names to functions
        guard: Shared Blind AI SDK client

    Returns:
        Dictionary with all functions wrapped
    """
    if guard is None:
        guard = ToolGuard()

    return {
        name: protect_kernel_function(guard=guard)(func)
        for name, func in functions.items()
    }
