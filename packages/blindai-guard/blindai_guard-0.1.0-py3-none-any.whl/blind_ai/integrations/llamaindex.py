"""LlamaIndex integration for Blind AI.

Provides secure tool wrappers for LlamaIndex applications.
"""

import asyncio
import json
import logging
from typing import Any, Callable, Dict, List, Optional, Union

from llama_index.core.tools import FunctionTool

from ..sdk import ThreatBlockedError, ToolGuard
from ..sdk.async_client import AsyncToolGuard
from .registry import auto_register_tool, infer_tool_type, infer_trust_level

# Set up logging
logger = logging.getLogger(__name__)

# Track sync guard usage in async context for performance warnings
_sync_guard_async_usage_count = 0
_SYNC_GUARD_WARNING_THRESHOLD = 10  # Warn after this many async calls with sync guard


class BlindAIToolWrapper:
    """Secure wrapper for LlamaIndex tools with Blind AI protection.

    Wraps any LlamaIndex FunctionTool to add threat detection before execution.

    Example:
        ```python
        from llama_index.core.tools import FunctionTool
        from blind_ai.integrations.llamaindex import protect_tool

        def execute_sql(query: str) -> str:
            return db.execute(query)

        # Create protected tool
        safe_tool = protect_tool(
            FunctionTool.from_defaults(fn=execute_sql),
            guard=ToolGuard(base_url="http://localhost:8000")
        )
        ```

    Attributes:
        tool: The wrapped LlamaIndex tool
        guard: Blind AI SDK client (sync or async)
    """

    def __init__(
        self,
        tool: FunctionTool,
        guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
        auto_register: bool = False,
        trust_level: Optional[str] = None,
        tool_type: Optional[str] = None,
    ):
        """Initialize protected tool wrapper.

        Args:
            tool: LlamaIndex tool to wrap
            guard: Blind AI SDK client - sync ToolGuard or async AsyncToolGuard
                  (creates default sync ToolGuard if not provided)
            auto_register: If True, automatically register tool with guard's registry
            trust_level: Override inferred trust level for registration
            tool_type: Override inferred tool type for registration
        """
        self.tool = tool
        self.guard = guard or ToolGuard()

        # Preserve tool metadata
        self.metadata = tool.metadata
        
        # Auto-register tool if requested
        if auto_register:
            self._auto_register(trust_level=trust_level, tool_type=tool_type)
    
    def _auto_register(
        self,
        trust_level: Optional[str] = None,
        tool_type: Optional[str] = None,
    ) -> bool:
        """Register this tool with the guard's tool registry."""
        # Get underlying function for better inference
        func = None
        if hasattr(self.tool, 'fn'):
            func = self.tool.fn
        elif hasattr(self.tool, '_fn'):
            func = self.tool._fn
        
        return auto_register_tool(
            guard=self.guard,
            name=self.metadata.name,
            description=self.metadata.description or "",
            func=func,
            trust_level=trust_level,
            tool_type=tool_type,
        )

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Call the tool with protection.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Tool execution result

        Raises:
            ThreatBlockedError: If threat detected
        """
        # Extract input text to check
        tool_input = self._extract_input(*args, **kwargs)

        # Check for threats
        try:
            self.guard.check(tool_input)
        except ThreatBlockedError as e:
            # Re-raise with tool context
            raise ThreatBlockedError(
                message=f"Blocked {self.metadata.name}: {str(e)}",
                threat_level=e.threat_level,
                threats=e.threats,
                response=e.response,
            ) from e
        except Exception as e:
            # Log infrastructure errors but don't block execution
            logger.error(f"Blind AI check failed for {self.metadata.name}: {e}", exc_info=True)
            # Fail open - allow the call to proceed

        # If safe (or check failed), run the wrapped tool
        return self.tool(*args, **kwargs)

    async def __acall__(self, *args: Any, **kwargs: Any) -> Any:
        """Call the tool asynchronously with protection.

        This method handles both sync and async guards:
        - AsyncToolGuard: Truly non-blocking, ideal for high-concurrency async apps
        - ToolGuard (sync): Runs in thread pool via asyncio.to_thread(), which works
          but consumes a thread per concurrent call. For high-concurrency async
          applications, consider using AsyncToolGuard instead.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Tool execution result

        Raises:
            ThreatBlockedError: If threat detected
        """
        global _sync_guard_async_usage_count
        
        # Extract input text to check
        tool_input = self._extract_input(*args, **kwargs)

        # Check for threats asynchronously
        try:
            if isinstance(self.guard, AsyncToolGuard):
                # Truly async - no blocking, no thread pool overhead
                await self.guard.check(tool_input)
            else:
                # Sync guard in async context - uses thread pool
                # This works but has overhead; warn if used frequently
                _sync_guard_async_usage_count += 1
                if _sync_guard_async_usage_count == _SYNC_GUARD_WARNING_THRESHOLD:
                    logger.warning(
                        f"Sync ToolGuard used {_SYNC_GUARD_WARNING_THRESHOLD} times in async context. "
                        "For better performance in async applications, consider using AsyncToolGuard: "
                        "from blind_ai.sdk.async_client import AsyncToolGuard"
                    )
                await asyncio.to_thread(self.guard.check, tool_input)
        except ThreatBlockedError as e:
            # Re-raise with tool context
            raise ThreatBlockedError(
                message=f"Blocked {self.metadata.name}: {str(e)}",
                threat_level=e.threat_level,
                threats=e.threats,
                response=e.response,
            ) from e
        except Exception as e:
            # Log infrastructure errors but don't block execution
            logger.error(f"Blind AI async check failed for {self.metadata.name}: {e}", exc_info=True)
            # Fail open - allow the call to proceed

        # If safe (or check failed), run the wrapped tool asynchronously
        if hasattr(self.tool, 'acall'):
            return await self.tool.acall(*args, **kwargs)
        else:
            # Fallback: run sync version in thread pool
            return await asyncio.to_thread(self.tool, *args, **kwargs)

    def _extract_input(self, *args: Any, **kwargs: Any) -> str:
        """Extract input text from arguments.

        Uses tool fn_schema to intelligently extract the right parameters,
        falling back to heuristics if schema is unavailable.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Extracted input text
        """
        # Strategy 1: Use fn_schema if available (LlamaIndex specific)
        if hasattr(self.tool, 'fn_schema') and self.tool.fn_schema:
            try:
                schema = self.tool.fn_schema
                if hasattr(schema, 'schema'):
                    properties = schema.schema().get('properties', {})
                elif hasattr(schema, 'model_json_schema'):
                    properties = schema.model_json_schema().get('properties', {})
                else:
                    properties = {}

                # Collect all string parameters from schema with their names
                extracted_params: Dict[str, Any] = {}
                for param_name, param_info in properties.items():
                    param_type = param_info.get('type')
                    if param_name in kwargs:
                        value = kwargs[param_name]
                        # Include strings and other serializable types
                        if param_type == 'string' and isinstance(value, str):
                            extracted_params[param_name] = value
                        elif param_type in ('integer', 'number', 'boolean'):
                            extracted_params[param_name] = value

                if extracted_params:
                    # Return JSON to preserve structure and parameter names
                    return json.dumps(extracted_params, ensure_ascii=False)
            except Exception as e:
                logger.debug(f"Could not extract from fn_schema: {e}")

        # Strategy 2: Check if args[0] is a dict (structured input)
        if args and isinstance(args[0], dict):
            # Preserve the dict structure as JSON
            try:
                return json.dumps(args[0], ensure_ascii=False, default=str)
            except (TypeError, ValueError):
                # Fallback to string values only
                string_values = [
                    str(v) for v in args[0].values()
                    if isinstance(v, str)
                ]
                if string_values:
                    return json.dumps({f"arg_{i}": v for i, v in enumerate(string_values)})

        # Strategy 3: First string argument
        if args:
            for arg in args:
                if isinstance(arg, str):
                    return arg

        # Strategy 4: Common parameter names in kwargs
        for key in ["input", "query", "command", "text", "prompt", "question", "message"]:
            if key in kwargs and isinstance(kwargs[key], str):
                return kwargs[key]

        # Strategy 5: All string values in kwargs with their keys
        string_kwargs = {k: v for k, v in kwargs.items() if isinstance(v, str)}
        if string_kwargs:
            return json.dumps(string_kwargs, ensure_ascii=False)

        # Fallback: convert all args to string
        if args:
            return " ".join(str(arg) for arg in args)

        return ""

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to wrapped tool.

        Args:
            name: Attribute name

        Returns:
            Attribute value
        """
        return getattr(self.tool, name)


