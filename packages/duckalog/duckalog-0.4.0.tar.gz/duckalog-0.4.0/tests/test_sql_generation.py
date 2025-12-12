"""SQL generation tests for Duckalog."""

from __future__ import annotations

import textwrap

import pytest

from duckalog import (
    Config,
    DuckDBConfig,
    ViewConfig,
    generate_all_views_sql,
    generate_view_sql,
    generate_secret_sql,
    quote_ident,
    quote_literal,
    render_options,
    SecretConfig,
    IcebergCatalogConfig,
)


def test_quote_ident_handles_spaces_and_quotes():
    assert quote_ident('user "events"') == '"user ""events"""'


def test_quote_literal_handles_quotes_and_special_chars():
    """Test quote_literal properly escapes single quotes and handles special characters."""
    assert quote_literal("user's data") == "'user''s data'"
    assert quote_literal("path/to/file.parquet") == "'path/to/file.parquet'"
    assert quote_literal("SELECT * FROM table") == "'SELECT * FROM table'"
    assert quote_literal("") == "''"
    assert quote_literal("multiple'quotes'here") == "'multiple''quotes''here'"


def test_quote_literal_vs_quote_ident():
    """Test that quote_literal and quote_ident handle quotes differently."""
    input_text = 'user "name"'
    assert quote_literal(input_text) == "'user \"name\"'"
    assert quote_ident(input_text) == '"user ""name"""'


def test_render_options_strict_type_checking():
    """Test that render_options enforces strict type checking for security."""
    with pytest.raises(TypeError, match="Unsupported option value"):
        render_options({"bad": [1, 2, 3]})

    with pytest.raises(TypeError, match="Unsupported option value"):
        render_options({"bad": {"nested": "dict"}})

    with pytest.raises(TypeError, match="Unsupported option value"):
        render_options({"bad": None})


def test_generate_view_sql_parquet_with_options():
    view = ViewConfig(
        name="daily users",
        source="parquet",
        uri="s3://bucket/path/*.parquet",
        options={"hive_partitioning": True, "sample_rate": 0.1},
    )

    sql = generate_view_sql(view)

    expected = textwrap.dedent(
        """
        CREATE OR REPLACE VIEW "daily users" AS
        SELECT * FROM parquet_scan('s3://bucket/path/*.parquet', hive_partitioning=TRUE, sample_rate=0.1);
        """
    ).strip()
    assert sql == expected


def test_generate_view_sql_delta_without_options():
    view = ViewConfig(
        name="events_delta",
        source="delta",
        uri="s3://delta/table",
    )

    sql = generate_view_sql(view)

    assert sql.endswith("SELECT * FROM delta_scan('s3://delta/table');")


def test_generate_view_sql_iceberg_uri_and_catalog():
    uri_view = ViewConfig(name="ic_uri", source="iceberg", uri="s3://warehouse/table")

    catalog_view = ViewConfig(
        name="ic_catalog",
        source="iceberg",
        catalog="main",
        table="analytics.orders",
        options={"snapshot_id": 42},
    )

    sql_uri = generate_view_sql(uri_view)
    sql_catalog = generate_view_sql(catalog_view)

    assert "iceberg_scan('s3://warehouse/table')" in sql_uri
    assert "iceberg_scan('main', 'analytics.orders', snapshot_id=42)" in sql_catalog


def test_generate_view_sql_attachment_sources():
    for source in ("duckdb", "sqlite", "postgres"):
        view = ViewConfig(
            name=f"{source}_view", source=source, database="refdb", table="public.users"
        )
        sql = generate_view_sql(view)
        assert sql.endswith('SELECT * FROM "refdb"."public.users";')


def test_generate_view_sql_injection_prevention():
    """Test that SQL injection via database/table names is prevented."""
    # Attempt SQL injection through database name
    malicious_db = '"; DROP TABLE users; --'
    malicious_table = '"; INSERT INTO users VALUES (1); --'

    view = ViewConfig(
        name="test_view",
        source="duckdb",
        database=malicious_db,
        table=malicious_table,
    )

    sql = generate_view_sql(view)

    # The SQL should contain properly quoted identifiers, not injected SQL
    expected_db = malicious_db.replace('"', '""')
    expected_table = malicious_table.replace('"', '""')
    expected = f'SELECT * FROM "{expected_db}"."{expected_table}"'
    assert expected in sql
    # The malicious content should be safely contained within quoted identifiers
    # It should NOT be executed as actual SQL statements
    assert sql.count("CREATE OR REPLACE VIEW") == 1  # Only our intended CREATE VIEW
    assert sql.count("SELECT * FROM") == 1  # Only our intended SELECT


