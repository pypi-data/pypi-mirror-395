"""Configuration loading orchestration for Duckalog catalogs.

This module provides the main entry points for loading and processing configuration files,
handling both local file loading and remote URI loading.
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Union

import yaml

from duckalog.errors import (
    CircularImportError,
    ConfigError,
    DuplicateNameError,
    ImportError,
    ImportFileNotFoundError,
    ImportValidationError,
    PathResolutionError,
)
from .validators import log_info, log_debug


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
    """Load SQL content from external files referenced in the config.

    This function processes views that reference external SQL files or templates
    and inlines the SQL content into the configuration.

    Args:
        config: The configuration object to process
        config_path: Path to the configuration file (for relative path resolution)
        sql_file_loader: Optional SQLFileLoader instance for loading SQL files

    Returns:
        Updated configuration with SQL content inlined

    Raises:
        ConfigError: If the config contains SQL file references that cannot be loaded
    """
    # Import here to avoid circular import
    from ..sql_file_loader import SQLFileError, SQLFileLoader

    if sql_file_loader is None:
        sql_file_loader = SQLFileLoader()

    # Check if any views have SQL file references
    has_sql_files = any(
        getattr(view, "sql_file", None) is not None
        or getattr(view, "sql_template", None) is not None
        for view in config.views
    )

    if not has_sql_files:
        # No SQL files to process
        return config

    log_info("Loading SQL files", total_views=len(config.views))

    updated_views = []
    for view in config.views:
        if view.sql_file is not None:
            # Handle direct SQL file reference
            try:
                sql_content = sql_file_loader.load_sql_file(
                    file_path=view.sql_file.path,
                    config_file_path=str(config_path),
                    variables=view.sql_file.variables,
                    as_template=view.sql_file.as_template,
                )

                # Create new view with inline SQL
                updated_view = view.model_copy(
                    update={"sql": sql_content, "sql_file": None}
                )
                updated_views.append(updated_view)
                log_debug("Loaded SQL file for view", view_name=view.name)

            except SQLFileError as exc:
                raise ConfigError(
                    f"Failed to load SQL file for view '{view.name}': {exc}"
                ) from exc

        elif view.sql_template is not None:
            # Handle SQL template reference
            try:
                sql_content = sql_file_loader.load_sql_file(
                    file_path=view.sql_template.path,
                    config_file_path=str(config_path),
                    variables=view.sql_template.variables,
                    as_template=True,  # Templates are always processed as templates
                )

                # Create new view with inline SQL
                updated_view = view.model_copy(
                    update={"sql": sql_content, "sql_template": None}
                )
                updated_views.append(updated_view)
                log_debug("Loaded SQL template for view", view_name=view.name)

            except SQLFileError as exc:
                raise ConfigError(
                    f"Failed to load SQL template for view '{view.name}': {exc}"
                ) from exc

        else:
            # No SQL file reference, keep original view
            updated_views.append(view)

    # Create updated config with processed views
    updated_config = config.model_copy(update={"views": updated_views})

    file_based_views = len(
        [
            v
            for v in updated_views
            if v.sql
            and v != next((ov for ov in config.views if ov.name == v.name), None)
        ]
    )

    log_info(
        "SQL files loaded",
        total_views=len(config.views),
        file_based_views=file_based_views,
    )

    return updated_config


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

    # Local file loading - delegate to the dedicated helper with import support
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
    """Load a configuration from a local file with import support.

    This is an internal helper responsible for local file reading, environment
    interpolation, path resolution, validation, and import processing.

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
    config_path = Path(path)
    if not config_path.exists():
        raise ConfigError(f"Config file not found: {path}")

    log_info("Loading config", path=str(config_path))

    # Use the new _load_config_with_imports function which handles everything
    return _load_config_with_imports(
        file_path=str(config_path),
        filesystem=filesystem,
        resolve_paths=resolve_paths,
        load_sql_files=load_sql_files,
        sql_file_loader=sql_file_loader,
    )


@dataclass
class ImportContext:
    """Tracks import state during loading."""
    visited_files: set[str] = field(default_factory=set)
    import_stack: list[str] = field(default_factory=list)
    config_cache: dict[str, Any] = field(default_factory=dict)
    import_chain: list[str] = field(default_factory=list)


