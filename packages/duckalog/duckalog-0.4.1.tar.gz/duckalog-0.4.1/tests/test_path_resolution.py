"""Tests for path resolution utilities and configuration integration."""

import os
import tempfile
from pathlib import Path
from typing import List

import pytest
import yaml

from duckalog.config import (
    Config,
    load_config,
)
from duckalog.errors import ConfigError, PathResolutionError
from duckalog.config import (
    detect_path_type,
    is_relative_path,
    is_windows_path_absolute,
    normalize_path_for_sql,
    resolve_relative_path,
    validate_file_accessibility,
    validate_path_security,
    is_within_allowed_roots,
)


class TestPathDetection:
    """Test path detection functionality."""

    def test_is_relative_path_basic(self):
        """Test basic relative path detection."""
        # Relative paths should return True
        assert is_relative_path("data/file.parquet")
        assert is_relative_path("./data/file.parquet")
        assert is_relative_path("../data/file.parquet")
        assert is_relative_path("file.parquet")
        assert is_relative_path("subdir/file.parquet")

        # Edge cases
        assert not is_relative_path("")
        assert not is_relative_path("  ")

    def test_is_relative_path_absolute_unix(self):
        """Test absolute path detection on Unix-like systems."""
        # Absolute paths should return False
        assert not is_relative_path("/absolute/path/file.parquet")
        assert not is_relative_path("/home/user/data/file.parquet")
        assert not is_relative_path("/")

    def test_is_relative_path_windows(self):
        """Test Windows-specific path detection."""
        # Windows drive letters should be absolute
        assert not is_relative_path("C:\\data\\file.parquet")
        assert not is_relative_path("D:/data/file.parquet")
        assert not is_relative_path("c:\\Users\\file.parquet")

        # Windows UNC paths should be absolute
        assert not is_relative_path("\\\\server\\share\\file.parquet")
        assert not is_relative_path("\\\\server\\share")

    def test_is_relative_path_remote_uris(self):
        """Test remote URI detection."""
        # Remote URIs should not be relative
        assert not is_relative_path("s3://bucket/data/file.parquet")
        assert not is_relative_path("gs://bucket/data/file.parquet")
        assert not is_relative_path("http://example.com/file.parquet")
        assert not is_relative_path("https://example.com/file.parquet")
        assert not is_relative_path("ftp://example.com/file.parquet")

    def test_detect_path_type(self):
        """Test path type categorization."""
        assert detect_path_type("data/file.parquet") == "relative"
        assert detect_path_type("./data/file.parquet") == "relative"
        assert detect_path_type("../data/file.parquet") == "relative"

        assert detect_path_type("/absolute/path/file.parquet") == "absolute"
        assert detect_path_type("C:\\data\\file.parquet") == "absolute"

        assert detect_path_type("s3://bucket/file.parquet") == "remote"
        assert detect_path_type("http://example.com/file") == "remote"

        assert detect_path_type("") == "invalid"
        assert detect_path_type("  ") == "invalid"


class TestPathResolution:
    """Test path resolution functionality."""

    def test_resolve_relative_path_basic(self):
        """Test basic relative path resolution."""
        config_dir = Path("/project/config")

        # Simple relative path
        resolved = resolve_relative_path("data/file.parquet", config_dir)
        assert resolved == "/project/config/data/file.parquet"

        # Parent directory
        resolved = resolve_relative_path("../data/file.parquet", config_dir)
        assert resolved == "/project/data/file.parquet"

        # Current directory
        resolved = resolve_relative_path("./file.parquet", config_dir)
        assert resolved == "/project/config/file.parquet"

    def test_resolve_relative_path_absolute_unchanged(self):
        """Test that absolute paths remain unchanged."""
        config_dir = Path("/project/config")

        # Unix absolute path
        resolved = resolve_relative_path("/absolute/data/file.parquet", config_dir)
        assert resolved == "/absolute/data/file.parquet"

        # Windows absolute path
        resolved = resolve_relative_path("C:\\data\\file.parquet", config_dir)
        assert resolved == "C:\\data\\file.parquet"

        # Remote URI
        resolved = resolve_relative_path("s3://bucket/file.parquet", config_dir)
        assert resolved == "s3://bucket/file.parquet"

    def test_resolve_relative_path_error_cases(self):
        """Test error handling in path resolution."""
        config_dir = Path("/project/config")

        # Empty path
        with pytest.raises(ValueError, match="Path cannot be empty"):
            resolve_relative_path("", config_dir)

        # Whitespace-only path
        with pytest.raises(ValueError, match="Path cannot be empty"):
            resolve_relative_path("   ", config_dir)

    def test_is_windows_path_absolute(self):
        """Test Windows absolute path detection."""
        # Drive letter paths
        assert is_windows_path_absolute("C:\\data\\file.parquet")
        assert is_windows_path_absolute("D:/data/file.parquet")
        assert is_windows_path_absolute("c:\\Users\\file.parquet")

        # UNC paths
        assert is_windows_path_absolute("\\\\server\\share\\file.parquet")
        assert is_windows_path_absolute("\\\\server\\share")

        # Non-Windows paths
        assert not is_windows_path_absolute("/unix/path/file.parquet")
        assert not is_windows_path_absolute("relative/path/file.parquet")
        assert not is_windows_path_absolute("s3://bucket/file.parquet")


