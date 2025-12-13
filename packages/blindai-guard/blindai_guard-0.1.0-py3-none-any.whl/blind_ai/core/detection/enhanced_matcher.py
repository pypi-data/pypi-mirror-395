"""Enhanced pattern matching with validation, context, and confidence scoring.

This module provides advanced pattern matching capabilities including:
- Checksum validation for PII patterns
- Context window matching for ambiguous patterns
- Confidence scoring based on multiple factors
- Pattern chaining detection for split attacks
"""

import logging
import re
from dataclasses import dataclass
from typing import Any

from .patterns import (
    ALL_PII_PATTERNS,
    ALL_PROMPT_PATTERNS,
    ALL_SQL_PATTERNS,
    PIIPattern,
    PromptPattern,
    SQLPattern,
)
from .patterns.validators import (
    luhn_check,
    validate_ein,
    validate_iban_checksum,
    validate_medicare_id,
    validate_npi,
    validate_phone_e164,
    validate_ssn_format,
)


# Module logger
logger = logging.getLogger(__name__)


@dataclass
class PatternMatch:
    """A single pattern match with confidence score."""

    pattern_name: str
    pattern_type: str  # "pii", "sql", or "prompt"
    match_text: str
    start_pos: int
    end_pos: int
    confidence: float  # 0.0-1.0
    severity: str
    description: str
    validation_passed: bool | None = None  # None if no validation required
    context_matched: bool | None = None  # None if no context keywords
    metadata: dict[str, Any] | None = None


