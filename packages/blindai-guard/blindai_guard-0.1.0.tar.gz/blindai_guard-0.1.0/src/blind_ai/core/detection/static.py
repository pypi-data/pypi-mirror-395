"""Static rule-based detector using Aho-Corasick automaton.

This module implements high-performance pattern matching for:
- SQL injection attacks
- Prompt injection attacks
- PII detection (credit cards, SSNs, etc.)

Performance target: <1ms for typical requests

Security features:
- Regex timeout protection against ReDoS attacks
- Input size limits enforced at model layer
"""

import logging
import re
import signal
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

import ahocorasick

from blind_ai.core.detection.patterns.pii import (
    ALL_PII_PATTERNS,
    PIICategory,
    RiskLevel,
)
from blind_ai.core.detection.patterns.prompt import (
    ALL_PROMPT_PATTERNS,
    PromptInjectionType,
)
from blind_ai.core.detection.patterns.sql import (
    ALL_SQL_PATTERNS,
    SQLInjectionType,
)
from blind_ai.core.detection.patterns.prompt import Severity as PromptSeverity
from blind_ai.core.detection.patterns.sql import Severity as SQLSeverity


logger = logging.getLogger(__name__)


# Regex timeout to prevent catastrophic backtracking (ReDoS)
REGEX_TIMEOUT_SECONDS = 0.1  # 100ms max per regex operation


class RegexTimeoutError(Exception):
    """Raised when a regex operation exceeds the timeout."""
    pass


def regex_search_with_timeout(
    pattern: re.Pattern,
    text: str,
    timeout: float = REGEX_TIMEOUT_SECONDS,
) -> Optional[re.Match]:
    """Execute regex search with timeout protection against ReDoS.
    
    Uses a thread pool to execute the regex with a timeout. If the regex
    takes longer than the timeout, it's considered a potential ReDoS attack
    and returns None.
    
    Args:
        pattern: Compiled regex pattern
        text: Text to search
        timeout: Maximum seconds to allow (default: 100ms)
        
    Returns:
        Match object if found within timeout, None otherwise
        
    Note:
        This adds ~1ms overhead per call, but protects against exponential
        backtracking patterns like (a+)+$ which can take hours on crafted input.
    """
    # For short texts, skip the timeout overhead
    if len(text) < 1000:
        try:
            return pattern.search(text)
        except Exception:
            return None
    
    # For longer texts, use timeout protection
    result = [None]
    exception = [None]
    
    def search_task():
        try:
            result[0] = pattern.search(text)
        except Exception as e:
            exception[0] = e
    
    thread = threading.Thread(target=search_task)
    thread.start()
    thread.join(timeout=timeout)
    
    if thread.is_alive():
        # Regex is taking too long - potential ReDoS
        logger.warning(
            f"Regex timeout exceeded ({timeout}s) - potential ReDoS attack. "
            f"Pattern: {pattern.pattern[:50]}..., Text length: {len(text)}"
        )
        # Thread will eventually complete, but we return None
        return None
    
    if exception[0]:
        logger.warning(f"Regex error: {exception[0]}")
        return None
        
    return result[0]


class ThreatType(Enum):
    """Types of threats detected by static analyzer."""

    SQL_INJECTION = "sql_injection"
    PROMPT_INJECTION = "prompt_injection"
    PII = "pii"


class ActionType(Enum):
    """Actions to take based on threat detection."""

    ALLOW = "allow"  # Request is safe
    BLOCK = "block"  # High confidence threat
    CHALLENGE = "challenge"  # Medium confidence, require approval
    LOG = "log"  # Low severity, log for monitoring

@dataclass
class DetectionResult:
    """Result from static detection.

    Attributes:
        threat_type: Type of threat detected
        pattern_name: Name of the matching pattern
        severity: Severity level (CRITICAL, HIGH, MEDIUM, LOW)
        action: Recommended action (ALLOW, BLOCK, CHALLENGE, LOG)
        description: Human-readable explanation
        matched_text: The text that triggered detection
        confidence: Confidence score (0.0-1.0)
    """

    threat_type: ThreatType
    pattern_name: str
    severity: str
    action: ActionType
    description: str
    matched_text: str
    confidence: float = 1.0  # Static patterns are high confidence

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "threat_type": self.threat_type.value,
            "pattern_name": self.pattern_name,
            "severity": self.severity,
            "action": self.action.value,
            "description": self.description,
            "matched_text": self.matched_text,
            "confidence": self.confidence,
        }


