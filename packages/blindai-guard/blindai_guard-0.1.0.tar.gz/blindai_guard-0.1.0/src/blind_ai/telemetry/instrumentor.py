"""OpenTelemetry Instrumentor for Blind AI SDK.

Provides automatic instrumentation of ToolGuard and AsyncToolGuard clients.
"""

import functools
import time
from typing import Any, Callable, Optional, Collection

from .setup import get_tracer
from .metrics import get_metrics


class BlindAIInstrumentor:
    """Instrumentor for automatic tracing of Blind AI operations.

    Wraps ToolGuard and AsyncToolGuard methods to add OpenTelemetry spans
    and metrics automatically.

    Example:
        ```python
        from blind_ai.telemetry import BlindAIInstrumentor, setup_telemetry

        # Setup telemetry first
        setup_telemetry(service_name="my-agent")

        # Instrument the SDK
        instrumentor = BlindAIInstrumentor()
        instrumentor.instrument()

        # Now all operations are traced
        from blind_ai import ToolGuard
        guard = ToolGuard()
        guard.check("SELECT * FROM users")  # Automatically creates span
        ```
    """

    _instance: Optional["BlindAIInstrumentor"] = None
    _is_instrumented: bool = False

    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize instrumentor."""
        self._tracer = get_tracer("blind_ai")
        self._metrics = get_metrics()
        self._original_methods = {}

    def instrument(
        self,
        tracer_provider=None,
        meter_provider=None,
    ) -> None:
        """Instrument Blind AI SDK for automatic tracing.

        Args:
            tracer_provider: Optional custom tracer provider
            meter_provider: Optional custom meter provider

        Note:
            This modifies ToolGuard and AsyncToolGuard classes globally.
            Call uninstrument() to restore original behavior.
        """
        if self._is_instrumented:
            return

        # Instrument sync client
        self._instrument_sync_client()

        # Instrument async client
        self._instrument_async_client()

        BlindAIInstrumentor._is_instrumented = True

    def uninstrument(self) -> None:
        """Remove instrumentation and restore original methods."""
        if not self._is_instrumented:
            return

        # Restore original methods
        for (cls, method_name), original in self._original_methods.items():
            setattr(cls, method_name, original)

        self._original_methods.clear()
        BlindAIInstrumentor._is_instrumented = False

    def _instrument_sync_client(self) -> None:
        """Instrument synchronous ToolGuard client."""
        try:
            from blind_ai.sdk.client import ToolGuard
        except ImportError:
            return

        # Instrument check method
        self._wrap_method(
            ToolGuard,
            "check",
            self._create_sync_wrapper("blind_ai.check"),
        )

        # Instrument call_tool method
        self._wrap_method(
            ToolGuard,
            "call_tool",
            self._create_sync_wrapper("blind_ai.call_tool"),
        )

        # Instrument register_tool method
        self._wrap_method(
            ToolGuard,
            "register_tool",
            self._create_sync_wrapper("blind_ai.register_tool"),
        )

    def _instrument_async_client(self) -> None:
        """Instrument asynchronous AsyncToolGuard client."""
        try:
            from blind_ai.sdk.async_client import AsyncToolGuard
        except ImportError:
            return

        # Instrument async check method
        self._wrap_method(
            AsyncToolGuard,
            "check",
            self._create_async_wrapper("blind_ai.check"),
        )

    def _wrap_method(
        self,
        cls: type,
        method_name: str,
        wrapper_factory: Callable,
    ) -> None:
        """Wrap a method with instrumentation.

        Args:
            cls: Class containing the method
            method_name: Name of method to wrap
            wrapper_factory: Factory function that creates the wrapper
        """
        if not hasattr(cls, method_name):
            return

        original = getattr(cls, method_name)

        # Store original for uninstrument
        self._original_methods[(cls, method_name)] = original

        # Create and set wrapper
        wrapped = wrapper_factory(original)
        setattr(cls, method_name, wrapped)

    def _create_sync_wrapper(self, span_name: str) -> Callable:
        """Create a synchronous wrapper with tracing.

        Args:
            span_name: Name for the span

        Returns:
            Wrapper factory function
        """
        tracer = self._tracer
        metrics = self._metrics

        def wrapper_factory(original: Callable) -> Callable:
            @functools.wraps(original)
            def wrapper(self_instance, *args, **kwargs):
                start_time = time.perf_counter()

                # Extract attributes from arguments
                attrs = _extract_attributes(args, kwargs)

                with tracer.start_as_current_span(span_name) as span:
                    # Set span attributes
                    for key, value in attrs.items():
                        span.set_attribute(key, value)

                    try:
                        result = original(self_instance, *args, **kwargs)

                        # Record success metrics
                        latency_ms = (time.perf_counter() - start_time) * 1000

                        # Extract result attributes
                        result_attrs = _extract_result_attributes(result)
                        for key, value in result_attrs.items():
                            span.set_attribute(key, value)

                        # Record metrics
                        action = result_attrs.get("action", "allow")
                        threat_type = result_attrs.get("threat_type")
                        threat_level = result_attrs.get("threat_level", "none")

                        metrics.record_request(
                            action=action,
                            latency_ms=latency_ms,
                            threat_type=threat_type,
                            threat_level=threat_level,
                        )

                        return result

                    except Exception as e:
                        # Record error
                        latency_ms = (time.perf_counter() - start_time) * 1000
                        span.record_exception(e)

                        error_type = type(e).__name__
                        metrics.record_error(error_type)

                        # Check if it's a ThreatBlockedError
                        if hasattr(e, "threat_level"):
                            metrics.record_request(
                                action="block",
                                latency_ms=latency_ms,
                                threat_level=getattr(e, "threat_level", "unknown"),
                            )
                            span.set_attribute("threat_blocked", True)
                            span.set_attribute("threat_level", getattr(e, "threat_level", "unknown"))

                        raise

            return wrapper

        return wrapper_factory

    def _create_async_wrapper(self, span_name: str) -> Callable:
        """Create an asynchronous wrapper with tracing.

        Args:
            span_name: Name for the span

        Returns:
            Wrapper factory function
        """
        tracer = self._tracer
        metrics = self._metrics

        def wrapper_factory(original: Callable) -> Callable:
            @functools.wraps(original)
            async def wrapper(self_instance, *args, **kwargs):
                start_time = time.perf_counter()

                # Extract attributes from arguments
                attrs = _extract_attributes(args, kwargs)

                with tracer.start_as_current_span(span_name) as span:
                    # Set span attributes
                    for key, value in attrs.items():
                        span.set_attribute(key, value)

                    try:
                        result = await original(self_instance, *args, **kwargs)

                        # Record success metrics
                        latency_ms = (time.perf_counter() - start_time) * 1000

                        # Extract result attributes
                        result_attrs = _extract_result_attributes(result)
                        for key, value in result_attrs.items():
                            span.set_attribute(key, value)

                        # Record metrics
                        action = result_attrs.get("action", "allow")
                        threat_type = result_attrs.get("threat_type")
                        threat_level = result_attrs.get("threat_level", "none")

                        metrics.record_request(
                            action=action,
                            latency_ms=latency_ms,
                            threat_type=threat_type,
                            threat_level=threat_level,
                        )

                        return result

                    except Exception as e:
                        # Record error
                        latency_ms = (time.perf_counter() - start_time) * 1000
                        span.record_exception(e)

                        error_type = type(e).__name__
                        metrics.record_error(error_type)

                        # Check if it's a ThreatBlockedError
                        if hasattr(e, "threat_level"):
                            metrics.record_request(
                                action="block",
                                latency_ms=latency_ms,
                                threat_level=getattr(e, "threat_level", "unknown"),
                            )
                            span.set_attribute("threat_blocked", True)
                            span.set_attribute("threat_level", getattr(e, "threat_level", "unknown"))

                        raise

            return wrapper

        return wrapper_factory


def _extract_attributes(args: tuple, kwargs: dict) -> dict[str, Any]:
    """Extract span attributes from method arguments.

    Args:
        args: Positional arguments
        kwargs: Keyword arguments

    Returns:
        Dictionary of attributes
    """
    attrs = {}

    # Extract text (usually first arg for check())
    if args and isinstance(args[0], str):
        text = args[0]
        attrs["input_length"] = len(text)
        # Don't include actual text for privacy
        attrs["input_preview"] = text[:50] + "..." if len(text) > 50 else text

    # Extract context_id
    if "context_id" in kwargs:
        attrs["context_id"] = kwargs["context_id"]

    # Extract tool_name
    if "name" in kwargs:
        attrs["tool_name"] = kwargs["name"]

    # Extract user info
    if "user" in kwargs and kwargs["user"]:
        user = kwargs["user"]
        if hasattr(user, "user_id"):
            attrs["user_id"] = user.user_id
        if hasattr(user, "role"):
            attrs["user_role"] = str(user.role)

    return attrs


def _extract_result_attributes(result: Any) -> dict[str, Any]:
    """Extract span attributes from method result.

    Args:
        result: Method return value

    Returns:
        Dictionary of attributes
    """
    attrs = {}

    if result is None:
        return attrs

    # Handle ProtectionResult
    if hasattr(result, "is_threat"):
        attrs["is_threat"] = result.is_threat
    if hasattr(result, "threat_level"):
        attrs["threat_level"] = result.threat_level
    if hasattr(result, "final_action"):
        attrs["action"] = result.final_action
    if hasattr(result, "confidence"):
        attrs["confidence"] = result.confidence
    if hasattr(result, "processing_time_ms"):
        attrs["processing_time_ms"] = result.processing_time_ms

    # Extract first threat type if available
    if hasattr(result, "threats_detected") and result.threats_detected:
        first_threat = result.threats_detected[0]
        if isinstance(first_threat, dict):
            attrs["threat_type"] = first_threat.get("type", "unknown")
        elif hasattr(first_threat, "threat_type"):
            attrs["threat_type"] = str(first_threat.threat_type)

    return attrs
