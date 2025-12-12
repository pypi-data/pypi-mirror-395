"""Test filesystem parameter support in custom filesystem functionality."""

import tempfile
from unittest.mock import Mock, patch
from pathlib import Path

import pytest

from duckalog.remote_config import load_config_from_uri, RemoteConfigError


class TestCustomFilesystem:
    """Test custom filesystem parameter functionality."""

    def test_load_config_with_custom_filesystem_success(self):
        """Test successful loading with custom filesystem."""
        with patch("duckalog.remote_config.fetch_remote_content") as mock_fetch:
            mock_fetch.return_value = """
            version: 1
            duckdb:
              database: ":memory:"
            views:
              - name: test_view
                sql: "SELECT 1"
            """

            # Create a mock filesystem
            mock_fs = Mock()
            mock_fs.open.return_value.__enter__.return_value.read.return_value = (
                "mocked_content"
            )

            config = load_config_from_uri("s3://bucket/config.yaml", filesystem=mock_fs)

            assert config.version == 1
            assert len(config.views) == 1
            assert config.views[0].name == "test_view"

    def test_load_config_without_filesystem_backward_compatibility(self):
        """Test that loading without filesystem parameter still works."""
        with patch("duckalog.remote_config.fetch_remote_content") as mock_fetch:
            mock_fetch.return_value = """
            version: 1
            duckdb:
              database: ":memory:"
            views:
              - name: test_view
                sql: "SELECT 1"
            """

            # Should work without filesystem parameter (backward compatibility)
            config = load_config_from_uri("s3://bucket/config.yaml")

            assert config.version == 1
            assert len(config.views) == 1
            assert config.views[0].name == "test_view"

    def test_filesystem_validation_invalid_object(self):
        """Test that invalid filesystem objects are rejected."""
        with pytest.raises(RemoteConfigError, match="Invalid filesystem"):
            load_config_from_uri(
                "s3://bucket/config.yaml", filesystem="invalid_filesystem"
            )

    def test_filesystem_parameter_passed_to_sql_loading(self):
        """Test that filesystem parameter is passed through to SQL file loading."""
        with patch("duckalog.remote_config.fetch_remote_content") as mock_fetch:
            # Mock config with remote SQL file reference
            mock_fetch.return_value = """
            version: 1
            duckdb:
              database: ":memory:"
            views:
              - name: test_view
                sql_file:
                  path: "s3://bucket/sql/view.sql"
            """

            # Create a mock filesystem
            mock_fs = Mock()
            mock_fs.open.return_value.__enter__.return_value.read.return_value = (
                "SELECT * FROM table"
            )

            config = load_config_from_uri(
                "s3://bucket/config.yaml", filesystem=mock_fs, load_sql_files=True
            )

            # Should have loaded SQL file content
            assert config.views[0].sql == "SELECT * FROM table"
            assert config.views[0].sql_file is None  # Converted to inline SQL

    def test_filesystem_error_handling(self):
        """Test error handling with filesystem."""
        mock_fs = Mock()
        mock_fs.open.side_effect = Exception("Access denied")

        with pytest.raises(RemoteConfigError, match="Failed to fetch config from"):
            load_config_from_uri("s3://bucket/config.yaml", filesystem=mock_fs)

    def test_environment_variable_auth_unchanged(self):
        """Test that environment variable authentication still works."""
        with patch("duckalog.remote_config.fetch_remote_content") as mock_fetch:
            mock_fetch.return_value = """
            version: 1
            duckdb:
              database: ":memory:"
            views: []
            """

            # Should still work with environment variables when no filesystem provided
            config = load_config_from_uri("s3://bucket/config.yaml")

            assert config.version == 1
            assert len(config.views) == 0


class TestFilesystemIntegration:
    """Test integration with main load_config function."""

    @patch("duckalog.config.load_config_from_uri")
    def test_main_load_config_passes_filesystem(self, mock_load_from_uri):
        """Test that main load_config function passes filesystem parameter."""
        from duckalog.config import load_config

        mock_config = Mock()
        mock_config.views = []
        mock_load_from_uri.return_value = mock_config

        # Create a mock filesystem
        mock_fs = Mock()

        result = load_config("s3://bucket/config.yaml", filesystem=mock_fs)

        # Should have called remote loader with filesystem
        mock_load_from_uri.assert_called_once()
        call_args = mock_load_from_uri.call_args
        assert call_args[1]["filesystem"] == mock_fs

    @patch("duckalog.config.load_config_from_uri")
    def test_main_load_config_local_file_ignores_filesystem(self, mock_load_from_uri):
        """Test that local files ignore filesystem parameter."""
        from duckalog.config import load_config

        # Create a temporary local file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("version: 1\\nviews: []")
            local_file = f.name

        try:
            mock_config = Mock()
            mock_config.views = []
            mock_load_from_uri.return_value = mock_config

            # Create a mock filesystem (should be ignored for local files)
            mock_fs = Mock()

            result = load_config(local_file, filesystem=mock_fs)

            # Should NOT have called remote loader
            mock_load_from_uri.assert_not_called()
        finally:
            # Clean up
            Path(local_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__])
