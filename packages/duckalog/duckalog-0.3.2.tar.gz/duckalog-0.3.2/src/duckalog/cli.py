"""Typer-based CLI for Duckalog."""

from __future__ import annotations

# mypy: disable-error-code=assignment
import sys
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as pkg_version
from pathlib import Path
from typing import Any, Optional

from loguru import logger

import typer

# Import fsspec at module level for easier testing
try:
    import fsspec
except ImportError:
    fsspec = None  # Will be handled in the function

from .config import load_config, validate_file_accessibility

# from .dashboard import create_app
# from .dashboard.state import DashboardContext
from .config_init import create_config_template, validate_generated_config
from .engine import build_catalog
from .errors import ConfigError, EngineError
from .config import log_error, log_info
from .sql_generation import generate_all_views_sql

app = typer.Typer(help="Duckalog CLI for building and inspecting DuckDB catalogs.")


def _create_filesystem_from_options(
    protocol: Optional[str] = None,
    key: Optional[str] = None,
    secret: Optional[str] = None,
    token: Optional[str] = None,
    anon: bool = False,
    timeout: Optional[int] = 30,
    aws_profile: Optional[str] = None,
    gcs_credentials_file: Optional[str] = None,
    azure_connection_string: Optional[str] = None,
    sftp_host: Optional[str] = None,
    sftp_port: int = 22,
    sftp_key_file: Optional[str] = None,
):
    """Create a fsspec filesystem from CLI options.

    Returns None if no filesystem options are provided.

    Args:
        protocol: Filesystem protocol (s3, gcs, abfs, sftp, github)
        key: API key or access key
        secret: Secret key or password
        token: Authentication token
        anon: Use anonymous access
        timeout: Connection timeout
        aws_profile: AWS profile name
        gcs_credentials_file: Path to GCS credentials file
        azure_connection_string: Azure connection string
        sftp_host: SFTP server hostname
        sftp_port: SFTP server port
        sftp_key_file: Path to SFTP private key file

    Returns:
        fsspec filesystem object or None

    Raises:
        typer.Exit: If filesystem creation fails
    """
    # If no filesystem options provided, return None
    if not any(
        [
            protocol,
            key,
            secret,
            token,
            anon,
            aws_profile,
            gcs_credentials_file,
            azure_connection_string,
            sftp_host,
            sftp_key_file,
        ]
    ):
        return None

    # Check if fsspec is available
    if fsspec is None:
        typer.echo(
            "fsspec is required for filesystem options. Install with: pip install duckalog[remote]",
            err=True,
        )
        raise typer.Exit(4)

    # Validate protocol if provided or try to infer from other options
    if not protocol:
        # Try to infer protocol from provided options
        if aws_profile or (key and secret):
            protocol = "s3"
        elif gcs_credentials_file:
            protocol = "gcs"
        elif azure_connection_string or (key and secret):
            protocol = "abfs"
        elif sftp_host or sftp_key_file:
            protocol = "sftp"
        elif token:
            protocol = "github"
        else:
            typer.echo(
                "Protocol must be specified or inferable from provided options.",
                err=True,
            )
            raise typer.Exit(4)

    # Validate required options for specific protocols
    if protocol in ["s3"] and not any([aws_profile, key, secret, anon]):
        typer.echo(
            "For S3 protocol, provide either --aws-profile, --fs-key/--fs-secret, or use --fs-anon",
            err=True,
        )
        raise typer.Exit(4)

    if protocol in ["abfs", "adl", "az"] and not any(
        [azure_connection_string, key, secret]
    ):
        typer.echo(
            "For Azure protocol, provide either --azure-connection-string or --fs-key/--fs-secret",
            err=True,
        )
        raise typer.Exit(4)

    if protocol == "sftp" and not sftp_host:
        typer.echo(
            "SFTP protocol requires --sftp-host to be specified",
            err=True,
        )
        raise typer.Exit(4)

    # Validate mutual exclusivity
    if aws_profile and key:
        typer.echo(
            "Cannot specify both --aws-profile and --fs-key",
            err=True,
        )
        raise typer.Exit(4)

    if azure_connection_string and key:
        typer.echo(
            "Cannot specify both --azure-connection-string and --fs-key",
            err=True,
        )
        raise typer.Exit(4)

    # Validate file paths exist if provided
    if gcs_credentials_file and not Path(gcs_credentials_file).exists():
        typer.echo(
            f"GCS credentials file not found: {gcs_credentials_file}",
            err=True,
        )
        raise typer.Exit(4)

    if sftp_key_file and not Path(sftp_key_file).exists():
        typer.echo(
            f"SFTP key file not found: {sftp_key_file}",
            err=True,
        )
        raise typer.Exit(4)

    # Determine protocol from URI or explicit parameter
    filesystem_options = {}

    # Add timeout if specified
    if timeout:
        filesystem_options["timeout"] = timeout

    # Handle different protocols
    if protocol == "s3" or aws_profile:
        if aws_profile:
            filesystem_options["profile"] = aws_profile
        elif key and secret:
            filesystem_options.update(
                {
                    "key": key,
                    "secret": secret,
                    "anon": anon or False,
                }
            )
            # Add region if needed
            filesystem_options["client_kwargs"] = {}
        else:
            # Use default AWS credential resolution
            pass

    elif protocol == "gcs":
        if gcs_credentials_file:
            filesystem_options["token"] = gcs_credentials_file
        # Otherwise use default ADC

    elif protocol in ["abfs", "adl", "az"]:
        if azure_connection_string:
            filesystem_options["connection_string"] = azure_connection_string
        elif key and secret:
            # Handle Azure account key auth
            filesystem_options.update(
                {
                    "account_name": key,
                    "account_key": secret,
                }
            )

    elif protocol == "sftp":
        filesystem_options.update(
            {
                "host": sftp_host,
                "port": sftp_port,
            }
        )
        if sftp_key_file:
            filesystem_options["key_filename"] = sftp_key_file
        elif secret:  # Use password if key file not provided
            filesystem_options["password"] = secret
        elif key:  # Use key as username
            filesystem_options["username"] = key

    elif protocol == "github":
        if token:
            filesystem_options["token"] = token
        elif key:
            filesystem_options["username"] = key
            if secret:
                filesystem_options["password"] = secret

    elif protocol == "https" or protocol == "http":
        # HTTP/HTTPS doesn't need special filesystem creation
        # Just return None to use built-in requests
        return None

    try:
        return fsspec.filesystem(protocol, **filesystem_options)
    except Exception as exc:
        typer.echo(
            f"Failed to create filesystem for protocol '{protocol}': {exc}",
            err=True,
        )
        raise typer.Exit(4)


