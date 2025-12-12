"""SQL generation utilities for Duckalog views."""

from __future__ import annotations

from typing import Any

from .config import Config, SecretConfig, ViewConfig
from .secret_types import (
    AzureSecretConfig,
    GCSSecretConfig,
    HTTPSecretConfig,
    MySQLSecretConfig,
    PostgresSecretConfig,
    S3SecretConfig,
)


def quote_ident(value: str) -> str:
    """Quote a SQL identifier using double quotes.

    This helper wraps a string in double quotes and escapes any embedded
    double quotes according to SQL rules.

    Args:
        value: Identifier to quote (for example, a view or column name).

    Returns:
        The identifier wrapped in double quotes.

    Example:
        >>> quote_ident("events")
        '"events"'
    """

    escaped = value.replace('"', '""')
    return f'"{escaped}"'


def quote_literal(value: str) -> str:
    """Quote a SQL string literal using single quotes.

    This helper wraps a string in single quotes and escapes any embedded
    single quotes according to SQL rules.

    Args:
        value: String literal to quote (for example, a file path, secret, or connection string).

    Returns:
        The string wrapped in single quotes with proper escaping.

    Example:
        >>> quote_literal("path/to/file.parquet")
        "'path/to/file.parquet'"
        >>> quote_literal("user's data")
        "'user''s data'"
    """
    escaped = value.replace("'", "''")
    return f"'{escaped}'"


def _quote_literal(value: str) -> str:
    """Deprecated: Use quote_literal instead."""
    return quote_literal(value)


def render_options(options: dict[str, Any]) -> str:
    """Render a mapping of options into scan-function arguments.

    The resulting string is suitable for appending to a ``*_scan`` function
    call. Keys are sorted alphabetically to keep output deterministic.

    Args:
        options: Mapping of option name to value (str, bool, int, or float).

    Returns:
        A string that starts with ``, `` when options are present (for example,
        ``", hive_partitioning=TRUE"``) or an empty string when no options
        are provided.

    Raises:
        TypeError: If a value has a type that cannot be rendered safely.
    """

    if not options:
        return ""

    parts = []
    for key in sorted(options):
        value = options[key]
        if isinstance(value, bool):
            rendered = "TRUE" if value else "FALSE"
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            rendered = str(value)
        elif isinstance(value, str):
            rendered = _quote_literal(value)
        else:
            raise TypeError(
                f"Unsupported option value for '{key}': {value!r}. Expected str, bool, int, or float."
            )
        parts.append(f"{key}={rendered}")

    return ", " + ", ".join(parts)


def generate_view_sql(view: ViewConfig) -> str:
    """Generate a ``CREATE OR REPLACE VIEW`` statement for a single view.

    Args:
        view: The :class:`ViewConfig` to generate SQL for.

    Returns:
        A single SQL statement that creates or replaces the view.
    """

    # Generate schema-qualified view name if db_schema is provided
    if view.db_schema:
        view_name = f"{quote_ident(view.db_schema)}.{quote_ident(view.name)}"
    else:
        view_name = quote_ident(view.name)

    if view.sql:
        body = view.sql
    else:
        body = _render_view_body(view)

    return f"CREATE OR REPLACE VIEW {view_name} AS\n{body};"


def _render_view_body(view: ViewConfig) -> str:
    source = view.source
    if source is None:
        raise ValueError("View must define 'sql' or 'source'")

    if source in {"parquet", "delta"}:
        func = f"{source}_scan"
        assert view.uri is not None  # enforced by schema
        scan_call = f"{func}({_quote_literal(view.uri)}{render_options(view.options)})"
        return f"SELECT * FROM {scan_call}"

    if source == "iceberg":
        if view.uri:
            scan_call = f"iceberg_scan({_quote_literal(view.uri)}{render_options(view.options)})"
        else:
            assert view.catalog and view.table  # enforced by schema
            scan_call = (
                "iceberg_scan("
                f"{_quote_literal(view.catalog)}, {_quote_literal(view.table)}"
                f"{render_options(view.options)})"
            )
        return f"SELECT * FROM {scan_call}"

    if source in {"duckdb", "sqlite", "postgres"}:
        assert view.database and view.table  # enforced by schema
        return f"SELECT * FROM {quote_ident(view.database)}.{quote_ident(view.table)}"

    raise ValueError(f"Unsupported view source '{source}'")


def generate_all_views_sql(config: Config, include_secrets: bool = False) -> str:
    """Generate SQL for all views in a configuration.

    The output includes a descriptive header with the config version followed
    by a ``CREATE OR REPLACE VIEW`` statement for each view in the order they
    appear in the configuration.

    Args:
        config: The validated :class:`Config` instance to render.
        include_secrets: Whether to include CREATE SECRET statements for secrets.

    Returns:
        A multi-statement SQL script suitable for use as a catalog definition.
    """
    lines = [
        "-- Generated by Duckalog",
        f"-- Config version: {config.version}",
        "",
    ]

    for index, view in enumerate(config.views):
        lines.append(generate_view_sql(view))
        if index != len(config.views) - 1:
            lines.append("")

    # Add secrets if requested
    if include_secrets and config.duckdb.secrets:
        lines.extend(["", "-- Secrets"])
        for secret in config.duckdb.secrets:
            lines.append(generate_secret_sql(secret))

    return "\n".join(lines)


