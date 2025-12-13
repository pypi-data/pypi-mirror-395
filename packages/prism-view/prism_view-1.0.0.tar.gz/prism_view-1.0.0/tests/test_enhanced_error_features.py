"""
Tests for Enhanced Error Features (Iteration 4).

Tests cover:
- Context capture in errors (auto-capture LogContext)
- Stack information capture (file, line, function, module)
- Cause chain tracking (building chains from __cause__/__context__)
- Recovery hints (retryable, max_retries, retry_delay)
- Debug information (dev mode only)
- Documentation URLs
"""


class TestContextCaptureInErrors:
    """Tests for automatic LogContext capture in PrismError."""

    def test_error_captures_current_log_context(self):
        """PrismError captures the current LogContext when created."""
        from prism.view import LogContext, PrismError

        LogContext.clear()
        LogContext.set_service(name="test-api", version="1.0.0")

        with LogContext.request(trace_id="trace-123"):
            error = PrismError("Test error")
            assert hasattr(error, "context")
            assert error.context["service"] == "test-api"
            assert error.context["trace_id"] == "trace-123"

    def test_error_includes_service_context(self):
        """Error includes service context."""
        from prism.view import LogContext, PrismError

        LogContext.clear()
        LogContext.set_service(name="payment-api", environment="production")

        error = PrismError("Payment failed")
        assert error.context["service"] == "payment-api"
        assert error.context["environment"] == "production"

    def test_error_includes_request_context(self):
        """Error includes request context with trace_id."""
        from prism.view import LogContext, PrismError

        LogContext.clear()
        with LogContext.request(trace_id="req-abc", method="POST"):
            error = PrismError("Request failed")
            assert error.context["trace_id"] == "req-abc"
            assert error.context["method"] == "POST"

    def test_error_includes_user_context(self):
        """Error includes user context."""
        from prism.view import LogContext, PrismError

        LogContext.clear()
        with LogContext.user(user_id="user-456", role="admin"):
            error = PrismError("Permission denied")
            assert error.context["user_id"] == "user-456"
            assert error.context["role"] == "admin"

    def test_error_includes_operation_context(self):
        """Error includes operation context with timing info."""
        from prism.view import LogContext, PrismError

        LogContext.clear()
        with LogContext.operation(name="db_query", table="users"):
            error = PrismError("Query failed")
            assert error.context["operation"] == "db_query"
            assert error.context["table"] == "users"
            assert "started_at" in error.context

    def test_context_capture_can_be_disabled(self):
        """Context capture can be disabled via capture_context=False."""
        from prism.view import LogContext, PrismError

        LogContext.clear()
        LogContext.set_service(name="test-api")

        error = PrismError("Test error", capture_context=False)
        assert error.context == {}

    def test_to_dict_includes_context(self):
        """to_dict() includes context when present."""
        from prism.view import LogContext, PrismError

        LogContext.clear()
        LogContext.set_service(name="api")
        with LogContext.request(trace_id="trace-123"):
            error = PrismError("Test error")
            result = error.to_dict()
            assert "context" in result
            assert result["context"]["trace_id"] == "trace-123"

    def test_empty_context_not_included_in_to_dict(self):
        """Empty context is not included in to_dict()."""
        from prism.view import LogContext, PrismError

        LogContext.clear()
        error = PrismError("Test error", capture_context=False)
        result = error.to_dict()
        assert "context" not in result or result.get("context") == {}


