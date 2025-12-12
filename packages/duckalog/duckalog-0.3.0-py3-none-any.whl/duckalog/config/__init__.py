"""Configuration package for Duckalog catalogs.

This package provides a unified configuration layer that consolidates:
- Configuration schema definitions and validation (Pydantic models)
- Path resolution utilities with security validation
- SQL file loading and template processing
- Logging with automatic sensitive data redaction

The consolidation reduces complexity by eliminating separate modules for path resolution,
SQL file loading, and logging utilities, while maintaining the same public API.

## Key Functions

### Configuration Loading
- `load_config()`: Main entry point for loading configuration files
- `load_config_with_context()`: Load config with additional context information
- `load_config_with_schema()`: Load config using a custom schema class

### Path Resolution
- `is_relative_path()`: Detect if a path is relative
- `resolve_relative_path()`: Resolve relative paths to absolute paths
- `validate_path_security()`: Validate path security boundaries
- `normalize_path_for_sql()`: Normalize paths for SQL usage

### SQL File Processing
- Internal functions for loading SQL content from external files
- Template processing with variable substitution
- Security validation of SQL content

### Logging Utilities
- `log_info()`, `log_debug()`, `log_error()`: Redacted logging functions
- Automatic detection and redaction of sensitive data
"""

# Import all models and functions from the individual modules
# This maintains backward compatibility for existing imports

# Import models first (these are the foundation and don't have circular dependencies)
from .models import (
    Config,
    DuckDBConfig,
    SecretConfig,
    AttachmentsConfig,
    DuckDBAttachment,
    SQLiteAttachment,
    PostgresAttachment,
    DuckalogAttachment,
    IcebergCatalogConfig,
    ViewConfig,
    SemanticModelConfig,
    SemanticDimensionConfig,
    SemanticMeasureConfig,
    SemanticJoinConfig,
    SemanticDefaultsConfig,
    SQLFileReference,
)

# Import errors
from duckalog.errors import ConfigError

# Import path resolution and validation functions (these can import from models)
from .validators import (
    is_relative_path,
    resolve_relative_path,
    validate_path_security,
    normalize_path_for_sql,
    is_within_allowed_roots,
    is_windows_path_absolute,
    detect_path_type,
    validate_file_accessibility,
    log_info,
    log_debug,
    log_error,
    get_logger,
)

# Import interpolation functions
from .interpolation import _interpolate_env

# Import SQL integration functions
from .sql_integration import _load_sql_files_from_config

# Implement load_config directly here to avoid circular imports
import json
import os
import re
from pathlib import Path
from typing import Any, Optional

import yaml


def load_config(
    path: str,
    load_sql_files: bool = True,
    sql_file_loader: Optional[Any] = None,
    resolve_paths: bool = True,
    filesystem: Optional[Any] = None,
):
    """Load, interpolate, and validate a Duckalog configuration file.

    This helper is the main entry point for turning a YAML or JSON file into a
    validated :class:`Config` instance. It applies environment-variable
    interpolation and enforces the configuration schema.
    """
    # Check if this is a remote URI
    try:
        from duckalog.remote_config import is_remote_uri, load_config_from_uri

        if is_remote_uri(path):
            # For remote URIs, use the remote loader
            return load_config_from_uri(
                uri=path,
                load_sql_files=load_sql_files,
                sql_file_loader=sql_file_loader,
                resolve_paths=False,  # Remote configs don't resolve relative paths by default
                filesystem=filesystem,
            )
    except ImportError:
        # Remote functionality not available, continue with local loading
        pass

    # Local file loading
    config_path = Path(path)
    if not config_path.exists():
        raise ConfigError(f"Config file not found: {path}")

    log_info("Loading config", path=str(config_path))
    try:
        if filesystem is not None:
            if not hasattr(filesystem, "open") or not hasattr(filesystem, "exists"):
                raise ConfigError(
                    "filesystem object must provide 'open' and 'exists' methods "
                    "for fsspec-compatible interface"
                )
            if not filesystem.exists(str(config_path)):
                raise ConfigError(f"Config file not found: {path}")
            with filesystem.open(str(config_path), "r") as f:
                raw_text = f.read()
        else:
            raw_text = config_path.read_text()
    except OSError as exc:
        raise ConfigError(f"Failed to read config file: {exc}") from exc

    suffix = config_path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        parsed = yaml.safe_load(raw_text)
    elif suffix == ".json":
        parsed = json.loads(raw_text)
    else:
        raise ConfigError("Config files must use .yaml, .yml, or .json extensions")

    if parsed is None:
        raise ConfigError("Config file is empty")
    if not isinstance(parsed, dict):
        raise ConfigError("Config file must define a mapping at the top level")

    log_debug("Raw config keys", keys=list(parsed.keys()))
    interpolated = _interpolate_env(parsed)

    try:
        config = Config.model_validate(interpolated)
    except Exception as exc:
        raise ConfigError(f"Configuration validation failed: {exc}") from exc

    # Resolve relative paths if requested (simplified implementation)
    if resolve_paths:
        log_debug("Path resolution requested")

    # Load SQL from external files if requested
    if load_sql_files:
        config = _load_sql_files_from_config(config, config_path, sql_file_loader)

    log_info("Config loaded", path=str(config_path), views=len(config.views))
    return config


# Import errors
from duckalog.errors import ConfigError

# Import loader functions
from .loader import load_config

# Import path resolution functions
from .validators import (
    is_relative_path,
    resolve_relative_path,
    validate_path_security,
    normalize_path_for_sql,
    is_within_allowed_roots,
    is_windows_path_absolute,
    detect_path_type,
    validate_file_accessibility,
)

# Import logging utilities
from .validators import (
    get_logger,
    log_info,
    log_debug,
    log_error,
)

# Import errors
from duckalog.errors import ConfigError


# Import loader functions
from .loader import load_config


# Import path resolution functions (temporary placeholder - will be updated when validators.py is created)
from duckalog.config import (
    is_relative_path,
    resolve_relative_path,
    validate_path_security,
    normalize_path_for_sql,
    is_within_allowed_roots,
    is_windows_path_absolute,
    detect_path_type,
    validate_file_accessibility,
)

# Import logging utilities (temporary placeholder - will be updated when validators.py is created)
from duckalog.config import (
    get_logger,
    log_info,
    log_debug,
    log_error,
)

# Define the public API - all symbols that should be available for import
__all__ = [
    # Configuration models
    "Config",
    "ConfigError",
    "DuckDBConfig",
    "SecretConfig",
    "AttachmentsConfig",
    "DuckDBAttachment",
    "SQLiteAttachment",
    "PostgresAttachment",
    "DuckalogAttachment",
    "IcebergCatalogConfig",
    "ViewConfig",
    "SemanticModelConfig",
    "SemanticDimensionConfig",
    "SemanticMeasureConfig",
    "SemanticJoinConfig",
    "SemanticDefaultsConfig",
    "SQLFileReference",
    # Configuration loading
    "load_config",
    # Path resolution functions
    "is_relative_path",
    "resolve_relative_path",
    "validate_path_security",
    "normalize_path_for_sql",
    "is_within_allowed_roots",
    "is_windows_path_absolute",
    "detect_path_type",
    "validate_file_accessibility",
    # Logging utilities
    "get_logger",
    "log_info",
    "log_debug",
    "log_error",
]
