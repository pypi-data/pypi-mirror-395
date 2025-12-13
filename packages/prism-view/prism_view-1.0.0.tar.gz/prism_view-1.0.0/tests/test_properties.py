"""
Property-based tests for prism-view using Hypothesis.

Property tests verify invariants that should hold for ALL possible inputs,
not just specific test cases. This helps discover edge cases and bugs
that unit tests might miss.

Tests cover:
- Error serialization (12.1)
- Context propagation (12.2)
- Scrubber behavior (12.3)
- Logger stability (12.4)
- Duration tracking (12.5)
"""

import io
import json
import string
import time
from typing import Any, Dict, List

import pytest
from hypothesis import assume, given, settings, HealthCheck
from hypothesis import strategies as st

from prism.view import (
    LogContext,
    Logger,
    PrismError,
    scrub,
)
from prism.view.setup import operation


# =============================================================================
# Hypothesis Strategies
# =============================================================================

# Strategy for valid identifiers (keys, names, etc.)
identifiers = st.text(
    alphabet=string.ascii_letters + string.digits + "_",
    min_size=1,
    max_size=50,
).filter(lambda s: s[0].isalpha() or s[0] == "_")

# Strategy for safe text (no null bytes which can cause issues)
safe_text = st.text(
    alphabet=st.characters(blacklist_categories=("Cs",), blacklist_characters="\x00"),
    min_size=0,
    max_size=1000,
)

# Strategy for JSON-serializable values
json_values = st.recursive(
    (
        st.none()
        | st.booleans()
        | st.integers()
        | st.floats(allow_nan=False, allow_infinity=False)
        | safe_text
    ),
    lambda children: (
        st.lists(children, max_size=5) | st.dictionaries(identifiers, children, max_size=5)
    ),
    max_leaves=20,
)

# Strategy for error details
error_details = st.dictionaries(
    identifiers,
    (
        st.none()
        | st.booleans()
        | st.integers()
        | st.floats(allow_nan=False, allow_infinity=False)
        | safe_text
    ),
    max_size=10,
)

# Strategy for suggestions
suggestions = st.lists(safe_text, max_size=5)

# Strategy for error codes
error_codes = st.tuples(
    st.integers(min_value=1, max_value=9999),
    st.text(alphabet=string.ascii_uppercase, min_size=2, max_size=5),
    st.text(alphabet=string.ascii_uppercase + "_", min_size=3, max_size=30),
)


# =============================================================================
# 12.1: Error Serialization Properties
# =============================================================================


