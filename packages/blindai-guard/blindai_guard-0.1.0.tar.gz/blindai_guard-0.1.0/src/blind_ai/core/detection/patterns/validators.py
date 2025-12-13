"""Validation functions for PII patterns.

This module contains validation algorithms for credit cards, SSNs, and other
PII patterns to reduce false positives.
"""


def luhn_check(card_number: str) -> bool:
    """Validate credit card using Luhn algorithm.

    The Luhn algorithm (also known as "modulus 10" or "mod 10" algorithm)
    is a checksum formula used to validate credit card numbers.

    Args:
        card_number: Card number (may include spaces/dashes)

    Returns:
        True if valid by Luhn algorithm, False otherwise

    Example:
        >>> luhn_check("4532-1234-5678-9010")
        True
        >>> luhn_check("1234-5678-9012-3456")
        False
    """
    # Remove non-digit characters
    digits = "".join(c for c in card_number if c.isdigit())

    if len(digits) < 13 or len(digits) > 19:
        return False

    # Reject all zeros
    if digits == "0" * len(digits):
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


def validate_ssn_format(ssn: str) -> bool:
    """Validate US SSN format and reject known invalid patterns.

    Rejects:
    - Area number (first 3 digits): 000, 666, 900-999
    - Group number (middle 2 digits): 00
    - Serial number (last 4 digits): 0000

    Args:
        ssn: Social Security Number (may include dashes)

    Returns:
        True if format is valid, False otherwise

    Example:
        >>> validate_ssn_format("123-45-6789")
        True
        >>> validate_ssn_format("000-45-6789")
        False
        >>> validate_ssn_format("666-45-6789")
        False
    """
    # Remove non-digit characters
    digits = "".join(c for c in ssn if c.isdigit())

    if len(digits) != 9:
        return False

    area = int(digits[:3])
    group = int(digits[3:5])
    serial = int(digits[5:])

    # Invalid SSN patterns
    if area == 0 or area == 666 or area >= 900:
        return False
    if group == 0 or serial == 0:
        return False

    return True


def validate_iban_checksum(iban: str) -> bool:
    """Validate IBAN using modulo-97 checksum.

    The IBAN check digits are calculated using mod-97 algorithm.

    Args:
        iban: International Bank Account Number (may include spaces)

    Returns:
        True if checksum is valid, False otherwise

    Example:
        >>> validate_iban_checksum("GB82 WEST 1234 5698 7654 32")
        True
        >>> validate_iban_checksum("GB00 WEST 1234 5698 7654 32")
        False
    """
    # Remove spaces and convert to uppercase
    iban_clean = "".join(iban.split()).upper()

    # IBAN must be at least 15 characters (shortest valid IBAN)
    if len(iban_clean) < 15 or len(iban_clean) > 34:
        return False

    # Check if it starts with 2 letters and 2 digits
    if not (iban_clean[:2].isalpha() and iban_clean[2:4].isdigit()):
        return False

    # Move first 4 characters to end
    rearranged = iban_clean[4:] + iban_clean[:4]

    # Replace letters with numbers (A=10, B=11, ..., Z=35)
    numeric_string = ""
    for char in rearranged:
        if char.isalpha():
            numeric_string += str(ord(char) - ord("A") + 10)
        else:
            numeric_string += char

    # Check if mod 97 equals 1
    return int(numeric_string) % 97 == 1


