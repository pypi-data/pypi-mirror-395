"""High-level Python convenience functions for Duckalog."""

from __future__ import annotations

import duckdb
from contextlib import contextmanager
from pathlib import Path
from collections.abc import Generator
from typing import Any

from .config import ConfigError, load_config
from .engine import build_catalog
from .sql_generation import generate_all_views_sql


def generate_sql(config_path: str) -> str:
    """Generate a full SQL script from a config file.

    This is a convenience wrapper around :func:`load_config` and
    :func:`generate_all_views_sql` that does not connect to DuckDB.

    Args:
        config_path: Path to the YAML/JSON configuration file.

    Returns:
        A multi-statement SQL script containing ``CREATE OR REPLACE VIEW``
        statements for all configured views.

    Raises:
        ConfigError: If the configuration file is invalid.

    Example:
        >>> from duckalog import generate_sql
        >>> sql = generate_sql("catalog.yaml")
        >>> print("CREATE VIEW" in sql)
        True
    """

    config = load_config(config_path)
    return generate_all_views_sql(config)


def validate_config(config_path: str) -> None:
    """Validate a configuration file without touching DuckDB.

    Args:
        config_path: Path to the YAML/JSON configuration file.

    Raises:
        ConfigError: If the configuration file is missing, malformed, or does
            not satisfy the schema and interpolation rules.

    Example:
        >>> from duckalog import validate_config
        >>> validate_config("catalog.yaml")  # raises on invalid config
    """

    try:
        load_config(config_path)
    except ConfigError:
        raise


def connect_to_catalog(
    config_path: str,
    database_path: str | None = None,
    read_only: bool = False,
) -> duckdb.DuckDBPyConnection:
    """Connect to an existing DuckDB database created by Duckalog.

    This function provides a direct connection to a DuckDB database that was previously
    created using Duckalog. It simplifies the workflow for users who just want to start
    querying their catalog database.

    Args:
        config_path: Path to the YAML/JSON configuration file for an existing catalog.
        database_path: Optional database path override. If not provided, uses the
            path from the configuration.
        read_only: Open the connection in read-only mode for safety.

    Returns:
        An active DuckDB connection object ready for query execution.

    Raises:
        ConfigError: If the configuration file is invalid.
        FileNotFoundError: If the specified database file doesn't exist.
        duckdb.Error: If connection or queries fail.

    Example:
        Connect to an existing catalog::

            from duckalog import connect_to_catalog
            conn = connect_to_catalog("catalog.yaml")

            # Use the connection for queries
            result = conn.execute("SELECT * FROM some_table").fetchall()
            conn.close()

        With path override::

            conn = connect_to_catalog("catalog.yaml", database_path="analytics.db")

        With read-only mode::

            conn = connect_to_catalog("catalog.yaml", read_only=True)

        With context manager::

            from duckalog import connect_to_catalog_cm
            with connect_to_catalog_cm("catalog.yaml") as conn:
                data = conn.execute("SELECT * FROM users").fetchall()
                print(f"Found {len(data)} records")
            # Connection automatically closed here
    """

    # Load configuration to determine database path
    config = load_config(config_path)

    # Determine database path with precedence
    if database_path is None:
        database_path = config.duckdb.database

    # Ensure database_path is not None after fallback
    if database_path is None:
        raise ConfigError("No database path specified and no default in config")

    # Validate database path exists (for existing catalogs)
    db_path = Path(database_path)
    if database_path != ":memory:" and not db_path.exists():
        raise FileNotFoundError(f"Database file not found: {db_path}")

    # Create and return the connection
    return duckdb.connect(str(db_path), read_only=read_only)


@contextmanager
def connect_to_catalog_cm(
    config_path: str,
    database_path: str | None = None,
    read_only: bool = False,
) -> Generator[duckdb.DuckDBPyConnection]:
    """Context manager version of connect_to_catalog for automatic connection cleanup.

    Usage::

        from duckalog import connect_to_catalog_cm
        with connect_to_catalog_cm("catalog.yaml") as conn:
            data = conn.execute("SELECT * FROM users").fetchall()
            print(f"Found {len(data)} records")
        # Connection is automatically closed here

    Args:
        config_path: Path to the YAML/JSON configuration file for an existing catalog.
        database_path: Optional database path override.
        read_only: Open the connection in read-only mode for safety.

    Yields:
        An active DuckDB connection that will be closed automatically.

    Raises:
        ConfigError: If the configuration file is invalid.
        FileNotFoundError: If the specified database file doesn't exist.
        duckdb.Error: If connection or queries fail.
    """
    conn = None
    try:
        # Use the main function to get the connection
        conn = connect_to_catalog(
            config_path=config_path,
            database_path=database_path,
            read_only=read_only,
        )
        yield conn
    finally:
        # Ensure connection is closed even if there's an exception
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass


