"""Duckalog catalog build engine."""

from __future__ import annotations

import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import duckdb

from .config import Config, load_config, is_relative_path, resolve_relative_path
from .config import get_logger, log_debug, log_info, log_error

# Optional imports for remote export functionality
try:
    import fsspec  # type: ignore
    from urllib.parse import urlparse  # type: ignore

    FSSPEC_AVAILABLE = True
except ImportError:
    fsspec = None
    urlparse = None
    FSSPEC_AVAILABLE = False

# Import quoting functions after other imports to avoid circular imports
try:
    from .sql_generation import quote_ident, quote_literal
except ImportError:
    # Fallback for circular import issues
    def quote_ident(value: str) -> str:
        escaped = value.replace('"', '""')
        return f'"{escaped}"'

    def quote_literal(value: str) -> str:
        escaped = value.replace("'", "''")
        return f"'{escaped}'"


logger = get_logger()

# Supported remote export URI schemes for catalog export
REMOTE_EXPORT_SCHEMES = {
    "s3://": "Amazon S3",
    "gs://": "Google Cloud Storage",
    "gcs://": "Google Cloud Storage",
    "abfs://": "Azure Blob Storage",
    "adl://": "Azure Data Lake Storage",
    "sftp://": "SFTP Server",
}


class CatalogBuilder:
    """Orchestrates the catalog build workflow with clear method boundaries."""

    def __init__(
        self,
        config: Config,
        *,
        dry_run: bool = False,
        filesystem=None,
        config_path: str | None = None,
        db_path: str | None = None,
        verbose: bool = False,
        duckalog_results: dict[str, BuildResult] | None = None,
    ):
        self.config = config
        self.dry_run = dry_run
        self.filesystem = filesystem
        self.config_path = config_path
        self.db_path = db_path
        self.verbose = verbose
        self.conn = None
        self.temp_file = None
        self.temp_paths = []
        self.remote_uri = None
        self.duckalog_results = duckalog_results or {}

    def build(self) -> str | None:
        """Build the catalog using the orchestrated workflow."""
        try:
            if self.dry_run:
                return self._handle_dry_run()

            self._setup_connection()
            self._apply_pragmas()
            self._setup_attachments()
            self._create_secrets()
            self._create_views()
            return self._export_if_needed()
        finally:
            self._cleanup()

    def _handle_dry_run(self) -> str:
        """Handle dry run mode to generate SQL without connecting to DuckDB."""
        from .sql_generation import generate_all_views_sql

        sql = generate_all_views_sql(self.config, include_secrets=True)
        log_info("Dry run SQL generation complete", views=len(self.config.views))
        return sql

    def _setup_connection(self) -> None:
        """Create and configure the DuckDB connection."""
        target_db = _resolve_db_path(self.config, self.db_path)

        # Handle remote export: create temp file locally, then upload
        if is_remote_export_uri(target_db):
            if not FSSPEC_AVAILABLE:
                raise EngineError(
                    "Remote export requires fsspec. Install with: pip install duckalog[remote]"
                )
            self.remote_uri = target_db
            # Create temporary file for local database creation
            self.temp_file = tempfile.NamedTemporaryFile(suffix=".duckdb", delete=False)
            self.temp_file.close()
            target_db = self.temp_file.name
            self.temp_paths.append(Path(target_db))
            log_info(
                "Building catalog locally for remote export",
                temp_file=target_db,
                remote_uri=self.remote_uri,
            )

        log_info("Connecting to DuckDB", db_path=target_db)
        try:
            self.conn = duckdb.connect(target_db)
        except Exception as exc:
            raise EngineError(
                f"Failed to connect to DuckDB at {target_db}: {exc}"
            ) from exc

    def _apply_pragmas(self) -> None:
        """Apply DuckDB settings, pragmas, and extensions."""
        if self.conn:
            _apply_duckdb_settings(self.conn, self.config, self.verbose)

    def _setup_attachments(self) -> None:
        """Setup all database attachments (DuckDB, SQLite, Postgres)."""
        if self.conn:
            _setup_attachments(self.conn, self.config, self.verbose)

            # Setup Duckalog child catalogs that were built during dependency resolution
            if self.duckalog_results:
                self._setup_duckalog_attachments()

    def _setup_duckalog_attachments(self) -> None:
        """Setup built Duckalog attachments on the main connection."""
        if not self.duckalog_results or not self.conn:
            return

        log_info("Attaching built Duckalog catalogs", count=len(self.duckalog_results))
        for duckalog_attachment in self.config.attachments.duckalog:
            if duckalog_attachment.alias in self.duckalog_results:
                result = self.duckalog_results[duckalog_attachment.alias]
                clause = " (READ_ONLY)" if duckalog_attachment.read_only else ""
                log_info(
                    "Attaching Duckalog child catalog",
                    alias=duckalog_attachment.alias,
                    database_path=result.database_path,
                    read_only=duckalog_attachment.read_only,
                )
                attach_command = (
                    f"ATTACH DATABASE {quote_literal(result.database_path)} "
                    f"AS {quote_ident(duckalog_attachment.alias)}{clause}"
                )
                log_debug("Executing attach command", command=attach_command)
                self.conn.execute(attach_command)
                log_debug("Attach command completed successfully")

                # Verify the attachment actually worked
                databases = self.conn.execute("PRAGMA database_list").fetchall()
                attached_aliases = [row[1] for row in databases]
                if duckalog_attachment.alias not in attached_aliases:
                    raise EngineError(
                        f"Failed to attach Duckalog catalog '{duckalog_attachment.alias}'. "
                        f"Expected alias not found in attached databases: {attached_aliases}"
                    )
                log_debug(
                    "Attachment verified",
                    alias=duckalog_attachment.alias,
                    attached_databases=attached_aliases,
                )

    def _create_secrets(self) -> None:
        """Create DuckDB secrets from configuration."""
        if self.conn:
            _create_secrets(self.conn, self.config, self.verbose)

    def _create_views(self) -> None:
        """Create all configured views."""
        if self.conn:
            _create_views(self.conn, self.config, self.verbose)

    def _export_if_needed(self) -> str | None:
        """Handle remote export if needed and return result."""
        # Handle remote export upload
        if self.temp_file and self.remote_uri:
            try:
                _upload_to_remote(
                    Path(self.temp_file.name), self.remote_uri, self.filesystem
                )
                log_info("Remote export complete", remote_uri=self.remote_uri)
            finally:
                # Cleanup temp file handled in _cleanup
                pass
        else:
            target_db = _resolve_db_path(self.config, self.db_path)
            log_info("Catalog build complete", db_path=target_db)

        return None

    def _cleanup(self) -> None:
        """Clean up temporary resources and close connections."""
        # Close database connection
        if self.conn:
            try:
                self.conn.close()
            except Exception:
                pass  # Best effort cleanup

        # Clean up temp files
        if self.temp_file:
            try:
                Path(self.temp_file.name).unlink()
            except Exception:
                pass  # Best effort cleanup

        # Clean up any other temp paths
        for temp_path in self.temp_paths:
            try:
                if temp_path.exists():
                    temp_path.unlink()
            except Exception:
                pass  # Best effort cleanup


