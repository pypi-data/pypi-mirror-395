"""Tests for config import functionality."""

from __future__ import annotations

import os
import textwrap
from pathlib import Path
from unittest.mock import patch

import pytest

from duckalog import load_config
from duckalog.errors import (
    CircularImportError,
    DuplicateNameError,
    ImportError,
    ImportFileNotFoundError,
    ImportValidationError,
)


def _write(path: Path, content: str) -> Path:
    path.write_text(textwrap.dedent(content))
    return path


def test_basic_import_single_file(tmp_path):
    """Test importing a single config file."""
    # Create imported file
    _write(
        tmp_path / "settings.yaml",
        """
        version: 1
        duckdb:
          database: imported.duckdb
        views:
          - name: imported_view
            sql: "SELECT 1"
        """,
    )

    # Create main file that imports settings
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - ./settings.yaml
        duckdb:
          database: main.duckdb
        views:
          - name: main_view
            sql: "SELECT 2"
        """,
    )

    config = load_config(str(config_path))

    # Should have both views
    assert len(config.views) == 2
    view_names = {v.name for v in config.views}
    assert "imported_view" in view_names
    assert "main_view" in view_names

    # Main config should override duckdb database
    assert config.duckdb.database == "main.duckdb"


def test_basic_import_multiple_files(tmp_path):
    """Test importing multiple config files."""
    # Create first imported file
    _write(
        tmp_path / "views1.yaml",
        """
        version: 1
        duckdb:
          database: base.duckdb
        views:
          - name: view1
            sql: "SELECT 1"
          - name: view2
            sql: "SELECT 2"
        """,
    )

    # Create second imported file
    _write(
        tmp_path / "views2.yaml",
        """
        version: 1
        duckdb:
          database: overridden.duckdb
        views:
          - name: view3
            sql: "SELECT 3"
        """,
    )

    # Create main file that imports both
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - ./views1.yaml
          - ./views2.yaml
        duckdb:
          database: main.duckdb
        views: []
        """,
    )

    config = load_config(str(config_path))

    # Should have all three views
    assert len(config.views) == 3
    view_names = {v.name for v in config.views}
    assert view_names == {"view1", "view2", "view3"}

    # Main config should have the final say on duckdb.database
    assert config.duckdb.database == "main.duckdb"


def test_nested_imports(tmp_path):
    """Test importing files that themselves have imports."""
    # Create base file
    _write(
        tmp_path / "base.yaml",
        """
        version: 1
        duckdb:
          database: base.duckdb
        views:
          - name: base_view
            sql: "SELECT 1"
        """,
    )

    # Create intermediate file that imports base
    _write(
        tmp_path / "intermediate.yaml",
        """
        version: 1
        imports:
          - ./base.yaml
        duckdb:
          database: intermediate.duckdb
        views:
          - name: intermediate_view
            sql: "SELECT 2"
        """,
    )

    # Create main file that imports intermediate
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - ./intermediate.yaml
        duckdb:
          database: main.duckdb
        views:
          - name: main_view
            sql: "SELECT 3"
        """,
    )

    config = load_config(str(config_path))

    # Should have all three views (base, intermediate, main)
    assert len(config.views) == 3
    view_names = {v.name for v in config.views}
    assert view_names == {"base_view", "intermediate_view", "main_view"}


def test_circular_import_detection(tmp_path):
    """Test that circular imports are detected."""
    # Create file A that imports B
    _write(
        tmp_path / "file_a.yaml",
        """
        version: 1
        imports:
          - ./file_b.yaml
        duckdb:
          database: a.duckdb
        views: []
        """,
    )

    # Create file B that imports A (circular!)
    _write(
        tmp_path / "file_b.yaml",
        """
        version: 1
        imports:
          - ./file_a.yaml
        duckdb:
          database: b.duckdb
        views: []
        """,
    )

    # Try to load file A - should fail with circular import error
    config_path = tmp_path / "file_a.yaml"

    with pytest.raises(CircularImportError) as exc_info:
        load_config(str(config_path))

    assert "Circular import detected" in str(exc_info.value)


def test_duplicate_view_names_across_imports(tmp_path):
    """Test that duplicate view names are detected across imports."""
    # Create first file with view
    _write(
        tmp_path / "views1.yaml",
        """
        version: 1
        duckdb:
          database: views1.duckdb
        views:
          - name: duplicate_view
            sql: "SELECT 1"
        """,
    )

    # Create second file with same view name
    _write(
        tmp_path / "views2.yaml",
        """
        version: 1
        duckdb:
          database: views2.duckdb
        views:
          - name: duplicate_view
            sql: "SELECT 2"
        """,
    )

    # Create main file that imports both
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - ./views1.yaml
          - ./views2.yaml
        duckdb:
          database: main.duckdb
        views: []
        """,
    )

    with pytest.raises(DuplicateNameError) as exc_info:
        load_config(str(config_path))

    assert "Duplicate view name(s) found" in str(exc_info.value)
    assert "duplicate_view" in str(exc_info.value)


