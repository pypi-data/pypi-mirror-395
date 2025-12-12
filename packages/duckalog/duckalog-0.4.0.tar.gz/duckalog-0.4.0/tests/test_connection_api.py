"""Tests for DuckDB connection API functions."""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import duckdb
import pytest
import yaml

from duckalog import ConfigError, EngineError, Config, ViewConfig
from duckalog.python_api import (
    connect_to_catalog,
    connect_to_catalog_cm,
    connect_and_build_catalog,
)


@pytest.fixture
def sample_config():
    """Create a sample configuration for testing."""
    from duckalog import DuckDBConfig

    return Config(
        version=1,
        duckdb=DuckDBConfig(database=":memory:"),
        views=[
            ViewConfig(
                name="test_view",
                sql="SELECT 1 as id, 'test' as name",
                description="Test view",
                tags=["test"],
            ),
        ],
    )


@pytest.fixture
def sample_config_path(sample_config):
    """Create a temporary config file path."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(sample_config.model_dump(), f, default_flow_style=False)
        return f.name


class TestConnectToCatalog:
    """Test cases for connect_to_catalog function."""

    def test_connect_to_existing_catalog(self, sample_config_path: str):
        """Test connecting to an existing catalog database."""
        # First build a catalog to connect to
        from duckalog import build_catalog

        build_catalog(sample_config_path)

        # Now connect to it
        conn = connect_to_catalog(sample_config_path)

        assert conn is not None
        assert isinstance(conn, duckdb.DuckDBPyConnection)

        # Test that we can execute queries
        result = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        assert isinstance(result, list)

        conn.close()

    def test_connect_with_database_path_override(self, sample_config_path: str):
        """Test connecting with a custom database path override."""
        with tempfile.NamedTemporaryFile(suffix=".duckdb", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Create a database at the custom path
            conn = duckdb.connect(tmp_path)
            conn.execute("CREATE TABLE test_table (id INTEGER)")
            conn.close()

            # Connect using the override
            conn = connect_to_catalog(sample_config_path, database_path=tmp_path)

            result = conn.execute("SELECT * FROM test_table").fetchall()
            assert result == []

            conn.close()
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_connect_read_only_mode(self, sample_config_path: str):
        """Test connecting in read-only mode."""
        from duckalog import build_catalog

        build_catalog(sample_config_path)

        conn = connect_to_catalog(sample_config_path, read_only=True)

        # Should be able to read
        result = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        assert isinstance(result, list)

        # Should not be able to write (this will raise an exception)
        with pytest.raises(duckdb.Error):
            conn.execute("CREATE TABLE test_table (id INTEGER)")

        conn.close()

    def test_connect_to_in_memory_database(self, sample_config_path: str):
        """Test connecting to an in-memory database."""
        conn = connect_to_catalog(sample_config_path, database_path=":memory:")

        assert conn is not None
        assert isinstance(conn, duckdb.DuckDBPyConnection)

        # In-memory database should be empty
        result = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        assert result == []

        conn.close()

    def test_connect_nonexistent_database(self, sample_config_path: str):
        """Test connecting to a non-existent database raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="Database file not found"):
            connect_to_catalog(sample_config_path, database_path="/nonexistent/path.db")

    def test_connect_invalid_config(self):
        """Test connecting with invalid config raises ConfigError."""
        with pytest.raises(ConfigError):
            connect_to_catalog("/nonexistent/config.yaml")


