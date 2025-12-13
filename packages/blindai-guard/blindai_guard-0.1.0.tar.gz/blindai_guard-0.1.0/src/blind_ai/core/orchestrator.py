"""Detection orchestrator for coordinating multiple detection layers.

Coordinates static detection, ML detection, and policy evaluation to produce
final threat assessment and action recommendation.
"""

import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed
from typing import Optional

from .detection.ml.detector import MLDetector
from .detection.static import DetectionResult, StaticDetector
from .models import (
    DetectionRequest,
    DetectionResponse,
    FinalAction,
    OrchestrationConfig,
    ThreatLevel,
)
from .policy.policy import PolicyAction, PolicyEngine


class DetectionOrchestrator:
    """Orchestrates multi-layer threat detection.

    Coordinates static pattern detection, ML-based detection, and policy
    evaluation to produce comprehensive threat assessments.

    Attributes:
        config: Orchestration configuration
        static_detector: Static pattern detector
        ml_detector: ML-based detector
        policy_engine: Policy evaluation engine
        executor: Thread pool for parallel execution
        session_threat_history: Recent threats per session for correlation
    """

    # Maximum threats to track per session for correlation
    MAX_SESSION_HISTORY = 10
    # Time window for threat correlation (seconds)
    CORRELATION_WINDOW_SECONDS = 60.0

    def __init__(
        self,
        config: Optional[OrchestrationConfig] = None,
        static_detector: Optional[StaticDetector] = None,
        ml_detector: Optional[MLDetector] = None,
        policy_engine: Optional[PolicyEngine] = None,
    ):
        """Initialize detection orchestrator.

        Args:
            config: Orchestration configuration
            static_detector: Static detector instance
            ml_detector: ML detector instance
            policy_engine: Policy engine instance
        """
        self.config = config or OrchestrationConfig()

        # Initialize detection layers
        self.static_detector = static_detector or StaticDetector()
        self.ml_detector = ml_detector or MLDetector()
        self.policy_engine = policy_engine or PolicyEngine()

        # Thread pool for parallel execution
        self.executor = ThreadPoolExecutor(max_workers=3) if self.config.parallel_execution else None

        # Session-based threat history for cross-request correlation
        # Dict[context_id -> list of (timestamp, threat_types)]
        self._session_threat_history: dict[str, list[tuple[float, set[str]]]] = {}
        self._closed = False

    def shutdown(self, wait: bool = True) -> None:
        """Shutdown the orchestrator and release resources.

        Args:
            wait: If True, wait for pending tasks to complete
        """
        if self._closed:
            return
        self._closed = True
        if self.executor:
            self.executor.shutdown(wait=wait)
            self.executor = None

    def __enter__(self) -> "DetectionOrchestrator":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - ensures cleanup."""
        self.shutdown(wait=True)

    def __del__(self) -> None:
        """Destructor - ensures cleanup if not explicitly closed."""
        self.shutdown(wait=False)

    def detect(self, request: DetectionRequest) -> DetectionResponse:
        """Perform comprehensive threat detection.

        Args:
            request: Detection request

        Returns:
            Detection response with threat assessment and action recommendation
        """
        start_time = time.perf_counter()
        layers_executed = []

        try:
            # Execute detection layers
            if self.config.parallel_execution:
                results = self._execute_parallel(request)
            else:
                results = self._execute_sequential(request)

            static_results, ml_results, layers_executed = results

            # Policy evaluation (always sequential after detection)
            policy_action = self._evaluate_policy(static_results)

            # Aggregate results
            response = self._aggregate_results(
                static_results, ml_results, policy_action, layers_executed, request
            )

            # Calculate processing time
            processing_time = (time.perf_counter() - start_time) * 1000
            response.processing_time_ms = processing_time

            return response

        except TimeoutError:
            # Handle timeout
            if self.config.fail_open:
                return self._create_fail_open_response(start_time)
            else:
                return self._create_fail_closed_response(start_time)

        except Exception as e:
            # Handle unexpected errors
            if self.config.fail_open:
                return self._create_fail_open_response(start_time, error=str(e))
            else:
                return self._create_fail_closed_response(start_time, error=str(e))

    def _execute_parallel(
        self, request: DetectionRequest
    ) -> tuple[list[DetectionResult], dict, list[str]]:
        """Execute detection layers in parallel.

        Args:
            request: Detection request

        Returns:
            Tuple of (static_results, ml_results, layers_executed)
        """
        futures = {}
        layers_executed = []

        # Submit detection tasks
        if self.config.enable_static:
            futures["static"] = self.executor.submit(
                self.static_detector.detect, request.text
            )

        if self.config.enable_ml:
            futures["ml"] = self.executor.submit(
                self.ml_detector.detect, request.text
            )

        # Collect results with timeout
        timeout = self.config.timeout_ms / 1000.0  # Convert to seconds
        static_results = []
        ml_results = {}

        for future in as_completed(futures.values(), timeout=timeout):
            if futures.get("static") == future:
                static_results = future.result()
                layers_executed.append("static")
            elif futures.get("ml") == future:
                ml_results = future.result()
                layers_executed.append("ml")

        return static_results, ml_results, layers_executed

    def _execute_sequential(
        self, request: DetectionRequest
    ) -> tuple[list[DetectionResult], dict, list[str]]:
        """Execute detection layers sequentially.

        Args:
            request: Detection request

        Returns:
            Tuple of (static_results, ml_results, layers_executed)
        """
        static_results = []
        ml_results = {}
        layers_executed = []

        # Execute static detection
        if self.config.enable_static:
            static_results = self.static_detector.detect(request.text)
            layers_executed.append("static")

        # Execute ML detection
        if self.config.enable_ml:
            ml_results = self.ml_detector.detect(request.text)
            layers_executed.append("ml")

        return static_results, ml_results, layers_executed

    def _evaluate_policy(self, static_results: list[DetectionResult]) -> PolicyAction:
        """Evaluate policy against detection results.

        Args:
            static_results: Results from static detector

        Returns:
            Policy action recommendation
        """
        if not self.config.enable_policy or not static_results:
            return PolicyAction.ALLOW

        # Evaluate batch policy
        batch_result = self.policy_engine.evaluate_batch(static_results)
        return batch_result["overall_action"]

    def _aggregate_results(
        self,
        static_results: list[DetectionResult],
        ml_results: dict,
        policy_action: PolicyAction,
        layers_executed: list[str],
        request: DetectionRequest,
    ) -> DetectionResponse:
        """Aggregate results from all detection layers.

        Args:
            static_results: Static detection results
            ml_results: ML detection results
            policy_action: Policy action
            layers_executed: List of executed layers
            request: Original detection request for context

        Returns:
            Aggregated detection response
        """
        # Deduplicate static results (same pattern matching same text)
        static_results = self._deduplicate_results(static_results)

        # Apply context-aware severity adjustments
        static_results = self._adjust_severity_by_context(
            static_results, ml_results, request
        )

        # Determine if threat detected
        has_static_threats = len(static_results) > 0
        has_ml_threats = ml_results.get("is_threat", False)
        is_threat = has_static_threats or has_ml_threats

        # Calculate overall confidence
        confidence = self._calculate_confidence(static_results, ml_results)

        # Determine threat level (with session-based threat correlation)
        threat_level = self._determine_threat_level(
            static_results, ml_results, session_id=request.context_id
        )

        # Determine final action
        final_action = self._determine_final_action(policy_action, threat_level)

        # Build threats detected list
        threats_detected = self._build_threats_list(static_results, ml_results)

        # Format static results
        static_dict = {
            "count": len(static_results),
            "threats": [
                {
                    "type": r.threat_type.value,
                    "pattern": r.pattern_name,
                    "severity": r.severity,
                    "confidence": r.confidence,
                    "matched_text": r.matched_text,
                }
                for r in static_results
            ],
        }

        return DetectionResponse(
            is_threat=is_threat,
            threat_level=threat_level,
            final_action=final_action,
            confidence=confidence,
            threats_detected=threats_detected,
            static_results=static_dict,
            ml_results=ml_results,
            policy_action=policy_action.value,
            layers_executed=layers_executed,
        )

    def _deduplicate_results(
        self, results: list[DetectionResult]
    ) -> list[DetectionResult]:
        """Deduplicate detection results.

        Removes duplicate detections where the same pattern matched the same text.
        Keeps the result with highest confidence when duplicates found.

        Args:
            results: List of detection results

        Returns:
            Deduplicated list, keeping highest confidence for each unique match
        """
        if not results:
            return results

        # Use (pattern_name, matched_text) as deduplication key
        seen: dict[tuple[str, str], DetectionResult] = {}

        for result in results:
            key = (result.pattern_name, result.matched_text)

            if key not in seen:
                seen[key] = result
            elif result.confidence > seen[key].confidence:
                # Keep higher confidence match
                seen[key] = result

        return list(seen.values())

    def _adjust_severity_by_context(
        self,
        static_results: list[DetectionResult],
        ml_results: dict,
        request: DetectionRequest,
    ) -> list[DetectionResult]:
        """Adjust detection severity based on contextual factors.

        Can downgrade severity when context suggests lower risk:
        - Low ML confidence suggests static match may be false positive
        - Known safe patterns (e.g., SQL in educational content)
        - Request metadata indicating test/development context

        Args:
            static_results: Static detection results
            ml_results: ML detection results  
            request: Original detection request

        Returns:
            Results with potentially adjusted severities
        """
        if not static_results:
            return static_results

        ml_confidence = ml_results.get("confidence", 0.0) if ml_results else 0.0
        adjusted_results = []

        # Check for development/test context indicators
        is_dev_context = False
        if hasattr(request, "metadata") and request.metadata:
            env = request.metadata.get("environment", "")
            is_dev_context = env.lower() in ("development", "test", "staging", "dev")

        for result in static_results:
            adjusted_severity = result.severity

            # Low ML confidence can downgrade medium/low severity detections
            if ml_confidence < 0.3 and result.severity in ("medium", "low"):
                # Static-only detection with low ML signal - likely false positive
                if result.severity == "medium":
                    adjusted_severity = "low"
                # Note: We don't downgrade below "low" to preserve audit trail

            # Development context can downgrade non-critical threats
            if is_dev_context and result.severity not in ("critical",):
                severity_downgrade = {
                    "high": "medium",
                    "medium": "low",
                }
                adjusted_severity = severity_downgrade.get(adjusted_severity, adjusted_severity)

            # If severity changed, create new result with adjusted severity
            if adjusted_severity != result.severity:
                # Create adjusted result (DetectionResult is a dataclass)
                adjusted_result = DetectionResult(
                    threat_type=result.threat_type,
                    pattern_name=result.pattern_name,
                    severity=adjusted_severity,
                    action=result.action,
                    description=result.description + f" [Adjusted from {result.severity}]",
                    matched_text=result.matched_text,
                    confidence=result.confidence * 0.8,  # Reduce confidence for adjusted results
                )
                adjusted_results.append(adjusted_result)
            else:
                adjusted_results.append(result)

        return adjusted_results

    def _calculate_confidence(
        self, static_results: list[DetectionResult], ml_results: dict
    ) -> float:
        """Calculate overall confidence score with normalized weights.

        Args:
            static_results: Static detection results
            ml_results: ML detection results

        Returns:
            Overall confidence score (0.0 to 1.0)
            Returns 0.0 if no detectors produced results (no threat detected)
        """
        # Base weights for each detector type
        STATIC_WEIGHT = 0.6
        ML_WEIGHT = 0.4

        # Track which detectors contributed
        weighted_scores: list[float] = []
        total_weight = 0.0

        # Static detector confidence (average of all detections)
        if static_results:
            static_conf = sum(r.confidence for r in static_results) / len(static_results)
            weighted_scores.append(static_conf * STATIC_WEIGHT)
            total_weight += STATIC_WEIGHT

        # ML detector confidence (only if ML detected a threat)
        if ml_results and ml_results.get("is_threat", False):
            ml_conf = ml_results.get("confidence", 0.0)
            weighted_scores.append(ml_conf * ML_WEIGHT)
            total_weight += ML_WEIGHT

        # Normalize by total weight so scores range 0.0-1.0
        # If no detectors contributed (no threats), return 0.0
        if total_weight > 0:
            return sum(weighted_scores) / total_weight
        return 0.0

    def _get_session_threat_types(self, session_id: str | None) -> set[str]:
        """Get threat types from session history.
        
        Args:
            session_id: Session identifier (None means no session tracking)
            
        Returns:
            Set of threat type strings from recent session history
        """
        if not session_id or session_id not in self._session_threat_history:
            return set()
        return set(self._session_threat_history[session_id])
    
    def _record_session_threats(
        self, session_id: str | None, static_results: list[DetectionResult]
    ) -> None:
        """Record detected threats to session history.
        
        Args:
            session_id: Session identifier (None means no session tracking)
            static_results: Detection results from current request
        """
        if not session_id or not static_results:
            return
            
        if session_id not in self._session_threat_history:
            self._session_threat_history[session_id] = []
            
        for result in static_results:
            threat_type = result.threat_type.value
            if threat_type not in self._session_threat_history[session_id]:
                self._session_threat_history[session_id].append(threat_type)
                
        # Limit history size to prevent memory growth
        max_history = 20
        if len(self._session_threat_history[session_id]) > max_history:
            self._session_threat_history[session_id] = \
                self._session_threat_history[session_id][-max_history:]

    def _detect_threat_combinations(
        self, static_results: list[DetectionResult], session_id: str | None = None
    ) -> dict:
        """Detect dangerous combinations of threats that escalate severity.

        Certain threat combinations indicate sophisticated, targeted attacks
        that are more dangerous than individual threats alone.
        
        This method checks both:
        1. Threats within the current request
        2. Threat patterns across the session (if session_id provided)

        Args:
            static_results: Static detection results from current request
            session_id: Optional session ID for cross-request correlation

        Returns:
            Dictionary with:
                - has_combination: Whether dangerous combination found
                - combination_type: Type of combination detected
                - severity_boost: Amount to boost severity
                - description: Human-readable explanation
                - is_cross_request: Whether combination spans multiple requests
        """
        # Combine current threats with session history
        current_types = {r.threat_type.value for r in static_results}
        session_types = self._get_session_threat_types(session_id)
        
        # Record current threats to session history
        self._record_session_threats(session_id, static_results)
        
        # All threats (current + historical)
        all_threat_types = current_types | session_types
        
        # Check if we have enough threats to form combinations
        if len(current_types) < 2 and len(all_threat_types) < 2:
            return {"has_combination": False}

        # Use combined types for detection
        threat_types = all_threat_types
        is_cross_request = bool(session_types and current_types - session_types)
        
        # Helper to build result with cross-request info
        def make_result(combo_type: str, boost: int, desc: str) -> dict:
            result = {
                "has_combination": True,
                "combination_type": combo_type,
                "severity_boost": boost,
                "description": desc,
                "is_cross_request": is_cross_request,
            }
            if is_cross_request:
                result["description"] += " (detected across multiple requests in session)"
            return result

        # Define dangerous combinations
        # SQL injection + PII exfiltration = data theft attack
        if "sql_injection" in threat_types and "pii" in threat_types:
            return make_result(
                "data_exfiltration",
                1,  # Elevate by one level
                "SQL injection combined with PII patterns suggests data exfiltration attempt",
            )

        # Prompt injection + SQL injection = multi-vector attack
        if "prompt_injection" in threat_types and "sql_injection" in threat_types:
            return make_result(
                "multi_vector_attack",
                1,
                "Prompt injection combined with SQL injection indicates sophisticated multi-vector attack",
            )

        # Multiple high-severity threats = coordinated attack
        high_severity_count = sum(
            1 for r in static_results if r.severity in ("critical", "high")
        )
        if high_severity_count >= 3:
            return make_result(
                "coordinated_attack",
                1,
                f"Multiple high-severity threats ({high_severity_count}) suggest coordinated attack",
            )

        return {"has_combination": False, "is_cross_request": False}

    def _determine_threat_level(
        self, static_results: list[DetectionResult], ml_results: dict,
        session_id: str | None = None
    ) -> ThreatLevel:
        """Determine overall threat level.

        Args:
            static_results: Static detection results
            ml_results: ML detection results
            session_id: Optional session ID for cross-request correlation

        Returns:
            Overall threat level
        """
        if not static_results and not ml_results.get("is_threat"):
            return ThreatLevel.NONE

        # Check for threat combinations that escalate severity
        combination_result = self._detect_threat_combinations(
            static_results, session_id=session_id
        )
        severity_boost = combination_result.get("severity_boost", 0)

        # Check for critical threats
        has_critical = any(r.severity == "critical" for r in static_results)
        if has_critical:
            return ThreatLevel.CRITICAL

        # Check for high severity (with combination boost)
        has_high = any(r.severity == "high" for r in static_results)
        ml_high = ml_results.get("confidence", 0.0) > 0.8
        if has_high or ml_high:
            # Combination can elevate HIGH to CRITICAL
            if severity_boost > 0:
                return ThreatLevel.CRITICAL
            return ThreatLevel.HIGH

        # Check for medium severity (with combination boost)
        has_medium = any(r.severity == "medium" for r in static_results)
        ml_medium = ml_results.get("confidence", 0.0) > 0.6
        if has_medium or ml_medium:
            # Combination can elevate MEDIUM to HIGH
            if severity_boost > 0:
                return ThreatLevel.HIGH
            return ThreatLevel.MEDIUM

        # Low severity with combination boost elevates to MEDIUM
        if severity_boost > 0:
            return ThreatLevel.MEDIUM

        return ThreatLevel.LOW

    def _determine_final_action(
        self, policy_action: PolicyAction, threat_level: ThreatLevel
    ) -> FinalAction:
        """Determine final action recommendation.

        Args:
            policy_action: Policy engine recommendation
            threat_level: Overall threat level

        Returns:
            Final action to take
        """
        # Policy action takes precedence
        action_mapping = {
            PolicyAction.BLOCK: FinalAction.BLOCK,
            PolicyAction.CHALLENGE: FinalAction.CHALLENGE,
            PolicyAction.LOG: FinalAction.LOG,
            PolicyAction.ALLOW: FinalAction.ALLOW,
        }

        return action_mapping.get(policy_action, FinalAction.ALLOW)

    def _build_threats_list(
        self, static_results: list[DetectionResult], ml_results: dict
    ) -> list[dict]:
        """Build consolidated threats list.

        Args:
            static_results: Static detection results
            ml_results: ML detection results

        Returns:
            List of detected threats
        """
        threats = []

        # Add static threats
        for result in static_results:
            threats.append(
                {
                    "source": "static",
                    "type": result.threat_type.value,
                    "pattern": result.pattern_name,
                    "severity": result.severity,
                    "confidence": result.confidence,
                    "description": result.description,
                }
            )

        # Add ML threats
        if ml_results.get("is_threat"):
            threats.append(
                {
                    "source": "ml",
                    "type": "heuristic",
                    "confidence": ml_results.get("confidence", 0.0),
                    "heuristic_score": ml_results.get("heuristic_score", 0.0),
                    "multi_turn_risk": ml_results.get("multi_turn_risk", 0.0),
                }
            )

        return threats

    def _create_fail_open_response(
        self, start_time: float, error: Optional[str] = None
    ) -> DetectionResponse:
        """Create fail-open response (allow on error).

        Args:
            start_time: Request start time
            error: Optional error message

        Returns:
            Allow response
        """
        processing_time = (time.perf_counter() - start_time) * 1000

        return DetectionResponse(
            is_threat=False,
            threat_level=ThreatLevel.NONE,
            final_action=FinalAction.ALLOW,
            confidence=0.0,
            processing_time_ms=processing_time,
            metadata={"error": error, "fail_mode": "open"} if error else {},
        )

    def _create_fail_closed_response(
        self, start_time: float, error: Optional[str] = None
    ) -> DetectionResponse:
        """Create fail-closed response (block on error).

        Args:
            start_time: Request start time
            error: Optional error message

        Returns:
            Block response
        """
        processing_time = (time.perf_counter() - start_time) * 1000

        return DetectionResponse(
            is_threat=True,
            threat_level=ThreatLevel.HIGH,
            final_action=FinalAction.BLOCK,
            confidence=1.0,
            processing_time_ms=processing_time,
            metadata={"error": error, "fail_mode": "closed"} if error else {},
        )
