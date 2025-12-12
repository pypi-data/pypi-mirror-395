"""Tests for changelog automation workflow."""

import re
from datetime import datetime


def test_changelog_entry_generation():
    """Test changelog entry generation from commit messages."""
    print("Testing changelog entry generation...")

    # Test data simulating git log output
    test_commits = """
a1b2c3d|feat: Add automated version tagging
e4f5g6h|Fix bug in config parsing
i7j8k9l|docs: Update README with new features
m0n1o2p|refactor: Clean up code structure
q3r4s5t|test: Add unit tests for validation
u6v7w8x|chore: Update dependencies
"""

    # Simulate the changelog generation logic
    commit_entries = []
    for line in test_commits.strip().split("\n"):
        if not line or "|" not in line:
            continue
        hash_part, message = line.split("|", 1)
        hash_part = hash_part.strip()
        message = message.strip()

        # Determine change type
        if re.search(r"feat|add", message, re.IGNORECASE):
            change_type = "Added"
        elif re.search(r"fix|bugfix", message, re.IGNORECASE):
            change_type = "Fixed"
        elif re.search(r"docs|doc", message, re.IGNORECASE):
            change_type = "Changed"
        elif re.search(r"breaking|major", message, re.IGNORECASE):
            change_type = "Changed"
        else:
            change_type = "Changed"

        # Clean up commit message
        clean_message = re.sub(
            r"^(feat|fix|docs|chore|refactor|test)\((\w+)\):\s*",
            "",
            message,
            flags=re.IGNORECASE,
        )
        clean_message = clean_message.strip().capitalize()

        commit_entries.append(
            {"type": change_type, "message": clean_message, "hash": hash_part}
        )

    # Generate changelog
    changelog_entries = []
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Group by type
    types = ["Added", "Fixed", "Changed", "Deprecated", "Removed", "Security"]
    for change_type in types:
        type_entries = [e for e in commit_entries if e["type"] == change_type]
        if type_entries:
            changelog_entries.append(f"### {change_type}")
            for entry in type_entries:
                changelog_entry = f"- {entry['message']}"
                if entry["hash"]:
                    changelog_entry += f" ({entry['hash']})"
                changelog_entries.append(changelog_entry)
            changelog_entries.append("")

    # Add version header
    header = f"## [{current_date}] - 1.0.0"
    full_entry = header + "\n\n" + "\n".join(changelog_entries).strip() + "\n"

    print("Generated changelog entry:")
    print(full_entry)

    # Validate the generated changelog
    assert "## [" in full_entry, "Should have version header"
    assert "### Added" in full_entry, "Should have Added section"
    assert "### Fixed" in full_entry, "Should have Fixed section"
    assert "### Changed" in full_entry, "Should have Changed section"
    assert "Feat: add automated version tagging" in full_entry, (
        "Should include feature description"
    )
    assert "Fix bug in config parsing" in full_entry, (
        "Should include bug fix description"
    )
    assert "a1b2c3d" in full_entry, "Should include commit hash"

    print("✅ Changelog entry generation test passed")


def test_version_comparison():
    """Test version comparison logic."""
    print("Testing version comparison...")

    def compare_versions(current, latest):
        """Compare two semantic versions."""

        def parse_version(v):
            return [int(x) for x in v.split(".")]

        current_parts = parse_version(current)
        latest_parts = parse_version(latest)

        # Pad shorter version with zeros
        max_len = max(len(current_parts), len(latest_parts))
        current_parts.extend([0] * (max_len - len(current_parts)))
        latest_parts.extend([0] * (max_len - len(latest_parts)))

        # Compare part by part
        for i in range(max_len):
            if current_parts[i] > latest_parts[i]:
                return True  # current is newer
            elif current_parts[i] < latest_parts[i]:
                return False  # current is older

        return False  # equal versions

    test_cases = [
        ("0.1.0", "0.0.9", True),  # Newer
        ("0.1.0", "0.1.0", False),  # Same
        ("0.1.0", "0.2.0", False),  # Older
        ("1.0.0", "0.9.9", True),  # Newer major
        ("1.1.0", "1.0.9", True),  # Newer minor
        ("1.0.1", "1.0.0", True),  # Newer patch
    ]

    for current, latest, expected in test_cases:
        result = compare_versions(current, latest)

        if result == expected:
            print(f"✅ {current} vs {latest}: {result} (expected {expected})")
        else:
            print(f"❌ {current} vs {latest}: {result} (expected {expected})")
            assert False, f"Version comparison failed for {current} vs {latest}"


