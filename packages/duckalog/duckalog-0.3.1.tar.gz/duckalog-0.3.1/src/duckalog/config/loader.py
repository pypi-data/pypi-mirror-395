"""Configuration loading orchestration for Duckalog catalogs.

This module provides the main entry points for loading and processing configuration files,
handling both local file loading and remote URI loading.
"""

import json
import logging
from pathlib import Path
from typing import Any, Optional

import yaml

# Temporary import fixes to avoid circular imports
import json
import logging
from pathlib import Path
from typing import Any, Optional

import yaml

# Import directly from the main module for now to avoid circular imports
from duckalog.errors import ConfigError


def _interpolate_env(value: Any) -> Any:
    """Simple stub for environment variable interpolation."""
    if isinstance(value, str):
        # Simple ${env:VAR} replacement (basic implementation)
        import re
        import os

        pattern = re.compile(r"\$\{env:([A-Za-z_][A-Za-z0-9_]*)\}")

        def replace_env_match(match: Any) -> str:
            var_name = match.group(1)
            try:
                return os.environ[var_name]
            except KeyError as exc:
                raise ConfigError(
                    f"Environment variable '{var_name}' is not set"
                ) from exc

        return pattern.sub(replace_env_match, value)
    if isinstance(value, list):
        return [_interpolate_env(item) for item in value]
    if isinstance(value, dict):
        return {key: _interpolate_env(val) for key, val in value.items()}
    return value


def _load_sql_files_from_config(
    config: Any, config_path: Path, sql_file_loader: Optional[Any] = None
) -> Any:
    """Simple stub for SQL file loading."""
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

    return config


def log_info(message: str, **details: Any) -> None:
    """Simple logging stub."""
    print(f"INFO: {message} {details}")


def log_debug(message: str, **details: Any) -> None:
    """Simple logging stub."""
    print(f"DEBUG: {message} {details}")


from duckalog.errors import ConfigError


def load_config(
    path: str,
    load_sql_files: bool = True,
    sql_file_loader: Optional[Any] = None,
    resolve_paths: bool = True,
    filesystem: Optional[Any] = None,
) -> Any:
    """Load, interpolate, and validate a Duckalog configuration file.

    This helper is the main entry point for turning a YAML or JSON file into a
    validated :class:`Config` instance. It applies environment-variable
    interpolation and enforces the configuration schema.

    Args:
        path: Path to a YAML or JSON config file, or a remote URI.
        load_sql_files: Whether to load and process SQL from external files.
                      If False, SQL file references are left as-is for later processing.
        sql_file_loader: Optional SQLFileLoader instance for loading SQL files.
                        If None, a default loader will be created.
        resolve_paths: Whether to resolve relative paths to absolute paths.
                      If True, relative paths in view URIs and attachment paths
                      will be resolved relative to the config file's directory.
                      For remote configs, this defaults to False.
        filesystem: Optional fsspec filesystem object to use for remote operations.
                   If provided, this filesystem will be used instead of creating
                   a new one based on URI scheme. Useful for custom
                   authentication or advanced use cases.

    Returns:
        A validated :class:`Config` object.

    Raises:
        ConfigError: If the file cannot be read, is not valid YAML/JSON,
            fails schema validation, contains unresolved
            ``${env:VAR_NAME}`` placeholders, or if SQL file loading fails.

    Example:
        Load a catalog from ``catalog.yaml``::

            from duckalog import load_config

            config = load_config("catalog.yaml")
            print(len(config.views))

        Load a catalog from S3::

            config = load_config("s3://my-bucket/configs/catalog.yaml")
            print(len(config.views))

        Load a catalog with custom filesystem::

            import fsspec
            fs = fsspec.filesystem("s3", key="key", secret="secret", anon=False)
            config = load_config("s3://my-bucket/configs/catalog.yaml", filesystem=fs)
            print(len(config.views))
    """
    # Check if this is a remote URI
    try:
        from duckalog.remote_config import is_remote_uri, load_config_from_uri

        if is_remote_uri(path):
            # For remote URIs, use the remote loader
            # Default resolve_paths to False for remote configs
            return load_config_from_uri(
                uri=path,
                load_sql_files=load_sql_files,
                sql_file_loader=sql_file_loader,
                resolve_paths=False,  # Remote configs don't resolve relative paths by default
                filesystem=filesystem,  # Pass through filesystem parameter
            )
    except ImportError:
        # Remote functionality not available, continue with local loading
        pass

    # Local file loading - delegate to the dedicated helper
    return _load_config_from_local_file(
        path=path,
        load_sql_files=load_sql_files,
        sql_file_loader=sql_file_loader,
        resolve_paths=resolve_paths,
        filesystem=filesystem,
    )


def _load_config_from_local_file(
    path: str,
    load_sql_files: bool = True,
    sql_file_loader: Optional[Any] = None,
    resolve_paths: bool = True,
    filesystem: Optional[Any] = None,
) -> Any:
    """Load a configuration from a local file.

    This is an internal helper responsible for local file reading, environment
    interpolation, path resolution, and validation. It treats `filesystem` as
    an optional abstraction for local I/O when supplied (for example, fsspec-like
    objects in tests).

    Args:
        path: Path to a local YAML or JSON config file.
        load_sql_files: Whether to load and process SQL from external files.
        sql_file_loader: Optional SQLFileLoader instance for loading SQL files.
        resolve_paths: Whether to resolve relative paths to absolute paths.
        filesystem: Optional filesystem object for file I/O operations.
                   If None, uses default path-based file I/O.

    Returns:
        A validated :class:`Config` object.

    Raises:
        ConfigError: If the file cannot be read, is not valid YAML/JSON,
            fails schema validation, contains unresolved
            ``${env:VAR_NAME}`` placeholders, or if SQL file loading fails.
    """
    # Import Config here to avoid circular imports
    from .models import Config

    config_path = Path(path)
    if not config_path.exists():
        raise ConfigError(f"Config file not found: {path}")

    log_info("Loading config", path=str(config_path))
    try:
        if filesystem is not None:
            # Use provided filesystem for I/O
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
            # Use default path-based file I/O
            raw_text = config_path.read_text()
    except OSError as exc:  # pragma: no cover - filesystem failures are rare
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
    except Exception as exc:  # pragma: no cover - raised in tests
        raise ConfigError(f"Configuration validation failed: {exc}") from exc

    # Resolve relative paths if requested (simplified for now)
    if resolve_paths:
        log_debug(
            "Path resolution requested but not implemented in refactored structure"
        )

    # Load SQL from external files if requested
    if load_sql_files:
        config = _load_sql_files_from_config(config, config_path, sql_file_loader)

    log_info("Config loaded", path=str(config_path), views=len(config.views))
    return config
