"""Detection patterns for Blind AI.

This package contains all pattern definitions for static detection:
- SQL injection patterns (core + extended)
- Prompt injection patterns (core + extended)
- PII patterns (GDPR, HIPAA, PCI-DSS + extended)
- Validation functions
"""

from blind_ai.core.detection.patterns.pii import (
    ALL_PII_PATTERNS,
    PIICategory,
    PIIPattern,
    RiskLevel,
)
from blind_ai.core.detection.patterns.prompt import (
    ALL_PROMPT_PATTERNS,
    PromptInjectionType,
    PromptPattern,
)
from blind_ai.core.detection.patterns.sql import (
    ALL_SQL_PATTERNS,
    Severity,
    SQLInjectionType,
    SQLPattern,
)
from blind_ai.core.detection.patterns.validators import (
    luhn_check,
    validate_ein,
    validate_iban_checksum,
    validate_ip_address,
    validate_medicare_id,
    validate_npi,
    validate_phone_e164,
    validate_ssn_format,
    validate_pesel,
    validate_portuguese_nif,
    validate_south_africa_id,
    validate_israeli_id,
    validate_routing_number,
    validate_pattern_with_context,
)

__all__ = [
    # PII
    "ALL_PII_PATTERNS",
    "PIICategory",
    "PIIPattern",
    "RiskLevel",
    # SQL
    "ALL_SQL_PATTERNS",
    "SQLInjectionType",
    "SQLPattern",
    "Severity",
    # Prompt
    "ALL_PROMPT_PATTERNS",
    "PromptInjectionType",
    "PromptPattern",
    # Validators
    "luhn_check",
    "validate_ein",
    "validate_iban_checksum",
    "validate_ip_address",
    "validate_medicare_id",
    "validate_npi",
    "validate_phone_e164",
    "validate_ssn_format",
    "validate_pesel",
    "validate_portuguese_nif",
    "validate_south_africa_id",
    "validate_israeli_id",
    "validate_routing_number",
    "validate_pattern_with_context",
]