def protect_tool(
    tool: FunctionTool,
    guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
    auto_register: bool = False,
    trust_level: Optional[str] = None,
    tool_type: Optional[str] = None,
) -> BlindAIToolWrapper:
    """Convenience function to wrap a LlamaIndex tool with Blind AI protection.

    Args:
        tool: LlamaIndex tool to protect
        guard: Blind AI SDK client (sync ToolGuard or async AsyncToolGuard)
        auto_register: If True, automatically register tool with guard's registry
        trust_level: Override inferred trust level (HIGH, MEDIUM, LOW)
        tool_type: Override inferred tool type (DATABASE, API, EMAIL, etc.)

    Returns:
        Protected tool wrapper

    Example:
        ```python
        from llama_index.core.tools import FunctionTool
        from blind_ai.integrations.llamaindex import protect_tool
        from blind_ai.sdk import ToolGuard

        def search_db(query: str) -> str:
            return db.search(query)

        tool = FunctionTool.from_defaults(fn=search_db)
        
        # Basic protection
        safe_tool = protect_tool(tool, guard=ToolGuard())

        # With auto-registration
        guard = ToolGuard(base_url="http://localhost:8000")
        safe_tool = protect_tool(
            tool,
            guard=guard,
            auto_register=True,  # Registers with inferred type and trust
        )
        ```
    """
    return BlindAIToolWrapper(
        tool=tool,
        guard=guard,
        auto_register=auto_register,
        trust_level=trust_level,
        tool_type=tool_type,
    )