class TestPathValidation:
    """Test path security validation."""

    def test_validate_path_security_safe_paths(self):
        """Test that safe paths pass validation."""
        config_dir = Path("/project/config")

        # Safe relative paths
        assert validate_path_security("data/file.parquet", config_dir)
        assert validate_path_security("./data/file.parquet", config_dir)
        assert validate_path_security("subdir/file.parquet", config_dir)

        # Safe absolute paths within config directory
        assert validate_path_security("/project/config/data/file.parquet", config_dir)

        # Remote URIs should be considered safe
        assert validate_path_security("s3://bucket/file.parquet", config_dir)

    def test_validate_path_security_dangerous_paths(self):
        """Test that dangerous paths fail validation."""
        config_dir = Path("/project/config")

        # Directory traversal attempts
        assert not validate_path_security("../../../etc/passwd", config_dir)
        assert not validate_path_security("../outside/data/file.parquet", config_dir)
        assert not validate_path_security("/outside/data/file.parquet", config_dir)

        # Empty paths
        assert not validate_path_security("", config_dir)
        assert not validate_path_security("  ", config_dir)


class TestPathNormalization:
    """Test path normalization for SQL."""

    def test_normalize_path_for_sql_basic(self):
        """Test basic path normalization for SQL."""
        # Unix paths
        result = normalize_path_for_sql("/path/to/file.parquet")
        assert result == "'/path/to/file.parquet'"

        # Windows paths
        result = normalize_path_for_sql("C:\\path\\to\\file.parquet")
        assert result == "'C:\\path\\to\\file.parquet'"

        # Relative paths
        result = normalize_path_for_sql("data/file.parquet")
        assert result == "'data/file.parquet'"

    def test_normalize_path_for_sql_quoting(self):
        """Test that paths with quotes are properly escaped."""
        # Path with single quote
        result = normalize_path_for_sql("/path/file's_data.parquet")
        assert result == "'/path/file''s_data.parquet'"

        # Path with existing quotes
        result = normalize_path_for_sql('/path/file "name".parquet')
        assert result == "'/path/file \"name\".parquet'"

    def test_normalize_path_for_sql_error_cases(self):
        """Test error handling in path normalization."""
        # Empty path
        with pytest.raises(ValueError, match="Path cannot be empty"):
            normalize_path_for_sql("")


class TestFileAccessibility:
    """Test file accessibility validation."""

    def test_validate_file_accessibility_existing_file(self):
        """Test validation of existing accessible files."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            # Test existing file
            accessible, error = validate_file_accessibility(temp_path)
            assert accessible
            assert error is None
        finally:
            os.unlink(temp_path)

    def test_validate_file_accessibility_nonexistent_file(self):
        """Test validation of non-existent files."""
        # Non-existent file
        accessible, error = validate_file_accessibility("/nonexistent/file.parquet")
        assert not accessible
        assert "does not exist" in error

    def test_validate_file_accessibility_directory(self):
        """Test validation when path points to a directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Directory should not be considered accessible as a file
            accessible, error = validate_file_accessibility(temp_dir)
            assert not accessible
            assert "not a file" in error.lower()

    def test_validate_file_accessibility_invalid_paths(self):
        """Test validation of invalid paths."""
        # Empty path
        accessible, error = validate_file_accessibility("")
        assert not accessible
        assert "cannot be empty" in error.lower()