def _normalize_uri(uri: str) -> str:
    """Normalize a URI for consistent tracking in visited files set.

    This ensures that different representations of the same URI (e.g., with or
    without trailing slashes) are treated as the same file for circular import
    detection.

    Args:
        uri: The URI to normalize

    Returns:
        Normalized URI string
    """
    if not _is_remote_uri(uri):
        # For local files, use the absolute path
        return uri

    from urllib.parse import urlparse

    parsed = urlparse(uri)

    # Normalize the URI by reconstructing it with normalized components
    # - Use lowercase scheme
    # - Remove default ports
    # - Remove trailing slashes from path
    # - Normalize the netloc (remove default user info formatting)
    scheme = parsed.scheme.lower()

    netloc = parsed.netloc
    if netloc:
        # Split netloc into components
        if "@" in netloc:
            # Has authentication info
            auth, host = netloc.rsplit("@", 1)
        else:
            auth, host = "", netloc

        # Normalize host (lowercase, remove brackets for IPv6)
        if ":" in host and not host.startswith("["):
            # IPv6 address
            host = f"[{host}]"

        # Reconstruct netloc
        if auth:
            netloc = f"{auth}@{host}"
        else:
            netloc = host

    path = parsed.path.rstrip("/") if parsed.path != "/" else "/"

    # Reconstruct query without sorting to preserve order
    query = f"?{parsed.query}" if parsed.query else ""

    # Reconstruct fragment
    fragment = f"#{parsed.fragment}" if parsed.fragment else ""

    # Reconstruct URI
    normalized = f"{scheme}://{netloc}{path}{query}{fragment}"

    return normalized


def _is_remote_uri(path: str) -> bool:
    """Check if a path is a remote URI.

    This function uses the comprehensive implementation from remote_config.py
    to support all URI schemes including S3, GCS, Azure Blob, SFTP, and HTTPS.
    """
    try:
        from duckalog.remote_config import is_remote_uri as check_remote_uri

        return check_remote_uri(path)
    except ImportError:
        # Fallback to simple check if remote config is not available
        remote_schemes = ["http://", "https://", "s3://", "gcs://", "az://", "abfs://"]
        return any(path.startswith(scheme) for scheme in remote_schemes)


def _expand_glob_patterns(
    patterns: list[str],
    base_path: str,
    filesystem: Optional[Any] = None,
) -> list[str]:
    """Expand glob patterns into a list of matching file paths.

    Args:
        patterns: List of patterns, which can include glob patterns (*, ?, [...])
                  and exclude patterns (starting with !).
        base_path: Base path to resolve relative patterns against.
        filesystem: Optional filesystem object for remote operations.

    Returns:
        List of resolved file paths in deterministic order.

    Raises:
        ImportFileNotFoundError: If a pattern doesn't match any files.
    """
    import glob as glob_module

    resolved_files = []
    excluded_files = set()

    for pattern in patterns:
        # Handle exclude patterns
        if pattern.startswith("!"):
            exclude_pattern = pattern[1:]
            # Resolve relative to base_path
            if not _is_remote_uri(exclude_pattern):
                exclude_pattern = str(Path(base_path).parent / exclude_pattern)

            if _is_remote_uri(exclude_pattern):
                # For remote files, we can't easily glob, so skip exclude
                continue

            # Get all matching files for exclusion
            try:
                matches = glob_module.glob(exclude_pattern, recursive=True)
                excluded_files.update(matches)
            except Exception:
                # If glob fails, skip this exclude pattern
                pass
            continue

        # Handle include patterns
        # Resolve relative to base_path
        if not _is_remote_uri(pattern):
            resolved_pattern = str(Path(base_path).parent / pattern)
        else:
            # For remote URIs, glob patterns aren't supported yet
            if "*" in pattern or "?" in pattern:
                raise ImportError(
                    f"Glob patterns are not supported for remote URIs: {pattern}"
                )
            resolved_pattern = pattern

        if _is_remote_uri(resolved_pattern):
            # Remote file - add directly
            resolved_files.append(resolved_pattern)
        else:
            # Local file - expand glob
            try:
                matches = glob_module.glob(resolved_pattern, recursive=True)
                if not matches:
                    # Check if this is meant to be a single file (no glob chars)
                    if "*" not in resolved_pattern and "?" not in resolved_pattern:
                        # Single file - add it if it exists
                        if Path(resolved_pattern).exists():
                            resolved_files.append(resolved_pattern)
                    else:
                        # Glob pattern with no matches
                        raise ImportFileNotFoundError(
                            f"No files match pattern: {pattern}"
                        )
                else:
                    # Sort for deterministic order
                    resolved_files.extend(sorted(matches))
            except Exception as exc:
                raise ImportError(
                    f"Failed to expand glob pattern '{pattern}': {exc}"
                ) from exc

    # Remove excluded files
    result = [f for f in resolved_files if f not in excluded_files]

    # Remove duplicates while preserving order
    seen = set()
    final_result = []
    for f in result:
        if f not in seen:
            seen.add(f)
            final_result.append(f)

    log_debug(
        "Expanded glob patterns",
        input_patterns=patterns,
        resolved_files=final_result,
    )

    return final_result


