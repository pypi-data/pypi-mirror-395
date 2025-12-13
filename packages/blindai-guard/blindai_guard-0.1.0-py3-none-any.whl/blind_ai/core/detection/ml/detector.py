"""ML-based threat detector using ONNX inference.

This module provides machine learning enhanced detection using a DistilBERT
model exported to ONNX format for fast inference.

Note: ONNX model integration is planned for Week 2 Phase 2.
For now, this provides heuristic-based detection using the extracted features.
"""

from dataclasses import dataclass
from typing import Optional

from ..static import DetectionResult
from .cache import ResultCache
from .context import ConversationContext
from .heuristics import calculate_heuristic_score
from .preprocessing import deobfuscate_text, normalize_text


@dataclass
class MLDetectorWeights:
    """Configurable weights for ML detection scoring.

    Attributes:
        heuristic: Weight for heuristic analysis (default: 0.6)
        multi_turn: Weight for multi-turn attack risk (default: 0.25)
        behavioral: Weight for behavioral analysis (default: 0.15)
    """
    heuristic: float = 0.6
    multi_turn: float = 0.25
    behavioral: float = 0.15

    # Tolerance for weight sum validation (5%)
    WEIGHT_SUM_TOLERANCE: float = 0.05

    def __post_init__(self):
        """Validate weights sum to ~1.0 within tolerance."""
        total = self.heuristic + self.multi_turn + self.behavioral
        if abs(total - 1.0) > self.WEIGHT_SUM_TOLERANCE:
            raise ValueError(
                f"Weights must sum to 1.0 ± {self.WEIGHT_SUM_TOLERANCE}, got {total:.3f}"
            )
        # Ensure all weights are non-negative
        if any(w < 0 for w in [self.heuristic, self.multi_turn, self.behavioral]):
            raise ValueError("All weights must be non-negative")


class MLDetector:
    """ML-enhanced threat detector.

    Combines preprocessing, heuristic analysis, and context tracking.
    ONNX inference will be added in Phase 2.

    Attributes:
        cache: Result cache for expensive operations
        context: Conversation context tracker
        enable_caching: Whether to cache results
        heuristic_threshold: Threshold for heuristic-based detection
        weights: Configurable scoring weights
    """

    def __init__(
        self,
        enable_caching: bool = True,
        cache_size: int = 1000,
        heuristic_threshold: float = 0.7,
        weights: Optional[MLDetectorWeights] = None,
    ):
        """Initialize ML detector.

        Args:
            enable_caching: Enable result caching (default: True)
            cache_size: Maximum cache size (default: 1000)
            heuristic_threshold: Threshold for heuristic detection (default: 0.7)
            weights: Scoring weights configuration (default: MLDetectorWeights())
        """
        self.cache: Optional[ResultCache] = (
            ResultCache(max_size=cache_size) if enable_caching else None
        )
        self.context = ConversationContext()
        self.heuristic_threshold = heuristic_threshold
        self.enable_caching = enable_caching
        self.weights = weights or MLDetectorWeights()

    def detect(
        self, text: str, update_context: bool = True
    ) -> dict:
        """Detect threats using ML-enhanced analysis.

        Args:
            text: Text to analyze
            update_context: Whether to update conversation context

        Returns:
            Dictionary with detection results:
                - is_threat: Whether text is threatening
                - confidence: Confidence score (0.0 to 1.0)
                - heuristic_score: Heuristic analysis score
                - multi_turn_risk: Multi-turn attack risk
                - preprocessing: Preprocessing results
        """
        # Build cache context from conversation state
        cache_context = {
            "turn_count": self.context.turn_count,
            "update_context": update_context,
        }

        # Check cache first (with context awareness)
        if self.cache:
            cached = self.cache.get(text, context=cache_context)
            if cached is not None:
                return cached

        # Preprocessing
        normalized = normalize_text(text)
        deobfuscated = deobfuscate_text(text)

        # Heuristic analysis
        heuristic_score = calculate_heuristic_score(text)

        # Multi-turn risk assessment
        multi_turn_risk = self.context.detect_multi_turn_attack(text)

        # Behavioral analysis
        behavioral = self.context.analyze_behavioral_patterns()

        # Combined confidence score
        # TODO: Replace with ONNX model inference in Phase 2
        confidence = self._calculate_confidence(
            heuristic_score, multi_turn_risk, behavioral["total_risk"]
        )

        is_threat = confidence >= self.heuristic_threshold

        result = {
            "is_threat": is_threat,
            "confidence": confidence,
            "heuristic_score": heuristic_score,
            "multi_turn_risk": multi_turn_risk,
            "behavioral_risk": behavioral["total_risk"],
            "preprocessing": {
                "normalized": normalized,
                "deobfuscated": deobfuscated,
            },
        }

        # Update context
        if update_context:
            self.context.add_message(
                text, suspicious=is_threat, suspicion_score=confidence
            )

        # Cache result (with context awareness)
        if self.cache:
            self.cache.put(text, result, context=cache_context)

        return result

    def _calculate_confidence(
        self, heuristic_score: float, multi_turn_risk: float, behavioral_risk: float
    ) -> float:
        """Calculate overall confidence score.

        Combines multiple signals into final confidence using configurable weights.
        This is a placeholder until ONNX model integration.

        Args:
            heuristic_score: Heuristic analysis score
            multi_turn_risk: Multi-turn attack risk
            behavioral_risk: Behavioral analysis risk

        Returns:
            Combined confidence score (0.0 to 1.0)
        """
        confidence = (
            heuristic_score * self.weights.heuristic
            + multi_turn_risk * self.weights.multi_turn
            + behavioral_risk * self.weights.behavioral
        )

        return min(1.0, confidence)

    def reset_context(self) -> None:
        """Reset conversation context."""
        self.context.reset()

    def get_cache_stats(self) -> dict:
        """Get cache statistics.

        Returns:
            Cache statistics or empty dict if caching disabled
        """
        if self.cache:
            return self.cache.get_stats()
        return {}

    def clear_cache(self) -> None:
        """Clear result cache."""
        if self.cache:
            self.cache.clear()


# TODO: ONNX Integration (Week 2 Phase 2)
# class ONNXMLDetector(MLDetector):
#     """ML detector with ONNX inference.
#
#     Will replace heuristic scoring with DistilBERT ONNX model.
#     Target: <20ms P95 latency for inference.
#     """
#     pass