@dataclass
class BuildResult:
    """Result of building a Duckalog config."""

    database_path: str
    config_path: str
    was_built: bool  # True if newly built, False if cached


class ConfigDependencyGraph:
    """Manages Duckalog config dependencies using simplified DFS approach."""

    def __init__(self, max_depth: int = 5):
        self.visiting: set[str] = set()
        self.visited: set[str] = set()
        self.build_cache: dict[str, BuildResult] = {}
        self.max_depth = max_depth

    def build_config_with_dependencies(
        self,
        config_path: str,
        dry_run: bool = False,
        parent_alias: str | None = None,
        database_override: str | None = None,
        _depth: int = 0,
    ) -> BuildResult:
        """Build config with dependencies using depth-limited DFS."""
        if _depth > self.max_depth:
            raise EngineError(
                f"Maximum dependency depth ({self.max_depth}) exceeded while "
                f"building '{config_path}'. This may indicate a circular dependency "
                f"or overly deep nesting."
            )

        return self._build_with_dependencies_recursive(
            config_path, dry_run, parent_alias, database_override, _depth
        )

    def _build_with_dependencies_recursive(
        self,
        config_path: str,
        dry_run: bool = False,
        parent_alias: str | None = None,
        database_override: str | None = None,
        _depth: int = 0,
    ) -> BuildResult:
        """Recursive helper for dependency resolution with DFS."""
        config_path = str(Path(config_path).resolve())

        # Check cache first
        if config_path in self.build_cache:
            cached_result = self.build_cache[config_path]
            log_debug(
                "Using cached build result",
                config_path=config_path,
                database_path=cached_result.database_path,
            )
            return cached_result

        # Detect cycles using visiting set
        if config_path in self.visiting:
            cycle_path = " -> ".join(self.visiting) + f" -> {config_path}"
            raise EngineError(f"Cyclic attachment detected: {cycle_path}")

        self.visiting.add(config_path)

        try:
            # Load and validate child config
            child_config = load_config(config_path)
            self._validate_child_database(child_config, config_path, parent_alias)

            # Resolve effective database path
            effective_db_path = self._resolve_database_path(
                child_config, config_path, database_override, parent_alias
            )

            # Recursively build nested Duckalog attachments
            nested_results = self._build_nested_dependencies(
                child_config, config_path, dry_run, _depth
            )

            # Build the database
            result = self._build_database(
                child_config,
                config_path,
                effective_db_path,
                nested_results,
                dry_run,
                _depth,
            )

            self.build_cache[config_path] = result
            return result

        finally:
            self.visiting.remove(config_path)
            self.visited.add(config_path)

    def _validate_child_database(
        self, child_config: Config, config_path: str, parent_alias: str | None
    ) -> None:
        """Validate that child config has a durable database."""
        child_db_path = child_config.duckdb.database
        if child_db_path == ":memory:":
            if parent_alias:
                raise EngineError(
                    f"Child config '{config_path}' uses in-memory database. "
                    f"Child configs must use persistent database paths for attachments. "
                    f"Found in attachment '{parent_alias}'."
                )
            else:
                raise EngineError(
                    f"Child config '{config_path}' uses in-memory database. "
                    "Child configs must use persistent database paths for attachments."
                )

    def _resolve_database_path(
        self,
        child_config: Config,
        config_path: str,
        database_override: str | None,
        parent_alias: str | None,
    ) -> str:
        """Resolve the effective database path for child config."""
        child_db_path = child_config.duckdb.database

        if database_override:
            effective_db_path = database_override
            log_info(
                "Using database override for child config",
                config_path=config_path,
                original_path=child_db_path,
                override_path=effective_db_path,
            )
        else:
            # Resolve child's database path relative to child config directory
            effective_db_path = child_db_path
            if is_relative_path(effective_db_path):
                child_config_dir = Path(config_path).parent
                effective_db_path = str(child_config_dir / effective_db_path)
                log_debug(
                    "Resolved child database path",
                    config_path=config_path,
                    original_db=child_db_path,
                    resolved_db=effective_db_path,
                )

        return effective_db_path

    def _build_nested_dependencies(
        self,
        child_config: Config,
        config_path: str,
        dry_run: bool,
        _depth: int,
    ) -> dict[str, BuildResult]:
        """Build nested Duckalog attachments."""
        nested_results = {}
        for duckalog_attachment in child_config.attachments.duckalog:
            nested_config_path = duckalog_attachment.config_path

            # Resolve relative paths relative to the parent config directory
            if is_relative_path(nested_config_path):
                parent_config_dir = Path(config_path).parent
                nested_config_path = str(parent_config_dir / nested_config_path)

            log_info(
                "Building nested Duckalog attachment",
                parent_config=config_path,
                child_config=nested_config_path,
                alias=duckalog_attachment.alias,
            )

            nested_result = self._build_with_dependencies_recursive(
                nested_config_path,
                dry_run,
                duckalog_attachment.alias,
                _depth=_depth + 1,
            )
            nested_results[duckalog_attachment.alias] = nested_result

        return nested_results

    def _build_database(
        self,
        child_config: Config,
        config_path: str,
        effective_db_path: str,
        nested_results: dict[str, BuildResult],
        dry_run: bool,
        _depth: int,
    ) -> BuildResult:
        """Build the actual database or return dry-run result."""
        if dry_run:
            # In dry run, we just return the theoretical result
            return BuildResult(
                database_path=effective_db_path,
                config_path=config_path,
                was_built=True,
            )

        # Actually build the database
        target_db = effective_db_path
        if not Path(target_db).parent.exists():
            Path(target_db).parent.mkdir(parents=True, exist_ok=True)

        log_info(
            "Building child catalog",
            config_path=config_path,
            database_path=target_db,
        )

        # Create child connection and setup
        child_conn = duckdb.connect(target_db)
        try:
            _apply_duckdb_settings(child_conn, child_config, False)
            _setup_attachments(child_conn, child_config, False)

            # Setup nested Duckalog attachments that were built during dependency resolution
            self._setup_nested_attachments(child_conn, child_config, nested_results)

            _setup_iceberg_catalogs(child_conn, child_config, False)
            _create_views(child_conn, child_config, False)
        finally:
            child_conn.close()

        return BuildResult(
            database_path=effective_db_path,
            config_path=config_path,
            was_built=True,
        )

    def _setup_nested_attachments(
        self,
        child_conn: duckdb.DuckDBPyConnection,
        child_config: Config,
        nested_results: dict[str, BuildResult],
    ) -> None:
        """Setup built Duckalog attachments on child connection."""
        for duckalog_attachment in child_config.attachments.duckalog:
            if duckalog_attachment.alias in nested_results:
                nested_result = nested_results[duckalog_attachment.alias]

                clause = " (READ_ONLY)" if duckalog_attachment.read_only else ""
                log_info(
                    "Attaching built DuckDB child catalog",
                    alias=duckalog_attachment.alias,
                    database_path=nested_result.database_path,
                    read_only=duckalog_attachment.read_only,
                )
                child_conn.execute(
                    f"ATTACH DATABASE {quote_literal(nested_result.database_path)} "
                    f"AS {quote_ident(duckalog_attachment.alias)}{clause}"
                )


