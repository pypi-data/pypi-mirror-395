"""CrewAI integration for Blind AI.

Provides secure tool wrappers for CrewAI agents and crews.
"""

import json
import logging
from functools import wraps
from typing import Any, Callable, Dict, Optional, Union

from crewai.tools import BaseTool as CrewAIBaseTool
from crewai.tools import tool as crewai_tool
from pydantic import Field

from ..sdk import ThreatBlockedError, ToolGuard
from ..sdk.async_client import AsyncToolGuard

# Set up logging
logger = logging.getLogger(__name__)


class BlindAICrewTool(CrewAIBaseTool):
    """Secure wrapper for CrewAI tools with Blind AI protection.

    Wraps any CrewAI tool to add threat detection before execution.

    Example:
        ```python
        from crewai.tools import BaseTool
        from blind_ai.integrations.crewai import BlindAICrewTool

        class DatabaseQueryTool(BaseTool):
            name = "database_query"
            description = "Query the database"

            def _run(self, query: str) -> str:
                return db.execute(query)

        # Wrap with Blind AI protection
        safe_db_tool = BlindAICrewTool(
            tool=DatabaseQueryTool(),
            guard=ToolGuard(base_url="http://localhost:8000")
        )

        # Use in CrewAI agent
        agent = Agent(
            role="Data Analyst",
            tools=[safe_db_tool]
        )
        ```

    Attributes:
        wrapped_tool: The wrapped CrewAI tool
        guard: Blind AI SDK client
    """

    name: str = "blind_ai_protected_tool"
    description: str = "A tool protected by Blind AI"
    wrapped_tool: Any = Field(default=None, exclude=True)
    guard: Any = Field(default=None, exclude=True)

    def __init__(
        self,
        tool: CrewAIBaseTool,
        guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
        **kwargs: Any,
    ):
        """Initialize protected CrewAI tool wrapper.

        Args:
            tool: CrewAI tool to wrap
            guard: Blind AI SDK client (creates default if not provided)
            **kwargs: Additional arguments
        """
        if guard is None:
            guard = ToolGuard()

        super().__init__(
            name=tool.name,
            description=tool.description,
            **kwargs,
        )
        self.wrapped_tool = tool
        self.guard = guard

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the tool with Blind AI protection.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Tool execution result

        Raises:
            ThreatBlockedError: If threat detected
        """
        # Extract input to check
        tool_input = self._extract_input(*args, **kwargs)

        # Check for threats
        try:
            self.guard.check(tool_input)
        except ThreatBlockedError as e:
            logger.warning(f"Blocked {self.name}: {e}")
            raise ThreatBlockedError(
                message=f"Blocked {self.name}: {str(e)}",
                threat_level=e.threat_level,
                threats=e.threats,
                response=e.response,
            ) from e
        except Exception as e:
            # Log infrastructure errors but don't block execution
            logger.error(f"Blind AI check failed for {self.name}: {e}", exc_info=True)
            # Fail open - allow the call to proceed

        # If safe (or check failed), run the wrapped tool
        return self.wrapped_tool._run(*args, **kwargs)

    def _extract_input(self, *args: Any, **kwargs: Any) -> str:
        """Extract input text from arguments, preserving structure.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            JSON string preserving parameter names and values
        """
        extracted: Dict[str, Any] = {}

        # Add positional args with indexed keys
        for i, arg in enumerate(args):
            if isinstance(arg, (str, int, float, bool)):
                extracted[f"arg_{i}"] = arg
            elif isinstance(arg, dict):
                # Merge dict args
                extracted.update(arg)
            else:
                extracted[f"arg_{i}"] = str(arg)

        # Add keyword args (these take precedence)
        for key, value in kwargs.items():
            if isinstance(value, (str, int, float, bool)):
                extracted[key] = value
            else:
                extracted[key] = str(value)

        if extracted:
            return json.dumps(extracted, ensure_ascii=False)
        return ""


def protect_crew_tool(
    guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
    block_on_threat: bool = True,
) -> Callable:
    """Decorator to protect a CrewAI @tool function with Blind AI.

    Example:
        ```python
        from crewai.tools import tool
        from blind_ai.integrations.crewai import protect_crew_tool

        guard = ToolGuard(base_url="http://localhost:8000")

        @tool
        @protect_crew_tool(guard=guard)
        def search_database(query: str) -> str:
            '''Search the database for information.'''
            return db.search(query)
        ```

    Args:
        guard: Blind AI SDK client (creates default if not provided)
        block_on_threat: If True, raise exception on threat. If False, return error message.

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
                logger.warning(f"Blocked {func.__name__}: {e}")
                if block_on_threat:
                    raise
                return f"Error: Request blocked due to security policy - {e}"
            except Exception as e:
                # Log infrastructure errors but don't block execution
                logger.error(f"Blind AI check failed for {func.__name__}: {e}", exc_info=True)
                # Fail open - allow the call to proceed

            # If safe (or check failed), run the function
            return func(*args, **kwargs)

        return wrapper

    return decorator