def create_protected_tool(
    func: Callable,
    name: str,
    description: str,
    guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
    **kwargs,
) -> BlindAIToolWrapper:
    """Create a protected LlamaIndex tool from a function.

    Args:
        func: Function to wrap as tool
        name: Tool name
        description: Tool description
        guard: Blind AI SDK client (sync ToolGuard or async AsyncToolGuard)
        **kwargs: Additional FunctionTool arguments

    Returns:
        Protected tool

    Example:
        ```python
        from blind_ai.integrations.llamaindex import create_protected_tool
        from blind_ai.sdk.async_client import AsyncToolGuard

        def execute_sql(query: str) -> str:
            '''Execute a SQL query'''
            return db.execute(query)

        # Sync protection
        safe_sql_tool = create_protected_tool(
            func=execute_sql,
            name="sql_executor",
            description="Execute SQL queries safely"
        )

        # Async protection (truly non-blocking)
        async_guard = AsyncToolGuard()
        safe_async_sql = create_protected_tool(
            func=execute_sql,
            name="sql_executor",
            description="Execute SQL queries safely",
            guard=async_guard
        )
        ```
    """
    # Create FunctionTool
    base_tool = FunctionTool.from_defaults(
        fn=func,
        name=name,
        description=description,
        **kwargs,
    )

    # Wrap with protection
    return BlindAIToolWrapper(tool=base_tool, guard=guard)