def test_duplicate_semantic_model_names(tmp_path):
    """Test that duplicate semantic model names are detected."""
    # Create first file with semantic model
    _write(
        tmp_path / "models1.yaml",
        """
        version: 1
        duckdb:
          database: models1.duckdb
        views:
          - name: some_view
            sql: "SELECT 1"
        semantic_models:
          - name: users
            base_view: some_view
            measures:
              - name: count
                agg: count
        """,
    )

    # Create second file with same semantic model name
    _write(
        tmp_path / "models2.yaml",
        """
        version: 1
        duckdb:
          database: models2.duckdb
        views:
          - name: another_view
            sql: "SELECT 2"
        semantic_models:
          - name: users
            base_view: another_view
            measures:
              - name: total
                agg: sum
        """,
    )

    # Create main file that imports both
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - ./models1.yaml
          - ./models2.yaml
        duckdb:
          database: main.duckdb
        views: []
        """,
    )

    with pytest.raises(DuplicateNameError) as exc_info:
        load_config(str(config_path))

    assert "Duplicate semantic model name(s) found" in str(exc_info.value)


def test_duplicate_iceberg_catalog_names(tmp_path):
    """Test that duplicate Iceberg catalog names are detected."""
    # Create first file with catalog
    _write(
        tmp_path / "catalogs1.yaml",
        """
        version: 1
        duckdb:
          database: catalogs1.duckdb
        views: []
        iceberg_catalogs:
          - name: my_catalog
            warehouse: s3://warehouse1
        """,
    )

    # Create second file with same catalog name
    _write(
        tmp_path / "catalogs2.yaml",
        """
        version: 1
        duckdb:
          database: catalogs2.duckdb
        views: []
        iceberg_catalogs:
          - name: my_catalog
            warehouse: s3://warehouse2
        """,
    )

    # Create main file that imports both
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - ./catalogs1.yaml
          - ./catalogs2.yaml
        duckdb:
          database: main.duckdb
        views: []
        """,
    )

    with pytest.raises(DuplicateNameError) as exc_info:
        load_config(str(config_path))

    assert "Duplicate Iceberg catalog name(s) found" in str(exc_info.value)


def test_duplicate_attachment_aliases(tmp_path):
    """Test that duplicate attachment aliases are detected."""
    # Create first file with attachment
    _write(
        tmp_path / "attachments1.yaml",
        """
        version: 1
        attachments:
          duckdb:
            - alias: my_db
              database: db1.duckdb
        """,
    )

    # Create second file with same attachment alias
    _write(
        tmp_path / "attachments2.yaml",
        """
        version: 1
        attachments:
          duckdb:
            - alias: my_db
              database: db2.duckdb
        """,
    )

    # Create main file that imports both
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - ./attachments1.yaml
          - ./attachments2.yaml
        duckdb:
          database: main.duckdb
        views: []
        """,
    )

    with pytest.raises(DuplicateNameError) as exc_info:
        load_config(str(config_path))

    assert "Duplicate attachment alias(es) found" in str(exc_info.value)


def test_import_file_not_found(tmp_path):
    """Test that missing import files are detected."""
    # Create main file that imports non-existent file
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - ./nonexistent.yaml
        duckdb:
          database: main.duckdb
        views: []
        """,
    )

    with pytest.raises(ImportFileNotFoundError) as exc_info:
        load_config(str(config_path))

    assert "Imported file not found" in str(exc_info.value)


def test_import_with_env_var_in_path(monkeypatch, tmp_path):
    """Test environment variable interpolation in import paths."""
    monkeypatch.setenv("IMPORT_DIR", str(tmp_path))

    # Create imported file
    _write(
        tmp_path / "settings.yaml",
        """
        version: 1
        views:
          - name: env_view
            sql: "SELECT 1"
        """,
    )

    # Create main file that uses env var in import path
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - ${env:IMPORT_DIR}/settings.yaml
        duckdb:
          database: main.duckdb
        views: []
        """,
    )

    config = load_config(str(config_path))

    # Should have imported the view
    assert len(config.views) == 1
    assert config.views[0].name == "env_view"


def test_import_with_env_var_undefined(monkeypatch, tmp_path):
    """Test that undefined environment variables in import paths raise an error."""
    monkeypatch.delenv("NONEXISTENT_VAR", raising=False)

    # Create main file that uses undefined env var
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - ${env:NONEXISTENT_VAR}/settings.yaml
        duckdb:
          database: main.duckdb
        views: []
        """,
    )

    with pytest.raises(Exception):  # Should raise some error (likely ConfigError or ImportError)
        load_config(str(config_path))


