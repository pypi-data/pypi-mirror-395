"""Telemetry and observability for Blind AI.

Provides OpenTelemetry integration for distributed tracing and metrics.

Example:
    ```python
    from blind_ai import ToolGuard
    from blind_ai.telemetry import setup_telemetry, BlindAIInstrumentor

    # Setup OpenTelemetry with OTLP exporter
    setup_telemetry(
        service_name="my-ai-agent",
        otlp_endpoint="http://localhost:4317",
    )

    # Instrument the SDK
    BlindAIInstrumentor().instrument()

    # Now all ToolGuard operations are traced
    guard = ToolGuard(api_key="...")
    guard.check("SELECT * FROM users")  # Automatically traced
    ```
"""

from .instrumentor import BlindAIInstrumentor
from .setup import setup_telemetry
from .metrics import BlindAIMetrics

__all__ = [
    "BlindAIInstrumentor",
    "setup_telemetry",
    "BlindAIMetrics",
]
