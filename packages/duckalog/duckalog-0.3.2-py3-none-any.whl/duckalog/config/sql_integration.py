"""SQL file integration and path resolution utilities.

This module provides glue code for SQL file loading and path resolution
as part of the configuration processing pipeline.
"""

from pathlib import Path
from typing import Any

from duckalog.errors import ConfigError


def _load_sql_files_from_config(
    config: Any,
    config_path: Path,
    sql_file_loader: Any = None,
) -> Any:
    """Load SQL content from external files referenced in the config.

    This functionality has been simplified as part of the config layer consolidation.
    SQL file references are no longer supported - SQL content should be inlined.

    Args:
        config: The configuration object to process
        config_path: Path to the configuration file (for relative path resolution)
        sql_file_loader: Ignored parameter (functionality simplified)

    Returns:
        Updated configuration unchanged

    Raises:
        ConfigError: If the config contains SQL file references
    """
    # Check if any views have SQL file references
    has_sql_files = any(
        getattr(view, "sql_file", None) is not None
        or getattr(view, "sql_template", None) is not None
        for view in config.views
    )

    if has_sql_files:
        raise ConfigError(
            "SQL file references (sql_file, sql_template) are no longer supported "
            "as part of config layer consolidation. Please inline SQL content directly "
            "in your configuration files using the 'sql' field."
        )

    # No SQL files found, return config unchanged
    return config
