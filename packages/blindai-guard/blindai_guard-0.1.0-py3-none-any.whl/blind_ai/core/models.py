"""Data models for Blind AI detection system.

Defines request and response models for the detection pipeline.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


# Security limits to prevent DoS attacks
MAX_TEXT_LENGTH = 100_000  # 100KB max text size
MAX_CONTEXT_ID_LENGTH = 256  # Reasonable context ID length
MAX_METADATA_SIZE = 10_000  # 10KB max metadata size


class ThreatLevel(Enum):
    """Overall threat level assessment."""

    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FinalAction(Enum):
    """Final action recommendation."""

    ALLOW = "allow"
    LOG = "log"
    CHALLENGE = "challenge"
    BLOCK = "block"


class InputTooLargeError(ValueError):
    """Raised when input exceeds security limits."""
    pass


@dataclass
class DetectionRequest:
    """Request for threat detection.

    Attributes:
        text: Text to analyze (max 100KB)
        context_id: Optional context ID for multi-turn tracking (max 256 chars)
        metadata: Optional metadata about the request (max 10KB)
    """

    text: str
    context_id: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        """Validate input sizes to prevent DoS attacks."""
        if len(self.text) > MAX_TEXT_LENGTH:
            raise InputTooLargeError(
                f"Text exceeds maximum length of {MAX_TEXT_LENGTH} characters "
                f"(got {len(self.text)})"
            )
        
        if self.context_id and len(self.context_id) > MAX_CONTEXT_ID_LENGTH:
            raise InputTooLargeError(
                f"context_id exceeds maximum length of {MAX_CONTEXT_ID_LENGTH} "
                f"(got {len(self.context_id)})"
            )
        
        # Check metadata size (approximate)
        if self.metadata:
            import json
            try:
                metadata_str = json.dumps(self.metadata)
            except (TypeError, ValueError):
                # If metadata can't be serialized, allow but warn
                metadata_str = None
            
            if metadata_str and len(metadata_str) > MAX_METADATA_SIZE:
                raise InputTooLargeError(
                    f"metadata exceeds maximum size of {MAX_METADATA_SIZE} bytes "
                    f"(got {len(metadata_str)})"
                )


@dataclass
class DetectionResponse:
    """Response from threat detection pipeline.

    Attributes:
        is_threat: Whether a threat was detected
        threat_level: Overall threat level
        final_action: Recommended action
        confidence: Overall confidence score (0.0 to 1.0)
        threats_detected: List of specific threats detected
        static_results: Results from static detector
        ml_results: Results from ML detector
        policy_action: Action determined by policy engine
        processing_time_ms: Total processing time in milliseconds
        layers_executed: Which detection layers were executed
        metadata: Additional response metadata
    """

    is_threat: bool
    threat_level: ThreatLevel
    final_action: FinalAction
    confidence: float
    threats_detected: list[dict[str, Any]] = field(default_factory=list)
    static_results: dict[str, Any] = field(default_factory=dict)
    ml_results: dict[str, Any] = field(default_factory=dict)
    policy_action: str = "ALLOW"
    processing_time_ms: float = 0.0
    layers_executed: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert response to dictionary.

        Returns:
            Dictionary representation of response
        """
        return {
            "is_threat": self.is_threat,
            "threat_level": self.threat_level.value,
            "final_action": self.final_action.value,
            "confidence": self.confidence,
            "threats_detected": self.threats_detected,
            "static_results": self.static_results,
            "ml_results": self.ml_results,
            "policy_action": self.policy_action,
            "processing_time_ms": self.processing_time_ms,
            "layers_executed": self.layers_executed,
            "metadata": self.metadata,
        }


@dataclass
class OrchestrationConfig:
    """Configuration for detection orchestrator.

    Attributes:
        enable_static: Enable static pattern detection
        enable_ml: Enable ML-based detection
        enable_policy: Enable policy evaluation
        parallel_execution: Execute layers in parallel
        fail_open: Allow requests if detection fails
        timeout_ms: Maximum processing timeout in milliseconds
    """

    enable_static: bool = True
    enable_ml: bool = True
    enable_policy: bool = True
    parallel_execution: bool = True
    fail_open: bool = False
    timeout_ms: int = 50  # 50ms P95 target