from .errors import EngineError, DuckalogError


def build_catalog(
    config_path: str,
    db_path: str | None = None,
    dry_run: bool = False,
    verbose: bool = False,
    filesystem: Any | None = None,
    include_secrets: bool = True,
) -> str | None:
    """Build or update a DuckDB catalog from a configuration file.

    This function is the high-level entry point used by both the CLI and
    Python API. It loads the config, optionally performs a dry-run SQL
    generation, or otherwise connects to DuckDB, sets up attachments and
    Iceberg catalogs, and creates or replaces configured views.

    Args:
        config_path: Path to the YAML/JSON configuration file.
        db_path: Optional override for ``duckdb.database`` in the config.
            Can be a local path or remote URI (s3://, gs://, gcs://, abfs://, adl://, sftp://).
        dry_run: If ``True``, do not connect to DuckDB; instead generate and
            return the full SQL script for all views.
        verbose: If ``True``, enable more verbose logging via the standard
            logging module.
        filesystem: Optional pre-configured fsspec filesystem object for remote export
            authentication. If not provided, default authentication will be used.

    Returns:
        The generated SQL script as a string when ``dry_run`` is ``True``,
        otherwise ``None`` when the catalog is applied to DuckDB.

    Raises:
        ConfigError: If the configuration file is invalid.
        EngineError: If connecting to DuckDB or executing SQL fails, or if remote export fails.

    Example:
        Build a catalog in-place::

            from duckalog import build_catalog

            build_catalog("catalog.yaml")

        Build and export to remote storage::

            build_catalog("catalog.yaml", db_path="s3://my-bucket/catalog.duckdb")

        Generate SQL without modifying the database::

            sql = build_catalog("catalog.yaml", dry_run=True)
            print(sql)
    """

    # Note: Logging verbosity is configured at the CLI or application level,
    # not per-function. The logging configuration should already be set.

    config = load_config(config_path)

    # Handle Duckalog attachments/dependencies first
    dependency_graph = ConfigDependencyGraph()
    duckalog_results = {}

    if config.attachments.duckalog:
        log_info(
            "Building Duckalog attachment dependencies",
            count=len(config.attachments.duckalog),
        )

        for duckalog_attachment in config.attachments.duckalog:
            try:
                # Resolve database override path if provided
                database_override = None
                if duckalog_attachment.database:
                    database_override = duckalog_attachment.database
                    if is_relative_path(database_override):
                        # Resolve override path relative to parent config directory
                        parent_config_dir = Path(config_path).parent
                        try:
                            database_override = resolve_relative_path(
                                database_override, parent_config_dir
                            )
                        except Exception as exc:
                            raise EngineError(
                                f"Failed to resolve database override '{duckalog_attachment.database}' "
                                f"for attachment '{duckalog_attachment.alias}': {exc}"
                            ) from exc

                result = dependency_graph.build_config_with_dependencies(
                    duckalog_attachment.config_path,
                    dry_run,
                    duckalog_attachment.alias,
                    database_override,
                )
                duckalog_results[duckalog_attachment.alias] = result

            except EngineError as exc:
                raise EngineError(
                    f"Failed to build Duckalog attachment '{duckalog_attachment.alias}' "
                    f"from '{duckalog_attachment.config_path}': {exc}"
                ) from exc

    # Use CatalogBuilder for the main build process
    builder = CatalogBuilder(
        config,
        dry_run=dry_run,
        filesystem=filesystem,
        config_path=config_path,
        db_path=db_path,
        verbose=verbose,
        duckalog_results=duckalog_results,
    )

    return builder.build()


