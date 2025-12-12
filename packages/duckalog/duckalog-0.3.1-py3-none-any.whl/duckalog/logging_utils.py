"""Compatibility wrapper for logging utilities.

This module provides backward compatibility for imports while
the actual logging functions are now in config.py.
"""

from .config import get_logger, log_info, log_debug, log_error

__all__ = ["get_logger", "log_info", "log_debug", "log_error"]
