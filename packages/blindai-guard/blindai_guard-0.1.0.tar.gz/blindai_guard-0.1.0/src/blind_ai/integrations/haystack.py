"""Haystack integration for Blind AI.

Provides secure component wrappers for Deepset Haystack pipelines.
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


class BlindAIHaystackComponent:
    """Base component wrapper for Haystack with Blind AI protection.

    Wraps any Haystack component to add threat detection on inputs.

    Example:
        ```python
        from haystack.components.generators import OpenAIGenerator
        from blind_ai.integrations.haystack import BlindAIHaystackComponent

        # Wrap a generator component
        generator = OpenAIGenerator(model="gpt-4")
        safe_generator = BlindAIHaystackComponent(
            component=generator,
            guard=ToolGuard(base_url="http://localhost:8000"),
            input_fields=["prompt"]
        )

        # Use in pipeline
        pipeline.add_component("generator", safe_generator)
        ```

    Attributes:
        component: The wrapped Haystack component
        guard: Blind AI SDK client
        input_fields: Fields to check for threats
    """

    def __init__(
        self,
        component: Any,
        guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
        input_fields: Optional[List[str]] = None,
        block_on_threat: bool = True,
    ):
        """Initialize protected component wrapper.

        Args:
            component: Haystack component to wrap
            guard: Blind AI SDK client (creates default if not provided)
            input_fields: List of input field names to check (default: all string fields)
            block_on_threat: If True, raise exception. If False, return error in output.
        """
        self.component = component
        self.guard = guard or ToolGuard()
        self.input_fields = input_fields
        self.block_on_threat = block_on_threat

    def run(self, **kwargs: Any) -> Dict[str, Any]:
        """Run the component with Blind AI protection.

        Args:
            **kwargs: Input arguments for the component

        Returns:
            Component output

        Raises:
            ThreatBlockedError: If threat detected and block_on_threat is True
        """
        # Extract inputs to check and convert to JSON for structured analysis
        inputs_to_check = self._extract_inputs(kwargs)
        
        if inputs_to_check:
            # Check all inputs as a single structured JSON payload
            try:
                tool_input = json.dumps(inputs_to_check, ensure_ascii=False)
                self.guard.check(tool_input)
            except ThreatBlockedError as e:
                logger.warning(f"Blocked Haystack component: {e}")
                if self.block_on_threat:
                    raise ThreatBlockedError(
                        message=f"Blocked component input: {str(e)}",
                        threat_level=e.threat_level,
                        threats=e.threats,
                        response=e.response,
                    ) from e
                return {"error": f"Input blocked due to security policy: {e}"}
            except Exception as e:
                # Log infrastructure errors but don't block execution
                logger.error(f"Blind AI check failed for Haystack component: {e}", exc_info=True)
                # Fail open - allow the call to proceed

        # If safe (or check failed), run the wrapped component
        return self.component.run(**kwargs)

    async def run_async(self, **kwargs: Any) -> Dict[str, Any]:
        """Run the component asynchronously with Blind AI protection.

        Args:
            **kwargs: Input arguments for the component

        Returns:
            Component output
        """
        # Extract inputs to check and convert to JSON for structured analysis
        inputs_to_check = self._extract_inputs(kwargs)

        if inputs_to_check:
            # Check all inputs as a single structured JSON payload
            global _sync_guard_async_usage_count
            try:
                tool_input = json.dumps(inputs_to_check, ensure_ascii=False)
                if isinstance(self.guard, AsyncToolGuard):
                    # Truly async - no blocking, no thread pool overhead
                    await self.guard.check(tool_input)
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
                    import asyncio
                    await asyncio.to_thread(self.guard.check, tool_input)
            except ThreatBlockedError as e:
                logger.warning(f"Blocked Haystack component: {e}")
                if self.block_on_threat:
                    raise
                return {"error": f"Input blocked due to security policy: {e}"}
            except Exception as e:
                # Log infrastructure errors but don't block execution
                logger.error(f"Blind AI async check failed for Haystack component: {e}", exc_info=True)
                # Fail open - allow the call to proceed

        # If safe (or check failed), run the wrapped component
        if hasattr(self.component, 'run_async'):
            return await self.component.run_async(**kwargs)
        return self.component.run(**kwargs)

    def _extract_inputs(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Extract input values to check, preserving structure.

        Args:
            kwargs: Input arguments

        Returns:
            Dictionary of field names to values (serializable)
        """
        inputs: Dict[str, Any] = {}

        if self.input_fields:
            # Check specified fields
            for field in self.input_fields:
                if field in kwargs:
                    value = kwargs[field]
                    if isinstance(value, (str, int, float, bool)):
                        inputs[field] = value
                    elif isinstance(value, list):
                        # Preserve list structure
                        inputs[field] = [str(v) if not isinstance(v, (str, int, float, bool)) else v for v in value]
                    else:
                        inputs[field] = str(value)
        else:
            # Check all serializable fields
            for key, value in kwargs.items():
                if isinstance(value, (str, int, float, bool)):
                    inputs[key] = value
                elif isinstance(value, list) and value:
                    inputs[key] = [str(v) if not isinstance(v, (str, int, float, bool)) else v for v in value]

        return inputs

    # Delegate attribute access to wrapped component
    def __getattr__(self, name: str) -> Any:
        return getattr(self.component, name)


