"""Observability utilities for Blind AI integrations.

Provides metrics, structured logging, and distributed tracing support.
"""

import json
import logging
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union

# Set up logging
logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of metrics."""
    COUNTER = "counter"
    HISTOGRAM = "histogram"
    GAUGE = "gauge"


@dataclass
class SecurityMetrics:
    """Metrics collector for Blind AI security checks.
    
    Collects metrics that can be exported to Prometheus, StatsD, or other systems.
    
    Example:
        ```python
        from blind_ai.integrations.observability import SecurityMetrics
        
        metrics = SecurityMetrics()
        
        # Record a check
        metrics.record_check(
            tool_name="database_query",
            allowed=True,
            latency_ms=15.5,
            threat_level=None
        )
        
        # Get metrics for export
        print(metrics.get_summary())
        
        # Export to Prometheus format
        print(metrics.to_prometheus())
        ```
    """
    
    # Counters
    checks_total: int = 0
    checks_allowed: int = 0
    checks_blocked: int = 0
    checks_challenged: int = 0
    checks_failed: int = 0  # Infrastructure failures
    
    # Per-tool counters
    checks_by_tool: Dict[str, int] = field(default_factory=dict)
    blocks_by_tool: Dict[str, int] = field(default_factory=dict)
    
    # Per-threat counters
    threats_by_type: Dict[str, int] = field(default_factory=dict)
    
    # Latency tracking (for histogram)
    latencies_ms: List[float] = field(default_factory=list)
    _max_latency_samples: int = 10000  # Limit memory usage
    
    def record_check(
        self,
        tool_name: str,
        allowed: bool,
        latency_ms: float,
        threat_level: Optional[str] = None,
        threat_types: Optional[List[str]] = None,
        action: str = "allow",
    ) -> None:
        """Record a security check.
        
        Args:
            tool_name: Name of the tool being checked
            allowed: Whether the call was allowed
            latency_ms: Check latency in milliseconds
            threat_level: Threat level if detected (e.g., "high", "medium")
            threat_types: List of threat types detected
            action: Final action taken ("allow", "block", "challenge")
        """
        self.checks_total += 1
        
        # Track by tool
        self.checks_by_tool[tool_name] = self.checks_by_tool.get(tool_name, 0) + 1
        
        # Track outcome
        if action == "block":
            self.checks_blocked += 1
            self.blocks_by_tool[tool_name] = self.blocks_by_tool.get(tool_name, 0) + 1
        elif action == "challenge":
            self.checks_challenged += 1
        else:
            self.checks_allowed += 1
        
        # Track threat types
        if threat_types:
            for threat_type in threat_types:
                self.threats_by_type[threat_type] = self.threats_by_type.get(threat_type, 0) + 1
        
        # Track latency (with limit)
        if len(self.latencies_ms) < self._max_latency_samples:
            self.latencies_ms.append(latency_ms)
    
    def record_failure(self, tool_name: str, error: str) -> None:
        """Record an infrastructure failure.
        
        Args:
            tool_name: Name of the tool
            error: Error message
        """
        self.checks_failed += 1
        logger.debug(f"Recorded failure for {tool_name}: {error}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all metrics.
        
        Returns:
            Dictionary with metric summary
        """
        latency_stats = self._calculate_latency_stats()
        
        return {
            "checks": {
                "total": self.checks_total,
                "allowed": self.checks_allowed,
                "blocked": self.checks_blocked,
                "challenged": self.checks_challenged,
                "failed": self.checks_failed,
            },
            "by_tool": self.checks_by_tool,
            "blocks_by_tool": self.blocks_by_tool,
            "threats_by_type": self.threats_by_type,
            "latency_ms": latency_stats,
        }
    
    def _calculate_latency_stats(self) -> Dict[str, float]:
        """Calculate latency statistics."""
        if not self.latencies_ms:
            return {"p50": 0, "p95": 0, "p99": 0, "avg": 0, "max": 0}
        
        sorted_latencies = sorted(self.latencies_ms)
        n = len(sorted_latencies)
        
        return {
            "p50": sorted_latencies[int(n * 0.5)] if n > 0 else 0,
            "p95": sorted_latencies[int(n * 0.95)] if n > 0 else 0,
            "p99": sorted_latencies[int(n * 0.99)] if n > 0 else 0,
            "avg": sum(sorted_latencies) / n if n > 0 else 0,
            "max": max(sorted_latencies) if n > 0 else 0,
        }
    
    def to_prometheus(self, prefix: str = "blindai") -> str:
        """Export metrics in Prometheus format.
        
        Args:
            prefix: Metric name prefix
            
        Returns:
            Prometheus-formatted metrics string
        """
        lines = []
        
        # Counters
        lines.append(f"# HELP {prefix}_checks_total Total number of security checks")
        lines.append(f"# TYPE {prefix}_checks_total counter")
        lines.append(f"{prefix}_checks_total {self.checks_total}")
        
        lines.append(f"# HELP {prefix}_checks_allowed Number of allowed checks")
        lines.append(f"# TYPE {prefix}_checks_allowed counter")
        lines.append(f"{prefix}_checks_allowed {self.checks_allowed}")
        
        lines.append(f"# HELP {prefix}_checks_blocked Number of blocked checks")
        lines.append(f"# TYPE {prefix}_checks_blocked counter")
        lines.append(f"{prefix}_checks_blocked {self.checks_blocked}")
        
        lines.append(f"# HELP {prefix}_checks_failed Number of failed checks (infrastructure)")
        lines.append(f"# TYPE {prefix}_checks_failed counter")
        lines.append(f"{prefix}_checks_failed {self.checks_failed}")
        
        # Per-tool metrics
        lines.append(f"# HELP {prefix}_checks_by_tool Checks per tool")
        lines.append(f"# TYPE {prefix}_checks_by_tool counter")
        for tool, count in self.checks_by_tool.items():
            lines.append(f'{prefix}_checks_by_tool{{tool="{tool}"}} {count}')
        
        lines.append(f"# HELP {prefix}_blocks_by_tool Blocks per tool")
        lines.append(f"# TYPE {prefix}_blocks_by_tool counter")
        for tool, count in self.blocks_by_tool.items():
            lines.append(f'{prefix}_blocks_by_tool{{tool="{tool}"}} {count}')
        
        # Threat types
        lines.append(f"# HELP {prefix}_threats_by_type Threats detected by type")
        lines.append(f"# TYPE {prefix}_threats_by_type counter")
        for threat_type, count in self.threats_by_type.items():
            lines.append(f'{prefix}_threats_by_type{{type="{threat_type}"}} {count}')
        
        # Latency histogram summary
        stats = self._calculate_latency_stats()
        lines.append(f"# HELP {prefix}_check_latency_ms Check latency in milliseconds")
        lines.append(f"# TYPE {prefix}_check_latency_ms summary")
        lines.append(f'{prefix}_check_latency_ms{{quantile="0.5"}} {stats["p50"]}')
        lines.append(f'{prefix}_check_latency_ms{{quantile="0.95"}} {stats["p95"]}')
        lines.append(f'{prefix}_check_latency_ms{{quantile="0.99"}} {stats["p99"]}')
        
        return "\n".join(lines)
    
    def to_statsd(self, prefix: str = "blindai") -> List[str]:
        """Export metrics in StatsD format.
        
        Args:
            prefix: Metric name prefix
            
        Returns:
            List of StatsD-formatted metric strings
        """
        lines = []
        
        # Counters (use gauge for current values)
        lines.append(f"{prefix}.checks.total:{self.checks_total}|g")
        lines.append(f"{prefix}.checks.allowed:{self.checks_allowed}|g")
        lines.append(f"{prefix}.checks.blocked:{self.checks_blocked}|g")
        lines.append(f"{prefix}.checks.failed:{self.checks_failed}|g")
        
        # Per-tool
        for tool, count in self.checks_by_tool.items():
            safe_tool = tool.replace(".", "_")
            lines.append(f"{prefix}.checks.by_tool.{safe_tool}:{count}|g")
        
        # Latency
        stats = self._calculate_latency_stats()
        lines.append(f"{prefix}.latency.p50:{stats['p50']}|g")
        lines.append(f"{prefix}.latency.p95:{stats['p95']}|g")
        lines.append(f"{prefix}.latency.p99:{stats['p99']}|g")
        
        return lines
    
    def reset(self) -> None:
        """Reset all metrics."""
        self.checks_total = 0
        self.checks_allowed = 0
        self.checks_blocked = 0
        self.checks_challenged = 0
        self.checks_failed = 0
        self.checks_by_tool.clear()
        self.blocks_by_tool.clear()
        self.threats_by_type.clear()
        self.latencies_ms.clear()