def is_remote_export_uri(path: str) -> bool:
    """Check if a path is a remote export URI that requires upload.

    Args:
        path: The path to check

    Returns:
        True if the path is a remote export URI, False otherwise
    """
    if not path or not FSSPEC_AVAILABLE:
        return False

    return any(path.startswith(scheme) for scheme in REMOTE_EXPORT_SCHEMES)


def _upload_to_remote(local_file: Path, remote_uri: str, filesystem=None) -> None:
    """Upload local database file to remote storage using fsspec.

    Args:
        local_file: Path to the local database file to upload
        remote_uri: Remote URI to upload to (e.g., s3://bucket/catalog.duckdb)
        filesystem: Optional pre-configured fsspec filesystem object

    Raises:
        EngineError: If upload fails due to missing dependencies, auth, or network issues
    """
    if not FSSPEC_AVAILABLE:
        raise EngineError(
            "Remote export requires fsspec. Install with: pip install duckalog[remote]"
        )

    try:
        # Use provided filesystem or create one from the URI
        if filesystem is None:
            # Extract protocol from URI for filesystem creation
            if urlparse is None:
                raise EngineError("Remote export requires urlparse from urllib.parse")
            parsed = urlparse(remote_uri)
            protocol = parsed.scheme

            # Create filesystem with default authentication
            if fsspec is None:
                raise EngineError("Remote export requires fsspec")
            filesystem = fsspec.filesystem(protocol)

        log_info("Uploading catalog to remote storage", remote_uri=remote_uri)

        # Stream upload to minimize memory usage
        with open(local_file, "rb") as local_f:
            with filesystem.open(remote_uri, "wb") as remote_f:
                shutil.copyfileobj(local_f, remote_f)

        log_info("Upload complete", remote_uri=remote_uri)

    except Exception as exc:
        raise EngineError(f"Failed to upload catalog to {remote_uri}: {exc}") from exc


