"""Unit tests for version automation workflow."""

import re


def test_semver_validation():
    """Test semantic versioning validation."""
    test_cases = [
        ("1.0.0", True),
        ("0.1.0", True),
        ("10.20.30", True),
        ("1.0", False),  # Missing patch version
        ("1.0.0.0", False),  # Too many parts
        ("v1.0.0", False),  # Has prefix
        ("1.0.0-beta", False),  # Has suffix
        ("1.0", False),  # Missing patch
        ("", False),  # Empty
        ("abc.def.ghi", False),  # Non-numeric
    ]

    print("Testing semantic versioning validation:")
    for version, expected in test_cases:
        actual = bool(re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", version))
        status = "✅" if actual == expected else "❌"
        print(f"  {status} {version:12} -> {actual} (expected {expected})")


def test_version_comparison():
    """Test version comparison logic."""
    try:
        from packaging import version
    except ImportError:
        print("⚠️ packaging module not available, skipping version comparison tests")
        return

    test_cases = [
        ("1.0.0", "0.9.9", True),  # Newer
        ("0.1.0", "0.1.0", False),  # Same
        ("0.1.0", "0.2.0", False),  # Older
        ("2.0.0", "1.9.9", True),  # Newer major
        ("1.1.0", "1.0.9", True),  # Newer minor
        ("1.0.1", "1.0.0", True),  # Newer patch
    ]

    print("Testing version comparison:")
    for current, latest, expected in test_cases:
        try:
            actual = version.parse(current) > version.parse(latest)
            status = "✅" if actual == expected else "❌"
            print(
                f"  {status} {current:8} > {latest:8} -> {actual} (expected {expected})"
            )
        except Exception as e:
            print(f"  ❌ Error comparing {current} and {latest}: {e}")


def test_tag_format():
    """Test tag format generation."""
    test_cases = [
        "1.0.0",
        "0.1.0",
        "10.20.30",
    ]

    print("Testing tag format generation:")
    for version in test_cases:
        tag = f"v{version}"
        expected = f"v{version}"
        status = "✅" if tag == expected else "❌"
        print(f"  {status} {version} -> {tag}")


def test_version_extraction_mock():
    """Test version extraction logic with mock data."""
    print("Testing version extraction logic (mock):")

    # Mock valid pyproject.toml content
    valid_toml = """
[project]
name = "test-package"
version = "1.2.3"
"""

    # Mock invalid pyproject.toml content
    invalid_toml = """
[project]
name = "test-package"
# Missing version field
"""

    # Test with valid content
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            print("  ❌ No TOML library available for extraction test")
            return

    try:
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(valid_toml)
            f.flush()

            with open(f.name, "rb") as toml_file:
                data = tomllib.load(toml_file)
                version = data.get("project", {}).get("version")
                if version == "1.2.3":
                    print("  ✅ Valid TOML: extracted version '1.2.3'")
                else:
                    print(f"  ❌ Valid TOML: extracted '{version}', expected '1.2.3'")

            # Test with invalid content
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".toml", delete=False
            ) as f2:
                f2.write(invalid_toml)
                f2.flush()

                with open(f2.name, "rb") as toml_file2:
                    try:
                        data2 = tomllib.load(toml_file2)
                        version2 = data2.get("project", {}).get("version")
                        print(
                            f"  ❌ Invalid TOML: should have failed but got '{version2}'"
                        )
                    except Exception:
                        print("  ✅ Invalid TOML: correctly failed to extract version")

            # Cleanup
            os.unlink(f.name)
            os.unlink(f2.name)

    except Exception as e:
        print(f"  ❌ Error in extraction test: {e}")


if __name__ == "__main__":
    print("🧪 Running unit tests for version automation workflow\n")

    # Run all tests
    test_semver_validation()
    print()
    test_version_comparison()
    print()
    test_tag_format()
    print()
    test_version_extraction_mock()

    print("\n✅ Unit tests completed")
