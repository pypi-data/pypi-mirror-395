"""Validation and path resolution utilities for configuration processing.

This module contains complex validation helper functions and path resolution logic
used throughout the configuration system.
"""

import os
import re
from pathlib import Path
from typing import Any, Optional, Union

from loguru import logger
from duckalog.errors import ConfigError, PathResolutionError


# Logging and redaction utilities
LOGGER_NAME = "duckalog"
SENSITIVE_KEYWORDS = ("password", "secret", "token", "key", "pwd")


def get_logger(name: str = LOGGER_NAME):
    """Return a logger configured for Duckalog."""
    return logger.bind(name=name)


def _is_sensitive(key: str) -> bool:
    """Check if a key contains sensitive information."""
    lowered = key.lower()
    return any(keyword in lowered for keyword in SENSITIVE_KEYWORDS)


def _redact_value(value: Any, key_hint: str = "") -> Any:
    """Redact sensitive values from log data."""
    if isinstance(value, dict):
        return {k: _redact_value(v, k) for k, v in value.items()}
    if isinstance(value, list):
        return [_redact_value(item, key_hint) for item in value]
    if isinstance(value, str) and _is_sensitive(key_hint):
        return "***REDACTED***"
    return value


def _emit_loguru_logger(level_name: str, message: str, safe_details: dict[str, Any]) -> None:
    """Emit a log message using loguru."""
    if safe_details:
        logger.log(level_name, "{} {}", message, safe_details)
    else:
        logger.log(level_name, message)


def _log(level: int, message: str, **details: Any) -> None:
    """Log a redacted message."""
    safe_details: dict[str, Any] = {}
    if details:
        safe_details = {k: _redact_value(v, k) for k, v in details.items()}

    # Map stdlib logging levels to loguru
    level_map = {
        20: "INFO",   # logging.INFO
        10: "DEBUG",  # logging.DEBUG
        40: "ERROR",  # logging.ERROR
    }
    level_name = level_map.get(level, "INFO")
    _emit_loguru_logger(level_name, message, safe_details)


def log_info(message: str, **details: Any) -> None:
    """Log a redacted INFO-level message."""
    _log(20, message, **details)


def log_debug(message: str, **details: Any) -> None:
    """Log a redacted DEBUG-level message."""
    _log(10, message, **details)


def log_error(message: str, **details: Any) -> None:
    """Log a redacted ERROR-level message."""
    _log(40, message, **details)


# Path resolution and validation functions


def is_relative_path(path: str) -> bool:
    """Detect if a path is relative based on platform-specific rules."""
    if not path or not path.strip():
        return False

    # Check for protocols (http, s3, gs, https, etc.)
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", path):
        return False

    # Platform-specific checks
    try:
        if Path(path).is_absolute():
            return False
    except (OSError, ValueError):
        # Path might contain invalid characters for the current platform
        pass

    # Windows drive letter check (C:, D:, etc.)
    if re.match(r"^[a-zA-Z]:[\\\\/]", path):
        return False

    # Windows UNC path check (\\server\share)
    if path.startswith("\\\\"):
        return False

    return True


def resolve_relative_path(path: str, config_dir: Path) -> str:
    """Resolve a relative path to an absolute path relative to config directory."""
    if not path or not path.strip():
        raise ValueError("Path cannot be empty")

    path = path.strip()

    # If path is already absolute, return as-is
    if not is_relative_path(path):
        return path

    # Resolve relative path against config directory
    try:
        config_dir = config_dir.resolve()
        resolved_path = config_dir / path
        resolved_path = resolved_path.resolve()

        log_debug(
            f"Resolved relative path: {path} -> {resolved_path}",
            config_dir=str(config_dir),
        )

        return str(resolved_path)

    except (OSError, ValueError) as exc:
        raise ValueError(
            f"Failed to resolve path '{path}' relative to '{config_dir}': {exc}"
        ) from exc


def validate_path_security(path: str, config_dir: Path) -> bool:
    """Validate that resolved paths don't violate security boundaries."""
    if not path or not path.strip():
        return False

    # Remote URIs are considered safe
    if not is_relative_path(path):
        # Check if it's a remote URI (has protocol)
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", path):
            return True

    try:
        # Resolve relative paths only
        if is_relative_path(path):
            resolved_path_str = resolve_relative_path(path, config_dir.resolve())
            resolved_path = Path(resolved_path_str)
        else:
            # For non-relative local paths, validate them
            resolved_path = Path(path).resolve()

        config_dir_resolved = config_dir.resolve()

        # Check if resolved path is within allowed roots
        try:
            if is_within_allowed_roots(str(resolved_path), [config_dir_resolved]):
                return True
            else:
                log_debug(
                    f"Path resolution security violation: {resolved_path} is outside allowed root {config_dir_resolved}"
                )
                return False
        except ValueError as exc:
            # Path resolution failed (invalid path)
            log_debug(
                f"Path resolution validation failed: {exc}",
                path=path,
                resolved_path=str(resolved_path),
            )
            return False

    except (OSError, ValueError, RuntimeError):
        return False


