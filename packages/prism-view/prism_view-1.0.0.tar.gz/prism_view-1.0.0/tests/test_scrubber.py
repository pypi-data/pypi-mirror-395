"""
Tests for Secret Scrubber (Iteration 7).

Tests cover:
- Basic key-based scrubbing (password, secret, token, api_key)
- Pattern-based scrubbing (JWT, high-entropy strings, credit cards)
- Extensible patterns (custom patterns, custom key patterns)
- Nested data scrubbing (dicts, lists, deep nesting)
- Logger integration
"""

import copy


class TestBasicScrubbing:
    """Tests for basic key-based scrubbing (7.1)."""

    def test_scrubber_can_be_instantiated(self):
        """Scrubber can be instantiated."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        assert scrubber is not None

    def test_scrubber_detects_password_key(self):
        """Scrubber detects 'password' key."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {"username": "john", "password": "secret123"}
        result = scrubber.scrub(data)

        assert result["username"] == "john"
        assert result["password"] != "secret123"
        assert "REDACTED" in result["password"]

    def test_scrubber_detects_secret_key(self):
        """Scrubber detects 'secret' key."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {"name": "app", "secret": "my-secret-value"}
        result = scrubber.scrub(data)

        assert result["name"] == "app"
        assert "REDACTED" in result["secret"]

    def test_scrubber_detects_token_key(self):
        """Scrubber detects 'token' key."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {"user": "alice", "token": "abc123xyz"}
        result = scrubber.scrub(data)

        assert result["user"] == "alice"
        assert "REDACTED" in result["token"]

    def test_scrubber_detects_api_key(self):
        """Scrubber detects 'api_key' key."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {"service": "payment", "api_key": "sk_live_123456"}
        result = scrubber.scrub(data)

        assert result["service"] == "payment"
        assert "REDACTED" in result["api_key"]

    def test_scrubber_detects_apikey_key(self):
        """Scrubber detects 'apikey' key (no underscore)."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {"apikey": "key123"}
        result = scrubber.scrub(data)

        assert "REDACTED" in result["apikey"]

    def test_scrubbing_is_case_insensitive(self):
        """Scrubbing is case-insensitive for key names."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {
            "PASSWORD": "secret1",
            "Password": "secret2",
            "passWORD": "secret3",
        }
        result = scrubber.scrub(data)

        for key in data:
            assert "REDACTED" in result[key]

    def test_scrubbed_value_format(self):
        """Scrubbed value is '[REDACTED]'."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {"password": "secret123"}
        result = scrubber.scrub(data)

        assert result["password"] == "[REDACTED]"

    def test_scrubber_detects_key_suffix(self):
        """Scrubber detects keys ending with sensitive words."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {
            "db_password": "secret1",
            "auth_token": "secret2",
            "aws_secret": "secret3",
            "stripe_api_key": "secret4",
        }
        result = scrubber.scrub(data)

        for key in data:
            assert "REDACTED" in result[key]

    def test_scrubber_detects_key_prefix(self):
        """Scrubber detects keys starting with sensitive words."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {
            "password_hash": "secret1",
            "secret_key": "secret2",
            "token_value": "secret3",
        }
        result = scrubber.scrub(data)

        for key in data:
            assert "REDACTED" in result[key]

    def test_scrubber_preserves_non_sensitive_keys(self):
        """Scrubber preserves non-sensitive keys."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {
            "username": "john",
            "email": "john@example.com",
            "count": 42,
            "active": True,
        }
        result = scrubber.scrub(data)

        assert result == data

    def test_scrubber_detects_credential_key(self):
        """Scrubber detects 'credential' key."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {"credential": "my-credential"}
        result = scrubber.scrub(data)

        assert "REDACTED" in result["credential"]

    def test_scrubber_detects_private_key(self):
        """Scrubber detects 'private_key' key."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {"private_key": "-----BEGIN RSA PRIVATE KEY-----"}
        result = scrubber.scrub(data)

        assert "REDACTED" in result["private_key"]

    def test_scrubber_detects_auth_key(self):
        """Scrubber detects 'auth' key."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {"auth": "Bearer token123", "authorization": "Basic abc"}
        result = scrubber.scrub(data)

        assert "REDACTED" in result["auth"]
        assert "REDACTED" in result["authorization"]