class BlindAIObserver:
    """Non-blocking threat monitoring for LlamaIndex applications.

    Monitors tool calls and LLM interactions, logging detected threats
    without blocking execution. Useful for observability and analytics.

    Example:
        ```python
        from llama_index.core.agent import ReActAgent
        from blind_ai.integrations.llamaindex import BlindAIObserver

        # Create observer
        observer = BlindAIObserver(
            guard=ToolGuard(base_url="http://localhost:8000")
        )

        # Wrap tools for monitoring
        monitored_tools = observer.wrap_tools(tools)

        # Use in agent
        agent = ReActAgent.from_tools(monitored_tools, llm=llm)
        ```

    Attributes:
        guard: Blind AI SDK client
        threats_detected: List of detected threats
        block_on_threat: Whether to raise exception on threat
    """

    def __init__(
        self,
        guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
        block_on_threat: bool = False,
    ):
        """Initialize observer.

        Args:
            guard: Blind AI SDK client (sync ToolGuard or async AsyncToolGuard)
            block_on_threat: Whether to block execution on threat
        """
        self.guard = guard or ToolGuard()
        self.block_on_threat = block_on_threat
        self.threats_detected: List[Dict[str, Any]] = []

    def wrap_tools(
        self,
        tools: List[FunctionTool],
    ) -> List[BlindAIToolWrapper]:
        """Wrap multiple tools with monitoring.

        Args:
            tools: List of LlamaIndex tools to wrap

        Returns:
            List of wrapped tools

        Example:
            ```python
            observer = BlindAIObserver()
            safe_tools = observer.wrap_tools([tool1, tool2, tool3])
            ```
        """
        return [self._wrap_tool_with_monitoring(tool) for tool in tools]

    def _wrap_tool_with_monitoring(self, tool: FunctionTool) -> BlindAIToolWrapper:
        """Wrap a single tool with monitoring callback.

        Args:
            tool: Tool to wrap

        Returns:
            Wrapped tool
        """
        # Create wrapper that logs instead of blocks
        class MonitoringWrapper(BlindAIToolWrapper):
            def __init__(inner_self, tool, guard, observer):
                super().__init__(tool, guard)
                inner_self.observer = observer

            def __call__(inner_self, *args, **kwargs):
                tool_input = inner_self._extract_input(*args, **kwargs)

                try:
                    result = inner_self.guard.check(tool_input)

                    # Log if threat detected
                    if result.is_threat:
                        threat_info = {
                            "source": "tool",
                            "tool": inner_self.metadata.name,
                            "input": tool_input[:200],
                            "threat_level": result.threat_level,
                            "threats": result.threats_detected,
                            "action": result.final_action,
                        }
                        inner_self.observer.threats_detected.append(threat_info)

                        logger.warning(
                            f"Threat detected in tool {inner_self.metadata.name}: "
                            f"{result.threat_level} - {result.final_action}"
                        )

                        # Optionally block
                        if inner_self.observer.block_on_threat and result.final_action == "block":
                            raise ThreatBlockedError(
                                message=f"Blocked threat in {inner_self.metadata.name}",
                                threat_level=result.threat_level,
                                threats=result.threats_detected,
                                response={},
                            )

                except ThreatBlockedError:
                    raise
                except Exception as e:
                    logger.error(f"Blind AI check failed: {e}", exc_info=True)

                # Execute tool
                return inner_self.tool(*args, **kwargs)

            async def __acall__(inner_self, *args, **kwargs):
                tool_input = inner_self._extract_input(*args, **kwargs)

                try:
                    # Use truly async check if AsyncToolGuard, otherwise use thread pool
                    if isinstance(inner_self.guard, AsyncToolGuard):
                        # Truly async - no blocking!
                        result = await inner_self.guard.check(tool_input)
                    else:
                        # Sync guard - run in thread pool
                        result = await asyncio.to_thread(inner_self.guard.check, tool_input)

                    # Log if threat detected
                    if result.is_threat:
                        threat_info = {
                            "source": "tool",
                            "tool": inner_self.metadata.name,
                            "input": tool_input[:200],
                            "threat_level": result.threat_level,
                            "threats": result.threats_detected,
                            "action": result.final_action,
                        }
                        inner_self.observer.threats_detected.append(threat_info)

                        logger.warning(
                            f"Threat detected in tool {inner_self.metadata.name}: "
                            f"{result.threat_level} - {result.final_action}"
                        )

                        # Optionally block
                        if inner_self.observer.block_on_threat and result.final_action == "block":
                            raise ThreatBlockedError(
                                message=f"Blocked threat in {inner_self.metadata.name}",
                                threat_level=result.threat_level,
                                threats=result.threats_detected,
                                response={},
                            )

                except ThreatBlockedError:
                    raise
                except Exception as e:
                    logger.error(f"Blind AI check failed: {e}", exc_info=True)

                # Execute tool asynchronously
                if hasattr(inner_self.tool, 'acall'):
                    return await inner_self.tool.acall(*args, **kwargs)
                else:
                    return await asyncio.to_thread(inner_self.tool, *args, **kwargs)

        return MonitoringWrapper(tool, self.guard, self)

    def get_threat_summary(self) -> Dict[str, Any]:
        """Get summary of detected threats.

        Returns:
            Dictionary with threat statistics

        Example:
            ```python
            observer = BlindAIObserver()
            # ... after running agent ...
            summary = observer.get_threat_summary()
            print(f"Total threats: {summary['total_threats']}")
            print(f"Critical: {summary['threat_levels']['critical']}")
            ```
        """
        return {
            "total_threats": len(self.threats_detected),
            "threats": self.threats_detected,
            "threat_levels": {
                "critical": sum(
                    1 for t in self.threats_detected if t["threat_level"] == "critical"
                ),
                "high": sum(
                    1 for t in self.threats_detected if t["threat_level"] == "high"
                ),
                "medium": sum(
                    1 for t in self.threats_detected if t["threat_level"] == "medium"
                ),
                "low": sum(
                    1 for t in self.threats_detected if t["threat_level"] == "low"
                ),
            },
            "by_tool": {},  # Could add per-tool statistics
        }