def _resolve_db_path(config: Config, override: str | None) -> str:
    if override:
        return override
    if config.duckdb.database:
        return config.duckdb.database
    return ":memory:"


def _create_secrets(
    conn: duckdb.DuckDBPyConnection, config: Config, verbose: bool
) -> None:
    """Create DuckDB secrets from configuration."""
    db_conf = config.duckdb
    if not db_conf.secrets:
        return

    log_info("Creating DuckDB secrets", count=len(db_conf.secrets))

    # Import the SQL generation function
    from .sql_generation import generate_secret_sql

    for index, secret in enumerate(db_conf.secrets, start=1):
        log_debug(
            "Creating secret",
            index=index,
            type=secret.type,
            name=secret.name or secret.type,
        )

        sql = generate_secret_sql(secret)
        log_debug("Executing secret SQL", index=index, sql=sql)

        try:
            conn.execute(sql)
            log_info(
                "Secret created successfully",
                name=secret.name or secret.type,
                type=secret.type,
            )
        except Exception as e:
            log_error(
                "Failed to create secret", name=secret.name or secret.type, error=str(e)
            )
            raise EngineError(
                f"Failed to create secret '{secret.name or secret.type}': {e}"
            ) from e


def _apply_duckdb_settings(
    conn: duckdb.DuckDBPyConnection, config: Config, verbose: bool
) -> None:
    db_conf = config.duckdb
    for ext in db_conf.install_extensions:
        log_info("Installing DuckDB extension", extension=ext)
        conn.install_extension(ext)
    for ext in db_conf.load_extensions:
        log_info("Loading DuckDB extension", extension=ext)
        conn.load_extension(ext)

    # Create secrets after extensions but before pragmas
    _create_secrets(conn, config, verbose)

    if db_conf.pragmas:
        log_info("Executing DuckDB pragmas", count=len(db_conf.pragmas))
    for index, pragma in enumerate(db_conf.pragmas, start=1):
        log_debug("Running pragma", index=index)
        conn.execute(pragma)

    # Apply settings after pragmas
    if db_conf.settings:
        settings_list = (
            db_conf.settings
            if isinstance(db_conf.settings, list)
            else [db_conf.settings]
        )
        log_info("Executing DuckDB settings", count=len(settings_list))
        for index, setting in enumerate(settings_list, start=1):
            log_debug("Running setting", index=index, setting=setting)
            conn.execute(setting)