# Global metrics instance
_global_metrics: Optional[SecurityMetrics] = None


def get_metrics() -> SecurityMetrics:
    """Get the global metrics instance.
    
    Returns:
        Global SecurityMetrics instance
    """
    global _global_metrics
    if _global_metrics is None:
        _global_metrics = SecurityMetrics()
    return _global_metrics


def reset_metrics() -> None:
    """Reset the global metrics instance."""
    global _global_metrics
    if _global_metrics:
        _global_metrics.reset()


@dataclass
class StructuredLogContext:
    """Context for structured logging with correlation IDs.
    
    Example:
        ```python
        from blind_ai.integrations.observability import StructuredLogContext
        
        # Create context for a request
        ctx = StructuredLogContext(
            correlation_id="req-123",
            session_id="session-456",
            user_id="user-789"
        )
        
        # Log with context
        ctx.log_check_start("database_query", {"query": "SELECT..."})
        ctx.log_check_result("database_query", allowed=True, latency_ms=15.0)
        ```
    """
    
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)
    
    def _base_fields(self) -> Dict[str, Any]:
        """Get base fields for all log entries."""
        fields = {
            "correlation_id": self.correlation_id,
        }
        if self.session_id:
            fields["session_id"] = self.session_id
        if self.user_id:
            fields["user_id"] = self.user_id
        if self.trace_id:
            fields["trace_id"] = self.trace_id
        if self.span_id:
            fields["span_id"] = self.span_id
        fields.update(self.extra)
        return fields
    
    def log_check_start(
        self,
        tool_name: str,
        input_preview: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log the start of a security check.
        
        Args:
            tool_name: Name of the tool being checked
            input_preview: Preview of input (truncated for safety)
        """
        entry = {
            "event": "security_check_start",
            "tool": tool_name,
            **self._base_fields(),
        }
        if input_preview:
            # Truncate values for safety
            entry["input_preview"] = {
                k: str(v)[:100] + "..." if len(str(v)) > 100 else v
                for k, v in input_preview.items()
            }
        
        logger.info(json.dumps(entry))
    
    def log_check_result(
        self,
        tool_name: str,
        allowed: bool,
        latency_ms: float,
        action: str = "allow",
        threat_level: Optional[str] = None,
        threat_types: Optional[List[str]] = None,
    ) -> None:
        """Log the result of a security check.
        
        Args:
            tool_name: Name of the tool
            allowed: Whether the call was allowed
            latency_ms: Check latency in milliseconds
            action: Final action ("allow", "block", "challenge")
            threat_level: Threat level if detected
            threat_types: Types of threats detected
        """
        entry = {
            "event": "security_check_result",
            "tool": tool_name,
            "allowed": allowed,
            "action": action,
            "latency_ms": round(latency_ms, 2),
            **self._base_fields(),
        }
        if threat_level:
            entry["threat_level"] = threat_level
        if threat_types:
            entry["threat_types"] = threat_types
        
        log_level = logging.WARNING if action == "block" else logging.INFO
        logger.log(log_level, json.dumps(entry))
    
    def log_check_error(
        self,
        tool_name: str,
        error: str,
        error_type: str = "unknown",
    ) -> None:
        """Log a security check error.
        
        Args:
            tool_name: Name of the tool
            error: Error message
            error_type: Type of error
        """
        entry = {
            "event": "security_check_error",
            "tool": tool_name,
            "error": error,
            "error_type": error_type,
            **self._base_fields(),
        }
        logger.error(json.dumps(entry))


# Thread-local storage for context
import threading
_context_local = threading.local()


def get_current_context() -> Optional[StructuredLogContext]:
    """Get the current logging context.
    
    Returns:
        Current context or None
    """
    return getattr(_context_local, 'context', None)


def set_current_context(ctx: StructuredLogContext) -> None:
    """Set the current logging context.
    
    Args:
        ctx: Context to set
    """
    _context_local.context = ctx


@contextmanager
def logging_context(
    correlation_id: Optional[str] = None,
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    **extra,
):
    """Context manager for structured logging.
    
    Example:
        ```python
        from blind_ai.integrations.observability import logging_context
        
        with logging_context(correlation_id="req-123", user_id="user-456"):
            # All security checks in this block will include these IDs
            result = guard.check(input_text)
        ```
    
    Args:
        correlation_id: Correlation ID (auto-generated if not provided)
        session_id: Session ID
        user_id: User ID
        **extra: Additional context fields
    """
    ctx = StructuredLogContext(
        correlation_id=correlation_id or str(uuid.uuid4()),
        session_id=session_id,
        user_id=user_id,
        extra=extra,
    )
    old_ctx = get_current_context()
    set_current_context(ctx)
    try:
        yield ctx
    finally:
        set_current_context(old_ctx)


# OpenTelemetry support (optional dependency)
_tracer = None


def init_tracing(
    service_name: str = "blind-ai",
    exporter: Optional[str] = None,
    endpoint: Optional[str] = None,
) -> bool:
    """Initialize OpenTelemetry tracing.
    
    Args:
        service_name: Name of the service
        exporter: Exporter type ("jaeger", "zipkin", "otlp", or None for console)
        endpoint: Exporter endpoint URL
        
    Returns:
        True if tracing was initialized successfully
        
    Example:
        ```python
        from blind_ai.integrations.observability import init_tracing
        
        # Initialize with OTLP exporter
        init_tracing(
            service_name="my-ai-agent",
            exporter="otlp",
            endpoint="http://localhost:4317"
        )
        ```
    """
    global _tracer
    
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.resources import Resource
        
        # Create resource
        resource = Resource.create({"service.name": service_name})
        
        # Create provider
        provider = TracerProvider(resource=resource)
        
        # Add exporter based on type
        if exporter == "otlp":
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
            from opentelemetry.sdk.trace.export import BatchSpanProcessor
            
            otlp_exporter = OTLPSpanExporter(endpoint=endpoint)
            provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
            
        elif exporter == "jaeger":
            from opentelemetry.exporter.jaeger.thrift import JaegerExporter
            from opentelemetry.sdk.trace.export import BatchSpanProcessor
            
            jaeger_exporter = JaegerExporter(agent_host_name=endpoint or "localhost")
            provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
            
        elif exporter == "zipkin":
            from opentelemetry.exporter.zipkin.json import ZipkinExporter
            from opentelemetry.sdk.trace.export import BatchSpanProcessor
            
            zipkin_exporter = ZipkinExporter(endpoint=endpoint)
            provider.add_span_processor(BatchSpanProcessor(zipkin_exporter))
            
        else:
            # Console exporter for debugging
            from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
            provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
        
        # Set global provider
        trace.set_tracer_provider(provider)
        _tracer = trace.get_tracer(__name__)
        
        logger.info(f"OpenTelemetry tracing initialized with {exporter or 'console'} exporter")
        return True
        
    except ImportError as e:
        logger.warning(
            f"OpenTelemetry not available: {e}. "
            "Install with: pip install opentelemetry-api opentelemetry-sdk"
        )
        return False
    except Exception as e:
        logger.error(f"Failed to initialize tracing: {e}")
        return False


def get_tracer():
    """Get the OpenTelemetry tracer.
    
    Returns:
        Tracer instance or None if not initialized
    """
    return _tracer


@contextmanager
def trace_security_check(
    tool_name: str,
    input_size: Optional[int] = None,
    **attributes,
):
    """Context manager to trace a security check.
    
    Creates an OpenTelemetry span for the security check if tracing is enabled.
    
    Example:
        ```python
        from blind_ai.integrations.observability import trace_security_check
        
        with trace_security_check("database_query", input_size=len(query)) as span:
            result = guard.check(query)
            span.set_attribute("blindai.allowed", result.allowed)
        ```
    
    Args:
        tool_name: Name of the tool being checked
        input_size: Size of input in bytes/chars
        **attributes: Additional span attributes
    """
    tracer = get_tracer()
    
    if tracer is None:
        # No-op if tracing not initialized
        yield type('FakeSpan', (), {
            'set_attribute': lambda self, k, v: None,
            'set_status': lambda self, s: None,
            'record_exception': lambda self, e: None,
        })()
        return
    
    with tracer.start_as_current_span(
        f"blindai.check.{tool_name}",
        attributes={
            "blindai.tool": tool_name,
            "blindai.input_size": input_size or 0,
            **attributes,
        },
    ) as span:
        start_time = time.time()
        try:
            yield span
        except Exception as e:
            span.record_exception(e)
            span.set_attribute("blindai.error", str(e))
            raise
        finally:
            latency_ms = (time.time() - start_time) * 1000
            span.set_attribute("blindai.latency_ms", latency_ms)


class ObservableGuard:
    """Wrapper that adds observability to any guard.
    
    Automatically records metrics, structured logs, and traces for all checks.
    
    Example:
        ```python
        from blind_ai import ToolGuard
        from blind_ai.integrations.observability import ObservableGuard
        
        # Wrap your guard with observability
        guard = ToolGuard(base_url="http://localhost:8000")
        observable_guard = ObservableGuard(guard)
        
        # Use it normally - metrics and traces are automatic
        result = observable_guard.check(input_text)
        
        # Get metrics
        print(observable_guard.metrics.to_prometheus())
        ```
    """
    
    def __init__(
        self,
        guard,
        metrics: Optional[SecurityMetrics] = None,
        enable_tracing: bool = True,
        enable_logging: bool = True,
    ):
        """Initialize observable guard.
        
        Args:
            guard: The underlying guard (ToolGuard or AsyncToolGuard)
            metrics: Metrics collector (uses global if not provided)
            enable_tracing: Whether to create trace spans
            enable_logging: Whether to emit structured logs
        """
        self.guard = guard
        self.metrics = metrics or get_metrics()
        self.enable_tracing = enable_tracing
        self.enable_logging = enable_logging
    
    def check(
        self,
        input_text: str,
        tool_name: str = "unknown",
        context_id: Optional[str] = None,
    ):
        """Check input with full observability.
        
        Args:
            input_text: Input to check
            tool_name: Name of the tool
            context_id: Optional context ID
            
        Returns:
            Check result from underlying guard
        """
        ctx = get_current_context() or StructuredLogContext()
        
        if self.enable_logging:
            ctx.log_check_start(tool_name, {"input_length": len(input_text)})
        
        start_time = time.time()
        
        try:
            with trace_security_check(tool_name, input_size=len(input_text)) as span:
                result = self.guard.check(input_text, context_id=context_id)
                
                latency_ms = (time.time() - start_time) * 1000
                
                # Record metrics
                self.metrics.record_check(
                    tool_name=tool_name,
                    allowed=result.allowed if hasattr(result, 'allowed') else True,
                    latency_ms=latency_ms,
                    threat_level=getattr(result, 'threat_level', None),
                    threat_types=getattr(result, 'threats_detected', None),
                    action=getattr(result, 'final_action', 'allow'),
                )
                
                # Set span attributes
                if self.enable_tracing and span:
                    span.set_attribute("blindai.allowed", getattr(result, 'allowed', True))
                    span.set_attribute("blindai.action", getattr(result, 'final_action', 'allow'))
                
                # Log result
                if self.enable_logging:
                    ctx.log_check_result(
                        tool_name=tool_name,
                        allowed=getattr(result, 'allowed', True),
                        latency_ms=latency_ms,
                        action=getattr(result, 'final_action', 'allow'),
                        threat_level=getattr(result, 'threat_level', None),
                    )
                
                return result
                
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            
            self.metrics.record_failure(tool_name, str(e))
            
            if self.enable_logging:
                ctx.log_check_error(tool_name, str(e), type(e).__name__)
            
            raise
    
    async def acheck(
        self,
        input_text: str,
        tool_name: str = "unknown",
        context_id: Optional[str] = None,
    ):
        """Async check with full observability.
        
        Args:
            input_text: Input to check
            tool_name: Name of the tool
            context_id: Optional context ID
            
        Returns:
            Check result from underlying guard
        """
        ctx = get_current_context() or StructuredLogContext()
        
        if self.enable_logging:
            ctx.log_check_start(tool_name, {"input_length": len(input_text)})
        
        start_time = time.time()
        
        try:
            with trace_security_check(tool_name, input_size=len(input_text)) as span:
                # Use async check if available
                if hasattr(self.guard, 'acheck'):
                    result = await self.guard.acheck(input_text, context_id=context_id)
                else:
                    result = await self.guard.check(input_text, context_id=context_id)
                
                latency_ms = (time.time() - start_time) * 1000
                
                # Record metrics
                self.metrics.record_check(
                    tool_name=tool_name,
                    allowed=result.allowed if hasattr(result, 'allowed') else True,
                    latency_ms=latency_ms,
                    threat_level=getattr(result, 'threat_level', None),
                    threat_types=getattr(result, 'threats_detected', None),
                    action=getattr(result, 'final_action', 'allow'),
                )
                
                # Set span attributes
                if self.enable_tracing and span:
                    span.set_attribute("blindai.allowed", getattr(result, 'allowed', True))
                    span.set_attribute("blindai.action", getattr(result, 'final_action', 'allow'))
                
                # Log result
                if self.enable_logging:
                    ctx.log_check_result(
                        tool_name=tool_name,
                        allowed=getattr(result, 'allowed', True),
                        latency_ms=latency_ms,
                        action=getattr(result, 'final_action', 'allow'),
                        threat_level=getattr(result, 'threat_level', None),
                    )
                
                return result
                
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            
            self.metrics.record_failure(tool_name, str(e))
            
            if self.enable_logging:
                ctx.log_check_error(tool_name, str(e), type(e).__name__)
            
            raise