def test_generate_view_sql_special_characters_in_identifiers():
    """Test that special characters in identifiers are properly handled."""
    view = ViewConfig(
        name="test view",  # space in name
        source="sqlite",
        database='db with "quotes"',  # quotes in database
        table="table; DROP TABLE other;",  # semicolon in table
    )

    sql = generate_view_sql(view)

    # Verify proper quoting without SQL injection
    assert '"test view"' in sql  # quoted view name
    assert '"db with ""quotes"""' in sql  # quoted database with escaped quotes
    assert '"table; DROP TABLE other;"' in sql  # quoted table with escaped content
    # The malicious content should be safely contained within quoted identifiers
    assert sql.count("CREATE OR REPLACE VIEW") == 1  # Only our intended CREATE VIEW
    assert sql.count("SELECT * FROM") == 1  # Only our intended SELECT


def test_generate_view_sql_raw_sql_preserves_body():
    view = ViewConfig(name="vip", sql="SELECT * FROM base WHERE is_vip")

    sql = generate_view_sql(view)

    assert "SELECT * FROM base WHERE is_vip" in sql
    assert sql.startswith('CREATE OR REPLACE VIEW "vip"')


def test_generate_view_sql_ignores_metadata():
    view = ViewConfig(
        name="meta",
        sql="SELECT 1",
        description="A descriptive view",
        tags=["core", "reporting"],
    )

    sql = generate_view_sql(view)

    expected = textwrap.dedent(
        """
        CREATE OR REPLACE VIEW "meta" AS
        SELECT 1;
        """
    ).strip()
    assert sql.strip() == expected


def test_generate_all_views_sql_header_and_order():
    config = Config(
        version=3,
        duckdb=DuckDBConfig(database="catalog.duckdb"),
        views=[
            ViewConfig(name="first", sql="SELECT 1"),
            ViewConfig(name="second", source="delta", uri="s3://delta/second"),
        ],
    )

    sql = generate_all_views_sql(config)

    expected = textwrap.dedent(
        """
        -- Generated by Duckalog
        -- Config version: 3

        CREATE OR REPLACE VIEW "first" AS
        SELECT 1;

        CREATE OR REPLACE VIEW "second" AS
        SELECT * FROM delta_scan('s3://delta/second');
        """
    ).strip()

    assert sql == expected


# Secret SQL generation tests


def test_generate_secret_sql_s3_with_config_provider():
    """Test S3 secret with config provider generates correct SQL."""
    secret = SecretConfig(
        type="s3",
        name="prod_s3",
        provider="config",
        key_id="AKIA123",
        secret="secret456",
        region="us-west-2",
    )

    sql = generate_secret_sql(secret)

    expected = "CREATE SECRET prod_s3 (TYPE S3, KEY_ID 'AKIA123', SECRET 'secret456', REGION 'us-west-2')"
    assert sql == expected


def test_generate_secret_sql_s3_persistent():
    """Test persistent S3 secret generates correct SQL."""
    secret = SecretConfig(
        type="s3",
        name="prod_s3",
        provider="config",
        key_id="AKIA123",
        secret="secret456",
        persistent=True,
    )

    sql = generate_secret_sql(secret)

    expected = "CREATE PERSISTENT SECRET prod_s3 (TYPE S3, KEY_ID 'AKIA123', SECRET 'secret456')"
    assert sql == expected


def test_generate_secret_sql_s3_with_scope():
    """Test S3 secret with scope generates correct SQL."""
    secret = SecretConfig(
        type="s3",
        name="scoped_s3",
        provider="config",
        key_id="AKIA123",
        secret="secret456",
        scope="prod/",
    )

    sql = generate_secret_sql(secret)

    expected = "CREATE SECRET scoped_s3 (TYPE S3, KEY_ID 'AKIA123', SECRET 'secret456'); SCOPE 'prod/'"
    assert sql == expected


def test_generate_secret_sql_s3_credential_chain():
    """Test S3 secret with credential_chain provider generates correct SQL."""
    secret = SecretConfig(
        type="s3", name="auto_s3", provider="credential_chain", region="us-east-1"
    )

    sql = generate_secret_sql(secret)

    expected = (
        "CREATE SECRET auto_s3 (TYPE S3, PROVIDER credential_chain, REGION 'us-east-1')"
    )
    assert sql == expected


def test_generate_secret_sql_azure_connection_string():
    """Test Azure secret with connection string generates correct SQL."""
    secret = SecretConfig(
        type="azure",
        name="azure_prod",
        connection_string="DefaultEndpointsProtocol=https;AccountName=test;AccountKey=test",
    )

    sql = generate_secret_sql(secret)

    expected = "CREATE SECRET azure_prod (TYPE AZURE, CONNECTION_STRING 'DefaultEndpointsProtocol=https;AccountName=test;AccountKey=test')"
    assert sql == expected


