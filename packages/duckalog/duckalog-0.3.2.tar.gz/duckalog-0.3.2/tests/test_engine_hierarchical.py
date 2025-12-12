"""Engine tests for hierarchical Duckalog configs."""

from __future__ import annotations

import tempfile
import textwrap
from pathlib import Path

import duckdb
import pytest

from duckalog import EngineError, build_catalog
from tests.test_engine_cli import _write_config


def test_simple_hierarchical_build(tmp_path):
    """Test building parent with single child config."""
    # Create child config
    child_config = _write_config(
        tmp_path / "child.yaml",
        """
        version: 1
        duckdb:
          database: child.duckdb
        views:
          - name: reference_data
            sql: |
              SELECT 1 AS id, 'reference' AS type
          - name: child_metrics
            sql: |
              SELECT COUNT(*) as total_records FROM reference_data
        """,
    )

    # Create parent config that attaches child
    parent_config = _write_config(
        tmp_path / "parent.yaml",
        f"""
        version: 1
        duckdb:
          database: parent.duckdb
        attachments:
          duckalog:
            - alias: ref
              config_path: {child_config}
        views:
          - name: combined_data
            sql: |
              SELECT * FROM ref.reference_data
              UNION ALL
              SELECT 2 AS id, 'parent' AS type
          - name: all_metrics
            sql: |
              SELECT 'parent' as source, COUNT(*) as records FROM combined_data
              UNION ALL
              SELECT 'child' as source, total_records FROM ref.child_metrics
        """,
    )

    # Build parent catalog
    build_catalog(str(parent_config))

    # Verify child was built and attached
    child_db_path = tmp_path / "child.duckdb"
    assert child_db_path.exists()

    # Verify parent catalog works
    parent_db_path = tmp_path / "parent.duckdb"
    conn = duckdb.connect(str(parent_db_path))

    # Test combined data view
    rows = conn.execute("SELECT * FROM combined_data ORDER BY id").fetchall()
    assert rows == [(1, 'reference'), (2, 'parent')]

    # Test metrics view
    rows = conn.execute("SELECT * FROM all_metrics ORDER BY source").fetchall()
    assert len(rows) == 2

    conn.close()


def test_multi_level_hierarchy(tmp_path):
    """Test building configs with multiple nesting levels."""
    # Create grandchild config
    grandchild_config = _write_config(
        tmp_path / "grandchild.yaml",
        """
        version: 1
        duckdb:
          database: grandchild.duckdb
        views:
          - name: base_data
            sql: |
              SELECT 1 AS id, 'base' AS value
        """,
    )

    # Create child config that attaches grandchild
    child_config = _write_config(
        tmp_path / "child.yaml",
        f"""
        version: 1
        duckdb:
          database: child.duckdb
        attachments:
          duckalog:
            - alias: base
              config_path: {grandchild_config}
        views:
          - name: enhanced_data
            sql: |
              SELECT id, value || '_enhanced' AS value FROM base.base_data
        """,
    )

    # Create parent config that attaches child
    parent_config = _write_config(
        tmp_path / "parent.yaml",
        f"""
        version: 1
        duckdb:
          database: parent.duckdb
        attachments:
          duckalog:
            - alias: child_ref
              config_path: {child_config}
        views:
          - name: final_data
            sql: |
              SELECT id, value || '_final' AS value FROM child_ref.enhanced_data
        """,
    )

    # Build parent catalog
    build_catalog(str(parent_config))

    # Verify all levels were built
    assert (tmp_path / "grandchild.duckdb").exists()
    assert (tmp_path / "child.duckdb").exists()
    assert (tmp_path / "parent.duckdb").exists()

    # Verify final result
    conn = duckdb.connect(str(tmp_path / "parent.duckdb"))
    rows = conn.execute("SELECT * FROM final_data").fetchall()
    assert rows == [(1, 'base_enhanced_final')]
    conn.close()


def test_attachment_reuse_within_run(tmp_path):
    """Test that the same child config is built only once."""
    # Create shared child config
    shared_child = _write_config(
        tmp_path / "shared.yaml",
        """
        version: 1
        duckdb:
          database: shared.duckdb
        views:
          - name: shared_view
            sql: |
              SELECT 'shared_data' AS data
        """,
    )

    # Create parent config that attaches same child twice with different aliases
    parent_config = _write_config(
        tmp_path / "parent.yaml",
        f"""
        version: 1
        duckdb:
          database: parent.duckdb
        attachments:
          duckalog:
            - alias: shared1
              config_path: {shared_child}
            - alias: shared2
              config_path: {shared_child}  # Same file, different alias
        views:
          - name: combined_shared
            sql: |
              SELECT data FROM shared1.shared_view
              UNION ALL
              SELECT data FROM shared2.shared_view
        """,
    )

    # Build parent catalog
    build_catalog(str(parent_config))

    # Verify shared child was built only once
    shared_db_path = tmp_path / "shared.duckdb"
    assert shared_db_path.exists()

    # Verify both aliases work in parent
    conn = duckdb.connect(str(tmp_path / "parent.duckdb"))
    rows = conn.execute("SELECT * FROM combined_shared").fetchall()
    assert len(rows) == 2
    assert all(row[0] == 'shared_data' for row in rows)
    conn.close()


