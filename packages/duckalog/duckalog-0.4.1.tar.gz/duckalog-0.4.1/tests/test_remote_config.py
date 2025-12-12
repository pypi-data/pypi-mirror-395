"""Tests for remote configuration loading functionality."""

import json
import os
import tempfile
from unittest.mock import Mock, patch, mock_open
from urllib.parse import urlparse

import pytest
import yaml

from duckalog import load_config
from duckalog.config import ConfigError
from duckalog.remote_config import (
    RemoteConfigError,
    fetch_remote_content,
    is_remote_uri,
    load_config_from_uri,
    validate_remote_uri,
)


class TestRemoteURIIdentification:
    """Test identification of remote URIs."""

    def test_is_remote_uri_with_schemes(self):
        """Test that supported schemes are identified as remote."""
        remote_uris = [
            "s3://bucket/path/config.yaml",
            "s3a://bucket/path/config.yaml",
            "gcs://bucket/path/config.yaml",
            "gs://bucket/path/config.yaml",
            "abfs://account@container/path/config.yaml",
            "adl://account@container/path/config.yaml",
            "az://account@container/path/config.yaml",
            "sftp://user@host/path/config.yaml",
            "ssh://user@host/path/config.yaml",
            "https://example.com/config.yaml",
            "http://example.com/config.yaml",
        ]

        for uri in remote_uris:
            assert is_remote_uri(uri), f"URI {uri} should be identified as remote"

    def test_is_remote_uri_with_local_paths(self):
        """Test that local paths are not identified as remote."""
        local_paths = [
            "config.yaml",
            "./config.yaml",
            "/absolute/path/config.yaml",
            "relative/path/config.yaml",
            "C:\\Windows\\path\\config.yaml",
            "",
            "file:///absolute/path/config.yaml",  # file:// is not supported
        ]

        for path in local_paths:
            assert not is_remote_uri(path), (
                f"Path {path} should not be identified as remote"
            )

    def test_is_remote_uri_with_edge_cases(self):
        """Test edge cases for URI identification."""
        # Empty string
        assert not is_remote_uri("")

        # None
        assert not is_remote_uri(None)  # type: ignore

        # Unsupported schemes
        assert not is_remote_uri("ftp://example.com/config.yaml")
        assert not is_remote_uri("mailto:test@example.com")


class TestRemoteURIValidation:
    """Test validation of remote URIs."""

    def test_validate_remote_uri_supported_schemes(self):
        """Test validation of supported URI schemes."""
        # Should not raise for supported schemes
        supported_uris = [
            "s3://bucket/config.yaml",
            "https://example.com/config.yaml",
            "gcs://bucket/config.yaml",
        ]

        for uri in supported_uris:
            # Should not raise an exception
            validate_remote_uri(uri)

    @patch("duckalog.remote_config.FSSPEC_AVAILABLE", False)
    def test_validate_remote_uri_fsspec_not_available(self):
        """Test validation when fsspec is not available."""
        with pytest.raises(RemoteConfigError, match="fsspec is required"):
            validate_remote_uri("s3://bucket/config.yaml")

    @patch("duckalog.remote_config.REQUESTS_AVAILABLE", False)
    def test_validate_remote_uri_requests_not_available(self):
        """Test validation when requests is not available."""
        with pytest.raises(RemoteConfigError, match="requests is required"):
            validate_remote_uri("https://example.com/config.yaml")

    def test_validate_remote_uri_unsupported_scheme(self):
        """Test validation of unsupported URI schemes."""
        with pytest.raises(RemoteConfigError, match="Unsupported URI scheme"):
            validate_remote_uri("ftp://example.com/config.yaml")

    @patch("duckalog.remote_config.FSSPEC_AVAILABLE", True)
    @patch("duckalog.remote_config.fsspec", None)
    @patch("duckalog.remote_config.known_implementations", {})
    def test_validate_remote_uri_backend_not_available(self):
        """Test validation when specific backend is not available."""
        with pytest.raises(
            RemoteConfigError, match="fsspec backend for .* is not available"
        ):
            validate_remote_uri("s3://bucket/config.yaml")