def test_keep_a_changelog_format():
    """Test compliance with Keep a Changelog format."""
    print("Testing Keep a Changelog format compliance...")

    # Sample changelog content
    sample_content = """# Changelog

## [1.0.1] - 2024-01-15

### Added
- Automated version tagging workflow
- Changelog generation from git history (abc123)

### Fixed
- Bug in config parsing (def456)

## [1.0.0] - 2024-01-01

### Added
- Initial release
- Basic DuckDB catalog functionality
"""

    # Test format compliance
    lines = sample_content.strip().split("\n")

    # Check for proper headers
    assert lines[0] == "# Changelog", "Should start with # Changelog"
    assert lines[2].startswith("## ["), "Version headers should be ## [version] - date"
    assert "[1.0.1]" in lines[2], "Should include version in brackets"
    assert "2024-01-15" in lines[2], "Should include date"

    # Check for section headers
    section_headers = [line for line in lines if line.startswith("### ")]
    valid_sections = [
        "### Added",
        "### Fixed",
        "### Changed",
        "### Deprecated",
        "### Removed",
        "### Security",
    ]

    for header in section_headers:
        assert header in valid_sections, f"Invalid section header: {header}"

    # Check for proper bullet points
    bullet_lines = [line for line in lines if line.strip().startswith("- ")]
    for bullet in bullet_lines:
        assert bullet.startswith("- "), "Bullets should start with '- '"

    print("✅ Keep a Changelog format compliance test passed")


def test_changelog_update_logic():
    """Test CHANGELOG.md update logic."""
    print("Testing CHANGELOG.md update logic...")

    # Test with existing CHANGELOG
    existing_changelog = """# Changelog

## [1.0.0] - 2024-01-01

### Added
- Initial release
"""

    # New changelog entry
    new_entry = """## [1.0.1] - 2024-01-15

### Added
- Automated version tagging workflow

### Fixed
- Bug in config parsing
"""

    # Test update logic
    lines = existing_changelog.strip().split("\n")
    insert_pos = 2  # After "# Changelog" and blank line

    # Combine content
    updated_content = (
        lines[:insert_pos] + [""] + [new_entry.strip()] + lines[insert_pos:]
    )
    full_updated = "\n".join(updated_content)

    print("Updated changelog:")
    print(full_updated)

    # Validate the update
    assert "## [1.0.1]" in full_updated, "Should include new version"
    assert "## [1.0.0]" in full_updated, "Should preserve existing version"
    assert "Automated version tagging workflow" in full_updated, (
        "Should include new entry"
    )
    assert "Initial release" in full_updated, "Should preserve existing entry"

    # Verify proper ordering (newest first)
    lines = full_updated.strip().split("\n")
    version_lines = [line for line in lines if line.startswith("## [")]
    assert version_lines[0] == "## [1.0.1] - 2024-01-15", (
        "Newest version should be first"
    )

    print("✅ CHANGELOG.md update logic test passed")


def test_commit_message_categorization():
    """Test commit message categorization for changelog."""
    print("Testing commit message categorization...")

    test_messages = [
        ("feat: Add new feature", "Added"),
        ("feat: add user authentication", "Added"),
        ("add: new configuration option", "Added"),
        ("fix: resolve parsing error", "Fixed"),
        ("Fix authentication bug", "Fixed"),
        ("bugfix: user login issue", "Fixed"),
        ("docs: update README", "Changed"),
        ("Update documentation", "Changed"),
        ("refactor: improve code structure", "Changed"),
        ("Breaking: change API", "Changed"),
        ("BREAKING: remove old endpoint", "Changed"),
        ("chore: update dependencies", "Changed"),
        ("test: add unit tests", "Added"),
        ("deprecate: old function", "Deprecated"),
        ("remove: legacy code", "Removed"),
        ("security: fix vulnerability", "Fixed"),
    ]

    for message, expected_type in test_messages:
        # Simulate categorization logic
        if re.search(r"feat|add", message, re.IGNORECASE):
            actual_type = "Added"
        elif re.search(r"fix|bugfix", message, re.IGNORECASE):
            actual_type = "Fixed"
        elif re.search(r"docs|doc", message, re.IGNORECASE):
            actual_type = "Changed"
        elif re.search(r"breaking|major", message, re.IGNORECASE):
            actual_type = "Changed"
        elif re.search(r"deprecate", message, re.IGNORECASE):
            actual_type = "Deprecated"
        elif re.search(r"remove", message, re.IGNORECASE):
            actual_type = "Removed"
        elif re.search(r"security", message, re.IGNORECASE):
            actual_type = "Security"
        else:
            actual_type = "Changed"

        if actual_type == expected_type:
            print(f"✅ {message} -> {actual_type}")
        else:
            print(f"❌ {message} -> {actual_type} (expected {expected_type})")
            assert False, f"Categorization failed for: {message}"


if __name__ == "__main__":
    print("🧪 Running changelog automation tests\n")

    # Run all tests
    test_changelog_entry_generation()
    print()
    test_version_comparison()
    print()
    test_keep_a_changelog_format()
    print()
    test_changelog_update_logic()
    print()
    test_commit_message_categorization()

    print("\n✅ All changelog automation tests passed!")