def protect_haystack_component(
    guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
    input_fields: Optional[List[str]] = None,
    block_on_threat: bool = True,
) -> Callable:
    """Decorator to protect a Haystack custom component with Blind AI.

    Example:
        ```python
        from haystack import component
        from blind_ai.integrations.haystack import protect_haystack_component

        guard = ToolGuard(base_url="http://localhost:8000")

        @component
        class DatabaseQueryComponent:
            @component.output_types(results=List[str])
            @protect_haystack_component(guard=guard, input_fields=["query"])
            def run(self, query: str) -> Dict[str, List[str]]:
                results = db.execute(query)
                return {"results": results}
        ```

    Args:
        guard: Blind AI SDK client
        input_fields: List of input field names to check
        block_on_threat: If True, raise exception on threat

    Returns:
        Decorated function
    """
    if guard is None:
        guard = ToolGuard()

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Build input string from specified fields or all kwargs
            if input_fields:
                inputs = {k: str(v) for k, v in kwargs.items() if k in input_fields}
            else:
                inputs = {k: str(v) for k, v in kwargs.items() if isinstance(v, str)}

            # Check for threats
            for field_name, value in inputs.items():
                try:
                    guard.check(value)
                except ThreatBlockedError as e:
                    logger.warning(f"Blocked Haystack component {func.__name__}: {e}")
                    if block_on_threat:
                        raise
                    return {"error": f"Input blocked: {e}"}

            # If safe, run the function
            return func(*args, **kwargs)

        return wrapper

    return decorator


class BlindAIPipelineMonitor:
    """Monitor for Haystack pipelines to track and protect all component runs.

    Example:
        ```python
        from haystack import Pipeline
        from blind_ai.integrations.haystack import BlindAIPipelineMonitor

        pipeline = Pipeline()
        # ... add components ...

        monitor = BlindAIPipelineMonitor(guard=ToolGuard())

        # Run with monitoring
        result = monitor.run_pipeline(
            pipeline,
            data={"query": "user input here"}
        )
        ```
    """

    def __init__(
        self,
        guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
        check_inputs: bool = True,
        check_outputs: bool = False,
        log_runs: bool = True,
    ):
        """Initialize the monitor.

        Args:
            guard: Blind AI SDK client
            check_inputs: Whether to check pipeline inputs
            check_outputs: Whether to check component outputs
            log_runs: Whether to log all pipeline runs
        """
        self.guard = guard or ToolGuard()
        self.check_inputs = check_inputs
        self.check_outputs = check_outputs
        self.log_runs = log_runs
        self.run_history: List[Dict[str, Any]] = []
        self.blocked_count = 0
        self.allowed_count = 0

    def run_pipeline(
        self,
        pipeline: Any,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Run a pipeline with Blind AI monitoring.

        Args:
            pipeline: Haystack Pipeline instance
            data: Input data for the pipeline

        Returns:
            Pipeline output

        Raises:
            ThreatBlockedError: If threat detected in inputs
        """
        # Check inputs if enabled
        if self.check_inputs:
            self._check_data(data, "input")

        # Log if enabled
        if self.log_runs:
            run_record = {
                "inputs": {k: str(v)[:200] for k, v in data.items()},
                "blocked": False,
            }
            self.run_history.append(run_record)

        # Run the pipeline
        try:
            result = pipeline.run(data)
            self.allowed_count += 1

            # Check outputs if enabled
            if self.check_outputs:
                self._check_data(result, "output")

            return result

        except ThreatBlockedError:
            self.blocked_count += 1
            if self.log_runs and self.run_history:
                self.run_history[-1]["blocked"] = True
            raise

    def _check_data(self, data: Dict[str, Any], context: str) -> None:
        """Check data dictionary for threats.

        Args:
            data: Data to check
            context: Context string for logging ("input" or "output")
        """
        for key, value in data.items():
            if isinstance(value, str):
                try:
                    self.guard.check(value)
                except ThreatBlockedError as e:
                    logger.warning(f"Blocked Haystack pipeline {context} '{key}': {e}")
                    raise
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, str):
                        try:
                            self.guard.check(item)
                        except ThreatBlockedError as e:
                            logger.warning(
                                f"Blocked Haystack pipeline {context} '{key}[{i}]': {e}"
                            )
                            raise

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

    def get_run_history(self) -> List[Dict[str, Any]]:
        """Get the run history.

        Returns:
            List of run records
        """
        return self.run_history.copy()

    def clear_history(self) -> None:
        """Clear run history and reset stats."""
        self.run_history.clear()
        self.blocked_count = 0
        self.allowed_count = 0


def wrap_haystack_components(
    components: Dict[str, Any],
    guard: Optional[Union[ToolGuard, AsyncToolGuard]] = None,
    input_fields_map: Optional[Dict[str, List[str]]] = None,
) -> Dict[str, BlindAIHaystackComponent]:
    """Wrap multiple Haystack components with Blind AI protection.

    Example:
        ```python
        from haystack.components.generators import OpenAIGenerator
        from haystack.components.retrievers import InMemoryBM25Retriever
        from blind_ai.integrations.haystack import wrap_haystack_components

        components = {
            "generator": OpenAIGenerator(model="gpt-4"),
            "retriever": InMemoryBM25Retriever(document_store=store),
        }

        protected = wrap_haystack_components(
            components,
            guard=ToolGuard(),
            input_fields_map={
                "generator": ["prompt"],
                "retriever": ["query"],
            }
        )

        # Add to pipeline
        for name, component in protected.items():
            pipeline.add_component(name, component)
        ```

    Args:
        components: Dictionary of component names to components
        guard: Shared Blind AI SDK client
        input_fields_map: Optional mapping of component names to input fields to check

    Returns:
        Dictionary with all components wrapped
    """
    if guard is None:
        guard = ToolGuard()

    wrapped = {}
    for name, component in components.items():
        input_fields = None
        if input_fields_map and name in input_fields_map:
            input_fields = input_fields_map[name]

        wrapped[name] = BlindAIHaystackComponent(
            component=component,
            guard=guard,
            input_fields=input_fields,
        )

    return wrapped
