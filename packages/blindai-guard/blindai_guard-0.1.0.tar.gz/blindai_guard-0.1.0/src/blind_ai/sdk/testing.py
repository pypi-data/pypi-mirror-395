"""Testing utilities for Blind AI SDK.

Provides mock mode, recording mode, and test fixtures for easy testing.
"""

import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Union

from .client import ProgressMetadata
from .exceptions import ThreatBlockedError
from .models import ProtectionResult

logger = logging.getLogger(__name__)


@dataclass
class MockConfig:
    """Configuration for mock mode behavior.
    
    Attributes:
        is_threat: Whether to report as threat
        threat_level: Threat level to return ("none", "low", "medium", "high", "critical")
        final_action: Action to take ("allow", "block", "challenge")
        threats_detected: List of threat types to report
        confidence: Confidence score (0.0 to 1.0)
        latency_ms: Simulated latency in milliseconds
        raise_error: If set, raise this exception instead of returning result
    """
    is_threat: bool = False
    threat_level: str = "none"
    final_action: str = "allow"
    threats_detected: List[str] = field(default_factory=list)
    confidence: float = 0.0
    latency_ms: float = 1.0
    raise_error: Optional[Exception] = None
    
    @classmethod
    def allow(cls) -> "MockConfig":
        """Create config that allows all requests."""
        return cls(is_threat=False, threat_level="none", final_action="allow")
    
    @classmethod
    def block(cls, threat_level: str = "high", threats: Optional[List[str]] = None) -> "MockConfig":
        """Create config that blocks all requests."""
        return cls(
            is_threat=True,
            threat_level=threat_level,
            final_action="block",
            threats_detected=threats or ["mock_threat"],
            confidence=0.95,
        )
    
    @classmethod
    def challenge(cls, threat_level: str = "medium") -> "MockConfig":
        """Create config that challenges all requests."""
        return cls(
            is_threat=True,
            threat_level=threat_level,
            final_action="challenge",
            threats_detected=["requires_review"],
            confidence=0.7,
        )


@dataclass
class RecordedCheck:
    """A recorded security check for replay/analysis.
    
    Attributes:
        timestamp: When the check occurred
        text: Input text that was checked
        context_id: Context ID if provided
        metadata: Metadata if provided
        user_id: User ID if provided
        result: The protection result
        latency_ms: How long the check took
    """
    timestamp: str
    text: str
    context_id: Optional[str]
    metadata: Optional[Dict[str, Any]]
    user_id: Optional[str]
    result: Dict[str, Any]
    latency_ms: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "timestamp": self.timestamp,
            "text": self.text,
            "context_id": self.context_id,
            "metadata": self.metadata,
            "user_id": self.user_id,
            "result": self.result,
            "latency_ms": self.latency_ms,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecordedCheck":
        """Create from dictionary."""
        return cls(
            timestamp=data["timestamp"],
            text=data["text"],
            context_id=data.get("context_id"),
            metadata=data.get("metadata"),
            user_id=data.get("user_id"),
            result=data["result"],
            latency_ms=data.get("latency_ms", 0.0),
        )


