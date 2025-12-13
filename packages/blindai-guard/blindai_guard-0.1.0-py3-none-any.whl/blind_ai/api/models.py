"""Pydantic models for API requests and responses."""

from typing import Any, Optional

from pydantic import BaseModel, Field


class ProtectRequest(BaseModel):
    """Request to /v1/protect endpoint.

    Attributes:
        text: Text to analyze for threats
        context_id: Optional context ID for multi-turn tracking
        metadata: Optional metadata about the request
    """

    text: str = Field(..., min_length=1, description="Text to analyze")
    context_id: Optional[str] = Field(None, description="Context ID for multi-turn tracking")
    metadata: Optional[dict[str, Any]] = Field(default_factory=dict, description="Request metadata")


class ThreatDetail(BaseModel):
    """Details about a detected threat.

    Attributes:
        source: Detection source (static, ml, policy)
        type: Threat type (sql_injection, prompt_injection, etc.)
        pattern: Pattern name that matched (for static detections)
        severity: Threat severity
        confidence: Detection confidence
        description: Human-readable description
    """

    source: str = Field(..., description="Detection source")
    type: str = Field(..., description="Threat type")
    pattern: Optional[str] = Field(None, description="Pattern name")
    severity: Optional[str] = Field(None, description="Threat severity")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    description: Optional[str] = Field(None, description="Threat description")


class ProtectResponse(BaseModel):
    """Response from /v1/protect endpoint.

    Attributes:
        is_threat: Whether a threat was detected
        threat_level: Overall threat level (none, low, medium, high, critical)
        final_action: Recommended action (allow, log, challenge, block)
        confidence: Overall confidence score (0.0 to 1.0)
        threats_detected: List of specific threats detected
        processing_time_ms: Processing time in milliseconds
        metadata: Additional response metadata
    """

    is_threat: bool = Field(..., description="Whether threat was detected")
    threat_level: str = Field(..., description="Threat level")
    final_action: str = Field(..., description="Recommended action")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    threats_detected: list[ThreatDetail] = Field(default_factory=list, description="Detected threats")
    processing_time_ms: float = Field(..., description="Processing time in ms")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Response metadata")


class HealthResponse(BaseModel):
    """Response from /health endpoint.

    Attributes:
        status: Health status
        version: API version
        uptime_seconds: Uptime in seconds
    """

    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")
    uptime_seconds: float = Field(..., description="Uptime in seconds")


class ErrorResponse(BaseModel):
    """Error response model.

    Attributes:
        error: Error type
        message: Error message
        detail: Additional error details
    """

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[dict[str, Any]] = Field(None, description="Additional details")