class TestConnectToCatalogCm:
    """Test cases for connect_to_catalog_cm context manager."""

    def test_context_manager_automatic_cleanup(self, sample_config_path: str):
        """Test that context manager automatically closes connection."""
        from duckalog import build_catalog

        build_catalog(sample_config_path)

        with connect_to_catalog_cm(sample_config_path) as conn:
            assert conn is not None
            assert isinstance(conn, duckdb.DuckDBPyConnection)

            # Should be able to execute queries
            result = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
            assert isinstance(result, list)

        # Connection should be closed after exiting context
        # Trying to use it should raise an exception
        with pytest.raises(duckdb.Error):
            conn.execute("SELECT 1")

    def test_context_manager_with_exception(self, sample_config_path: str):
        """Test that context manager closes connection even when exception occurs."""
        from duckalog import build_catalog

        build_catalog(sample_config_path)

        connection_ref = None
        with pytest.raises(ValueError):
            with connect_to_catalog_cm(sample_config_path) as conn:
                assert conn is not None
                connection_ref = conn
                raise ValueError("Test exception")

        # Connection should still be closed despite the exception
        if connection_ref is not None:
            with pytest.raises(duckdb.Error):
                connection_ref.execute("SELECT 1")

    def test_context_manager_with_path_override(self, sample_config_path: str):
        """Test context manager with database path override."""
        with tempfile.NamedTemporaryFile(suffix=".duckdb", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Create a database at the custom path
            conn = duckdb.connect(tmp_path)
            conn.execute("CREATE TABLE test_table (id INTEGER)")
            conn.close()

            # Use context manager with override
            with connect_to_catalog_cm(
                sample_config_path, database_path=tmp_path
            ) as conn:
                result = conn.execute("SELECT * FROM test_table").fetchall()
                assert result == []
        finally:
            Path(tmp_path).unlink(missing_ok=True)


class TestConnectAndBuildCatalog:
    """Test cases for connect_and_build_catalog function."""

    def test_build_and_connect_success(self, sample_config_path: str):
        """Test successful build and connect operation."""
        conn = connect_and_build_catalog(sample_config_path)

        assert conn is not None
        assert isinstance(conn, duckdb.DuckDBPyConnection)

        # Should be able to execute queries
        result = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        assert isinstance(result, list)

        conn.close()

    def test_build_and_connect_with_custom_path(self, sample_config_path: str):
        """Test build and connect with custom database path."""
        with tempfile.NamedTemporaryFile(suffix=".duckdb", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            conn = connect_and_build_catalog(sample_config_path, database_path=tmp_path)

            assert conn is not None
            assert isinstance(conn, duckdb.DuckDBPyConnection)

            # Database should exist at custom path
            assert Path(tmp_path).exists()

            conn.close()
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_build_and_connect_dry_run(self, sample_config_path: str):
        """Test dry run mode returns SQL string instead of connection."""
        result = connect_and_build_catalog(sample_config_path, dry_run=True)

        assert isinstance(result, str)
        assert "CREATE VIEW" in result or "CREATE TABLE" in result
        # Should not be a connection object
        assert not hasattr(result, "execute")
        assert not hasattr(result, "close")

    def test_build_and_connect_read_only(self, sample_config_path: str):
        """Test build and connect in read-only mode."""
        conn = connect_and_build_catalog(sample_config_path, read_only=True)

        # Should be a connection object, not a string
        assert hasattr(conn, "execute")
        assert hasattr(conn, "close")
        assert isinstance(conn, duckdb.DuckDBPyConnection)

        # Should be able to read
        result = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        assert isinstance(result, list)

        # Should not be able to write
        with pytest.raises(duckdb.Error):
            conn.execute("CREATE TABLE test_table (id INTEGER)")

        conn.close()

    def test_build_and_connect_with_verbose(self, sample_config_path: str):
        """Test build and connect with verbose mode."""
        conn = connect_and_build_catalog(sample_config_path, verbose=True)

        assert conn is not None
        assert isinstance(conn, duckdb.DuckDBPyConnection)
        assert hasattr(conn, "execute")
        assert hasattr(conn, "close")

        conn.close()

    def test_build_and_connect_invalid_config(self):
        """Test build and connect with invalid config raises ConfigError."""
        with pytest.raises(ConfigError):
            connect_and_build_catalog("/nonexistent/config.yaml")

    def test_build_and_connect_build_failure(self):
        """Test that build failures prevent connection creation."""
        # Create a config that will fail during build
        invalid_config = """
duckdb:
  database: ":memory:"

views:
  - name: test_view
    query: "INVALID SQL SYNTAX"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as tmp:
            tmp.write(invalid_config)
            tmp_path = tmp.name

        try:
            with pytest.raises((EngineError, duckdb.Error)):
                connect_and_build_catalog(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_build_and_connect_with_kwargs(self, sample_config_path: str):
        """Test build and connect with additional keyword arguments."""
        # Test with filesystem kwarg (should be passed to build_catalog)
        conn = connect_and_build_catalog(
            sample_config_path,
            filesystem=None,  # This should be passed through to build_catalog
        )

        assert conn is not None
        assert isinstance(conn, duckdb.DuckDBPyConnection)

        conn.close()


class TestIntegrationWorkflow:
    """Integration tests for complete user workflows."""

    def test_config_to_queries_workflow(self, sample_config_path: str):
        """Test complete workflow from config to executing queries."""
        # Method 1: Build then connect
        from duckalog import build_catalog

        build_catalog(sample_config_path)

        conn = connect_to_catalog(sample_config_path)

        # Execute some queries
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        assert isinstance(tables, list)

        conn.close()

    def test_single_function_workflow(self, sample_config_path: str):
        """Test workflow using single function for build and connect."""
        conn = connect_and_build_catalog(sample_config_path)

        # Execute queries immediately
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        assert isinstance(tables, list)

        conn.close()

    def test_context_manager_workflow(self, sample_config_path: str):
        """Test workflow using context manager for automatic cleanup."""
        with connect_to_catalog_cm(sample_config_path) as conn:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
            assert isinstance(tables, list)

        # Connection is automatically closed

    def test_build_and_connect_context_manager_workflow(self, sample_config_path: str):
        """Test workflow combining build and connect with context manager."""
        # Build first, then use context manager
        connect_and_build_catalog(sample_config_path)

        with connect_to_catalog_cm(sample_config_path) as conn:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
            assert isinstance(tables, list)