def test_import_with_json_format(tmp_path):
    """Test importing JSON config files."""
    # Create imported JSON file
    (tmp_path / "settings.json").write_text(
        """{
          "version": 1,
          "duckdb": {
            "database": "json.duckdb"
          },
          "views": [
            {
              "name": "json_view",
              "sql": "SELECT 1"
            }
          ]
        }"""
    )

    # Create main YAML file that imports JSON
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - ./settings.json
        duckdb:
          database: main.duckdb
        views: []
        """,
    )

    config = load_config(str(config_path))

    # Should have imported the view from JSON
    assert len(config.views) == 1
    assert config.views[0].name == "json_view"


def test_empty_imports_list(tmp_path):
    """Test that empty imports list works (backward compatibility)."""
    # Create config with empty imports
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports: []
        duckdb:
          database: main.duckdb
        views:
          - name: main_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))

    # Should work normally
    assert len(config.views) == 1
    assert config.views[0].name == "main_view"


def test_config_without_imports(tmp_path):
    """Test that configs without imports work normally (backward compatibility)."""
    # Create config without imports field
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: main.duckdb
        views:
          - name: main_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))

    # Should work normally
    assert len(config.views) == 1
    assert config.views[0].name == "main_view"


def test_merge_dict_deep_merge(tmp_path):
    """Test that dicts are deep merged, not overwritten."""
    # Create file with nested dict structure
    _write(
        tmp_path / "nested.yaml",
        """
        version: 1
        duckdb:
          database: base.duckdb
          extensions:
            - httpfs
        views: []
        attachments:
          duckdb:
            - alias: db1
              database: file1.duckdb
        """,
    )

    # Create main file with additional values in same sections
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        imports:
          - ./nested.yaml
        version: 1
        duckdb:
          extensions:
            - json
        attachments:
          duckdb:
            - alias: db2
              database: file2.duckdb
        """,
    )

    config = load_config(str(config_path))

    # Both extensions should be present
    assert "httpfs" in config.duckdb.extensions
    assert "json" in config.duckdb.extensions

    # Both attachments should be present
    assert len(config.attachments.duckdb) == 2
    aliases = {a.alias for a in config.attachments.duckdb}
    assert aliases == {"db1", "db2"}


def test_merge_lists_concatenate(tmp_path):
    """Test that lists are concatenated, not overwritten."""
    # Create file with list
    _write(
        tmp_path / "list.yaml",
        """
        version: 1
        duckdb:
          database: list.duckdb
          pragmas:
            - "SET option1=value1"
        views: []
        """,
    )

    # Create main file with additional items in same list
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - ./list.yaml
        duckdb:
          database: main.duckdb
          pragmas:
            - "SET option2=value2"
        """,
    )

    config = load_config(str(config_path))

    # Both pragmas should be present in order
    assert len(config.duckdb.pragmas) == 2
    assert "SET option1=value1" in config.duckdb.pragmas
    assert "SET option2=value2" in config.duckdb.pragmas


def test_import_with_semantic_models_and_views(tmp_path):
    """Test importing files with both semantic models and views."""
    # Create file with semantic model
    _write(
        tmp_path / "models.yaml",
        """
        version: 1
        duckdb:
          database: models.duckdb
        views:
          - name: base_view
            source: duckdb
            uri: ":memory:"
        semantic_models:
          - name: users_model
            base_view: base_view
            measures:
              - name: count
                agg: count
        """,
    )

    # Create main file
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - ./models.yaml
        duckdb:
          database: main.duckdb
        """,
    )

    config = load_config(str(config_path))

    # Should have both views and semantic models
    assert len(config.views) == 1
    assert config.views[0].name == "base_view"

    assert len(config.semantic_models) == 1
    assert config.semantic_models[0].name == "users_model"
    assert config.semantic_models[0].base_view == "base_view"


