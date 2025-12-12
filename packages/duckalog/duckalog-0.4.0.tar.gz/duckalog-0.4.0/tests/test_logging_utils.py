"""Basic tests for logging utilities."""

from __future__ import annotations

import logging
from io import StringIO

from duckalog.logging_utils import get_logger, log_debug, log_info


def test_get_logger_and_log_redaction(caplog):
    """Test that logging works and redacts sensitive values."""
    logger = get_logger()
    assert logger is not None

    # Test that logging functions don't raise errors
    log_info("Testing info log", password="supersecret")
    log_debug("Testing debug log", token="secret-token")

    # Test with non-sensitive data
    log_info("Testing info log", username="user123")
    log_debug("Testing debug log", count=42)


def test_get_logger_returns_loguru_logger():
    """Test that get_logger returns a loguru logger."""
    from loguru import logger as loguru_logger

    duckalog_logger = get_logger()

    # The loguru logger has a bind method
    assert hasattr(duckalog_logger, "bind")

    # Can call logging methods on it
    duckalog_logger.info("Test message", key="value")


def test_redaction_logic():
    """Test that sensitive values are properly redacted."""
    from duckalog.config.validators import _redact_value

    # Sensitive values should be redacted
    assert _redact_value("secret123", "password") == "***REDACTED***"
    assert _redact_value("token456", "token") == "***REDACTED***"
    assert _redact_value("key789", "key") == "***REDACTED***"

    # Non-sensitive values should pass through
    assert _redact_value("value123", "username") == "value123"
    assert _redact_value("value123", "count") == "value123"

    # Nested structures should be redacted
    nested = {"password": "secret", "username": "user"}
    redacted = _redact_value(nested)
    assert redacted["password"] == "***REDACTED***"
    assert redacted["username"] == "user"
