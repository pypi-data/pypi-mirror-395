"""PII (Personally Identifiable Information) detection patterns.

Comprehensive patterns for GDPR, HIPAA, PCI-DSS and other regulatory frameworks.
See docs/PII-TAXONOMY.md for complete reference.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Pattern


class PIICategory(Enum):
    """PII category for risk assessment."""

    # GDPR Categories
    NATIONAL_ID = "national_id"
    PASSPORT = "passport"
    DRIVERS_LICENSE = "drivers_license"

    # Financial (PCI-DSS)
    CREDIT_CARD = "credit_card"
    BANK_ACCOUNT = "bank_account"
    IBAN = "iban"
    SWIFT_BIC = "swift_bic"

    # HIPAA
    SSN = "ssn"
    MEDICARE_ID = "medicare_id"
    MEDICAL_RECORD = "medical_record"

    # Contact Information
    EMAIL = "email"
    PHONE = "phone"
    IP_ADDRESS = "ip_address"
    MAC_ADDRESS = "mac_address"

    # Biometric (GDPR Art. 9)
    BIOMETRIC = "biometric"


class RiskLevel(Enum):
    """Risk level for PII exposure."""

    CRITICAL = "critical"  # Never store (CVV, PIN)
    HIGH = "high"  # Requires encryption (SSN, passport)
    MEDIUM = "medium"  # Requires consent (email, phone)
    LOW = "low"  # Public data


@dataclass
class PIIPattern:
    """PII detection pattern with metadata."""

    name: str
    category: PIICategory
    risk_level: RiskLevel
    pattern: Pattern[str]
    description: str
    regulation: str  # GDPR, HIPAA, PCI-DSS, etc.
    country: str = "GLOBAL"  # Specific country or GLOBAL
    context_keywords: list[str] | None = None  # Keywords that should appear nearby (±50 chars)
    requires_validation: bool = False  # Needs checksum/format validation
    examples: list[str] | None = None  # Example matches for testing
    gdpr_category: str | None = None  # GDPR Article 9 special category
    hipaa_identifier: bool = False  # Is this a HIPAA identifier?


# ============================================================================
# GDPR (EU) - Personal Data
# ============================================================================

# France
FRANCE_SIRET = PIIPattern(
    name="france_siret",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{3}\s?\d{3}\s?\d{3}\s?\d{5}\b"),
    description="France SIRET number (14 digits)",
    regulation="GDPR",
    country="FR",
)

FRANCE_SIREN = PIIPattern(
    name="france_siren",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{3}\s?\d{3}\s?\d{3}\b"),
    description="France SIREN number (9 digits)",
    regulation="GDPR",
    country="FR",
)

FRANCE_NIR = PIIPattern(
    name="france_nir",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b[12]\s?\d{2}\s?\d{2}\s?\d{2}\s?\d{3}\s?\d{3}\s?\d{2}\b"),
    description="France Social Security Number (15 digits)",
    regulation="GDPR",
    country="FR",
)

# UK
UK_NATIONAL_INSURANCE = PIIPattern(
    name="uk_national_insurance",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b[A-Z]{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?[A-Z]\b", re.IGNORECASE),
    description="UK National Insurance Number",
    regulation="GDPR",
    country="GB",
)

# Germany
GERMANY_TAX_ID = PIIPattern(
    name="germany_tax_id",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{2}\s?\d{3}\s?\d{3}\s?\d{3}\b"),
    description="Germany Tax ID (11 digits)",
    regulation="GDPR",
    country="DE",
)

# Spain
SPAIN_DNI = PIIPattern(
    name="spain_dni",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{8}-?[A-Z]\b", re.IGNORECASE),
    description="Spain DNI/NIE",
    regulation="GDPR",
    country="ES",
)

# Italy
ITALY_CODICE_FISCALE = PIIPattern(
    name="italy_codice_fiscale",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]\b", re.IGNORECASE),
    description="Italy Codice Fiscale",
    regulation="GDPR",
    country="IT",
)

# Netherlands
NETHERLANDS_BSN = PIIPattern(
    name="netherlands_bsn",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{8,9}\b"),
    description="Netherlands BSN (Citizen Service Number)",
    regulation="GDPR",
    country="NL",
)

# ============================================================================
# Financial Information (PCI-DSS)
# ============================================================================

# IBAN (International Bank Account Number)
IBAN = PIIPattern(
    name="iban",
    category=PIICategory.IBAN,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(
        r"\b[A-Z]{2}\d{2}\s?([A-Z0-9]{4}\s?){4,7}[A-Z0-9]{1,4}\b", re.IGNORECASE
    ),
    description="International Bank Account Number",
    regulation="GDPR",
)

# Credit Cards (Luhn validation recommended post-match)
CREDIT_CARD_VISA = PIIPattern(
    name="credit_card_visa",
    category=PIICategory.CREDIT_CARD,
    risk_level=RiskLevel.CRITICAL,
    pattern=re.compile(r"\b4\d{3}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"),
    description="Visa credit card (starts with 4)",
    regulation="PCI-DSS",
)

CREDIT_CARD_MASTERCARD = PIIPattern(
    name="credit_card_mastercard",
    category=PIICategory.CREDIT_CARD,
    risk_level=RiskLevel.CRITICAL,
    pattern=re.compile(r"\b5[1-5]\d{2}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"),
    description="Mastercard credit card (starts 51-55)",
    regulation="PCI-DSS",
)

CREDIT_CARD_AMEX = PIIPattern(
    name="credit_card_amex",
    category=PIICategory.CREDIT_CARD,
    risk_level=RiskLevel.CRITICAL,
    pattern=re.compile(r"\b3[47]\d{2}[-\s]?\d{6}[-\s]?\d{5}\b"),
    description="American Express (15 digits)",
    regulation="PCI-DSS",
)

CREDIT_CARD_DISCOVER = PIIPattern(
    name="credit_card_discover",
    category=PIICategory.CREDIT_CARD,
    risk_level=RiskLevel.CRITICAL,
    pattern=re.compile(r"\b6(?:011|5\d{2})[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"),
    description="Discover card (starts 6011 or 65)",
    regulation="PCI-DSS",
)

# SWIFT/BIC
SWIFT_BIC = PIIPattern(
    name="swift_bic",
    category=PIICategory.SWIFT_BIC,
    risk_level=RiskLevel.MEDIUM,
    pattern=re.compile(r"\b[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?\b", re.IGNORECASE),
    description="SWIFT/BIC code",
    regulation="GDPR",
)

# VAT Numbers
VAT_FRANCE = PIIPattern(
    name="vat_france",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.MEDIUM,
    pattern=re.compile(r"\bFR\s?[A-Z0-9]{2}\s?\d{9}\b", re.IGNORECASE),
    description="France VAT Number",
    regulation="GDPR",
    country="FR",
)

VAT_GERMANY = PIIPattern(
    name="vat_germany",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.MEDIUM,
    pattern=re.compile(r"\bDE\d{9}\b", re.IGNORECASE),
    description="Germany VAT Number",
    regulation="GDPR",
    country="DE",
)

VAT_UK = PIIPattern(
    name="vat_uk",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.MEDIUM,
    pattern=re.compile(r"\bGB\d{9}\b", re.IGNORECASE),
    description="UK VAT Number",
    regulation="GDPR",
    country="GB",
)

# ============================================================================
# HIPAA (US) - Protected Health Information
# ============================================================================

# Social Security Number
SSN = PIIPattern(
    name="ssn",
    category=PIICategory.SSN,
    risk_level=RiskLevel.CRITICAL,
    pattern=re.compile(r"\b\d{3}-?\d{2}-?\d{4}\b"),
    description="US Social Security Number",
    regulation="HIPAA",
    country="US",
)

# Medicare ID (new format 2018+)
MEDICARE_ID = PIIPattern(
    name="medicare_id",
    category=PIICategory.MEDICARE_ID,
    risk_level=RiskLevel.CRITICAL,
    pattern=re.compile(r"\b\d[A-Z]{2}\d-?[A-Z]{2}\d-?[A-Z]{2}\d{2}\b", re.IGNORECASE),
    description="US Medicare ID (new format)",
    regulation="HIPAA",
    country="US",
)

# Medical Record Number
MEDICAL_RECORD_NUMBER = PIIPattern(
    name="medical_record_number",
    category=PIICategory.MEDICAL_RECORD,
    risk_level=RiskLevel.CRITICAL,
    pattern=re.compile(r"\bMRN\s?\d{6,10}\b", re.IGNORECASE),
    description="Medical Record Number",
    regulation="HIPAA",
    country="US",
)

# National Provider Identifier
NPI = PIIPattern(
    name="npi",
    category=PIICategory.MEDICAL_RECORD,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{10}\b"),
    description="National Provider Identifier (10 digits)",
    regulation="HIPAA",
    country="US",
)

# ============================================================================
# Contact Information
# ============================================================================

EMAIL = PIIPattern(
    name="email",
    category=PIICategory.EMAIL,
    risk_level=RiskLevel.MEDIUM,
    pattern=re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", re.IGNORECASE
    ),
    description="Email address",
    regulation="GDPR",
)

PHONE_E164 = PIIPattern(
    name="phone_e164",
    category=PIICategory.PHONE,
    risk_level=RiskLevel.MEDIUM,
    pattern=re.compile(r"\+\d{1,3}\s?\d{1,4}\s?\d{1,4}\s?\d{1,4}\s?\d{1,9}"),
    description="Phone number (E.164 international format)",
    regulation="GDPR",
)

PHONE_US = PIIPattern(
    name="phone_us",
    category=PIICategory.PHONE,
    risk_level=RiskLevel.MEDIUM,
    pattern=re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"),
    description="US phone number",
    regulation="GDPR",
    country="US",
)

IP_V4 = PIIPattern(
    name="ipv4",
    category=PIICategory.IP_ADDRESS,
    risk_level=RiskLevel.LOW,
    pattern=re.compile(
        r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
        r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    ),
    description="IPv4 address",
    regulation="GDPR",
)

IP_V6 = PIIPattern(
    name="ipv6",
    category=PIICategory.IP_ADDRESS,
    risk_level=RiskLevel.LOW,
    pattern=re.compile(
        r"\b(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}\b", re.IGNORECASE
    ),
    description="IPv6 address",
    regulation="GDPR",
)

MAC_ADDRESS = PIIPattern(
    name="mac_address",
    category=PIICategory.MAC_ADDRESS,
    risk_level=RiskLevel.LOW,
    pattern=re.compile(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"),
    description="MAC address",
    regulation="GDPR",
)

# ============================================================================
# Asia-Pacific Identifiers
# ============================================================================

CHINA_ID = PIIPattern(
    name="china_id",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{17}[\dXx]\b"),
    description="China National ID (18 chars)",
    regulation="GDPR",
    country="CN",
)

INDIA_AADHAAR = PIIPattern(
    name="india_aadhaar",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.CRITICAL,
    pattern=re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b"),
    description="India Aadhaar Number",
    regulation="GDPR",
    country="IN",
)

INDIA_PAN = PIIPattern(
    name="india_pan",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b", re.IGNORECASE),
    description="India Permanent Account Number",
    regulation="GDPR",
    country="IN",
)

JAPAN_MY_NUMBER = PIIPattern(
    name="japan_my_number",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.CRITICAL,
    pattern=re.compile(r"\b\d{4}-?\d{4}-?\d{4}\b"),
    description="Japan My Number",
    regulation="GDPR",
    country="JP",
)

AUSTRALIA_TFN = PIIPattern(
    name="australia_tfn",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.CRITICAL,
    pattern=re.compile(r"\b\d{3}\s?\d{3}\s?\d{3}\b"),
    description="Australia Tax File Number",
    regulation="GDPR",
    country="AU",
)

SINGAPORE_NRIC = PIIPattern(
    name="singapore_nric",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b[STFG]\d{7}[A-Z]\b", re.IGNORECASE),
    description="Singapore NRIC",
    regulation="GDPR",
    country="SG",
)

# ============================================================================
# Latin America Identifiers
# ============================================================================

BRAZIL_CPF = PIIPattern(
    name="brazil_cpf",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"),
    description="Brazil CPF (Individual Tax ID)",
    regulation="LGPD",
    country="BR",
)

BRAZIL_CNPJ = PIIPattern(
    name="brazil_cnpj",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.MEDIUM,
    pattern=re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b"),
    description="Brazil CNPJ (Company Tax ID)",
    regulation="LGPD",
    country="BR",
)

MEXICO_RFC = PIIPattern(
    name="mexico_rfc",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b[A-Z]{3,4}\d{6}[A-Z0-9]{3}\b", re.IGNORECASE),
    description="Mexico RFC (Tax ID)",
    regulation="GDPR",
    country="MX",
)

MEXICO_CURP = PIIPattern(
    name="mexico_curp",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(
        r"\b[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d\b", re.IGNORECASE
    ),
    description="Mexico CURP (Unique Population Registry Code)",
    regulation="GDPR",
    country="MX",
)

ARGENTINA_DNI = PIIPattern(
    name="argentina_dni",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{1,2}\.\d{3}\.\d{3}\b"),
    description="Argentina DNI",
    regulation="GDPR",
    country="AR",
)

# ============================================================================
# Extended US Identifiers
# ============================================================================

US_ITIN = PIIPattern(
    name="us_itin",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b9\d{2}-[7-9]\d-\d{4}\b"),
    description="US Individual Taxpayer Identification Number",
    regulation="HIPAA",
    country="US",
    examples=["900-70-1234", "912-88-5678"],
    gdpr_category="special_category_data",
)

US_PASSPORT = PIIPattern(
    name="us_passport",
    category=PIICategory.PASSPORT,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b(?:[A-Z]\d{8}|\d{9})\b"),
    description="US Passport Number (new: letter + 8 digits, old: 9 digits)",
    regulation="GDPR",
    country="US",
    context_keywords=["passport"],
    requires_validation=True,
    examples=["A12345678", "123456789"],
    gdpr_category="special_category_data",
)

# ============================================================================
# Additional EU/UK Identifiers
# ============================================================================

POLISH_PESEL = PIIPattern(
    name="polish_pesel",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{11}\b"),
    description="Polish PESEL (11 digits with checksum)",
    regulation="GDPR",
    country="PL",
    context_keywords=["pesel", "poland", "polish"],
    requires_validation=True,
    examples=["44051401359", "92032112345"],
    gdpr_category="special_category_data",
)

BELGIAN_NATIONAL_NUMBER = PIIPattern(
    name="belgian_national_number",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{2}\.\d{2}\.\d{2}-\d{3}\.\d{2}\b"),
    description="Belgian National Number",
    regulation="GDPR",
    country="BE",
    examples=["85.07.30-033.84", "12.03.15-123.45"],
    gdpr_category="special_category_data",
)

SWEDISH_PERSONNUMMER = PIIPattern(
    name="swedish_personnummer",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{6}-?\d{4}\b|\b\d{8}-?\d{4}\b"),
    description="Swedish Personal Identity Number (Personnummer)",
    regulation="GDPR",
    country="SE",
    context_keywords=["personnummer", "sweden", "swedish"],
    examples=["701010-1234", "19850214-1234"],
    gdpr_category="special_category_data",
)

PORTUGUESE_NIF = PIIPattern(
    name="portuguese_nif",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b[1-9]\d{8}\b"),
    description="Portuguese Tax Identification Number (NIF)",
    regulation="GDPR",
    country="PT",
    context_keywords=["nif", "portugal", "portuguese", "fiscal"],
    requires_validation=True,
    examples=["123456789", "987654321"],
    gdpr_category="special_category_data",
)

IRISH_PPS = PIIPattern(
    name="irish_pps",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{7}[A-Z]{1,2}\b"),
    description="Irish Personal Public Service Number",
    regulation="GDPR",
    country="IE",
    context_keywords=["pps", "ireland", "irish"],
    examples=["1234567A", "9876543TW"],
    gdpr_category="special_category_data",
)

# ============================================================================
# Extended Financial Identifiers
# ============================================================================

CVV_CVC = PIIPattern(
    name="cvv_cvc",
    category=PIICategory.CREDIT_CARD,
    risk_level=RiskLevel.CRITICAL,
    pattern=re.compile(r"\b\d{3,4}\b"),
    description="Credit Card CVV/CVC Code",
    regulation="PCI-DSS",
    context_keywords=["cvv", "cvc", "security code", "card"],
    examples=["123", "4567"],
    gdpr_category="financial_data",
)

US_ROUTING_NUMBER = PIIPattern(
    name="us_routing_number",
    category=PIICategory.BANK_ACCOUNT,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{9}\b"),
    description="US Bank Routing Number (ABA)",
    regulation="PCI-DSS",
    country="US",
    context_keywords=["routing", "aba", "bank"],
    requires_validation=True,
    examples=["021000021", "111000025"],
    gdpr_category="financial_data",
)

CUSIP = PIIPattern(
    name="cusip",
    category=PIICategory.BANK_ACCOUNT,
    risk_level=RiskLevel.MEDIUM,
    pattern=re.compile(r"\b[A-Z0-9]{9}\b"),
    description="CUSIP (Committee on Uniform Securities Identification Procedures)",
    regulation="GDPR",
    context_keywords=["cusip", "security", "bond", "stock"],
    examples=["037833100", "459200101"],
    gdpr_category="financial_data",
)

BITCOIN_ADDRESS = PIIPattern(
    name="bitcoin_address",
    category=PIICategory.BANK_ACCOUNT,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b"),
    description="Bitcoin Wallet Address",
    regulation="GDPR",
    examples=["1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "3J98t1WpEZ73CNmYviecrnyiWrnqRhWNLy"],
    gdpr_category="financial_data",
)

ETHEREUM_ADDRESS = PIIPattern(
    name="ethereum_address",
    category=PIICategory.BANK_ACCOUNT,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b0x[a-fA-F0-9]{40}\b"),
    description="Ethereum Wallet Address",
    regulation="GDPR",
    examples=["0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2"],
    gdpr_category="financial_data",
)

# ============================================================================
# Extended Healthcare Identifiers
# ============================================================================

DEA_NUMBER = PIIPattern(
    name="dea_number",
    category=PIICategory.MEDICAL_RECORD,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b[A-Z]{2}\d{7}\b"),
    description="DEA (Drug Enforcement Administration) Number",
    regulation="HIPAA",
    country="US",
    context_keywords=["dea", "prescription", "prescriber"],
    examples=["AB1234563", "FG9876543"],
    gdpr_category="health_data",
)

NDC_CODE = PIIPattern(
    name="ndc_code",
    category=PIICategory.MEDICAL_RECORD,
    risk_level=RiskLevel.MEDIUM,
    pattern=re.compile(r"\b\d{4,5}-\d{3,4}-\d{1,2}\b"),
    description="National Drug Code",
    regulation="HIPAA",
    country="US",
    context_keywords=["ndc", "drug", "medication"],
    examples=["0777-3105-02", "12345-678-90"],
    gdpr_category="health_data",
)

ICD_CODE = PIIPattern(
    name="icd_code",
    category=PIICategory.MEDICAL_RECORD,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b[A-Z]\d{2}\.?\d{0,2}\b"),
    description="ICD Diagnosis Code",
    regulation="HIPAA",
    country="US",
    context_keywords=["icd", "diagnosis", "condition"],
    examples=["I10", "E11.9", "J44.1"],
    gdpr_category="health_data",
)

# ============================================================================
# Additional APAC Identifiers
# ============================================================================

SOUTH_KOREA_RRN = PIIPattern(
    name="south_korea_rrn",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{6}-[1-4]\d{6}\b"),
    description="South Korea Resident Registration Number",
    regulation="GDPR",
    country="KR",
    examples=["900101-1234567", "851231-2345678"],
    gdpr_category="special_category_data",
)

TAIWAN_NATIONAL_ID = PIIPattern(
    name="taiwan_national_id",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b[A-Z][12]\d{8}\b"),
    description="Taiwan National Identification Card",
    regulation="GDPR",
    country="TW",
    examples=["A123456789", "Z212345678"],
    gdpr_category="special_category_data",
)

HONG_KONG_ID = PIIPattern(
    name="hong_kong_id",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b[A-Z]{1,2}\d{6}\([0-9A]\)\b"),
    description="Hong Kong Identity Card",
    regulation="GDPR",
    country="HK",
    examples=["A123456(7)", "AB987654(A)"],
    gdpr_category="special_category_data",
)

MALAYSIA_NRIC = PIIPattern(
    name="malaysia_nric",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{6}-\d{2}-\d{4}\b"),
    description="Malaysia National Registration Identity Card",
    regulation="GDPR",
    country="MY",
    examples=["900101-01-1234", "851231-14-5678"],
    gdpr_category="special_category_data",
)

PHILIPPINES_SSS = PIIPattern(
    name="philippines_sss",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{2}-\d{7}-\d\b"),
    description="Philippines Social Security System Number",
    regulation="GDPR",
    country="PH",
    examples=["34-1234567-8", "12-9876543-2"],
    gdpr_category="special_category_data",
)

# ============================================================================
# Middle East/Africa Identifiers
# ============================================================================

UAE_EMIRATES_ID = PIIPattern(
    name="uae_emirates_id",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b784-\d{4}-\d{7}-\d\b"),
    description="UAE Emirates ID",
    regulation="GDPR",
    country="AE",
    examples=["784-1234-1234567-1", "784-2024-9876543-8"],
    gdpr_category="special_category_data",
)

SOUTH_AFRICA_ID = PIIPattern(
    name="south_africa_id",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{13}\b"),
    description="South African ID Number (13 digits)",
    regulation="GDPR",
    country="ZA",
    context_keywords=["south africa", "rsa", "id number"],
    requires_validation=True,
    examples=["9001015009087", "8505205800082"],
    gdpr_category="special_category_data",
)

ISRAEL_TEUDAT_ZEHUT = PIIPattern(
    name="israel_id",
    category=PIICategory.NATIONAL_ID,
    risk_level=RiskLevel.HIGH,
    pattern=re.compile(r"\b\d{9}\b"),
    description="Israeli ID Number (Teudat Zehut, 9 digits with checksum)",
    regulation="GDPR",
    country="IL",
    context_keywords=["teudat zehut", "israel", "israeli id"],
    requires_validation=True,
    examples=["123456789", "987654321"],
    gdpr_category="special_category_data",
)

# ============================================================================
# All Patterns Collection
# ============================================================================

ALL_PII_PATTERNS: list[PIIPattern] = [
    # GDPR - France
    FRANCE_SIRET,
    FRANCE_SIREN,
    FRANCE_NIR,
    VAT_FRANCE,
    # GDPR - UK
    UK_NATIONAL_INSURANCE,
    VAT_UK,
    # GDPR - Germany
    GERMANY_TAX_ID,
    VAT_GERMANY,
    # GDPR - Other EU
    SPAIN_DNI,
    ITALY_CODICE_FISCALE,
    NETHERLANDS_BSN,
    POLISH_PESEL,
    BELGIAN_NATIONAL_NUMBER,
    SWEDISH_PERSONNUMMER,
    PORTUGUESE_NIF,
    IRISH_PPS,
    # Financial
    IBAN,
    CREDIT_CARD_VISA,
    CREDIT_CARD_MASTERCARD,
    CREDIT_CARD_AMEX,
    CREDIT_CARD_DISCOVER,
    SWIFT_BIC,
    CVV_CVC,
    US_ROUTING_NUMBER,
    CUSIP,
    BITCOIN_ADDRESS,
    ETHEREUM_ADDRESS,
    # HIPAA - US
    SSN,
    US_ITIN,
    US_PASSPORT,
    MEDICARE_ID,
    MEDICAL_RECORD_NUMBER,
    NPI,
    DEA_NUMBER,
    NDC_CODE,
    ICD_CODE,
    # Contact
    EMAIL,
    PHONE_E164,
    PHONE_US,
    IP_V4,
    IP_V6,
    MAC_ADDRESS,
    # Asia-Pacific
    CHINA_ID,
    INDIA_AADHAAR,
    INDIA_PAN,
    JAPAN_MY_NUMBER,
    AUSTRALIA_TFN,
    SINGAPORE_NRIC,
    SOUTH_KOREA_RRN,
    TAIWAN_NATIONAL_ID,
    HONG_KONG_ID,
    MALAYSIA_NRIC,
    PHILIPPINES_SSS,
    # Latin America
    BRAZIL_CPF,
    BRAZIL_CNPJ,
    MEXICO_RFC,
    MEXICO_CURP,
    ARGENTINA_DNI,
    # Middle East/Africa
    UAE_EMIRATES_ID,
    SOUTH_AFRICA_ID,
    ISRAEL_TEUDAT_ZEHUT,
]


# ============================================================================
# Context Keywords for Enhanced Detection
# ============================================================================

PII_CONTEXT_KEYWORDS: dict[str, list[str]] = {
    "health": [
        "patient",
        "diagnosis",
        "treatment",
        "prescription",
        "medical",
        "doctor",
        "hospital",
        "clinic",
        "health",
        "medication",
    ],
    "financial": [
        "account",
        "card",
        "payment",
        "transaction",
        "bank",
        "balance",
        "credit",
        "debit",
        "invoice",
        "billing",
    ],
    "identity": [
        "passport",
        "license",
        "ssn",
        "national_id",
        "birth",
        "citizen",
        "identity",
        "tax_id",
        "social_security",
    ],
    "contact": [
        "address",
        "phone",
        "email",
        "contact",
        "mobile",
        "tel",
        "telephone",
        "cell",
        "fax",
    ],
    "biometric": [
        "fingerprint",
        "face",
        "iris",
        "voice",
        "dna",
        "biometric",
        "retina",
        "facial",
    ],
}