def _configure_logging(verbose: bool) -> None:
    """Configure global logging settings for CLI commands.

    Args:
        verbose: When ``True``, set the log level to ``INFO``; otherwise use
            ``WARNING``.
    """
    # Remove default handler to avoid duplicate output
    logger.remove()

    # Add a new handler with appropriate level and format
    level = "INFO" if verbose else "WARNING"
    logger.add(
        sys.stderr,
        level=level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | {message}"
    )


# Shared callback for filesystem options across all commands
@app.callback()
def main_callback(
    ctx: typer.Context,
    fs_protocol: Optional[str] = typer.Option(
        None,
        "--fs-protocol",
        help="Remote filesystem protocol: s3 (AWS), gcs (Google), abfs (Azure), sftp, github. Protocol can be inferred from other options.",
    ),
    fs_key: Optional[str] = typer.Option(
        None,
        "--fs-key",
        help="API key, access key, or username for authentication (protocol-specific)",
    ),
    fs_secret: Optional[str] = typer.Option(
        None,
        "--fs-secret",
        help="Secret key, password, or token for authentication (protocol-specific)",
    ),
    fs_token: Optional[str] = typer.Option(
        None,
        "--fs-token",
        help="Authentication token for services like GitHub personal access tokens",
    ),
    fs_anon: bool = typer.Option(
        False,
        "--fs-anon",
        help="Use anonymous access (no authentication required). Useful for public S3 buckets.",
    ),
    fs_timeout: Optional[int] = typer.Option(
        None, "--fs-timeout", help="Connection timeout in seconds (default: 30)"
    ),
    aws_profile: Optional[str] = typer.Option(
        None,
        "--aws-profile",
        help="AWS profile name for S3 authentication (overrides --fs-key/--fs-secret)",
    ),
    gcs_credentials_file: Optional[str] = typer.Option(
        None,
        "--gcs-credentials-file",
        help="Path to Google Cloud service account credentials JSON file",
    ),
    azure_connection_string: Optional[str] = typer.Option(
        None,
        "--azure-connection-string",
        help="Azure storage connection string (overrides --fs-key/--fs-secret for Azure)",
    ),
    sftp_host: Optional[str] = typer.Option(
        None, "--sftp-host", help="SFTP server hostname (required for SFTP protocol)"
    ),
    sftp_port: int = typer.Option(
        22, "--sftp-port", help="SFTP server port (default: 22)"
    ),
    sftp_key_file: Optional[str] = typer.Option(
        None,
        "--sftp-key-file",
        help="Path to SSH private key file for SFTP authentication",
    ),
) -> None:
    """Shared callback that creates filesystem objects from CLI options.

    This callback applies to all commands and creates a filesystem object
    from the provided options, storing it in ctx.obj["filesystem"].
    """
    if ctx.resilient_parsing:
        return

    # Initialize context object if needed
    if ctx.obj is None:
        ctx.obj = {}

    # Create filesystem object using existing helper
    filesystem = _create_filesystem_from_options(
        protocol=fs_protocol,
        key=fs_key,
        secret=fs_secret,
        token=fs_token,
        anon=fs_anon,
        timeout=fs_timeout,
        aws_profile=aws_profile,
        gcs_credentials_file=gcs_credentials_file,
        azure_connection_string=azure_connection_string,
        sftp_host=sftp_host,
        sftp_port=sftp_port,
        sftp_key_file=sftp_key_file,
    )

    # Store filesystem in context for command access
    ctx.obj["filesystem"] = filesystem