def calculate_pattern_confidence(
    pattern_severity: str,
    match_text: str,
    full_text: str,
    threat_type: ThreatType,
) -> float:
    """Calculate calibrated confidence score for a pattern match.

    Base confidence comes from pattern severity, with adjustments based on:
    - Match specificity (how unique the match is)
    - Context indicators (surrounding text)
    - Match coverage (what percentage of suspicious content was matched)

    Args:
        pattern_severity: Severity level of matched pattern
        match_text: The actual matched text
        full_text: The full input text
        threat_type: Type of threat detected

    Returns:
        Calibrated confidence score (0.0 to 1.0)
    """
    # Base confidence by severity
    base_confidence = {
        "critical": 0.95,
        "high": 0.85,
        "medium": 0.70,
        "low": 0.50,
    }.get(pattern_severity.lower(), 0.60)

    # Match specificity adjustment
    # Longer matches are more specific and reliable
    match_len = len(match_text)
    if match_len > 50:
        base_confidence = min(1.0, base_confidence + 0.05)
    elif match_len < 5:
        base_confidence = max(0.3, base_confidence - 0.1)

    # Context adjustment - look for attack indicators near the match
    attack_context_indicators = [
        "'", '"', ";", "--", "/*", "*/", "||", "&&",
        "UNION", "SELECT", "DROP", "DELETE", "INSERT",
        "ignore", "bypass", "override", "jailbreak",
    ]
    context_window = full_text[
        max(0, full_text.find(match_text) - 50):
        full_text.find(match_text) + len(match_text) + 50
    ].lower()

    context_matches = sum(1 for ind in attack_context_indicators if ind.lower() in context_window)
    if context_matches >= 3:
        base_confidence = min(1.0, base_confidence + 0.05)

    # Threat type specific adjustments
    if threat_type == ThreatType.SQL_INJECTION:
        # SQL with quotes or comment markers is more confident
        if any(c in match_text for c in ["'", '"', "--", "/*"]):
            base_confidence = min(1.0, base_confidence + 0.05)
    elif threat_type == ThreatType.PROMPT_INJECTION:
        # Prompt injection with explicit override language is more confident
        override_terms = ["ignore", "disregard", "forget", "override", "bypass"]
        if any(term in match_text.lower() for term in override_terms):
            base_confidence = min(1.0, base_confidence + 0.05)

    return round(base_confidence, 3)