def validate_medicare_id(medicare_id: str) -> bool:
    """Validate new Medicare ID format (MBI).

    New Medicare Beneficiary Identifier (MBI) format (2018+):
    - 11 characters
    - Positions 1, 4, 7, 10: Numeric (1-9)
    - Positions 2, 5, 8, 11: Alphabetic (excludes S, L, O, I, B, Z)
    - Positions 3, 6, 9: Alphanumeric (excludes S, L, O, I, B, Z)

    Args:
        medicare_id: Medicare Beneficiary Identifier

    Returns:
        True if format matches MBI pattern, False otherwise

    Example:
        >>> validate_medicare_id("1EG4-TE5-MK73")
        True
        >>> validate_medicare_id("1SG4-TE5-MK73")  # S is excluded
        False
    """
    # Remove non-alphanumeric characters
    mbi_clean = "".join(c for c in medicare_id.upper() if c.isalnum())

    if len(mbi_clean) != 11:
        return False

    # Characters to exclude
    excluded = set("SLOIBZ")

    # Position 1: Numeric 1-9
    if not mbi_clean[0].isdigit() or mbi_clean[0] == "0":
        return False

    # Position 2: Alpha (excluded chars)
    if not mbi_clean[1].isalpha() or mbi_clean[1] in excluded:
        return False

    # Position 3: Alphanumeric (excluded chars)
    if not mbi_clean[2].isalnum() or mbi_clean[2] in excluded:
        return False

    # Position 4: Numeric 0-9
    if not mbi_clean[3].isdigit():
        return False

    # Position 5: Alpha (excluded chars)
    if not mbi_clean[4].isalpha() or mbi_clean[4] in excluded:
        return False

    # Position 6: Alphanumeric (excluded chars)
    if not mbi_clean[5].isalnum() or mbi_clean[5] in excluded:
        return False

    # Position 7: Numeric 0-9
    if not mbi_clean[6].isdigit():
        return False

    # Position 8: Alpha (excluded chars)
    if not mbi_clean[7].isalpha() or mbi_clean[7] in excluded:
        return False

    # Position 9: Alphanumeric (excluded chars)
    if not mbi_clean[8].isalnum() or mbi_clean[8] in excluded:
        return False

    # Position 10: Numeric 0-9
    if not mbi_clean[9].isdigit():
        return False

    # Position 11: Alpha (excluded chars)
    if not mbi_clean[10].isalpha() or mbi_clean[10] in excluded:
        return False

    return True


def validate_npi(npi: str) -> bool:
    """Validate National Provider Identifier (NPI) using Luhn algorithm.

    NPI is a 10-digit identifier for healthcare providers in the US.
    It uses the Luhn algorithm for validation.

    Args:
        npi: National Provider Identifier

    Returns:
        True if valid NPI, False otherwise

    Example:
        >>> validate_npi("1234567893")
        True
        >>> validate_npi("1234567890")
        False
    """
    # Remove non-digit characters
    digits = "".join(c for c in npi if c.isdigit())

    if len(digits) != 10:
        return False

    # NPI uses Luhn algorithm with prefix 80840
    # Add prefix for validation
    full_number = "80840" + digits

    # Apply Luhn algorithm
    total = 0
    reverse_digits = full_number[::-1]

    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n

    return total % 10 == 0


def validate_ein(ein: str) -> bool:
    """Validate US Employer Identification Number (EIN) format.

    EIN format: XX-XXXXXXX (9 digits total)
    First 2 digits (campus code) must be between 01-99 (excluding some ranges)

    Args:
        ein: Employer Identification Number

    Returns:
        True if format is valid, False otherwise

    Example:
        >>> validate_ein("12-3456789")
        True
        >>> validate_ein("00-3456789")
        False
    """
    # Remove non-digit characters
    digits = "".join(c for c in ein if c.isdigit())

    if len(digits) != 9:
        return False

    # Campus code (first 2 digits)
    campus_code = int(digits[:2])

    # Valid campus codes are 01-06, 10-16, 20-27, 30-39, 40-48,
    # 50-59, 60-67, 71-77, 80-88, 90-99
    valid_ranges = [
        (1, 6),
        (10, 16),
        (20, 27),
        (30, 39),
        (40, 48),
        (50, 59),
        (60, 67),
        (71, 77),
        (80, 88),
        (90, 99),
    ]

    for start, end in valid_ranges:
        if start <= campus_code <= end:
            return True

    return False


def validate_phone_e164(phone: str) -> bool:
    """Validate phone number in E.164 format.

    E.164 format: +[country code][subscriber number]
    - Starts with +
    - Country code: 1-3 digits
    - Subscriber number: up to 15 digits total

    Args:
        phone: Phone number

    Returns:
        True if valid E.164 format, False otherwise

    Example:
        >>> validate_phone_e164("+1-202-555-0173")
        True
        >>> validate_phone_e164("202-555-0173")
        False
    """
    # Must start with +
    if not phone.strip().startswith("+"):
        return False

    # Remove all non-digit characters except leading +
    digits = "".join(c for c in phone if c.isdigit())

    # E.164 allows 1-15 digits after country code
    if len(digits) < 4 or len(digits) > 15:
        return False

    return True


