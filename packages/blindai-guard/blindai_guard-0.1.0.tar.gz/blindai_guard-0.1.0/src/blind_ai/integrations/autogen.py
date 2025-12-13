"""AutoGen integration for Blind AI.

Provides secure function wrappers for Microsoft AutoGen agents.
"""

import json
import logging
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union

from ..sdk import ThreatBlockedError, ToolGuard
from ..sdk.async_client import AsyncToolGuard

# Set up logging
logger = logging.getLogger(__name__)


def protect_autogen_function(
    guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
    block_on_threat: bool = True,
) -> Callable:
    """Decorator to protect an AutoGen function with Blind AI.

    AutoGen uses regular Python functions registered with agents.
    This decorator wraps those functions with Blind AI protection.

    Example:
        ```python
        from autogen import AssistantAgent, UserProxyAgent
        from blind_ai.integrations.autogen import protect_autogen_function

        guard = ToolGuard(base_url="http://localhost:8000")

        @protect_autogen_function(guard=guard)
        def execute_sql(query: str) -> str:
            '''Execute SQL query on the database.'''
            return db.execute(query)

        @protect_autogen_function(guard=guard)
        def send_email(to: str, subject: str, body: str) -> str:
            '''Send an email.'''
            return email_client.send(to, subject, body)

        # Register with AutoGen agent
        assistant = AssistantAgent(
            name="assistant",
            llm_config=llm_config,
        )

        user_proxy = UserProxyAgent(
            name="user_proxy",
            function_map={
                "execute_sql": execute_sql,
                "send_email": send_email,
            }
        )
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
            # Build structured input preserving parameter names
            extracted: Dict[str, Any] = {}
            for i, arg in enumerate(args):
                extracted[f"arg_{i}"] = arg if isinstance(arg, (str, int, float, bool)) else str(arg)
            for k, v in kwargs.items():
                extracted[k] = v if isinstance(v, (str, int, float, bool)) else str(v)
            tool_input = json.dumps(extracted, ensure_ascii=False) if extracted else ""

            # Check for threats
            try:
                guard.check(tool_input)
            except ThreatBlockedError as e:
                logger.warning(f"Blocked AutoGen function {func.__name__}: {e}")
                if block_on_threat:
                    raise
                return f"Error: Request blocked due to security policy - {e}"
            except Exception as e:
                # Log infrastructure errors but don't block execution
                logger.error(f"Blind AI check failed for {func.__name__}: {e}", exc_info=True)
                # Fail open - allow the call to proceed

            # If safe (or check failed), run the function
            return func(*args, **kwargs)

        # Preserve function metadata for AutoGen
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__

        return wrapper

    return decorator


def wrap_autogen_functions(
    function_map: Dict[str, Callable],
    guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
    block_on_threat: bool = True,
) -> Dict[str, Callable]:
    """Wrap all functions in an AutoGen function_map with Blind AI protection.

    Example:
        ```python
        from blind_ai.integrations.autogen import wrap_autogen_functions

        # Original function map
        function_map = {
            "execute_sql": execute_sql,
            "send_email": send_email,
            "search_web": search_web,
        }

        # Wrap all functions
        protected_map = wrap_autogen_functions(function_map, guard=ToolGuard())

        # Use with AutoGen
        user_proxy = UserProxyAgent(
            name="user_proxy",
            function_map=protected_map
        )
        ```

    Args:
        function_map: Dictionary of function names to functions
        guard: Shared Blind AI SDK client
        block_on_threat: If True, raise exception. If False, return error message.

    Returns:
        Dictionary with all functions wrapped
    """
    if guard is None:
        guard = ToolGuard()

    protected_map = {}
    for name, func in function_map.items():
        protected_map[name] = protect_autogen_function(
            guard=guard,
            block_on_threat=block_on_threat,
        )(func)

    return protected_map


class BlindAIAutoGenMonitor:
    """Monitor for AutoGen conversations to detect threats in agent messages.

    Can be used to scan agent outputs before they're processed.

    Example:
        ```python
        from blind_ai.integrations.autogen import BlindAIAutoGenMonitor

        monitor = BlindAIAutoGenMonitor(guard=ToolGuard())

        # In your conversation flow
        def process_message(sender, message):
            # Check message for threats
            if monitor.check_message(message):
                # Safe to process
                return handle_message(message)
            else:
                # Threat detected
                return "Message blocked for security reasons"
        ```
    """

    def __init__(
        self,
        guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
        log_messages: bool = True,
    ):
        """Initialize the monitor.

        Args:
            guard: Blind AI SDK client
            log_messages: Whether to log all messages
        """
        self.guard = guard or ToolGuard()
        self.log_messages = log_messages
        self.message_history: List[Dict[str, Any]] = []
        self.blocked_count = 0
        self.allowed_count = 0

    def check_message(self, message: Union[str, Dict[str, Any]]) -> bool:
        """Check a message for threats.

        Args:
            message: Message content (string or dict with 'content' key)

        Returns:
            True if safe, False if threat detected
        """
        # Extract content from message
        if isinstance(message, dict):
            content = message.get("content", "")
            if isinstance(content, list):
                # Handle multimodal messages
                content = " ".join(
                    item.get("text", "") if isinstance(item, dict) else str(item)
                    for item in content
                )
        else:
            content = str(message)

        # Log if enabled
        if self.log_messages:
            self.message_history.append({
                "content": content[:500],  # Truncate for logging
                "blocked": False,
            })

        # Check for threats
        try:
            self.guard.check(content)
            self.allowed_count += 1
            return True
        except ThreatBlockedError as e:
            logger.warning(f"Blocked AutoGen message: {e}")
            self.blocked_count += 1
            if self.log_messages and self.message_history:
                self.message_history[-1]["blocked"] = True
            return False

    def check_function_call(
        self,
        function_name: str,
        arguments: Dict[str, Any],
    ) -> bool:
        """Check a function call for threats.

        Args:
            function_name: Name of the function being called
            arguments: Function arguments

        Returns:
            True if safe, False if threat detected
        """
        # Build input string
        arg_str = " ".join(f"{k}={v}" for k, v in arguments.items())
        tool_input = f"{function_name}: {arg_str}"

        # Log if enabled
        if self.log_messages:
            self.message_history.append({
                "type": "function_call",
                "function": function_name,
                "arguments": arguments,
                "blocked": False,
            })

        # Check for threats
        try:
            self.guard.check(tool_input)
            self.allowed_count += 1
            return True
        except ThreatBlockedError as e:
            logger.warning(f"Blocked AutoGen function call {function_name}: {e}")
            self.blocked_count += 1
            if self.log_messages and self.message_history:
                self.message_history[-1]["blocked"] = True
            return False

    def get_stats(self) -> Dict[str, int]:
        """Get monitoring statistics.

        Returns:
            Dictionary with allowed and blocked counts
        """
        return {
            "allowed": self.allowed_count,
            "blocked": self.blocked_count,
            "total": self.allowed_count + self.blocked_count,
        }

    def get_message_history(self) -> List[Dict[str, Any]]:
        """Get the message history.

        Returns:
            List of message records
        """
        return self.message_history.copy()

    def clear_history(self) -> None:
        """Clear message history and reset stats."""
        self.message_history.clear()
        self.blocked_count = 0
        self.allowed_count = 0


def create_safe_autogen_agent(
    agent_class: type,
    guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
    **agent_kwargs: Any,
) -> Any:
    """Create an AutoGen agent with Blind AI protection on all functions.

    Example:
        ```python
        from autogen import UserProxyAgent
        from blind_ai.integrations.autogen import create_safe_autogen_agent

        # Create protected agent
        user_proxy = create_safe_autogen_agent(
            UserProxyAgent,
            guard=ToolGuard(),
            name="user_proxy",
            function_map={
                "execute_sql": execute_sql,
                "send_email": send_email,
            }
        )
        ```

    Args:
        agent_class: AutoGen agent class to instantiate
        guard: Blind AI SDK client
        **agent_kwargs: Arguments to pass to agent constructor

    Returns:
        AutoGen agent with protected functions
    """
    if guard is None:
        guard = ToolGuard()

    # Wrap function_map if present
    if "function_map" in agent_kwargs:
        agent_kwargs["function_map"] = wrap_autogen_functions(
            agent_kwargs["function_map"],
            guard=guard,
        )

    return agent_class(**agent_kwargs)