@app.command(name="version", help="Show duckalog version.")
def version_command() -> None:
    """Show the installed duckalog package version."""

    try:
        current_version = pkg_version("duckalog")
    except PackageNotFoundError:
        current_version = "unknown"
    typer.echo(f"duckalog {current_version}")


@app.command(help="Build or update a DuckDB catalog from a config file or remote URI.")
def build(
    ctx: typer.Context,
    config_path: str = typer.Argument(
        ...,
        help="Path to configuration file or remote URI (e.g., s3://bucket/config.yaml)",
    ),
    db_path: Optional[str] = typer.Option(
        None,
        "--db-path",
        help="Override DuckDB database path. Supports local paths and remote URIs (s3://, gs://, gcs://, abfs://, adl://, sftp://).",
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Generate SQL without executing against DuckDB."
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose logging output."
    ),
) -> None:
    """CLI entry point for the ``build`` command.

    This command loads a configuration file and applies it to a DuckDB
    catalog, or prints the generated SQL when ``--dry-run`` is used.

    Examples:
        # Local configuration file
        duckalog build config.yaml

        # S3 with access key and secret
        duckalog build s3://my-bucket/config.yaml --fs-key AKIA... --fs-secret wJalr...

        # S3 with AWS profile
        duckalog build s3://my-bucket/config.yaml --aws-profile my-profile

        # GitHub with personal access token
        duckalog build github://user/repo/config.yaml --fs-token ghp_xxxxxxxxxxxx

        # Azure with connection string
        duckalog build abfs://account@container/config.yaml --azure-connection-string "..."

        # SFTP with key authentication
        duckalog build sftp://server/config.yaml --sftp-host server.com --sftp-key-file ~/.ssh/id_rsa

        # Anonymous S3 access (public bucket)
        duckalog build s3://public-bucket/config.yaml --fs-anon

        # Export catalog to remote storage
        duckalog build config.yaml --db-path s3://my-bucket/catalog.duckdb

        # Export to GCS with service account credentials
        duckalog build config.yaml --db-path gs://my-project-bucket/catalog.duckdb --gcs-credentials-file /path/to/creds.json

        # Export to Azure with connection string
        duckalog build config.yaml --db-path abfs://account@container/catalog.duckdb --azure-connection-string "..."

        # Export to SFTP server
        duckalog build config.yaml --db-path sftp://server/path/catalog.duckdb --sftp-host server.com --sftp-key-file ~/.ssh/id_rsa

    Args:
        config_path: Path to configuration file or remote URI (e.g., s3://bucket/config.yaml).
        db_path: Optional override for the DuckDB database file path. Supports local paths and remote URIs for cloud storage export.
        dry_run: If ``True``, print SQL instead of modifying the database.
        verbose: If ``True``, enable more verbose logging.
    """
    _configure_logging(verbose)

    # Get filesystem from context (created by shared callback)
    filesystem = ctx.obj.get("filesystem")

    # Validate that local files exist, but allow remote URIs
    try:
        from .remote_config import is_remote_uri

        if not is_remote_uri(config_path):
            # This is a local path, check if it exists
            local_path = Path(config_path)
            if not local_path.exists():
                _fail(f"Config file not found: {config_path}", 2)
    except ImportError:
        # Remote functionality not available, treat as local path
        local_path = Path(config_path)
        if not local_path.exists():
            _fail(f"Config file not found: {config_path}", 2)

    log_info(
        "CLI build invoked",
        config_path=config_path,
        db_path=db_path,
        dry_run=dry_run,
        filesystem=filesystem is not None,
    )
    try:
        sql = build_catalog(
            str(config_path),
            db_path=db_path,
            dry_run=dry_run,
            verbose=verbose,
            filesystem=filesystem,
        )
    except ConfigError as exc:
        log_error("Build failed due to config error", error=str(exc))
        _fail(f"Config error: {exc}", 2)
    except EngineError as exc:
        log_error("Build failed due to engine error", error=str(exc))
        _fail(f"Engine error: {exc}", 3)
    except Exception as exc:  # pragma: no cover - unexpected failures
        if verbose:
            raise
        log_error("Build failed unexpectedly", error=str(exc))
        _fail(f"Unexpected error: {exc}", 1)

    if dry_run and sql:
        typer.echo(sql)
    elif not dry_run:
        typer.echo("Catalog build completed.")


