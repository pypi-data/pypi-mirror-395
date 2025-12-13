"""
Secret scrubber for prism-view.

Provides automatic PII/secret redaction with extensible patterns.

Features:
    - Key-based scrubbing: Detects sensitive keys (password, token, secret, etc.)
    - Pattern-based scrubbing: Detects JWT tokens, credit cards, AWS keys
    - Extensible: Add custom key patterns and value patterns
    - Deep scrubbing: Handles nested dicts, lists, and mixed structures
    - Non-mutating: Creates copies, never modifies original data

Example:
    >>> from prism.view.scrubber import Scrubber, scrub
    >>>
    >>> # Use default scrubber
    >>> data = {"password": "secret123", "username": "john"}
    >>> scrub(data)
    {'password': '[REDACTED]', 'username': 'john'}
    >>>
    >>> # Add custom patterns
    >>> scrubber = Scrubber()
    >>> scrubber.add_key_pattern("ssn")
    >>> scrubber.scrub({"ssn": "123-45-6789"})
    {'ssn': '[REDACTED]'}
"""

import copy
import re
from typing import Any, Dict, List, Optional, Pattern, Set, Tuple


# Default sensitive key patterns (case-insensitive)
DEFAULT_SENSITIVE_KEYS: Set[str] = {
    "password",
    "passwd",
    "pwd",
    "secret",
    "token",
    "api_key",
    "apikey",
    "api-key",
    "auth",
    "authorization",
    "credential",
    "credentials",
    "private_key",
    "privatekey",
    "private-key",
    "access_token",
    "refresh_token",
    "bearer",
    "session_id",
    "sessionid",
    "cookie",
    "jwt",
}

# Key suffixes that indicate sensitive data
SENSITIVE_KEY_SUFFIXES: Set[str] = {
    "password",
    "secret",
    "token",
    "key",
    "auth",
    "credential",
}

# Key prefixes that indicate sensitive data
SENSITIVE_KEY_PREFIXES: Set[str] = {
    "password",
    "secret",
    "token",
    "auth",
}

# Default replacement text
DEFAULT_REPLACEMENT = "[REDACTED]"