def _resolve_import_path(import_path: str, base_path: str) -> str:
    """Resolve an import path relative to the base configuration file.

    Args:
        import_path: The import path (can be relative, absolute, or remote URI).
        base_path: Path to the base configuration file.

    Returns:
        Resolved import path as a string.

    Raises:
        PathResolutionError: If the import path cannot be resolved.
    """
    # If it's a remote URI, return as-is
    if _is_remote_uri(import_path):
        return import_path

    # Handle absolute paths
    if Path(import_path).is_absolute():
        return import_path

    # Handle relative paths - resolve relative to the directory containing base_path
    base_dir = Path(base_path).parent
    resolved_path = (base_dir / import_path).resolve()

    if not resolved_path.exists():
        raise PathResolutionError(
            f"Failed to resolve import path: {import_path}",
            f"Resolved path does not exist: {resolved_path}",
        )

    return str(resolved_path)


def _normalize_imports_for_processing(
    imports: Union[list[str], Any],
    base_path: str,
    filesystem: Optional[Any] = None,
) -> list[tuple[str, bool, Optional[str]]]:
    """Normalize imports for processing.

    Converts various import formats into a list of tuples:
    (resolved_path, override, section_name)

    Args:
        imports: Can be a simple list of strings or a SelectiveImports object
        base_path: Base path to resolve relative patterns against
        filesystem: Optional filesystem for remote operations

    Returns:
        List of tuples: (path, override, section_name)
        where section_name is None for global imports or the section name for selective imports
    """
    from .models import ImportEntry

    # Handle simple list format (backward compatible)
    if isinstance(imports, list):
        normalized = []
        for item in imports:
            if isinstance(item, str):
                # Simple string path
                normalized.append((item, True, None))
            elif isinstance(item, ImportEntry):
                # ImportEntry with options
                normalized.append((item.path, item.override, None))
            else:
                raise ConfigError(
                    f"Invalid import format: expected string or ImportEntry, got {type(item)}"
                )
        return normalized

    # Handle SelectiveImports object
    if hasattr(imports, "model_fields"):
        # This is a SelectiveImports object
        from .models import SelectiveImports

        normalized = []

        # Process each section
        for field_name, field_value in imports:
            if field_value is None:
                continue

            section_name = field_name

            for item in field_value:
                if isinstance(item, str):
                    # Simple string path
                    normalized.append((item, True, section_name))
                elif isinstance(item, ImportEntry):
                    # ImportEntry with options
                    override = item.override
                    normalized.append((item.path, override, section_name))
                else:
                    raise ConfigError(
                        f"Invalid import format in {section_name}: expected string or ImportEntry, got {type(item)}"
                    )

        return normalized

    # Fallback: treat as list
    return [(str(path), True, None) for path in imports]


def _deep_merge_dict(base: dict, override: dict) -> dict:
    """Deep merge two dictionaries.

    Args:
        base: Base dictionary to merge into.
        override: Override dictionary with new/updated values.

    Returns:
        A new dictionary with merged content.
    """
    result = base.copy()

    for key, override_value in override.items():
        if key not in result:
            # New key, just add it
            result[key] = override_value
        else:
            # Key exists, need to merge
            base_value = result[key]

            if isinstance(base_value, dict) and isinstance(override_value, dict):
                # Both are dicts, recursively merge
                result[key] = _deep_merge_dict(base_value, override_value)
            elif isinstance(base_value, list) and isinstance(override_value, list):
                # Both are lists, concatenate
                result[key] = base_value + override_value
            else:
                # Override scalar values
                result[key] = override_value

    return result


