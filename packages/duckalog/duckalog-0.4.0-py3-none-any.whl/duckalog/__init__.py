"""Duckalog public API."""

from .config import (
    AttachmentsConfig,
    Config,
    DuckDBAttachment,
    DuckDBConfig,
    IcebergCatalogConfig,
    PostgresAttachment,
    SQLiteAttachment,
    ViewConfig,
    SecretConfig,
    load_config,
)
from .remote_config import load_config_from_uri
from .engine import build_catalog
from .errors import (
    DuckalogError,
    ConfigError,
    EngineError,
    PathResolutionError,
    RemoteConfigError,
    SQLFileError,
    SQLFileNotFoundError,
    SQLFilePermissionError,
    SQLFileEncodingError,
    SQLFileSizeError,
    SQLTemplateError,
)
from .sql_file_loader import SQLFileLoader
from .sql_generation import (
    generate_all_views_sql,
    generate_view_sql,
    generate_secret_sql,
    quote_ident,
    quote_literal,
    render_options,
)
from .python_api import (
    generate_sql,
    validate_config,
    connect_to_catalog,
    connect_to_catalog_cm,
    connect_and_build_catalog,
)
from .config_init import create_config_template, validate_generated_config, ConfigFormat

__all__ = [
    "Config",
    "ConfigError",
    "DuckDBConfig",
    "AttachmentsConfig",
    "DuckDBAttachment",
    "SQLiteAttachment",
    "PostgresAttachment",
    "IcebergCatalogConfig",
    "ViewConfig",
    "SecretConfig",
    "load_config",
    "build_catalog",
    "EngineError",
    "generate_sql",
    "validate_config",
    "connect_to_catalog",
    "connect_to_catalog_cm",
    "connect_and_build_catalog",
    "quote_ident",
    "quote_literal",
    "render_options",
    "generate_view_sql",
    "generate_all_views_sql",
    "generate_secret_sql",
    "create_config_template",
    "validate_generated_config",
    "ConfigFormat",
    "SQLFileLoader",
    "SQLFileError",
    "SQLFileNotFoundError",
    "SQLFilePermissionError",
    "SQLFileEncodingError",
    "SQLFileSizeError",
    "SQLTemplateError",
]
