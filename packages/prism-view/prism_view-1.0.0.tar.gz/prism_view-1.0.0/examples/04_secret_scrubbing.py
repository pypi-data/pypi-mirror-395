"""
Secret scrubbing example for prism-view.

This example demonstrates:
- Automatic sensitive data redaction
- Key-based scrubbing (password, token, secret, etc.)
- Pattern-based scrubbing (JWT, credit cards, AWS keys)
- Adding custom scrubbing patterns
- Nested data structure scrubbing

Usage:
    python examples/04_secret_scrubbing.py
"""

from prism.view import scrub, Scrubber


# =============================================================================
# Basic Scrubbing
# =============================================================================

print("=== Basic Key-Based Scrubbing ===\n")

# Data with sensitive fields
user_data = {
    "username": "alice",
    "email": "alice@example.com",
    "password": "super-secret-password",
    "api_key": "sk_live_abc123xyz",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U",
}

# Scrub the data
scrubbed = scrub(user_data)

print("Original data:")
for key, value in user_data.items():
    print(f"  {key}: {value[:30]}..." if len(str(value)) > 30 else f"  {key}: {value}")

print("\nScrubbed data:")
for key, value in scrubbed.items():
    print(f"  {key}: {value}")


# =============================================================================
# Pattern-Based Scrubbing
# =============================================================================

print("\n=== Pattern-Based Scrubbing ===\n")

log_data = {
    "message": "User authentication",
    "authorization_header": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiam9obiJ9.abc123",
    "url": "https://api.example.com?password=secret123&user=john",
    "aws_key": "AKIAIOSFODNN7EXAMPLE",
    "card_number": "4111-1111-1111-1111",
}

scrubbed = scrub(log_data)

print("Scrubbed log data:")
for key, value in scrubbed.items():
    print(f"  {key}: {value}")


# =============================================================================
# Nested Data Structures
# =============================================================================

print("\n=== Nested Data Structures ===\n")

nested_data = {
    "user": {
        "name": "John Doe",
        "auth": {
            "password": "my-password",
            "refresh_token": "refresh-token-value",
        },
    },
    "payments": [
        {"card_number": "4111111111111111", "amount": 99.99},
        {"card_number": "5555555555554444", "amount": 149.99},
    ],
    "config": {
        "database": {
            "host": "localhost",
            "password": "db-password",
        }
    },
}

scrubbed = scrub(nested_data)

import json
print("Scrubbed nested data:")
print(json.dumps(scrubbed, indent=2))


# =============================================================================
# Custom Scrubbing Patterns
# =============================================================================

print("\n=== Custom Scrubbing Patterns ===\n")

# Create a custom scrubber
custom_scrubber = Scrubber()

# Add custom key patterns
custom_scrubber.add_key_pattern("ssn")
custom_scrubber.add_key_pattern("social_security")
custom_scrubber.add_key_pattern("drivers_license")

# Add custom value pattern (US phone numbers)
custom_scrubber.add_value_pattern(
    name="phone",
    pattern=r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b",
    replacement="[PHONE]",
)

# Add custom value pattern (email addresses in text)
custom_scrubber.add_value_pattern(
    name="email",
    pattern=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    replacement="[EMAIL]",
)

personal_data = {
    "name": "John Doe",
    "ssn": "123-45-6789",
    "phone": "555-123-4567",
    "contact_info": "Call me at 555.987.6543 or email john.doe@example.com",
    "drivers_license": "D1234567",
}

scrubbed = custom_scrubber.scrub(personal_data)

print("Custom scrubbed data:")
for key, value in scrubbed.items():
    print(f"  {key}: {value}")


# =============================================================================
# Logger Integration
# =============================================================================

print("\n=== Logger Integration ===\n")

from prism.view import get_logger, setup_logging

setup_logging(mode="dev", show_banner=False)

# Logger automatically scrubs by default
logger = get_logger("secure-app")

# This will automatically redact the password
logger.info(
    "User login attempt",
    username="alice",
    password="should-be-redacted",
    ip_address="192.168.1.1",
)

# Disable scrubbing if needed (not recommended for production!)
from prism.view.logger import Logger

unscrubbed_logger = Logger("test", scrub=False)
unscrubbed_logger.info(
    "This won't be scrubbed",
    password="visible-password",
)