class MockGuard:
    """Mock guard for testing without making real API calls.
    
    Simulates ToolGuard behavior with configurable responses.
    
    Example:
        ```python
        from blind_ai.sdk.testing import MockGuard, MockConfig
        
        # Always allow
        guard = MockGuard()
        result = guard.check("SELECT * FROM users")
        assert not result.is_threat
        
        # Always block
        guard = MockGuard(MockConfig.block())
        try:
            guard.check("DROP TABLE users")
        except ThreatBlockedError:
            print("Blocked as expected!")
        
        # Custom behavior per input
        guard = MockGuard()
        guard.add_rule("DROP", MockConfig.block(threat_level="critical"))
        guard.add_rule("SELECT", MockConfig.allow())
        ```
    """
    
    def __init__(
        self,
        default_config: Optional[MockConfig] = None,
        rules: Optional[Dict[str, MockConfig]] = None,
    ):
        """Initialize mock guard.
        
        Args:
            default_config: Default mock configuration
            rules: Dictionary mapping text patterns to configs
        """
        self.default_config = default_config or MockConfig.allow()
        self.rules: Dict[str, MockConfig] = rules or {}
        self.call_history: List[Dict[str, Any]] = []
    
    def add_rule(self, pattern: str, config: MockConfig) -> None:
        """Add a rule for specific text patterns.
        
        Args:
            pattern: Text pattern to match (case-insensitive substring)
            config: MockConfig to use when pattern matches
        """
        self.rules[pattern.lower()] = config
    
    def clear_rules(self) -> None:
        """Clear all rules."""
        self.rules.clear()
    
    def clear_history(self) -> None:
        """Clear call history."""
        self.call_history.clear()
    
    def _get_config(self, text: str) -> MockConfig:
        """Get config for given text, checking rules first."""
        text_lower = text.lower()
        for pattern, config in self.rules.items():
            if pattern in text_lower:
                return config
        return self.default_config
    
    def check(
        self,
        text: str,
        context_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        user: Optional[Any] = None,
    ) -> ProtectionResult:
        """Mock check that returns configured result.
        
        Args:
            text: Text to check
            context_id: Optional context ID
            metadata: Optional metadata
            user: Optional user context
            
        Returns:
            Configured ProtectionResult
            
        Raises:
            ThreatBlockedError: If configured to block
            Exception: If raise_error is set in config
        """
        config = self._get_config(text)
        
        # Record the call
        self.call_history.append({
            "text": text,
            "context_id": context_id,
            "metadata": metadata,
            "user_id": user.user_id if user and hasattr(user, 'user_id') else None,
            "config_used": config,
            "timestamp": datetime.utcnow().isoformat(),
        })
        
        # Simulate latency
        if config.latency_ms > 0:
            time.sleep(config.latency_ms / 1000)
        
        # Raise error if configured
        if config.raise_error:
            raise config.raise_error
        
        # Build result
        result = ProtectionResult(
            is_threat=config.is_threat,
            threat_level=config.threat_level,
            final_action=config.final_action,
            threats_detected=config.threats_detected,
            confidence=config.confidence,
            processing_time_ms=config.latency_ms,
            metadata={"mock": True},
        )
        
        # Raise if blocking
        if config.final_action == "block":
            raise ThreatBlockedError(
                message=f"Mock blocked: {config.threat_level}",
                threat_level=config.threat_level,
                threats=config.threats_detected,
                response={"mock": True},
            )
        
        return result
    
    def check_batch(
        self,
        items: List[Dict[str, Any]],
        fail_fast: bool = False,
        parallel: bool = True,
        on_progress: Optional[Callable] = None,
    ) -> List[ProtectionResult]:
        """Mock batch check with progress metadata support.
        
        Args:
            items: List of check items
            fail_fast: Stop on first threat
            parallel: Ignored in mock
            on_progress: Optional progress callback. Can be:
                - Simple: func(completed, total)
                - With metadata: func(completed, total, metadata)
            
        Returns:
            List of ProtectionResults
        """
        import inspect
        
        results = []
        total = len(items)
        threats_detected = 0
        blocked_count = 0
        total_latency_ms = 0.0
        errors_count = 0
        
        # Check if callback accepts metadata
        accepts_metadata = False
        if on_progress:
            try:
                sig = inspect.signature(on_progress)
                accepts_metadata = len(sig.parameters) >= 3
            except (ValueError, TypeError):
                pass
        
        for i, item in enumerate(items):
            item_start = time.time()
            try:
                result = self.check(
                    text=item["text"],
                    context_id=item.get("context_id"),
                    metadata=item.get("metadata"),
                    user=item.get("user"),
                )
                results.append(result)
                
                if result.is_threat:
                    threats_detected += 1
                    
            except ThreatBlockedError as e:
                blocked_count += 1
                threats_detected += 1
                if fail_fast:
                    raise
                # For non-fail-fast, we still need to record it somehow
                results.append(ProtectionResult(
                    is_threat=True,
                    threat_level=e.threat_level,
                    final_action="block",
                    threats_detected=e.threats,
                    confidence=0.95,
                    processing_time_ms=0,
                    metadata={"mock": True, "blocked": True},
                ))
            
            item_latency = (time.time() - item_start) * 1000
            total_latency_ms += item_latency
            completed = i + 1
            
            # Report progress
            if on_progress:
                if accepts_metadata:
                    text = item.get("text", "")
                    preview = text[:50] + "..." if len(text) > 50 else text
                    metadata = ProgressMetadata(
                        threats_detected=threats_detected,
                        blocked_count=blocked_count,
                        avg_latency_ms=total_latency_ms / completed,
                        total_latency_ms=total_latency_ms,
                        current_item_preview=preview,
                        current_index=i,
                        errors_count=errors_count,
                    )
                    on_progress(completed, total, metadata)
                else:
                    on_progress(completed, total)
        
        return results
    
    def assert_called(self, times: Optional[int] = None) -> None:
        """Assert that check was called.
        
        Args:
            times: If provided, assert exact number of calls
        """
        if times is not None:
            assert len(self.call_history) == times, \
                f"Expected {times} calls, got {len(self.call_history)}"
        else:
            assert len(self.call_history) > 0, "Expected at least one call"
    
    def assert_called_with(self, text: str) -> None:
        """Assert that check was called with specific text.
        
        Args:
            text: Text to look for in call history
        """
        texts = [call["text"] for call in self.call_history]
        assert text in texts, f"Expected call with '{text}', got: {texts}"
    
    def assert_not_called(self) -> None:
        """Assert that check was never called."""
        assert len(self.call_history) == 0, \
            f"Expected no calls, got {len(self.call_history)}"