@app.command(name="generate-sql", help="Validate config and emit CREATE VIEW SQL only.")
def generate_sql(
    ctx: typer.Context,
    config_path: str = typer.Argument(
        ..., help="Path to configuration file or remote URI"
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Write SQL output to file instead of stdout."
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose logging output."
    ),
) -> None:
    """CLI entry point for ``generate-sql`` command.

    Args:
        config_path: Path to configuration file or remote URI.
        output: Optional output file path. If omitted, SQL is printed to
            standard output.
        verbose: If ``True``, enable more verbose logging.
    """
    _configure_logging(verbose)

    # Get filesystem from context (created by shared callback)
    filesystem = ctx.obj.get("filesystem")

    # Validate that local files exist, but allow remote URIs
    try:
        from .remote_config import is_remote_uri

        if not is_remote_uri(config_path):
            # This is a local path, check if it exists
            local_path = Path(config_path)
            if not local_path.exists():
                _fail(f"Config file not found: {config_path}", 2)
    except ImportError:
        # Remote functionality not available, treat as local path
        local_path = Path(config_path)
        if not local_path.exists():
            _fail(f"Config file not found: {config_path}", 2)

    log_info(
        "CLI generate-sql invoked",
        config_path=config_path,
        output=str(output) if output else "stdout",
        filesystem=filesystem is not None,
    )
    try:
        config = load_config(config_path, filesystem=filesystem)
        sql = generate_all_views_sql(config)
    except ConfigError as exc:
        log_error("Generate-sql failed due to config error", error=str(exc))
        _fail(f"Config error: {exc}", 2)

    if output:
        out_path = Path(output)
        out_path.write_text(sql)
        if verbose:
            typer.echo(f"Wrote SQL to {out_path}")
    else:
        typer.echo(sql)


@app.command(help="Validate a config file and report success or failure.")
def validate(
    ctx: typer.Context,
    config_path: str = typer.Argument(
        ..., help="Path to configuration file or remote URI"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose logging output."
    ),
) -> None:
    """CLI entry point for ``validate`` command.

    Args:
        config_path: Path to configuration file or remote URI.
        verbose: If ``True``, enable more verbose logging.
    """
    _configure_logging(verbose)

    # Get filesystem from context (created by shared callback)
    filesystem = ctx.obj.get("filesystem")

    # Validate that local files exist, but allow remote URIs
    try:
        from .remote_config import is_remote_uri

        if not is_remote_uri(config_path):
            # This is a local path, check if it exists
            local_path = Path(config_path)
            if not local_path.exists():
                _fail(f"Config file not found: {config_path}", 2)
    except ImportError:
        # Remote functionality not available, treat as local path
        local_path = Path(config_path)
        if not local_path.exists():
            _fail(f"Config file not found: {config_path}", 2)

    log_info(
        "CLI validate invoked",
        config_path=config_path,
        filesystem=filesystem is not None,
    )
    try:
        load_config(config_path, filesystem=filesystem)
    except ConfigError as exc:
        log_error("Validate failed due to config error", error=str(exc))
        _fail(f"Config error: {exc}", 2)

    typer.echo("Config is valid.")


