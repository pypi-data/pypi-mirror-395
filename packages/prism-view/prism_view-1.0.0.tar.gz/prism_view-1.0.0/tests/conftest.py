"""
Shared pytest fixtures for prism-view tests.
"""

import os

import pytest


@pytest.fixture
def prism_env(monkeypatch, tmp_path):
    """
    Standard test environment for all Prism tests.

    Provides:
    - Isolated temporary directory
    - Clean environment variables
    - Automatic cleanup
    """
    # Store original env
    original_env = os.environ.copy()

    # Clear all env vars that might affect tests
    for key in list(os.environ.keys()):
        if key.startswith(("PRISM_", "APP_", "LOG_")):
            monkeypatch.delenv(key, raising=False)

    yield {
        "tmp_path": tmp_path,
        "monkeypatch": monkeypatch,
    }

    # Restore original env
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def sample_config_dict():
    """Basic configuration as a Python dict for testing."""
    return {
        "app": {
            "name": "test-app",
            "environment": "dev",
        },
        "logging": {
            "level": "DEBUG",
            "format": "dev",
        },
    }


@pytest.fixture
def mock_context():
    """
    Mock LogContext for testing.

    Returns a dict that simulates LogContext.get_current() output.
    """
    return {
        "service": {
            "name": "test-service",
            "version": "1.0.0",
            "environment": "test",
        },
        "request": {
            "trace_id": "test-trace-123",
            "method": "GET",
            "path": "/api/test",
        },
        "user": {
            "user_id": "user-456",
            "username": "testuser",
        },
        "operation": {
            "name": "test_operation",
            "started_at": "2025-01-01T00:00:00Z",
        },
    }


@pytest.fixture
def sample_error_data():
    """
    Sample error data for testing PrismError.

    Returns kwargs suitable for PrismError instantiation.
    """
    return {
        "message": "Test error message",
        "details": {
            "field": "test_field",
            "value": "invalid_value",
        },
        "suggestions": [
            "Check the input value",
            "Refer to documentation",
        ],
    }


@pytest.fixture(autouse=True)
def clear_logger_cache():
    """Clear the logger cache before each test."""
    from prism.view.logger import clear_logger_cache

    clear_logger_cache()
    yield
    clear_logger_cache()


@pytest.fixture(autouse=True)
def clear_log_context():
    """Clear the LogContext before each test."""
    from prism.view.context import LogContext

    LogContext.clear()
    yield
    LogContext.clear()