class EnhancedPatternMatcher:
    """Pattern matcher with validation, context, and confidence scoring."""

    def __init__(
        self,
        context_window: int = 50,
        min_confidence: float = 0.5,
        enable_validation: bool = True,
    ):
        """Initialize enhanced pattern matcher.

        Args:
            context_window: Number of characters to search before/after match for context keywords
            min_confidence: Minimum confidence score to report a match (0.0-1.0)
            enable_validation: Whether to perform checksum validation
        """
        self.context_window = context_window
        self.min_confidence = min_confidence
        self.enable_validation = enable_validation

    def find_context_keywords(
        self, text: str, match_start: int, match_end: int, keywords: list[str]
    ) -> bool:
        """Check if any context keywords appear near the match.

        Args:
            text: Full text being scanned
            match_start: Start position of match
            match_end: End position of match
            keywords: List of context keywords to search for

        Returns:
            True if any keyword found within context window
        """
        # Extract context window around match
        window_start = max(0, match_start - self.context_window)
        window_end = min(len(text), match_end + self.context_window)
        context = text[window_start:window_end].lower()

        # Check if any keyword appears in context
        return any(keyword.lower() in context for keyword in keywords)

    def validate_pii_match(self, pattern: PIIPattern, match_text: str) -> bool:
        """Validate PII match using checksum or format validation.

        Args:
            pattern: The PII pattern that matched
            match_text: The matched text

        Returns:
            True if validation passes or not required
        """
        if not self.enable_validation or not pattern.requires_validation:
            return True

        # Clean match text (remove spaces, dashes)
        cleaned = re.sub(r"[\s-]", "", match_text)

        # Route to appropriate validator based on pattern name
        validators = {
            "ssn": validate_ssn_format,
            "credit_card_visa": luhn_check,
            "credit_card_mastercard": luhn_check,
            "credit_card_amex": luhn_check,
            "credit_card_discover": luhn_check,
            "iban": validate_iban_checksum,
            "medicare_id": validate_medicare_id,
            "npi": validate_npi,
            "phone_e164": validate_phone_e164,
            "us_ein": validate_ein,
        }

        validator = validators.get(pattern.name)
        if validator:
            try:
                return validator(cleaned)
            except Exception as e:
                # Log the validation failure for debugging
                logger.warning(
                    "Validation failed for pattern '%s' with text '%s': %s",
                    pattern.name,
                    match_text[:20] + "..." if len(match_text) > 20 else match_text,
                    str(e),
                    exc_info=True,
                )
                # Be conservative and flag it as potentially matching
                return False

        # No specific validator, assume valid
        return True

    def calculate_confidence(
        self,
        pattern: PIIPattern | SQLPattern | PromptPattern,
        match_text: str,
        validation_passed: bool | None,
        context_matched: bool | None,
    ) -> float:
        """Calculate confidence score for a match.

        Confidence factors:
        - Base severity: CRITICAL=1.0, HIGH=0.8, MEDIUM=0.6, LOW=0.4
        - Validation passed: +0.2 (if applicable)
        - Context matched: +0.15 (if applicable)
        - Pattern false positive rate: -FP_rate

        Args:
            pattern: The pattern that matched
            match_text: The matched text
            validation_passed: Whether validation passed (if applicable)
            context_matched: Whether context keywords matched (if applicable)

        Returns:
            Confidence score between 0.0 and 1.0
        """
        # Base confidence from severity
        severity_scores = {
            "critical": 1.0,
            "high": 0.8,
            "medium": 0.6,
            "low": 0.4,
        }

        # Get severity value
        if hasattr(pattern, "risk_level"):  # PII
            severity_str = pattern.risk_level.value
        else:  # SQL or Prompt
            severity_str = pattern.severity.value

        confidence = severity_scores.get(severity_str, 0.5)

        # Adjust for validation result
        if validation_passed is not None:
            if validation_passed:
                confidence = min(1.0, confidence + 0.2)
            else:
                confidence = max(0.0, confidence - 0.4)  # Failed validation is very bad

        # Adjust for context matching
        if context_matched is not None:
            if context_matched:
                confidence = min(1.0, confidence + 0.15)
            else:
                # No context match for ambiguous pattern reduces confidence
                if hasattr(pattern, "context_keywords") and pattern.context_keywords:
                    confidence = max(0.0, confidence - 0.3)

        # Adjust for known false positive rate
        if hasattr(pattern, "false_positive_rate"):
            confidence = max(0.0, confidence - pattern.false_positive_rate)

        return round(confidence, 2)

    def match_pii(self, text: str) -> list[PatternMatch]:
        """Find all PII matches with validation and confidence scoring.

        Args:
            text: Text to scan for PII

        Returns:
            List of pattern matches above min_confidence threshold
        """
        matches = []

        for pattern in ALL_PII_PATTERNS:
            for match in pattern.pattern.finditer(text):
                match_text = match.group(0)

                # Check validation if required
                validation_passed = None
                if pattern.requires_validation:
                    validation_passed = self.validate_pii_match(pattern, match_text)

                # Check context keywords if specified
                context_matched = None
                if pattern.context_keywords:
                    context_matched = self.find_context_keywords(
                        text, match.start(), match.end(), pattern.context_keywords
                    )

                # Calculate confidence
                confidence = self.calculate_confidence(
                    pattern, match_text, validation_passed, context_matched
                )

                # Only report if confidence meets threshold
                if confidence >= self.min_confidence:
                    matches.append(
                        PatternMatch(
                            pattern_name=pattern.name,
                            pattern_type="pii",
                            match_text=match_text,
                            start_pos=match.start(),
                            end_pos=match.end(),
                            confidence=confidence,
                            severity=pattern.risk_level.value,
                            description=pattern.description,
                            validation_passed=validation_passed,
                            context_matched=context_matched,
                            metadata={
                                "category": pattern.category.value,
                                "regulation": pattern.regulation,
                                "country": pattern.country,
                            },
                        )
                    )

        return matches

    def match_sql(self, text: str) -> list[PatternMatch]:
        """Find all SQL injection matches with confidence scoring.

        Args:
            text: Text to scan for SQL injection

        Returns:
            List of pattern matches above min_confidence threshold
        """
        matches = []

        for pattern in ALL_SQL_PATTERNS:
            for match in pattern.pattern.finditer(text):
                match_text = match.group(0)

                # Check context keywords if specified
                context_matched = None
                if pattern.context_keywords:
                    context_matched = self.find_context_keywords(
                        text, match.start(), match.end(), pattern.context_keywords
                    )

                # Calculate confidence
                confidence = self.calculate_confidence(
                    pattern, match_text, None, context_matched
                )

                # Only report if confidence meets threshold
                if confidence >= self.min_confidence:
                    matches.append(
                        PatternMatch(
                            pattern_name=pattern.name,
                            pattern_type="sql",
                            match_text=match_text,
                            start_pos=match.start(),
                            end_pos=match.end(),
                            confidence=confidence,
                            severity=pattern.severity.value,
                            description=pattern.description,
                            validation_passed=None,
                            context_matched=context_matched,
                            metadata={
                                "injection_type": pattern.injection_type.value,
                            },
                        )
                    )

        return matches

    def match_prompt(self, text: str) -> list[PatternMatch]:
        """Find all prompt injection matches with confidence scoring.

        Args:
            text: Text to scan for prompt injection

        Returns:
            List of pattern matches above min_confidence threshold
        """
        matches = []

        for pattern in ALL_PROMPT_PATTERNS:
            for match in pattern.pattern.finditer(text):
                match_text = match.group(0)

                # Check context keywords if specified
                context_matched = None
                if pattern.context_keywords:
                    context_matched = self.find_context_keywords(
                        text, match.start(), match.end(), pattern.context_keywords
                    )

                # Calculate confidence
                confidence = self.calculate_confidence(
                    pattern, match_text, None, context_matched
                )

                # Only report if confidence meets threshold
                if confidence >= self.min_confidence:
                    matches.append(
                        PatternMatch(
                            pattern_name=pattern.name,
                            pattern_type="prompt",
                            match_text=match_text,
                            start_pos=match.start(),
                            end_pos=match.end(),
                            confidence=confidence,
                            severity=pattern.severity.value,
                            description=pattern.description,
                            validation_passed=None,
                            context_matched=context_matched,
                            metadata={
                                "injection_type": pattern.injection_type.value,
                            },
                        )
                    )

        return matches

    def match_all(self, text: str) -> dict[str, list[PatternMatch]]:
        """Find all threats (PII, SQL, Prompt) in text.

        Args:
            text: Text to scan

        Returns:
            Dictionary with keys "pii", "sql", "prompt" containing match lists
        """
        return {
            "pii": self.match_pii(text),
            "sql": self.match_sql(text),
            "prompt": self.match_prompt(text),
        }