class TestConfigIntegration:
    """Test path resolution integration with configuration loading."""

    def test_load_config_with_relative_paths(self):
        """Test loading a config with relative paths."""
        # Create a temporary directory structure
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_dir = temp_path / "config"
            data_dir = temp_path / "data"

            config_dir.mkdir()
            data_dir.mkdir()

            # Create a dummy data file
            data_file = data_dir / "test.parquet"
            data_file.write_text("dummy parquet data")

            # Create config with relative path
            config_data = {
                "version": 1,
                "duckdb": {"database": "test.duckdb"},
                "views": [
                    {
                        "name": "test_view",
                        "source": "parquet",
                        "uri": "data/test.parquet",
                        "description": "Test view with relative path",
                    }
                ],
            }

            config_file = config_dir / "catalog.yaml"
            with open(config_file, "w") as f:
                yaml.dump(config_data, f)

            # Load config with path resolution enabled
            config = load_config(str(config_file), resolve_paths=True)

            # Verify that the path was resolved
            assert len(config.views) == 1
            view = config.views[0]
            assert view.name == "test_view"
            assert view.source == "parquet"

            # The URI should be resolved to absolute path (relative to config file)
            expected_uri = str((config_dir / "data/test.parquet").resolve())
            assert view.uri == expected_uri
            assert view.uri.startswith("/")  # Should be absolute

    def test_load_config_with_absolute_paths_unchanged(self):
        """Test that absolute paths are not modified during resolution."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_dir = temp_path / "config"
            data_dir = temp_path / "data"

            config_dir.mkdir()
            data_dir.mkdir()

            # Create a dummy data file
            data_file = data_dir / "test.parquet"
            data_file.write_text("dummy parquet data")

            # Create config with absolute path
            config_data = {
                "version": 1,
                "duckdb": {"database": "test.duckdb"},
                "views": [
                    {
                        "name": "test_view",
                        "source": "parquet",
                        "uri": str(data_file.absolute()),
                        "description": "Test view with absolute path",
                    }
                ],
            }

            config_file = config_dir / "catalog.yaml"
            with open(config_file, "w") as f:
                yaml.dump(config_data, f)

            # Load config with path resolution enabled
            config = load_config(str(config_file), resolve_paths=True)

            # Verify that the absolute path was not modified
            view = config.views[0]
            assert view.uri == str(data_file.absolute())

    def test_load_config_without_path_resolution(self):
        """Test that path resolution can be disabled."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_dir = temp_path / "config"
            data_dir = temp_path / "data"

            config_dir.mkdir()

            # Create config with relative path
            config_data = {
                "version": 1,
                "duckdb": {"database": "test.duckdb"},
                "views": [
                    {
                        "name": "test_view",
                        "source": "parquet",
                        "uri": "data/test.parquet",
                        "description": "Test view with relative path",
                    }
                ],
            }

            config_file = config_dir / "catalog.yaml"
            with open(config_file, "w") as f:
                yaml.dump(config_data, f)

            # Load config with path resolution disabled
            config = load_config(str(config_file), resolve_paths=False)

            # Verify that the path was not resolved
            view = config.views[0]
            assert view.uri == "data/test.parquet"  # Should remain relative

    def test_load_config_with_attachment_paths(self):
        """Test that attachment paths are also resolved."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_dir = temp_path / "config"
            data_dir = temp_path / "data"

            config_dir.mkdir()
            data_dir.mkdir()

            # Create dummy database files
            duckdb_file = data_dir / "reference.duckdb"
            sqlite_file = data_dir / "users.db"
            duckdb_file.write_text("dummy duckdb")
            sqlite_file.write_text("dummy sqlite")

            # Create config with attachment paths
            config_data = {
                "version": 1,
                "duckdb": {"database": "test.duckdb"},
                "views": [
                    {
                        "name": "test_view",
                        "sql": "SELECT 1 as test",
                        "description": "Test view",
                    }
                ],
                "attachments": {
                    "duckdb": [
                        {
                            "alias": "ref_db",
                            "path": "data/reference.duckdb",
                            "read_only": True,
                        }
                    ],
                    "sqlite": [{"alias": "users_db", "path": "./data/users.db"}],
                },
            }

            config_file = config_dir / "catalog.yaml"
            with open(config_file, "w") as f:
                yaml.dump(config_data, f)

            # Load config with path resolution enabled
            config = load_config(str(config_file), resolve_paths=True)

            # Verify that attachment paths were resolved
            assert len(config.attachments.duckdb) == 1
            assert len(config.attachments.sqlite) == 1

            duckdb_attachment = config.attachments.duckdb[0]
            sqlite_attachment = config.attachments.sqlite[0]

            expected_duckdb_path = str((config_dir / "data/reference.duckdb").resolve())
            expected_sqlite_path = str((config_dir / "data/users.db").resolve())

            assert duckdb_attachment.path == expected_duckdb_path
            assert sqlite_attachment.path == expected_sqlite_path

    def test_load_config_with_security_violation(self):
        """Test that security violations are properly detected and reported."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_dir = temp_path / "config"

            config_dir.mkdir()

            # Create config with malicious relative path
            config_data = {
                "version": 1,
                "duckdb": {"database": "test.duckdb"},
                "views": [
                    {
                        "name": "malicious_view",
                        "source": "parquet",
                        "uri": "../../../etc/passwd",  # Directory traversal attempt
                        "description": "Malicious view",
                    }
                ],
            }

            config_file = config_dir / "catalog.yaml"
            with open(config_file, "w") as f:
                yaml.dump(config_data, f)

            # Loading should fail due to security violation
            with pytest.raises(ConfigError, match="Path resolution failed"):
                load_config(str(config_file), resolve_paths=True)