def normalize_path_for_sql(path: str) -> str:
    """Normalize a path for use in SQL statements."""
    if not path or not path.strip():
        raise ValueError("Path cannot be empty")

    path = path.strip()

    # Convert to Path object for normalization
    try:
        path_obj = Path(path)
        normalized = str(path_obj)
    except (OSError, ValueError):
        # If pathlib can't handle it, use as-is
        normalized = path

    # Import quote_literal from sql_generation to avoid circular imports
    from duckalog.sql_generation import quote_literal

    return quote_literal(normalized)


def is_within_allowed_roots(candidate_path: str, allowed_roots: list[Path]) -> bool:
    """Check if a resolved path is within any of the allowed root directories."""
    try:
        # Resolve the candidate path to absolute, following symlinks
        resolved_candidate = Path(candidate_path).resolve()
    except (OSError, ValueError, RuntimeError) as exc:
        raise ValueError(f"Cannot resolve path '{candidate_path}': {exc}") from exc

    # Resolve all allowed roots to absolute paths
    try:
        resolved_roots = [root.resolve() for root in allowed_roots]
    except (OSError, ValueError, RuntimeError) as exc:
        raise ValueError(f"Cannot resolve allowed root: {exc}") from exc

    # Check if candidate is within any allowed root
    for root in resolved_roots:
        try:
            # Use commonpath to find the common prefix
            common = Path(os.path.commonpath([resolved_candidate, root]))

            # If the common path equals the root, then candidate is within this root
            if common == root:
                return True

        except ValueError:
            # os.path.commonpath raises ValueError when paths are on different
            # drives (Windows) or have no common prefix - treat as not within root
            continue

    return False


def is_windows_path_absolute(path: str) -> bool:
    """Check Windows-specific absolute path patterns."""
    # Drive letter: C:\path
    if re.match(r"^[a-zA-Z]:[\\\\/]", path):
        return True

    # UNC path: \\server\share
    if path.startswith("\\\\"):
        return True

    return False


def detect_path_type(path: str) -> str:
    """Detect the type of path for categorization."""
    if not path or not path.strip():
        return "invalid"

    # Check for remote URIs with protocols
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", path):
        return "remote"

    # Check for absolute paths
    if not is_relative_path(path):
        return "absolute"

    # Otherwise it's relative
    return "relative"


def validate_file_accessibility(path: str) -> tuple[bool, Optional[str]]:
    """Validate that a file path is accessible."""
    if not path or not path.strip():
        return False, "Path cannot be empty"

    try:
        path_obj = Path(path)

        # Check if file exists
        if not path_obj.exists():
            return False, f"File does not exist: {path}"

        # Check if it's a file (not a directory)
        if not path_obj.is_file():
            return False, f"Path is not a file: {path}"

        # Check if file is readable
        try:
            with open(path_obj, "rb"):
                pass
        except PermissionError:
            return False, f"Permission denied reading file: {path}"
        except OSError as exc:
            return False, f"Error accessing file {path}: {exc}"

        return True, None

    except (OSError, ValueError) as exc:
        return False, f"Invalid path: {exc}"


def _resolve_paths_in_config(config, config_path: Path):
    """Resolve relative paths in a configuration to absolute paths.

    This function processes view URIs and attachment paths, resolving any
    relative paths to absolute paths relative to the configuration file's directory.

    Args:
        config: The loaded configuration object
        config_path: Path to the configuration file

    Returns:
        The configuration with resolved paths

    Raises:
        ConfigError: If path resolution fails due to security or access issues
    """
    try:
        # Import Config here to avoid circular imports
        from duckalog.config.models import Config

        config_dict = config.model_dump(mode="python")
        config_dir = config_path.parent

        # Resolve paths in views
        if "views" in config_dict and config_dict["views"]:
            for view_data in config_dict["views"]:
                _resolve_view_paths(view_data, config_dir)

        # Resolve paths in attachments
        if "attachments" in config_dict and config_dict["attachments"]:
            _resolve_attachment_paths(config_dict["attachments"], config_dir)

        # Re-validate the config with resolved paths
        resolved_config = Config.model_validate(config_dict)

        log_debug(
            "Path resolution completed",
            config_path=str(config_path),
            views_count=len(resolved_config.views),
            attachments_count=len(
                resolved_config.attachments.duckdb
                + resolved_config.attachments.sqlite
                + resolved_config.attachments.postgres
                + resolved_config.attachments.duckalog
            ),
        )

        return resolved_config

    except Exception as exc:
        raise ConfigError(f"Path resolution failed: {exc}") from exc