def validate_ip_address(ip: str) -> bool:
    """Validate IPv4 or IPv6 address format.

    Args:
        ip: IP address string

    Returns:
        True if valid IPv4 or IPv6, False otherwise

    Example:
        >>> validate_ip_address("192.168.1.1")
        True
        >>> validate_ip_address("2001:0db8:85a3::8a2e:0370:7334")
        True
        >>> validate_ip_address("256.1.1.1")
        False
    """
    # Try IPv4
    if "." in ip:
        parts = ip.split(".")
        if len(parts) != 4:
            return False

        try:
            for part in parts:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            return True
        except ValueError:
            return False

    # Try IPv6
    if ":" in ip:
        # Simplified IPv6 validation
        parts = ip.split(":")

        # Must have at least 2 parts
        if len(parts) < 3:
            return False

        # Check for double colon (::)
        has_double_colon = "" in parts

        # Each part must be valid hex (0-4 characters)
        for part in parts:
            if part == "":
                continue  # Skip empty parts from ::

            if len(part) > 4:
                return False

            try:
                int(part, 16)
            except ValueError:
                return False

        return True

    return False


def validate_pesel(pesel: str) -> bool:
    """Validate Polish PESEL using checksum algorithm."""
    digits = "".join(c for c in pesel if c.isdigit())
    if len(digits) != 11:
        return False
    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    total = sum(int(digits[i]) * weights[i] for i in range(10))
    checksum = (10 - (total % 10)) % 10
    return int(digits[10]) == checksum


def validate_portuguese_nif(nif: str) -> bool:
    """Validate Portuguese NIF using checksum."""
    digits = "".join(c for c in nif if c.isdigit())
    if len(digits) != 9 or digits[0] == "0":
        return False
    total = sum(int(digits[i]) * (9 - i) for i in range(8))
    checksum = 11 - (total % 11)
    if checksum >= 10:
        checksum = 0
    return int(digits[8]) == checksum


def validate_south_africa_id(id_number: str) -> bool:
    """Validate South African ID using Luhn algorithm."""
    digits = "".join(c for c in id_number if c.isdigit())
    if len(digits) != 13:
        return False
    # Validate date
    month, day = int(digits[2:4]), int(digits[4:6])
    if month < 1 or month > 12 or day < 1 or day > 31:
        return False
    # Luhn algorithm
    total = 0
    for i, digit in enumerate(digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def validate_israeli_id(id_number: str) -> bool:
    """Validate Israeli ID using checksum."""
    digits = "".join(c for c in id_number if c.isdigit())
    if len(digits) != 9:
        return False
    total = 0
    for i, digit in enumerate(digits):
        n = int(digit)
        if (i + 1) % 2 == 0:
            n *= 2
        if n > 9:
            n = (n // 10) + (n % 10)
        total += n
    return total % 10 == 0


def validate_routing_number(routing: str) -> bool:
    """Validate US bank routing number (ABA)."""
    digits = "".join(c for c in routing if c.isdigit())
    if len(digits) != 9:
        return False
    checksum = (
        3 * (int(digits[0]) + int(digits[3]) + int(digits[6])) +
        7 * (int(digits[1]) + int(digits[4]) + int(digits[7])) +
        (int(digits[2]) + int(digits[5]) + int(digits[8]))
    )
    return checksum % 10 == 0


def validate_pattern_with_context(
    text: str,
    match_start: int,
    match_end: int,
    context_keywords: list[str],
    window_size: int = 50
) -> bool:
    """Check if context keywords appear near the match."""
    if not context_keywords:
        return True
    context_start = max(0, match_start - window_size)
    context_end = min(len(text), match_end + window_size)
    context = text[context_start:context_end].lower()
    return any(keyword.lower() in context for keyword in context_keywords)