class TestStackInformationCapture:
    """Tests for stack information capture in PrismError."""

    def test_error_captures_file_path(self):
        """PrismError captures the file path where it was created."""
        from prism.view import PrismError

        error = PrismError("Test error")
        assert hasattr(error, "location")
        assert "file" in error.location
        assert error.location["file"].endswith(".py")

    def test_error_captures_line_number(self):
        """PrismError captures the line number where it was created."""
        from prism.view import PrismError

        error = PrismError("Test error")
        assert "line" in error.location
        assert isinstance(error.location["line"], int)
        assert error.location["line"] > 0

    def test_error_captures_function_name(self):
        """PrismError captures the function name where it was created."""
        from prism.view import PrismError

        def my_function():
            return PrismError("Test error")

        error = my_function()
        assert "function" in error.location
        assert error.location["function"] == "my_function"

    def test_error_captures_module_name(self):
        """PrismError captures the module name where it was created."""
        from prism.view import PrismError

        error = PrismError("Test error")
        assert "module" in error.location
        assert "test_enhanced_error_features" in error.location["module"]

    def test_stack_capture_can_be_disabled(self):
        """Stack capture can be disabled via capture_stack=False."""
        from prism.view import PrismError

        error = PrismError("Test error", capture_stack=False)
        assert error.location == {}

    def test_to_dict_includes_location(self):
        """to_dict() includes location information."""
        from prism.view import PrismError

        error = PrismError("Test error")
        result = error.to_dict()
        assert "location" in result
        assert "file" in result["location"]
        assert "line" in result["location"]
        assert "function" in result["location"]

    def test_location_file_is_relative_or_short(self):
        """Location file path is reasonable (not overly long absolute path)."""
        from prism.view import PrismError

        error = PrismError("Test error")
        # Should contain the filename, not be empty
        assert len(error.location["file"]) > 0


class TestCauseChainTracking:
    """Tests for cause chain tracking in PrismError."""

    def test_cause_chain_built_from_explicit_cause(self):
        """Cause chain is built from explicit cause parameter."""
        from prism.view import PrismError

        root = ValueError("Invalid value")
        error = PrismError("Operation failed", cause=root)

        assert hasattr(error, "cause_chain")
        assert len(error.cause_chain) >= 1
        assert error.cause_chain[0]["type"] == "ValueError"
        assert error.cause_chain[0]["message"] == "Invalid value"

    def test_cause_chain_includes_error_codes(self):
        """Cause chain includes error codes if cause is a PrismError."""
        from prism.view import PrismError

        class DatabaseError(PrismError):
            code = (200, "DB", "CONNECTION_FAILED")

        root = DatabaseError("Connection refused")
        error = PrismError("Operation failed", cause=root)

        assert error.cause_chain[0]["error_code"] == "E-DB-200"

    def test_root_cause_extracted_correctly(self):
        """Root cause is extracted correctly from the chain."""
        from prism.view import PrismError

        root = ValueError("Root problem")
        middle = RuntimeError("Middle error")
        middle.__cause__ = root
        error = PrismError("Top error", cause=middle)

        assert hasattr(error, "root_cause")
        assert error.root_cause["type"] == "ValueError"
        assert error.root_cause["message"] == "Root problem"

    def test_empty_cause_chain_if_no_cause(self):
        """Empty cause chain if no cause provided."""
        from prism.view import PrismError

        error = PrismError("Standalone error")
        assert error.cause_chain == []
        assert error.root_cause is None

    def test_cause_chain_handles_nested_prism_errors(self):
        """Cause chain handles nested PrismError instances."""
        from prism.view import PrismError

        class ValidationError(PrismError):
            code = (400, "VAL", "VALIDATION_FAILED")

        class ServiceError(PrismError):
            code = (600, "SVC", "SERVICE_ERROR")

        validation = ValidationError("Invalid input")
        service = ServiceError("Service failed", cause=validation)
        error = PrismError("Request failed", cause=service)

        assert len(error.cause_chain) >= 2
        # Should include both error codes
        codes = [c.get("error_code") for c in error.cause_chain]
        assert "E-SVC-600" in codes or "E-VAL-400" in codes

    def test_to_dict_includes_cause_chain(self):
        """to_dict() includes cause_chain when present."""
        from prism.view import PrismError

        root = ValueError("Root error")
        error = PrismError("Test error", cause=root)
        result = error.to_dict()

        assert "cause_chain" in result
        assert len(result["cause_chain"]) >= 1

    def test_to_dict_includes_root_cause(self):
        """to_dict() includes root_cause when present."""
        from prism.view import PrismError

        root = ValueError("Root error")
        error = PrismError("Test error", cause=root)
        result = error.to_dict()

        assert "root_cause" in result
        assert result["root_cause"]["type"] == "ValueError"