def _setup_attachments(
    conn: duckdb.DuckDBPyConnection, config: Config, verbose: bool
) -> None:
    for duckdb_attachment in config.attachments.duckdb:
        clause = " (READ_ONLY)" if duckdb_attachment.read_only else ""
        log_info(
            "Attaching DuckDB database",
            alias=duckdb_attachment.alias,
            path=duckdb_attachment.path,
            read_only=duckdb_attachment.read_only,
        )
        conn.execute(
            f"ATTACH DATABASE {quote_literal(duckdb_attachment.path)} AS {quote_ident(duckdb_attachment.alias)}{clause}"
        )

    for sqlite_attachment in config.attachments.sqlite:
        log_info(
            "Attaching SQLite database",
            alias=sqlite_attachment.alias,
            path=sqlite_attachment.path,
        )
        conn.execute(
            f"ATTACH DATABASE {quote_literal(sqlite_attachment.path)} AS {quote_ident(sqlite_attachment.alias)} (TYPE SQLITE)"
        )

    for pg_attachment in config.attachments.postgres:
        log_info(
            "Attaching Postgres database",
            alias=pg_attachment.alias,
            host=pg_attachment.host,
            database=pg_attachment.database,
            user=pg_attachment.user,
        )
        log_debug(
            "Postgres attachment details",
            alias=pg_attachment.alias,
            user=pg_attachment.user,
            password="<REDACTED>",
            options=pg_attachment.options,
        )
        clauses = [
            "TYPE POSTGRES",
            f"HOST {quote_literal(pg_attachment.host)}",
            f"PORT {pg_attachment.port}",
            f"USER {quote_literal(pg_attachment.user)}",
            f"PASSWORD {quote_literal(pg_attachment.password)}",
            f"DATABASE {quote_literal(pg_attachment.database)}",
        ]
        if pg_attachment.sslmode:
            clauses.append(f"SSLMODE {quote_literal(pg_attachment.sslmode)}")
        for key, value in pg_attachment.options.items():
            clauses.append(f"{key.upper()} {quote_literal(str(value))}")
        clause_sql = ", ".join(clauses)
        conn.execute(
            f"ATTACH DATABASE {quote_literal(pg_attachment.database)} AS {quote_ident(pg_attachment.alias)} ({clause_sql})"
        )


def _setup_iceberg_catalogs(
    conn: duckdb.DuckDBPyConnection, config: Config, verbose: bool
) -> None:
    for catalog in config.iceberg_catalogs:
        log_info(
            "Registering Iceberg catalog",
            name=catalog.name,
            catalog_type=catalog.catalog_type,
        )
        log_debug("Iceberg catalog options", name=catalog.name, options=catalog.options)
        options = []
        if catalog.uri:
            options.append(f"uri => {quote_literal(catalog.uri)}")
        if catalog.warehouse:
            options.append(f"warehouse => {quote_literal(catalog.warehouse)}")
        for key, value in catalog.options.items():
            options.append(f"{key} => {quote_literal(str(value))}")
        options_sql = ", ".join(options)
        query = (
            "CALL iceberg_attach("
            f"{quote_literal(catalog.name)}, "
            f"{quote_literal(catalog.catalog_type)}"
            f"{', ' + options_sql if options_sql else ''})"
        )
        conn.execute(query)


def _create_views(
    conn: duckdb.DuckDBPyConnection, config: Config, verbose: bool
) -> None:
    for view in config.views:
        from .sql_generation import generate_view_sql

        sql = generate_view_sql(view)
        log_info("Creating or replacing view", name=view.name)
        conn.execute(sql)


__all__ = ["build_catalog", "CatalogBuilder", "EngineError", "is_remote_export_uri"]
