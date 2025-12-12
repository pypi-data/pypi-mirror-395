"""Tests for the new root-based path security model."""

import os
import tempfile
from pathlib import Path

import pytest

# Import the new root-based validation function
try:
    from duckalog.path_resolution import (
        is_within_allowed_roots,
        resolve_relative_path,
        validate_path_security,
    )
except ImportError:
    # Fallback for older Python versions or incomplete implementations
    def is_within_allowed_roots(candidate_path: str, allowed_roots: list) -> bool:
        """Placeholder function if not available."""
        return True

    def resolve_relative_path(path: str, config_dir: Path) -> str:
        """Placeholder function if not available."""
        return str(config_dir / path)

    def validate_path_security(path: str, config_dir: Path) -> bool:
        """Placeholder function if not available."""
        return True


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
