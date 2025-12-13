"""Data models for Blind AI SDK."""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ProtectionResult:
    """Result from protection check.

    Attributes:
        is_threat: Whether a threat was detected
        threat_level: Threat severity level
        final_action: Recommended action (allow, log, challenge, block)
        confidence: Detection confidence (0.0 to 1.0)
        threats_detected: List of specific threats
        processing_time_ms: Processing time in milliseconds
        metadata: Additional metadata
    """

    is_threat: bool
    threat_level: str
    final_action: str
    confidence: float
    threats_detected: list[dict[str, Any]] = field(default_factory=list)
    processing_time_ms: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api_response(cls, response: dict) -> "ProtectionResult":
        """Create ProtectionResult from API response.

        Args:
            response: API response dictionary

        Returns:
            ProtectionResult instance
        """
        return cls(
            is_threat=response["is_threat"],
            threat_level=response["threat_level"],
            final_action=response["final_action"],
            confidence=response["confidence"],
            threats_detected=response.get("threats_detected", []),
            processing_time_ms=response.get("processing_time_ms", 0.0),
            metadata=response.get("metadata", {}),
        )


@dataclass
class SDKConfig:
    """Configuration for Blind AI SDK.

    Attributes:
        api_key: API key for authentication
        base_url: Base URL for API
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
        retry_backoff: Backoff multiplier for retries
        fail_open: Allow on error (True) or block on error (False)
        verify_ssl: Verify SSL certificates
    """

    api_key: Optional[str] = None
    base_url: str = "http://localhost:8000"
    timeout: float = 10.0
    max_retries: int = 3
    retry_backoff: float = 0.5
    fail_open: bool = False
    verify_ssl: bool = True

    def __post_init__(self):
        """Validate configuration."""
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.retry_backoff < 0:
            raise ValueError("retry_backoff must be non-negative")