class TestConfigValidation:
    """Test path resolution with configuration validation."""

    def test_invalid_relative_path_in_view(self):
        """Test that invalid paths in views are caught during validation."""
        # Test with empty URI
        with pytest.raises(ValueError, match="requires a 'uri'"):
            from duckalog.config import ViewConfig

            ViewConfig(name="test", source="parquet", uri="")

    def test_path_resolution_preserves_original_path_in_errors(self):
        """Test that original paths are preserved in error messages."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = Path(temp_dir)

            # Test with a path that would fail security validation (directory traversal)
            try:
                resolve_relative_path("../../../etc/passwd", config_dir)
                assert False, "Should have raised ValueError"
            except ValueError as exc:
                # Error message should include the problematic path
                assert "etc/passwd" in str(exc)


# Integration test examples that could be run manually
def manual_test_example():
    """Manual test example to verify path resolution works end-to-end."""
    print(
        "This is a manual test example. Run it to verify path resolution works end-to-end."
    )

    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create directory structure
        (temp_path / "config").mkdir()
        (temp_path / "data").mkdir()

        # Create sample data file
        data_file = temp_path / "data" / "sample.parquet"
        data_file.write_text("sample data")

        # Create catalog configuration with relative paths
        config_content = f"""
version: 1

duckdb:
  database: {temp_path}/config/catalog.duckdb

views:
  - name: sample_data
    source: parquet
    uri: data/sample.parquet
    description: "Sample data with relative path"

attachments:
  duckdb:
    - alias: temp_db
      path: data/sample.parquet
      read_only: true