def _merge_config_with_override(
    base: Any,
    override: Any,
    override_mode: bool = True,
) -> Any:
    """Merge two Config objects with override control.

    Args:
        base: Base Config object (imported config).
        override: Override Config object (main config or later import).
        override_mode: If True, values from override take precedence (normal merge).
                      If False, only fill in missing fields without overwriting existing ones.

    Returns:
        A new Config object with merged content.
    """
    from .models import Config

    # Get the field values from both configs
    base_dict = base.model_dump(mode='json')
    override_dict = override.model_dump(mode='json')

    log_debug("Deep merge base keys", keys=list(base_dict.keys()))
    log_debug("Deep merge override keys", keys=list(override_dict.keys()))

    # Extract imports from override before merging
    # Import configs shouldn't have their own imports field in the final merged config
    # Only the main config's imports should be kept
    override_imports = override_dict.get('imports', [])

    # Also remove imports from base_dict to ensure only main config's imports are used
    base_dict = base_dict.copy()
    base_dict.pop('imports', None)

    # Remove imports from override_dict after extraction
    override_dict = override_dict.copy()
    override_dict.pop('imports', None)

    log_debug("After removing imports - base_dict keys", keys=list(base_dict.keys()))
    log_debug("After removing imports - override_dict keys", keys=list(override_dict.keys()))

    # Deep merge the dicts
    if override_mode:
        # Normal merge: override takes precedence
        merged_dict = _deep_merge_dict(base_dict, override_dict)
    else:
        # Non-overriding merge: only fill in missing fields
        merged_dict = base_dict.copy()
        for key, value in override_dict.items():
            if key not in merged_dict or merged_dict[key] is None:
                merged_dict[key] = value

    # Set the imports field to the main config's imports
    merged_dict['imports'] = override_imports

    log_debug("Deep merge result keys", keys=list(merged_dict.keys()))

    try:
        # Create a new Config from the merged dict
        # Use ** to unpack the dict and let Pydantic properly instantiate nested objects
        result = Config(**merged_dict)
        log_debug("Config created successfully", views=len(result.views))
        return result
    except ValueError as e:
        # Check if this is a duplicate name error from the Config model validator
        if "Duplicate view name" in str(e):
            # Extract duplicate names from error message
            import re
            match = re.search(r"Duplicate view name\(s\) found: (.+)", str(e))
            if match:
                duplicates = match.group(1)
                raise DuplicateNameError(
                    f"Duplicate view name(s) found: {duplicates}",
                    name_type="view",
                    duplicate_names=[d.strip() for d in duplicates.split(",")],
                ) from e
        # Check for other duplicate types
        elif "Duplicate Iceberg catalog name" in str(e):
            raise DuplicateNameError(
                str(e), name_type="iceberg_catalog"
            ) from e
        elif "Duplicate semantic model name" in str(e):
            raise DuplicateNameError(
                str(e), name_type="semantic_model"
            ) from e
        elif "Duplicate attachment alias" in str(e):
            raise DuplicateNameError(
                str(e), name_type="attachment"
            ) from e
        # Re-raise as is if not a duplicate error
        log_debug("Failed to create Config", error=str(e))
        log_debug("merged_dict details", merged_dict=str(merged_dict))
        raise
    except Exception as e:
        log_debug("Failed to create Config", error=str(e))
        log_debug("merged_dict details", merged_dict=str(merged_dict))
        raise


def _merge_section_specific(
    imported_config: Any,
    base_config: Any,
    section_name: str,
    override_mode: bool = True,
) -> Any:
    """Merge a specific section from imported config into base config.

    Args:
        imported_config: Config object to merge from.
        base_config: Config object to merge into.
        section_name: Name of the section to merge (e.g., 'views', 'duckdb').
        override_mode: If True, values from imported_config take precedence.
                      If False, only fill in missing fields.

    Returns:
        A new Config object with the merged section.
    """
    from .models import Config

    # Get the field values from both configs
    imported_dict = imported_config.model_dump(mode='json')
    base_dict = base_config.model_dump(mode='json')

    log_debug(
        "Merging section-specific imports",
        section=section_name,
        override_mode=override_mode,
    )

    # Check if the section exists in the imported config
    if section_name not in imported_dict:
        log_debug("Section not found in imported config", section=section_name)
        return base_config

    # Get the section value from imported config
    imported_section = imported_dict.get(section_name)

    # Remove imports from both dicts
    imported_dict.pop('imports', None)
    base_dict.pop('imports', None)

    # Create a copy of base_dict to modify
    merged_dict = base_dict.copy()

    # Merge only the specified section
    if section_name in merged_dict:
        base_section = merged_dict[section_name]

        if override_mode:
            # Normal merge: imported takes precedence
            if isinstance(base_section, dict) and isinstance(imported_section, dict):
                merged_dict[section_name] = _deep_merge_dict(base_section, imported_section)
            elif isinstance(base_section, list) and isinstance(imported_section, list):
                # For lists, concatenate
                merged_dict[section_name] = base_section + imported_section
            else:
                # Override scalar values
                merged_dict[section_name] = imported_section
        else:
            # Non-overriding merge: only fill in missing fields
            if isinstance(base_section, dict) and isinstance(imported_section, dict):
                for key, value in imported_section.items():
                    if key not in base_section or base_section[key] is None:
                        merged_dict[section_name][key] = value
            elif isinstance(base_section, list) and isinstance(imported_section, list):
                # For lists, append if not already present
                for item in imported_section:
                    if item not in base_section:
                        merged_dict[section_name].append(item)
            else:
                # Only set if not already set
                if base_section is None:
                    merged_dict[section_name] = imported_section
    else:
        # Section doesn't exist in base, just add it
        merged_dict[section_name] = imported_section

    # Set the imports field to the base config's imports
    merged_dict['imports'] = base_dict.get('imports', [])

    try:
        # Create a new Config from the merged dict
        result = Config(**merged_dict)
        log_debug("Section merged successfully", section=section_name)
        return result
    except ValueError as e:
        # Check if this is a duplicate name error from the Config model validator
        if "Duplicate view name" in str(e):
            # Extract duplicate names from error message
            import re
            match = re.search(r"Duplicate view name\(s\) found: (.+)", str(e))
            if match:
                duplicates = match.group(1)
                raise DuplicateNameError(
                    f"Duplicate view name(s) found: {duplicates}",
                    name_type="view",
                    duplicate_names=[d.strip() for d in duplicates.split(",")],
                ) from e
        # Check for other duplicate types
        elif "Duplicate Iceberg catalog name" in str(e):
            raise DuplicateNameError(
                str(e), name_type="iceberg_catalog"
            ) from e
        elif "Duplicate semantic model name" in str(e):
            raise DuplicateNameError(
                str(e), name_type="semantic_model"
            ) from e
        elif "Duplicate attachment alias" in str(e):
            raise DuplicateNameError(
                str(e), name_type="attachment"
            ) from e
        # Re-raise as is if not a duplicate error
        log_debug("Failed to create Config", error=str(e))
        log_debug("merged_dict details", merged_dict=str(merged_dict))
        raise
    except Exception as e:
        log_debug("Failed to create Config", error=str(e))
        log_debug("merged_dict details", merged_dict=str(merged_dict))
        raise


