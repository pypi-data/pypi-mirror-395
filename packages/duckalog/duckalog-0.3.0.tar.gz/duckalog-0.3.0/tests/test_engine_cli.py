"""Engine and CLI tests for Duckalog."""

from __future__ import annotations

import logging
import textwrap
from pathlib import Path

import duckdb
import pytest

from duckalog import (
    ConfigError,
    EngineError,
    build_catalog,
    generate_sql,
    validate_config,
)
from duckalog.cli import app
from typer.testing import CliRunner


def _write_config(path: Path, content: str) -> Path:
    path.write_text(textwrap.dedent(content))
    return path


def test_build_catalog_idempotent(tmp_path):
    config_path = _write_config(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: answer_view
            sql: |
              SELECT 42 AS answer
        """,
    )
    db_file = tmp_path / "out.duckdb"

    build_catalog(str(config_path), db_path=str(db_file))
    build_catalog(str(config_path), db_path=str(db_file))

    conn = duckdb.connect(str(db_file))
    rows = conn.execute("SELECT * FROM answer_view").fetchall()
    conn.close()

    assert rows == [(42,)]


def test_build_catalog_missing_iceberg_catalog(tmp_path):
    config_path = _write_config(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        iceberg_catalogs:
          - name: main_ic
            catalog_type: rest
        views:
          - name: missing_catalog_view
            source: iceberg
            catalog: other_ic
            table: analytics.orders
        """,
    )

    with pytest.raises(ConfigError):
        build_catalog(str(config_path), db_path=str(tmp_path / "out.duckdb"))


def test_build_catalog_with_duckdb_attachment(tmp_path):
    attached_path = tmp_path / "ref.duckdb"
    conn = duckdb.connect(str(attached_path))
    conn.execute("CREATE TABLE reference(id INTEGER, name TEXT)")
    conn.execute("INSERT INTO reference VALUES (1, 'X'), (2, 'Y')")
    conn.close()

    config_path = _write_config(
        tmp_path / "catalog.yaml",
        f"""
        version: 1
        duckdb:
          database: catalog.duckdb
        attachments:
          duckdb:
            - alias: refdata
              path: {attached_path}
              read_only: true
        views:
          - name: ref_view
            source: duckdb
            database: refdata
            table: reference
        """,
    )

    db_file = tmp_path / "out.duckdb"
    build_catalog(str(config_path), db_path=str(db_file))

    conn = duckdb.connect(str(db_file))
    tables = conn.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_name='ref_view'"
    ).fetchall()
    conn.close()

    assert tables == [("ref_view",)]


def test_build_catalog_dry_run_returns_sql(tmp_path):
    config_path = _write_config(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: dry_view
            sql: "SELECT 1"
        """,
    )

    sql = build_catalog(str(config_path), dry_run=True)

    assert sql is not None
    assert 'CREATE OR REPLACE VIEW "dry_view"' in sql


def test_python_api_generate_sql(tmp_path):
    config_path = _write_config(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: pyapi
            sql: "SELECT 1"
        """,
    )

    sql = generate_sql(str(config_path))

    assert 'CREATE OR REPLACE VIEW "pyapi"' in sql


def test_python_api_validate_config_errors(monkeypatch, tmp_path):
    config_path = _write_config(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: failing
            source: parquet
            uri: "${env:MISSING}"  # unresolved env var triggers ConfigError
        """,
    )

    with pytest.raises(ConfigError):
        validate_config(str(config_path))


def test_build_catalog_attachment_error(monkeypatch, tmp_path):
    from duckalog import engine as engine_module

    called = {}

    def fake_attachments(*args, **kwargs):
        called["attachments"] = True
        raise EngineError("attachment failure")

    monkeypatch.setattr(engine_module, "_setup_attachments", fake_attachments)

    config_path = _write_config(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: v1
            sql: "SELECT 1"
        """,
    )

    with pytest.raises(EngineError):
        engine_module.build_catalog(
            str(config_path), db_path=str(tmp_path / "cat.duckdb")
        )

    assert called.get("attachments")


def test_build_catalog_iceberg_error(monkeypatch, tmp_path):
    from duckalog import engine as engine_module

    def fake_iceberg(*args, **kwargs):
        raise EngineError("iceberg failure")

    monkeypatch.setattr(engine_module, "_setup_iceberg_catalogs", fake_iceberg)

    config_path = _write_config(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: v1
            sql: "SELECT 1"
        """,
    )

    with pytest.raises(EngineError):
        engine_module.build_catalog(
            str(config_path), db_path=str(tmp_path / "cat.duckdb")
        )


def test_cli_generate_sql_writes_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("catalog.yaml").write_text(
            textwrap.dedent(
                """
                version: 1
                duckdb:
                  database: catalog.duckdb
                views:
                  - name: users
                    source: parquet
                    uri: s3://bucket/path
                """
            )
        )
        result = runner.invoke(
            app, ["generate-sql", "catalog.yaml", "--output", "views.sql"]
        )
        assert result.exit_code == 0
        assert Path("views.sql").exists()
        assert "parquet_scan" in Path("views.sql").read_text()


def test_cli_validate_success_and_failure(monkeypatch):
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("valid.yaml").write_text(
            textwrap.dedent(
                """
                version: 1
                duckdb:
                  database: catalog.duckdb
                views:
                  - name: ok
                    sql: "SELECT 1"
                """
            )
        )
        Path("invalid.yaml").write_text(
            textwrap.dedent(
                """
                version: 1
                duckdb:
                  database: catalog.duckdb
                views:
                  - name: bad
                    source: parquet
                    uri: "${env:MISSING}"  # unresolved env var to trigger error
                """
            )
        )
        result = runner.invoke(app, ["validate", "valid.yaml"])
        assert result.exit_code == 0
        assert "Config is valid" in result.output

        result = runner.invoke(app, ["validate", "invalid.yaml"])
        assert result.exit_code == 2
        assert "Config error" in result.output


def test_cli_build_reports_engine_error(tmp_path):
    runner = CliRunner()
    config_text = textwrap.dedent(
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        views:
          - name: bad_view
            sql: "SELECT * FROM missing_table"
        """
    )
    config_path = tmp_path / "catalog.yaml"
    config_path.write_text(config_text)
    db_path = tmp_path / "catalog.duckdb"

    result = runner.invoke(
        app,
        ["build", str(config_path), "--db-path", str(db_path)],
    )

    assert result.exit_code == 3
    assert "Engine error" in result.output