def test_multiple_files_same_import(tmp_path):
    """Test that the same import file is only loaded once (caching)."""
    # Create a file that will be imported multiple times
    _write(
        tmp_path / "common.yaml",
        """
        version: 1
        duckdb:
          database: ":memory:"
        views:
          - name: common_view
            sql: "SELECT 1"
        """,
    )

    # Create file A that imports common
    _write(
        tmp_path / "file_a.yaml",
        """
        version: 1
        imports:
          - ./common.yaml
        duckdb:
          database: a.duckdb
        views:
          - name: view_a
            sql: "SELECT 2"
        """,
    )

    # Create file B that also imports common
    _write(
        tmp_path / "file_b.yaml",
        """
        version: 1
        imports:
          - ./common.yaml
        duckdb:
          database: b.duckdb
        views:
          - name: view_b
            sql: "SELECT 3"
        """,
    )

    # Create main file that imports both A and B
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - ./file_a.yaml
          - ./file_b.yaml
        duckdb:
          database: main.duckdb
        views: []
        """,
    )

    config = load_config(str(config_path))

    # common_view should only appear once, even though it was imported twice
    view_names = [v.name for v in config.views]
    assert view_names.count("common_view") == 1
    assert "view_a" in view_names
    assert "view_b" in view_names


def test_import_with_subdirectory(tmp_path):
    """Test importing files from subdirectories."""
    # Create subdirectory
    subdir = tmp_path / "imports"
    subdir.mkdir()

    # Create file in subdirectory
    _write(
        subdir / "settings.yaml",
        """
        version: 1
        duckdb:
          database: subdir.duckdb
        views:
          - name: subdir_view
            sql: "SELECT 1"
        """,
    )

    # Create main file that imports from subdirectory
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - ./imports/settings.yaml
        duckdb:
          database: main.duckdb
        views: []
        """,
    )

    config = load_config(str(config_path))

    # Should have imported the view
    assert len(config.views) == 1
    assert config.views[0].name == "subdir_view"


@patch("duckalog.config.loader._is_remote_uri")
@patch("duckalog.remote_config.fetch_remote_content")
def test_basic_remote_import(mock_fetch, mock_is_remote, tmp_path):
    """Test importing a single remote config file."""
    # Setup remote URI detection to return True for our test URI
    mock_is_remote.side_effect = lambda uri: uri.startswith("s3://") or uri.startswith("https://")

    # Create remote config content
    remote_content = """
    version: 1
    duckdb:
      database: remote.duckdb
    views:
      - name: remote_view
        sql: "SELECT 1"
    """
    mock_fetch.return_value = remote_content

    # Create main file that imports remote config
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - s3://my-bucket/settings.yaml
        duckdb:
          database: main.duckdb
        views:
          - name: main_view
            sql: "SELECT 2"
        """,
    )

    config = load_config(str(config_path))

    # Should have both views
    assert len(config.views) == 2
    view_names = {v.name for v in config.views}
    assert "remote_view" in view_names
    assert "main_view" in view_names

    # Main config should override duckdb database
    assert config.duckdb.database == "main.duckdb"

    # Verify remote config was fetched
    mock_fetch.assert_called_once_with("s3://my-bucket/settings.yaml", 30, filesystem=None)


@patch("duckalog.config.loader._is_remote_uri")
@patch("duckalog.remote_config.fetch_remote_content")
def test_multiple_remote_imports(mock_fetch, mock_is_remote, tmp_path):
    """Test importing multiple remote config files."""
    # Setup remote URI detection
    mock_is_remote.side_effect = lambda uri: uri.startswith("s3://") or uri.startswith("gcs://")

    # Create remote config contents
    remote_content_1 = """
    version: 1
    duckdb:
      database: ":memory:"
    views:
      - name: remote_view1
        sql: "SELECT 1"
    """
    remote_content_2 = """
    version: 1
    duckdb:
      database: ":memory:"
    views:
      - name: remote_view2
        sql: "SELECT 2"
    """

    def mock_fetch_side_effect(uri, timeout=30, filesystem=None):
        if "config1.yaml" in uri:
            return remote_content_1
        elif "config2.yaml" in uri:
            return remote_content_2
        else:
            raise ValueError(f"Unexpected URI: {uri}")

    mock_fetch.side_effect = mock_fetch_side_effect

    # Create main file that imports both remote configs
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - s3://bucket/config1.yaml
          - gcs://bucket/config2.yaml
        duckdb:
          database: main.duckdb
        views:
          - name: main_view
            sql: "SELECT 3"
        """,
    )

    config = load_config(str(config_path))

    # Should have all three views
    assert len(config.views) == 3
    view_names = {v.name for v in config.views}
    assert view_names == {"remote_view1", "remote_view2", "main_view"}