def _resolve_import_path(import_path: str, base_path: str) -> str:
    """Resolve an import path relative to the importing file.

    Args:
        import_path: The import path to resolve (can contain ${env:VAR}).
        base_path: Path to the importing file.

    Returns:
        The resolved absolute path.

    Raises:
        PathResolutionError: If path resolution fails.
    """
    # Apply environment variable interpolation
    if "${env:" in import_path:
        import_path = _interpolate_env(import_path)

    # Check if it's a remote URI
    if _is_remote_uri(import_path):
        return import_path

    # Resolve relative to base file
    if os.path.isabs(import_path):
        resolved_path = import_path
    else:
        base_dir = os.path.dirname(base_path)
        resolved_path = os.path.normpath(os.path.join(base_dir, import_path))

    # Security check - ensure path doesn't escape allowed directory
    # This is a basic check - the actual validation will happen during file loading
    if not os.path.isabs(resolved_path):
        raise PathResolutionError(
            f"Failed to resolve import path: {import_path}",
            original_path=import_path,
            resolved_path=resolved_path,
        )

    return resolved_path


def _validate_unique_names(config: Any, context: ImportContext) -> None:
    """Validate unique names across all config sections.

    Args:
        config: The merged Config object.
        context: Import context with import chain information.

    Raises:
        DuplicateNameError: If duplicate names are found.
    """
    # Validate unique view names
    view_names: dict[tuple[Optional[str], str], int] = {}
    duplicates = []
    for view in config.views:
        key = (view.db_schema, view.name)
        if key in view_names:
            schema_part = f"{view.db_schema}." if view.db_schema else ""
            duplicates.append(f"{schema_part}{view.name}")
        else:
            view_names[key] = 1

    if duplicates:
        raise DuplicateNameError(
            f"Duplicate view name(s) found: {', '.join(sorted(set(duplicates)))}",
            name_type="view",
            duplicate_names=sorted(set(duplicates)),
        )

    # Validate unique Iceberg catalog names
    catalog_names: dict[str, int] = {}
    duplicates = []
    for catalog in config.iceberg_catalogs:
        if catalog.name in catalog_names:
            duplicates.append(catalog.name)
        else:
            catalog_names[catalog.name] = 1

    if duplicates:
        raise DuplicateNameError(
            f"Duplicate Iceberg catalog name(s) found: {', '.join(sorted(set(duplicates)))}",
            name_type="iceberg_catalog",
            duplicate_names=sorted(set(duplicates)),
        )

    # Validate unique semantic model names
    semantic_model_names: dict[str, int] = {}
    duplicates = []
    for semantic_model in config.semantic_models:
        if semantic_model.name in semantic_model_names:
            duplicates.append(semantic_model.name)
        else:
            semantic_model_names[semantic_model.name] = 1

    if duplicates:
        raise DuplicateNameError(
            f"Duplicate semantic model name(s) found: {', '.join(sorted(set(duplicates)))}",
            name_type="semantic_model",
            duplicate_names=sorted(set(duplicates)),
        )

    # Validate unique attachment aliases
    attachment_aliases: dict[str, int] = {}
    duplicates = []

    # Check duckdb attachments
    for attachment in config.attachments.duckdb:
        if attachment.alias in attachment_aliases:
            duplicates.append(f"duckdb.{attachment.alias}")
        else:
            attachment_aliases[attachment.alias] = 1

    # Check sqlite attachments
    for attachment in config.attachments.sqlite:
        if attachment.alias in attachment_aliases:
            duplicates.append(f"sqlite.{attachment.alias}")
        else:
            attachment_aliases[attachment.alias] = 1

    # Check postgres attachments
    for attachment in config.attachments.postgres:
        if attachment.alias in attachment_aliases:
            duplicates.append(f"postgres.{attachment.alias}")
        else:
            attachment_aliases[attachment.alias] = 1

    # Check duckalog attachments
    for attachment in config.attachments.duckalog:
        if attachment.alias in attachment_aliases:
            duplicates.append(f"duckalog.{attachment.alias}")
        else:
            attachment_aliases[attachment.alias] = 1

    if duplicates:
        raise DuplicateNameError(
            f"Duplicate attachment alias(es) found: {', '.join(sorted(set(duplicates)))}",
            name_type="attachment",
            duplicate_names=sorted(set(duplicates)),
        )


