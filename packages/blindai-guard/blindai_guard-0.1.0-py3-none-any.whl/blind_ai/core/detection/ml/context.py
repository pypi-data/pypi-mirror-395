"""Conversation context tracking for multi-turn attack detection.

Tracks conversation history, user behavior patterns, and temporal analysis
to detect sophisticated multi-turn attacks.
"""

import time
from dataclasses import dataclass, field


# Memory bounds to prevent unbounded growth
MAX_MESSAGE_HISTORY = 100  # Maximum messages to retain per session
MAX_BEHAVIOR_HISTORY = 50  # Maximum entries in behavior tracking lists


@dataclass
class ConversationContext:
    """Track conversation history and behavioral patterns.

    Attributes:
        messages: List of message dictionaries with metadata (max MAX_MESSAGE_HISTORY)
        user_behavior: Behavioral metrics (response time, message length, suspicion)
        session_start: Timestamp when session started
        turn_count: Number of turns in conversation
    """

    messages: list[dict] = field(default_factory=list)
    user_behavior: dict = field(
        default_factory=lambda: {
            "avg_response_time": 0.0,
            "message_lengths": [],
            "suspicion_trend": [],
        }
    )
    session_start: float = field(default_factory=time.time)
    turn_count: int = 0

    def add_message(
        self, text: str, suspicious: bool = False, suspicion_score: float = 0.0
    ) -> None:
        """Add a message to conversation history with metadata.

        Enforces memory bounds by trimming oldest entries when limits exceeded.

        Args:
            text: Message text
            suspicious: Whether message was flagged as suspicious
            suspicion_score: Numerical suspicion score (0.0 to 1.0)
        """
        self.messages.append(
            {
                "text": text,
                "timestamp": time.time(),
                "suspicious": suspicious,
                "suspicion_score": suspicion_score,
            }
        )
        self.turn_count += 1
        self.user_behavior["message_lengths"].append(len(text))
        self.user_behavior["suspicion_trend"].append(suspicion_score)
        
        # Enforce memory bounds - trim oldest entries
        if len(self.messages) > MAX_MESSAGE_HISTORY:
            self.messages = self.messages[-MAX_MESSAGE_HISTORY:]
        
        if len(self.user_behavior["message_lengths"]) > MAX_BEHAVIOR_HISTORY:
            self.user_behavior["message_lengths"] = \
                self.user_behavior["message_lengths"][-MAX_BEHAVIOR_HISTORY:]
        
        if len(self.user_behavior["suspicion_trend"]) > MAX_BEHAVIOR_HISTORY:
            self.user_behavior["suspicion_trend"] = \
                self.user_behavior["suspicion_trend"][-MAX_BEHAVIOR_HISTORY:]

    def analyze_behavioral_patterns(self) -> dict:
        """Analyze user behavior for attack indicators.

        Detects:
        - Rapid-fire messages (DoS-like behavior)
        - Escalating suspicion (gradual attack buildup)
        - Unusual message patterns

        Returns:
            Dictionary with risk scores:
                - rapid_fire_risk: Messages sent too quickly
                - escalation_risk: Suspicion increasing over time
                - total_risk: Overall behavioral risk
        """
        if len(self.messages) < 3:
            return {
                "total_risk": 0.0,
                "rapid_fire_risk": 0.0,
                "escalation_risk": 0.0,
            }

        # Rapid-fire detection (DoS-like behavior) with gradient scoring
        recent_messages = self.messages[-3:]
        time_gaps = [
            recent_messages[i + 1]["timestamp"] - recent_messages[i]["timestamp"]
            for i in range(len(recent_messages) - 1)
        ]

        avg_gap = sum(time_gaps) / len(time_gaps) if time_gaps else float("inf")
        # Gradient scoring: sub-second = 1.0, 1-5 seconds = 0.3-0.8, >5 seconds = 0.0
        if avg_gap < 0.5:
            rapid_fire_risk = 1.0
        elif avg_gap < 1.0:
            rapid_fire_risk = 0.8
        elif avg_gap < 2.0:
            rapid_fire_risk = 0.5
        elif avg_gap < 5.0:
            rapid_fire_risk = 0.3
        else:
            rapid_fire_risk = 0.0

        # Escalation pattern detection (increasingly aggressive) with magnitude check
        suspicion_scores = [
            msg.get("suspicion_score", 0) for msg in self.messages[-5:]
        ]

        if len(suspicion_scores) >= 3:
            # Calculate actual increase magnitude, not just monotonicity
            # Require strictly increasing (>) and meaningful delta
            increases = [
                suspicion_scores[i + 1] - suspicion_scores[i]
                for i in range(len(suspicion_scores) - 1)
            ]
            # Check for strictly increasing with minimum delta of 0.05
            strictly_increasing = all(delta > 0.05 for delta in increases)
            total_increase = suspicion_scores[-1] - suspicion_scores[0]
            
            if strictly_increasing and total_increase > 0.2:
                # Scale risk by how much the score actually increased
                escalation_risk = min(0.8, total_increase * 1.5)
            else:
                escalation_risk = 0.0
        else:
            escalation_risk = 0.0

        # Calculate total risk
        total_risk = max(rapid_fire_risk, escalation_risk)

        return {
            "rapid_fire_risk": rapid_fire_risk,
            "escalation_risk": escalation_risk,
            "total_risk": total_risk,
        }

    def detect_multi_turn_attack(self, current_text: str) -> float:
        """Detect multi-turn attack patterns.

        Looks for:
        - Continuation markers ("as I said", "remember")
        - Building attack across multiple turns
        - Gradual escalation

        Args:
            current_text: Current message text

        Returns:
            Risk score from 0.0 to 1.0
        """
        risk_score = 0.0

        if self.turn_count <= 1:
            return 0.0

        # Check for continuation patterns
        continuation_markers = [
            r"\b(continue|as I said|remember|earlier)\b",
            r"\b(from before|previously|like I mentioned)\b",
        ]

        for pattern in continuation_markers:
            import re

            if re.search(pattern, current_text, re.IGNORECASE):
                risk_score += 0.2
                break

        # Check if previous messages had suspicious patterns
        suspicious_count = sum(1 for msg in self.messages if msg.get("suspicious", False))
        if suspicious_count > 0:
            risk_score += 0.3

        # Check for gradual escalation
        if self.turn_count >= 3 and suspicious_count >= 2:
            risk_score += 0.4

        return min(1.0, risk_score)

    def get_recent_messages(self, count: int = 5) -> list[dict]:
        """Get most recent messages.

        Args:
            count: Number of recent messages to retrieve

        Returns:
            List of recent message dictionaries
        """
        return self.messages[-count:]

    def get_suspicion_trend(self, window: int = 5) -> list[float]:
        """Get recent suspicion score trend.

        Args:
            window: Number of recent scores to include

        Returns:
            List of recent suspicion scores
        """
        return self.user_behavior["suspicion_trend"][-window:]

    def is_escalating(self, threshold: float = 0.1) -> bool:
        """Check if suspicion is escalating.

        Args:
            threshold: Minimum increase to consider escalation

        Returns:
            True if suspicion is increasing significantly
        """
        trend = self.get_suspicion_trend()
        if len(trend) < 3:
            return False

        # Check if recent scores show upward trend
        differences = [trend[i + 1] - trend[i] for i in range(len(trend) - 1)]
        avg_increase = sum(differences) / len(differences)

        return avg_increase > threshold

    def reset(self) -> None:
        """Reset conversation context to initial state."""
        self.messages.clear()
        self.user_behavior = {
            "avg_response_time": 0.0,
            "message_lengths": [],
            "suspicion_trend": [],
        }
        self.session_start = time.time()
        self.turn_count = 0

    def get_session_duration(self) -> float:
        """Get duration of current session in seconds.

        Returns:
            Session duration in seconds
        """
        return time.time() - self.session_start

    def get_average_message_length(self) -> float:
        """Get average message length across session.

        Returns:
            Average message length in characters
        """
        lengths = self.user_behavior["message_lengths"]
        return sum(lengths) / len(lengths) if lengths else 0.0

    def get_suspicious_message_count(self) -> int:
        """Get count of messages flagged as suspicious.

        Returns:
            Number of suspicious messages
        """
        return sum(1 for msg in self.messages if msg.get("suspicious", False))