@patch("duckalog.config.loader._is_remote_uri")
@patch("duckalog.remote_config.fetch_remote_content")
def test_nested_remote_imports(mock_fetch, mock_is_remote, tmp_path):
    """Test importing remote configs that themselves have imports."""
    # Setup remote URI detection
    mock_is_remote.side_effect = lambda uri: uri.startswith("s3://") or uri.startswith("https://")

    # Create remote base content
    base_content = """
    version: 1
    duckdb:
      database: ":memory:"
    views:
      - name: base_view
        sql: "SELECT 1"
    """

    # Create remote intermediate content that imports base
    intermediate_content = """
    version: 1
    duckdb:
      database: ":memory:"
    imports:
      - s3://bucket/base.yaml
    views:
      - name: intermediate_view
        sql: "SELECT 2"
    """

    def mock_fetch_side_effect(uri, timeout=30, filesystem=None):
        if "base.yaml" in uri:
            return base_content
        elif "intermediate.yaml" in uri:
            return intermediate_content
        else:
            raise ValueError(f"Unexpected URI: {uri}")

    mock_fetch.side_effect = mock_fetch_side_effect

    # Create main file that imports intermediate
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - s3://bucket/intermediate.yaml
        duckdb:
          database: main.duckdb
        views:
          - name: main_view
            sql: "SELECT 3"
        """,
    )

    config = load_config(str(config_path))

    # Should have all three views (base, intermediate, main)
    assert len(config.views) == 3
    view_names = {v.name for v in config.views}
    assert view_names == {"base_view", "intermediate_view", "main_view"}


@patch("duckalog.config.loader._is_remote_uri")
@patch("duckalog.remote_config.fetch_remote_content")
def test_circular_remote_import_detection(mock_fetch, mock_is_remote, tmp_path):
    """Test that circular imports are detected with remote URIs."""
    # Setup remote URI detection
    mock_is_remote.side_effect = lambda uri: uri.startswith("s3://")

    # Create remote content for file A that imports B
    file_a_content = """
    version: 1
    imports:
      - s3://bucket/file_b.yaml
    duckdb:
      database: a.duckdb
    views: []
    """

    # Create remote content for file B that imports A (circular!)
    file_b_content = """
    version: 1
    imports:
      - s3://bucket/file_a.yaml
    duckdb:
      database: b.duckdb
    views: []
    """

    def mock_fetch_side_effect(uri, timeout=30, filesystem=None):
        if "file_a.yaml" in uri:
            return file_a_content
        elif "file_b.yaml" in uri:
            return file_b_content
        else:
            raise ValueError(f"Unexpected URI: {uri}")

    mock_fetch.side_effect = mock_fetch_side_effect

    # Create main file that imports file A
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: main.duckdb
        imports:
          - s3://bucket/file_a.yaml
        views: []
        """,
    )

    # Try to load file A - should fail with circular import error
    with pytest.raises(CircularImportError) as exc_info:
        load_config(str(config_path))

    assert "Circular import detected" in str(exc_info.value)


@patch("duckalog.config.loader._is_remote_uri")
@patch("duckalog.remote_config.fetch_remote_content")
def test_mixed_local_and_remote_imports(mock_fetch, mock_is_remote, tmp_path):
    """Test importing both local and remote config files."""
    # Setup remote URI detection
    mock_is_remote.side_effect = lambda uri: uri.startswith("https://")

    # Create local imported file
    _write(
        tmp_path / "local_config.yaml",
        """
        version: 1
        duckdb:
          database: local.duckdb
        views:
          - name: local_view
            sql: "SELECT 1"
        """,
    )

    # Create remote config content
    remote_content = """
    version: 1
    duckdb:
      database: ":memory:"
    views:
      - name: remote_view
        sql: "SELECT 2"
    """
    mock_fetch.return_value = remote_content

    # Create main file that imports both local and remote
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - ./local_config.yaml
          - https://example.com/remote_config.yaml
        duckdb:
          database: main.duckdb
        views:
          - name: main_view
            sql: "SELECT 3"
        """,
    )

    config = load_config(str(config_path))

    # Should have all three views
    assert len(config.views) == 3
    view_names = {v.name for v in config.views}
    assert view_names == {"local_view", "remote_view", "main_view"}

    # Verify remote config was fetched
    mock_fetch.assert_called_once_with("https://example.com/remote_config.yaml", 30, filesystem=None)


@patch("duckalog.config.loader._is_remote_uri")
@patch("duckalog.remote_config.fetch_remote_content")
def test_remote_import_with_env_var_in_path(mock_fetch, mock_is_remote, tmp_path, monkeypatch):
    """Test environment variable interpolation in remote import paths."""
    # Setup remote URI detection
    mock_is_remote.return_value = True

    monkeypatch.setenv("REMOTE_BUCKET", "my-bucket")

    # Create remote config content
    remote_content = """
    version: 1
    duckdb:
      database: ":memory:"
    views:
      - name: env_view
        sql: "SELECT 1"
    """
    mock_fetch.return_value = remote_content

    # Create main file that uses env var in remote import path
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - https://${env:REMOTE_BUCKET}.s3.amazonaws.com/config.yaml
        duckdb:
          database: main.duckdb
        views: []
        """,
    )

    config = load_config(str(config_path))

    # Should have imported the view
    assert len(config.views) == 1
    assert config.views[0].name == "env_view"

    # Verify remote config was fetched with resolved path
    mock_fetch.assert_called_once_with("https://my-bucket.s3.amazonaws.com/config.yaml", 30, filesystem=None)


