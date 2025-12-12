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

    This function delegates to the loader module's implementation
    for SQL file loading.

    Args:
        config: The configuration object to process
        config_path: Path to the configuration file (for relative path resolution)
        sql_file_loader: Optional SQLFileLoader instance for loading SQL files

    Returns:
        Updated configuration with SQL content inlined

    Raises:
        ConfigError: If the config contains SQL file references
    """
    # Delegate to the loader module's implementation
    from .loader import _load_sql_files_from_config as load_sql_files

    return load_sql_files(config, config_path, sql_file_loader)