def _resolve_and_load_import(
    import_path: str,
    base_path: str,
    filesystem: Optional[Any],
    resolve_paths: bool,
    load_sql_files: bool,
    sql_file_loader: Optional[Any],
    import_context: ImportContext,
) -> Any:
    """Resolve and load an imported config file.

    Args:
        import_path: Path to the import (can be relative or remote).
        base_path: Path to the importing file.
        filesystem: Optional filesystem object.
        resolve_paths: Whether to resolve relative paths.
        load_sql_files: Whether to load SQL files.
        sql_file_loader: Optional SQLFileLoader instance.
        import_context: Import context for tracking visited files.

    Returns:
        The loaded Config object.

    Raises:
        CircularImportError: If a circular import is detected.
        ImportFileNotFoundError: If the imported file doesn't exist.
        ImportValidationError: If the imported config fails validation.
    """
    # Resolve the import path
    try:
        resolved_path = _resolve_import_path(import_path, base_path)
    except Exception as exc:
        raise ImportFileNotFoundError(
            f"Failed to resolve import path '{import_path}' from '{base_path}': {exc}",
            import_path=import_path,
            cause=exc,
        ) from exc

    log_debug("Resolving import", import_path=import_path, resolved_path=resolved_path)

    # Normalize the path for consistent tracking in visited files
    # This ensures remote URIs are normalized for circular import detection
    normalized_path = _normalize_uri(resolved_path)

    # Check for circular imports
    # Use the normalized path as the key to handle different representations of the same URI
    if normalized_path in import_context.visited_files:
        # Check if it's in the current import stack
        if normalized_path in import_context.import_stack:
            # Circular import detected!
            # Show the import chain with normalized paths
            chain = " -> ".join(
                _normalize_uri(p) for p in import_context.import_stack + [resolved_path]
            )
            raise CircularImportError(
                f"Circular import detected in import chain: {chain}",
                import_chain=import_context.import_stack + [resolved_path],
            )
        else:
            # This file was already loaded in a different branch, use cached version
            log_debug("Using cached config for already-loaded import", path=resolved_path)
            return import_context.config_cache.get(resolved_path)

    # Add to import stack and visited files (use both original and normalized for tracking)
    import_context.import_stack.append(resolved_path)
    import_context.visited_files.add(normalized_path)

    try:
        # Load the imported config
        # Check if it's a remote URI
        if _is_remote_uri(resolved_path):
            # For remote URIs, we need to use the remote loader
            try:
                from duckalog.remote_config import load_config_from_uri

                imported_config = load_config_from_uri(
                    uri=resolved_path,
                    load_sql_files=load_sql_files,
                    sql_file_loader=sql_file_loader,
                    resolve_paths=False,
                    filesystem=filesystem,
                )
            except Exception as exc:
                raise ImportValidationError(
                    f"Failed to load remote config '{resolved_path}': {exc}",
                    import_path=resolved_path,
                    cause=exc,
                ) from exc
        else:
            # Local file loading
            config_path = Path(resolved_path)
            if not config_path.exists():
                raise ImportFileNotFoundError(
                    f"Imported file not found: {resolved_path}",
                    import_path=resolved_path,
                )

            try:
                if filesystem is not None:
                    if not hasattr(filesystem, "open") or not hasattr(filesystem, "exists"):
                        raise ImportError(
                            "filesystem object must provide 'open' and 'exists' methods"
                        )
                    if not filesystem.exists(resolved_path):
                        raise ImportFileNotFoundError(
                            f"Imported file not found: {resolved_path}",
                            import_path=resolved_path,
                        )
                    with filesystem.open(resolved_path, "r") as f:
                        raw_text = f.read()
                else:
                    raw_text = config_path.read_text()
            except OSError as exc:
                raise ImportValidationError(
                    f"Failed to read imported file '{resolved_path}': {exc}",
                    import_path=resolved_path,
                    cause=exc,
                ) from exc

            suffix = config_path.suffix.lower()
            if suffix in {".yaml", ".yml"}:
                parsed = yaml.safe_load(raw_text)
            elif suffix == ".json":
                parsed = json.loads(raw_text)
            else:
                raise ImportValidationError(
                    f"Imported file must use .yaml, .yml, or .json extension: {resolved_path}",
                    import_path=resolved_path,
                )

            if parsed is None:
                raise ImportValidationError(
                    f"Imported file is empty: {resolved_path}",
                    import_path=resolved_path,
                )
            if not isinstance(parsed, dict):
                raise ImportValidationError(
                    f"Imported file must define a mapping at the top level: {resolved_path}",
                    import_path=resolved_path,
                )

            # Apply environment variable interpolation
            interpolated = _interpolate_env(parsed)

            # Validate the imported config
            from .models import Config

            try:
                imported_config = Config.model_validate(interpolated)
            except Exception as exc:
                raise ImportValidationError(
                    f"Imported config validation failed: {exc}",
                    import_path=resolved_path,
                    cause=exc,
                ) from exc

            # Load SQL files if requested
            if load_sql_files:
                imported_config = _load_sql_files_from_config(
                    imported_config, config_path, sql_file_loader
                )

        # Cache the imported config using both the resolved path and normalized path
        # for consistency in lookup
        import_context.config_cache[resolved_path] = imported_config
        import_context.config_cache[normalized_path] = imported_config

        # Recursively process imports in the imported config
        if imported_config.imports:
            log_debug(
                "Processing nested imports",
                path=resolved_path,
                import_count=len(imported_config.imports),
            )
            for nested_import_path in imported_config.imports:
                nested_config = _resolve_and_load_import(
                    import_path=nested_import_path,
                    base_path=resolved_path,
                    filesystem=filesystem,
                    resolve_paths=resolve_paths,
                    load_sql_files=load_sql_files,
                    sql_file_loader=sql_file_loader,
                    import_context=import_context,
                )
                # Merge the nested import into the imported config
                # Main config should override imported config, so import goes first
                imported_config = _deep_merge_config(nested_config, imported_config)

        return imported_config

    finally:
        # Remove from import stack (use the original path, not normalized)
        import_context.import_stack.pop()