"""

        config_file = temp_path / "config" / "catalog.yaml"
        with open(config_file, "w") as f:
            f.write(config_content)

        try:
            # Load the configuration with path resolution
            config = load_config(str(config_file), resolve_paths=True)

            print(f"✅ Successfully loaded config with {len(config.views)} views")
            print(f"📁 View URI resolved to: {config.views[0].uri}")
            print(f"🔗 Attachment resolved to: {config.attachments.duckdb[0].path}")

            # Verify paths are absolute
            assert Path(config.views[0].uri).is_absolute()
            assert Path(config.attachments.duckdb[0].path).is_absolute()

            print("✅ All paths are absolute and resolved correctly!")

        except Exception as e:
            print(f"❌ Failed to load config: {e}")
            raise


class TestRootBasedPathSecurity:
    """Test the new root-based path security model."""

    def test_is_within_allowed_roots_basic_valid(self):
        """Test valid paths within allowed roots."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)

            # Create subdirectory structure
            data_dir = config_dir / "data"
            data_dir.mkdir()
            safe_file = data_dir / "file.parquet"
            safe_file.write_text("test")

            # Test paths within allowed root
            assert is_within_allowed_roots(str(safe_file), [config_dir])
            assert is_within_allowed_roots(str(data_dir), [config_dir])

            # Test single file in root
            root_file = config_dir / "config.yaml"
            root_file.write_text("test")
            assert is_within_allowed_roots(str(root_file), [config_dir])

    def test_is_within_allowed_roots_basic_invalid(self):
        """Test invalid paths outside allowed roots."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)

            # Test path outside allowed root
            outside_path = "/tmp/malicious_file.parquet"
            assert not is_within_allowed_roots(outside_path, [config_dir])

            # Test path in different directory
            different_dir = Path("/var/log")
            assert not is_within_allowed_roots(str(different_dir), [config_dir])

    def test_is_within_allowed_roots_traversal_attacks(self):
        """Test path traversal attacks are blocked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)

            # Test various traversal attack patterns
            malicious_paths = [
                "../../../etc/passwd",
                "../../../../../../etc/shadow",
                "../..//../etc/passwd",
                "..\\..\\..\\windows\\system32\\config\\sam",
                "../../../../../../../usr/bin/python",
                "../../../../../../../sbin/init",
            ]

            for malicious_path in malicious_paths:
                # These should raise ValueError due to path resolution or return False
                try:
                    result = is_within_allowed_roots(malicious_path, [config_dir])
                    assert not result, f"Path '{malicious_path}' should be rejected"
                except ValueError:
                    # Path resolution failed, which is also acceptable
                    pass

    def test_is_within_allowed_roots_multiple_roots(self):
        """Test validation with multiple allowed roots."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)

            # Create additional allowed root
            other_dir = Path(tmpdir) / "other"
            other_dir.mkdir()

            allowed_roots = [config_dir, other_dir]

            # Test paths in each root
            config_file = config_dir / "config.yaml"
            config_file.write_text("test")
            assert is_within_allowed_roots(str(config_file), allowed_roots)

            other_file = other_dir / "data.csv"
            other_file.write_text("test")
            assert is_within_allowed_roots(str(other_file), allowed_roots)

            # Test path outside all roots
            outside_path = "/tmp/file.txt"
            assert not is_within_allowed_roots(outside_path, allowed_roots)

    def test_is_within_allowed_roots_symlink_resolution(self):
        """Test that symlinks are properly resolved during validation."""
        # Skip on systems that don't support symlinks
        if not hasattr(os, "symlink"):
            pytest.skip("System doesn't support symlinks")

        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)

            # Create a file outside the allowed root
            outside_dir = Path(tmpdir) / "outside"
            outside_dir.mkdir()
            outside_file = outside_dir / "secret.txt"
            outside_file.write_text("secret")

            # Create symlink inside allowed root pointing outside
            symlink_path = config_dir / "symlink_to_secret"
            try:
                os.symlink(outside_file, symlink_path)

                # The symlink should be rejected because it points outside allowed root
                result = is_within_allowed_roots(str(symlink_path), [config_dir])
                assert not result, (
                    "Symlink pointing outside allowed root should be rejected"
                )

            except (OSError, NotImplementedError):
                # Symlink creation failed (Windows with restricted privileges, etc.)
                pytest.skip("Cannot create symlink on this system")

    def test_is_within_allowed_roots_invalid_paths(self):
        """Test handling of invalid or undecodable paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)

            # Test invalid paths that cannot be resolved
            invalid_paths = [
                "",  # Empty path
                "\x00invalid",  # Null bytes
                "///invalid???",  # Invalid characters
            ]

            for invalid_path in invalid_paths:
                with pytest.raises(ValueError, match="Cannot resolve path"):
                    is_within_allowed_roots(invalid_path, [config_dir])

    def test_is_within_allowed_roots_cross_platform(self):
        """Test cross-platform path handling."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)

            # Test Unix-style paths
            unix_path = tmpdir + "/subdir/file.parquet"
            assert is_within_allowed_roots(unix_path, [config_dir])

            # Test paths with mixed separators (if applicable)
            mixed_path = tmpdir + "\\subdir\\file.parquet"
            result = is_within_allowed_roots(mixed_path, [config_dir])
            # This should work on Unix (treating backslash as regular char)
            # or fail gracefully on Windows

            # Test relative paths that resolve within root
            relative_path = "data/file.parquet"
            os.makedirs(os.path.join(tmpdir, "data"), exist_ok=True)
            full_relative = os.path.join(tmpdir, relative_path)
            Path(full_relative).touch()

            assert is_within_allowed_roots(full_relative, [config_dir])

    def test_resolve_relative_path_uses_new_security_model(self):
        """Test that resolve_relative_path uses the new root-based security model."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)

            # Test valid relative path
            valid_relative = "data/file.parquet"
            os.makedirs(os.path.join(tmpdir, "data"), exist_ok=True)

            resolved = resolve_relative_path(valid_relative, config_dir)
            assert resolved.startswith(str(config_dir))

            # Test that excessive traversal is blocked with new model
            with pytest.raises(ValueError, match="outside the allowed root"):
                resolve_relative_path("../../../etc/passwd", config_dir)

    def test_validate_path_security_uses_new_model(self):
        """Test that validate_path_security uses the new root-based model."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)

            # Test valid path
            valid_path = os.path.join(tmpdir, "data/file.parquet")
            os.makedirs(os.path.dirname(valid_path), exist_ok=True)
            Path(valid_path).touch()

            assert validate_path_security(valid_path, config_dir)

            # Test invalid path
            invalid_path = "/etc/passwd"
            assert not validate_path_security(invalid_path, config_dir)


if __name__ == "__main__":
    # Run the manual test when executed directly
    manual_test_example()
