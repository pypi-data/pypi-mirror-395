"""Tests for CLI query command."""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import duckdb
import pytest
import typer

from duckalog.cli import query, _display_table, _fail


class TestCLIQuery:
    """Test CLI query functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_catalog = self.temp_dir / "test_catalog.duckdb"

        # Create a test catalog with sample data
        conn = duckdb.connect(str(self.test_catalog))
        conn.execute("CREATE TABLE users (id INTEGER, name VARCHAR, email VARCHAR)")
        conn.execute("INSERT INTO users VALUES (1, 'Alice', 'alice@example.com')")
        conn.execute("INSERT INTO users VALUES (2, 'Bob', 'bob@example.com')")
        conn.execute("CREATE VIEW active_users AS SELECT * FROM users")
        conn.close()

    def test_query_with_explicit_catalog_path(self):
        """Test querying with an explicit catalog path."""
        with patch("duckalog.cli.typer.echo") as mock_echo:
            query(
                sql="SELECT * FROM users ORDER BY id",
                catalog=str(self.test_catalog),
                verbose=False,
            )

            # Verify that output was printed
            mock_echo.assert_called()

            # Check that table formatting was called
            calls = [call.args[0] for call in mock_echo.call_args_list]
            # Should contain table borders and data
            output_text = "".join(calls)
            assert "Alice" in output_text
            assert "Bob" in output_text
            assert "+" in output_text  # Table borders

    def test_query_with_implicit_catalog_discovery(self):
        """Test querying with implicit catalog discovery."""
        # Change to temp directory and create catalog.duckdb
        original_cwd = Path.cwd()
        default_catalog = self.temp_dir / "catalog.duckdb"

        # Create a proper catalog.duckdb with users data
        conn = duckdb.connect(str(default_catalog))
        conn.execute("CREATE TABLE users (id INTEGER, name VARCHAR, email VARCHAR)")
        conn.execute("INSERT INTO users VALUES (1, 'Alice', 'alice@example.com')")
        conn.execute("INSERT INTO users VALUES (2, 'Bob', 'bob@example.com')")
        conn.close()

        try:
            # Change to temp directory
            os.chdir(self.temp_dir)

            with patch("duckalog.cli.typer.echo") as mock_echo:
                query(
                    catalog=None,  # Should discover catalog.duckdb
                    sql="SELECT COUNT(*) as count FROM users",
                    verbose=False,
                )

                mock_echo.assert_called()
                calls = [call.args[0] for call in mock_echo.call_args_list]
                output_text = "".join(calls)
                assert "2" in output_text  # Should show count of 2 users

        finally:
            os.chdir(original_cwd)

    def test_query_missing_catalog_file(self):
        """Test behavior when catalog file does not exist."""
        non_existent_path = str(self.temp_dir / "non_existent.duckdb")

        with patch("duckalog.cli.typer.echo") as mock_echo:
            with pytest.raises(typer.Exit) as exc_info:
                query(catalog=non_existent_path, sql="SELECT 1", verbose=False)

            assert exc_info.value.exit_code == 2
            mock_echo.assert_called_with(
                f"Catalog file not found: {non_existent_path}", err=True
            )

    def test_query_no_default_catalog(self):
        """Test error when no catalog specified and no default found."""
        original_cwd = Path.cwd()
        empty_dir = self.temp_dir / "empty"
        empty_dir.mkdir()

        try:
            os.chdir(empty_dir)

            with patch("duckalog.cli.typer.echo") as mock_echo:
                with pytest.raises(typer.Exit) as exc_info:
                    query(catalog=None, sql="SELECT 1", verbose=False)

                assert exc_info.value.exit_code == 2
                call_args = mock_echo.call_args[0][0]
                assert "No catalog file specified" in call_args
                assert "catalog.duckdb not found" in call_args

        finally:
            os.chdir(original_cwd)

    def test_query_invalid_sql(self):
        """Test behavior with invalid SQL."""
        with patch("duckalog.cli.typer.echo") as mock_echo:
            with pytest.raises(typer.Exit) as exc_info:
                query(
                    catalog=str(self.test_catalog),
                    sql="SELECT * FROM non_existent_table",
                    verbose=False,
                )

            assert exc_info.value.exit_code == 3
            mock_echo.assert_called()
            # Should be an SQL error message
            error_call = mock_echo.call_args_list[-1]
            assert "SQL error:" in str(error_call)

    def test_query_no_results(self):
        """Test querying with no results returned."""
        with patch("duckalog.cli.typer.echo") as mock_echo:
            query(
                catalog=str(self.test_catalog),
                sql="SELECT * FROM users WHERE id = 999",
                verbose=False,
            )

            mock_echo.assert_called()
            calls = [call.args[0] for call in mock_echo.call_args_list]
            output_text = "".join(calls)
            assert "No rows returned" in output_text

    def test_display_table_function(self):
        """Test table display function directly."""
        columns = ["id", "name", "email"]
        rows = [(1, "Alice", "alice@example.com"), (2, "Bob", "bob@example.com")]

        with patch("duckalog.cli.typer.echo") as mock_echo:
            _display_table(columns, rows)

            # Should have been called multiple times for table formatting
            assert mock_echo.call_count > 0

            # Check output contains expected elements
            calls = [call.args[0] for call in mock_echo.call_args_list]
            output_text = "".join(calls)
            assert "Alice" in output_text
            assert "Bob" in output_text
            assert "+" in output_text  # Table borders
            assert "|" in output_text  # Table dividers

    def test_display_table_empty_data(self):
        """Test table display with empty data."""
        with patch("duckalog.cli.typer.echo") as mock_echo:
            _display_table([], [])
            mock_echo.assert_not_called()

            _display_table(["col1"], [])
            mock_echo.assert_not_called()

    def test_query_verbose_logging(self):
        """Test verbose logging in query command."""
        with patch("duckalog.cli._configure_logging") as mock_logging:
            with patch("duckalog.cli.typer.echo"):
                query(catalog=str(self.test_catalog), sql="SELECT 1", verbose=True)

                mock_logging.assert_called_once_with(True)

    def test_query_connection_error(self):
        """Test handling of DuckDB connection errors."""
        # Create a file that's not a valid DuckDB database
        invalid_db = self.temp_dir / "invalid.duckdb"
        invalid_db.write_text("not a database")

        with patch("duckalog.cli.typer.echo") as mock_echo:
            with pytest.raises(typer.Exit) as exc_info:
                query(catalog=str(invalid_db), sql="SELECT 1", verbose=False)

            assert exc_info.value.exit_code == 3
            mock_echo.assert_called()
            # Should be a database error message
            error_call = mock_echo.call_args_list[-1]
            assert "Database error:" in str(error_call)

    def test_query_with_mixed_column_types(self):
        """Test query with different column types."""
        # Add more complex data to test catalog
        conn = duckdb.connect(str(self.test_catalog))
        conn.execute("""
            CREATE TABLE mixed_types (
                id INTEGER,
                name VARCHAR,
                active BOOLEAN,
                score FLOAT,
                created_date DATE
            )
        """)
        conn.execute("""
            INSERT INTO mixed_types VALUES 
            (1, 'Alice', true, 95.5, '2023-01-01'),
            (2, 'Bob', false, 87.2, '2023-01-02')
        """)
        conn.close()

        with patch("duckalog.cli.typer.echo") as mock_echo:
            query(
                catalog=str(self.test_catalog),
                sql="SELECT * FROM mixed_types ORDER BY id",
                verbose=False,
            )

            mock_echo.assert_called()
            calls = [call.args[0] for call in mock_echo.call_args_list]
            output_text = "".join(calls)
            assert "Alice" in output_text
            assert "Bob" in output_text
            assert "95.5" in output_text

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)