@app.command(help="Show resolved paths for a configuration file.")
def show_paths(
    config_path: Path = typer.Argument(
        ..., exists=True, file_okay=True, dir_okay=False
    ),
    check_accessibility: bool = typer.Option(
        False, "--check", "-c", help="Check if files are accessible."
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose logging output."
    ),
) -> None:
    """Show how paths in a configuration are resolved.

    This command displays the original paths from the configuration file
    and their resolved absolute paths.

    Args:
        config_path: Path to the configuration file.
        check_accessibility: If True, check if resolved file paths are accessible.
        verbose: If True, enable more verbose logging.
    """
    _configure_logging(verbose)
    log_info("CLI show-paths invoked", config_path=str(config_path))

    try:
        config = load_config(str(config_path))
    except ConfigError as exc:
        log_error("Show-paths failed due to config error", error=str(exc))
        _fail(f"Config error: {exc}", 2)

    config_dir = config_path.resolve().parent
    typer.echo(f"Configuration: {config_path}")
    typer.echo(f"Config directory: {config_dir}")
    typer.echo("")

    # Show view paths
    typer.echo("View Paths:")
    typer.echo("-" * 80)
    if config.views:
        for view in config.views:
            if view.uri:
                typer.echo(f"{view.name}:")
                typer.echo(f"  Original: {view.uri}")
                # For file-based views, show what would be resolved
                if view.source in ("parquet", "delta"):
                    from .config import is_relative_path, resolve_relative_path

                    if is_relative_path(view.uri):
                        resolved = resolve_relative_path(view.uri, config_dir)
                        typer.echo(f"  Resolved: {resolved}")
                    else:
                        typer.echo(f"  Resolved: {view.uri} (absolute path)")

                    if check_accessibility:
                        is_accessible, error_msg = validate_file_accessibility(resolved)
                        if is_accessible:
                            typer.echo("  Status: ✅ Accessible")
                        else:
                            typer.echo(f"  Status: ❌ {error_msg}")
                typer.echo("")
    else:
        typer.echo("No views with file paths found.")


@app.command(help="Validate config and check path accessibility.")
def validate_paths(
    config_path: Path = typer.Argument(
        ..., exists=True, file_okay=True, dir_okay=False
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose logging output."
    ),
) -> None:
    """Validate configuration and check path accessibility.

    This command validates the configuration file and checks if all file
    paths are accessible.

    Args:
        config_path: Path to the configuration file.
        verbose: If True, enable more verbose logging.
    """
    _configure_logging(verbose)
    log_info("CLI validate-paths invoked", config_path=str(config_path))

    try:
        config = load_config(str(config_path))
        typer.echo("✅ Configuration is valid.")
    except ConfigError as exc:
        log_error("Validate-paths failed due to config error", error=str(exc))
        _fail(f"Config error: {exc}", 2)

    config_dir = config_path.resolve().parent
    inaccessible_files = []

    # Check accessibility of view files
    typer.echo("")
    typer.echo("Checking file accessibility...")
    typer.echo("-" * 50)

    if config.views:
        for view in config.views:
            if view.uri and view.source in ("parquet", "delta"):
                from .config import is_relative_path, resolve_relative_path

                path_to_check = view.uri
                if is_relative_path(view.uri):
                    path_to_check = resolve_relative_path(view.uri, config_dir)

                is_accessible, error_msg = validate_file_accessibility(path_to_check)
                if is_accessible:
                    typer.echo(f"✅ {view.name}: {path_to_check}")
                else:
                    typer.echo(f"❌ {view.name}: {error_msg}")
                    inaccessible_files.append((view.name, path_to_check, error_msg))

    # Summary
    typer.echo("")
    if inaccessible_files:
        typer.echo(f"❌ Found {len(inaccessible_files)} inaccessible files:")
        for name, path, error in inaccessible_files:
            typer.echo(f"  - {name}: {error}")
        _fail("Some files are not accessible.", 3)
    else:
        typer.echo("✅ All files are accessible.")


def _fail(message: str, code: int) -> None:
    """Print an error message and exit with the given code.

    Args:
        message: Message to write to stderr.
        code: Process exit code.
    """

    typer.echo(message, err=True)
    raise typer.Exit(code)


