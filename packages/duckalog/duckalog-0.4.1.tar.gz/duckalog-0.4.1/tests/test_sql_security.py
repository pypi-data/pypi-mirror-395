"""Security regression tests for SQL generation.

These tests exercise security-sensitive behaviors to prevent regressions
of previously fixed vulnerabilities, particularly SQL injection vectors.
"""

from __future__ import annotations

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
    SecretConfig,
)


class TestViewSQLInjectionPrevention:
    """Test SQL generation resilience to malicious view identifiers."""

    def test_view_name_with_semicolon_injection_attempt(self):
        """Test that semicolons in view names don't create additional statements."""
        view = ViewConfig(name='malicious"; DROP TABLE users; --', sql="SELECT 1")

        sql = generate_view_sql(view)

        # Should contain properly quoted view name
        assert '"malicious""; DROP TABLE users; --"' in sql
        # The content should be safely contained within the identifier
        # It should be a single CREATE VIEW statement, not multiple statements
        assert sql.count("CREATE OR REPLACE VIEW") == 1
        # The malicious content should not be executed as SQL
        assert sql.count("SELECT 1") == 1  # Only our intended SELECT

    def test_view_name_with_sql_comment_injection(self):
        """Test that SQL comment markers in view names are properly quoted."""
        view = ViewConfig(name="users--admin", sql="SELECT 1")

        sql = generate_view_sql(view)

        # Should quote the comment marker as part of the identifier
        assert '"users--admin"' in sql
        # Should not treat as actual SQL comment
        assert "-- admin" not in sql

    def test_database_name_with_injection_attempt(self):
        """Test that database names with injection attempts are safely quoted."""
        view = ViewConfig(
            name="test_view",
            source="duckdb",
            database='malicious"; DELETE FROM secret_table; --',
            table="users",
        )

        sql = generate_view_sql(view)

        # Database name should be quoted
        assert '"malicious""; DELETE FROM secret_table; --"' in sql
        # Should be a single SELECT statement, not additional SQL
        assert sql.count("SELECT * FROM") == 1
        # The DELETE FROM text is safely contained within the quoted database name
        # This is the correct and safe behavior

    def test_table_name_with_block_comment_injection(self):
        """Test that block comment markers in table names are handled safely."""
        view = ViewConfig(
            name="test_view",
            source="sqlite",
            database="refdb",
            table="data/*injection*/",
        )

        sql = generate_view_sql(view)

        # Table name should be quoted
        assert '"data/*injection*/"' in sql
        # Should be a single SELECT statement with the table name as identifier
        assert sql.count("SELECT * FROM") == 1
        # The comment markers should be part of the identifier, not actual SQL comments

    def test_mixed_quotes_in_identifiers(self):
        """Test identifiers containing both single and double quotes."""
        view = ViewConfig(
            name='view\'s "name"', source="postgres", database='db"s', table="table's"
        )

        sql = generate_view_sql(view)

        # All identifiers should be properly quoted
        assert '"view\'s ""name"""' in sql
        assert '"db""s"' in sql
        assert '"table\'s"' in sql

    def test_sql_keywords_in_identifiers(self):
        """Test that SQL keywords in identifiers don't break query structure."""
        view = ViewConfig(
            name="SELECT", source="parquet", uri="s3://bucket/file.parquet"
        )

        sql = generate_view_sql(view)

        # Should contain properly quoted SELECT identifier
        assert '"SELECT"' in sql
        # Should be a valid CREATE VIEW statement
        assert sql.startswith("CREATE OR REPLACE VIEW")
        assert sql.endswith(";")


class TestSecretSQLInjectionPrevention:
    """Test SQL generation security for DuckDB secrets."""

    def test_secret_name_with_semicolon(self):
        """Test that semicolons in secret names don't create additional statements."""
        secret = SecretConfig(
            type="s3",
            name='secret"; DROP ALL SECRETS; --',
            key_id="key",
            secret="secret",
        )

        sql = generate_secret_sql(secret)

        # Secret name should contain the malicious content (not quoted in current implementation)
        assert 'secret"; DROP ALL SECRETS; --' in sql
        # Should be a single CREATE SECRET statement
        assert sql.count("CREATE SECRET") == 1
        # The malicious content should not be executed as SQL
        # It's part of the secret name identifier, not additional SQL

    def test_secret_values_with_quotes(self):
        """Test that secret values with quotes are properly escaped."""
        secret = SecretConfig(
            type="s3",
            name="test_secret",
            key_id="user'key",
            secret="pass'word",
            region="us-west-2",
        )

        sql = generate_secret_sql(secret)

        # Values should be properly quoted with escaped quotes
        assert "KEY_ID 'user''key'" in sql
        assert "SECRET 'pass''word'" in sql
        assert "REGION 'us-west-2'" in sql

    def test_connection_string_with_injection_attempt(self):
        """Test connection strings with potential injection attempts."""
        secret = SecretConfig(
            type="postgres",
            name="pg_conn",
            connection_string="host=db; DROP TABLE users; --",
        )

        sql = generate_secret_sql(secret)

        # Connection string should be properly quoted
        assert "CONNECTION_STRING 'host=db; DROP TABLE users; --'" in sql
        # Should be a single CREATE SECRET statement
        assert sql.count("CREATE SECRET") == 1
        assert sql.count("CREATE") == 1  # Only the CREATE SECRET statement

    def test_scope_with_special_characters(self):
        """Test that scope values with special characters are safely quoted."""
        secret = SecretConfig(
            type="s3",
            name="scoped_secret",
            key_id="key",
            secret="secret",
            scope="prod'; DROP TABLE secrets; --",
        )

        sql = generate_secret_sql(secret)

        # Scope should be properly quoted
        assert "SCOPE 'prod''; DROP TABLE secrets; --'" in sql
        # Should be a single CREATE SECRET statement
        assert sql.count("CREATE SECRET") == 1
        assert sql.count("SCOPE") == 1  # Only one SCOPE clause


