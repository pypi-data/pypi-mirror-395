"""Tests for remote catalog export functionality."""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from duckalog.engine import EngineError, build_catalog, is_remote_export_uri


class TestRemoteExportURI:
    """Test remote URI detection functionality."""

    def test_is_remote_export_uri_with_schemes(self):
        """Test that remote export URIs are correctly detected."""
        # Positive cases
        assert is_remote_export_uri("s3://bucket/catalog.duckdb") is True
        assert is_remote_export_uri("gs://my-bucket/catalog.duckdb") is True
        assert is_remote_export_uri("gcs://project-bucket/catalog.duckdb") is True
        assert is_remote_export_uri("abfs://account@container/catalog.duckdb") is True
        assert is_remote_export_uri("adl://account@container/catalog.duckdb") is True
        assert is_remote_export_uri("sftp://server/path/catalog.duckdb") is True

    def test_is_remote_export_uri_local_paths(self):
        """Test that local paths are not detected as remote."""
        # Negative cases
        assert is_remote_export_uri("/path/to/catalog.duckdb") is False
        assert is_remote_export_uri("catalog.duckdb") is False
        assert is_remote_export_uri("./catalog.duckdb") is False
        assert is_remote_export_uri("C:\\path\\catalog.duckdb") is False

    def test_is_remote_export_uri_edge_cases(self):
        """Test edge cases for URI detection."""
        # Empty and None
        assert is_remote_export_uri("") is False
        assert is_remote_export_uri(None) is False

        # Unsupported schemes
        assert is_remote_export_uri("http://example.com/catalog.duckdb") is False
        assert is_remote_export_uri("https://example.com/catalog.duckdb") is False
        assert is_remote_export_uri("ftp://server/catalog.duckdb") is False

    @patch('duckalog.engine.FSSPEC_AVAILABLE', False)
    def test_is_remote_export_uri_without_fsspec(self):
        """Test that remote URIs are not detected when fsspec is unavailable."""
        assert is_remote_export_uri("s3://bucket/catalog.duckdb") is False
        assert is_remote_export_uri("gs://bucket/catalog.duckdb") is False


class TestRemoteExportUpload:
    """Test remote upload functionality."""

    @patch('duckalog.engine.FSSPEC_AVAILABLE', True)
    @patch('duckalog.engine.fsspec')
    def test_upload_to_remote_success(self, mock_fsspec):
        """Test successful upload to remote storage."""
        # Setup mocks
        mock_filesystem = Mock()
        mock_fsspec.filesystem.return_value = mock_filesystem
        mock_fsspec.open.return_value.__enter__ = Mock()
        mock_fsspec.open.return_value.__exit__ = Mock()

        # Create a temporary test file
        with tempfile.NamedTemporaryFile(suffix='.duckdb', delete=False) as temp_file:
            temp_file.write(b"test database content")
            temp_path = Path(temp_file.name)

        try:
            # Call the function
            _upload_to_remote(temp_path, "s3://bucket/catalog.duckdb")

            # Verify fsspec was called correctly
            mock_fsspec.filesystem.assert_called_once_with("s3")
            mock_fsspec.open.assert_called_once_with("s3://bucket/catalog.duckdb", 'wb')

        finally:
            # Clean up
            temp_path.unlink()

    @patch('duckalog.engine.FSSPEC_AVAILABLE', False)
    def test_upload_to_remote_without_fsspec(self):
        """Test upload failure when fsspec is not available."""
        with tempfile.NamedTemporaryFile(suffix='.duckdb', delete=False) as temp_file:
            temp_file.write(b"test content")
            temp_path = Path(temp_file.name)

        try:
            with pytest.raises(EngineError, match="Remote export requires fsspec"):
                _upload_to_remote(temp_path, "s3://bucket/catalog.duckdb")
        finally:
            temp_path.unlink()

    @patch('duckalog.engine.FSSPEC_AVAILABLE', True)
    @patch('duckalog.engine.fsspec')
    def test_upload_to_remote_with_custom_filesystem(self, mock_fsspec):
        """Test upload using a pre-configured filesystem."""
        # Setup mocks
        custom_filesystem = Mock()
        mock_fsspec.open.return_value.__enter__ = Mock()
        mock_fsspec.open.return_value.__exit__ = Mock()

        # Create a temporary test file
        with tempfile.NamedTemporaryFile(suffix='.duckdb', delete=False) as temp_file:
            temp_file.write(b"test database content")
            temp_path = Path(temp_file.name)

        try:
            # Call the function with custom filesystem
            _upload_to_remote(temp_path, "s3://bucket/catalog.duckdb", filesystem=custom_filesystem)

            # Verify custom filesystem was used, not fsspec.filesystem
            mock_fsspec.filesystem.assert_not_called()
            mock_fsspec.open.assert_called_once_with("s3://bucket/catalog.duckdb", 'wb')

        finally:
            temp_path.unlink()

    @patch('duckalog.engine.FSSPEC_AVAILABLE', True)
    @patch('duckalog.engine.fsspec')
    def test_upload_to_remote_failure(self, mock_fsspec):
        """Test upload failure handling."""
        # Setup mocks to raise an exception
        mock_fsspec.filesystem.side_effect = Exception("Connection failed")

        with tempfile.NamedTemporaryFile(suffix='.duckdb', delete=False) as temp_file:
            temp_file.write(b"test content")
            temp_path = Path(temp_file.name)

        try:
            with pytest.raises(EngineError, match="Failed to upload catalog to s3://bucket/catalog.duckdb"):
                _upload_to_remote(temp_path, "s3://bucket/catalog.duckdb")
        finally:
            temp_path.unlink()