def _resolve_view_paths(view_data: dict, config_dir: Path) -> None:
    """Resolve paths in a single view configuration.

    Args:
        view_data: Dictionary representation of a view
        config_dir: Configuration file directory

    Raises:
        PathResolutionError: If path resolution fails security validation
    """
    if "uri" in view_data and view_data["uri"]:
        original_uri = view_data["uri"]

        if is_relative_path(original_uri):
            # Resolve the path (security validation is handled within resolve_relative_path)
            try:
                resolved_uri = resolve_relative_path(original_uri, config_dir)
                view_data["uri"] = resolved_uri
                log_debug(
                    "Resolved view URI", original=original_uri, resolved=resolved_uri
                )
            except ValueError as exc:
                raise PathResolutionError(
                    f"Failed to resolve URI '{original_uri}': {exc}",
                    original_path=original_uri,
                ) from exc


def _resolve_attachment_paths(attachments_data: dict, config_dir: Path) -> None:
    """Resolve paths in attachment configurations.

    Args:
        attachments_data: Dictionary representation of attachments
        config_dir: Configuration file directory

    Raises:
        PathResolutionError: If path resolution fails security validation
    """
    # Resolve DuckDB attachment paths
    if "duckdb" in attachments_data and attachments_data["duckdb"]:
        for attachment in attachments_data["duckdb"]:
            if "path" in attachment and attachment["path"]:
                original_path = attachment["path"]

                if is_relative_path(original_path):
                    # Resolve the path (security validation is handled within resolve_relative_path)
                    try:
                        resolved_path = resolve_relative_path(original_path, config_dir)
                        attachment["path"] = resolved_path
                        log_debug(
                            "Resolved DuckDB attachment",
                            original=original_path,
                            resolved=resolved_path,
                        )
                    except ValueError as exc:
                        raise PathResolutionError(
                            f"Failed to resolve DuckDB attachment path '{original_path}': {exc}",
                            original_path=original_path,
                        ) from exc

    # Resolve SQLite attachment paths
    if "sqlite" in attachments_data and attachments_data["sqlite"]:
        for attachment in attachments_data["sqlite"]:
            if "path" in attachment and attachment["path"]:
                original_path = attachment["path"]

                if is_relative_path(original_path):
                    # Resolve the path (security validation is handled within resolve_relative_path)
                    try:
                        resolved_path = resolve_relative_path(original_path, config_dir)
                        attachment["path"] = resolved_path
                        log_debug(
                            "Resolved SQLite attachment",
                            original=original_path,
                            resolved=resolved_path,
                        )
                    except ValueError as exc:
                        raise PathResolutionError(
                            f"Failed to resolve SQLite attachment path '{original_path}': {exc}",
                            original_path=original_path,
                        ) from exc

    # Resolve Duckalog attachment paths
    if "duckalog" in attachments_data and attachments_data["duckalog"]:
        for attachment in attachments_data["duckalog"]:
            # Resolve config_path relative to parent config
            if "config_path" in attachment and attachment["config_path"]:
                original_path = attachment["config_path"]
                if is_relative_path(original_path):
                    try:
                        resolved_path = resolve_relative_path(original_path, config_dir)
                        attachment["config_path"] = resolved_path
                        log_debug(
                            "Resolved Duckalog attachment config path",
                            original=original_path,
                            resolved=resolved_path,
                        )
                    except ValueError as exc:
                        raise PathResolutionError(
                            f"Failed to resolve Duckalog attachment config_path '{original_path}': {exc}",
                            original_path=original_path,
                        ) from exc

            # Resolve database override relative to parent config
            if "database" in attachment and attachment["database"]:
                original_db = attachment["database"]
                if is_relative_path(original_db):
                    try:
                        resolved_db = resolve_relative_path(original_db, config_dir)
                        attachment["database"] = resolved_db
                        log_debug(
                            "Resolved Duckalog attachment database override",
                            original=original_db,
                            resolved=resolved_db,
                        )
                    except ValueError as exc:
                        raise PathResolutionError(
                            f"Failed to resolve Duckalog attachment database '{original_db}': {exc}",
                            original_path=original_db,
                        ) from exc