class RecordingGuard:
    """Guard wrapper that records all checks for later analysis.
    
    Wraps a real guard and records all inputs and outputs.
    
    Example:
        ```python
        from blind_ai.sdk import ToolGuard
        from blind_ai.sdk.testing import RecordingGuard
        
        # Wrap real guard with recording
        real_guard = ToolGuard(base_url="http://localhost:8000")
        guard = RecordingGuard(real_guard)
        
        # Use normally
        guard.check("SELECT * FROM users")
        guard.check("DROP TABLE users")
        
        # Export recordings
        guard.export_recordings("test_cases.json")
        
        # Or get recordings directly
        for recording in guard.recordings:
            print(f"{recording.text} -> {recording.result['final_action']}")
        ```
    """
    
    def __init__(self, guard: Any):
        """Initialize recording guard.
        
        Args:
            guard: The underlying guard to wrap (ToolGuard or AsyncToolGuard)
        """
        self.guard = guard
        self.recordings: List[RecordedCheck] = []
    
    def check(
        self,
        text: str,
        context_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        user: Optional[Any] = None,
    ) -> ProtectionResult:
        """Check with recording.
        
        Args:
            text: Text to check
            context_id: Optional context ID
            metadata: Optional metadata
            user: Optional user context
            
        Returns:
            ProtectionResult from underlying guard
        """
        start_time = time.perf_counter()
        result = None
        error = None
        
        try:
            result = self.guard.check(
                text=text,
                context_id=context_id,
                metadata=metadata,
                user=user,
            )
            return result
        except ThreatBlockedError as e:
            error = e
            # Create result from error for recording
            result = ProtectionResult(
                is_threat=True,
                threat_level=e.threat_level,
                final_action="block",
                threats_detected=e.threats,
                confidence=0.95,
                processing_time_ms=0,
                metadata={"blocked": True},
            )
            raise
        finally:
            latency_ms = (time.perf_counter() - start_time) * 1000
            
            # Record the check
            if result:
                self.recordings.append(RecordedCheck(
                    timestamp=datetime.utcnow().isoformat(),
                    text=text,
                    context_id=context_id,
                    metadata=metadata,
                    user_id=user.user_id if user and hasattr(user, 'user_id') else None,
                    result={
                        "is_threat": result.is_threat,
                        "threat_level": result.threat_level,
                        "final_action": result.final_action,
                        "threats_detected": result.threats_detected,
                        "confidence": result.confidence,
                    },
                    latency_ms=latency_ms,
                ))
    
    def check_batch(
        self,
        items: List[Dict[str, Any]],
        fail_fast: bool = False,
        parallel: bool = True,
    ) -> List[ProtectionResult]:
        """Batch check with recording.
        
        Args:
            items: List of check items
            fail_fast: Stop on first threat
            parallel: Use parallel execution
            
        Returns:
            List of ProtectionResults
        """
        # Record each item individually for detailed tracking
        results = []
        for item in items:
            try:
                result = self.check(
                    text=item["text"],
                    context_id=item.get("context_id"),
                    metadata=item.get("metadata"),
                    user=item.get("user"),
                )
                results.append(result)
            except ThreatBlockedError as e:
                if fail_fast:
                    raise
                results.append(ProtectionResult(
                    is_threat=True,
                    threat_level=e.threat_level,
                    final_action="block",
                    threats_detected=e.threats,
                    confidence=0.95,
                    processing_time_ms=0,
                    metadata={"blocked": True},
                ))
        return results
    
    def export_recordings(self, filepath: str) -> None:
        """Export recordings to JSON file.
        
        Args:
            filepath: Path to output file
        """
        data = {
            "exported_at": datetime.utcnow().isoformat(),
            "total_checks": len(self.recordings),
            "recordings": [r.to_dict() for r in self.recordings],
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Exported {len(self.recordings)} recordings to {filepath}")
    
    def import_recordings(self, filepath: str) -> None:
        """Import recordings from JSON file.
        
        Args:
            filepath: Path to input file
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.recordings = [
            RecordedCheck.from_dict(r)
            for r in data.get("recordings", [])
        ]
        
        logger.info(f"Imported {len(self.recordings)} recordings from {filepath}")
    
    def clear_recordings(self) -> None:
        """Clear all recordings."""
        self.recordings.clear()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of recordings.
        
        Returns:
            Dictionary with recording statistics
        """
        if not self.recordings:
            return {"total": 0}
        
        threats = [r for r in self.recordings if r.result.get("is_threat")]
        blocked = [r for r in self.recordings if r.result.get("final_action") == "block"]
        
        latencies = [r.latency_ms for r in self.recordings]
        
        return {
            "total": len(self.recordings),
            "threats_detected": len(threats),
            "blocked": len(blocked),
            "allowed": len(self.recordings) - len(blocked),
            "latency_avg_ms": sum(latencies) / len(latencies),
            "latency_max_ms": max(latencies),
            "latency_min_ms": min(latencies),
            "threat_levels": {
                level: sum(1 for r in self.recordings if r.result.get("threat_level") == level)
                for level in ["none", "low", "medium", "high", "critical"]
            },
        }
    
    # Delegate other attributes to underlying guard
    def __getattr__(self, name: str) -> Any:
        return getattr(self.guard, name)


class ReplayGuard:
    """Guard that replays recorded checks for deterministic testing.
    
    Uses previously recorded checks to provide deterministic responses.
    
    Example:
        ```python
        from blind_ai.sdk.testing import ReplayGuard
        
        # Load recordings and replay
        guard = ReplayGuard.from_file("test_cases.json")
        
        # Checks return recorded results
        result = guard.check("SELECT * FROM users")
        ```
    """
    
    def __init__(self, recordings: List[RecordedCheck]):
        """Initialize replay guard.
        
        Args:
            recordings: List of recorded checks to replay
        """
        self.recordings = recordings
        self._index = 0
        self._by_text: Dict[str, RecordedCheck] = {
            r.text: r for r in recordings
        }
    
    @classmethod
    def from_file(cls, filepath: str) -> "ReplayGuard":
        """Create replay guard from recording file.
        
        Args:
            filepath: Path to recordings JSON file
            
        Returns:
            ReplayGuard instance
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        recordings = [
            RecordedCheck.from_dict(r)
            for r in data.get("recordings", [])
        ]
        
        return cls(recordings)
    
    def check(
        self,
        text: str,
        context_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        user: Optional[Any] = None,
    ) -> ProtectionResult:
        """Replay recorded check result.
        
        First tries to match by exact text, then falls back to sequential replay.
        
        Args:
            text: Text to check
            context_id: Ignored
            metadata: Ignored
            user: Ignored
            
        Returns:
            Recorded ProtectionResult
        """
        # Try exact text match first
        if text in self._by_text:
            recording = self._by_text[text]
        elif self._index < len(self.recordings):
            # Fall back to sequential
            recording = self.recordings[self._index]
            self._index += 1
        else:
            # No more recordings, return safe default
            return ProtectionResult(
                is_threat=False,
                threat_level="none",
                final_action="allow",
                threats_detected=[],
                confidence=0.0,
                processing_time_ms=0,
                metadata={"replay": True, "no_recording": True},
            )
        
        result = ProtectionResult(
            is_threat=recording.result.get("is_threat", False),
            threat_level=recording.result.get("threat_level", "none"),
            final_action=recording.result.get("final_action", "allow"),
            threats_detected=recording.result.get("threats_detected", []),
            confidence=recording.result.get("confidence", 0.0),
            processing_time_ms=recording.latency_ms,
            metadata={"replay": True},
        )
        
        # Raise if blocked
        if result.final_action == "block":
            raise ThreatBlockedError(
                message=f"Replay blocked: {result.threat_level}",
                threat_level=result.threat_level,
                threats=result.threats_detected,
                response={"replay": True},
            )
        
        return result
    
    def reset(self) -> None:
        """Reset replay index to beginning."""
        self._index = 0


# Convenience function to create test guard
def create_test_guard(
    mode: str = "mock",
    mock_config: Optional[MockConfig] = None,
    recordings_file: Optional[str] = None,
    real_guard: Optional[Any] = None,
) -> Union[MockGuard, RecordingGuard, ReplayGuard]:
    """Create a test guard with specified mode.
    
    Args:
        mode: Test mode - "mock", "record", or "replay"
        mock_config: Configuration for mock mode
        recordings_file: File path for replay mode
        real_guard: Real guard for recording mode
        
    Returns:
        Appropriate test guard instance
        
    Example:
        ```python
        from blind_ai.sdk.testing import create_test_guard, MockConfig
        
        # Mock mode
        guard = create_test_guard("mock", mock_config=MockConfig.block())
        
        # Recording mode
        real_guard = ToolGuard(base_url="http://localhost:8000")
        guard = create_test_guard("record", real_guard=real_guard)
        
        # Replay mode
        guard = create_test_guard("replay", recordings_file="tests.json")
        ```
    """
    if mode == "mock":
        return MockGuard(default_config=mock_config)
    elif mode == "record":
        if real_guard is None:
            raise ValueError("real_guard required for record mode")
        return RecordingGuard(real_guard)
    elif mode == "replay":
        if recordings_file is None:
            raise ValueError("recordings_file required for replay mode")
        return ReplayGuard.from_file(recordings_file)
    else:
        raise ValueError(f"Unknown mode: {mode}")
