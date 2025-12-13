"""Mapping of PII patterns to their validation functions."""

from .validators import (
    luhn_check,
    validate_ssn_format,
    validate_iban_checksum,
    validate_medicare_id,
    validate_npi,
    validate_ein,
    validate_phone_e164,
    validate_ip_address,
    validate_pesel,
    validate_portuguese_nif,
    validate_south_africa_id,
    validate_israeli_id,
    validate_routing_number,
)

# Mapping of pattern name to validation function
VALIDATION_FUNCTIONS = {
    # Credit cards
    "credit_card_visa": luhn_check,
    "credit_card_mastercard": luhn_check,
    "credit_card_amex": luhn_check,
    "credit_card_discover": luhn_check,
    
    # US IDs
    "ssn": validate_ssn_format,
    "medicare_id": validate_medicare_id,
    "npi": validate_npi,
    "us_ein": validate_ein,
    
    # EU IDs
    "iban": validate_iban_checksum,
    "polish_pesel": validate_pesel,
    "portuguese_nif": validate_portuguese_nif,
    
    # Other IDs
    "south_africa_id": validate_south_africa_id,
    "israel_id": validate_israeli_id,
    
    # Financial
    "us_routing_number": validate_routing_number,
    
    # Contact
    "phone_e164": validate_phone_e164,
    "ipv4": validate_ip_address,
    "ipv6": validate_ip_address,
}


def get_validation_function(pattern_name: str):
    """Get validation function for a pattern."""
    return VALIDATION_FUNCTIONS.get(pattern_name)
