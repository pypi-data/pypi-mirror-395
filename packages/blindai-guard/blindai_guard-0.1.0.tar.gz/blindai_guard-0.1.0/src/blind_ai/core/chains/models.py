"""Tool chain models for tracking multi-tool sequences."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class ToolCall:
    """Record of a single tool execution.

    Attributes:
        tool_name: Name of tool executed
        parameters: Parameters passed to tool
        timestamp: When tool was called
        user_id: User who called the tool
        session_id: Session identifier
    """

    tool_name: str
    parameters: dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None
    session_id: Optional[str] = None


@dataclass
class ToolChain:
    """Sequence of tool calls in a session.

    Attributes:
        session_id: Session identifier
        calls: List of tool calls in order
        user_id: User making the calls
    """

    session_id: str
    calls: list[ToolCall] = field(default_factory=list)
    user_id: Optional[str] = None

    def add_call(self, call: ToolCall) -> None:
        """Add a tool call to the chain."""
        self.calls.append(call)

    def matches_pattern(self, pattern: "ChainPattern") -> bool:
        """Check if chain matches a pattern.
        
        Args:
            pattern: The pattern to match against
            
        Returns:
            True if the chain matches the pattern (including time window if specified)
        """
        if len(self.calls) < len(pattern.sequence):
            return False

        # Check last N calls match pattern
        recent_calls = self.calls[-len(pattern.sequence) :]
        for call, expected_tool in zip(recent_calls, pattern.sequence):
            if call.tool_name != expected_tool:
                return False

        # Check time window constraint if specified
        if pattern.window_seconds is not None:
            first_call = recent_calls[0]
            last_call = recent_calls[-1]
            elapsed = (last_call.timestamp - first_call.timestamp).total_seconds()
            if elapsed > pattern.window_seconds:
                return False

        return True

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "calls": [
                {
                    "tool_name": call.tool_name,
                    "parameters": call.parameters,
                    "timestamp": call.timestamp.isoformat(),
                    "user_id": call.user_id,
                    "session_id": call.session_id,
                }
                for call in self.calls
            ],
        }


@dataclass
class ChainPattern:
    """Pattern for detecting suspicious tool sequences.

    Attributes:
        name: Pattern name
        sequence: Ordered list of tool names
        description: What this pattern indicates
        severity: Risk level (low, medium, high, critical)
        window_seconds: Optional time window - pattern only matches if all calls
                       occur within this many seconds (None = no time limit)
    """

    name: str
    sequence: list[str]
    description: str
    severity: str = "medium"
    window_seconds: Optional[int] = None

    def __post_init__(self) -> None:
        """Validate pattern."""
        if not self.sequence or len(self.sequence) < 2:
            raise ValueError("Pattern must have at least 2 tools")
        if self.severity not in ("low", "medium", "high", "critical"):
            raise ValueError("Invalid severity level")
        if self.window_seconds is not None and self.window_seconds <= 0:
            raise ValueError("window_seconds must be positive")
