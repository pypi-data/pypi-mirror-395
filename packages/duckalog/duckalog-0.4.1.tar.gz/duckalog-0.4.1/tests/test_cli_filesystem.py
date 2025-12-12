"""Tests for CLI filesystem options."""

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
import typer

from duckalog.cli import _create_filesystem_from_options


class TestCLIFileSystem:
    """Test CLI filesystem functionality."""

    def test_create_filesystem_from_options_no_options(self):
        """Test that None is returned when no filesystem options are provided."""
        result = _create_filesystem_from_options()
        assert result is None

    def test_create_filesystem_from_options_import_error(self):
        """Test that proper error is shown when fsspec is not available."""
        with (
            patch("duckalog.cli.typer.echo") as mock_echo,
            patch.dict("sys.modules", {"fsspec": None}),
        ):
            with pytest.raises(typer.Exit):
                _create_filesystem_from_options(
                    protocol="s3", key="test", secret="test"
                )
            mock_echo.assert_called()

    def test_create_filesystem_from_options_s3_with_profile(self):
        """Test S3 filesystem creation with AWS profile."""
        with patch("duckalog.cli.fsspec") as mock_fsspec:
            mock_fs = MagicMock()
            mock_fsspec.filesystem.return_value = mock_fs

            result = _create_filesystem_from_options(
                protocol="s3", aws_profile="test-profile"
            )

            assert result == mock_fs
            mock_fsspec.filesystem.assert_called_once_with("s3", profile="test-profile")

    def test_create_filesystem_from_options_s3_with_key_secret(self):
        """Test S3 filesystem creation with access key and secret."""
        with patch("duckalog.cli.fsspec") as mock_fsspec:
            mock_fs = MagicMock()
            mock_fsspec.filesystem.return_value = mock_fs

            result = _create_filesystem_from_options(
                protocol="s3", key="test-key", secret="test-secret"
            )

            assert result == mock_fs
            mock_fsspec.filesystem.assert_called_once_with(
                "s3", key="test-key", secret="test-secret", anon=False, timeout=30
            )

    def test_create_filesystem_from_options_s3_anon(self):
        """Test S3 filesystem creation with anonymous access."""
        with patch("duckalog.cli.fsspec") as mock_fsspec:
            mock_fs = MagicMock()
            mock_fsspec.filesystem.return_value = mock_fs

            result = _create_filesystem_from_options(protocol="s3", anon=True)

            assert result == mock_fs
            mock_fsspec.filesystem.assert_called_once_with("s3", anon=True, timeout=30)

    def test_create_filesystem_from_options_github_token(self):
        """Test GitHub filesystem creation with token."""
        with patch("duckalog.cli.fsspec") as mock_fsspec:
            mock_fs = MagicMock()
            mock_fsspec.filesystem.return_value = mock_fs

            result = _create_filesystem_from_options(
                protocol="github", token="test-token"
            )

            assert result == mock_fs
            mock_fsspec.filesystem.assert_called_once_with(
                "github", token="test-token", timeout=30
            )

    def test_create_filesystem_from_options_sftp_with_key_file(self):
        """Test SFTP filesystem creation with key file."""
        with (
            patch("duckalog.cli.fsspec") as mock_fsspec,
            patch("pathlib.Path.exists", return_value=True),
        ):
            mock_fs = MagicMock()
            mock_fsspec.filesystem.return_value = mock_fs

            result = _create_filesystem_from_options(
                protocol="sftp", sftp_host="example.com", sftp_key_file="/path/to/key"
            )

            assert result == mock_fs
            mock_fsspec.filesystem.assert_called_once_with(
                "sftp",
                host="example.com",
                port=22,
                key_filename="/path/to/key",
                timeout=30,
            )

    def test_create_filesystem_from_options_sftp_missing_host(self):
        """Test that error is raised when SFTP host is missing."""
        with patch("duckalog.cli.typer.echo") as mock_echo:
            with pytest.raises(typer.Exit):
                _create_filesystem_from_options(protocol="sftp")
            mock_echo.assert_called_with(
                "SFTP protocol requires --sftp-host to be specified", err=True
            )

    def test_create_filesystem_from_options_protocol_inference_s3(self):
        """Test that protocol is inferred from AWS profile for S3."""
        with patch("duckalog.cli.fsspec") as mock_fsspec:
            mock_fs = MagicMock()
            mock_fsspec.filesystem.return_value = mock_fs

            result = _create_filesystem_from_options(aws_profile="test-profile")

            assert result == mock_fs
            mock_fsspec.filesystem.assert_called_once_with("s3", profile="test-profile")

    def test_create_filesystem_from_options_protocol_inference_github(self):
        """Test that protocol is inferred from token for GitHub."""
        with patch("duckalog.cli.fsspec") as mock_fsspec:
            mock_fs = MagicMock()
            mock_fsspec.filesystem.return_value = mock_fs

            result = _create_filesystem_from_options(token="test-token")

            assert result == mock_fs
            mock_fsspec.filesystem.assert_called_once_with(
                "github", token="test-token", timeout=30
            )

    def test_create_filesystem_from_options_no_protocol_or_options(self):
        """Test that error is raised when no protocol can be inferred."""
        with patch("duckalog.cli.typer.echo") as mock_echo:
            with pytest.raises(typer.Exit):
                _create_filesystem_from_options()
            mock_echo.assert_called_with(
                "Protocol must be specified or inferable from provided options.",
                err=True,
            )

    def test_create_filesystem_from_options_mutual_exclusivity_aws(self):
        """Test that error is raised for mutually exclusive AWS options."""
        with patch("duckalog.cli.typer.echo") as mock_echo:
            with pytest.raises(typer.Exit):
                _create_filesystem_from_options(
                    aws_profile="test-profile", key="test-key"
                )
            mock_echo.assert_called_with(
                "Cannot specify both --aws-profile and --fs-key", err=True
            )

    def test_create_filesystem_from_options_mutual_exclusivity_azure(self):
        """Test that error is raised for mutually exclusive Azure options."""
        with patch("duckalog.cli.typer.echo") as mock_echo:
            with pytest.raises(typer.Exit):
                _create_filesystem_from_options(
                    azure_connection_string="conn_str", key="test-key"
                )
            mock_echo.assert_called_with(
                "Cannot specify both --azure-connection-string and --fs-key", err=True
            )

    def test_create_filesystem_from_options_missing_gcs_credentials_file(self):
        """Test that error is raised when GCS credentials file doesn't exist."""
        with (
            patch("duckalog.cli.typer.echo") as mock_echo,
            patch("pathlib.Path.exists", return_value=False),
        ):
            with pytest.raises(typer.Exit):
                _create_filesystem_from_options(
                    protocol="gcs", gcs_credentials_file="/nonexistent/file.json"
                )
            mock_echo.assert_called_with(
                "GCS credentials file not found: /nonexistent/file.json", err=True
            )

    def test_create_filesystem_from_options_missing_sftp_key_file(self):
        """Test that error is raised when SFTP key file doesn't exist."""
        with (
            patch("duckalog.cli.typer.echo") as mock_echo,
            patch("pathlib.Path.exists", return_value=False),
        ):
            with pytest.raises(typer.Exit):
                _create_filesystem_from_options(
                    protocol="sftp",
                    sftp_host="example.com",
                    sftp_key_file="/nonexistent/key",
                )
            mock_echo.assert_called_with(
                "SFTP key file not found: /nonexistent/key", err=True
            )

    def test_create_filesystem_from_options_s3_missing_credentials(self):
        """Test that error is raised when S3 credentials are missing."""
        with patch("duckalog.cli.typer.echo") as mock_echo:
            with pytest.raises(typer.Exit):
                _create_filesystem_from_options(protocol="s3")
            mock_echo.assert_called()

    def test_create_filesystem_from_options_azure_missing_credentials(self):
        """Test that error is raised when Azure credentials are missing."""
        with patch("duckalog.cli.typer.echo") as mock_echo:
            with pytest.raises(typer.Exit):
                _create_filesystem_from_options(protocol="abfs")
            mock_echo.assert_called()

    def test_create_filesystem_from_options_filesystem_creation_error(self):
        """Test that error is raised when filesystem creation fails."""
        with (
            patch("duckalog.cli.fsspec") as mock_fsspec,
            patch("duckalog.cli.typer.echo") as mock_echo,
        ):
            mock_fsspec.filesystem.side_effect = Exception("Connection failed")

            with pytest.raises(typer.Exit):
                _create_filesystem_from_options(
                    protocol="s3", key="test", secret="test"
                )
            mock_echo.assert_called_with(
                "Failed to create filesystem for protocol 's3': Connection failed",
                err=True,
            )

    def test_cli_help_text_includes_filesystem_options(self):
        """Test that help text includes filesystem options."""
        # This test verifies that the CLI commands include filesystem options in their help
        result = subprocess.run(
            [sys.executable, "-m", "duckalog.cli", "build", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        # Check that help includes filesystem-related options
        help_output = result.stdout
        assert "--fs-protocol" in help_output
        assert "--fs-key" in help_output
        assert "--fs-secret" in help_output
        assert "--fs-token" in help_output
        assert "--aws-profile" in help_output

    def test_cli_validate_command_help_includes_filesystem_options(self):
        """Test that validate command help includes filesystem options."""
        result = subprocess.run(
            [sys.executable, "-m", "duckalog.cli", "validate", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        # Check that help includes filesystem-related options
        help_output = result.stdout
        assert "--fs-protocol" in help_output
        assert "--fs-key" in help_output

    def test_cli_generate_sql_command_help_includes_filesystem_options(self):
        """Test that generate-sql command help includes filesystem options."""
        result = subprocess.run(
            [sys.executable, "-m", "duckalog.cli", "generate-sql", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        # Check that help includes filesystem-related options
        help_output = result.stdout
        assert "--fs-protocol" in help_output
        assert "--fs-key" in help_output

    def test_cli_build_command_with_filesystem_options_structure(self):
        """Test that build command accepts filesystem options without immediate error."""
        # This test just checks that the command accepts the options without parsing errors
        # We don't test actual remote access since that would require real credentials
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "duckalog.cli",
                "build",
                "nonexistent.yaml",  # This will fail but not due to option parsing
                "--fs-protocol",
                "s3",
                "--fs-key",
                "test",
                "--fs-secret",
                "test",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        # Should fail because file doesn't exist, not because of option parsing
        assert result.returncode != 0
        assert "not found" in result.stderr or "does not exist" in result.stderr

    def test_cli_validate_command_with_filesystem_options_structure(self):
        """Test that validate command accepts filesystem options without immediate error."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "duckalog.cli",
                "validate",
                "nonexistent.yaml",
                "--fs-protocol",
                "github",
                "--fs-token",
                "test",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        # Should fail because file doesn't exist, not because of option parsing
        assert result.returncode != 0
        assert "not found" in result.stderr or "does not exist" in result.stderr

    def test_cli_generate_sql_command_with_filesystem_options_structure(self):
        """Test that generate-sql command accepts filesystem options without immediate error."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "duckalog.cli",
                "generate-sql",
                "nonexistent.yaml",
                "--fs-protocol",
                "sftp",
                "--sftp-host",
                "example.com",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        # Should fail because file doesn't exist, not because of option parsing
        assert result.returncode != 0
        assert "not found" in result.stderr or "does not exist" in result.stderr


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