# @app.command(
#     name="ui", help="Launch the local starhtml/starui dashboard for a catalog."
# )
# def ui(
#     config_path: str = typer.Argument(
#         ..., help="Path to configuration file (local or remote)."
#     ),
#     host: str = typer.Option(
#         "127.0.0.1", "--host", help="Host to bind (default: loopback)."
#     ),
#     port: int = typer.Option(8787, "--port", help="Port to bind (default: 8787)."),
#     row_limit: int = typer.Option(
#         500, "--row-limit", help="Max rows to show in query results."
#     ),
#     verbose: bool = typer.Option(
#         False, "--verbose", "-v", help="Enable verbose logging output."
#     ),
# ) -> None:
#     """Start a local dashboard to inspect and query a Duckalog catalog."""

#     _configure_logging(verbose)

#     try:
#         config = load_config(config_path)
#     except ConfigError as exc:
#         _fail(f"Config error: {exc}", 2)

#     ctx = DashboardContext(config, config_path=config_path, row_limit=row_limit)
#     app = create_app(ctx)

#     try:
#         import uvicorn
#     except ImportError:  # pragma: no cover
#         _fail("uvicorn is required. Install with: pip install duckalog[ui]", 2)

#     typer.echo(f"Starting dashboard at http://{host}:{port}")
#     if host not in ("127.0.0.1", "localhost", "::1"):
#         typer.echo(
#             "Warning: binding to a non-loopback host may expose the dashboard to others on your network.",
#             err=True,
#         )
#     uvicorn.run(app, host=host, port=port, log_level="info")


@app.command(help="Initialize a new Duckalog configuration file.")
def init(
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path for the configuration. Defaults to catalog.yaml or catalog.json based on format.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        help="Output format: yaml or json (default: yaml)",
    ),
    database_name: str = typer.Option(
        "analytics_catalog.duckdb",
        "--database",
        "-d",
        help="DuckDB database filename (default: analytics_catalog.duckdb)",
    ),
    project_name: str = typer.Option(
        "my_analytics_project",
        "--project",
        "-p",
        help="Project name used in comments (default: my_analytics_project)",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite existing file without prompting",
    ),
    skip_existing: bool = typer.Option(
        False,
        "--skip-existing",
        help="Skip file creation if it already exists",
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose logging output."
    ),
) -> None:
    """Create a new Duckalog configuration file.

    This command generates a basic, valid configuration template with
    sensible defaults and educational example content.

    Examples:
        # Create a basic YAML config
        duckalog init

        # Create a JSON config with custom filename
        duckalog init --format json --output my_config.json

        # Create with custom database and project names
        duckalog init --database sales.db --project sales_analytics

        # Force overwrite existing file
        duckalog init --force
    """
    from pathlib import Path

    _configure_logging(verbose)

    # Validate format
    if format not in ("yaml", "json"):
        typer.echo(f"Error: Format must be 'yaml' or 'json', got '{format}'", err=True)
        raise typer.Exit(1)

    # Determine default output path
    if not output:
        output = f"catalog.{format}"

    output_path = Path(output)

    # Check if file already exists
    if output_path.exists():
        if skip_existing:
            typer.echo(f"File {output_path} already exists, skipping.")
            return
        elif not force:
            # Prompt for confirmation
            if not typer.confirm(f"File {output_path} already exists. Overwrite?"):
                typer.echo("Operation cancelled.")
                return

    try:
        # Generate the configuration template
        content = create_config_template(
            format=format,
            output_path=str(output_path),
            database_name=database_name,
            project_name=project_name,
        )

        # Validate the generated content
        validate_generated_config(content, format=format)

        # Determine default filename for messaging
        if output == f"catalog.{format}":
            filename_msg = f"catalog.{format} (default filename)"
        else:
            filename_msg = str(output_path)

        typer.echo(f"✅ Created Duckalog configuration: {filename_msg}")
        typer.echo(f"📁 Path: {output_path.resolve()}")
        typer.echo(f"📄 Format: {format.upper()}")
        typer.echo(f"💾 Database: {database_name}")

        if verbose:
            typer.echo("\n🔧 Next steps:")
            typer.echo(f"   1. Edit {output_path} to customize views and data sources")
            typer.echo(
                f"   2. Run 'duckalog validate {output_path}' to check your configuration"
            )
            typer.echo(
                f"   3. Run 'duckalog build {output_path}' to create your catalog"
            )

    except Exception as exc:
        if verbose:
            raise
        typer.echo(f"Error creating configuration: {exc}", err=True)
        raise typer.Exit(1)


def main_entry() -> None:
    """Invoke the Typer application as the console entry point."""

    app()


__all__ = ["app", "main_entry"]
