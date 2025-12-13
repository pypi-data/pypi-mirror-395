"""Protection endpoint for threat detection."""

from fastapi import APIRouter, Depends, HTTPException, status

from ...core.models import DetectionRequest
from ..auth import verify_api_key
from ..models import ProtectRequest, ProtectResponse, ThreatDetail

router = APIRouter()


@router.post("/protect", response_model=ProtectResponse, status_code=status.HTTP_200_OK)
async def protect_endpoint(
    request: ProtectRequest,
    api_key: str = Depends(verify_api_key),
):
    """Detect threats in text input.

    Analyzes the provided text using multi-layer detection (static patterns,
    ML-based detection, and policy evaluation) to identify potential threats.

    Args:
        request: Protection request with text to analyze

    Returns:
        Detection response with threat assessment and recommended action

    Raises:
        HTTPException: If detection service unavailable or error occurs

    Example:
        ```json
        POST /v1/protect
        {
            "text": "DROP TABLE users; --",
            "context_id": "session-123"
        }
        ```

        Response:
        ```json
        {
            "is_threat": true,
            "threat_level": "critical",
            "final_action": "block",
            "confidence": 0.95,
            "threats_detected": [
                {
                    "source": "static",
                    "type": "sql_injection",
                    "pattern": "drop_table",
                    "severity": "critical",
                    "confidence": 0.95,
                    "description": "SQL injection attempt detected"
                }
            ],
            "processing_time_ms": 1.2
        }
        ```
    """
    # Import here to avoid circular dependency
    from ..app import get_orchestrator

    try:
        # Get orchestrator
        orchestrator = get_orchestrator()

        # Create detection request
        detection_request = DetectionRequest(
            text=request.text,
            context_id=request.context_id,
            metadata=request.metadata or {},
        )

        # Perform detection
        response = orchestrator.detect(detection_request)

        # Convert threats to API models
        threats = []
        for threat in response.threats_detected:
            threats.append(
                ThreatDetail(
                    source=threat.get("source", "unknown"),
                    type=threat.get("type", "unknown"),
                    pattern=threat.get("pattern"),
                    severity=threat.get("severity"),
                    confidence=threat.get("confidence", 0.0),
                    description=threat.get("description"),
                )
            )

        # Return response
        return ProtectResponse(
            is_threat=response.is_threat,
            threat_level=response.threat_level.value,
            final_action=response.final_action.value,
            confidence=response.confidence,
            threats_detected=threats,
            processing_time_ms=response.processing_time_ms,
            metadata=response.metadata,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Detection failed: {str(e)}",
        ) from e