def test_generate_secret_sql_azure_individual_params():
    """Test Azure secret with individual parameters generates correct SQL."""
    secret = SecretConfig(
        type="azure",
        name="azure_prod",
        tenant_id="tenant123",
        account_name="myaccount",
        secret="mysecret",
    )

    sql = generate_secret_sql(secret)

    expected = "CREATE SECRET azure_prod (TYPE AZURE, TENANT_ID 'tenant123', SECRET 'mysecret', ACCOUNT_NAME 'myaccount')"
    assert sql == expected


def test_generate_secret_sql_postgres_connection_string():
    """Test PostgreSQL secret with connection string generates correct SQL."""
    secret = SecretConfig(
        type="postgres",
        name="pg_prod",
        connection_string="postgresql://user:password@localhost:5432/mydb",
    )

    sql = generate_secret_sql(secret)

    expected = "CREATE SECRET pg_prod (TYPE POSTGRES, CONNECTION_STRING 'postgresql://user:password@localhost:5432/mydb')"
    assert sql == expected


def test_generate_secret_sql_postgres_individual_params():
    """Test PostgreSQL secret with individual parameters generates correct SQL."""
    secret = SecretConfig(
        type="postgres",
        name="pg_prod",
        host="localhost",
        port=5432,
        database="analytics",
        key_id="user",
        secret="password",
    )

    sql = generate_secret_sql(secret)

    expected = "CREATE SECRET pg_prod (TYPE POSTGRES, HOST 'localhost', PORT 5432, DATABASE 'analytics', USER 'user', PASSWORD 'password')"
    assert sql == expected


def test_generate_secret_sql_http_basic_auth():
    """Test HTTP secret for basic auth generates correct SQL."""
    secret = SecretConfig(
        type="http", name="api_auth", key_id="myusername", secret="mypassword"
    )

    sql = generate_secret_sql(secret)

    expected = "CREATE SECRET api_auth (TYPE HTTP, USERNAME 'myusername', PASSWORD 'mypassword')"
    assert sql == expected


def test_generate_secret_sql_with_options():
    """Test secret with options generates correct SQL."""
    secret = SecretConfig(
        type="s3",
        name="test_s3",
        provider="config",
        key_id="AKIA123",
        secret="secret456",
        options={"url_style": "path", "use_ssl": True},
    )

    sql = generate_secret_sql(secret)

    assert "CREATE SECRET test_s3" in sql
    assert "TYPE S3" in sql
    assert "KEY_ID 'AKIA123'" in sql
    assert "SECRET 'secret456'" in sql
    assert "URL_STYLE 'path'" in sql
    assert "USE_SSL TRUE" in sql


def test_generate_secret_sql_options_strict_typing():
    """Test that secret options enforce strict type checking."""
    # Test with unsupported type - should raise TypeError
    with pytest.raises(TypeError, match="Unsupported option value"):
        secret = SecretConfig(
            type="s3",
            name="test_s3",
            provider="config",
            key_id="AKIA123",
            secret="secret456",
            options={"bad_option": [1, 2, 3]},  # list is not allowed
        )
        generate_secret_sql(secret)

    with pytest.raises(TypeError, match="Unsupported option value"):
        secret = SecretConfig(
            type="s3",
            name="test_s3",
            provider="config",
            key_id="AKIA123",
            secret="secret456",
            options={"bad_option": {"nested": "dict"}},  # dict is not allowed
        )
        generate_secret_sql(secret)


def test_generate_secret_sql_with_quotes_in_values():
    """Test that quotes in secret values are properly escaped."""
    secret = SecretConfig(
        type="s3",
        name="test_s3",
        provider="config",
        key_id="user's key",  # contains single quote
        secret="secret'with'quotes",  # contains single quotes
        region="us-west-2",
    )

    sql = generate_secret_sql(secret)

    # Verify proper escaping of single quotes
    assert "KEY_ID 'user''s key'" in sql
    assert "SECRET 'secret''with''quotes'" in sql
    assert "REGION 'us-west-2'" in sql


def test_generate_secret_sql_connection_string_quotes():
    """Test that connection strings with quotes are properly handled."""
    secret = SecretConfig(
        type="postgres",
        name="pg_conn",
        connection_string="postgresql://user:pass'word@localhost:5432/db",  # quote in password
    )

    sql = generate_secret_sql(secret)

    # Verify proper escaping
    assert "CONNECTION_STRING 'postgresql://user:pass''word@localhost:5432/db'" in sql


