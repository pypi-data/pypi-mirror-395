import json
from pathlib import Path

from starlette.testclient import TestClient

from duckalog.dashboard.app import create_app
from duckalog.dashboard.state import DashboardContext


def _write_config(tmp_path: Path) -> Path:
    db_path = tmp_path / "catalog.duckdb"
    config_path = tmp_path / "catalog.yaml"
    config_path.write_text(
        """
version: 1
duckdb:
  database: "{db}"
views:
  - name: foo
    sql: "select 1 as x"
""".format(
            db=db_path
        )
    )
    return config_path


def test_dashboard_routes_work(tmp_path: Path):
    config_path = _write_config(tmp_path)
    ctx = DashboardContext.from_path(str(config_path))
    app = create_app(ctx)
    client = TestClient(app)

    resp = client.get("/")
    assert resp.status_code == 200
    assert "Duckalog Dashboard" in resp.text

    resp = client.get("/views")
    assert resp.status_code == 200
    assert "foo" in resp.text

    resp = client.get("/views/foo")
    assert resp.status_code == 200
    assert "foo" in resp.text

    resp = client.post("/query", data={"sql": "select 1 as x"})
    assert resp.status_code == 200
    assert "1" in resp.text

    resp = client.post("/build", follow_redirects=False)
    assert resp.status_code == 303
    # After build, home should still respond
    resp = client.get("/")
    assert resp.status_code == 200
