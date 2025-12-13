"""Enhanced pattern detector with context awareness and confidence scoring."""

from dataclasses import dataclass
from typing import Optional

from .patterns import PIIPattern, PromptPattern, SQLPattern
from .patterns.validators import validate_pattern_with_context
from .patterns.validation_mapping import get_validation_function


@dataclass
class EnhancedDetectionResult:
    """Enhanced detection result with confidence scoring."""
    
    pattern_name: str
    pattern_type: str  # "pii", "sql", "prompt"
    matched_text: str
    start_pos: int
    end_pos: int
    severity: str
    confidence: float  # 0.0-1.0
    validation_passed: bool
    context_matched: bool
    description: str


class EnhancedPatternDetector:
    """Pattern detector with context awareness and confidence scoring."""
    
    def __init__(self, context_window_size: int = 50):
        """Initialize enhanced detector.
        
        Args:
            context_window_size: Number of characters to search for context keywords
        """
        self.context_window_size = context_window_size
    
    def detect_with_confidence(
        self,
        text: str,
        pattern: PIIPattern | PromptPattern | SQLPattern,
        pattern_type: str
    ) -> list[EnhancedDetectionResult]:
        """Detect patterns with confidence scoring.
        
        Args:
            text: Text to analyze
            pattern: Pattern to match
            pattern_type: Type of pattern ("pii", "sql", "prompt")
        
        Returns:
            List of enhanced detection results with confidence scores
        """
        results = []
        
        for match in pattern.pattern.finditer(text):
            matched_text = match.group(0)
            start_pos = match.start()
            end_pos = match.end()
            
            # Calculate confidence score
            confidence = self._calculate_confidence(
                text=text,
                pattern=pattern,
                matched_text=matched_text,
                start_pos=start_pos,
                end_pos=end_pos
            )
            
            # Check validation
            validation_passed = self._validate_match(pattern, matched_text)
            
            # Check context
            context_matched = self._check_context(
                text=text,
                pattern=pattern,
                start_pos=start_pos,
                end_pos=end_pos
            )
            
            # Get severity
            severity = getattr(pattern, "severity", getattr(pattern, "risk_level", "MEDIUM"))
            if hasattr(severity, "value"):
                severity = severity.value
            
            result = EnhancedDetectionResult(
                pattern_name=pattern.name,
                pattern_type=pattern_type,
                matched_text=matched_text,
                start_pos=start_pos,
                end_pos=end_pos,
                severity=severity,
                confidence=confidence,
                validation_passed=validation_passed,
                context_matched=context_matched,
                description=pattern.description
            )
            
            results.append(result)
        
        return results
    
    def _calculate_confidence(
        self,
        text: str,
        pattern: PIIPattern | PromptPattern | SQLPattern,
        matched_text: str,
        start_pos: int,
        end_pos: int
    ) -> float:
        """Calculate confidence score for a match.
        
        Confidence calculation:
        - Base: 0.4 (pattern match)
        - +0.3 if context keywords found
        - +0.3 if validation passed
        - Result: 0.4-1.0
        
        Args:
            text: Full text
            pattern: Pattern that matched
            matched_text: Matched text
            start_pos: Start position
            end_pos: End position
        
        Returns:
            Confidence score (0.0-1.0)
        """
        confidence = 0.4  # Base confidence for pattern match
        
        # Check context keywords (+0.3)
        if hasattr(pattern, "context_keywords") and pattern.context_keywords:
            if self._check_context(text, pattern, start_pos, end_pos):
                confidence += 0.3
        else:
            # No context required, give partial credit
            confidence += 0.15
        
        # Check validation (+0.3)
        if hasattr(pattern, "requires_validation") and pattern.requires_validation:
            if self._validate_match(pattern, matched_text):
                confidence += 0.3
        else:
            # No validation required, give partial credit
            confidence += 0.15
        
        return min(1.0, confidence)
    
    def _validate_match(
        self,
        pattern: PIIPattern | PromptPattern | SQLPattern,
        matched_text: str
    ) -> bool:
        """Validate a match using checksum/format validation.
        
        Args:
            pattern: Pattern that matched
            matched_text: Matched text
        
        Returns:
            True if validation passed or not required, False if failed
        """
        # Check if validation is required
        if not hasattr(pattern, "requires_validation") or not pattern.requires_validation:
            return True
        
        # Get validation function
        validation_func = get_validation_function(pattern.name)
        if not validation_func:
            return True  # No validator available
        
        try:
            return validation_func(matched_text)
        except Exception:
            return False
    
    def _check_context(
        self,
        text: str,
        pattern: PIIPattern | PromptPattern | SQLPattern,
        start_pos: int,
        end_pos: int
    ) -> bool:
        """Check if context keywords appear near the match.
        
        Args:
            text: Full text
            pattern: Pattern that matched
            start_pos: Start position of match
            end_pos: End position of match
        
        Returns:
            True if context matched or not required, False otherwise
        """
        # Check if context is required
        if not hasattr(pattern, "context_keywords") or not pattern.context_keywords:
            return True
        
        return validate_pattern_with_context(
            text=text,
            match_start=start_pos,
            match_end=end_pos,
            context_keywords=pattern.context_keywords,
            window_size=self.context_window_size
        )
