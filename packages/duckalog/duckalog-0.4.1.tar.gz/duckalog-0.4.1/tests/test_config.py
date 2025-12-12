"""Tests for the Duckalog configuration schema and loader."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from duckalog import ConfigError, load_config
from duckalog.remote_config import is_remote_uri


def _write(path: Path, content: str) -> Path:
    path.write_text(textwrap.dedent(content))
    return path


def test_load_config_yaml_with_env_interpolation(monkeypatch, tmp_path):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "AKIA123")
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          pragmas:
            - "SET s3_access_key_id='${env:AWS_ACCESS_KEY_ID}'"
        views:
          - name: vip_users
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))

    assert config.duckdb.pragmas == ["SET s3_access_key_id='AKIA123'"]


def test_load_config_json_parses(tmp_path):
    payload = {
        "version": 2,
        "duckdb": {"database": "test.duckdb"},
        "views": [
            {
                "name": "users",
                "source": "parquet",
                "uri": "s3://bucket/users/*.parquet",
                "options": {"hive_partitioning": True},
            }
        ],
    }
    config_path = tmp_path / "catalog.json"
    config_path.write_text(json.dumps(payload))

    config = load_config(str(config_path))

    assert config.version == 2
    assert config.views[0].source == "parquet"
    assert config.views[0].uri == "s3://bucket/users/*.parquet"


def test_missing_env_variable_raises(monkeypatch, tmp_path):
    monkeypatch.delenv("MISSING_SECRET", raising=False)
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          pragmas:
            - "SET secret='${env:MISSING_SECRET}'"
        views:
          - name: v1
            sql: "SELECT 1"
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "MISSING_SECRET" in str(exc.value)


def test_duplicate_view_names_rejected(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: duplicate
            sql: "SELECT 1"
          - name: duplicate
            sql: "SELECT 2"
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "Duplicate view name" in str(exc.value)


def test_view_and_attachment_field_validation(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        attachments:
          sqlite:
            - alias: legacy
        iceberg_catalogs:
          - name: missing_type
        views:
          - name: parquet_view
            source: parquet
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    message = str(exc.value).lower()
    assert "uri' for source" in message
    assert "field required" in message  # sqlite.path missing or catalog_type missing


def test_iceberg_view_requires_exclusive_fields(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: iceberg_view
            source: iceberg
            uri: "s3://warehouse/table"
            catalog: wrong
            table: foo.bar
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "either 'uri' OR both 'catalog' and 'table'" in str(exc.value)


def test_view_metadata_fields(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: meta_view
            sql: "SELECT 1"
            description: "Primary metrics view"
            tags: [core, metrics]
        """,
    )

    config = load_config(str(config_path))

    view = config.views[0]
    assert view.description == "Primary metrics view"
    assert view.tags == ["core", "metrics"]