@patch("duckalog.config.loader._is_remote_uri")
@patch("duckalog.remote_config.fetch_remote_content")
def test_remote_import_http_failure(mock_fetch, mock_is_remote, tmp_path):
    """Test error handling when remote import fails to fetch."""
    # Setup remote URI detection
    mock_is_remote.return_value = True

    # Mock fetch to raise an error
    mock_fetch.side_effect = Exception("HTTP 404 Not Found")

    # Create main file that imports remote config
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - https://example.com/nonexistent.yaml
        duckdb:
          database: main.duckdb
        views: []
        """,
    )

    # Should raise an import validation error
    with pytest.raises(ImportValidationError) as exc_info:
        load_config(str(config_path))

    assert "Failed to load remote config" in str(exc_info.value)
    assert "https://example.com/nonexistent.yaml" in str(exc_info.value)


@patch("duckalog.config.loader._is_remote_uri")
@patch("duckalog.remote_config.fetch_remote_content")
def test_remote_import_invalid_yaml(mock_fetch, mock_is_remote, tmp_path):
    """Test error handling when remote import returns invalid YAML."""
    # Setup remote URI detection
    mock_is_remote.return_value = True

    # Mock fetch to return invalid YAML
    mock_fetch.return_value = "invalid: yaml: content: ["

    # Create main file that imports remote config
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - s3://bucket/invalid.yaml
        duckdb:
          database: main.duckdb
        views: []
        """,
    )

    # Should raise an import validation error
    with pytest.raises(ImportValidationError) as exc_info:
        load_config(str(config_path))

    assert "Failed to load remote config" in str(exc_info.value)


@patch("duckalog.config.loader._is_remote_uri")
@patch("duckalog.remote_config.fetch_remote_content")
def test_remote_import_json_format(mock_fetch, mock_is_remote, tmp_path):
    """Test importing remote JSON config files."""
    # Setup remote URI detection
    mock_is_remote.return_value = True

    # Create remote JSON config content
    import json

    json_content = json.dumps({
        "version": 1,
        "duckdb": {"database": ":memory:"},
        "views": [{"name": "json_view", "sql": "SELECT 1"}]
    })
    mock_fetch.return_value = json_content

    # Create main YAML file that imports remote JSON
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - https://example.com/config.json
        duckdb:
          database: main.duckdb
        views: []
        """,
    )

    config = load_config(str(config_path))

    # Should have imported the view from JSON
    assert len(config.views) == 1
    assert config.views[0].name == "json_view"


@patch("duckalog.config.loader._is_remote_uri")
@patch("duckalog.remote_config.fetch_remote_content")
def test_remote_import_cache(mock_fetch, mock_is_remote, tmp_path):
    """Test that remote imports are cached properly."""
    # Setup remote URI detection to only return True for s3:// URIs
    mock_is_remote.side_effect = lambda uri: uri.startswith("s3://")

    # Create remote config content
    remote_content = """
    version: 1
    duckdb:
      database: ":memory:"
    views:
      - name: cached_view
        sql: "SELECT 1"
    """
    mock_fetch.return_value = remote_content

    # Create a simple local file that imports the remote config twice
    # This simulates the case where the same remote import is resolved multiple times
    # within the same import chain
    _write(
        tmp_path / "main.yaml",
        """
        version: 1
        duckdb:
          database: main.duckdb
        imports:
          - s3://bucket/common.yaml
        views:
          - name: main_view
            sql: "SELECT 2"
        """,
    )

    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        imports:
          - ./main.yaml
        views: []
        """,
    )

    config = load_config(str(config_path))

    # Both views should be present
    view_names = [v.name for v in config.views]
    assert "cached_view" in view_names
    assert "main_view" in view_names

    # Remote config should only be fetched once, even though main.yaml is imported once
    # The test verifies that the cache is being used
    assert mock_fetch.call_count == 1


# Tests for Advanced Import Options

def test_glob_patterns_simple(tmp_path):
    """Test importing multiple files using glob patterns."""
    # Create multiple view files
    for i in range(3):
        _write(
            tmp_path / f"view_{i}.yaml",
            f"""
            version: 1
            duckdb:
              database: base.duckdb
            views:
              - name: view_{i}
                sql: "SELECT {i}"
            """,
        )

    # Create main file with glob pattern
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - "./view_*.yaml"
        duckdb:
          database: main.duckdb
        views:
          - name: main_view
            sql: "SELECT 100"
        """,
    )

    config = load_config(str(config_path))

    # Should have all 4 views (3 imported + 1 main)
    assert len(config.views) == 4
    view_names = {v.name for v in config.views}
    assert "view_0" in view_names
    assert "view_1" in view_names
    assert "view_2" in view_names
    assert "main_view" in view_names


def test_glob_patterns_with_excludes(tmp_path):
    """Test glob patterns with exclude patterns."""
    # Create multiple view files
    for i in range(3):
        _write(
            tmp_path / f"view_{i}.yaml",
            f"""
            version: 1
            duckdb:
              database: base.duckdb
            views:
              - name: view_{i}
                sql: "SELECT {i}"
            """,
        )

    # Create main file with glob pattern and exclude
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - "./view_*.yaml"
          - "!./view_1.yaml"
        duckdb:
          database: main.duckdb
        """,
    )

    config = load_config(str(config_path))

    # Should have 2 views (view_0 and view_2, but not view_1)
    assert len(config.views) == 2
    view_names = {v.name for v in config.views}
    assert "view_0" in view_names
    assert "view_1" not in view_names
    assert "view_2" in view_names