def test_cli_build_dry_run_outputs_sql(tmp_path):
    runner = CliRunner()
    config_path = tmp_path / "catalog.yaml"
    config_path.write_text(
        textwrap.dedent(
            """
            version: 1
            duckdb:
              database: catalog.duckdb
            views:
              - name: sample
                sql: "SELECT 1"
            """
        )
    )

    result = runner.invoke(app, ["build", str(config_path), "--dry-run"])

    assert result.exit_code == 0
    assert 'CREATE OR REPLACE VIEW "sample"' in result.output


def test_cli_version_flag():
    runner = CliRunner()
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "duckalog" in result.output


def test_info_logs_redact_secrets(monkeypatch, tmp_path, caplog):
    import duckdb as duckdb_module

    class FakeConnection:
        def install_extension(self, *_args, **_kwargs):
            return None

        def load_extension(self, *_args, **_kwargs):
            return None

        def execute(self, *_args, **_kwargs):
            return None

        def close(self) -> None:  # pragma: no cover - simple stub
            return None

    monkeypatch.setattr(duckdb_module, "connect", lambda _path: FakeConnection())

    config_path = _write_config(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        attachments:
          postgres:
            - alias: analytics
              host: db.local
              port: 5432
              database: analytics
              user: analyst
              password: supersecret
        views:
          - name: secure_view
            sql: "SELECT 1"
        """,
    )

    caplog.set_level(logging.DEBUG, logger="duckalog")
    build_catalog(str(config_path), db_path=str(tmp_path / "out.duckdb"))

    assert "Attaching Postgres database" in caplog.text
    assert "***REDACTED***" in caplog.text
    assert "supersecret" not in caplog.text


def test_build_catalog_applies_settings(tmp_path):
    config_path = _write_config(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          settings:
            - "SET enable_progress_bar = false"
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    db_file = tmp_path / "out.duckdb"
    build_catalog(str(config_path), db_path=str(db_file))

    conn = duckdb.connect(str(db_file))

    # Verify that setting was applied
    progress_result = conn.execute(
        "SELECT current_setting('enable_progress_bar')"
    ).fetchone()

    conn.close()

    assert progress_result is not None and progress_result[0] is False


def test_build_catalog_applies_single_setting(tmp_path):
    config_path = _write_config(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          settings: "SET enable_progress_bar = false"
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    db_file = tmp_path / "out.duckdb"
    build_catalog(str(config_path), db_path=str(db_file))

    conn = duckdb.connect(str(db_file))

    # Verify that setting was applied
    result = conn.execute("SELECT current_setting('enable_progress_bar')").fetchone()

    conn.close()

    assert result is not None and result[0] is False


def test_build_catalog_processes_s3_secret(tmp_path):
    config_path = _write_config(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          secrets:
            - type: s3
              name: test_s3
              key_id: AKIAIOSFODNN7EXAMPLE
              secret: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
              region: us-west-2
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    db_file = tmp_path / "out.duckdb"

    # Should not raise any errors during catalog build
    build_catalog(str(config_path), db_path=str(db_file))

    # Verify that database file was created
    assert db_file.exists()


def test_build_catalog_processes_persistent_secret(tmp_path):
    config_path = _write_config(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          secrets:
            - type: http
              name: api_auth
              persistent: true
              scope: 'api/'
              key_id: myusername
              secret: mypassword
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    db_file = tmp_path / "out.duckdb"

    # Should not raise any errors during catalog build
    build_catalog(str(config_path), db_path=str(db_file))

    # Verify that database file was created
    assert db_file.exists()


def test_build_catalog_processes_credential_chain_secret(tmp_path):
    config_path = _write_config(
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

    db_file = tmp_path / "out.duckdb"

    # Should not raise any errors during catalog build
    build_catalog(str(config_path), db_path=str(db_file))

    # Verify that database file was created
    assert db_file.exists()


def test_build_catalog_processes_multiple_secrets(tmp_path):
    config_path = _write_config(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
          secrets:
            - type: s3
              name: s3_main
              key_id: AKIAIOSFODNN7EXAMPLE
              secret: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
              region: us-west-2
            - type: http
              name: api_auth
              key_id: apiuser
              secret: apipass
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    db_file = tmp_path / "out.duckdb"

    # Should not raise any errors during catalog build
    build_catalog(str(config_path), db_path=str(db_file))

    # Verify that database file was created
    assert db_file.exists()