def test_iceberg_view_catalog_reference_valid(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        iceberg_catalogs:
          - name: main_ic
            catalog_type: rest
        views:
          - name: iceberg_catalog_view
            source: iceberg
            catalog: main_ic
            table: analytics.orders
        """,
    )

    config = load_config(str(config_path))

    assert config.views[0].catalog == "main_ic"


def test_duckdb_attachment_read_only_default(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        attachments:
          duckdb:
            - alias: ref
              path: ./ref.duckdb
        views:
          - name: v1
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))

    assert len(config.attachments.duckdb) == 1
    attachment = config.attachments.duckdb[0]
    assert attachment.alias == "ref"
    assert attachment.read_only is True


def test_duckdb_attachment_read_only_explicit_false(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        attachments:
          duckdb:
            - alias: ref
              path: ./ref.duckdb
              read_only: false
        views:
          - name: v1
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))

    attachment = config.attachments.duckdb[0]
    assert attachment.read_only is False


def test_iceberg_view_catalog_reference_missing(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        iceberg_catalogs:
          - name: defined_ic
            catalog_type: rest
        views:
          - name: missing_catalog_view
            source: iceberg
            catalog: missing_ic
            table: analytics.orders
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "missing_catalog_view" in str(exc.value)
    assert "missing_ic" in str(exc.value)


def test_sql_file_path_cannot_be_empty(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: file_view
            sql_file:
              path: ""
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "sql_file.path cannot be empty" in str(exc.value)


def test_sql_template_path_cannot_be_empty(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: template_view
            sql_template:
              path: "   "
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "sql_template.path cannot be empty" in str(exc.value)


def test_duckdb_settings_single_string(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          settings: "SET threads = 32"
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))
    assert config.duckdb.settings == "SET threads = 32"


def test_duckdb_settings_list(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          settings:
            - "SET threads = 32"
            - "SET memory_limit = '1GB'"
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))
    assert config.duckdb.settings == ["SET threads = 32", "SET memory_limit = '1GB'"]


def test_duckdb_settings_with_env_interpolation(monkeypatch, tmp_path):
    monkeypatch.setenv("THREAD_COUNT", "16")
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          settings: "SET threads = ${env:THREAD_COUNT}"
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))
    assert config.duckdb.settings == "SET threads = 16"


def test_duckdb_settings_empty_string(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          settings: ""
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))
    assert config.duckdb.settings is None


def test_duckdb_settings_empty_list(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          settings: []
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))
    assert config.duckdb.settings is None


def test_duckdb_settings_invalid_format_not_set(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          settings: "threads = 32"
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "Settings must be valid DuckDB SET statements" in str(exc.value)


def test_duckdb_settings_invalid_format_in_list(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          settings:
            - "SET threads = 32"
            - "memory_limit = '1GB'"
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "Settings must be valid DuckDB SET statements" in str(exc.value)


def test_duckdb_settings_no_settings(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))
    assert config.duckdb.settings is None


def test_duckdb_secrets_s3_config(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          secrets:
            - type: s3
              key_id: AKIAIOSFODNN7EXAMPLE
              secret: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
              region: us-west-2
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))
    assert len(config.duckdb.secrets) == 1
    secret = config.duckdb.secrets[0]
    assert secret.type == "s3"
    assert secret.key_id == "AKIAIOSFODNN7EXAMPLE"
    assert secret.secret == "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    assert secret.region == "us-west-2"
    assert secret.provider == "config"
    assert secret.persistent is False


def test_duckdb_secrets_azure_persistent(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          secrets:
            - type: azure
              name: azure_prod
              provider: config
              persistent: true
              scope: 'prod/'
              connection_string: DefaultEndpointsProtocol=https;AccountName=myaccount;AccountKey=mykey;EndpointSuffix=core.windows.net
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))
    assert len(config.duckdb.secrets) == 1
    secret = config.duckdb.secrets[0]
    assert secret.type == "azure"
    assert secret.name == "azure_prod"
    assert secret.provider == "config"
    assert secret.persistent is True
    assert secret.scope == "prod/"
    assert (
        secret.connection_string
        == "DefaultEndpointsProtocol=https;AccountName=myaccount;AccountKey=mykey;EndpointSuffix=core.windows.net"
    )


def test_duckdb_secrets_credential_chain(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          secrets:
            - type: s3
              name: s3_auto
              provider: credential_chain
              region: us-east-1
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))
    assert len(config.duckdb.secrets) == 1
    secret = config.duckdb.secrets[0]
    assert secret.type == "s3"
    assert secret.name == "s3_auto"
    assert secret.provider == "credential_chain"
    assert secret.region == "us-east-1"
    assert secret.key_id is None
    assert secret.secret is None


def test_duckdb_secrets_http_basic_auth(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          secrets:
            - type: http
              name: api_auth
              key_id: myusername
              secret: mypassword
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))
    assert len(config.duckdb.secrets) == 1
    secret = config.duckdb.secrets[0]
    assert secret.type == "http"
    assert secret.name == "api_auth"
    assert secret.key_id == "myusername"
    assert secret.secret == "mypassword"


def test_duckdb_secrets_postgres_connection_string(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          secrets:
            - type: postgres
              name: pg_prod
              connection_string: postgresql://user:password@localhost:5432/mydb
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))
    assert len(config.duckdb.secrets) == 1
    secret = config.duckdb.secrets[0]
    assert secret.type == "postgres"
    assert secret.name == "pg_prod"
    assert secret.connection_string == "postgresql://user:password@localhost:5432/mydb"


def test_duckdb_secrets_with_env_interpolation(monkeypatch, tmp_path):
    monkeypatch.setenv("AWS_ACCESS_KEY", "AKIA123")
    monkeypatch.setenv("AWS_SECRET_KEY", "secret123")
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          secrets:
            - type: s3
              key_id: ${env:AWS_ACCESS_KEY}
              secret: ${env:AWS_SECRET_KEY}
              region: us-west-2
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))
    assert len(config.duckdb.secrets) == 1
    secret = config.duckdb.secrets[0]
    assert secret.key_id == "AKIA123"
    assert secret.secret == "secret123"


def test_duckdb_secrets_validation_s3_missing_fields(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          secrets:
            - type: s3
              key_id: AKIAIOSFODNN7EXAMPLE
              # Missing secret field
              region: us-west-2
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "S3 config provider requires key_id and secret" in str(exc.value)


def test_duckdb_secrets_validation_azure_missing_fields(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          secrets:
            - type: azure
              # Missing connection_string or tenant_id + account_name
              account_name: myaccount
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert (
        "Azure config provider requires connection_string or (tenant_id and account_name)"
        in str(exc.value)
    )


def test_duckdb_secrets_validation_http_missing_fields(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          secrets:
            - type: http
              key_id: myusername
              # Missing secret field
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "HTTP secret requires key_id (username) and secret (password)" in str(
        exc.value
    )


def test_duckdb_secrets_empty_secrets(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          secrets: []
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))
    assert config.duckdb.secrets == []


def test_duckdb_secrets_no_secrets(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))
    assert config.duckdb.secrets == []


def test_semantic_models_basic_config(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: sales_data
            sql: "SELECT * FROM sales"
        semantic_models:
          - name: sales_analytics
            base_view: sales_data
            label: "Sales Analytics"
            description: "Business metrics for sales analysis"
            tags: ["sales", "revenue"]
            dimensions:
              - name: order_date
                expression: "created_at::date"
                label: "Order Date"
                type: "date"
              - name: customer_region
                expression: "UPPER(customer_region)"
                label: "Customer Region"
                type: "string"
            measures:
              - name: total_revenue
                expression: "SUM(amount)"
                label: "Total Revenue"
                type: "number"
              - name: order_count
                expression: "COUNT(*)"
                label: "Order Count"
                type: "number"
        """,
    )

    config = load_config(str(config_path))

    assert len(config.semantic_models) == 1
    semantic_model = config.semantic_models[0]
    assert semantic_model.name == "sales_analytics"
    assert semantic_model.base_view == "sales_data"
    assert semantic_model.label == "Sales Analytics"
    assert semantic_model.description == "Business metrics for sales analysis"
    assert semantic_model.tags == ["sales", "revenue"]

    # Check dimensions
    assert len(semantic_model.dimensions) == 2
    order_date = semantic_model.dimensions[0]
    assert order_date.name == "order_date"
    assert order_date.expression == "created_at::date"
    assert order_date.label == "Order Date"
    assert order_date.type == "date"

    customer_region = semantic_model.dimensions[1]
    assert customer_region.name == "customer_region"
    assert customer_region.expression == "UPPER(customer_region)"
    assert customer_region.label == "Customer Region"
    assert customer_region.type == "string"

    # Check measures
    assert len(semantic_model.measures) == 2
    total_revenue = semantic_model.measures[0]
    assert total_revenue.name == "total_revenue"
    assert total_revenue.expression == "SUM(amount)"
    assert total_revenue.label == "Total Revenue"
    assert total_revenue.type == "number"

    order_count = semantic_model.measures[1]
    assert order_count.name == "order_count"
    assert order_count.expression == "COUNT(*)"
    assert order_count.label == "Order Count"
    assert order_count.type == "number"