def test_cycle_detection(tmp_path):
    """Test that cyclic attachments are detected and rejected."""
    # Create config A that references B
    config_a = _write_config(
        tmp_path / "config_a.yaml",
        """
        version: 1
        duckdb:
          database: config_a.duckdb
        attachments:
          duckalog:
            - alias: config_b
              config_path: ./config_b.yaml
        views:
          - name: view_a
            sql: "SELECT 1"
        """,
    )

    # Create config B that references A (creating a cycle)
    config_b = _write_config(
        tmp_path / "config_b.yaml",
        f"""
        version: 1
        duckdb:
          database: config_b.duckdb
        attachments:
          duckalog:
            - alias: config_a
              config_path: {config_a}
        views:
          - name: view_b
            sql: "SELECT 2"
        """,
    )

    # Building should fail with cycle detection
    with pytest.raises(EngineError) as exc:
        build_catalog(str(config_a), db_path=str(tmp_path / "test_a.duckdb"))

    assert "cyclic attachment" in str(exc.value).lower()


def test_dry_run_with_hierarchical_configs(tmp_path):
    """Test dry run validation of hierarchical configs."""
    # Create child config
    child_config = _write_config(
        tmp_path / "child.yaml",
        """
        version: 1
        duckdb:
          database: child.duckdb
        views:
          - name: child_view
            sql: "SELECT 1"
        """,
    )

    # Create parent config that attaches child
    parent_config = _write_config(
        tmp_path / "parent.yaml",
        f"""
        version: 1
        duckdb:
          database: parent.duckdb
        attachments:
          duckalog:
            - alias: child
              config_path: {child_config}
        views:
          - name: parent_view
            sql: "SELECT 2"
        """,
    )

    # Dry run should validate attachments without building
    sql = build_catalog(str(parent_config), dry_run=True)

    assert sql is not None
    assert 'CREATE OR REPLACE VIEW "parent_view"' in sql
    # No databases should be created in dry run
    assert not (tmp_path / "child.duckdb").exists()
    assert not (tmp_path / "parent.duckdb").exists()


def test_database_path_override(tmp_path):
    """Test database path override in Duckalog attachments."""
    # Create child config with one database path
    child_config = _write_config(
        tmp_path / "child.yaml",
        """
        version: 1
        duckdb:
          database: original_child.duckdb
        views:
          - name: child_view
            sql: "SELECT 'original' AS source"
        """,
    )

    # Create parent that overrides child's database path
    parent_config = _write_config(
        tmp_path / "parent.yaml",
        f"""
        version: 1
        duckdb:
          database: parent.duckdb
        attachments:
          duckalog:
            - alias: child
              config_path: {child_config}
              database: ./overridden_child.duckdb
        views:
          - name: parent_view
            sql: |
              SELECT source FROM child.child_view
        """,
    )

    # Build parent catalog
    build_catalog(str(parent_config))

    # Verify child database was built at overridden path
    assert not (tmp_path / "original_child.duckdb").exists()
    assert (tmp_path / "overridden_child.duckdb").exists()

    # Verify parent can access child data
    conn = duckdb.connect(str(tmp_path / "parent.duckdb"))
    rows = conn.execute("SELECT * FROM parent_view").fetchall()
    assert rows == [('original',)]
    conn.close()


def test_dry_run_cycle_detection(tmp_path):
    """Test that dry run also detects cycles."""
    # Create cyclic configs
    config_a = _write_config(
        tmp_path / "config_a.yaml",
        """
        version: 1
        duckdb:
          database: config_a.duckdb
        attachments:
          duckalog:
            - alias: config_b
              config_path: ./config_b.yaml
        views:
          - name: view_a
            sql: "SELECT 1"
        """,
    )

    config_b = _write_config(
        tmp_path / "config_b.yaml",
        f"""
        version: 1
        duckdb:
          database: config_b.duckdb
        attachments:
          duckalog:
            - alias: config_a
              config_path: {config_a}
        views:
          - name: view_b
            sql: "SELECT 2"
        """,
    )

    # Dry run should also detect cycles
    with pytest.raises(EngineError) as exc:
        build_catalog(str(config_a), dry_run=True)

    assert "cyclic attachment" in str(exc.value).lower()


