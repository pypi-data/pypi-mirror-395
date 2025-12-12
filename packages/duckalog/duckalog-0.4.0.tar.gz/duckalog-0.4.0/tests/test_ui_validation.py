import sys
import time
import types

import pytest

if "datastar_py" not in sys.modules:
    sys.modules["datastar_py"] = types.SimpleNamespace(
        ServerSentEventGenerator=type("DummySSE", (), {})
    )

from duckalog.ui import _validate_read_only_query, UIServer


def test_validate_allows_simple_select():
    assert _validate_read_only_query("SELECT 1;") == "SELECT 1;"


def test_validate_allows_semicolons_in_strings_and_comments():
    query = """
    -- this is a comment ; drop table foo
    SELECT 'value;still select' as c
    /* block comment ; delete */
    """
    assert _validate_read_only_query(query) == query


def test_validate_rejects_multiple_statements():
    with pytest.raises(ValueError):
        _validate_read_only_query("SELECT 1; SELECT 2;")


def test_validate_rejects_ddl_and_dml():
    with pytest.raises(ValueError):
        _validate_read_only_query("DROP TABLE x")
    with pytest.raises(ValueError):
        _validate_read_only_query("UPDATE t SET a=1")


def test_task_pruning_size_and_ttl(monkeypatch, tmp_path):
    # Bypass config loading
    monkeypatch.setattr(UIServer, "_load_config", lambda self: None)
    server = UIServer(str(tmp_path / "dummy.yaml"))
    server._task_results.clear()
    server._task_max_items = 2
    server._task_ttl_seconds = 0

    # Add three tasks; ensure prune keeps max items
    for i in range(3):
        server._task_results[f"t{i}"] = {"created_at": time.time()}
        server._prune_task_results()

    assert len(server._task_results) <= 2

    # TTL prune
    server._task_ttl_seconds = 0
    server._task_results["old"] = {"created_at": time.time() - 10}
    server._prune_task_results()
    assert "old" not in server._task_results