class TestRemoteContentFetching:
    """Test fetching content from remote URIs."""

    @patch("duckalog.remote_config.requests.get")
    def test_fetch_http_content_success(self, mock_get):
        """Test successful HTTP content fetching."""
        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.text = "version: 1\\nviews: []"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        content = fetch_remote_content("https://example.com/config.yaml")

        assert content == "version: 1\\nviews: []"
        mock_get.assert_called_once_with("https://example.com/config.yaml", timeout=30)

    @patch("duckalog.remote_config.requests.get")
    def test_fetch_http_content_error(self, mock_get):
        """Test HTTP error handling."""
        # Mock HTTP error
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("HTTP Error")
        mock_get.return_value = mock_response

        with pytest.raises(RemoteConfigError, match="Failed to fetch config from"):
            fetch_remote_content("https://example.com/config.yaml")

    @patch("duckalog.remote_config.FSSPEC_AVAILABLE", True)
    @patch("duckalog.remote_config.fsspec")
    def test_fetch_fsspec_content_success(self, mock_fsspec):
        """Test successful fsspec content fetching."""
        # Mock fsspec open context manager
        mock_file = Mock()
        mock_file.read.return_value = "version: 1\\nviews: []"
        mock_fsspec.open.return_value.__enter__.return_value = mock_file

        content = fetch_remote_content("s3://bucket/config.yaml")

        assert content == "version: 1\\nviews: []"
        mock_fsspec.open.assert_called_once_with(
            "s3://bucket/config.yaml", "r", timeout=30
        )

    @patch("duckalog.remote_config.FSSPEC_AVAILABLE", True)
    @patch("duckalog.remote_config.fsspec")
    def test_fetch_fsspec_content_error(self, mock_fsspec):
        """Test fsspec error handling."""
        # Mock fsspec error
        mock_fsspec.open.side_effect = Exception("S3 Error")

        with pytest.raises(RemoteConfigError, match="Failed to fetch config from"):
            fetch_remote_content("s3://bucket/config.yaml")