class Scrubber:
    """
    Secret scrubber for automatic PII/secret redaction.

    Detects and redacts sensitive data based on:
    - Key names (password, token, secret, api_key, etc.)
    - Value patterns (JWT tokens, credit cards, AWS keys)

    Attributes:
        replacement: Text to replace sensitive values with

    Example:
        >>> scrubber = Scrubber()
        >>> scrubber.scrub({"password": "secret123"})
        {'password': '[REDACTED]'}
    """

    def __init__(self, replacement: str = DEFAULT_REPLACEMENT):
        """
        Initialize a Scrubber.

        Args:
            replacement: Text to replace sensitive values with (default: "[REDACTED]")
        """
        self.replacement = replacement

        # Sensitive key patterns (exact match or substring)
        self._sensitive_keys: Set[str] = set(DEFAULT_SENSITIVE_KEYS)
        self._sensitive_suffixes: Set[str] = set(SENSITIVE_KEY_SUFFIXES)
        self._sensitive_prefixes: Set[str] = set(SENSITIVE_KEY_PREFIXES)

        # Custom key patterns added by user
        self._custom_key_patterns: Set[str] = set()

        # Value patterns: list of (name, compiled_regex, replacement)
        self._value_patterns: List[Tuple[str, Pattern[str], str]] = []

        # Add default value patterns
        self._add_default_value_patterns()

    def _add_default_value_patterns(self) -> None:
        """Add default value patterns for common secrets."""
        # JWT tokens (eyJ...)
        self._value_patterns.append(
            (
                "jwt",
                re.compile(r"eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*"),
                "[JWT]",
            )
        )

        # Bearer tokens
        self._value_patterns.append(
            (
                "bearer",
                re.compile(r"Bearer\s+[A-Za-z0-9_\-\.]+", re.IGNORECASE),
                "Bearer [REDACTED]",
            )
        )

        # AWS Access Key IDs (start with AKIA)
        self._value_patterns.append(
            (
                "aws_key",
                re.compile(r"AKIA[0-9A-Z]{16}"),
                "[AWS_KEY]",
            )
        )

        # Credit card numbers (13-19 digits, with optional dashes/spaces)
        self._value_patterns.append(
            (
                "credit_card",
                re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
                "[CARD]",
            )
        )

        # password= in query strings or logs
        self._value_patterns.append(
            (
                "password_param",
                re.compile(r"password\s*[=:]\s*[^\s&]+", re.IGNORECASE),
                "password=[REDACTED]",
            )
        )

    def add_key_pattern(self, key: str) -> None:
        """
        Add a custom key pattern to detect.

        The key pattern is matched case-insensitively against data keys.

        Args:
            key: Key pattern to detect (e.g., "ssn", "drivers_license")

        Example:
            >>> scrubber = Scrubber()
            >>> scrubber.add_key_pattern("ssn")
            >>> scrubber.scrub({"ssn": "123-45-6789"})
            {'ssn': '[REDACTED]'}
        """
        self._custom_key_patterns.add(key.lower())

    def add_value_pattern(
        self,
        name: str,
        pattern: str,
        replacement: Optional[str] = None,
    ) -> None:
        """
        Add a custom value pattern to detect.

        The pattern is a regex that matches against string values.
        Matched portions are replaced with the replacement text.

        Args:
            name: Name for this pattern (for debugging)
            pattern: Regex pattern to match
            replacement: Replacement text (default: "[{NAME}]")

        Example:
            >>> scrubber = Scrubber()
            >>> scrubber.add_value_pattern("phone", r"\\d{3}-\\d{3}-\\d{4}", "[PHONE]")
            >>> scrubber.scrub({"contact": "Call 555-123-4567"})
            {'contact': 'Call [PHONE]'}
        """
        compiled = re.compile(pattern)
        repl = replacement or f"[{name.upper()}]"
        self._value_patterns.append((name, compiled, repl))

    def _is_sensitive_key(self, key: str) -> bool:
        """
        Check if a key is sensitive.

        A key is sensitive if:
        - It matches a known sensitive key exactly
        - It contains a sensitive substring
        - It starts with a sensitive prefix
        - It ends with a sensitive suffix
        - It matches a custom pattern

        Args:
            key: Key to check

        Returns:
            True if key is sensitive, False otherwise
        """
        key_lower = key.lower()

        # Exact match
        if key_lower in self._sensitive_keys:
            return True

        # Custom patterns
        if key_lower in self._custom_key_patterns:
            return True

        # Check if key contains sensitive word
        for sensitive in self._sensitive_keys:
            if sensitive in key_lower:
                return True

        # Check custom patterns as substrings too
        for pattern in self._custom_key_patterns:
            if pattern in key_lower:
                return True

        # Suffix check
        for suffix in self._sensitive_suffixes:
            if key_lower.endswith(suffix):
                return True

        # Prefix check
        for prefix in self._sensitive_prefixes:
            if key_lower.startswith(prefix):
                return True

        return False

    def _scrub_value(self, value: str) -> str:
        """
        Scrub patterns from a string value.

        Args:
            value: String value to scrub

        Returns:
            Scrubbed string with patterns replaced
        """
        result = value
        for _name, pattern, replacement in self._value_patterns:
            result = pattern.sub(replacement, result)
        return result

    def _scrub_recursive(self, data: Any) -> Any:
        """
        Recursively scrub data structure.

        Args:
            data: Data to scrub (dict, list, or scalar)

        Returns:
            Scrubbed copy of data
        """
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                if self._is_sensitive_key(str(key)):
                    # Sensitive key - redact entire value
                    if value is None:
                        result[key] = None
                    elif isinstance(value, bytes):
                        result[key] = self.replacement
                    else:
                        result[key] = self.replacement
                else:
                    # Non-sensitive key - recurse
                    result[key] = self._scrub_recursive(value)
            return result

        elif isinstance(data, list):
            return [self._scrub_recursive(item) for item in data]

        elif isinstance(data, str):
            # Apply value patterns to strings
            return self._scrub_value(data)

        elif isinstance(data, bytes):
            # Convert bytes to string and scrub
            try:
                decoded = data.decode("utf-8", errors="replace")
                return self._scrub_value(decoded)
            except Exception:
                return data

        else:
            # Scalars (int, float, bool, None) pass through
            return data

    def scrub(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scrub sensitive data from a dictionary.

        Creates a deep copy of the data and replaces sensitive values
        with redaction markers. The original data is not modified.

        Args:
            data: Dictionary to scrub

        Returns:
            Scrubbed copy of data

        Example:
            >>> scrubber = Scrubber()
            >>> scrubber.scrub({"password": "secret", "user": "john"})
            {'password': '[REDACTED]', 'user': 'john'}
        """
        # Deep copy to avoid modifying original
        data_copy = copy.deepcopy(data)
        return self._scrub_recursive(data_copy)


# Default scrubber instance
default_scrubber = Scrubber()


def scrub(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Scrub sensitive data using the default scrubber.

    Convenience function that uses the module-level default scrubber.

    Args:
        data: Dictionary to scrub

    Returns:
        Scrubbed copy of data

    Example:
        >>> from prism.view.scrubber import scrub
        >>> scrub({"password": "secret123"})
        {'password': '[REDACTED]'}
    """
    return default_scrubber.scrub(data)