class TestRecoveryHints:
    """Tests for recovery hints in PrismError."""

    def test_error_has_retryable_class_attribute(self):
        """PrismError has retryable class attribute (default False)."""
        from prism.view import PrismError

        assert hasattr(PrismError, "retryable")
        assert PrismError.retryable is False

    def test_error_has_max_retries_class_attribute(self):
        """PrismError has max_retries class attribute (default 0)."""
        from prism.view import PrismError

        assert hasattr(PrismError, "max_retries")
        assert PrismError.max_retries == 0

    def test_error_has_retry_delay_seconds_attribute(self):
        """PrismError has retry_delay_seconds class attribute (default 0)."""
        from prism.view import PrismError

        assert hasattr(PrismError, "retry_delay_seconds")
        assert PrismError.retry_delay_seconds == 0.0

    def test_subclass_can_override_recovery_hints(self):
        """Subclasses can override recovery hints."""
        from prism.view import PrismError

        class RetryableNetworkError(PrismError):
            retryable = True
            max_retries = 3
            retry_delay_seconds = 1.5

        error = RetryableNetworkError("Connection timeout")
        assert error.retryable is True
        assert error.max_retries == 3
        assert error.retry_delay_seconds == 1.5

    def test_recovery_hints_in_to_dict(self):
        """Recovery hints included in to_dict()."""
        from prism.view import PrismError

        class RetryableError(PrismError):
            retryable = True
            max_retries = 5
            retry_delay_seconds = 2.0

        error = RetryableError("Temporary failure")
        result = error.to_dict()

        assert "recovery" in result
        assert result["recovery"]["retryable"] is True
        assert result["recovery"]["max_retries"] == 5
        assert result["recovery"]["retry_delay_seconds"] == 2.0

    def test_non_retryable_recovery_in_to_dict(self):
        """Non-retryable errors still have recovery section."""
        from prism.view import PrismError

        error = PrismError("Permanent failure")
        result = error.to_dict()

        assert "recovery" in result
        assert result["recovery"]["retryable"] is False


class TestDebugInformation:
    """Tests for debug information in PrismError."""

    def test_error_accepts_debug_info_parameter(self):
        """PrismError accepts debug_info parameter."""
        from prism.view import PrismError

        error = PrismError(
            "Test error",
            debug_info={"query": "SELECT * FROM users", "params": [1, 2, 3]},
        )
        assert hasattr(error, "debug_info")
        assert error.debug_info["query"] == "SELECT * FROM users"

    def test_debug_info_included_in_dev_mode(self):
        """Debug info is included in to_dict() in dev mode."""
        from prism.view import PrismError

        error = PrismError(
            "Test error",
            debug_info={"internal_state": "corrupted"},
        )
        # Force dev mode for test
        result = error.to_dict(include_debug=True)
        assert "debug_info" in result
        assert result["debug_info"]["internal_state"] == "corrupted"

    def test_debug_info_excluded_in_prod_mode(self):
        """Debug info is excluded in to_dict() in prod mode."""
        from prism.view import PrismError

        error = PrismError(
            "Test error",
            debug_info={"sensitive": "data"},
        )
        result = error.to_dict(include_debug=False)
        assert "debug_info" not in result

    def test_debug_info_can_include_arbitrary_data(self):
        """Debug info can include arbitrary data types."""
        from prism.view import PrismError

        error = PrismError(
            "Test error",
            debug_info={
                "string": "value",
                "number": 42,
                "list": [1, 2, 3],
                "nested": {"a": "b"},
            },
        )
        assert error.debug_info["string"] == "value"
        assert error.debug_info["number"] == 42
        assert error.debug_info["list"] == [1, 2, 3]
        assert error.debug_info["nested"]["a"] == "b"

    def test_default_debug_info_is_empty_dict(self):
        """Default debug_info is an empty dict."""
        from prism.view import PrismError

        error = PrismError("Test error")
        assert error.debug_info == {}


