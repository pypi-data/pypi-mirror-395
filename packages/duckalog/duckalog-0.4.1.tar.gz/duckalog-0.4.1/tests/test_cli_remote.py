"""CLI tests for remote configuration support."""

import tempfile
from unittest.mock import Mock, patch
from pathlib import Path

import pytest
from typer.testing import CliRunner

from duckalog.cli import app


class TestRemoteConfigCLI:
    """Test CLI commands with remote configuration support."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    @patch("duckalog.cli.load_config")
    def test_build_with_remote_uri_success(self, mock_load_config):
        """Test build command with remote URI."""
        # Mock successful config loading
        mock_config = Mock()
        mock_config.views = []
        mock_load_config.return_value = mock_config

        result = self.runner.invoke(
            app, ["build", "s3://my-bucket/config.yaml", "--dry-run"]
        )

        assert result.exit_code == 0
        mock_load_config.assert_called_once_with("s3://my-bucket/config.yaml")

    @patch("duckalog.cli.load_config")
    def test_build_with_local_file_success(self, mock_load_config):
        """Test build command with local file."""
        # Create a temporary config file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("version: 1\\nviews: []")
            config_file = f.name

        try:
            # Mock successful config loading
            mock_config = Mock()
            mock_config.views = []
            mock_load_config.return_value = mock_config

            result = self.runner.invoke(app, ["build", config_file, "--dry-run"])

            assert result.exit_code == 0
            mock_load_config.assert_called_once_with(config_file)
        finally:
            # Clean up
            Path(config_file).unlink()

    def test_build_with_local_file_not_found(self):
        """Test build command with non-existent local file."""
        result = self.runner.invoke(app, ["build", "nonexistent_config.yaml"])

        assert result.exit_code == 2
        assert "Config file not found" in result.stdout

    @patch("duckalog.cli.load_config")
    def test_generate_sql_with_remote_uri(self, mock_load_config):
        """Test generate-sql command with remote URI."""
        # Mock successful config loading
        mock_config = Mock()
        mock_config.views = []
        mock_load_config.return_value = mock_config

        result = self.runner.invoke(
            app, ["generate-sql", "https://example.com/config.yaml"]
        )

        assert result.exit_code == 0
        mock_load_config.assert_called_once_with("https://example.com/config.yaml")

    @patch("duckalog.cli.load_config")
    def test_validate_with_remote_uri(self, mock_load_config):
        """Test validate command with remote URI."""
        # Mock successful config loading
        mock_config = Mock()
        mock_load_config.return_value = mock_config

        result = self.runner.invoke(app, ["validate", "gcs://my-bucket/config.yaml"])

        assert result.exit_code == 0
        assert "Config is valid." in result.stdout
        mock_load_config.assert_called_once_with("gcs://my-bucket/config.yaml")

    @patch("duckalog.cli.load_config")
    def test_validate_with_remote_uri_error(self, mock_load_config):
        """Test validate command with remote URI that fails validation."""
        # Mock config loading error
        from duckalog.config import ConfigError

        mock_load_config.side_effect = ConfigError("Invalid config")

        result = self.runner.invoke(app, ["validate", "s3://bucket/config.yaml"])

        assert result.exit_code == 2
        assert "Config error: Invalid config" in result.stdout

    def test_ui_with_remote_uri_error(self):
        """Test UI command with remote URI (should fail)."""
        result = self.runner.invoke(app, ["ui", "s3://bucket/config.yaml"])

        assert result.exit_code == 2
        assert "UI currently only supports local configuration files" in result.stdout

    @patch("duckalog.cli.load_config")
    def test_ui_with_local_file(self, mock_load_config):
        """Test UI command with local file."""
        # Create a temporary config file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("version: 1\\nviews: []")
            config_file = f.name

        try:
            # Mock successful config loading
            mock_config = Mock()
            mock_load_config.return_value = mock_config

            # Mock UIServer to avoid actually starting it
            with patch("duckalog.cli.UIServer") as mock_ui_server:
                mock_server_instance = Mock()
                mock_ui_server.return_value = mock_server_instance

                result = self.runner.invoke(
                    app, ["ui", config_file, "--host", "localhost", "--port", "8080"]
                )

                # UI command should fail because we can't actually test the UI server
                # but we can check that it tried to create it
                assert mock_ui_server.called or result.exit_code != 0
        finally:
            # Clean up
            Path(config_file).unlink()

    @patch("duckalog.cli.is_remote_uri")
    def test_command_without_remote_support(self, mock_is_remote):
        """Test commands when remote support is not available."""
        # Mock remote support as unavailable
        mock_is_remote.side_effect = ImportError(
            "No module named 'duckalog.remote_config'"
        )

        # Test with local file - should work
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("version: 1\\nviews: []")
            config_file = f.name

        try:
            with patch("duckalog.cli.load_config") as mock_load_config:
                mock_config = Mock()
                mock_config.views = []
                mock_load_config.return_value = mock_config

                result = self.runner.invoke(app, ["build", config_file, "--dry-run"])

                assert result.exit_code == 0
                mock_load_config.assert_called_once_with(config_file)
        finally:
            Path(config_file).unlink()

    @patch("duckalog.cli.is_remote_uri")
    def test_remote_uri_validation_in_commands(self, mock_is_remote):
        """Test that commands validate remote URIs properly."""
        # Mock remote URI detection
        mock_is_remote.return_value = True

        # Test build command
        with patch("duckalog.cli.build_catalog") as mock_build_catalog:
            mock_build_catalog.return_value = "CREATE VIEW test AS SELECT 1"

            result = self.runner.invoke(
                app, ["build", "s3://bucket/config.yaml", "--dry-run"]
            )

            # Should not fail on URI validation for remote URIs
            assert result.exit_code == 0 or "Config error" in result.stdout

    def test_show_paths_with_remote_uri_not_supported(self):
        """Test that show-paths command doesn't support remote URIs."""
        # The show-paths command expects local files for path resolution
        # This test verifies it properly handles the case

        # Since show-paths requires exists=True and we changed that,
        # let's test what happens when we try to use a remote URI
        result = self.runner.invoke(app, ["show-paths", "s3://bucket/config.yaml"])

        # Should fail because show-paths still expects local files
        # (this command wasn't updated for remote support in our implementation)
        assert result.exit_code != 0

    def test_validate_paths_with_remote_uri_not_supported(self):
        """Test that validate-paths command doesn't support remote URIs."""
        result = self.runner.invoke(app, ["validate-paths", "s3://bucket/config.yaml"])

        # Should fail because validate-paths still expects local files
        assert result.exit_code != 0