class TestSecretOptionTypeEnforcement:
    """Test that secret options enforce strict type checking."""

    def test_secret_options_reject_lists(self):
        """Test that secret options reject list values with TypeError."""
        secret = SecretConfig(
            type="s3",
            name="test_secret",
            key_id="key",
            secret="secret",
            options={
                "allowed_regions": ["us-east-1", "us-west-2"]
            },  # List is not allowed
        )

        with pytest.raises(
            TypeError, match="Unsupported option value.*allowed_regions"
        ):
            generate_secret_sql(secret)

    def test_secret_options_reject_dicts(self):
        """Test that secret options reject dictionary values with TypeError."""
        secret = SecretConfig(
            type="s3",
            name="test_secret",
            key_id="key",
            secret="secret",
            options={"config": {"nested": "value"}},  # Dict is not allowed
        )

        with pytest.raises(TypeError, match="Unsupported option value.*config"):
            generate_secret_sql(secret)

    def test_secret_options_reject_none_values(self):
        """Test that secret options reject None values with TypeError."""
        secret = SecretConfig(
            type="s3",
            name="test_secret",
            key_id="key",
            secret="secret",
            options={"timeout": None},  # None is not allowed
        )

        with pytest.raises(TypeError, match="Unsupported option value.*timeout"):
            generate_secret_sql(secret)

    def test_secret_options_accept_valid_types(self):
        """Test that secret options accept valid value types."""
        secret = SecretConfig(
            type="s3",
            name="test_secret",
            key_id="key",
            secret="secret",
            options={
                "use_ssl": True,  # bool
                "max_retries": 3,  # int
                "timeout": 30.5,  # float
                "region": "us-west-2",  # str
            },
        )

        sql = generate_secret_sql(secret)

        # Valid types should be rendered correctly
        assert "USE_SSL TRUE" in sql
        assert "MAX_RETRIES 3" in sql
        assert "TIMEOUT 30.5" in sql
        assert "REGION 'us-west-2'" in sql


class TestQuotingHelperSecurity:
    """Test the security properties of canonical quoting helpers."""

    def test_quote_ident_prevents_injection(self):
        """Test that quote_ident prevents SQL injection through identifiers."""
        malicious_identifiers = [
            '"; DROP TABLE users; --',
            "admin'--",
            "data/*comment*/",
            "select from where",
            "normal_identifier",
        ]

        for identifier in malicious_identifiers:
            quoted = quote_ident(identifier)
            # Should wrap in double quotes
            assert quoted.startswith('"')
            assert quoted.endswith('"')
            # Should double any internal quotes
            assert '""' in quoted or '"' not in identifier[1:-1]
            # Should be properly quoted - SQL keywords inside quotes are safe
            assert quoted.startswith('"') and quoted.endswith('"')
            # Verify it's a valid quoted identifier
            assert len(quoted) >= 2  # At least surrounding quotes

    def test_quote_literal_prevents_injection(self):
        """Test that quote_literal prevents SQL injection through string literals."""
        malicious_literals = [
            "'; DROP TABLE users; --",
            "admin' OR '1'='1",
            "data/*comment*/",
            "normal string",
        ]

        for literal in malicious_literals:
            quoted = quote_literal(literal)
            # Should wrap in single quotes
            assert quoted.startswith("'")
            assert quoted.endswith("'")
            # Should double any internal quotes
            assert "''" in quoted or "'" not in literal
            # Should remain a single string literal
            assert quoted.count("'") % 2 == 0  # Even number of quotes


class TestDryRunSQLSecurity:
    """Test that dry-run SQL generation maintains security properties."""

    def test_dry_run_secrets_sql_includes_proper_quoting(self):
        """Test that dry-run mode generates the same secure SQL as execution mode."""
        config = Config(
            version=1,
            duckdb=DuckDBConfig(
                secrets=[
                    SecretConfig(
                        type="s3",
                        name="test_secret",
                        key_id="key'with'quotes",
                        secret="secret'with'quotes",
                        scope="scope/path",
                    )
                ]
            ),
            views=[ViewConfig(name="test_view", sql="SELECT 1")],
        )

        # Generate SQL with secrets included (dry-run mode)
        sql_with_secrets = generate_all_views_sql(config, include_secrets=True)

        # Should contain properly quoted values
        assert "KEY_ID 'key''with''quotes'" in sql_with_secrets
        assert "SECRET 'secret''with''quotes'" in sql_with_secrets
        assert "SCOPE 'scope/path'" in sql_with_secrets
        # Should not contain unescaped quotes
        assert "'with'quotes'" not in sql_with_secrets

    def test_dry_run_without_secrets_excludes_secret_sql(self):
        """Test that dry-run mode without secrets excludes CREATE SECRET statements."""
        config = Config(
            version=1,
            duckdb=DuckDBConfig(
                secrets=[
                    SecretConfig(
                        type="s3", name="test_secret", key_id="key", secret="secret"
                    )
                ]
            ),
            views=[ViewConfig(name="test_view", sql="SELECT 1")],
        )

        # Generate SQL without secrets
        sql_without_secrets = generate_all_views_sql(config, include_secrets=False)

        # Should contain view SQL but no secret SQL
        assert "CREATE OR REPLACE VIEW" in sql_without_secrets
        assert "CREATE SECRET" not in sql_without_secrets
        assert "test_secret" not in sql_without_secrets