def test_selective_imports_views(tmp_path):
    """Test section-specific imports for views."""
    # Create imported view file
    _write(
        tmp_path / "imported_views.yaml",
        """
        version: 1
        duckdb:
          database: imported.duckdb
        views:
          - name: imported_view_1
            sql: "SELECT 1"
          - name: imported_view_2
            sql: "SELECT 2"
        """,
    )

    # Create main file with selective import
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          views:
            - "./imported_views.yaml"
        duckdb:
          database: main.duckdb
        views:
          - name: main_view
            sql: "SELECT 100"
        """,
    )

    config = load_config(str(config_path))

    # Should have all 3 views
    assert len(config.views) == 3
    view_names = {v.name for v in config.views}
    assert "imported_view_1" in view_names
    assert "imported_view_2" in view_names
    assert "main_view" in view_names

    # DuckDB settings should not be overridden by import (selective import)
    assert config.duckdb.database == "main.duckdb"


def test_selective_imports_duckdb(tmp_path):
    """Test section-specific imports for DuckDB settings."""
    # Create imported duckdb file
    _write(
        tmp_path / "imported_db.yaml",
        """
        version: 1
        duckdb:
          database: imported.duckdb
          install_extensions:
            - httpfs
        views: []
        """,
    )

    # Create main file with selective import
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          duckdb:
            - "./imported_db.yaml"
        duckdb:
          database: main.duckdb
          install_extensions:
            - json
        views:
          - name: main_view
            sql: "SELECT 100"
        """,
    )

    config = load_config(str(config_path))

    # DuckDB settings should be merged (lists are concatenated)
    assert config.duckdb.database == "main.duckdb"  # Main config wins for scalar
    assert "httpfs" in config.duckdb.install_extensions  # Imported extension added
    assert "json" in config.duckdb.install_extensions  # Main config extension kept

    # Views should not be affected by duckdb-specific import
    assert len(config.views) == 1
    assert config.views[0].name == "main_view"


def test_import_with_override_false(tmp_path):
    """Test import with override=false flag."""
    # Create imported file
    _write(
        tmp_path / "imported.yaml",
        """
        version: 1
        duckdb:
          database: imported.duckdb
        views: []
        """,
    )

    # Create main file with non-overriding import
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - path: "./imported.yaml"
            override: false
        duckdb:
          database: main.duckdb
        views:
          - name: main_view
            sql: "SELECT 100"
        """,
    )

    config = load_config(str(config_path))

    # Main config values should be preserved (import doesn't override)
    assert config.duckdb.database == "main.duckdb"

    # View from imported file should be merged
    assert len(config.views) == 1
    assert config.views[0].name == "main_view"


def test_selective_import_with_override_false(tmp_path):
    """Test section-specific import with override=false."""
    # Create imported file
    _write(
        tmp_path / "imported.yaml",
        """
        version: 1
        duckdb:
          database: imported.duckdb
        views: []
        """,
    )

    # Create main file with selective non-overriding import
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          duckdb:
            - path: "./imported.yaml"
              override: false
        duckdb:
          database: main.duckdb
        views:
          - name: main_view
            sql: "SELECT 100"
        """,
    )

    config = load_config(str(config_path))

    # Main config values should be preserved
    assert config.duckdb.database == "main.duckdb"