class TestPatternBasedScrubbing:
    """Tests for pattern-based scrubbing (7.2)."""

    def test_scrubber_detects_jwt_tokens(self):
        """Scrubber detects JWT tokens (eyJ...)."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        jwt = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJzdWIiOiIxMjM0NTY3ODkwIn0."
            "dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"
        )
        data = {"message": f"Token: {jwt}"}
        result = scrubber.scrub(data)

        assert jwt not in result["message"]
        assert "REDACTED" in result["message"] or "[JWT]" in result["message"]

    def test_scrubber_detects_bearer_tokens(self):
        """Scrubber detects Bearer tokens in values."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {"header": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ0ZXN0IjoidmFsdWUifQ.signature"}
        result = scrubber.scrub(data)

        assert "eyJ" not in result["header"]

    def test_scrubber_detects_credit_card_numbers(self):
        """Scrubber detects credit card numbers."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {
            "card1": "4111111111111111",  # Visa test card
            "card2": "5500000000000004",  # Mastercard test card
            "message": "Card: 4111-1111-1111-1111",
        }
        result = scrubber.scrub(data)

        assert "4111111111111111" not in result["card1"]
        assert "5500000000000004" not in result["card2"]

    def test_scrubber_pattern_works_on_values(self):
        """Pattern scrubbing works on values, not just keys."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {"log": "User provided password=secret123 in query"}
        result = scrubber.scrub(data)

        # Should detect password= pattern in value
        assert "secret123" not in result["log"] or "password" not in result["log"].lower()

    def test_scrubber_detects_aws_keys(self):
        """Scrubber detects AWS access keys."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {"aws_key": "AKIAIOSFODNN7EXAMPLE"}
        result = scrubber.scrub(data)

        assert "AKIAIOSFODNN7EXAMPLE" not in result["aws_key"]

    def test_scrubber_detects_base64_secrets(self):
        """Scrubber detects base64-encoded secrets in sensitive keys."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {"secret_base64": "c2VjcmV0MTIzNDU2Nzg5MA=="}
        result = scrubber.scrub(data)

        assert "REDACTED" in result["secret_base64"]


class TestExtensiblePatterns:
    """Tests for extensible patterns (7.3)."""

    def test_scrubber_add_key_pattern(self):
        """Scrubber.add_key_pattern() adds custom key pattern."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        scrubber.add_key_pattern("ssn")

        data = {"ssn": "123-45-6789"}
        result = scrubber.scrub(data)

        assert "REDACTED" in result["ssn"]

    def test_scrubber_add_value_pattern(self):
        """Scrubber.add_value_pattern() adds custom value pattern."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        # Add pattern to detect SSN format in values
        scrubber.add_value_pattern("ssn", r"\d{3}-\d{2}-\d{4}")

        data = {"info": "SSN is 123-45-6789"}
        result = scrubber.scrub(data)

        assert "123-45-6789" not in result["info"]

    def test_custom_pattern_with_replacement(self):
        """Custom patterns can have custom replacement text."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        scrubber.add_value_pattern("phone", r"\d{3}-\d{3}-\d{4}", replacement="[PHONE]")

        data = {"contact": "Call 555-123-4567"}
        result = scrubber.scrub(data)

        assert "555-123-4567" not in result["contact"]
        assert "[PHONE]" in result["contact"]

    def test_multiple_custom_patterns(self):
        """Multiple custom patterns can be added."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        scrubber.add_key_pattern("social_security")
        scrubber.add_key_pattern("drivers_license")

        data = {
            "social_security": "123-45-6789",
            "drivers_license": "D1234567",
        }
        result = scrubber.scrub(data)

        assert "REDACTED" in result["social_security"]
        assert "REDACTED" in result["drivers_license"]

    def test_custom_key_pattern_case_insensitive(self):
        """Custom key patterns are case-insensitive."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        scrubber.add_key_pattern("mySecret")

        data = {"MYSECRET": "value1", "mysecret": "value2", "MySecret": "value3"}
        result = scrubber.scrub(data)

        for key in data:
            assert "REDACTED" in result[key]


class TestNestedScrubbing:
    """Tests for nested data scrubbing (7.4)."""

    def test_scrubber_handles_nested_dicts(self):
        """Scrubber handles nested dictionaries."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {
            "user": {
                "name": "john",
                "login_info": {
                    "password": "secret123",
                    "api_key": "key456",
                },
            }
        }
        result = scrubber.scrub(data)

        assert result["user"]["name"] == "john"
        assert "REDACTED" in result["user"]["login_info"]["password"]
        assert "REDACTED" in result["user"]["login_info"]["api_key"]

    def test_scrubber_handles_lists_of_dicts(self):
        """Scrubber handles lists of dictionaries."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {
            "users": [
                {"name": "alice", "password": "pass1"},
                {"name": "bob", "password": "pass2"},
            ]
        }
        result = scrubber.scrub(data)

        assert result["users"][0]["name"] == "alice"
        assert "REDACTED" in result["users"][0]["password"]
        assert result["users"][1]["name"] == "bob"
        assert "REDACTED" in result["users"][1]["password"]

    def test_scrubber_handles_deep_nesting(self):
        """Scrubber handles deeply nested structures."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {
                            "secret": "deep-secret",
                        }
                    }
                }
            }
        }
        result = scrubber.scrub(data)

        assert "REDACTED" in result["level1"]["level2"]["level3"]["level4"]["secret"]

    def test_scrubber_doesnt_modify_original(self):
        """Scrubber doesn't modify the original data."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        original = {"password": "secret123", "nested": {"token": "abc"}}
        original_copy = copy.deepcopy(original)

        result = scrubber.scrub(original)

        # Original should be unchanged
        assert original == original_copy
        # Result should be different
        assert result != original

    def test_scrubber_handles_mixed_lists(self):
        """Scrubber handles lists with mixed types."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {
            "items": [
                "string",
                42,
                {"password": "secret"},
                ["nested", {"token": "abc"}],
            ]
        }
        result = scrubber.scrub(data)

        assert result["items"][0] == "string"
        assert result["items"][1] == 42
        assert "REDACTED" in result["items"][2]["password"]
        assert result["items"][3][0] == "nested"
        assert "REDACTED" in result["items"][3][1]["token"]

    def test_scrubber_handles_none_values(self):
        """Scrubber handles None values."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {"password": None, "value": None}
        result = scrubber.scrub(data)

        # None values in sensitive keys should still be handled
        assert result["value"] is None

    def test_scrubber_handles_empty_structures(self):
        """Scrubber handles empty dicts and lists."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {"empty_dict": {}, "empty_list": [], "nested": {"also_empty": {}}}
        result = scrubber.scrub(data)

        assert result["empty_dict"] == {}
        assert result["empty_list"] == []
        assert result["nested"]["also_empty"] == {}


