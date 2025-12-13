"""
Tests for ErrorCategory class.

Verifies standard error categories are defined and accessible.
"""


class TestErrorCategory:
    """Tests for ErrorCategory constants."""

    def test_category_has_configuration(self):
        """ErrorCategory should have CONFIGURATION."""
        from prism.view.errors import ErrorCategory

        assert hasattr(ErrorCategory, "CONFIGURATION")
        assert ErrorCategory.CONFIGURATION == "CONFIGURATION"

    def test_category_has_security(self):
        """ErrorCategory should have SECURITY."""
        from prism.view.errors import ErrorCategory

        assert hasattr(ErrorCategory, "SECURITY")
        assert ErrorCategory.SECURITY == "SECURITY"

    def test_category_has_database(self):
        """ErrorCategory should have DATABASE."""
        from prism.view.errors import ErrorCategory

        assert hasattr(ErrorCategory, "DATABASE")
        assert ErrorCategory.DATABASE == "DATABASE"

    def test_category_has_network(self):
        """ErrorCategory should have NETWORK."""
        from prism.view.errors import ErrorCategory

        assert hasattr(ErrorCategory, "NETWORK")
        assert ErrorCategory.NETWORK == "NETWORK"

    def test_category_has_validation(self):
        """ErrorCategory should have VALIDATION."""
        from prism.view.errors import ErrorCategory

        assert hasattr(ErrorCategory, "VALIDATION")
        assert ErrorCategory.VALIDATION == "VALIDATION"

    def test_category_has_filesystem(self):
        """ErrorCategory should have FILESYSTEM."""
        from prism.view.errors import ErrorCategory

        assert hasattr(ErrorCategory, "FILESYSTEM")
        assert ErrorCategory.FILESYSTEM == "FILESYSTEM"

    def test_category_has_runtime(self):
        """ErrorCategory should have RUNTIME."""
        from prism.view.errors import ErrorCategory

        assert hasattr(ErrorCategory, "RUNTIME")
        assert ErrorCategory.RUNTIME == "RUNTIME"

    def test_category_has_external(self):
        """ErrorCategory should have EXTERNAL."""
        from prism.view.errors import ErrorCategory

        assert hasattr(ErrorCategory, "EXTERNAL")
        assert ErrorCategory.EXTERNAL == "EXTERNAL"

    def test_category_values_are_strings(self):
        """All ErrorCategory values should be strings."""
        from prism.view.errors import ErrorCategory

        categories = [
            ErrorCategory.CONFIGURATION,
            ErrorCategory.SECURITY,
            ErrorCategory.DATABASE,
            ErrorCategory.NETWORK,
            ErrorCategory.VALIDATION,
            ErrorCategory.FILESYSTEM,
            ErrorCategory.RUNTIME,
            ErrorCategory.EXTERNAL,
        ]

        for category in categories:
            assert isinstance(category, str)

    def test_category_is_enum_like(self):
        """ErrorCategory should be usable like an enum."""
        from prism.view.errors import ErrorCategory

        # Should be able to compare values
        assert ErrorCategory.SECURITY == "SECURITY"
        assert ErrorCategory.SECURITY != ErrorCategory.DATABASE
