"""Remote configuration loading utilities for Duckalog.

This module provides functionality to load Duckalog configuration files from
remote storage systems using fsspec, supporting schemes like S3, GCS,
Azure Blob Storage, SFTP, and HTTPS.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .config import Config
from .errors import ConfigError, DuckalogError, RemoteConfigError
from .logging_utils import log_debug, log_info

# Optional imports for remote functionality
try:
    import fsspec
    from fsspec.registry import known_implementations

    FSSPEC_AVAILABLE = True
except ImportError:
    fsspec = None  # type: ignore
    known_implementations = {}  # type: ignore
    FSSPEC_AVAILABLE = False

try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    requests = None  # type: ignore
    REQUESTS_AVAILABLE = False


# Supported URI schemes and their required dependencies
SCHEME_REQUIREMENTS = {
    "s3": {"fsspec": True, "extra": "s3"},
    "s3a": {"fsspec": True, "extra": "s3"},
    "gcs": {"fsspec": True, "extra": "gcs"},
    "gs": {"fsspec": True, "extra": "gcs"},
    "abfs": {"fsspec": True, "extra": "azure"},
    "adl": {"fsspec": True, "extra": "azure"},
    "az": {"fsspec": True, "extra": "azure"},
    "sftp": {"fsspec": True, "extra": "sftp"},
    "ssh": {"fsspec": True, "extra": "sftp"},
    "https": {"fsspec": False, "extra": None},
    "http": {"fsspec": False, "extra": None},
}

# Auth resolution order per backend (following provider defaults)
AUTH_GUIDANCE = {
    "s3": "AWS credentials via environment variables, ~/.aws/credentials, or IAM role",
    "gcs": "Google Cloud credentials via GOOGLE_APPLICATION_CREDENTIALS or ADC",
    "gs": "Google Cloud credentials via GOOGLE_APPLICATION_CREDENTIALS or ADC",
    "abfs": "Azure credentials via environment variables or managed identity",
    "adl": "Azure credentials via environment variables or managed identity",
    "az": "Azure credentials via environment variables or managed identity",
    "sftp": "SFTP credentials via SSH config or environment variables",
    "ssh": "SSH credentials via SSH config or environment variables",
    "https": "No authentication required for public URLs",
    "http": "No authentication required for public URLs",
}


def is_remote_uri(uri: str) -> bool:
    """Check if a URI is a remote URI that should be handled by remote loading.

    Args:
        uri: The URI to check

    Returns:
        True if the URI is a remote URI, False otherwise
    """
    if not uri:
        return False

    parsed = urlparse(uri)
    return parsed.scheme in SCHEME_REQUIREMENTS


def validate_filesystem(filesystem: Any) -> None:
    """Validate that a filesystem object is properly configured.

    Args:
        filesystem: The filesystem object to validate

    Raises:
        RemoteConfigError: If the filesystem is invalid
    """
    if filesystem is None:
        return

    # Check if filesystem has the required methods
    if not hasattr(filesystem, "open"):
        raise RemoteConfigError(
            "Invalid filesystem: missing 'open' method. "
            "Expected fsspec-compatible filesystem object."
        )

    # Basic type check - should be fsspec compatible
    try:
        # Try to get the protocol to validate it's a proper filesystem
        if hasattr(filesystem, "protocol"):
            # Most fsspec filesystems have a protocol attribute
            protocol = getattr(filesystem, "protocol", None)
            if not protocol:
                raise RemoteConfigError("Filesystem missing protocol attribute")
    except Exception:
        # If we can't access the protocol, that's ok - the filesystem
        # might be valid but not expose this attribute
        pass


def validate_remote_uri(uri: str, filesystem: Any | None = None) -> None:
    """Validate that a remote URI is supported and dependencies are available.

    Args:
        uri: The remote URI to validate
        filesystem: Optional filesystem object to validate

    Raises:
        RemoteConfigError: If the URI scheme is unsupported or dependencies are missing
    """
    parsed = urlparse(uri)
    scheme = parsed.scheme.lower()

    if scheme not in SCHEME_REQUIREMENTS:
        raise RemoteConfigError(
            f"Unsupported URI scheme '{scheme}'. "
            f"Supported schemes are: {', '.join(sorted(SCHEME_REQUIREMENTS.keys()))}"
        )

    requirements = SCHEME_REQUIREMENTS[scheme]

    if requirements["fsspec"] and not FSSPEC_AVAILABLE:
        raise RemoteConfigError(
            f"fsspec is required for '{scheme}://' URIs. "
            f"Install with: pip install duckalog[remote]"
        )

    # Check for specific backend implementations
    if (
        requirements["fsspec"]
        and fsspec is not None
        and known_implementations is not None
    ):
        protocol = scheme
        if scheme in ["s3", "s3a"]:
            protocol = "s3"
        elif scheme in ["gcs", "gs"]:
            protocol = "gcs"
        elif scheme in ["abfs", "adl", "az"]:
            protocol = "abfs"
        elif scheme in ["sftp", "ssh"]:
            protocol = "sftp"

        if protocol not in known_implementations:
            extra_name = requirements["extra"]
            if extra_name:
                raise RemoteConfigError(
                    f"fsspec backend for '{scheme}://' is not available. "
                    f"Install with: pip install duckalog[remote-{extra_name}]"
                )
            else:
                raise RemoteConfigError(
                    f"fsspec backend for '{scheme}://' is not available. "
                    f"Install fsspec with appropriate backend support."
                )

    # For HTTP/HTTPS, check requests availability
    if scheme in ["http", "https"] and not REQUESTS_AVAILABLE:
        raise RemoteConfigError(
            f"requests is required for '{scheme}://' URIs. "
            f"Install with: pip install duckalog[remote]"
        )


def fetch_remote_content(
    uri: str, timeout: int = 30, filesystem: Any | None = None
) -> str:
    """Fetch content from a remote URI.

    Args:
        uri: The remote URI to fetch from
        timeout: Timeout in seconds for the fetch operation
        filesystem: Optional fsspec filesystem object to use. If provided,
                   this filesystem will be used instead of creating a new one.
                   Useful for custom authentication or advanced use cases.

    Returns:
        The content as a string

    Raises:
        RemoteConfigError: If the fetch fails
    """
    validate_remote_uri(uri, filesystem)

    # Validate the filesystem if provided
    validate_filesystem(filesystem)

    parsed = urlparse(uri)
    scheme = parsed.scheme.lower()

    log_info("Fetching remote config", uri=uri, scheme=scheme)

    try:
        if scheme in ["http", "https"]:
            return _fetch_http_content(uri, timeout)
        else:
            return _fetch_fsspec_content(uri, timeout, filesystem)
    except Exception as exc:
        auth_hint = AUTH_GUIDANCE.get(scheme, "")
        if auth_hint:
            auth_hint = f" Authentication hint: {auth_hint}"

        raise RemoteConfigError(
            f"Failed to fetch config from '{uri}': {exc}{auth_hint}"
        ) from exc


def _fetch_http_content(uri: str, timeout: int) -> str:
    """Fetch content using requests for HTTP/HTTPS URIs."""
    if not REQUESTS_AVAILABLE:
        raise RemoteConfigError("requests library is not available")

    response = requests.get(uri, timeout=timeout)
    response.raise_for_status()

    content = response.text
    log_debug("HTTP fetch completed", uri=uri, content_length=len(content))
    return content


def _fetch_fsspec_content(uri: str, timeout: int, filesystem: Any | None = None) -> str:
    """Fetch content using fsspec for other remote URIs."""
    if not FSSPEC_AVAILABLE or fsspec is None:
        raise RemoteConfigError("fsspec library is not available")

    # Use provided filesystem or create a new one
    if filesystem is not None:
        # Use the provided filesystem
        fs = filesystem
        fs_options = {}
    else:
        # Create filesystem from URI with timeout
        fs_options = {"timeout": timeout}
        fs = None

    # For some backends, we might need additional options
    parsed = urlparse(uri)
    scheme = parsed.scheme.lower()

    # Add scheme-specific options if needed (only when creating new filesystem)
    if filesystem is None:
        if scheme in ["s3", "s3a"]:
            # S3-specific options can be added here if needed
            pass
        elif scheme in ["gcs", "gs"]:
            # GCS-specific options can be added here if needed
            pass
        elif scheme in ["abfs", "adl", "az"]:
            # Azure-specific options can be added here if needed
            pass
        elif scheme in ["sftp", "ssh"]:
            # SFTP-specific options can be added here if needed
            pass

    if filesystem is not None:
        # Use provided filesystem
        with fs.open(uri, "r") as f:
            content = f.read()
    else:
        # Use fsspec.open with timeout
        with fsspec.open(uri, "r", **fs_options) as f:
            content = f.read()

    log_debug("fsspec fetch completed", uri=uri, content_length=len(content))
    return content


def load_config_from_uri(
    uri: str,
    load_sql_files: bool = True,
    sql_file_loader: Any | None = None,
    resolve_paths: bool = False,  # Default to False for remote configs
    timeout: int = 30,
    filesystem: Any | None = None,
) -> Config:
    """Load a Duckalog configuration from a remote URI.

    This function fetches configuration content from remote storage systems
    and processes it using the same validation and interpolation logic as
    local configuration files.

    Args:
        uri: Remote URI pointing to the configuration file
        load_sql_files: Whether to load and process SQL from external files.
                       If False, SQL file references are left as-is for later processing.
        sql_file_loader: Optional SQLFileLoader instance for loading SQL files.
                        If None, a default loader will be created.
        resolve_paths: Whether to resolve relative paths to absolute paths.
                      For remote configs, this defaults to False since relative
                      paths may not make sense in remote contexts.
        timeout: Timeout in seconds for the remote fetch operation
        filesystem: Optional fsspec filesystem object to use for remote operations.
                   If provided, this filesystem will be used instead of creating
                   a new one based on the URI scheme. Useful for custom
                   authentication or advanced use cases.

    Returns:
        A validated Config object

    Raises:
        RemoteConfigError: If remote fetching or config processing fails

    Example:
        Load a catalog from S3 with environment variables::

            from duckalog.remote import load_config_from_uri

            config = load_config_from_uri("s3://my-bucket/configs/catalog.yaml")
            print(len(config.views))

        Load a catalog with custom S3 filesystem::

            import fsspec
            fs = fsspec.filesystem("s3",
                key="AKIAIOSFODNN7EXAMPLE",
                secret="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
            )
            config = load_config_from_uri(
                "s3://my-bucket/configs/catalog.yaml",
                filesystem=fs
            )

        Load a catalog from GitHub with token::

            fs = fsspec.filesystem("github", token="ghp_xxxxxxxxxxxxxxxxxxxx")
            config = load_config_from_uri(
                "github://user/repo/catalog.yaml",
                filesystem=fs
            )

        Load a catalog from Azure with connection string::

            fs = fsspec.filesystem("abfs",
                connection_string="DefaultEndpointsProtocol=https;AccountName=account;AccountKey=key"
            )
            config = load_config_from_uri(
                "abfs://account@container/catalog.yaml",
                filesystem=fs
            )

        Load a catalog from HTTPS (no authentication needed)::

            config = load_config_from_uri(
                "https://raw.githubusercontent.com/user/repo/main/catalog.yaml"
            )
    """
    if not is_remote_uri(uri):
        raise RemoteConfigError(f"URI '{uri}' is not a recognized remote URI")

    # Fetch the remote content
    content = fetch_remote_content(uri, timeout, filesystem=filesystem)

    # For remote configs, we need to handle the content differently
    # since we can't use Path operations directly
    log_info("Processing remote config", uri=uri)

    # Parse the content based on the URI extension
    parsed_uri = urlparse(uri)
    path = Path(parsed_uri.path)
    suffix = path.suffix.lower()

    if suffix in {".yaml", ".yml"}:
        import yaml

        try:
            parsed_config = yaml.safe_load(content)
        except yaml.YAMLError as exc:
            raise RemoteConfigError(f"Invalid YAML in remote config: {exc}") from exc
    elif suffix == ".json":
        import json

        try:
            parsed_config = json.loads(content)
        except json.JSONDecodeError as exc:
            raise RemoteConfigError(f"Invalid JSON in remote config: {exc}") from exc
    else:
        raise RemoteConfigError(
            "Remote config files must use .yaml, .yml, or .json extensions"
        )

    if parsed_config is None:
        raise RemoteConfigError("Remote config file is empty")
    if not isinstance(parsed_config, dict):
        raise RemoteConfigError(
            "Remote config file must define a mapping at the top level"
        )

    # Process the configuration using the same logic as local configs
    # but adapted for remote content
    from duckalog.config.interpolation import _interpolate_env

    log_debug("Remote config keys", keys=list(parsed_config.keys()))
    interpolated = _interpolate_env(parsed_config)

    try:
        config = Config.model_validate(interpolated)
    except Exception as exc:
        raise RemoteConfigError(f"Remote config validation failed: {exc}") from exc

    # For remote configs, path resolution is disabled by default
    # but can be enabled if explicitly requested
    if resolve_paths:
        # For remote configs, we can't resolve relative paths meaningfully
        # so we skip path resolution
        log_debug("Path resolution skipped for remote config", uri=uri)

    # Load SQL from external files if requested
    if load_sql_files:
        config = _load_sql_files_from_remote_config(
            config, uri, sql_file_loader, filesystem
        )

    log_info("Remote config loaded", uri=uri, views=len(config.views))
    return config


def _load_sql_files_from_remote_config(
    config: Config,
    config_uri: str,
    sql_file_loader: Any | None = None,
    filesystem: Any | None = None,
) -> Config:
    """Load SQL content from external files referenced in a remote config.

    This handles SQL file references that might be relative to the remote
    config location or might themselves be remote URIs.
    """
    # Import here to avoid circular import
    from .sql_file_loader import SQLFileError, SQLFileLoader

    if sql_file_loader is None:
        sql_file_loader = SQLFileLoader()

    # Get the base directory for resolving relative paths
    parsed_uri = urlparse(config_uri)
    base_path = Path(parsed_uri.path).parent

    # Check if any views have SQL file references
    has_sql_files = any(
        view.sql_file is not None or view.sql_template is not None
        for view in config.views
    )

    if not has_sql_files:
        # No SQL files to process
        return config

    log_info("Loading SQL files from remote config", uri=config_uri)

    updated_views = []
    for view in config.views:
        if view.sql_file is not None:
            # Handle direct SQL file reference
            file_path = view.sql_file.path

            # Check if the SQL file path is a remote URI
            if is_remote_uri(file_path):
                # Load from remote URI
                try:
                    sql_content = fetch_remote_content(file_path, filesystem=filesystem)

                    # Process as template if needed
                    if view.sql_file.as_template:
                        sql_content = sql_file_loader._process_template(
                            sql_content, view.sql_file.variables or {}, file_path
                        )
                except Exception as exc:
                    raise RemoteConfigError(
                        f"Failed to load remote SQL file for view '{view.name}': {exc}"
                    ) from exc
            else:
                # Load as local file (relative to remote config location)
                try:
                    # For remote configs, we construct a fake config file path
                    # for relative resolution
                    fake_config_path = str(base_path / "config.yaml")
                    sql_content = sql_file_loader.load_sql_file(
                        file_path=file_path,
                        config_file_path=fake_config_path,
                        variables=view.sql_file.variables,
                        as_template=view.sql_file.as_template,
                    )
                except SQLFileError as exc:
                    raise RemoteConfigError(
                        f"Failed to load SQL file for view '{view.name}': {exc}"
                    ) from exc

            # Create new view with inline SQL
            updated_view = view.model_copy(
                update={"sql": sql_content, "sql_file": None}
            )
            updated_views.append(updated_view)

        elif view.sql_template is not None:
            # Handle SQL template reference
            file_path = view.sql_template.path

            # Check if the SQL template path is a remote URI
            if is_remote_uri(file_path):
                try:
                    sql_content = fetch_remote_content(file_path, filesystem=filesystem)
                    # Process template variables
                    sql_content = sql_file_loader._process_template(
                        sql_content, view.sql_template.variables or {}, file_path
                    )
                except Exception as exc:
                    raise RemoteConfigError(
                        f"Failed to load remote SQL template for view '{view.name}': {exc}"
                    ) from exc
            else:
                try:
                    fake_config_path = str(base_path / "config.yaml")
                    sql_content = sql_file_loader.load_sql_file(
                        file_path=file_path,
                        config_file_path=fake_config_path,
                        variables=view.sql_template.variables,
                        as_template=True,  # Templates are always processed as templates
                    )
                except SQLFileError as exc:
                    raise RemoteConfigError(
                        f"Failed to load SQL template for view '{view.name}': {exc}"
                    ) from exc

            # Create new view with inline SQL
            updated_view = view.model_copy(
                update={"sql": sql_content, "sql_template": None}
            )
            updated_views.append(updated_view)

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
        "SQL files loaded from remote config",
        uri=config_uri,
        total_views=len(config.views),
        file_based_views=file_based_views,
    )

    return updated_config


__all__ = [
    "RemoteConfigError",
    "is_remote_uri",
    "load_config_from_uri",
    "fetch_remote_content",
    "validate_remote_uri",
]