@dataclass
class PatternChain:
    """Detected pattern chain across multiple messages."""

    patterns: list[str]  # Pattern names in sequence
    confidence: float  # Overall confidence this is a real attack
    description: str
    messages: list[int]  # Message indices in conversation


class PatternChainDetector:
    """Detect multi-message attack patterns."""

    def __init__(self, max_gap: int = 3, window_size: int = 10):
        """Initialize chain detector.

        Args:
            max_gap: Maximum messages between chain elements
            window_size: Number of recent messages to analyze
        """
        self.max_gap = max_gap
        self.window_size = window_size
        self.message_history: list[tuple[str, list[PatternMatch]]] = []

    def add_message(self, text: str, matches: list[PatternMatch]) -> None:
        """Add a message to history for chain detection.

        Args:
            text: Message text
            matches: Pattern matches found in message
        """
        self.message_history.append((text, matches))

        # Keep only recent history
        if len(self.message_history) > self.window_size:
            self.message_history.pop(0)

    def detect_chains(self) -> list[PatternChain]:
        """Detect attack chains in message history.

        Common chains:
        - "ignore" + "previous" (split injection)
        - "you are" + "now" + "unrestricted" (split role manipulation)
        - Multiple data exfiltration attempts

        Returns:
            List of detected pattern chains
        """
        chains = []

        # Chain 1: Split "ignore previous instructions"
        ignore_indices = []
        previous_indices = []

        for i, (text, matches) in enumerate(self.message_history):
            text_lower = text.lower()
            if "ignore" in text_lower or "disregard" in text_lower or "forget" in text_lower:
                ignore_indices.append(i)
            if "previous" in text_lower or "above" in text_lower or "earlier" in text_lower:
                previous_indices.append(i)

        # Check if ignore and previous appear within max_gap
        for ignore_idx in ignore_indices:
            for prev_idx in previous_indices:
                if 0 < abs(ignore_idx - prev_idx) <= self.max_gap:
                    chains.append(
                        PatternChain(
                            patterns=["context_switching_split"],
                            confidence=0.85,
                            description="Split context switching attack across messages",
                            messages=[min(ignore_idx, prev_idx), max(ignore_idx, prev_idx)],
                        )
                    )

        return chains
