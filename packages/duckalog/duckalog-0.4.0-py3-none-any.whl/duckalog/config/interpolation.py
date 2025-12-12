"""Environment variable interpolation utilities for configuration loading.

This module handles the resolution of ${env:VAR_NAME} placeholders in configuration
values, providing environment variable interpolation functionality.
"""

import os
import re

from duckalog.errors import ConfigError

# Regular expression pattern for environment variable interpolation
ENV_PATTERN = re.compile(r"\$\{env:([A-Za-z_][A-Za-z0-9_]*)\}")


def _interpolate_env(value):
    """Recursively interpolate ${env:VAR} placeholders in config data.

    Args:
        value: The value to interpolate. Can be a string, list, dict, or other type.

    Returns:
        The interpolated value with environment variables resolved.

    Raises:
        ConfigError: If an environment variable is not set.
    """
    if isinstance(value, str):
        return ENV_PATTERN.sub(_replace_env_match, value)
    if isinstance(value, list):
        return [_interpolate_env(item) for item in value]
    if isinstance(value, dict):
        return {key: _interpolate_env(val) for key, val in value.items()}
    return value


def _replace_env_match(match):
    """Replace environment variable match with its actual value.

    Args:
        match: Regular expression match object containing the variable name.

    Returns:
        The value of the environment variable.

    Raises:
        ConfigError: If the environment variable is not set.
    """
    var_name = match.group(1)
    try:
        return os.environ[var_name]
    except KeyError as exc:
        raise ConfigError(f"Environment variable '{var_name}' is not set") from exc
