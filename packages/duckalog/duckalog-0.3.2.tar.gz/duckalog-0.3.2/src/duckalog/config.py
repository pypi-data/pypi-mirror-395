"""Configuration schema and loader for Duckalog catalogs.

This module provides a unified configuration layer that consolidates:

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

# Re-export everything from the config package to maintain backward compatibility
from duckalog.config import (
    # Configuration models
    Config,
    ConfigError,
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
    # Configuration loading
    load_config,
    # Path resolution functions
    is_relative_path,
    resolve_relative_path,
    validate_path_security,
    normalize_path_for_sql,
    is_within_allowed_roots,
    is_windows_path_absolute,
    detect_path_type,
    validate_file_accessibility,
    # Logging utilities
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
