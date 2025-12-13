"""
Tests for ErrorSeverity class.

Verifies standard severity levels are defined and accessible.
"""


class TestErrorSeverity:
    """Tests for ErrorSeverity constants."""

    def test_severity_has_debug(self):
        """ErrorSeverity should have DEBUG."""
        from prism.view.errors import ErrorSeverity

        assert hasattr(ErrorSeverity, "DEBUG")
        assert ErrorSeverity.DEBUG == "DEBUG"

    def test_severity_has_info(self):
        """ErrorSeverity should have INFO."""
        from prism.view.errors import ErrorSeverity

        assert hasattr(ErrorSeverity, "INFO")
        assert ErrorSeverity.INFO == "INFO"

    def test_severity_has_warning(self):
        """ErrorSeverity should have WARNING."""
        from prism.view.errors import ErrorSeverity

        assert hasattr(ErrorSeverity, "WARNING")
        assert ErrorSeverity.WARNING == "WARNING"

    def test_severity_has_error(self):
        """ErrorSeverity should have ERROR."""
        from prism.view.errors import ErrorSeverity

        assert hasattr(ErrorSeverity, "ERROR")
        assert ErrorSeverity.ERROR == "ERROR"

    def test_severity_has_critical(self):
        """ErrorSeverity should have CRITICAL."""
        from prism.view.errors import ErrorSeverity

        assert hasattr(ErrorSeverity, "CRITICAL")
        assert ErrorSeverity.CRITICAL == "CRITICAL"

    def test_severity_values_are_strings(self):
        """All ErrorSeverity values should be strings."""
        from prism.view.errors import ErrorSeverity

        severities = [
            ErrorSeverity.DEBUG,
            ErrorSeverity.INFO,
            ErrorSeverity.WARNING,
            ErrorSeverity.ERROR,
            ErrorSeverity.CRITICAL,
        ]

        for severity in severities:
            assert isinstance(severity, str)

    def test_severity_is_enum_like(self):
        """ErrorSeverity should be usable like an enum."""
        from prism.view.errors import ErrorSeverity

        # Should be able to compare values
        assert ErrorSeverity.ERROR == "ERROR"
        assert ErrorSeverity.ERROR != ErrorSeverity.WARNING
