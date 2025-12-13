"""LangChain integration for Blind AI.

Provides secure tool wrappers and callbacks for LangChain applications.
"""

import asyncio
import json
import logging
from typing import Any, Callable, Dict, List, Optional, Union

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.tools import BaseTool, StructuredTool

from ..sdk import ThreatBlockedError, ToolGuard
from ..sdk.async_client import AsyncToolGuard
from .registry import auto_register_tool, infer_tool_type, infer_trust_level
from .utils import (
    MAX_INPUT_SIZE,
    extract_tool_input,
    safe_json_serialize,
    truncate_input,
)

# Set up logging
logger = logging.getLogger(__name__)

# Track sync guard usage in async context for performance warnings
_sync_guard_async_usage_count = 0
_SYNC_GUARD_WARNING_THRESHOLD = 10  # Warn after this many async calls with sync guard


class BlindAIToolWrapper(BaseTool):
    """Secure wrapper for LangChain tools with Blind AI protection.

    Wraps any LangChain tool to add threat detection before execution.

    Example:
        ```python
        from langchain.tools import ShellTool
        from blind_ai.integrations.langchain import BlindAIToolWrapper

        # Wrap a dangerous tool
        shell_tool = ShellTool()
        safe_shell = BlindAIToolWrapper(
            tool=shell_tool,
            guard=ToolGuard(base_url="http://localhost:8000")
        )

        # This will be blocked
        try:
            safe_shell.run("rm -rf /")
        except ThreatBlockedError:
            print("Blocked malicious command!")
        ```

    Attributes:
        tool: The wrapped LangChain tool
        guard: Blind AI SDK client
        name: Tool name
        description: Tool description
    """

    tool: BaseTool
    guard: Union[ToolGuard, AsyncToolGuard]
    name: str = ""
    description: str = ""

    def __init__(
        self,
        tool: BaseTool,
        guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
        auto_register: bool = False,
        trust_level: Optional[str] = None,
        tool_type: Optional[str] = None,
        **kwargs,
    ):
        """Initialize protected tool wrapper.

        Args:
            tool: LangChain tool to wrap
            guard: Blind AI SDK client - sync ToolGuard or async AsyncToolGuard
                  (creates default sync ToolGuard if not provided)
            auto_register: If True, automatically register tool with guard's registry
            trust_level: Override inferred trust level for registration
            tool_type: Override inferred tool type for registration
            **kwargs: Additional arguments
        """
        # Initialize guard if not provided
        if guard is None:
            guard = ToolGuard()

        # Set name and description from wrapped tool
        name = kwargs.pop("name", tool.name)
        description = kwargs.pop("description", tool.description)

        super().__init__(
            tool=tool,
            guard=guard,
            name=name,
            description=description,
            **kwargs,
        )
        
        # Auto-register tool if requested
        if auto_register:
            self._auto_register(trust_level=trust_level, tool_type=tool_type)
    
    def _auto_register(
        self,
        trust_level: Optional[str] = None,
        tool_type: Optional[str] = None,
    ) -> bool:
        """Register this tool with the guard's tool registry.
        
        Args:
            trust_level: Override inferred trust level
            tool_type: Override inferred tool type
            
        Returns:
            True if registration succeeded
        """
        # Get underlying function for better inference
        func = None
        if hasattr(self.tool, 'func'):
            func = self.tool.func
        elif hasattr(self.tool, '_run'):
            func = self.tool._run
        
        return auto_register_tool(
            guard=self.guard,
            name=self.name,
            description=self.description,
            func=func,
            trust_level=trust_level,
            tool_type=tool_type,
        )

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the tool with protection.

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
        return self.tool._run(*args, **kwargs)

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        """Run the tool asynchronously with protection.

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
                message=f"Blocked {self.name}: {str(e)}",
                threat_level=e.threat_level,
                threats=e.threats,
                response=e.response,
            ) from e
        except Exception as e:
            # Log infrastructure errors but don't block execution
            logger.error(f"Blind AI async check failed for {self.name}: {e}", exc_info=True)
            # Fail open - allow the call to proceed

        # If safe (or check failed), run the wrapped tool
        return await self.tool._arun(*args, **kwargs)

    def _extract_input(self, *args: Any, **kwargs: Any) -> str:
        """Extract input text from arguments with size limits.

        Uses tool schema to intelligently extract the right parameters,
        falling back to heuristics if schema is unavailable.
        Applies size limits to prevent oversized inputs.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Extracted input text (truncated if exceeds MAX_INPUT_SIZE)
        """
        result = ""
        
        # Strategy 1: Use tool schema if available
        if hasattr(self.tool, 'args_schema') and self.tool.args_schema:
            try:
                schema = self.tool.args_schema
                # Try model_json_schema first (Pydantic v2), fall back to schema() (v1)
                if hasattr(schema, 'model_json_schema'):
                    properties = schema.model_json_schema().get('properties', {})
                elif hasattr(schema, 'schema'):
                    properties = schema.schema().get('properties', {})
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
                    result = safe_json_serialize(extracted_params, MAX_INPUT_SIZE)
                    return result
            except Exception as e:
                logger.debug(f"Could not extract from schema: {e}")

        # Strategy 2: Check if args[0] is a dict (structured tool input)
        if args and isinstance(args[0], dict):
            result = safe_json_serialize(args[0], MAX_INPUT_SIZE)
            return result

        # Strategy 3: First string argument
        if args:
            for arg in args:
                if isinstance(arg, str):
                    result, _ = truncate_input(arg, MAX_INPUT_SIZE)
                    return result

        # Strategy 4: Common parameter names in kwargs
        for key in ["input", "query", "command", "text", "prompt", "question", "message"]:
            if key in kwargs and isinstance(kwargs[key], str):
                result, _ = truncate_input(kwargs[key], MAX_INPUT_SIZE)
                return result

        # Strategy 5: All string values in kwargs with their keys
        string_kwargs = {k: v for k, v in kwargs.items() if isinstance(v, str)}
        if string_kwargs:
            result = safe_json_serialize(string_kwargs, MAX_INPUT_SIZE)
            return result

        # Fallback: use generic extraction with size limits
        return extract_tool_input(args, kwargs, max_size=MAX_INPUT_SIZE)


class BlindAICallbackHandler(BaseCallbackHandler):
    """LangChain callback handler for monitoring and logging threats.

    Monitors tool calls and LLM prompts, logs detected threats without blocking execution.
    Useful for observability and analytics.

    Example:
        ```python
        from langchain.agents import initialize_agent
        from blind_ai.integrations.langchain import BlindAICallbackHandler

        # Add callback to agent
        callback = BlindAICallbackHandler(
            guard=ToolGuard(base_url="http://localhost:8000")
        )

        agent = initialize_agent(
            tools=[...],
            llm=llm,
            callbacks=[callback]
        )
        ```

    Attributes:
        guard: Blind AI SDK client
        threats_detected: List of detected threats
        block_on_threat: Whether to raise exception on threat
        context_map: Maps run_ids to context for multi-turn tracking
    """

    def __init__(
        self,
        guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
        block_on_threat: bool = False,
        track_llm_prompts: bool = True,
    ):
        """Initialize callback handler.

        Args:
            guard: Blind AI SDK client (sync ToolGuard or async AsyncToolGuard)
            block_on_threat: Whether to block execution on threat
            track_llm_prompts: Whether to check LLM prompts for threats
        """
        super().__init__()
        self.guard = guard or ToolGuard()
        self.block_on_threat = block_on_threat
        self.track_llm_prompts = track_llm_prompts
        self.threats_detected: List[Dict[str, Any]] = []
        self.context_map: Dict[str, str] = {}  # Maps run_id to context_id

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs: Any,
    ) -> None:
        """Check tool input for threats before execution.

        Args:
            serialized: Serialized tool
            input_str: Tool input string
            **kwargs: Additional arguments (may include run_id)
        """
        run_id = kwargs.get("run_id")
        context_id = self.context_map.get(str(run_id)) if run_id else None

        try:
            result = self.guard.check(input_str, context_id=context_id)

            # Log if threat detected
            if result.is_threat:
                threat_info = {
                    "source": "tool",
                    "tool": serialized.get("name", "unknown"),
                    "input": input_str,
                    "threat_level": result.threat_level,
                    "threats": result.threats_detected,
                    "action": result.final_action,
                    "run_id": str(run_id) if run_id else None,
                }
                self.threats_detected.append(threat_info)

                logger.warning(
                    f"Threat detected in tool {serialized.get('name', 'unknown')}: "
                    f"{result.threat_level} - {result.final_action}"
                )

                # Optionally block
                if self.block_on_threat and result.final_action == "block":
                    raise ThreatBlockedError(
                        message=f"Blocked threat in {serialized.get('name', 'tool')}",
                        threat_level=result.threat_level,
                        threats=result.threats_detected,
                        response={},
                    )

        except ThreatBlockedError:
            # Re-raise blocking errors
            raise
        except Exception as e:
            # Log other errors but don't block
            logger.error(f"Blind AI check failed: {e}", exc_info=True)

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        **kwargs: Any,
    ) -> None:
        """Check LLM prompts for threats before execution.

        Args:
            serialized: Serialized LLM
            prompts: List of prompts
            **kwargs: Additional arguments (may include run_id)
        """
        if not self.track_llm_prompts:
            return

        run_id = kwargs.get("run_id")
        context_id = self.context_map.get(str(run_id)) if run_id else None

        for idx, prompt in enumerate(prompts):
            try:
                result = self.guard.check(prompt, context_id=context_id)

                # Log if threat detected
                if result.is_threat:
                    threat_info = {
                        "source": "llm_prompt",
                        "llm": serialized.get("name", "unknown"),
                        "prompt_index": idx,
                        "prompt": prompt[:200],  # Truncate for logging
                        "threat_level": result.threat_level,
                        "threats": result.threats_detected,
                        "action": result.final_action,
                        "run_id": str(run_id) if run_id else None,
                    }
                    self.threats_detected.append(threat_info)

                    logger.warning(
                        f"Threat detected in LLM prompt: "
                        f"{result.threat_level} - {result.final_action}"
                    )

                    # Optionally block
                    if self.block_on_threat and result.final_action == "block":
                        raise ThreatBlockedError(
                            message=f"Blocked threat in LLM prompt",
                            threat_level=result.threat_level,
                            threats=result.threats_detected,
                            response={},
                        )

            except ThreatBlockedError:
                # Re-raise blocking errors
                raise
            except Exception as e:
                # Log other errors but don't block
                logger.error(f"Blind AI check failed on LLM prompt: {e}", exc_info=True)

    def on_tool_end(
        self,
        output: str,
        **kwargs: Any,
    ) -> None:
        """Check tool output for threats after execution.

        Args:
            output: Tool output
            **kwargs: Additional arguments (may include run_id)
        """
        run_id = kwargs.get("run_id")
        context_id = self.context_map.get(str(run_id)) if run_id else None

        try:
            result = self.guard.check(output, context_id=context_id)

            # Log if threat detected in output
            if result.is_threat:
                threat_info = {
                    "source": "tool_output",
                    "output": output[:200],  # Truncate for logging
                    "threat_level": result.threat_level,
                    "threats": result.threats_detected,
                    "action": result.final_action,
                    "run_id": str(run_id) if run_id else None,
                }
                self.threats_detected.append(threat_info)

                logger.warning(
                    f"Threat detected in tool output: "
                    f"{result.threat_level} - {result.final_action}"
                )

                # Note: We don't block on output since the tool already ran
                # But we log for monitoring and can alert

        except Exception as e:
            # Log errors but don't block
            logger.error(f"Blind AI check failed on tool output: {e}", exc_info=True)

    def set_context(self, run_id: str, context_id: str) -> None:
        """Set context ID for a specific run.

        Enables multi-turn tracking by associating a run_id with a context_id.

        Args:
            run_id: LangChain run ID
            context_id: Blind AI context ID for session tracking

        Example:
            ```python
            callback = BlindAICallbackHandler()
            callback.set_context(run_id="abc-123", context_id="session-456")
            ```
        """
        self.context_map[run_id] = context_id

    def clear_context(self, run_id: str) -> None:
        """Clear context for a specific run.

        Args:
            run_id: LangChain run ID to clear
        """
        self.context_map.pop(run_id, None)

    def get_threat_summary(self) -> Dict[str, Any]:
        """Get summary of detected threats.

        Returns:
            Dictionary with threat statistics

        Example:
            ```python
            callback = BlindAICallbackHandler()
            # ... after running agent ...
            summary = callback.get_threat_summary()
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
            "by_source": {
                "tool": sum(1 for t in self.threats_detected if t.get("source") == "tool"),
                "llm_prompt": sum(1 for t in self.threats_detected if t.get("source") == "llm_prompt"),
                "tool_output": sum(1 for t in self.threats_detected if t.get("source") == "tool_output"),
            },
        }


def protect_tool(
    tool: BaseTool,
    guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
    auto_register: bool = False,
    trust_level: Optional[str] = None,
    tool_type: Optional[str] = None,
) -> BlindAIToolWrapper:
    """Convenience function to wrap a LangChain tool with Blind AI protection.

    Args:
        tool: LangChain tool to protect
        guard: Blind AI SDK client (sync ToolGuard or async AsyncToolGuard)
        auto_register: If True, automatically register tool with guard's registry
        trust_level: Override inferred trust level (HIGH, MEDIUM, LOW)
        tool_type: Override inferred tool type (DATABASE, API, EMAIL, etc.)

    Returns:
        Protected tool wrapper

    Example:
        ```python
        from langchain.tools import ShellTool
        from blind_ai.integrations.langchain import protect_tool
        from blind_ai.sdk import ToolGuard

        # Basic protection
        shell = protect_tool(ShellTool(), guard=ToolGuard())

        # With auto-registration
        guard = ToolGuard(base_url="http://localhost:8000")
        shell = protect_tool(
            ShellTool(),
            guard=guard,
            auto_register=True,  # Registers with inferred type=COMMAND, trust=LOW
        )

        # Override inferred values
        sql_tool = protect_tool(
            my_sql_tool,
            guard=guard,
            auto_register=True,
            trust_level="LOW",
            tool_type="DATABASE",
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
    """Create a protected LangChain tool from a function.

    Args:
        func: Function to wrap as tool
        name: Tool name
        description: Tool description
        guard: Blind AI SDK client (sync ToolGuard or async AsyncToolGuard)
        **kwargs: Additional StructuredTool arguments

    Returns:
        Protected tool

    Example:
        ```python
        from blind_ai.integrations.langchain import create_protected_tool
        from blind_ai.sdk.async_client import AsyncToolGuard

        def execute_sql(query: str) -> str:
            return db.execute(query)

        # Sync protection
        safe_sql_tool = create_protected_tool(
            func=execute_sql,
            name="sql_executor",
            description="Execute SQL queries"
        )

        # Async protection (truly non-blocking)
        async_guard = AsyncToolGuard()
        safe_async_sql = create_protected_tool(
            func=execute_sql,
            name="sql_executor",
            description="Execute SQL queries",
            guard=async_guard
        )
        ```
    """
    # Create StructuredTool from function
    base_tool = StructuredTool.from_function(
        func=func,
        name=name,
        description=description,
        **kwargs,
    )

    # Wrap with protection
    return BlindAIToolWrapper(tool=base_tool, guard=guard)