class TestRemoteConfigLoading:
    """Test loading configuration from remote URIs."""

    def test_load_config_from_uri_not_remote(self):
        """Test error when URI is not remote."""
        with pytest.raises(RemoteConfigError, match="not a recognized remote URI"):
            load_config_from_uri("local_config.yaml")

    @patch("duckalog.remote_config.fetch_remote_content")
    def test_load_config_from_uri_yaml_success(self, mock_fetch):
        """Test successful YAML config loading from remote URI."""
        # Mock remote content
        yaml_content = """
        version: 1
        duckdb:
          database: ":memory:"
        views:
          - name: test_view
            sql: "SELECT 1"
        """
        mock_fetch.return_value = yaml_content

        config = load_config_from_uri("s3://bucket/config.yaml")

        assert config.version == 1
        assert len(config.views) == 1
        assert config.views[0].name == "test_view"
        mock_fetch.assert_called_once_with("s3://bucket/config.yaml", 30)

    @patch("duckalog.remote_config.fetch_remote_content")
    def test_load_config_from_uri_json_success(self, mock_fetch):
        """Test successful JSON config loading from remote URI."""
        # Mock remote content
        json_content = {
            "version": 1,
            "duckdb": {"database": ":memory:"},
            "views": [{"name": "test_view", "sql": "SELECT 1"}],
        }
        mock_fetch.return_value = json.dumps(json_content)

        config = load_config_from_uri("https://example.com/config.json")

        assert config.version == 1
        assert len(config.views) == 1
        assert config.views[0].name == "test_view"

    @patch("duckalog.remote_config.fetch_remote_content")
    def test_load_config_from_uri_invalid_yaml(self, mock_fetch):
        """Test handling of invalid YAML content."""
        # Mock invalid YAML
        mock_fetch.return_value = "invalid: yaml: content: ["

        with pytest.raises(RemoteConfigError, match="Invalid YAML in remote config"):
            load_config_from_uri("s3://bucket/config.yaml")

    @patch("duckalog.remote_config.fetch_remote_content")
    def test_load_config_from_uri_invalid_json(self, mock_fetch):
        """Test handling of invalid JSON content."""
        # Mock invalid JSON
        mock_fetch.return_value = "invalid json content"

        with pytest.raises(RemoteConfigError, match="Invalid JSON in remote config"):
            load_config_from_uri("https://example.com/config.json")

    @patch("duckalog.remote_config.fetch_remote_content")
    def test_load_config_from_uri_empty_content(self, mock_fetch):
        """Test handling of empty content."""
        # Mock empty content
        mock_fetch.return_value = ""

        with pytest.raises(RemoteConfigError, match="Remote config file is empty"):
            load_config_from_uri("s3://bucket/config.yaml")

    @patch("duckalog.remote_config.fetch_remote_content")
    def test_load_config_from_uri_invalid_structure(self, mock_fetch):
        """Test handling of invalid config structure."""
        # Mock content that's not a mapping
        mock_fetch.return_value = "not a mapping"

        with pytest.raises(
            RemoteConfigError, match="must define a mapping at the top level"
        ):
            load_config_from_uri("s3://bucket/config.yaml")

    @patch("duckalog.remote_config.fetch_remote_content")
    def test_load_config_from_uri_validation_error(self, mock_fetch):
        """Test handling of config validation errors."""
        # Mock content that fails validation
        mock_fetch.return_value = """
        version: 1
        duckdb:
          database: ":memory:"
        views: []  # Missing required views
        """

        with pytest.raises(RemoteConfigError, match="Remote config validation failed"):
            load_config_from_uri("s3://bucket/config.yaml")

    @patch("duckalog.remote_config.fetch_remote_content")
    def test_load_config_from_uri_with_timeout(self, mock_fetch):
        """Test loading with custom timeout."""
        mock_fetch.return_value = "version: 1\\nviews: []"

        load_config_from_uri("s3://bucket/config.yaml", timeout=60)

        mock_fetch.assert_called_once_with("s3://bucket/config.yaml", 60)


class TestRemoteSQLFileLoading:
    """Test loading SQL files from remote configurations."""

    @patch("duckalog.remote_config.fetch_remote_content")
    def test_load_config_with_remote_sql_file(self, mock_fetch):
        """Test loading config with remote SQL file reference."""
        # Mock config content with SQL file reference
        config_content = """
        version: 1
        duckdb:
          database: ":memory:"
        views:
          - name: test_view
            sql_file:
              path: "s3://bucket/sql/view.sql"
        """
        # Mock SQL file content
        sql_content = "SELECT * FROM table"

        # Mock fetch to return different content based on URI
        def mock_fetch_side_effect(uri, timeout=30):
            if uri.endswith("config.yaml"):
                return config_content
            elif uri.endswith("view.sql"):
                return sql_content
            else:
                raise ValueError(f"Unexpected URI: {uri}")

        mock_fetch.side_effect = mock_fetch_side_effect

        config = load_config_from_uri("s3://bucket/config.yaml")

        assert len(config.views) == 1
        assert config.views[0].name == "test_view"
        assert config.views[0].sql == sql_content
        assert config.views[0].sql_file is None  # Should be resolved to inline SQL

    @patch("duckalog.remote_config.fetch_remote_content")
    def test_load_config_with_local_sql_file(self, mock_fetch):
        """Test loading config with local SQL file reference."""
        # Create a temporary SQL file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as f:
            f.write("SELECT * FROM table")
            sql_file_path = f.name

        try:
            # Mock config content with local SQL file reference
            config_content = f"""
            version: 1
            duckdb:
              database: ":memory:"
            views:
              - name: test_view
                sql_file:
                  path: "{os.path.basename(sql_file_path)}"
            """
            mock_fetch.return_value = config_content

            # This should fail because local SQL files can't be resolved from remote configs
            with pytest.raises(RemoteConfigError):
                load_config_from_uri("s3://bucket/config.yaml")
        finally:
            # Clean up temp file
            os.unlink(sql_file_path)