def test_generate_secret_sql_scope_quoting():
    """Test that scope values are properly quoted."""
    secret = SecretConfig(
        type="s3",
        name="scoped_s3",
        provider="config",
        key_id="AKIA123",
        secret="secret456",
        scope="prod/env'1",  # scope with quote
    )

    sql = generate_secret_sql(secret)

    # Verify scope is properly quoted
    assert "SCOPE 'prod/env''1'" in sql


def test_generate_secret_sql_default_name():
    """Test secret with no name uses type as name."""
    secret = SecretConfig(
        type="s3", provider="config", key_id="AKIA123", secret="secret456"
    )

    sql = generate_secret_sql(secret)

    expected = "CREATE SECRET s3 (TYPE S3, KEY_ID 'AKIA123', SECRET 'secret456')"
    assert sql == expected


def test_generate_view_sql_with_schema():
    """Test that generate_view_sql produces schema-qualified identifiers when db_schema is provided."""
    view = ViewConfig(
        name="test_view", db_schema="analytics", sql="SELECT * FROM table"
    )

    sql = generate_view_sql(view)

    # Should produce schema-qualified view name
    expected = 'CREATE OR REPLACE VIEW "analytics"."test_view" AS\nSELECT * FROM table;'
    assert sql == expected


def test_generate_view_sql_without_schema():
    """Test that generate_view_sql produces unqualified identifiers when db_schema is None."""
    view = ViewConfig(name="test_view", sql="SELECT * FROM table")

    sql = generate_view_sql(view)

    # Should produce unqualified view name
    expected = 'CREATE OR REPLACE VIEW "test_view" AS\nSELECT * FROM table;'
    assert sql == expected


def test_generate_view_sql_with_special_characters_in_schema():
    """Test that view names with special characters in both schema and name are properly quoted."""
    view = ViewConfig(
        name='user "events"', db_schema="my schema", sql="SELECT * FROM table"
    )

    sql = generate_view_sql(view)

    # Both schema and name should be properly quoted
    expected = (
        'CREATE OR REPLACE VIEW "my schema"."user ""events""" AS\nSELECT * FROM table;'
    )
    assert sql == expected


def test_generate_all_views_sql_with_mixed_schemas():
    """Test that generate_all_views_sql handles views with and without schemas correctly."""
    config = Config(
        version=1,
        duckdb=DuckDBConfig(),
        views=[
            ViewConfig(name="view_with_schema", db_schema="analytics", sql="SELECT 1"),
            ViewConfig(name="view_without_schema", sql="SELECT 2"),
            ViewConfig(
                name="another_with_schema", db_schema="reporting", sql="SELECT 3"
            ),
        ],
    )

    sql = generate_all_views_sql(config)

    lines = sql.split("\n")

    # Check that schema-qualified and unqualified views are handled correctly
    assert '"analytics"."view_with_schema"' in sql
    assert '"view_without_schema"' in sql
    assert '"reporting"."another_with_schema"' in sql

    # Should have CREATE OR REPLACE VIEW statements for each
    create_statements = [
        line for line in lines if line.startswith("CREATE OR REPLACE VIEW")
    ]
    assert len(create_statements) == 3


def test_generate_all_views_sql_parquet_source_with_schema():
    """Test SQL generation for parquet source views with schema qualification."""
    config = Config(
        version=1,
        duckdb=DuckDBConfig(),
        views=[
            ViewConfig(
                name="parquet_view",
                db_schema="data",
                source="parquet",
                uri="s3://bucket/file.parquet",
            ),
        ],
    )

    sql = generate_all_views_sql(config)

    expected_view_name = '"data"."parquet_view"'
    assert expected_view_name in sql
    assert "CREATE OR REPLACE VIEW" in sql
    assert "parquet_scan" in sql
    assert "s3://bucket/file.parquet" in sql


def test_generate_all_views_sql_iceberg_source_with_schema():
    """Test SQL generation for iceberg source views with schema qualification."""
    config = Config(
        version=1,
        duckdb=DuckDBConfig(),
        views=[
            ViewConfig(
                name="iceberg_view",
                db_schema="warehouse",
                source="iceberg",
                catalog="prod_catalog",
                table="sales",
            ),
        ],
        iceberg_catalogs=[
            IcebergCatalogConfig(name="prod_catalog", catalog_type="rest"),
        ],
    )

    sql = generate_all_views_sql(config)

    expected_view_name = '"warehouse"."iceberg_view"'
    assert expected_view_name in sql
    assert "CREATE OR REPLACE VIEW" in sql
    assert "iceberg_scan" in sql