def test_semantic_models_minimal_config(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: users
            sql: "SELECT * FROM users"
        semantic_models:
          - name: user_analytics
            base_view: users
        """,
    )

    config = load_config(str(config_path))

    assert len(config.semantic_models) == 1
    semantic_model = config.semantic_models[0]
    assert semantic_model.name == "user_analytics"
    assert semantic_model.base_view == "users"
    assert semantic_model.label is None
    assert semantic_model.description is None
    assert semantic_model.tags == []
    assert semantic_model.dimensions == []
    assert semantic_model.measures == []


def test_semantic_models_empty_list(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: test_view
            sql: "SELECT 1"
        semantic_models: []
        """,
    )

    config = load_config(str(config_path))
    assert config.semantic_models == []


def test_semantic_models_no_section(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))
    assert config.semantic_models == []


def test_semantic_models_duplicate_names_rejected(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: view1
            sql: "SELECT 1"
          - name: view2
            sql: "SELECT 2"
        semantic_models:
          - name: duplicate_model
            base_view: view1
          - name: duplicate_model
            base_view: view2
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "Duplicate semantic model name" in str(exc.value)
    assert "duplicate_model" in str(exc.value)


def test_semantic_models_missing_base_view_rejected(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: existing_view
            sql: "SELECT 1"
        semantic_models:
          - name: broken_model
            base_view: missing_view
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "reference undefined base view" in str(exc.value)
    assert "broken_model -> missing_view" in str(exc.value)


def test_semantic_models_duplicate_dimension_names_rejected(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: test_view
            sql: "SELECT 1"
        semantic_models:
          - name: test_model
            base_view: test_view
            dimensions:
              - name: duplicate_dim
                expression: "col1"
              - name: duplicate_dim
                expression: "col2"
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "Duplicate dimension name" in str(exc.value)
    assert "duplicate_dim" in str(exc.value)


def test_semantic_models_duplicate_measure_names_rejected(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: test_view
            sql: "SELECT 1"
        semantic_models:
          - name: test_model
            base_view: test_view
            measures:
              - name: duplicate_measure
                expression: "SUM(col1)"
              - name: duplicate_measure
                expression: "SUM(col2)"
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "Duplicate measure name" in str(exc.value)
    assert "duplicate_measure" in str(exc.value)


def test_semantic_models_dimension_measure_name_conflict_rejected(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: test_view
            sql: "SELECT 1"
        semantic_models:
          - name: test_model
            base_view: test_view
            dimensions:
              - name: conflict_name
                expression: "col1"
            measures:
              - name: conflict_name
                expression: "SUM(col2)"
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "Dimension and measure name(s) conflict" in str(exc.value)
    assert "conflict_name" in str(exc.value)


def test_semantic_models_empty_name_rejected(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: test_view
            sql: "SELECT 1"
        semantic_models:
          - name: ""
            base_view: test_view
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "Semantic model name cannot be empty" in str(exc.value)


def test_semantic_models_empty_base_view_rejected(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: test_view
            sql: "SELECT 1"
        semantic_models:
          - name: test_model
            base_view: ""
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "Base view cannot be empty" in str(exc.value)


def test_semantic_models_empty_dimension_name_rejected(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: test_view
            sql: "SELECT 1"
        semantic_models:
          - name: test_model
            base_view: test_view
            dimensions:
              - name: ""
                expression: "col1"
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "Dimension name cannot be empty" in str(exc.value)


def test_semantic_models_empty_dimension_expression_rejected(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: test_view
            sql: "SELECT 1"
        semantic_models:
          - name: test_model
            base_view: test_view
            dimensions:
              - name: test_dim
                expression: ""
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "Dimension expression cannot be empty" in str(exc.value)


def test_semantic_models_empty_measure_name_rejected(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: test_view
            sql: "SELECT 1"
        semantic_models:
          - name: test_model
            base_view: test_view
            measures:
              - name: ""
                expression: "SUM(col1)"
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "Measure name cannot be empty" in str(exc.value)


def test_semantic_models_empty_measure_expression_rejected(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: test_view
            sql: "SELECT 1"
        semantic_models:
          - name: test_model
            base_view: test_view
            measures:
              - name: test_measure
                expression: ""
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "Measure expression cannot be empty" in str(exc.value)


def test_semantic_models_with_env_interpolation(monkeypatch, tmp_path):
    monkeypatch.setenv("SALES_VIEW_NAME", "sales_data")
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: sales_data
            sql: "SELECT * FROM sales"
        semantic_models:
          - name: sales_analytics
            base_view: ${env:SALES_VIEW_NAME}
            dimensions:
              - name: order_date
                expression: "created_at::date"
        """,
    )

    config = load_config(str(config_path))

    assert len(config.semantic_models) == 1
    semantic_model = config.semantic_models[0]
    assert semantic_model.name == "sales_analytics"
    assert semantic_model.base_view == "sales_data"


def test_semantic_models_python_api_access(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: sales_data
            sql: "SELECT * FROM sales"
          - name: user_data
            sql: "SELECT * FROM users"
        semantic_models:
          - name: sales_analytics
            base_view: sales_data
            dimensions:
              - name: order_date
                expression: "created_at::date"
            measures:
              - name: total_revenue
                expression: "SUM(amount)"
          - name: user_analytics
            base_view: user_data
            dimensions:
              - name: user_type
                expression: "user_type"
        """,
    )

    config = load_config(str(config_path))

    # Test accessing semantic models via Python API
    assert len(config.semantic_models) == 2

    # Find specific semantic models
    sales_model = next(
        (sm for sm in config.semantic_models if sm.name == "sales_analytics"), None
    )
    assert sales_model is not None
    assert sales_model.base_view == "sales_data"
    assert len(sales_model.dimensions) == 1
    assert len(sales_model.measures) == 1

    user_model = next(
        (sm for sm in config.semantic_models if sm.name == "user_analytics"), None
    )
    assert user_model is not None
    assert user_model.base_view == "user_data"
    assert len(user_model.dimensions) == 1
    assert len(user_model.measures) == 0


# Semantic Layer v2 Tests


def test_semantic_models_v2_with_joins_and_time_dimensions(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: sales_data
            sql: "SELECT * FROM sales"
          - name: customers
            sql: "SELECT * FROM customer_dim"
          - name: products
            sql: "SELECT * FROM product_dim"
        semantic_models:
          - name: sales_analytics
            base_view: sales_data
            label: "Sales Analytics"
            description: "Business metrics for sales analysis"
            joins:
              - to_view: customers
                type: left
                on_condition: "sales.customer_id = customers.id"
              - to_view: products
                type: left
                on_condition: "sales.product_id = products.id"
            dimensions:
              - name: order_date
                expression: "created_at"
                type: "time"
                time_grains: ["year", "quarter", "month", "day"]
                label: "Order Date"
              - name: customer_region
                expression: "customers.region"
                type: "string"
                label: "Customer Region"
              - name: product_category
                expression: "products.category"
                type: "string"
                label: "Product Category"
            measures:
              - name: total_revenue
                expression: "SUM(sales.amount)"
                label: "Total Revenue"
                type: "number"
              - name: order_count
                expression: "COUNT(DISTINCT sales.id)"
                label: "Order Count"
                type: "number"
            defaults:
              time_dimension: order_date
              primary_measure: total_revenue
              default_filters:
                - dimension: customer_region
                  operator: "="
                  value: "NORTH AMERICA"
        """,
    )

    config = load_config(str(config_path))

    assert len(config.semantic_models) == 1
    semantic_model = config.semantic_models[0]
    assert semantic_model.name == "sales_analytics"
    assert semantic_model.base_view == "sales_data"

    # Test joins
    assert len(semantic_model.joins) == 2
    join1 = semantic_model.joins[0]
    assert join1.to_view == "customers"
    assert join1.type == "left"
    assert join1.on_condition == "sales.customer_id = customers.id"

    join2 = semantic_model.joins[1]
    assert join2.to_view == "products"
    assert join2.type == "left"
    assert join2.on_condition == "sales.product_id = products.id"

    # Test dimensions with time grains
    assert len(semantic_model.dimensions) == 3
    time_dim = next(
        dim for dim in semantic_model.dimensions if dim.name == "order_date"
    )
    assert time_dim.type == "time"
    assert time_dim.time_grains == ["year", "quarter", "month", "day"]

    # Test defaults
    assert semantic_model.defaults is not None
    assert semantic_model.defaults.time_dimension == "order_date"
    assert semantic_model.defaults.primary_measure == "total_revenue"
    assert len(semantic_model.defaults.default_filters) == 1
    assert semantic_model.defaults.default_filters[0]["dimension"] == "customer_region"


def test_semantic_models_v2_invalid_join_type_rejected(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: sales_data
            sql: "SELECT * FROM sales"
          - name: customers
            sql: "SELECT * FROM customers"
        semantic_models:
          - name: sales_analytics
            base_view: sales_data
            joins:
              - to_view: customers
                type: invalid_join_type
                on_condition: "sales.customer_id = customers.id"
        """,
    )

    with pytest.raises(ConfigError, match="Invalid join type 'invalid_join_type'"):
        load_config(str(config_path))


def test_semantic_models_v2_time_grains_only_for_time_dimensions(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: sales_data
            sql: "SELECT * FROM sales"
        semantic_models:
          - name: sales_analytics
            base_view: sales_data
            dimensions:
              - name: customer_region
                expression: "customer_region"
                type: "string"
                time_grains: ["year", "month"]
        """,
    )

    with pytest.raises(
        ConfigError, match="time_grains can only be specified for time dimensions"
    ):
        load_config(str(config_path))


def test_semantic_models_v2_invalid_time_grain_rejected(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: sales_data
            sql: "SELECT * FROM sales"
        semantic_models:
          - name: sales_analytics
            base_view: sales_data
            dimensions:
              - name: order_date
                expression: "created_at"
                type: "time"
                time_grains: ["invalid_grain"]
        """,
    )

    with pytest.raises(ConfigError, match="Invalid time grain 'invalid_grain'"):
        load_config(str(config_path))


def test_semantic_models_v2_invalid_dimension_type_rejected(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: sales_data
            sql: "SELECT * FROM sales"
        semantic_models:
          - name: sales_analytics
            base_view: sales_data
            dimensions:
              - name: order_date
                expression: "created_at"
                type: "invalid_type"
        """,
    )

    with pytest.raises(ConfigError, match="Invalid dimension type 'invalid_type'"):
        load_config(str(config_path))


def test_semantic_models_v2_join_to_nonexistent_view_rejected(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: sales_data
            sql: "SELECT * FROM sales"
        semantic_models:
          - name: sales_analytics
            base_view: sales_data
            joins:
              - to_view: nonexistent_view
                type: left
                on_condition: "sales.id = nonexistent_view.id"
        """,
    )

    with pytest.raises(
        ConfigError,
        match="Semantic model join\\(s\\) reference undefined view\\(s\\): sales_analytics.nonexistent_view",
    ):
        load_config(str(config_path))


def test_semantic_models_v2_default_time_dimension_must_exist(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: sales_data
            sql: "SELECT * FROM sales"
        semantic_models:
          - name: sales_analytics
            base_view: sales_data
            defaults:
              time_dimension: nonexistent_dimension
        """,
    )

    with pytest.raises(
        ConfigError,
        match="Default time dimension 'nonexistent_dimension' does not exist in dimensions",
    ):
        load_config(str(config_path))


def test_semantic_models_v2_default_time_dimension_must_be_time_type(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: sales_data
            sql: "SELECT * FROM sales"
        semantic_models:
          - name: sales_analytics
            base_view: sales_data
            dimensions:
              - name: customer_region
                expression: "customer_region"
                type: "string"
            defaults:
              time_dimension: customer_region
        """,
    )

    with pytest.raises(
        ConfigError,
        match="Default time dimension 'customer_region' must have type 'time'",
    ):
        load_config(str(config_path))


def test_semantic_models_v2_default_primary_measure_must_exist(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: sales_data
            sql: "SELECT * FROM sales"
        semantic_models:
          - name: sales_analytics
            base_view: sales_data
            defaults:
              primary_measure: nonexistent_measure
        """,
    )

    with pytest.raises(
        ConfigError,
        match="Default primary measure 'nonexistent_measure' does not exist in measures",
    ):
        load_config(str(config_path))


def test_semantic_models_v2_default_filter_dimension_must_exist(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: sales_data
            sql: "SELECT * FROM sales"
        semantic_models:
          - name: sales_analytics
            base_view: sales_data
            defaults:
              default_filters:
                - dimension: nonexistent_dimension
                  operator: "="
                  value: "test"
        """,
    )

    with pytest.raises(
        ConfigError,
        match="Default filter dimension 'nonexistent_dimension' does not exist in dimensions",
    ):
        load_config(str(config_path))


def test_semantic_models_v2_empty_join_fields_rejected(tmp_path):
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: sales_data
            sql: "SELECT * FROM sales"
          - name: customers
            sql: "SELECT * FROM customers"
        semantic_models:
          - name: sales_analytics
            base_view: sales_data
            joins:
              - to_view: ""
                type: "left"
                on_condition: "sales.id = customers.id"
        """,
    )

    with pytest.raises(ConfigError, match="Join 'to_view' cannot be empty"):
        load_config(str(config_path))


def test_semantic_models_v2_backward_compatibility(tmp_path):
    # Test that v1 semantic models still work with v2 schema
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: sales_data
            sql: "SELECT * FROM sales"
        semantic_models:
          - name: sales_analytics
            base_view: sales_data
            label: "Sales Analytics"
            description: "Business metrics for sales analysis"
            dimensions:
              - name: order_date
                expression: "created_at::date"
                label: "Order Date"
              - name: customer_region
                expression: "UPPER(customer_region)"
                label: "Customer Region"
            measures:
              - name: total_revenue
                expression: "SUM(amount)"
                label: "Total Revenue"
              - name: order_count
                expression: "COUNT(*)"
                label: "Order Count"
        """,
    )

    config = load_config(str(config_path))

    assert len(config.semantic_models) == 1
    semantic_model = config.semantic_models[0]
    assert semantic_model.name == "sales_analytics"
    assert semantic_model.base_view == "sales_data"

    # V1 models should have empty joins and None defaults
    assert len(semantic_model.joins) == 0
    assert semantic_model.defaults is None

    # Original dimensions and measures should work
    assert len(semantic_model.dimensions) == 2
    assert len(semantic_model.measures) == 2


def test_load_config_filesystem_parameter_backward_compatibility(tmp_path):
    """Test that filesystem parameter doesn't break local config loading."""
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    # Test without filesystem parameter (should still work)
    config1 = load_config(str(config_path))
    assert config1.version == 1
    assert len(config1.views) == 1

    # Test with None filesystem parameter (should still work)
    config2 = load_config(str(config_path), filesystem=None)
    assert config2.version == 1
    assert len(config2.views) == 1

    # Test that they produce the same result
    assert config1.views[0].name == config2.views[0].name


def test_load_config_filesystem_parameter_validation():
    """Test filesystem parameter type validation."""
    config_path = "s3://bucket/config.yaml"

    # Test with invalid filesystem parameter
    with pytest.raises((TypeError, ValueError)):
        load_config(config_path, filesystem="not_a_filesystem")  # type: ignore

    with pytest.raises((TypeError, ValueError)):
        load_config(config_path, filesystem=123)  # type: ignore


def test_duckalog_attachment_validation(tmp_path):
    """Test DuckalogAttachment validation."""
    # Test missing alias
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        attachments:
          duckalog:
            - config_path: child.yaml
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    with pytest.raises(Exception) as exc:
        load_config(str(config_path))
    assert "alias" in str(exc.value).lower()


def test_duckalog_attachment_validation_empty_config_path(tmp_path):
    """Test DuckalogAttachment with empty config_path."""
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        attachments:
          duckalog:
            - alias: child
              config_path: ""
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    with pytest.raises(Exception) as exc:
        load_config(str(config_path))
    assert "config_path" in str(exc.value).lower() or "empty" in str(exc.value).lower()


def test_duckalog_attachment_validation_empty_alias(tmp_path):
    """Test DuckalogAttachment with empty alias."""
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        attachments:
          duckalog:
            - alias: ""
              config_path: child.yaml
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    with pytest.raises(Exception) as exc:
        load_config(str(config_path))
    assert "alias" in str(exc.value).lower() or "empty" in str(exc.value).lower()


def test_duckalog_attachment_path_resolution(tmp_path):
    """Test path resolution for Duckalog attachments."""
    child_config_path = _write(
        tmp_path / "child.yaml",
        """
        version: 1
        duckdb:
          database: child.duckdb
        views:
          - name: child_view
            sql: "SELECT 1"
        """,
    )

    config_path = _write(
        tmp_path / "catalog.yaml",
        f"""
        version: 1
        duckdb:
          database: catalog.duckdb
        attachments:
          duckalog:
            - alias: child_catalog
              config_path: ./child.yaml
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))
    attachment = config.attachments.duckalog[0]
    assert attachment.config_path == str(child_config_path.resolve())


def test_duckalog_attachment_database_override_path_resolution(tmp_path):
    """Test database override path resolution for Duckalog attachments."""
    # Create override directory
    override_dir = tmp_path / "custom_databases"
    override_dir.mkdir()

    child_config_path = _write(
        tmp_path / "child.yaml",
        """
        version: 1
        duckdb:
          database: child.duckdb
        views:
          - name: child_view
            sql: "SELECT 1"
        """,
    )

    config_path = _write(
        tmp_path / "catalog.yaml",
        f"""
        version: 1
        duckdb:
          database: catalog.duckdb
        attachments:
          duckalog:
            - alias: child_catalog
              config_path: {child_config_path}
              database: ./custom_databases/overridden.duckdb
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))
    attachment = config.attachments.duckalog[0]
    assert attachment.config_path == str(child_config_path.resolve())
    assert attachment.database == str(
        (tmp_path / "custom_databases" / "overridden.duckdb").resolve()
    )


def test_load_config_delegates_to_local_helper_for_local_paths(monkeypatch, tmp_path):
    """Test that load_config delegates to _load_config_from_local_file for local paths."""
    from duckalog.config import _load_config_from_local_file

    # Mock the local helper function
    mock_local = monkeypatch.setattr(
        _load_config_from_local_file,
        "func",
        lambda *args, **kwargs: "local_config_result",
    )
    monkeypatch.setattr(
        _load_config_from_local_file, "return_value", "local_config_result"
    )

    # Write a simple config file
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    # Mock remote URI detection to return False
    def mock_is_remote_uri(uri):
        return False

    monkeypatch.setattr("duckalog.config.is_remote_uri", mock_is_remote_uri)

    # Call load_config with a local path
    result = load_config(str(config_path))

    # Should have delegated to local helper
    assert result == "local_config_result"


def test_load_config_delegates_to_remote_helper_for_remote_uris(monkeypatch, tmp_path):
    """Test that load_config delegates to load_config_from_uri for remote URIs."""
    from duckalog.remote_config import load_config_from_uri

    # Mock the remote helper function
    monkeypatch.setattr(
        load_config_from_uri, "func", lambda *args, **kwargs: "remote_config_result"
    )
    monkeypatch.setattr(load_config_from_uri, "return_value", "remote_config_result")

    # Mock remote URI detection to return True
    def mock_is_remote_uri(uri):
        return True

    monkeypatch.setattr("duckalog.config.is_remote_uri", mock_is_remote_uri)

    # Call load_config with a remote URI
    result = load_config("s3://bucket/catalog.yaml")

    # Should have delegated to remote helper
    assert result == "remote_config_result"


def test_load_config_filesystem_validation_for_local_files(tmp_path):
    """Test that load_config validates filesystem interface for local file loading."""
    from duckalog.config import _load_config_from_local_file, ConfigError

    # Write a simple config file
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    # Test with None filesystem (should work)
    config = _load_config_from_local_file(str(config_path), filesystem=None)
    assert config is not None

    # Test with invalid filesystem object (missing required methods)
    class InvalidFilesystem:
        pass

    invalid_fs = InvalidFilesystem()
    with pytest.raises(
        ConfigError, match="filesystem object must provide 'open' and 'exists' methods"
    ):
        _load_config_from_local_file(str(config_path), filesystem=invalid_fs)

    # Test with filesystem that exists but missing 'open' method
    class MissingOpenFilesystem:
        def exists(self, path):
            return True

    missing_open_fs = MissingOpenFilesystem()
    with pytest.raises(
        ConfigError, match="filesystem object must provide 'open' and 'exists' methods"
    ):
        _load_config_from_local_file(str(config_path), filesystem=missing_open_fs)

    # Test with filesystem that has both methods
    class ValidFilesystem:
        def __init__(self, base_path):
            self.base_path = base_path

        def exists(self, path):
            return True

        def open(self, path, mode="r"):
            return open(path, mode)

    valid_fs = ValidFilesystem(tmp_path)
    config = _load_config_from_local_file(str(config_path), filesystem=valid_fs)
    assert config is not None


def test_load_config_uri_detection(monkeypatch):
    """Test URI detection for load_config dispatch."""
    from duckalog.remote_config import is_remote_uri

    # Test local paths (no scheme)
    assert not is_remote_uri("catalog.yaml")
    assert not is_remote_uri("./config/catalog.yaml")
    assert not is_remote_uri("/absolute/path/catalog.yaml")
    assert not is_remote_uri("folder/catalog.yaml")

    # Test remote URIs (with schemes)
    assert is_remote_uri("s3://bucket/catalog.yaml")
    assert is_remote_uri("https://example.com/catalog.yaml")
    assert is_remote_uri("http://example.com/catalog.yaml")
    assert is_remote_uri("gcs://bucket/catalog.yaml")
    assert is_remote_uri("abfs://container/catalog.yaml")
    assert is_remote_uri("sftp://server/path/catalog.yaml")


def test_view_with_schema_field(tmp_path):
    """Test that views can have an optional db_schema field."""
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: analytics_view
            db_schema: analytics
            sql: "SELECT 1 as id"
          - name: default_view
            sql: "SELECT 2 as id"
        """,
    )

    config = load_config(str(config_path))

    assert len(config.views) == 2
    assert config.views[0].name == "analytics_view"
    assert config.views[0].db_schema == "analytics"
    assert config.views[1].name == "default_view"
    assert config.views[1].db_schema is None


def test_view_schema_field_validation(tmp_path):
    """Test that empty schema field is rejected."""
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: test_view
            db_schema: ""
            sql: "SELECT 1"
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "View db_schema cannot be empty" in str(exc.value)


def test_duplicate_schema_name_combination_rejected(tmp_path):
    """Test that duplicate (schema, name) combinations are rejected."""
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: same_name
            db_schema: same_schema
            sql: "SELECT 1"
          - name: same_name
            db_schema: same_schema
            sql: "SELECT 2"
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    assert "Duplicate view name(s) found" in str(exc.value)
    assert "same_schema.same_name" in str(exc.value)


def test_same_name_different_schemas_allowed(tmp_path):
    """Test that views with same name but different schemas are allowed."""
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: same_name
            db_schema: schema1
            sql: "SELECT 1"
          - name: same_name
            db_schema: schema2
            sql: "SELECT 2"
          - name: same_name
            sql: "SELECT 3"
        """,
    )

    config = load_config(str(config_path))

    assert len(config.views) == 3
    # Views should be distinguished by their schema
    view_schemas = [(v.name, v.db_schema) for v in config.views]
    assert ("same_name", "schema1") in view_schemas
    assert ("same_name", "schema2") in view_schemas
    assert ("same_name", None) in view_schemas


def test_semantic_model_with_schema_qualified_base_view(tmp_path):
    """Test that semantic models can reference schema-qualified base views."""
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: base_view
            db_schema: analytics
            sql: "SELECT id FROM table1"
        semantic_models:
          - name: test_model
            base_view: analytics.base_view
            dimensions:
              - name: id
                expression: id
        """,
    )

    config = load_config(str(config_path))

    assert len(config.semantic_models) == 1
    assert config.semantic_models[0].base_view == "analytics.base_view"


def test_semantic_model_with_ambiguous_view_reference(tmp_path):
    """Test that semantic models with ambiguous view references are rejected."""
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: ambiguous_view
            db_schema: schema1
            sql: "SELECT 1"
          - name: ambiguous_view
            db_schema: schema2
            sql: "SELECT 2"
        semantic_models:
          - name: test_model
            base_view: schema1.ambiguous_view
            joins:
              - to_view: ambiguous_view
                type: inner
                on_condition: "1 = 1"
            dimensions:
              - name: test
                expression: "1"
        """,
    )

    with pytest.raises(ConfigError) as exc:
        load_config(str(config_path))

    error_msg = str(exc.value)
    assert "ambiguous" in error_msg.lower()
    assert "test_model" in error_msg
    assert "ambiguous_view" in error_msg