class StaticDetector:
    """High-performance static pattern detector using Aho-Corasick.

    Uses Aho-Corasick automaton for efficient multi-pattern matching.
    Complexity: O(n + m) where n = text length, m = number of matches.

    Example:
        >>> detector = StaticDetector()
        >>> results = detector.detect("DROP TABLE users")
        >>> results[0].threat_type
        <ThreatType.SQL_INJECTION: 'sql_injection'>
    """

    def __init__(self) -> None:
        """Initialize detector and build Aho-Corasick automaton."""
        # Aho-Corasick automaton for SQL keywords
        self._sql_automaton = ahocorasick.Automaton()
        self._build_sql_automaton()

        # Aho-Corasick automaton for prompt injection keywords
        self._prompt_automaton = ahocorasick.Automaton()
        self._build_prompt_automaton()

        # Store patterns for detailed checking
        self._sql_patterns = ALL_SQL_PATTERNS
        self._prompt_patterns = ALL_PROMPT_PATTERNS
        self._pii_patterns = ALL_PII_PATTERNS

    def _build_sql_automaton(self) -> None:
        """Build Aho-Corasick automaton for SQL injection keywords."""
        # SQL keywords to search for (case-insensitive)
        sql_keywords = [
            "drop",
            "delete",
            "truncate",
            "union",
            "information_schema",
            "load_file",
            "outfile",
            "waitfor",
            "sleep",
            "benchmark",
            "xp_cmdshell",
            "exec",
            "execute",
            "--",
            "/*",
            "*/",
            "0x",  # Hex encoding
        ]

        for keyword in sql_keywords:
            self._sql_automaton.add_word(keyword.lower(), keyword)

        self._sql_automaton.make_automaton()

    def _build_prompt_automaton(self) -> None:
        """Build Aho-Corasick automaton for prompt injection keywords."""
        # Prompt injection keywords to search for
        prompt_keywords = [
            "ignore",
            "disregard",
            "forget",
            "override",
            "bypass",
            "jailbreak",
            "dan",
            "evil mode",
            "developer mode",
            "unrestricted",
            "system",
            "new instructions",
            "pretend",
            "simulate",
            "roleplay",
            "send",
            "email",
            "post",
            "transmit",
            "curl",
            "wget",
        ]

        for keyword in prompt_keywords:
            self._prompt_automaton.add_word(keyword.lower(), keyword)

        self._prompt_automaton.make_automaton()

    def detect(self, text: str) -> list[DetectionResult]:
        """Detect all threats in text.

        Args:
            text: Text to analyze (tool parameters, prompts, etc.)

        Returns:
            List of detection results, sorted by severity

        Example:
            >>> detector = StaticDetector()
            >>> results = detector.detect("admin' OR 1=1--")
            >>> len(results) > 0
            True
        """
        results = []

        # Run all detectors in parallel (they're independent)
        results.extend(self._detect_sql_injection(text))
        results.extend(self._detect_prompt_injection(text))
        results.extend(self._detect_pii(text))

        # Sort by severity (CRITICAL > HIGH > MEDIUM > LOW)
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        results.sort(key=lambda r: severity_order.get(r.severity.lower(), 4))

        return results

    def _detect_sql_injection(self, text: str) -> list[DetectionResult]:
        """Detect SQL injection patterns.

        Args:
            text: Text to analyze

        Returns:
            List of SQL injection detections
        """
        results = []
        text_lower = text.lower()

        # Fast keyword check with Aho-Corasick
        has_sql_keywords = False
        for _ in self._sql_automaton.iter(text_lower):
            has_sql_keywords = True
            break

        if not has_sql_keywords:
            return results

        # Detailed pattern matching with timeout protection
        for pattern in self._sql_patterns:
            match = regex_search_with_timeout(pattern.pattern, text)
            if match:
                # Map SQL severity to action
                action = self._sql_severity_to_action(pattern.severity)
                matched_text = match.group(0)

                # Calculate calibrated confidence
                confidence = calculate_pattern_confidence(
                    pattern.severity.value,
                    matched_text,
                    text,
                    ThreatType.SQL_INJECTION,
                )

                results.append(
                    DetectionResult(
                        threat_type=ThreatType.SQL_INJECTION,
                        pattern_name=pattern.name,
                        severity=pattern.severity.value,
                        action=action,
                        description=pattern.description,
                        matched_text=matched_text,
                        confidence=confidence,
                    )
                )

        return results

    def _detect_prompt_injection(self, text: str) -> list[DetectionResult]:
        """Detect prompt injection patterns.

        Args:
            text: Text to analyze

        Returns:
            List of prompt injection detections
        """
        results = []
        text_lower = text.lower()

        # Fast keyword check with Aho-Corasick
        has_prompt_keywords = False
        for _ in self._prompt_automaton.iter(text_lower):
            has_prompt_keywords = True
            break

        if not has_prompt_keywords:
            return results

        # Detailed pattern matching with timeout protection
        for pattern in self._prompt_patterns:
            match = regex_search_with_timeout(pattern.pattern, text)
            if match:
                # Map prompt severity to action
                action = self._prompt_severity_to_action(pattern.severity)
                matched_text = match.group(0)

                # Calculate calibrated confidence
                confidence = calculate_pattern_confidence(
                    pattern.severity.value,
                    matched_text,
                    text,
                    ThreatType.PROMPT_INJECTION,
                )

                results.append(
                    DetectionResult(
                        threat_type=ThreatType.PROMPT_INJECTION,
                        pattern_name=pattern.name,
                        severity=pattern.severity.value,
                        action=action,
                        description=pattern.description,
                        matched_text=matched_text,
                        confidence=confidence,
                    )
                )

        return results

    def _detect_pii(self, text: str) -> list[DetectionResult]:
        """Detect PII patterns (credit cards, SSNs, etc.).

        Args:
            text: Text to analyze

        Returns:
            List of PII detections
        """
        results = []

        for pattern in self._pii_patterns:
            # Use timeout-protected search for long texts
            if len(text) >= 1000:
                # For long texts, just check if pattern exists first
                match = regex_search_with_timeout(pattern.pattern, text)
                if not match:
                    continue
                matches = [match]  # Only process first match for safety
            else:
                # For short texts, process all matches
                matches = list(pattern.pattern.finditer(text))
            
            for match in matches:
                # Additional validation for credit cards (Luhn algorithm)
                if pattern.category == PIICategory.CREDIT_CARD and "card" in pattern.name:
                    if not self._validate_luhn(match.group(0)):
                        continue  # Skip false positive

                # Map PII risk level to action
                action = self._pii_risk_to_action(pattern.risk_level)
                matched_text = match.group(0)

                # Calculate calibrated confidence
                confidence = calculate_pattern_confidence(
                    pattern.risk_level.value,
                    matched_text,
                    text,
                    ThreatType.PII,
                )

                results.append(
                    DetectionResult(
                        threat_type=ThreatType.PII,
                        pattern_name=pattern.name,
                        severity=pattern.risk_level.value,
                        action=action,
                        description=f"{pattern.description} ({pattern.regulation})",
                        matched_text=self._mask_pii(matched_text),
                        confidence=confidence,
                    )
                )

        return results

    def _sql_severity_to_action(self, severity: SQLSeverity) -> ActionType:
        """Map SQL injection severity to action.

        Args:
            severity: SQL injection severity level

        Returns:
            Action to take
        """
        if severity == SQLSeverity.CRITICAL:
            return ActionType.BLOCK
        elif severity == SQLSeverity.HIGH:
            return ActionType.BLOCK
        elif severity == SQLSeverity.MEDIUM:
            return ActionType.CHALLENGE
        else:
            return ActionType.LOG

    def _prompt_severity_to_action(self, severity: PromptSeverity) -> ActionType:
        """Map prompt injection severity to action.

        Args:
            severity: Prompt injection severity level

        Returns:
            Action to take
        """
        if severity == PromptSeverity.CRITICAL:
            return ActionType.BLOCK
        elif severity == PromptSeverity.HIGH:
            return ActionType.BLOCK
        elif severity == PromptSeverity.MEDIUM:
            return ActionType.CHALLENGE
        else:
            return ActionType.LOG

    def _pii_risk_to_action(self, risk_level: RiskLevel) -> ActionType:
        """Map PII risk level to action.

        Args:
            risk_level: PII risk level

        Returns:
            Action to take
        """
        if risk_level == RiskLevel.CRITICAL:
            return ActionType.BLOCK
        elif risk_level == RiskLevel.HIGH:
            return ActionType.BLOCK
        elif risk_level == RiskLevel.MEDIUM:
            return ActionType.CHALLENGE
        else:
            return ActionType.LOG

    def _validate_luhn(self, card_number: str) -> bool:
        """Validate credit card using Luhn algorithm.

        Args:
            card_number: Credit card number (may include spaces/dashes)

        Returns:
            True if valid by Luhn algorithm, False otherwise
        """
        # Remove non-digit characters
        digits = "".join(c for c in card_number if c.isdigit())

        if len(digits) < 13 or len(digits) > 19:
            return False

        # Luhn algorithm
        total = 0
        reverse_digits = digits[::-1]

        for i, digit in enumerate(reverse_digits):
            n = int(digit)
            if i % 2 == 1:  # Every second digit from right
                n *= 2
                if n > 9:
                    n -= 9
            total += n

        return total % 10 == 0

    def _mask_pii(self, text: str) -> str:
        """Mask PII for safe logging.

        Args:
            text: PII text to mask

        Returns:
            Masked version (e.g., "4532****6789")
        """
        # Remove spaces/dashes for consistent masking
        cleaned = "".join(c for c in text if c.isalnum())

        if len(cleaned) <= 8:
            # Short values - mask middle
            return f"{cleaned[:2]}***{cleaned[-2:]}"
        else:
            # Long values - show first 4 and last 4
            return f"{cleaned[:4]}****{cleaned[-4:]}"

    def get_blocking_threats(self, results: list[DetectionResult]) -> list[DetectionResult]:
        """Filter results to only blocking threats.

        Args:
            results: All detection results

        Returns:
            Only results with action=BLOCK
        """
        return [r for r in results if r.action == ActionType.BLOCK]

    def has_critical_threat(self, results: list[DetectionResult]) -> bool:
        """Check if any result is CRITICAL severity.

        Args:
            results: Detection results to check

        Returns:
            True if any CRITICAL severity threat found
        """
        return any(r.severity.lower() == "critical" for r in results)
