"""Basic tests for logging utilities."""

from __future__ import annotations

import logging

from duckalog.logging_utils import get_logger, log_debug, log_info


def test_get_logger_and_log_redaction(caplog):
    caplog.set_level(logging.DEBUG, logger="duckalog")

    logger = get_logger()
    assert logger is not None

    log_info("Testing info log", password="supersecret")
    log_debug("Testing debug log", token="secret-token")

    text = caplog.text
    assert "Testing info log" in text
    assert "Testing debug log" in text
    assert "***REDACTED***" in text
    assert "supersecret" not in text
