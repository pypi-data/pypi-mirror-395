"""
StandardErrorCode constants for prism-view.

Provides Prism's built-in error codes organized by category.
Each code is a tuple of (number, category_prefix, name).

Code Ranges:
    001-099: Configuration errors (CFG)
    100-199: Security errors (SEC)
    200-299: Database errors (DB)
    300-399: Network errors (NET)
    400-499: Validation errors (VAL)
    500-599: Filesystem errors (FS)
    600-699: Runtime errors (RUN)

Example:
    >>> from prism.view.errors import StandardErrorCode
    >>> code = StandardErrorCode.CONFIG_FILE_NOT_FOUND
    >>> print(code)
    (1, 'CFG', 'CONFIG_FILE_NOT_FOUND')
    >>> print(StandardErrorCode.format(code))
    'E-CFG-001'
"""

from typing import Optional, Tuple


class StandardErrorCode:
    """
    Built-in error codes for Prism applications.

    Each error code is a tuple: (number, category_prefix, name)
    - number: Unique number within category (1-99 per category)
    - category_prefix: Short category code (CFG, SEC, DB, etc.)
    - name: Human-readable error name

    These are OPTIONAL - users can define their own error codes
    using the same tuple format.
    """

    # =========================================================================
    # Configuration Errors (001-099) - CFG
    # =========================================================================
    CONFIG_FILE_NOT_FOUND = (1, "CFG", "CONFIG_FILE_NOT_FOUND")
    CONFIG_PARSE_ERROR = (2, "CFG", "CONFIG_PARSE_ERROR")
    CONFIG_VALIDATION_ERROR = (3, "CFG", "CONFIG_VALIDATION_ERROR")
    CONFIG_MISSING_REQUIRED = (4, "CFG", "CONFIG_MISSING_REQUIRED")
    CONFIG_INVALID_VALUE = (5, "CFG", "CONFIG_INVALID_VALUE")
    CONFIG_SECRET_NOT_FOUND = (6, "CFG", "CONFIG_SECRET_NOT_FOUND")

    # =========================================================================
    # Security Errors (100-199) - SEC
    # =========================================================================
    AUTHENTICATION_FAILED = (100, "SEC", "AUTHENTICATION_FAILED")
    AUTHORIZATION_DENIED = (101, "SEC", "AUTHORIZATION_DENIED")
    TOKEN_EXPIRED = (102, "SEC", "TOKEN_EXPIRED")
    TOKEN_INVALID = (103, "SEC", "TOKEN_INVALID")
    CREDENTIALS_INVALID = (104, "SEC", "CREDENTIALS_INVALID")
    SESSION_EXPIRED = (105, "SEC", "SESSION_EXPIRED")
    ACCESS_DENIED = (106, "SEC", "ACCESS_DENIED")

    # =========================================================================
    # Database Errors (200-299) - DB
    # =========================================================================
    DATABASE_CONNECTION_FAILED = (200, "DB", "DATABASE_CONNECTION_FAILED")
    QUERY_FAILED = (201, "DB", "QUERY_FAILED")
    TRANSACTION_FAILED = (202, "DB", "TRANSACTION_FAILED")
    RECORD_NOT_FOUND = (203, "DB", "RECORD_NOT_FOUND")
    DUPLICATE_RECORD = (204, "DB", "DUPLICATE_RECORD")
    CONSTRAINT_VIOLATION = (205, "DB", "CONSTRAINT_VIOLATION")

    # =========================================================================
    # Network Errors (300-399) - NET
    # =========================================================================
    CONNECTION_TIMEOUT = (300, "NET", "CONNECTION_TIMEOUT")
    SERVICE_UNAVAILABLE = (301, "NET", "SERVICE_UNAVAILABLE")
    REQUEST_FAILED = (302, "NET", "REQUEST_FAILED")
    RESPONSE_INVALID = (303, "NET", "RESPONSE_INVALID")
    DNS_RESOLUTION_FAILED = (304, "NET", "DNS_RESOLUTION_FAILED")
    SSL_ERROR = (305, "NET", "SSL_ERROR")

    # =========================================================================
    # Validation Errors (400-499) - VAL
    # =========================================================================
    VALIDATION_FAILED = (400, "VAL", "VALIDATION_FAILED")
    INVALID_INPUT = (401, "VAL", "INVALID_INPUT")
    MISSING_FIELD = (402, "VAL", "MISSING_FIELD")
    INVALID_FORMAT = (403, "VAL", "INVALID_FORMAT")
    VALUE_OUT_OF_RANGE = (404, "VAL", "VALUE_OUT_OF_RANGE")
    TYPE_MISMATCH = (405, "VAL", "TYPE_MISMATCH")

    # =========================================================================
    # Filesystem Errors (500-599) - FS
    # =========================================================================
    FILE_NOT_FOUND = (500, "FS", "FILE_NOT_FOUND")
    PERMISSION_DENIED = (501, "FS", "PERMISSION_DENIED")
    FILE_READ_ERROR = (502, "FS", "FILE_READ_ERROR")
    FILE_WRITE_ERROR = (503, "FS", "FILE_WRITE_ERROR")
    DIRECTORY_NOT_FOUND = (504, "FS", "DIRECTORY_NOT_FOUND")
    DISK_FULL = (505, "FS", "DISK_FULL")

    # =========================================================================
    # Runtime Errors (600-699) - RUN
    # =========================================================================
    UNEXPECTED_ERROR = (600, "RUN", "UNEXPECTED_ERROR")
    OPERATION_FAILED = (601, "RUN", "OPERATION_FAILED")
    TIMEOUT = (602, "RUN", "TIMEOUT")
    RESOURCE_EXHAUSTED = (603, "RUN", "RESOURCE_EXHAUSTED")
    NOT_IMPLEMENTED = (604, "RUN", "NOT_IMPLEMENTED")
    INTERNAL_ERROR = (605, "RUN", "INTERNAL_ERROR")

    @classmethod
    def format(cls, code: Tuple[int, str, str], severity: Optional[str] = "ERROR") -> str:
        """
        Format an error code tuple as a string.

        Args:
            code: Error code tuple (number, category, name)
            severity: Severity level for prefix (ERROR -> E, WARNING -> W, etc.)

        Returns:
            Formatted string like "E-CFG-001"

        Example:
            >>> StandardErrorCode.format(StandardErrorCode.CONFIG_FILE_NOT_FOUND)
            'E-CFG-001'
            >>> StandardErrorCode.format(StandardErrorCode.CONFIG_FILE_NOT_FOUND, "WARNING")
            'W-CFG-001'
        """
        if not isinstance(code, tuple) or len(code) != 3:
            return str(code)

        number, category, _ = code

        # Get severity prefix (first letter, uppercase)
        if severity:
            prefix = severity[0].upper()
        else:
            prefix = "E"  # Default to Error

        return f"{prefix}-{category}-{number:03d}"
