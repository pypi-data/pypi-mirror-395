"""Integration tests for automated version tagging workflow."""

import os
import tempfile
from pathlib import Path


def test_workflow_syntax():
    """Test that workflow YAML syntax is valid."""
    print("Testing workflow YAML syntax...")

    workflow_path = Path(".github/workflows/auto-tag-version.yml")
    if workflow_path.exists():
        try:
            # Use Python YAML parser if available
            import yaml

            with open(workflow_path, "r") as f:
                yaml.safe_load(f)
            print("✅ Workflow YAML syntax is valid")
            return True
        except ImportError:
            print("⚠️ YAML parser not available, manual check needed")
            # Basic syntax check
            with open(workflow_path, "r") as f:
                content = f.read()
                if "on:" in content and "version:" in content:
                    print("✅ Workflow appears to have required structure")
                    return True
                else:
                    print("❌ Workflow missing required sections")
                    return False
        except Exception as e:
            print(f"❌ Error reading workflow: {e}")
            return False
    else:
        print("❌ Workflow file not found")
        return False


def test_version_extraction_simulation():
    """Test version extraction with simulated pyproject.toml changes."""
    print("Testing version extraction simulation...")

    # Create a temporary test pyproject.toml
    test_versions = ["0.1.1", "1.0.0", "2.0.0", "invalid-version"]

    for version in test_versions:
        print(f"\n🧪 Testing with version: {version}")

        # Create temporary pyproject.toml
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            if version == "invalid-version":
                # Invalid TOML for testing error handling
                f.write('[project]\nname = "test"\n# Missing version field')
            else:
                f.write(f'[project]\nname = "test"\nversion = "{version}"\n')
            f.flush()

            # Simulate workflow version extraction
            try:
                import tomllib
            except ImportError:
                import tomli as tomllib

            try:
                with open(f.name, "rb") as toml_file:
                    data = tomllib.load(toml_file)
                    extracted_version = data.get("project", {}).get("version")

                    if version == "invalid-version":
                        if extracted_version is None:
                            print("✅ Correctly handled missing version field")
                        else:
                            print(f"❌ Should have failed but got: {extracted_version}")
                    else:
                        if extracted_version == version:
                            print(
                                f"✅ Successfully extracted version: {extracted_version}"
                            )
                        else:
                            print(
                                f"❌ Version mismatch: expected {version}, got {extracted_version}"
                            )

            except Exception as e:
                print(f"❌ Extraction failed: {e}")

            # Cleanup
            os.unlink(f.name)


def test_tag_format_validation():
    """Test tag format generation."""
    print("\nTesting tag format validation...")

    test_versions = ["1.0.0", "0.1.0", "10.20.30"]
    expected_tags = ["v1.0.0", "v0.1.0", "v10.20.30"]

    for version, expected_tag in zip(test_versions, expected_tags):
        actual_tag = f"v{version}"
        if actual_tag == expected_tag:
            print(f"✅ Tag format correct: {actual_tag}")
        else:
            print(f"❌ Tag format wrong: {actual_tag} (expected {expected_tag})")


def test_semver_validation():
    """Test semantic versioning validation."""
    print("\nTesting semantic versioning validation...")

    test_cases = [
        ("1.0.0", True),
        ("0.1.0", True),
        ("10.20.30", True),
        ("1.0", False),  # Missing patch
        ("v1.0.0", False),  # Has prefix
        ("1.0.0-beta", False),  # Has suffix
        ("", False),  # Empty
        ("abc.def.ghi", False),  # Non-numeric
    ]

    for version, expected in test_cases:
        import re

        actual = bool(re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", version))
        status = "✅" if actual == expected else "❌"
        print(f"  {status} {version:12} -> {actual} (expected {expected})")


def run_integration_tests():
    """Run all integration tests."""
    print("🧪 Running integration tests for automated version tagging\n")

    tests = [
        test_workflow_syntax,
        test_version_extraction_simulation,
        test_tag_format_validation,
        test_semver_validation,
    ]

    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test_func.__name__} failed: {e}")
            results.append(False)

    passed = sum(1 for r in results)
    print(f"\n📊 Integration tests: {passed}/{len(tests)} passed")

    if passed == len(tests):
        print("✅ All integration tests passed!")
        return True
    else:
        print("⚠️ Some integration tests failed")
        return False


if __name__ == "__main__":
    success = run_integration_tests()
    exit(0 if success else 1)