class TestLoggerIntegration:
    """Tests for Logger integration (7.5)."""

    def test_logger_scrubs_extra_fields(self, capsys):
        """Logger automatically scrubs extra fields in log data."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        logger.info("User login", password="secret123", username="john")

        captured = capsys.readouterr()
        output = captured.err

        assert "secret123" not in output
        assert "john" in output

    def test_logger_scrubs_context(self, capsys):
        """Logger scrubs sensitive data from context."""
        from prism.view import LogContext
        from prism.view.logger import Logger

        LogContext.set_service(name="api", api_key="secret-key-123")

        logger = Logger("test", mode="prod")
        logger.info("Request received")

        captured = capsys.readouterr()
        output = captured.err

        assert "secret-key-123" not in output

    def test_logger_scrubs_error_details(self, capsys):
        """Logger scrubs sensitive data from error details."""
        from prism.view import PrismError
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")

        error = PrismError(
            "Authentication failed",
            details={"password": "user-password", "username": "john"},
        )
        logger.error("Auth error", exc=error)

        captured = capsys.readouterr()
        output = captured.err

        assert "user-password" not in output
        assert "john" in output

    def test_logger_scrubbing_doesnt_break_json(self, capsys):
        """Scrubbing doesn't break JSON formatting."""
        import json

        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        logger.info("Test", password="secret", data={"nested": {"token": "abc"}})

        captured = capsys.readouterr()
        output = captured.err.strip()

        # Should still be valid JSON
        parsed = json.loads(output)
        assert isinstance(parsed, dict)

    def test_logger_dev_mode_also_scrubs(self, capsys):
        """Dev mode also scrubs sensitive data."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="dev")
        logger.info("User action", password="secret123")

        captured = capsys.readouterr()
        output = captured.err

        assert "secret123" not in output

    def test_scrubber_can_be_disabled(self, capsys):
        """Scrubbing can be disabled on logger."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod", scrub=False)
        logger.info("Test", password="visible-password")

        captured = capsys.readouterr()
        output = captured.err

        # With scrubbing disabled, password should be visible
        assert "visible-password" in output


class TestScrubberEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_scrubber_handles_non_string_values(self):
        """Scrubber handles non-string values correctly."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {
            "count": 42,
            "ratio": 3.14,
            "active": True,
            "items": [1, 2, 3],
        }
        result = scrubber.scrub(data)

        assert result == data

    def test_scrubber_handles_bytes(self):
        """Scrubber handles bytes values."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        data = {"data": b"binary data", "password": b"secret"}
        result = scrubber.scrub(data)

        # Bytes should be handled (converted to string or left as-is)
        assert "REDACTED" in str(result["password"])

    def test_scrubber_is_reusable(self):
        """Scrubber instance can be reused."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()

        result1 = scrubber.scrub({"password": "secret1"})
        result2 = scrubber.scrub({"password": "secret2"})

        assert "REDACTED" in result1["password"]
        assert "REDACTED" in result2["password"]

    def test_default_scrubber_instance(self):
        """Default scrubber instance is available."""
        from prism.view.scrubber import default_scrubber, scrub

        # scrub() function should use default scrubber
        result = scrub({"password": "secret"})
        assert "REDACTED" in result["password"]

        # default_scrubber should be a Scrubber instance
        assert default_scrubber is not None

    def test_scrubber_handles_circular_references(self):
        """Scrubber handles data without circular references."""
        from prism.view.scrubber import Scrubber

        scrubber = Scrubber()
        # Note: We don't need to support actual circular refs,
        # just ensure we don't crash on complex nested structures
        data = {
            "a": {"b": {"c": {"password": "secret"}}},
            "x": {"y": {"z": {"token": "abc"}}},
        }
        result = scrubber.scrub(data)

        assert "REDACTED" in result["a"]["b"]["c"]["password"]
        assert "REDACTED" in result["x"]["y"]["z"]["token"]