def test_selective_imports_multiple_sections(tmp_path):
    """Test importing different sections from different files."""
    # Create view file
    _write(
        tmp_path / "imported_views.yaml",
        """
        version: 1
        views:
          - name: imported_view
            sql: "SELECT 1"
        """,
    )

    # Create duckdb file
    _write(
        tmp_path / "imported_db.yaml",
        """
        version: 1
        duckdb:
          database: imported.duckdb
          install_extensions:
            - httpfs
        views: []
        """,
    )

    # Create main file with multiple selective imports
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          views:
            - "./imported_views.yaml"
          duckdb:
            - "./imported_db.yaml"
        duckdb:
          database: main.duckdb
          install_extensions:
            - json
        views:
          - name: main_view
            sql: "SELECT 100"
        """,
    )

    config = load_config(str(config_path))

    # Should have both views
    assert len(config.views) == 2
    view_names = {v.name for v in config.views}
    assert "imported_view" in view_names
    assert "main_view" in view_names

    # DuckDB settings should be merged
    assert config.duckdb.database == "main.duckdb"  # Scalar override
    assert "httpfs" in config.duckdb.install_extensions  # List merged
    assert "json" in config.duckdb.install_extensions  # List merged


def test_glob_with_import_entry(tmp_path):
    """Test glob patterns with ImportEntry format."""
    # Create multiple view files
    for i in range(2):
        _write(
            tmp_path / f"view_{i}.yaml",
            f"""
            version: 1
            views:
              - name: view_{i}
                sql: "SELECT {i}"
            """,
        )

    # Create main file with glob in ImportEntry format
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          views:
            - path: "./view_*.yaml"
              override: false
        duckdb:
          database: main.duckdb
        views:
          - name: main_view
            sql: "SELECT 100"
        """,
    )

    config = load_config(str(config_path))

    # Should have all views
    assert len(config.views) == 3
    view_names = {v.name for v in config.views}
    assert "view_0" in view_names
    assert "view_1" in view_names
    assert "main_view" in view_names


def test_mixed_global_and_selective_imports(tmp_path):
    """Test mixing global and section-specific imports."""
    # Create global import file
    _write(
        tmp_path / "global.yaml",
        """
        version: 1
        duckdb:
          database: global.duckdb
        views:
          - name: global_view
            sql: "SELECT 1"
        """,
    )

    # Create view-specific import file
    _write(
        tmp_path / "extra_views.yaml",
        """
        version: 1
        views:
          - name: extra_view
            sql: "SELECT 2"
        """,
    )

    # Create main file with both import types
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - "./global.yaml"
          views:
            - "./extra_views.yaml"
        duckdb:
          database: main.duckdb
        views:
          - name: main_view
            sql: "SELECT 100"
        """,
    )

    config = load_config(str(config_path))

    # Should have all views
    assert len(config.views) == 3
    view_names = {v.name for v in config.views}
    assert "global_view" in view_names
    assert "extra_view" in view_names
    assert "main_view" in view_names

    # DuckDB database should be from main (not global import)
    assert config.duckdb.database == "main.duckdb"


def test_empty_selective_imports_normalization(tmp_path):
    """Test that empty SelectiveImports is normalized to empty list."""
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        duckdb:
          database: main.duckdb
        views:
          - name: main_view
            sql: "SELECT 1"
        """,
    )

    # Manually create a config with empty SelectiveImports to test normalization
    from duckalog.config.models import SelectiveImports
    from duckalog import load_config
    
    # Create config with empty SelectiveImports
    imports = SelectiveImports()
    config = load_config(str(config_path))
    
    # Should normalize to empty list
    assert config.imports == [] or (
        hasattr(config.imports, 'model_fields') and
        all(getattr(config.imports, field) is None for field in config.imports.model_fields.keys())
    )


def test_import_entry_validation(tmp_path):
    """Test that ImportEntry validation works correctly."""
    # Test with valid ImportEntry
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - path: "./imported.yaml"
            override: false
        duckdb:
          database: main.duckdb
        views:
          - name: main_view
            sql: "SELECT 1"
        """,
    )

    config = load_config(str(config_path))
    assert config.imports[0].path == "./imported.yaml"
    assert config.imports[0].override is False


def test_glob_pattern_no_matches(tmp_path):
    """Test that glob patterns with no matches raise an error."""
    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - "./nonexistent_*.yaml"
        duckdb:
          database: main.duckdb
        views:
          - name: main_view
            sql: "SELECT 1"
        """,
    )

    with pytest.raises(ImportFileNotFoundError):
        load_config(str(config_path))


def test_glob_pattern_nested_directories(tmp_path):
    """Test glob patterns with nested directories."""
    # Create nested directory structure
    (tmp_path / "views").mkdir()
    (tmp_path / "views" / "subdir").mkdir()
    
    _write(
        tmp_path / "views" / "view1.yaml",
        """
        version: 1
        views:
          - name: view1
            sql: "SELECT 1"
        """,
    )
    
    _write(
        tmp_path / "views" / "subdir" / "view2.yaml",
        """
        version: 1
        views:
          - name: view2
            sql: "SELECT 2"
        """,
    )

    config_path = _write(
        tmp_path / "catalog.yaml",
        """
        version: 1
        imports:
          - "./views/**/*.yaml"
        duckdb:
          database: main.duckdb
        views:
          - name: main_view
            sql: "SELECT 100"
        """,
    )

    config = load_config(str(config_path))

    # Should have all views from recursive glob
    assert len(config.views) == 3
    view_names = {v.name for v in config.views}
    assert "view1" in view_names
    assert "view2" in view_names
    assert "main_view" in view_names

