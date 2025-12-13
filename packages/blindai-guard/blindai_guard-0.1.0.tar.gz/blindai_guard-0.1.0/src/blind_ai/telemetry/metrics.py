"""Metrics collection for Blind AI.

Provides pre-defined metrics for monitoring Blind AI performance and security.
"""

from typing import Optional, Dict, Any
from .setup import get_meter


class BlindAIMetrics:
    """Pre-configured metrics for Blind AI monitoring.

    Provides standard metrics for:
    - Request counts (by action: allow/block/challenge)
    - Latency histograms
    - Threat detection counts (by type)
    - Error counts

    Example:
        ```python
        from blind_ai.telemetry import BlindAIMetrics

        metrics = BlindAIMetrics()

        # Record a blocked request
        metrics.record_request(
            action="block",
            threat_type="sql_injection",
            latency_ms=15.5,
        )

        # Record an error
        metrics.record_error("timeout")
        ```
    """

    def __init__(self, meter_name: str = "blind_ai"):
        """Initialize metrics.

        Args:
            meter_name: Name for the meter (default: "blind_ai")
        """
        self._meter = get_meter(meter_name)
        self._initialized = False
        self._counters = {}
        self._histograms = {}
        self._init_metrics()

    def _init_metrics(self) -> None:
        """Initialize all metric instruments."""
        # Request counter - counts all protection checks
        self._counters["requests"] = self._meter.create_counter(
            name="blind_ai.requests",
            description="Total number of protection requests",
            unit="1",
        )

        # Threat counter - counts detected threats by type
        self._counters["threats"] = self._meter.create_counter(
            name="blind_ai.threats_detected",
            description="Number of threats detected by type",
            unit="1",
        )

        # Block counter - counts blocked requests
        self._counters["blocks"] = self._meter.create_counter(
            name="blind_ai.requests_blocked",
            description="Number of requests blocked",
            unit="1",
        )

        # Challenge counter - counts challenged requests
        self._counters["challenges"] = self._meter.create_counter(
            name="blind_ai.requests_challenged",
            description="Number of requests requiring challenge",
            unit="1",
        )

        # Error counter
        self._counters["errors"] = self._meter.create_counter(
            name="blind_ai.errors",
            description="Number of errors encountered",
            unit="1",
        )

        # Latency histogram
        self._histograms["latency"] = self._meter.create_histogram(
            name="blind_ai.request_latency",
            description="Request processing latency",
            unit="ms",
        )

        # Detection latency by layer
        self._histograms["static_latency"] = self._meter.create_histogram(
            name="blind_ai.static_detection_latency",
            description="Static detection layer latency",
            unit="ms",
        )

        self._histograms["ml_latency"] = self._meter.create_histogram(
            name="blind_ai.ml_detection_latency",
            description="ML detection layer latency",
            unit="ms",
        )

        self._initialized = True

    def record_request(
        self,
        action: str,
        latency_ms: float,
        threat_type: Optional[str] = None,
        threat_level: Optional[str] = None,
        tool_name: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> None:
        """Record a protection request.

        Args:
            action: Action taken (allow, block, challenge, log)
            latency_ms: Total processing latency in milliseconds
            threat_type: Type of threat detected (if any)
            threat_level: Severity level (none, low, medium, high, critical)
            tool_name: Name of the tool being protected
            user_id: User ID (for per-user metrics)
        """
        # Base attributes
        attrs = {
            "action": action,
            "threat_level": threat_level or "none",
        }
        if tool_name:
            attrs["tool_name"] = tool_name
        if user_id:
            attrs["user_id"] = user_id

        # Count request
        self._counters["requests"].add(1, attrs)

        # Record latency
        self._histograms["latency"].record(latency_ms, attrs)

        # Count by action type
        if action == "block":
            self._counters["blocks"].add(1, attrs)
        elif action == "challenge":
            self._counters["challenges"].add(1, attrs)

        # Count threat if detected
        if threat_type:
            threat_attrs = {**attrs, "threat_type": threat_type}
            self._counters["threats"].add(1, threat_attrs)

    def record_detection_latency(
        self,
        layer: str,
        latency_ms: float,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record detection layer latency.

        Args:
            layer: Detection layer (static, ml, policy)
            latency_ms: Layer processing latency in milliseconds
            attributes: Additional attributes
        """
        attrs = attributes or {}
        attrs["layer"] = layer

        if layer == "static":
            self._histograms["static_latency"].record(latency_ms, attrs)
        elif layer == "ml":
            self._histograms["ml_latency"].record(latency_ms, attrs)

    def record_error(
        self,
        error_type: str,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record an error.

        Args:
            error_type: Type of error (timeout, api_error, validation, etc.)
            attributes: Additional attributes
        """
        attrs = {"error_type": error_type}
        if attributes:
            attrs.update(attributes)

        self._counters["errors"].add(1, attrs)

    def record_threat(
        self,
        threat_type: str,
        severity: str,
        source: str = "unknown",
        attributes: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record a detected threat.

        Args:
            threat_type: Type of threat (sql_injection, prompt_injection, pii)
            severity: Severity level (low, medium, high, critical)
            source: Detection source (static, ml, policy)
            attributes: Additional attributes
        """
        attrs = {
            "threat_type": threat_type,
            "severity": severity,
            "source": source,
        }
        if attributes:
            attrs.update(attributes)

        self._counters["threats"].add(1, attrs)


# Global metrics instance for convenience
_global_metrics: Optional[BlindAIMetrics] = None


def get_metrics() -> BlindAIMetrics:
    """Get global metrics instance.

    Returns:
        BlindAIMetrics instance (creates one if needed)
    """
    global _global_metrics
    if _global_metrics is None:
        _global_metrics = BlindAIMetrics()
    return _global_metrics