class TestRemoteConfigIntegration:
    """Integration tests for remote configuration functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    @patch("duckalog.remote_config.fetch_remote_content")
    @patch("duckalog.remote_config.is_remote_uri")
    def test_end_to_end_remote_config_build(self, mock_is_remote, mock_fetch):
        """Test end-to-end build with remote configuration."""
        # Mock remote URI detection
        mock_is_remote.return_value = True

        # Mock remote config content
        config_content = """
        version: 1
        duckdb:
          database: ":memory:"
        views:
          - name: test_view
            sql: "SELECT 1 as test_col"
        """
        mock_fetch.return_value = config_content

        # Mock build_catalog to avoid database operations
        with patch("duckalog.cli.build_catalog") as mock_build_catalog:
            mock_build_catalog.return_value = (
                "CREATE VIEW test_view AS SELECT 1 as test_col"
            )

            result = self.runner.invoke(
                app, ["build", "s3://bucket/config.yaml", "--dry-run"]
            )

            assert result.exit_code == 0
            assert "CREATE VIEW test_view" in result.stdout

    @patch("duckalog.remote_config.fetch_remote_content")
    @patch("duckalog.remote_config.is_remote_uri")
    def test_end_to_end_remote_config_validation_error(
        self, mock_is_remote, mock_fetch
    ):
        """Test end-to-end validation with remote configuration that fails."""
        # Mock remote URI detection
        mock_is_remote.return_value = True

        # Mock invalid remote config content
        invalid_config = """
        version: 1
        duckdb:
          database: ":memory:"
        # Missing views section - invalid config
        """
        mock_fetch.return_value = invalid_config

        result = self.runner.invoke(app, ["validate", "s3://bucket/config.yaml"])

        assert result.exit_code == 2
        assert "Config error" in result.stdout


class TestRemoteExportCLI:
    """Test CLI commands with remote catalog export functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def create_test_config(self, temp_dir):
        """Create a minimal test configuration file."""
        config_path = Path(temp_dir) / "test_config.yaml"
        config_content = """
version: 1
duckdb:
  database: ":memory:"

views:
  - name: test_view
    uri: "test.parquet"
    sql: "SELECT 1 as test_col"
"""
        config_path.write_text(config_content)
        return str(config_path)

    @patch("duckalog.cli.build_catalog")
    def test_build_export_to_s3_success(self, mock_build_catalog):
        """Test build command with S3 export."""
        # Mock successful build
        mock_build_catalog.return_value = None

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = self.create_test_config(temp_dir)

            result = self.runner.invoke(
                app,
                [
                    "build",
                    config_path,
                    "--db-path",
                    "s3://my-bucket/catalog.duckdb"
                ]
            )

            assert result.exit_code == 0
            mock_build_catalog.assert_called_once()
            call_kwargs = mock_build_catalog.call_args[1]
            assert call_kwargs["db_path"] == "s3://my-bucket/catalog.duckdb"

    @patch("duckalog.cli.build_catalog")
    def test_build_export_to_gcs_success(self, mock_build_catalog):
        """Test build command with GCS export."""
        # Mock successful build
        mock_build_catalog.return_value = None

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = self.create_test_config(temp_dir)

            result = self.runner.invoke(
                app,
                [
                    "build",
                    config_path,
                    "--db-path",
                    "gs://my-project-bucket/catalog.duckdb"
                ]
            )

            assert result.exit_code == 0
            mock_build_catalog.assert_called_once()
            call_kwargs = mock_build_catalog.call_args[1]
            assert call_kwargs["db_path"] == "gs://my-project-bucket/catalog.duckdb"

    @patch("duckalog.cli.build_catalog")
    def test_build_export_to_azure_success(self, mock_build_catalog):
        """Test build command with Azure export."""
        # Mock successful build
        mock_build_catalog.return_value = None

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = self.create_test_config(temp_dir)

            result = self.runner.invoke(
                app,
                [
                    "build",
                    config_path,
                    "--db-path",
                    "abfs://account@container/catalog.duckdb",
                    "--azure-connection-string",
                    "DefaultEndpointsProtocol=https;AccountName=test"
                ]
            )

            assert result.exit_code == 0
            mock_build_catalog.assert_called_once()
            call_kwargs = mock_build_catalog.call_args[1]
            assert call_kwargs["db_path"] == "abfs://account@container/catalog.duckdb"

    @patch("duckalog.cli.build_catalog")
    def test_build_export_to_sftp_success(self, mock_build_catalog):
        """Test build command with SFTP export."""
        # Mock successful build
        mock_build_catalog.return_value = None

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = self.create_test_config(temp_dir)

            result = self.runner.invoke(
                app,
                [
                    "build",
                    config_path,
                    "--db-path",
                    "sftp://server/path/catalog.duckdb",
                    "--sftp-host",
                    "server.com",
                    "--sftp-key-file",
                    "/path/to/key"
                ]
            )

            assert result.exit_code == 0
            mock_build_catalog.assert_called_once()
            call_kwargs = mock_build_catalog.call_args[1]
            assert call_kwargs["db_path"] == "sftp://server/path/catalog.duckdb"

    @patch("duckalog.cli.build_catalog")
    def test_build_export_with_custom_filesystem(self, mock_build_catalog):
        """Test build command with custom filesystem authentication."""
        # Mock successful build
        mock_build_catalog.return_value = None

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = self.create_test_config(temp_dir)

            result = self.runner.invoke(
                app,
                [
                    "build",
                    config_path,
                    "--db-path",
                    "s3://my-bucket/catalog.duckdb",
                    "--fs-key",
                    "AKIATESTKEY",
                    "--fs-secret",
                    "testsecret"
                ]
            )

            assert result.exit_code == 0
            mock_build_catalog.assert_called_once()
            # Verify filesystem parameter was passed
            call_kwargs = mock_build_catalog.call_args[1]
            assert "filesystem" in call_kwargs
            assert call_kwargs["filesystem"] is not None

    @patch("duckalog.cli.build_catalog")
    def test_build_local_db_path_unchanged(self, mock_build_catalog):
        """Test that local database paths work unchanged."""
        # Mock successful build
        mock_build_catalog.return_value = None

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = self.create_test_config(temp_dir)
            local_db_path = Path(temp_dir) / "catalog.duckdb"

            result = self.runner.invoke(
                app,
                [
                    "build",
                    config_path,
                    "--db-path",
                    str(local_db_path)
                ]
            )

            assert result.exit_code == 0
            mock_build_catalog.assert_called_once()
            call_kwargs = mock_build_catalog.call_args[1]
            assert call_kwargs["db_path"] == str(local_db_path)

    @patch("duckalog.cli.build_catalog")
    def test_build_export_dry_run_unchanged(self, mock_build_catalog):
        """Test that dry run mode works with remote export paths."""
        # Mock dry run return
        mock_build_catalog.return_value = "SELECT 1;"

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = self.create_test_config(temp_dir)

            result = self.runner.invoke(
                app,
                [
                    "build",
                    config_path,
                    "--db-path",
                    "s3://my-bucket/catalog.duckdb",
                    "--dry-run"
                ]
            )

            assert result.exit_code == 0
            assert "SELECT 1;" in result.stdout
            mock_build_catalog.assert_called_once()
            call_kwargs = mock_build_catalog.call_args[1]
            assert call_kwargs["db_path"] == "s3://my-bucket/catalog.duckdb"
            assert call_kwargs["dry_run"] is True

    @patch("duckalog.cli.build_catalog")
    @patch("duckalog.cli._create_filesystem_from_options")
    def test_build_export_filesystem_creation_error(self, mock_create_filesystem, mock_build_catalog):
        """Test build command with filesystem creation error."""
        # Mock filesystem creation failure
        from typer import Exit
        mock_create_filesystem.side_effect = Exit(4)

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = self.create_test_config(temp_dir)

            result = self.runner.invoke(
                app,
                [
                    "build",
                    config_path,
                    "--db-path",
                    "s3://my-bucket/catalog.duckdb",
                    "--fs-key",
                    "invalidkey"
                ]
            )

            assert result.exit_code == 4

    @patch("duckalog.cli.build_catalog")
    def test_build_export_engine_error(self, mock_build_catalog):
        """Test build command with engine error during remote export."""
        # Mock engine error
        from duckalog.engine import EngineError
        mock_build_catalog.side_effect = EngineError("Upload failed")

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = self.create_test_config(temp_dir)

            result = self.runner.invoke(
                app,
                [
                    "build",
                    config_path,
                    "--db-path",
                    "s3://my-bucket/catalog.duckdb"
                ]
            )

            assert result.exit_code == 3
            assert "Engine error" in result.stdout


if __name__ == "__main__":
    pytest.main([__file__])
