"""
Tests for StandardErrorCode class.

Verifies built-in error codes use tuple format and are unique.
"""


class TestStandardErrorCode:
    """Tests for StandardErrorCode constants."""

    def test_error_code_uses_tuple_format(self):
        """Error codes should be tuples of (number, category, name)."""
        from prism.view.errors import StandardErrorCode

        # Check a sample error code
        code = StandardErrorCode.CONFIG_FILE_NOT_FOUND
        assert isinstance(code, tuple)
        assert len(code) == 3

        number, category, name = code
        assert isinstance(number, int)
        assert isinstance(category, str)
        assert isinstance(name, str)

    def test_config_file_not_found_code(self):
        """CONFIG_FILE_NOT_FOUND should have correct values."""
        from prism.view.errors import StandardErrorCode

        code = StandardErrorCode.CONFIG_FILE_NOT_FOUND
        number, category, name = code

        assert number == 1
        assert category == "CFG"
        assert name == "CONFIG_FILE_NOT_FOUND"

    def test_validation_failed_code(self):
        """VALIDATION_FAILED should have correct values."""
        from prism.view.errors import StandardErrorCode

        code = StandardErrorCode.VALIDATION_FAILED
        number, category, name = code

        assert category == "VAL"
        assert name == "VALIDATION_FAILED"

    def test_error_codes_are_unique(self):
        """All error codes should have unique (category, number) combinations."""
        from prism.view.errors import StandardErrorCode

        seen = set()
        for attr_name in dir(StandardErrorCode):
            if attr_name.startswith("_"):
                continue
            attr = getattr(StandardErrorCode, attr_name)
            if isinstance(attr, tuple) and len(attr) == 3:
                number, category, name = attr
                key = (category, number)
                assert key not in seen, f"Duplicate code: {category}-{number}"
                seen.add(key)

    def test_format_error_code(self):
        """StandardErrorCode.format() should return formatted string."""
        from prism.view.errors import StandardErrorCode

        code = StandardErrorCode.CONFIG_FILE_NOT_FOUND
        formatted = StandardErrorCode.format(code)

        # Should be like "E-CFG-001" (Error severity prefix)
        assert isinstance(formatted, str)
        assert "CFG" in formatted
        assert "001" in formatted

    def test_format_with_severity(self):
        """StandardErrorCode.format() should accept severity prefix."""
        from prism.view.errors import StandardErrorCode

        code = StandardErrorCode.CONFIG_FILE_NOT_FOUND

        # Error severity
        formatted_error = StandardErrorCode.format(code, severity="ERROR")
        assert formatted_error.startswith("E-")

        # Warning severity
        formatted_warning = StandardErrorCode.format(code, severity="WARNING")
        assert formatted_warning.startswith("W-")

        # Critical severity
        formatted_critical = StandardErrorCode.format(code, severity="CRITICAL")
        assert formatted_critical.startswith("C-")

    def test_has_configuration_errors(self):
        """Should have configuration error codes (001-099)."""
        from prism.view.errors import StandardErrorCode

        assert hasattr(StandardErrorCode, "CONFIG_FILE_NOT_FOUND")
        assert hasattr(StandardErrorCode, "CONFIG_PARSE_ERROR")
        assert hasattr(StandardErrorCode, "CONFIG_VALIDATION_ERROR")

    def test_has_security_errors(self):
        """Should have security error codes (100-199)."""
        from prism.view.errors import StandardErrorCode

        assert hasattr(StandardErrorCode, "AUTHENTICATION_FAILED")
        assert hasattr(StandardErrorCode, "AUTHORIZATION_DENIED")
        assert hasattr(StandardErrorCode, "TOKEN_EXPIRED")

    def test_has_database_errors(self):
        """Should have database error codes (200-299)."""
        from prism.view.errors import StandardErrorCode

        assert hasattr(StandardErrorCode, "DATABASE_CONNECTION_FAILED")
        assert hasattr(StandardErrorCode, "QUERY_FAILED")

    def test_has_network_errors(self):
        """Should have network error codes (300-399)."""
        from prism.view.errors import StandardErrorCode

        assert hasattr(StandardErrorCode, "CONNECTION_TIMEOUT")
        assert hasattr(StandardErrorCode, "SERVICE_UNAVAILABLE")

    def test_has_validation_errors(self):
        """Should have validation error codes (400-499)."""
        from prism.view.errors import StandardErrorCode

        assert hasattr(StandardErrorCode, "VALIDATION_FAILED")
        assert hasattr(StandardErrorCode, "INVALID_INPUT")

    def test_has_filesystem_errors(self):
        """Should have filesystem error codes (500-599)."""
        from prism.view.errors import StandardErrorCode

        assert hasattr(StandardErrorCode, "FILE_NOT_FOUND")
        assert hasattr(StandardErrorCode, "PERMISSION_DENIED")

    def test_has_runtime_errors(self):
        """Should have runtime error codes (600-699)."""
        from prism.view.errors import StandardErrorCode

        assert hasattr(StandardErrorCode, "UNEXPECTED_ERROR")
        assert hasattr(StandardErrorCode, "OPERATION_FAILED")
