"""Configuration template generation for Duckalog."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

import yaml

from .config import Config, load_config
from .logging_utils import log_info

ConfigFormat = Literal["yaml", "json"]


def create_config_template(
    format: ConfigFormat = "yaml",
    output_path: str | None = None,
    database_name: str = "analytics_catalog.duckdb",
    project_name: str = "my_analytics_project",
) -> str:
    """Generate a basic, valid Duckalog configuration template.

    This function creates a configuration template with sensible defaults
    and educational example content that demonstrates key Duckalog features.

    Args:
        format: Output format for the configuration ('yaml' or 'json').
            Defaults to 'yaml'.
        output_path: Optional path to write the configuration file.
            If provided, the template is written to this path and the
            content is also returned as a string.
        database_name: Name for the DuckDB database file.
        project_name: Name used in comments to personalize the template.

    Returns:
        The generated configuration as a string.

    Raises:
        ValueError: If format is not 'yaml' or 'json'.
        ConfigError: If the generated template fails validation.
        OSError: If writing to output_path fails.

    Example:
        Generate a YAML template::

            template = create_config_template(format='yaml')
            print(template)

        Generate and save a JSON template::

            template = create_config_template(
                format='json',
                output_path='my_config.json'
            )
    """
    if format not in ("yaml", "json"):
        raise ValueError("Format must be 'yaml' or 'json'")

    # Generate the template configuration
    template_data = _generate_template_data(project_name, database_name)

    # Validate the template before returning
    _validate_template(template_data)

    # Convert to requested format
    if format == "yaml":
        content = _format_as_yaml(template_data)
    else:  # json
        content = _format_as_json(template_data)

    # Write to file if requested
    if output_path:
        _write_config_file(content, output_path)

    return content


def _generate_template_data(project_name: str, database_name: str) -> dict[str, Any]:
    """Generate the dictionary structure for the config template."""
    return {
        "version": 1,
        "duckdb": {
            "database": database_name,
            "pragmas": [
                # Memory and performance optimizations
                "SET memory_limit='2GB'",
                "SET threads='4'",
                "SET enable_progress_bar=true",
            ],
        },
        # Example views demonstrating different data sources and patterns
        "views": [
            {
                "name": "example_parquet_data",
                "source": "parquet",
                "uri": "./data/sample_data.parquet",
                "description": "Example view reading from Parquet files - replace with your actual data path",
            },
            {
                "name": "example_derived_view",
                "sql": """
-- Example derived view - demonstrates SQL transformations
SELECT 
    DATE(event_timestamp) as event_date,
    COUNT(*) as event_count,
    COUNT(DISTINCT user_id) as unique_users
FROM example_parquet_data
WHERE event_timestamp >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(event_timestamp)
ORDER BY event_date DESC
""".strip(),
                "description": "Example derived view showing analytics - customize for your use case",
            },
            {
                "name": "example_daily_summary",
                "sql": f"""
-- Example time-series aggregation view for {project_name}
SELECT 
    event_date,
    event_count,
    unique_users,
    event_count::FLOAT / unique_users as avg_events_per_user
FROM example_derived_view
WHERE event_date >= CURRENT_DATE - INTERVAL '7 days'
""".strip(),
                "description": f"Example summary view for {project_name} - demonstrates referencing other views",
            },
        ],
    }


def _validate_template(template_data: dict[str, Any]) -> None:
    """Validate that the generated template is a valid Duckalog configuration."""
    try:
        # Use the existing Config model to validate
        Config.model_validate(template_data)
    except Exception as exc:
        from .errors import ConfigError

        raise ConfigError(f"Generated template is invalid: {exc}") from exc


def _format_as_yaml(template_data: dict[str, Any]) -> str:
    """Format template data as YAML with helpful comments."""
    # Create a YAML document with comments
    yaml_content = yaml.dump(template_data, default_flow_style=False, sort_keys=False)

    # Add educational header comments
    header_comments = """# Duckalog Configuration for Analytics Project
# This is a generated configuration template for Duckalog.
# 
# Key sections:
# - version: Configuration schema version (required)
# - duckdb: Database settings, pragmas, and extensions
# - views: Catalog views that query your data sources
# - attachments: Optional external database connections
# - iceberg_catalogs: Optional Apache Iceberg catalog configurations
#
# Data source types supported in views:
# - parquet: Apache Parquet files (local or cloud storage)
# - delta: Delta Lake tables  
# - iceberg: Apache Iceberg tables
# - duckdb: Attached DuckDB databases
# - sqlite: SQLite database files
# - postgres: PostgreSQL databases
#
# For more examples and advanced configurations, see:
# https://github.com/sst/duckalog/tree/main/examples

"""

    return header_comments + yaml_content


def _format_as_json(template_data: dict[str, Any]) -> str:
    """Format template data as JSON with proper formatting."""
    return json.dumps(template_data, indent=2)


def _write_config_file(content: str, output_path: str) -> None:
    """Write the configuration content to a file."""
    path = Path(output_path)

    # Create parent directories if they don't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write the file
    path.write_text(content, encoding="utf-8")

    log_info("Configuration template written", path=str(path))


def validate_generated_config(content: str, format: ConfigFormat = "yaml") -> None:
    """Validate that generated configuration content can be loaded successfully.

    Args:
        content: Configuration content as string.
        format: Format of the content ('yaml' or 'json').

    Raises:
        ConfigError: If the configuration cannot be loaded or is invalid.
    """
    from tempfile import NamedTemporaryFile
    from .errors import ConfigError

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
            Path(temp_path).unlink(missing_ok=True)

    except Exception as exc:
        raise ConfigError(f"Generated configuration validation failed: {exc}") from exc


__all__ = [
    "create_config_template",
    "validate_generated_config",
    "ConfigFormat",
]