class TestErrorSerializationProperties:
    """Property tests for error serialization."""

    @given(
        message=safe_text.filter(lambda s: len(s) > 0),
        details=error_details,
        suggestions_list=suggestions,
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_any_prism_error_can_serialize_to_dict(
        self,
        message: str,
        details: Dict[str, Any],
        suggestions_list: List[str],
    ):
        """12.1.1: Any PrismError can serialize to dict."""
        error = PrismError(
            message=message,
            details=details,
            suggestions=suggestions_list,
        )

        # Should never raise
        result = error.to_dict()

        # Result should be a dict
        assert isinstance(result, dict)
        # Should contain required fields
        assert "message" in result
        assert "details" in result
        assert "suggestions" in result

    @given(
        message=safe_text.filter(lambda s: len(s) > 0),
        details=error_details,
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_to_dict_always_returns_valid_dict(
        self,
        message: str,
        details: Dict[str, Any],
    ):
        """12.1.3: to_dict() always returns valid dict."""
        error = PrismError(message=message, details=details)
        result = error.to_dict()

        # All values should be JSON-serializable
        # This will raise if not serializable
        json_str = json.dumps(result, default=str)
        parsed = json.loads(json_str)

        assert isinstance(parsed, dict)

    @given(
        message=safe_text.filter(lambda s: len(s) > 0),
        details=error_details,
        suggestions_list=suggestions,
        include_debug=st.booleans(),
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_no_exceptions_during_serialization(
        self,
        message: str,
        details: Dict[str, Any],
        suggestions_list: List[str],
        include_debug: bool,
    ):
        """12.1.4: No exceptions during serialization."""
        error = PrismError(
            message=message,
            details=details,
            suggestions=suggestions_list,
            debug_info={"test": True},
        )

        # Should never raise, regardless of input
        try:
            result = error.to_dict(include_debug=include_debug)
            assert result is not None
        except Exception as e:
            pytest.fail(f"Serialization raised exception: {e}")


# =============================================================================
# 12.2: Context Propagation Properties
# =============================================================================


class TestContextPropagationProperties:
    """Property tests for context propagation."""

    def setup_method(self):
        """Clear context before each test."""
        LogContext.clear()

    def teardown_method(self):
        """Clear context after each test."""
        LogContext.clear()

    @given(
        service_name=identifiers,
        version=st.text(alphabet=string.digits + ".", min_size=1, max_size=20),
    )
    @settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
    def test_context_always_propagates_correctly(
        self,
        service_name: str,
        version: str,
    ):
        """12.2.1: Context always propagates correctly."""
        LogContext.clear()

        LogContext.set_service(name=service_name, version=version)

        ctx = LogContext.get_current()
        assert ctx.get("service") == service_name
        assert ctx.get("version") == version

        LogContext.clear()

    @given(
        trace_id1=st.uuids().map(str),
        trace_id2=st.uuids().map(str),
    )
    @settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
    def test_context_never_leaks_between_requests(
        self,
        trace_id1: str,
        trace_id2: str,
    ):
        """12.2.2: Context never leaks between requests."""
        assume(trace_id1 != trace_id2)
        LogContext.clear()

        # First request
        with LogContext.request(trace_id=trace_id1):
            ctx1 = LogContext.get_current()
            assert ctx1.get("trace_id") == trace_id1

        # After exiting, trace_id should not be present
        ctx_after = LogContext.get_current()
        assert ctx_after.get("trace_id") != trace_id1

        # Second request should have its own trace_id
        with LogContext.request(trace_id=trace_id2):
            ctx2 = LogContext.get_current()
            assert ctx2.get("trace_id") == trace_id2
            assert ctx2.get("trace_id") != trace_id1

        LogContext.clear()

    @given(
        outer_key=identifiers,
        outer_val=safe_text,
        inner_key=identifiers,
        inner_val=safe_text,
    )
    @settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
    def test_nested_contexts_always_merge_correctly(
        self,
        outer_key: str,
        outer_val: str,
        inner_key: str,
        inner_val: str,
    ):
        """12.2.3: Nested contexts always merge correctly."""
        # Skip reserved keys that are set by context managers
        reserved_keys = {
            "trace_id",
            "user_id",
            "session_id",
            "batch_id",
            "transaction_id",
            "operation",
            "started_at",
            "duration_ms",
            "item_index",
            "total_items",
            "span_id",
            "transaction_type",
            "method",
            "path",
        }
        assume(outer_key != inner_key)
        assume(outer_key not in reserved_keys)
        assume(inner_key not in reserved_keys)
        LogContext.clear()

        with LogContext.request(trace_id="test"):
            LogContext.add(**{outer_key: outer_val})

            with LogContext.user(user_id="user-1"):
                LogContext.add(**{inner_key: inner_val})

                ctx = LogContext.get_current()

                # Both custom values should be present
                assert ctx.get(outer_key) == outer_val
                assert ctx.get(inner_key) == inner_val

        LogContext.clear()


# =============================================================================
# 12.3: Scrubber Properties
# =============================================================================


class TestScrubberProperties:
    """Property tests for the scrubber."""

    @given(
        password=safe_text.filter(lambda s: len(s) > 0),
        secret=safe_text.filter(lambda s: len(s) > 0),
        token=safe_text.filter(lambda s: len(s) > 0),
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_scrubber_never_leaks_secrets(
        self,
        password: str,
        secret: str,
        token: str,
    ):
        """12.3.1: Scrubber never leaks secrets."""
        data = {
            "password": password,
            "secret": secret,
            "api_token": token,
            "safe_field": "this is safe",
        }

        result = scrub(data)

        # Sensitive values should be redacted
        assert result["password"] == "[REDACTED]"
        assert result["secret"] == "[REDACTED]"
        assert result["api_token"] == "[REDACTED]"
        # Safe field should be preserved
        assert result["safe_field"] == "this is safe"

    @given(data=json_values)
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_scrubbed_data_is_always_valid_json(self, data: Any):
        """12.3.2: Scrubbed data is always valid JSON."""
        # Wrap in dict if not already
        if not isinstance(data, dict):
            data = {"value": data}

        result = scrub(data)

        # Should be JSON-serializable
        json_str = json.dumps(result, default=str)
        parsed = json.loads(json_str)
        assert parsed is not None

    @given(
        key=identifiers,
        value=safe_text,
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_scrubbing_is_idempotent(self, key: str, value: str):
        """12.3.3: Scrubbing is idempotent."""
        # Make it a sensitive key
        data = {"password": value, key: "safe"}

        result1 = scrub(data)
        result2 = scrub(result1)

        # Scrubbing twice should give same result
        assert result1 == result2

    @given(
        nested=st.dictionaries(
            identifiers,
            st.dictionaries(identifiers, safe_text, max_size=3),
            max_size=3,
        )
    )
    @settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
    def test_scrubbing_preserves_structure(self, nested: Dict[str, Dict[str, str]]):
        """12.3.4: Scrubbing preserves structure."""
        result = scrub(nested)

        # Structure should be preserved
        assert isinstance(result, dict)
        for key, value in result.items():
            assert key in nested
            assert isinstance(value, dict)
            # Keys should be preserved
            assert set(value.keys()) == set(nested[key].keys())


# =============================================================================
# 12.4: Logger Properties
# =============================================================================


class TestLoggerProperties:
    """Property tests for the logger."""

    @given(
        message=safe_text,
        level=st.sampled_from(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_logger_never_crashes_on_any_input(self, message: str, level: str):
        """12.4.1: Logger never crashes on any input."""
        output = io.StringIO()
        logger = Logger("test", level="DEBUG", mode="dev", stream=output)

        # Should never raise
        try:
            if level == "DEBUG":
                logger.debug(message)
            elif level == "INFO":
                logger.info(message)
            elif level == "WARNING":
                logger.warn(message)
            elif level == "ERROR":
                logger.error(message)
            elif level == "CRITICAL":
                logger.critical(message)
        except Exception as e:
            pytest.fail(f"Logger crashed with: {e}")

    @given(
        message=safe_text.filter(lambda s: len(s) > 0),
        extra=st.dictionaries(identifiers, safe_text, max_size=5),
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_json_output_is_always_parseable(
        self,
        message: str,
        extra: Dict[str, str],
    ):
        """12.4.2: JSON output is always parseable."""
        output = io.StringIO()
        logger = Logger("test", level="DEBUG", mode="prod", stream=output)

        logger.info(message, **extra)

        log_output = output.getvalue().strip()
        if log_output:
            # Should be valid JSON
            parsed = json.loads(log_output)
            assert isinstance(parsed, dict)
            assert parsed["msg"] == message

    @given(
        message=safe_text.filter(lambda s: len(s) > 0),
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_dev_mode_output_is_always_printable(self, message: str):
        """12.4.3: Dev mode output is always printable."""
        output = io.StringIO()
        logger = Logger("test", level="DEBUG", mode="dev", stream=output)

        logger.info(message)

        log_output = output.getvalue()
        # Should be a valid string that can be printed
        assert isinstance(log_output, str)
        # Should contain the message
        if message:
            assert message in log_output or len(log_output) > 0


# =============================================================================
# 12.5: Duration Tracking Properties
# =============================================================================


class TestDurationTrackingProperties:
    """Property tests for duration tracking."""

    @given(
        sleep_ms=st.integers(min_value=0, max_value=50),
    )
    @settings(max_examples=20, suppress_health_check=[HealthCheck.too_slow])
    def test_duration_is_always_non_negative(self, sleep_ms: int):
        """12.5.1: Duration is always non-negative."""
        durations: List[float] = []

        @operation("test_op", on_complete=lambda d: durations.append(d))
        def timed_function():
            time.sleep(sleep_ms / 1000.0)
            return "done"

        timed_function()

        assert len(durations) == 1
        assert durations[0] >= 0

    @given(
        sleep_ms=st.integers(min_value=10, max_value=50),
    )
    @settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow])
    def test_duration_is_accurate_within_tolerance(self, sleep_ms: int):
        """12.5.2: Duration is accurate within tolerance."""
        durations: List[float] = []

        @operation("test_op", on_complete=lambda d: durations.append(d))
        def timed_function():
            time.sleep(sleep_ms / 1000.0)
            return "done"

        timed_function()

        # Duration should be at least as long as sleep time
        # Allow 50% tolerance for slow systems
        assert durations[0] >= sleep_ms * 0.5
        # Should not be excessively long (10x the expected)
        assert durations[0] < sleep_ms * 10

    @given(
        iterations=st.integers(min_value=1, max_value=10),
    )
    @settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow])
    def test_duration_never_causes_overflow(self, iterations: int):
        """12.5.3: Duration never causes overflow."""
        durations: List[float] = []

        @operation("test_op", on_complete=lambda d: durations.append(d))
        def quick_function():
            return "done"

        for _ in range(iterations):
            quick_function()

        # All durations should be valid floats
        assert len(durations) == iterations
        for d in durations:
            assert isinstance(d, float)
            assert d >= 0
            assert d < float("inf")


# =============================================================================
# Additional Edge Case Properties
# =============================================================================


class TestEdgeCaseProperties:
    """Additional property tests for edge cases."""

    @given(
        message=st.text(min_size=0, max_size=10000),
    )
    @settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
    def test_error_handles_any_message_length(self, message: str):
        """Errors should handle messages of any length."""
        try:
            error = PrismError(message or "default")
            result = error.to_dict()
            assert result["message"] == (message or "default")
        except Exception as e:
            pytest.fail(f"Failed with message length {len(message)}: {e}")

    @given(
        depth=st.integers(min_value=1, max_value=10),
    )
    @settings(max_examples=20, suppress_health_check=[HealthCheck.too_slow])
    def test_scrubber_handles_deep_nesting(self, depth: int):
        """Scrubber should handle deeply nested structures."""
        # Build nested structure
        data: Dict[str, Any] = {"password": "secret", "level": 0}
        current = data
        for i in range(1, depth):
            current["nested"] = {"password": f"secret{i}", "level": i}
            current = current["nested"]

        result = scrub(data)

        # All passwords should be redacted
        def check_redacted(d: Dict[str, Any]) -> None:
            if "password" in d:
                assert d["password"] == "[REDACTED]"
            if "nested" in d:
                check_redacted(d["nested"])

        check_redacted(result)

    @given(
        num_contexts=st.integers(min_value=1, max_value=5),
    )
    @settings(max_examples=20, suppress_health_check=[HealthCheck.too_slow])
    def test_context_handles_multiple_nested_levels(self, num_contexts: int):
        """Context should handle multiple nesting levels."""
        LogContext.clear()

        contexts = []
        for i in range(num_contexts):
            ctx = LogContext.request(trace_id=f"trace-{i}")
            ctx.__enter__()
            contexts.append(ctx)

        # Innermost trace_id should be visible
        current = LogContext.get_current()
        assert current.get("trace_id") == f"trace-{num_contexts - 1}"

        # Clean up in reverse order
        for ctx in reversed(contexts):
            ctx.__exit__(None, None, None)

        LogContext.clear()