def generate_secret_sql(secret: SecretConfig) -> str:
    """Generate CREATE SECRET statement for a DuckDB secret.

    Args:
        secret: Secret configuration object.

    Returns:
        SQL CREATE SECRET statement.
    """
    # Get the secret name
    secret_name = secret.name or secret.type

    # Build the secret type and parameters
    params = [f"TYPE {secret.type.upper()}"]

    # Add provider if not 'config'
    if secret.provider == "credential_chain":
        params.append("PROVIDER credential_chain")

    # Add parameters based on secret type
    if secret.type == "s3":
        if secret.provider == "credential_chain":
            if secret.region:
                params.append(f"REGION {quote_literal(secret.region)}")
        else:  # config provider
            if secret.key_id:
                params.append(f"KEY_ID {quote_literal(secret.key_id)}")
            if secret.secret:
                params.append(f"SECRET {quote_literal(secret.secret)}")
            if secret.region:
                params.append(f"REGION {quote_literal(secret.region)}")
            if secret.endpoint:
                params.append(f"ENDPOINT {quote_literal(secret.endpoint)}")

    elif secret.type == "azure":
        if secret.connection_string:
            params.append(
                f"CONNECTION_STRING {quote_literal(secret.connection_string)}"
            )
        else:
            if secret.tenant_id:
                params.append(f"TENANT_ID {quote_literal(secret.tenant_id)}")
            if secret.client_id:
                params.append(f"CLIENT_ID {quote_literal(secret.client_id)}")
            client_secret = secret.client_secret or secret.secret
            if client_secret:
                params.append(f"SECRET {quote_literal(client_secret)}")
            if secret.account_name:
                params.append(f"ACCOUNT_NAME {quote_literal(secret.account_name)}")

    elif secret.type == "gcs":
        if secret.service_account_key:
            params.append(
                f"SERVICE_ACCOUNT_KEY {quote_literal(secret.service_account_key)}"
            )
        elif secret.json_key:
            params.append(f"JSON_KEY {quote_literal(secret.json_key)}")
        elif secret.key_id and secret.secret:
            # Fallback to key_id/secret for basic auth
            params.append(f"KEY_ID {quote_literal(secret.key_id)}")
            params.append(f"SECRET {quote_literal(secret.secret)}")

    elif secret.type == "http":
        if secret.bearer_token:
            params.append(f"BEARER_TOKEN {quote_literal(secret.bearer_token)}")
        elif secret.header:
            params.append(f"HEADER {quote_literal(secret.header)}")
        else:
            # Fallback for basic auth
            if secret.key_id:
                params.append(f"USERNAME {quote_literal(secret.key_id)}")
            if secret.secret:
                params.append(f"PASSWORD {quote_literal(secret.secret)}")

    elif secret.type == "postgres":
        if secret.connection_string:
            params.append(
                f"CONNECTION_STRING {quote_literal(secret.connection_string)}"
            )
        else:
            if secret.host:
                params.append(f"HOST {quote_literal(secret.host)}")
            if secret.port:
                params.append(f"PORT {secret.port}")
            if secret.database:
                params.append(f"DATABASE {quote_literal(secret.database)}")
            # Check both user and key_id (for compatibility)
            user_field = secret.user or secret.key_id
            if user_field:
                params.append(f"USER {quote_literal(user_field)}")
            # Check both password and secret (for compatibility)
            password_field = secret.password or secret.secret
            if password_field:
                params.append(f"PASSWORD {quote_literal(password_field)}")

    elif secret.type == "mysql":
        if secret.connection_string:
            params.append(
                f"CONNECTION_STRING {quote_literal(secret.connection_string)}"
            )
        else:
            if secret.host:
                params.append(f"HOST {quote_literal(secret.host)}")
            if secret.port:
                params.append(f"PORT {secret.port}")
            if secret.database:
                params.append(f"DATABASE {quote_literal(secret.database)}")
            # Check both user and key_id (for compatibility)
            user_field = secret.user or secret.key_id
            if user_field:
                params.append(f"USER {quote_literal(user_field)}")
            # Check both password and secret (for compatibility)
            password_field = secret.password or secret.secret
            if password_field:
                params.append(f"PASSWORD {quote_literal(password_field)}")

    # Add options if provided
    if secret.options:
        for key, value in sorted(secret.options.items()):
            if isinstance(value, bool):
                rendered = "TRUE" if value else "FALSE"
            elif isinstance(value, (int, float)) and not isinstance(value, bool):
                rendered = str(value)
            elif isinstance(value, str):
                rendered = quote_literal(value)
            else:
                raise TypeError(
                    f"Unsupported option value for '{key}': {value!r}. "
                    f"Expected str, bool, int, or float."
                )
            params.append(f"{key.upper()} {rendered}")

    # Build the full SQL statement
    secret_sql = f"CREATE {'PERSISTENT ' if secret.persistent else ''}SECRET {secret_name} ({', '.join(params)})"

    # Add scope if provided
    if secret.scope:
        secret_sql += f"; SCOPE {quote_literal(secret.scope)}"

    return secret_sql


__all__ = [
    "quote_ident",
    "quote_literal",
    "render_options",
    "generate_view_sql",
    "generate_all_views_sql",
    "generate_secret_sql",
]