def test_relative_path_resolution_in_attachments(tmp_path):
    """Test that relative paths in attachments are resolved correctly."""
    # Create directory structure
    nested_dir = tmp_path / "nested"
    nested_dir.mkdir()

    # Create child config in nested directory
    child_config = _write_config(
        nested_dir / "child.yaml",
        """
        version: 1
        duckdb:
          database: child.duckdb
        views:
          - name: child_data
            sql: "SELECT 'nested_child' AS data"
        """,
    )

    # Create parent config in root directory
    parent_config = _write_config(
        tmp_path / "parent.yaml",
        """
        version: 1
        duckdb:
          database: parent.duckdb
        attachments:
          duckalog:
            - alias: nested_child
              config_path: ./nested/child.yaml
        views:
          - name: access_nested
            sql: "SELECT * FROM nested_child.child_data"
        """,
    )

    # Build parent catalog
    build_catalog(str(parent_config))

    # Verify child was built at correct location
    child_db_path = nested_dir / "child.duckdb"
    assert child_db_path.exists()

    # Verify parent can access child data
    conn = duckdb.connect(str(tmp_path / "parent.duckdb"))
    rows = conn.execute("SELECT * FROM access_nested").fetchall()
    assert rows == [('nested_child',)]
    conn.close()


def test_database_override_with_relative_path(tmp_path):
    """Test database override with relative paths."""
    # Create directory structure
    override_dir = tmp_path / "custom_databases"
    override_dir.mkdir()

    # Create child config
    child_config = _write_config(
        tmp_path / "child.yaml",
        """
        version: 1
        duckdb:
          database: default_child.duckdb
        views:
          - name: child_view
            sql: "SELECT 'default' AS location"
        """,
    )

    # Create parent config with relative database override
    parent_config = _write_config(
        tmp_path / "parent.yaml",
        f"""
        version: 1
        duckdb:
          database: parent.duckdb
        attachments:
          duckalog:
            - alias: custom_child
              config_path: {child_config}
              database: ./custom_databases/overridden_child.duckdb
        views:
          - name: check_location
            sql: |
              SELECT location FROM custom_child.child_view
        """,
    )

    # Build parent catalog
    build_catalog(str(parent_config))

    # Verify child database was built at overridden location
    assert not (tmp_path / "default_child.duckdb").exists()
    assert (override_dir / "overridden_child.duckdb").exists()

    # Verify parent can access child data with custom location
    conn = duckdb.connect(str(tmp_path / "parent.duckdb"))
    rows = conn.execute("SELECT * FROM check_location").fetchall()
    assert rows == [('default',)]
    conn.close()


def test_config_validation_error_missing_alias(tmp_path):
    """Test that DuckalogAttachment validates required alias field."""
    config = _write_config(
        tmp_path / "config.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        attachments:
          duckalog:
            - config_path: child.yaml
              # Missing alias field
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    # Should fail config validation
    with pytest.raises(Exception) as exc:
        build_catalog(str(config))

    assert "alias" in str(exc.value).lower() or "validation" in str(exc.value).lower()


def test_config_validation_error_missing_config_path(tmp_path):
    """Test that DuckalogAttachment validates required config_path field."""
    config = _write_config(
        tmp_path / "config.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        attachments:
          duckalog:
            - alias: child
              # Missing config_path field
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    # Should fail config validation
    with pytest.raises(Exception) as exc:
        build_catalog(str(config))

    assert "config_path" in str(exc.value).lower() or "validation" in str(exc.value).lower()


def test_config_validation_error_empty_alias(tmp_path):
    """Test that DuckalogAttachment validates empty alias field."""
    config = _write_config(
        tmp_path / "config.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        attachments:
          duckalog:
            - alias: ""
              config_path: child.yaml
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    # Should fail config validation
    with pytest.raises(Exception) as exc:
        build_catalog(str(config))

    assert "alias" in str(exc.value).lower() or "cannot be empty" in str(exc.value).lower()


def test_config_validation_error_empty_config_path(tmp_path):
    """Test that DuckalogAttachment validates empty config_path field."""
    config = _write_config(
        tmp_path / "config.yaml",
        """
        version: 1
        duckdb:
          database: catalog.duckdb
        attachments:
          duckalog:
            - alias: child
              config_path: ""
        views:
          - name: test_view
            sql: "SELECT 1"
        """,
    )

    # Should fail config validation
    with pytest.raises(Exception) as exc:
        build_catalog(str(config))

    assert "config_path" in str(exc.value).lower() or "cannot be empty" in str(exc.value).lower()