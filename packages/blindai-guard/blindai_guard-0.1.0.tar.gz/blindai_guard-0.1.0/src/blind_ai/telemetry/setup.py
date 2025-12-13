"""OpenTelemetry setup utilities for Blind AI.

Provides easy setup for OpenTelemetry tracing and metrics exporters.
"""

import os
from typing import Optional, Sequence

# Lazy imports to avoid requiring opentelemetry as a hard dependency
_tracer_provider = None
_meter_provider = None


def setup_telemetry(
    service_name: str = "blind-ai",
    service_version: Optional[str] = None,
    otlp_endpoint: Optional[str] = None,
    otlp_headers: Optional[dict[str, str]] = None,
    console_export: bool = False,
    enable_metrics: bool = True,
    enable_tracing: bool = True,
    resource_attributes: Optional[dict[str, str]] = None,
) -> None:
    """Setup OpenTelemetry tracing and metrics for Blind AI.

    This configures OpenTelemetry with OTLP exporters for sending telemetry
    data to observability backends like Jaeger, Zipkin, Honeycomb, etc.

    Args:
        service_name: Name of your service (default: "blind-ai")
        service_version: Version of your service (default: blind_ai.__version__)
        otlp_endpoint: OTLP collector endpoint (e.g., "http://localhost:4317")
                      Falls back to OTEL_EXPORTER_OTLP_ENDPOINT env var
        otlp_headers: Headers for OTLP exporter (e.g., API keys)
                     Falls back to OTEL_EXPORTER_OTLP_HEADERS env var
        console_export: Also export to console for debugging (default: False)
        enable_metrics: Enable metrics collection (default: True)
        enable_tracing: Enable distributed tracing (default: True)
        resource_attributes: Additional resource attributes

    Raises:
        ImportError: If opentelemetry packages are not installed

    Example:
        ```python
        from blind_ai.telemetry import setup_telemetry

        # Basic setup with OTLP
        setup_telemetry(
            service_name="my-agent",
            otlp_endpoint="http://localhost:4317",
        )

        # Setup with Honeycomb
        setup_telemetry(
            service_name="my-agent",
            otlp_endpoint="https://api.honeycomb.io",
            otlp_headers={"x-honeycomb-team": "your-api-key"},
        )

        # Debug mode with console output
        setup_telemetry(
            service_name="my-agent",
            console_export=True,
        )
        ```
    """
    global _tracer_provider, _meter_provider

    try:
        from opentelemetry import trace, metrics
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.metrics import MeterProvider
        from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
    except ImportError as e:
        raise ImportError(
            "OpenTelemetry packages not installed. Install with:\n"
            "  pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp"
        ) from e

    # Get version
    if service_version is None:
        try:
            from blind_ai import __version__
            service_version = __version__
        except ImportError:
            service_version = "unknown"

    # Build resource attributes
    attrs = {
        SERVICE_NAME: service_name,
        SERVICE_VERSION: service_version,
    }
    if resource_attributes:
        attrs.update(resource_attributes)

    resource = Resource.create(attrs)

    # Get endpoint from env if not provided
    endpoint = otlp_endpoint or os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")

    # Setup tracing
    if enable_tracing:
        _tracer_provider = _setup_tracing(
            resource=resource,
            endpoint=endpoint,
            headers=otlp_headers,
            console_export=console_export,
        )
        trace.set_tracer_provider(_tracer_provider)

    # Setup metrics
    if enable_metrics:
        _meter_provider = _setup_metrics(
            resource=resource,
            endpoint=endpoint,
            headers=otlp_headers,
            console_export=console_export,
        )
        metrics.set_meter_provider(_meter_provider)


def _setup_tracing(
    resource,
    endpoint: Optional[str],
    headers: Optional[dict[str, str]],
    console_export: bool,
):
    """Setup tracing with exporters."""
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

    provider = TracerProvider(resource=resource)

    # Add OTLP exporter if endpoint provided
    if endpoint:
        try:
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

            otlp_exporter = OTLPSpanExporter(
                endpoint=endpoint,
                headers=headers or {},
            )
            provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        except ImportError:
            # Try HTTP exporter as fallback
            try:
                from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter as HTTPSpanExporter

                otlp_exporter = HTTPSpanExporter(
                    endpoint=f"{endpoint}/v1/traces",
                    headers=headers or {},
                )
                provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
            except ImportError:
                import warnings
                warnings.warn(
                    "OTLP exporter not available. Install with: "
                    "pip install opentelemetry-exporter-otlp-proto-grpc"
                )

    # Add console exporter for debugging
    if console_export:
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    return provider


def _setup_metrics(
    resource,
    endpoint: Optional[str],
    headers: Optional[dict[str, str]],
    console_export: bool,
):
    """Setup metrics with exporters."""
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import (
        ConsoleMetricExporter,
        PeriodicExportingMetricReader,
    )

    readers = []

    # Add OTLP exporter if endpoint provided
    if endpoint:
        try:
            from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

            otlp_exporter = OTLPMetricExporter(
                endpoint=endpoint,
                headers=headers or {},
            )
            readers.append(PeriodicExportingMetricReader(otlp_exporter))
        except ImportError:
            try:
                from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter as HTTPMetricExporter

                otlp_exporter = HTTPMetricExporter(
                    endpoint=f"{endpoint}/v1/metrics",
                    headers=headers or {},
                )
                readers.append(PeriodicExportingMetricReader(otlp_exporter))
            except ImportError:
                import warnings
                warnings.warn(
                    "OTLP metric exporter not available. Install with: "
                    "pip install opentelemetry-exporter-otlp-proto-grpc"
                )

    # Add console exporter for debugging
    if console_export:
        readers.append(PeriodicExportingMetricReader(ConsoleMetricExporter()))

    return MeterProvider(resource=resource, metric_readers=readers)


def get_tracer(name: str = "blind_ai"):
    """Get a tracer instance.

    Args:
        name: Tracer name (default: "blind_ai")

    Returns:
        OpenTelemetry Tracer instance
    """
    try:
        from opentelemetry import trace
        return trace.get_tracer(name)
    except ImportError:
        return _NoOpTracer()


def get_meter(name: str = "blind_ai"):
    """Get a meter instance for metrics.

    Args:
        name: Meter name (default: "blind_ai")

    Returns:
        OpenTelemetry Meter instance
    """
    try:
        from opentelemetry import metrics
        return metrics.get_meter(name)
    except ImportError:
        return _NoOpMeter()


class _NoOpTracer:
    """No-op tracer when OpenTelemetry is not installed."""

    def start_span(self, name, **kwargs):
        return _NoOpSpan()

    def start_as_current_span(self, name, **kwargs):
        return _NoOpContextManager()


class _NoOpSpan:
    """No-op span."""

    def set_attribute(self, key, value):
        pass

    def set_status(self, status):
        pass

    def record_exception(self, exception):
        pass

    def end(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class _NoOpContextManager:
    """No-op context manager."""

    def __enter__(self):
        return _NoOpSpan()

    def __exit__(self, *args):
        pass


class _NoOpMeter:
    """No-op meter when OpenTelemetry is not installed."""

    def create_counter(self, name, **kwargs):
        return _NoOpCounter()

    def create_histogram(self, name, **kwargs):
        return _NoOpHistogram()

    def create_up_down_counter(self, name, **kwargs):
        return _NoOpCounter()


class _NoOpCounter:
    """No-op counter."""

    def add(self, value, attributes=None):
        pass


class _NoOpHistogram:
    """No-op histogram."""

    def record(self, value, attributes=None):
        pass