class TestIntegrationWithLocalConfig:
    """Test integration with local config loading."""

    @patch("duckalog.remote_config.is_remote_uri")
    def test_local_config_unchanged(self, mock_is_remote):
        """Test that local config loading is unchanged."""
        mock_is_remote.return_value = False

        # Create a temporary config file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(
                {
                    "version": 1,
                    "duckdb": {"database": ":memory:"},
                    "views": [{"name": "test_view", "sql": "SELECT 1"}],
                },
                f,
            )
            config_file_path = f.name

        try:
            # This should use local loading, not remote
            from duckalog.config import load_config

            config = load_config(config_file_path)

            assert config.version == 1
            assert len(config.views) == 1
            assert config.views[0].name == "test_view"
        finally:
            # Clean up temp file
            os.unlink(config_file_path)

    @patch("duckalog.remote_config.is_remote_uri")
    @patch("duckalog.remote_config.load_config_from_uri")
    def test_remote_config_delegation(self, mock_load_from_uri, mock_is_remote):
        """Test that remote URIs are delegated to remote loader."""
        mock_is_remote.return_value = True
        mock_config = Mock()
        mock_load_from_uri.return_value = mock_config

        from duckalog.config import load_config

        config = load_config("s3://bucket/config.yaml")

        assert config == mock_config
        mock_is_remote.assert_called_once_with("s3://bucket/config.yaml")
        mock_load_from_uri.assert_called_once_with(
            "s3://bucket/config.yaml",
            load_sql_files=True,
            sql_file_loader=None,
            resolve_paths=False,
        )


class TestFilesystemParameter:
    """Test filesystem parameter functionality."""

    @patch("duckalog.remote_config.FSSPEC_AVAILABLE", True)
    def test_filesystem_parameter_passed_to_load_config_from_uri(self):
        """Test that filesystem parameter is correctly passed through the call chain."""
        # Create a mock filesystem
        mock_fs = Mock()

        with patch("duckalog.remote_config.load_config_from_uri") as mock_load:
            mock_config = Mock()
            mock_load.return_value = mock_config

            # Import and call the function
            from duckalog.config import load_config

            config = load_config("s3://bucket/config.yaml", filesystem=mock_fs)

            # Verify the filesystem parameter was passed correctly
            mock_load.assert_called_once_with(
                "s3://bucket/config.yaml",
                load_sql_files=True,
                sql_file_loader=None,
                resolve_paths=False,
                filesystem=mock_fs,
            )

            assert config == mock_config

    def test_filesystem_parameter_none_behavior(self):
        """Test that None filesystem parameter doesn't affect normal operation."""
        # This should behave like the old version without filesystem parameter
        with patch("duckalog.remote_config.is_remote_uri") as mock_is_remote:
            mock_is_remote.return_value = False

            config_path = "/local/config.yaml"
            with patch("duckalog.config._load_config_from_local_file") as mock_load:
                mock_config = Mock()
                mock_load.return_value = mock_config

                from duckalog.config import load_config

                config = load_config(config_path, filesystem=None)

                # Should work without filesystem parameter
                mock_load.assert_called_once_with(config_path, None)
                assert config == mock_config

    @patch("duckalog.remote_config.FSSPEC_AVAILABLE", True)
    def test_filesystem_parameter_with_remote_uri(self):
        """Test filesystem parameter with remote URI loading."""
        mock_fs = Mock()

        # Mock successful remote content fetching
        with patch("duckalog.remote_config.fetch_remote_content") as mock_fetch:
            mock_fetch.return_value = """
            version: 1
            duckdb:
              database: ":memory:"
            views:
              - name: test_view
                sql: "SELECT 1"
            """

            config = load_config_from_uri("s3://bucket/config.yaml", filesystem=mock_fs)

            assert config.version == 1
            assert len(config.views) == 1
            assert config.views[0].name == "test_view"

            # The filesystem should be used by fetch_remote_content
            # (though in this test we're mocking it, the parameter is passed through)


if __name__ == "__main__":
    pytest.main([__file__])