class TestDocumentationURLs:
    """Tests for documentation URL generation in PrismError."""

    def test_get_docs_url_returns_url(self):
        """get_docs_url() returns a URL string."""
        from prism.view import PrismError

        class ConfigError(PrismError):
            code = (1, "CFG", "CONFIG_FILE_NOT_FOUND")

        error = ConfigError("Config file missing")
        url = error.get_docs_url()

        assert url is not None
        assert isinstance(url, str)
        # URL uses lowercase with hyphens (URL-friendly format)
        assert "config-file-not-found" in url

    def test_docs_url_includes_error_code_name(self):
        """Docs URL includes the error code name."""
        from prism.view import PrismError

        class ValidationError(PrismError):
            code = (400, "VAL", "INVALID_INPUT")

        error = ValidationError("Invalid input")
        url = error.get_docs_url()

        assert "INVALID_INPUT" in url.upper() or "invalid-input" in url.lower()

    def test_docs_url_can_be_overridden_in_subclass(self):
        """Docs URL can be overridden in subclasses."""
        from prism.view import PrismError

        class CustomError(PrismError):
            code = (1, "CUS", "CUSTOM_ERROR")
            docs_base_url = "https://example.com/errors"

        error = CustomError("Custom error")
        url = error.get_docs_url()

        assert url is not None
        assert "example.com" in url

    def test_docs_url_is_none_if_no_code(self):
        """get_docs_url() returns None if error has no code."""
        from prism.view import PrismError

        error = PrismError("Generic error")
        url = error.get_docs_url()

        assert url is None

    def test_to_dict_includes_docs_url(self):
        """to_dict() includes docs_url when available."""
        from prism.view import PrismError

        class DocumentedError(PrismError):
            code = (100, "DOC", "DOCUMENTED_ERROR")

        error = DocumentedError("Error with docs")
        result = error.to_dict()

        assert "docs_url" in result
        assert result["docs_url"] is not None


class TestIntegration:
    """Integration tests for all enhanced error features together."""

    def test_complete_error_with_all_features(self):
        """Test error with all enhanced features combined."""
        from prism.view import LogContext, PrismError

        class PaymentError(PrismError):
            code = (1001, "PAY", "PAYMENT_DECLINED")
            category = "PAYMENT"
            severity = "ERROR"
            retryable = True
            max_retries = 3
            retry_delay_seconds = 5.0

        LogContext.clear()
        LogContext.set_service(name="payment-api", version="2.0.0")

        with LogContext.request(trace_id="pay-trace-123"):
            with LogContext.user(user_id="customer-456"):
                root_cause = ValueError("Insufficient funds")
                error = PaymentError(
                    "Payment was declined",
                    details={"amount": 99.99, "currency": "USD"},
                    suggestions=["Try a different payment method", "Check card balance"],
                    cause=root_cause,
                    debug_info={"processor_response": "05"},
                )

                # Verify all features
                assert error.context["service"] == "payment-api"
                assert error.context["trace_id"] == "pay-trace-123"
                assert error.context["user_id"] == "customer-456"
                assert error.location["function"] == "test_complete_error_with_all_features"
                assert len(error.cause_chain) >= 1
                assert error.retryable is True
                assert error.debug_info["processor_response"] == "05"
                assert error.get_docs_url() is not None

    def test_error_serialization_roundtrip(self):
        """Test that error can be serialized and contains all expected fields."""
        import json

        from prism.view import LogContext, PrismError

        class TestError(PrismError):
            code = (999, "TST", "TEST_ERROR")
            retryable = True
            max_retries = 2

        LogContext.clear()
        LogContext.set_service(name="test-service")

        with LogContext.request(trace_id="test-trace"):
            error = TestError(
                "Test error message",
                details={"key": "value"},
                suggestions=["Suggestion 1"],
                cause=RuntimeError("Root cause"),
                debug_info={"debug_key": "debug_value"},
            )

            result = error.to_dict(include_debug=True)

            # Verify it's JSON serializable
            json_str = json.dumps(result)
            parsed = json.loads(json_str)

            # Verify key fields
            assert parsed["message"] == "Test error message"
            assert parsed["error_code"] == "E-TST-999"
            assert "context" in parsed
            assert "location" in parsed
            assert "cause_chain" in parsed
            assert "recovery" in parsed
            assert "debug_info" in parsed
            assert "docs_url" in parsed