def _load_config_with_imports(
    file_path: str,
    content: Optional[str] = None,
    format: str = "yaml",
    filesystem: Optional[Any] = None,
    resolve_paths: bool = True,
    load_sql_files: bool = True,
    sql_file_loader: Optional[Any] = None,
    import_context: Optional[ImportContext] = None,
) -> Any:
    """Load config with import support.

    Args:
        file_path: Path to the config file.
        content: Optional file content (if not provided, will read from file_path).
        format: File format (yaml or json).
        filesystem: Optional filesystem object.
        resolve_paths: Whether to resolve relative paths.
        load_sql_files: Whether to load SQL files.
        sql_file_loader: Optional SQLFileLoader instance.
        import_context: Optional existing import context.

    Returns:
        A validated and merged Config object.

    Raises:
        ConfigError: If the config cannot be loaded or validated.
    """
    if import_context is None:
        import_context = ImportContext()

    config_path = Path(file_path)
    resolved_path = str(config_path.resolve())

    log_debug("Loading config with imports", path=resolved_path)

    # Normalize the path for consistent tracking
    normalized_path = _normalize_uri(resolved_path)

    # Check if config is already in cache (check both original and normalized)
    if resolved_path in import_context.config_cache:
        log_debug("Using cached config", path=resolved_path)
        return import_context.config_cache[resolved_path]
    if normalized_path in import_context.config_cache:
        log_debug("Using cached config (via normalized path)", path=resolved_path)
        return import_context.config_cache[normalized_path]

    # Add to visited files (use normalized for remote URIs, original for local)
    import_context.visited_files.add(normalized_path)
    import_context.import_stack.append(resolved_path)

    try:
        # Load the base config
        if content is not None:
            raw_text = content
        else:
            if filesystem is not None:
                if not hasattr(filesystem, "open") or not hasattr(filesystem, "exists"):
                    raise ConfigError(
                        "filesystem object must provide 'open' and 'exists' methods"
                    )
                if not filesystem.exists(resolved_path):
                    raise ConfigError(f"Config file not found: {file_path}")
                with filesystem.open(resolved_path, "r") as f:
                    raw_text = f.read()
            else:
                if not config_path.exists():
                    raise ConfigError(f"Config file not found: {file_path}")
                raw_text = config_path.read_text()

        # Parse the content
        if format == "yaml":
            parsed = yaml.safe_load(raw_text)
        elif format == "json":
            parsed = json.loads(raw_text)
        else:
            raise ConfigError("Config files must use .yaml, .yml, or .json extensions")

        if parsed is None:
            raise ConfigError("Config file is empty")
        if not isinstance(parsed, dict):
            raise ConfigError("Config file must define a mapping at the top level")

        # Apply environment variable interpolation
        interpolated = _interpolate_env(parsed)

        # Validate the base config
        from .models import Config

        try:
            config = Config.model_validate(interpolated)
        except Exception as exc:
            log_debug("Validation failed interpolated keys", keys=list(interpolated.keys()))
            if 'views' in interpolated:
                log_debug("views value", views=interpolated['views'])
            else:
                log_debug("views missing from interpolated dict")
            raise ConfigError(f"Configuration validation failed: {exc}") from exc

        # Cache the base config using both original and normalized paths
        import_context.config_cache[resolved_path] = config
        import_context.config_cache[normalized_path] = config

        # Process imports
        if config.imports:
            # Handle both list and SelectiveImports formats
            if isinstance(config.imports, list):
                import_count = len(config.imports)
            else:
                # SelectiveImports - count total imports across all sections
                import_count = sum(
                    len(field_value) if field_value else 0
                    for field_value in config.imports
                    if field_value is not None
                )
            log_debug("Processing imports", import_count=import_count)

            # Normalize imports to handle both simple list and SelectiveImports formats
            normalized_imports = _normalize_imports_for_processing(
                config.imports,
                base_path=resolved_path,
                filesystem=filesystem,
            )

            # Group imports by section for selective merging
            global_imports = []
            section_imports = {}

            for path, override, section in normalized_imports:
                if section is None:
                    # Global import
                    global_imports.append((path, override))
                else:
                    # Section-specific import
                    if section not in section_imports:
                        section_imports[section] = []
                    section_imports[section].append((path, override))

            # Process global imports first (backward compatible behavior)
            for import_path, override in global_imports:
                # Expand glob patterns
                expanded_paths = _expand_glob_patterns(
                    [import_path],
                    base_path=resolved_path,
                    filesystem=filesystem,
                )

                for expanded_path in expanded_paths:
                    imported_config = _resolve_and_load_import(
                        import_path=expanded_path,
                        base_path=resolved_path,
                        filesystem=filesystem,
                        resolve_paths=resolve_paths,
                        load_sql_files=load_sql_files,
                        sql_file_loader=sql_file_loader,
                        import_context=import_context,
                    )
                    # Merge the imported config into the base config
                    # When override=True: imported values override main config (normal behavior)
                    # When override=False: main config values are preserved, only missing fields filled
                    config = _merge_config_with_override(config, imported_config, override_mode=override)

            # Process section-specific imports
            for section_name, imports_list in section_imports.items():
                for import_path, override in imports_list:
                    # Expand glob patterns
                    expanded_paths = _expand_glob_patterns(
                        [import_path],
                        base_path=resolved_path,
                        filesystem=filesystem,
                    )

                    for expanded_path in expanded_paths:
                        imported_config = _resolve_and_load_import(
                            import_path=expanded_path,
                            base_path=resolved_path,
                            filesystem=filesystem,
                            resolve_paths=resolve_paths,
                            load_sql_files=load_sql_files,
                            sql_file_loader=sql_file_loader,
                            import_context=import_context,
                        )

                        # Merge only the specified section
                        config = _merge_section_specific(
                            imported_config,
                            config,
                            section_name,
                            override_mode=override,
                        )

        # Validate merged config
        _validate_unique_names(config, import_context)

        # Load SQL files if requested (after all merges are complete)
        if load_sql_files:
            config = _load_sql_files_from_config(config, config_path, sql_file_loader)

        log_debug("Config loaded with imports", path=resolved_path, views=len(config.views))
        return config

    finally:
        # Remove from import stack
        import_context.import_stack.pop()