def wrap_crew_tools(
    tools: list[CrewAIBaseTool],
    guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
) -> list[BlindAICrewTool]:
    """Wrap multiple CrewAI tools with Blind AI protection.

    Example:
        ```python
        from blind_ai.integrations.crewai import wrap_crew_tools

        tools = [SearchTool(), DatabaseTool(), EmailTool()]
        protected_tools = wrap_crew_tools(tools, guard=ToolGuard())

        agent = Agent(role="Assistant", tools=protected_tools)
        ```

    Args:
        tools: List of CrewAI tools to wrap
        guard: Shared Blind AI SDK client

    Returns:
        List of protected tools
    """
    if guard is None:
        guard = ToolGuard()

    return [BlindAICrewTool(tool=tool, guard=guard) for tool in tools]


class BlindAICrewCallback:
    """Callback handler for CrewAI to monitor all agent actions.

    Provides visibility into agent behavior and can block suspicious patterns.

    Example:
        ```python
        from crewai import Crew
        from blind_ai.integrations.crewai import BlindAICrewCallback

        callback = BlindAICrewCallback(guard=ToolGuard())

        crew = Crew(
            agents=[agent1, agent2],
            tasks=[task1, task2],
            callbacks=[callback]
        )
        ```
    """

    def __init__(
        self,
        guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
        log_all_actions: bool = True,
    ):
        """Initialize callback handler.

        Args:
            guard: Blind AI SDK client
            log_all_actions: Whether to log all agent actions
        """
        self.guard = guard or ToolGuard()
        self.log_all_actions = log_all_actions
        self.action_history: list[dict[str, Any]] = []

    def on_tool_start(self, tool_name: str, tool_input: str) -> None:
        """Called when a tool is about to be executed.

        Args:
            tool_name: Name of the tool
            tool_input: Input to the tool
        """
        if self.log_all_actions:
            self.action_history.append({
                "type": "tool_start",
                "tool": tool_name,
                "input": tool_input,
            })

        # Check for threats
        try:
            self.guard.check(tool_input)
        except ThreatBlockedError as e:
            logger.warning(f"CrewAI callback blocked {tool_name}: {e}")
            raise

    def on_tool_end(self, tool_name: str, tool_output: str) -> None:
        """Called when a tool finishes execution.

        Args:
            tool_name: Name of the tool
            tool_output: Output from the tool
        """
        if self.log_all_actions:
            self.action_history.append({
                "type": "tool_end",
                "tool": tool_name,
                "output": tool_output[:500],  # Truncate for logging
            })

    def get_action_history(self) -> list[dict[str, Any]]:
        """Get the history of all agent actions.

        Returns:
            List of action records
        """
        return self.action_history.copy()

    def clear_history(self) -> None:
        """Clear the action history."""
        self.action_history.clear()