def connect_and_build_catalog(
    config_path: str,
    database_path: str | None = None,
    dry_run: bool = False,
    verbose: bool = False,
    read_only: bool = False,
    **kwargs: Any,
) -> duckdb.DuckDBPyConnection | str | None:
    """Build a catalog and create a DuckDB connection in one operation.

    This function combines catalog building with connection creation, providing a streamlined
    workflow for users who want to start working with their catalog immediately after creating it.

    Args:
        config_path: Path to the YAML/JSON configuration file.
        database_path: Optional database path override.
        dry_run: If True, only validates configuration and returns SQL. If False,
            builds the catalog and creates a connection.
        verbose: Enable verbose logging during build process.
        read_only: Open the resulting connection in read-only mode.
        **kwargs: Additional keyword arguments.

    Returns:
        A DuckDB connection object for immediate use, or SQL string when dry_run=True.

    Raises:
        ConfigError: If the configuration file is invalid.
        EngineError: If catalog building or connection fails.
        FileNotFoundError: If the resulting database file doesn't exist (after build).

    Example:
        Build catalog and start querying immediately::

            conn = connect_and_build_catalog("catalog.yaml")
            data = conn.execute("SELECT * FROM important_table").fetchall()
            print(f"Found {len(data)} records")
            conn.close()

        Validate only (dry run)::

        sql = connect_and_build_catalog("catalog.yaml", dry_run=True)
        print("SQL generation completed, no database created")

        Custom database path::

            conn = connect_and_build_catalog("catalog.yaml", database_path="analytics.db")
            print("Connected to custom database: analytics.db")

    If `dry_run=True`, the function only validates the configuration and returns the SQL script
    without creating any database files or connections.
    """

    if dry_run:
        # Just validate configuration and return SQL
        return build_catalog(
            config_path,
            db_path=database_path,
            dry_run=True,
            verbose=verbose,
            filesystem=kwargs.get("filesystem"),
        )

    # Extract build kwargs that aren't for the connection
    build_kwargs = {k: v for k, v in kwargs.items() if k in ["filesystem"]}

    # First, build the catalog (reuse existing logic)
    build_catalog(
        config_path=config_path,
        db_path=database_path,
        dry_run=False,
        verbose=verbose,
        **build_kwargs,
    )

    # Validate the database was created
    if database_path is None:
        database_path = load_config(config_path).duckdb.database

    # Extract connection kwargs (everything else)
    connection_kwargs = {k: v for k, v in kwargs.items() if k not in ["filesystem"]}

    # Create connection to the catalog database
    return duckdb.connect(str(database_path), read_only=read_only, **connection_kwargs)


def validate_generated_config(content: str, format: str = "yaml") -> None:
    """Validate that generated configuration content can be loaded successfully.

    This helper function validates that the configuration content can be loaded and parsed
    by the current Duckalog configuration system.

    Args:
        content: Configuration content as string.
        format: "yaml" or "json".

    Raises:
        ConfigError: If the configuration cannot be loaded or is invalid.
    """
    from tempfile import NamedTemporaryFile

    try:
        # Write content to a temporary file to test loading
        with NamedTemporaryFile(mode="w", suffix=f".{format}", delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            # Try to load the config using the existing loader
            load_config(temp_path, load_sql_files=False)
        finally:
            # Clean up the temporary file
            import os

            os.unlink(temp_path)

    except Exception as exc:
        raise ConfigError(f"Generated configuration validation failed: {exc}") from exc


__all__ = [
    "generate_sql",
    "validate_config",
    "connect_to_catalog",
    "connect_to_catalog_cm",
    "connect_and_build_catalog",
    "validate_generated_config",
]