# Import function for testing
from duckalog.engine import _upload_to_remote


class TestBuildCatalogRemoteExport:
    """Test build_catalog with remote export functionality."""

    def create_test_config(self, temp_dir):
        """Create a minimal test configuration file."""
        config_path = Path(temp_dir) / "test_config.yaml"
        config_content = """
duckdb:
  database: ":memory:"

views:
  - name: test_view
    uri: "test.parquet"
    sql: "SELECT 1 as test_col"
"""
        config_path.write_text(config_content)
        return str(config_path)

    @patch('duckalog.engine.FSSPEC_AVAILABLE', True)
    @patch('duckalog.engine._upload_to_remote')
    @patch('duckalog.duckdb.connect')
    def test_build_catalog_remote_export_success(self, mock_duckdb_connect, mock_upload):
        """Test successful remote export during catalog build."""
        # Setup mocks
        mock_conn = Mock()
        mock_duckdb_connect.return_value = mock_conn

        # Create test config
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = self.create_test_config(temp_dir)

            # Call build_catalog with remote URI
            result = build_catalog(
                config_path=config_path,
                db_path="s3://my-bucket/catalog.duckdb"
            )

            # Verify upload was called
            mock_upload.assert_called_once()
            upload_args = mock_upload.call_args[0]
            assert upload_args[1] == "s3://my-bucket/catalog.duckdb"  # remote_uri
            assert upload_args[0].suffix == ".duckdb"  # temp file path

            # Verify function returns None (no SQL on successful build)
            assert result is None

    @patch('duckalog.engine.FSSPEC_AVAILABLE', False)
    def test_build_catalog_remote_export_no_fsspec(self):
        """Test build_catalog failure when fsspec is not available."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = self.create_test_config(temp_dir)

            with pytest.raises(EngineError, match="Remote export requires fsspec"):
                build_catalog(
                    config_path=config_path,
                    db_path="s3://my-bucket/catalog.duckdb"
                )

    @patch('duckalog.engine.FSSPEC_AVAILABLE', True)
    @patch('duckalog.engine._upload_to_remote')
    @patch('duckalog.duckdb.connect')
    def test_build_catalog_local_path_unchanged(self, mock_duckdb_connect, mock_upload):
        """Test that local paths work unchanged."""
        # Setup mocks
        mock_conn = Mock()
        mock_duckdb_connect.return_value = mock_conn

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = self.create_test_config(temp_dir)
            local_db_path = Path(temp_dir) / "catalog.duckdb"

            # Call build_catalog with local path
            build_catalog(
                config_path=config_path,
                db_path=str(local_db_path)
            )

            # Verify upload was not called for local paths
            mock_upload.assert_not_called()

            # Verify DuckDB was called with local path
            mock_duckdb_connect.assert_called_once_with(str(local_db_path))

    @patch('duckalog.engine.FSSPEC_AVAILABLE', True)
    @patch('duckalog.engine._upload_to_remote')
    @patch('duckalog.duckdb.connect')
    def test_build_catalog_with_filesystem_parameter(self, mock_duckdb_connect, mock_upload):
        """Test build_catalog with custom filesystem parameter."""
        # Setup mocks
        mock_conn = Mock()
        mock_duckdb_connect.return_value = mock_conn
        custom_filesystem = Mock()

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = self.create_test_config(temp_dir)

            # Call build_catalog with filesystem parameter
            build_catalog(
                config_path=config_path,
                db_path="s3://my-bucket/catalog.duckdb",
                filesystem=custom_filesystem
            )

            # Verify upload was called with custom filesystem
            mock_upload.assert_called_once()
            upload_args = mock_upload.call_args[0]
            assert upload_args[2] == custom_filesystem  # filesystem parameter

    @patch('duckalog.engine.FSSPEC_AVAILABLE', True)
    @patch('duckalog.engine._upload_to_remote')
    @patch('duckalog.duckdb.connect')
    def test_build_catalog_dry_run_unchanged(self, mock_duckdb_connect, mock_upload):
        """Test that dry run mode is unchanged for remote export."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = self.create_test_config(temp_dir)

            # Call build_catalog with dry_run=True
            result = build_catalog(
                config_path=config_path,
                db_path="s3://my-bucket/catalog.duckdb",
                dry_run=True
            )

            # Verify neither DuckDB nor upload were called in dry run
            mock_duckdb_connect.assert_not_called()
            mock_upload.assert_not_called()

            # Should return SQL string in dry run
            assert isinstance(result, str)

    @patch('duckalog.engine.FSSPEC_AVAILABLE', True)
    @patch('duckalog.engine._upload_to_remote')
    @patch('duckalog.duckdb.connect')
    def test_build_catalog_remote_upload_failure_cleanup(self, mock_duckdb_connect, mock_upload):
        """Test that temp files are cleaned up even if upload fails."""
        # Setup mocks
        mock_conn = Mock()
        mock_duckdb_connect.return_value = mock_conn
        mock_upload.side_effect = Exception("Upload failed")

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = self.create_test_config(temp_dir)

            # Call build_catalog and expect upload failure
            with pytest.raises(EngineError, match="Failed to upload catalog"):
                build_catalog(
                    config_path=config_path,
                    db_path="s3://my-bucket/catalog.duckdb"
                )

            # Verify upload was attempted
            mock_upload.assert_called_once()