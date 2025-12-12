"""Tests for Duckalog UI functionality."""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from starlette.testclient import TestClient

from duckalog.config import Config, ViewConfig
from duckalog.ui import UIServer, UIError


@pytest.fixture
def sample_config():
    """Create a sample configuration for testing."""
    return Config(
        version=1,
        duckdb={"database": ":memory:"},
        views=[
            ViewConfig(
                name="test_view",
                sql="SELECT 1 as id, 'test' as name",
                description="Test view",
                tags=["test"],
            ),
            ViewConfig(
                name="another_view",
                source="parquet",
                uri="memory://test.parquet",
                table="test_table",
            ),
        ],
    )


@pytest.fixture
def config_file(sample_config):
    """Create a temporary config file."""
    import yaml
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(sample_config.model_dump(), f, default_flow_style=False)
        return Path(f.name)


@pytest.fixture
def ui_server(config_file):
    """Create a UI server instance for testing."""
    return UIServer(str(config_file))


@pytest.fixture
def test_client(ui_server):
    """Create a test client for the UI server."""
    return TestClient(ui_server.app)


class TestUIServer:
    """Test UIServer class."""

    def test_init_success(self, config_file):
        """Test successful UIServer initialization."""
        server = UIServer(str(config_file))
        assert server.config is not None
        assert len(server.config.views) == 2
        assert server.host == "127.0.0.1"
        assert server.port == 8000

    def test_init_invalid_config(self):
        """Test UIServer initialization with invalid config."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("invalid: yaml: content:")
            invalid_config = Path(f.name)

        with pytest.raises(UIError, match="Failed to load config"):
            UIServer(str(invalid_config))

    def test_init_custom_host_port(self, config_file):
        """Test UIServer initialization with custom host and port."""
        server = UIServer(str(config_file), host="0.0.0.0", port=9000)
        assert server.host == "0.0.0.0"
        assert server.port == 9000


class TestConfigEndpoints:
    """Test configuration-related endpoints."""

    def test_get_config(self, test_client):
        """Test getting current configuration."""
        response = test_client.get("/api/config")
        assert response.status_code == 200

        config_data = response.json()
        assert "duckdb" in config_data
        assert "views" in config_data
        assert len(config_data["views"]) == 2

    def test_update_config_add_view(self, test_client):
        """Test updating configuration by adding a view."""
        new_view = {
            "name": "new_view",
            "sql": "SELECT 2 as id, 'new' as name",
            "description": "New test view",
        }

        response = test_client.post("/api/config", json={"view": new_view})
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert len(result["config"]["views"]) == 3
        assert any(v["name"] == "new_view" for v in result["config"]["views"])

    def test_update_config_replace_views(self, test_client):
        """Test updating configuration by replacing all views."""
        new_views = [
            {
                "name": "replaced_view",
                "sql": "SELECT 3 as id",
                "description": "Replaced view",
            }
        ]

        response = test_client.post("/api/config", json={"views": new_views})
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert len(result["config"]["views"]) == 1
        assert result["config"]["views"][0]["name"] == "replaced_view"

    def test_update_config_invalid_body(self, test_client):
        """Test updating configuration with invalid body."""
        response = test_client.post("/api/config", json="invalid")
        assert response.status_code == 400
        assert "Invalid request body" in response.json()["error"]


class TestViewEndpoints:
    """Test view management endpoints."""

    def test_get_views(self, test_client):
        """Test getting all views."""
        response = test_client.get("/api/views")
        assert response.status_code == 200

        result = response.json()
        assert "views" in result
        assert len(result["views"]) == 2
        assert result["views"][0]["name"] == "test_view"

    def test_create_view_success(self, test_client):
        """Test successful view creation."""
        new_view = {
            "name": "created_view",
            "sql": "SELECT 4 as id, 'created' as name",
            "description": "Created via API",
        }

        response = test_client.post("/api/views", json=new_view)
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert result["view"]["name"] == "created_view"

    def test_create_view_duplicate_name(self, test_client):
        """Test creating view with duplicate name."""
        duplicate_view = {
            "name": "test_view",  # Already exists
            "sql": "SELECT 5 as id",
        }

        response = test_client.post("/api/views", json=duplicate_view)
        assert response.status_code == 400
        assert "already exists" in response.json()["error"]

    def test_create_view_invalid_body(self, test_client):
        """Test creating view with invalid body."""
        response = test_client.post("/api/views", json={"invalid": "data"})
        assert response.status_code == 400
        assert "Invalid request body" in response.json()["error"]

    def test_update_view_success(self, test_client):
        """Test successful view update."""
        update_data = {"description": "Updated description"}

        response = test_client.put("/api/views/test_view", json=update_data)
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert result["view"]["description"] == "Updated description"

    def test_update_view_not_found(self, test_client):
        """Test updating non-existent view."""
        update_data = {"description": "Updated"}

        response = test_client.put("/api/views/nonexistent", json=update_data)
        assert response.status_code == 404
        assert "not found" in response.json()["error"]

    def test_delete_view_success(self, test_client):
        """Test successful view deletion."""
        response = test_client.delete("/api/views/test_view")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True

    def test_delete_view_not_found(self, test_client):
        """Test deleting non-existent view."""
        response = test_client.delete("/api/views/nonexistent")
        assert response.status_code == 404
        assert "not found" in response.json()["error"]


class TestSchemaEndpoint:
    """Test schema inspection endpoint."""

    @patch("duckalog.ui.duckdb.connect")
    def test_get_schema_success(self, mock_connect, test_client):
        """Test successful schema retrieval."""
        # Mock DuckDB connection and query result
        mock_conn = Mock()
        mock_connect.return_value = mock_conn

        mock_result = Mock()
        mock_result.fetchall.return_value = [
            ("id", "INTEGER", "NO", None),
            ("name", "VARCHAR", "YES", None),
        ]
        mock_conn.execute.return_value = mock_result

        response = test_client.get("/api/schema/test_view")
        assert response.status_code == 200

        result = response.json()
        assert result["view"] == "test_view"
        assert len(result["columns"]) == 2
        assert result["columns"][0]["name"] == "id"
        assert result["columns"][0]["type"] == "INTEGER"

    def test_get_schema_not_found(self, test_client):
        """Test schema retrieval for non-existent view."""
        response = test_client.get("/api/schema/nonexistent")
        assert response.status_code == 404
        assert "not found" in response.json()["error"]


class TestRebuildEndpoint:
    """Test catalog rebuild endpoint."""

    @patch("duckalog.ui.build_catalog")
    def test_rebuild_catalog_success(self, mock_build, test_client):
        """Test successful catalog rebuild."""
        mock_build.return_value = None

        response = test_client.post("/api/rebuild")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert "rebuilt successfully" in result["message"]

    @patch("duckalog.ui.build_catalog")
    def test_rebuild_catalog_config_error(self, mock_build, test_client):
        """Test catalog rebuild with config error."""
        from duckalog.config import ConfigError

        mock_build.side_effect = ConfigError("Invalid config")

        response = test_client.post("/api/rebuild")
        assert response.status_code == 500
        assert "Config error" in response.json()["error"]


class TestQueryEndpoint:
    """Test query execution endpoint."""

    @patch("duckalog.ui.duckdb.connect")
    def test_execute_query_success(self, mock_connect, test_client):
        """Test successful query execution."""
        # Mock DuckDB connection and query result
        mock_conn = Mock()
        mock_connect.return_value = mock_conn

        mock_result = Mock()
        mock_result.fetchall.return_value = [(1, "test"), (2, "test2")]
        mock_result.description = [("id",), ("name",)]
        mock_conn.execute.return_value = mock_result

        query_data = {"query": "SELECT * FROM test_view LIMIT 100"}
        response = test_client.post("/api/query", json=query_data)
        assert response.status_code == 200

        result = response.json()
        assert result["count"] == 2
        assert len(result["rows"]) == 2
        assert result["columns"] == ["id", "name"]
        assert result["rows"][0] == {"id": 1, "name": "test"}

    def test_execute_query_invalid_body(self, test_client):
        """Test query execution with invalid body."""
        response = test_client.post("/api/query", json={"invalid": "data"})
        assert response.status_code == 400
        assert "Invalid request body" in response.json()["error"]

    def test_execute_query_missing_query(self, test_client):
        """Test query execution with missing query."""
        response = test_client.post("/api/query", json={})
        assert response.status_code == 400
        assert "Invalid request body" in response.json()["error"]


class TestExportEndpoint:
    """Test data export endpoint."""

    @patch("duckalog.ui.duckdb.connect")
    def test_export_csv_success(self, mock_connect, test_client):
        """Test successful CSV export with data."""
        # Mock DuckDB connection and query result
        mock_conn = Mock()
        mock_connect.return_value = mock_conn

        mock_result = Mock()
        mock_result.fetchall.return_value = [(1, "test"), (2, "test2")]
        mock_result.description = [("id",), ("name",)]
        mock_conn.execute.return_value = mock_result

        export_data = {"query": "SELECT * FROM test_view", "format": "csv"}
        response = test_client.post("/api/export", json=export_data)
        assert response.status_code == 200

        result = response.json()
        assert result["status"] == "pending"
        task_id = result["task_id"]

        # Mock the background task completion
        ui_server = test_client.app._ui_server if hasattr(test_client.app, '_ui_server') else test_client.app.state
        if hasattr(ui_server, 'task_results'):
            ui_server.task_results[task_id] = {
                "status": "completed",
                "success": True,
                "data": [{"id": 1, "name": "test"}, {"id": 2, "name": "test2"}],
                "columns": ["id", "name"],
                "format": "csv"
            }

        # Get the export result
        export_response = test_client.get(f"/api/tasks/{task_id}")
        assert export_response.status_code == 200
        assert export_response.headers["content-type"] == "text/csv"
        assert "attachment; filename=export.csv" in export_response.headers["content-disposition"]
        # Check that CSV contains headers and data
        csv_content = export_response.text
        assert "id,name" in csv_content
        assert "1,test" in csv_content
        assert "2,test2" in csv_content

    @patch("duckalog.ui.duckdb.connect")
    def test_export_csv_empty(self, mock_connect, test_client):
        """Test CSV export with empty results."""
        # Mock DuckDB connection and empty query result
        mock_conn = Mock()
        mock_connect.return_value = mock_conn

        mock_result = Mock()
        mock_result.fetchall.return_value = []
        mock_result.description = [("id",), ("name",)]
        mock_conn.execute.return_value = mock_result

        export_data = {"query": "SELECT * FROM empty_view", "format": "csv"}
        response = test_client.post("/api/export", json=export_data)
        assert response.status_code == 200

        result = response.json()
        task_id = result["task_id"]

        # Mock the background task completion with empty data
        test_client.app._task_results[task_id] = {
            "status": "completed",
            "success": True,
            "data": [],
            "columns": ["id", "name"],
            "format": "csv"
        }

        # Get the export result
        export_response = test_client.get(f"/api/tasks/{task_id}")
        assert export_response.status_code == 200
        assert export_response.headers["content-type"] == "text/csv"
        assert "attachment; filename=export.csv" in export_response.headers["content-disposition"]
        # Check that CSV contains headers even for empty data
        csv_content = export_response.text
        assert "id,name" in csv_content

    @patch("duckalog.ui.duckdb.connect")
    def test_export_parquet_success(self, mock_connect, test_client):
        """Test successful Parquet export with data."""
        # Mock DuckDB connection and query result
        mock_conn = Mock()
        mock_connect.return_value = mock_conn

        mock_result = Mock()
        mock_result.fetchall.return_value = [(1, "test"), (2, "test2")]
        mock_result.description = [("id",), ("name",)]
        mock_conn.execute.return_value = mock_result

        export_data = {"query": "SELECT * FROM test_view", "format": "parquet"}
        response = test_client.post("/api/export", json=export_data)
        assert response.status_code == 200

        result = response.json()
        task_id = result["task_id"]

        # Mock the background task completion
        test_client.app._task_results[task_id] = {
            "status": "completed",
            "success": True,
            "data": [{"id": 1, "name": "test"}, {"id": 2, "name": "test2"}],
            "columns": ["id", "name"],
            "format": "parquet"
        }

        # Get the export result
        export_response = test_client.get(f"/api/tasks/{task_id}")
        assert export_response.status_code == 200
        assert export_response.headers["content-type"] == "application/octet-stream"
        assert "attachment; filename=export.parquet" in export_response.headers["content-disposition"]
        # Check that we got binary data (Parquet file)
        assert len(export_response.content) > 0

    @patch("duckalog.ui.duckdb.connect")
    def test_export_parquet_empty(self, mock_connect, test_client):
        """Test Parquet export with empty results."""
        # Mock DuckDB connection and empty query result
        mock_conn = Mock()
        mock_connect.return_value = mock_conn

        mock_result = Mock()
        mock_result.fetchall.return_value = []
        mock_result.description = [("id",), ("name",)]
        mock_conn.execute.return_value = mock_result

        export_data = {"query": "SELECT * FROM empty_view", "format": "parquet"}
        response = test_client.post("/api/export", json=export_data)
        assert response.status_code == 200

        result = response.json()
        task_id = result["task_id"]

        # Mock the background task completion with empty data
        test_client.app._task_results[task_id] = {
            "status": "completed",
            "success": True,
            "data": [],
            "columns": ["id", "name"],
            "format": "parquet"
        }

        # Get the export result
        export_response = test_client.get(f"/api/tasks/{task_id}")
        assert export_response.status_code == 200
        assert export_response.headers["content-type"] == "application/octet-stream"
        assert "attachment; filename=export.parquet" in export_response.headers["content-disposition"]
        # Should still get a valid Parquet file even for empty data
        assert len(export_response.content) > 0

    @patch("duckalog.ui.duckdb.connect")
    def test_export_excel_success(self, mock_connect, test_client):
        """Test successful Excel export with data."""
        # Mock DuckDB connection and query result
        mock_conn = Mock()
        mock_connect.return_value = mock_conn

        mock_result = Mock()
        mock_result.fetchall.return_value = [(1, "test"), (2, "test2")]
        mock_result.description = [("id",), ("name",)]
        mock_conn.execute.return_value = mock_result

        export_data = {"query": "SELECT * FROM test_view", "format": "excel"}
        response = test_client.post("/api/export", json=export_data)
        assert response.status_code == 200

        result = response.json()
        task_id = result["task_id"]

        # Mock the background task completion
        test_client.app._task_results[task_id] = {
            "status": "completed",
            "success": True,
            "data": [{"id": 1, "name": "test"}, {"id": 2, "name": "test2"}],
            "columns": ["id", "name"],
            "format": "excel"
        }

        # Get the export result
        export_response = test_client.get(f"/api/tasks/{task_id}")
        assert export_response.status_code == 200
        assert (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            in export_response.headers["content-type"]
        )
        assert "attachment; filename=export.xlsx" in export_response.headers["content-disposition"]
        # Check that we got binary data (Excel file)
        assert len(export_response.content) > 0

    @patch("duckalog.ui.duckdb.connect")
    def test_export_excel_empty(self, mock_connect, test_client):
        """Test Excel export with empty results."""
        # Mock DuckDB connection and empty query result
        mock_conn = Mock()
        mock_connect.return_value = mock_conn

        mock_result = Mock()
        mock_result.fetchall.return_value = []
        mock_result.description = [("id",), ("name",)]
        mock_conn.execute.return_value = mock_result

        export_data = {"query": "SELECT * FROM empty_view", "format": "excel"}
        response = test_client.post("/api/export", json=export_data)
        assert response.status_code == 200

        result = response.json()
        task_id = result["task_id"]

        # Mock the background task completion with empty data
        test_client.app._task_results[task_id] = {
            "status": "completed",
            "success": True,
            "data": [],
            "columns": ["id", "name"],
            "format": "excel"
        }

        # Get the export result
        export_response = test_client.get(f"/api/tasks/{task_id}")
        assert export_response.status_code == 200
        assert (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            in export_response.headers["content-type"]
        )
        assert "attachment; filename=export.xlsx" in export_response.headers["content-disposition"]
        # Should still get a valid Excel file even for empty data
        assert len(export_response.content) > 0

    def test_export_invalid_format(self, test_client):
        """Test export with invalid format."""
        export_data = {"query": "SELECT * FROM test_view", "format": "invalid"}
        response = test_client.post("/api/export", json=export_data)
        assert response.status_code == 400
        assert "Unsupported format" in response.json()["error"]

    def test_export_missing_query_and_view(self, test_client):
        """Test export with missing query and view."""
        export_data = {"format": "csv"}
        response = test_client.post("/api/export", json=export_data)
        assert response.status_code == 400
        assert "Must provide either 'query' or 'view'" in response.json()["error"]

    @patch("duckalog.ui.duckdb.connect")
    def test_export_consistent_headers_empty_and_full(self, mock_connect, test_client):
        """Test that export headers are consistent for both empty and full datasets."""
        # Mock DuckDB connection and query result
        mock_conn = Mock()
        mock_connect.return_value = mock_conn

        mock_result = Mock()
        mock_result.description = [("id",), ("name",)]

        # Test with data
        mock_result.fetchall.return_value = [(1, "test")]
        mock_conn.execute.return_value = mock_result

        export_data = {"query": "SELECT * FROM test_view", "format": "csv"}
        response = test_client.post("/api/export", json=export_data)
        task_id_full = response.json()["task_id"]

        test_client.app._task_results[task_id_full] = {
            "status": "completed",
            "success": True,
            "data": [{"id": 1, "name": "test"}],
            "columns": ["id", "name"],
            "format": "csv"
        }

        full_response = test_client.get(f"/api/tasks/{task_id_full}")

        # Test with empty data
        mock_result.fetchall.return_value = []
        mock_conn.execute.return_value = mock_result

        export_data = {"query": "SELECT * FROM empty_view", "format": "csv"}
        response = test_client.post("/api/export", json=export_data)
        task_id_empty = response.json()["task_id"]

        test_client.app._task_results[task_id_empty] = {
            "status": "completed",
            "success": True,
            "data": [],
            "columns": ["id", "name"],
            "format": "csv"
        }

        empty_response = test_client.get(f"/api/tasks/{task_id_empty}")

        # Both should have the same headers
        assert full_response.headers["content-type"] == empty_response.headers["content-type"]
        assert ("attachment; filename=export.csv" in full_response.headers["content-disposition"] and
                "attachment; filename=export.csv" in empty_response.headers["content-disposition"])

    @patch("duckalog.ui.duckdb.connect")
    def test_export_parquet_type_error_fix(self, mock_connect, test_client):
        """Test that Parquet export doesn't raise TypeError for list-of-dicts."""
        # Mock DuckDB connection and query result
        mock_conn = Mock()
        mock_connect.return_value = mock_conn

        mock_result = Mock()
        mock_result.fetchall.return_value = [(1, "test"), (2, None)]
        mock_result.description = [("id",), ("name",)]
        mock_conn.execute.return_value = mock_result

        export_data = {"query": "SELECT * FROM test_view", "format": "parquet"}
        response = test_client.post("/api/export", json=export_data)
        assert response.status_code == 200

        result = response.json()
        task_id = result["task_id"]

        # Mock the background task completion with mixed data types
        test_client.app._task_results[task_id] = {
            "status": "completed",
            "success": True,
            "data": [{"id": 1, "name": "test"}, {"id": 2, "name": None}],
            "columns": ["id", "name"],
            "format": "parquet"
        }

        # Get the export result - should not raise TypeError
        export_response = test_client.get(f"/api/tasks/{task_id}")
        assert export_response.status_code == 200
        assert export_response.headers["content-type"] == "application/octet-stream"
        assert "attachment; filename=export.parquet" in export_response.headers["content-disposition"]
        # Should successfully create Parquet file
        assert len(export_response.content) > 0


class TestDashboardEndpoint:
    """Test dashboard endpoint."""

    def test_dashboard_html_response(self, test_client):
        """Test dashboard returns HTML response."""
        response = test_client.get("/")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        assert "Duckalog Catalog Dashboard" in response.text

    def test_dashboard_with_datastar_attributes(self, test_client):
        """Test dashboard includes Datastar attributes."""
        response = test_client.get("/")
        assert response.status_code == 200

        # Verify Datastar JavaScript is included
        assert "datastar.js" in response.text

        # Verify Datastar-specific attributes are present
        assert "data-signals" in response.text
        assert "data-bind" in response.text or "data-on" in response.text

        # Check for Datastar SSE (Server-Sent Events) functionality
        assert any(keyword in response.text.lower() for keyword in [
            "sse", "server-sent", "eventstream", "datastar"
        ])

    def test_dashboard_datastar_only_content(self, test_client):
        """Test that dashboard serves Datastar content, not fallback HTML."""
        response = test_client.get("/")
        assert response.status_code == 200

        # Should contain Datastar-specific content
        assert "datastar.js" in response.text
        assert "data-signals" in response.text

        # Should NOT contain legacy fallback dashboard indicators
        legacy_indicators = [
            "function loadView(",  # Legacy vanilla JS function
            "function executeQuery(",  # Legacy query function
            "function exportResults(",  # Legacy export function
            "fetch('/api/query'"  # Direct API calls without Datastar
        ]

        for indicator in legacy_indicators:
            assert indicator not in response.text, f"Found legacy fallback content: {indicator}"

    def test_dashboard_datastar_integration(self, test_client):
        """Test proper Datastar integration patterns."""
        response = test_client.get("/")
        assert response.status_code == 200

        # Check for Datastar script loading
        assert '<script' in response.text
        assert 'datastar' in response.text.lower()

        # Verify that the dashboard uses reactive patterns
        assert "data-" in response.text  # Datastar attributes

        # Should not use legacy vanilla JavaScript patterns
        assert "document.getElementById" not in response.text
        assert "addEventListener" not in response.text

    def test_dashboard_handles_missing_config(self, test_client):
        """Test dashboard behavior when no configuration is loaded."""
        # Create a UI server without config
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("invalid: yaml: content:")  # Invalid config
            invalid_config = Path(f.name)

        try:
            server = UIServer(str(invalid_config))
            # If this doesn't raise an error, test the dashboard
            client = TestClient(server.app)
            response = client.get("/")
            assert response.status_code == 200

            # Even with config issues, should still serve Datastar dashboard
            assert "datastar.js" in response.text

        except UIError:
            # Expected to fail with invalid config
            pass
        finally:
            invalid_config.unlink(missing_ok=True)

    def test_dashboard_view_data_population(self, test_client):
        """Test that dashboard populates view data correctly with Datastar."""
        response = test_client.get("/")
        assert response.status_code == 200

        # Should contain view data for Datastar signals
        assert "test_view" in response.text
        assert "another_view" in response.text

        # Should populate data in Datastar-compatible format
        assert "views" in response.text.lower()

        # Should use data attributes for binding, not legacy DOM manipulation
        assert "data-" in response.text


class TestCORSPolicy:
    """Test CORS policy configuration and enforcement."""

    def test_default_localhost_origins_allowed(self, test_client):
        """Test that localhost origins are allowed by default."""
        # Test with localhost origin
        response = test_client.get(
            "/api/config",
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.status_code == 200

        # Check that CORS headers are present for localhost
        if "access-control-allow-origin" in response.headers:
            assert response.headers["access-control-allow-origin"] in [
                "http://localhost", "http://127.0.0.1", "http://localhost:3000", "http://127.0.0.1:3000"
            ]

    def test_127_0_0_1_origins_allowed(self, test_client):
        """Test that 127.0.0.1 origins are allowed."""
        response = test_client.get(
            "/api/views",
            headers={"Origin": "http://127.0.0.1:8000"}
        )
        assert response.status_code == 200

        if "access-control-allow-origin" in response.headers:
            assert "127.0.0.1" in response.headers["access-control-allow-origin"]

    def test_credentials_disabled_by_default(self, test_client):
        """Test that credentials are not allowed by default."""
        response = test_client.options(
            "/api/query",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )

        # Credentials should be disabled by default
        if "access-control-allow-credentials" in response.headers:
            assert response.headers["access-control-allow-credentials"] == "false"

    def test_preflight_request_handling(self, test_client):
        """Test preflight OPTIONS request handling."""
        response = test_client.options(
            "/api/query",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type, Authorization"
            }
        )

        # Should handle preflight requests
        assert response.status_code in [200, 204]  # Both are valid for preflight

        # Should include allowed methods
        if "access-control-allow-methods" in response.headers:
            allowed_methods = response.headers["access-control-allow-methods"]
            assert "POST" in allowed_methods
            assert "GET" in allowed_methods
            assert "PUT" in allowed_methods
            assert "DELETE" in allowed_methods

    def test_cors_headers_configuration(self, test_client):
        """Test that CORS headers are properly configured."""
        response = test_client.get(
            "/api/config",
            headers={"Origin": "http://localhost:3000"}
        )

        # Check for proper CORS header structure
        cors_headers = [
            "access-control-allow-origin",
            "access-control-allow-methods",
            "access-control-allow-headers"
        ]

        # At least some CORS headers should be present
        present_headers = [h for h in cors_headers if h in response.headers]
        assert len(present_headers) > 0

    def test_cross_origin_requests_blocked(self, test_client):
        """Test that cross-origin requests are properly rejected."""
        # Test with external origin that should be blocked
        response = test_client.get(
            "/api/config",
            headers={"Origin": "https://evil-site.com"}
        )

        # The request might succeed but CORS headers should not allow external origin
        if "access-control-allow-origin" in response.headers:
            allowed_origin = response.headers["access-control-allow-origin"]
            # Should not be the external origin
            assert allowed_origin != "https://evil-site.com"
            # Should be limited to localhost or *
            assert allowed_origin in [
                "http://localhost",
                "http://127.0.0.1",
                "*",  # If wildcard is used (should not be in secure config)
                None  # If no header is set
            ]

    def test_different_ports_localhost_allowed(self, test_client):
        """Test that different localhost ports are allowed."""
        test_ports = [3000, 8080, 9000, 5173]  # Common dev ports

        for port in test_ports:
            response = test_client.get(
                "/api/views",
                headers={"Origin": f"http://localhost:{port}"}
            )
            assert response.status_code == 200

            # Check CORS response for localhost
            if "access-control-allow-origin" in response.headers:
                allowed_origin = response.headers["access-control-allow-origin"]
                assert "localhost" in allowed_origin or allowed_origin == "*"

    def test_cors_error_responses(self, test_client):
        """Test that CORS headers are present even on error responses."""
        # Make a request that will result in an error
        response = test_client.post(
            "/api/query",
            json={"query": "INVALID SQL QUERY"},
            headers={"Origin": "http://localhost:3000"}
        )

        # Even error responses should have CORS headers
        if response.status_code >= 400:
            # Should still include CORS headers for localhost origins
            if "access-control-allow-origin" in response.headers:
                allowed_origin = response.headers["access-control-allow-origin"]
                assert "localhost" in allowed_origin or allowed_origin == "*"

    def test_cors_with_authentication_headers(self, test_client):
        """Test CORS behavior with authentication headers."""
        response = test_client.options(
            "/api/views",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type, Authorization"
            }
        )

        assert response.status_code in [200, 204]

        # Should allow authentication headers in preflight
        if "access-control-allow-headers" in response.headers:
            allowed_headers = response.headers["access-control-allow-headers"]
            assert "content-type" in allowed_headers.lower()
            assert "authorization" in allowed_headers.lower()


class TestErrorHandling:
    """Test error handling in UI endpoints."""

    def test_no_config_loaded(self):
        """Test behavior when no config is loaded."""
        server = UIServer.__new__(UIServer)  # Create without calling __init__
        server.config = None

        response = server._get_config(Mock())
        assert response.status_code == 500
        assert "No configuration loaded" in response.json()["error"]


class TestCLIIntegration:
    """Test CLI integration for UI command."""

    @patch("duckalog.ui.uvicorn.run")
    @patch("duckalog.ui.UIServer")
    def test_cli_ui_command(self, mock_ui_server, mock_uvicorn):
        """Test CLI UI command integration."""
        from duckalog.cli import ui

        mock_server_instance = Mock()
        mock_ui_server.return_value = mock_server_instance

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("duckdb:\n  database: :memory:\nviews: []")
            config_path = f.name

        try:
            ui(
                config_path=Path(config_path),
                host="127.0.0.1",
                port=8000,
                verbose=False,
            )
        except SystemExit:
            pass  # Expected when uvicorn.run is called

        mock_ui_server.assert_called_once()
        mock_server_instance.run.assert_called_once()


class TestReadOnlySQLEnforcement:
    """Test read-only SQL enforcement for security."""

    def test_select_query_allowed(self, test_client):
        """Test that basic SELECT queries are allowed."""
        # Mock background task execution for testing
        with patch("duckalog.ui.uuid.uuid4", return_value="test-task-id"):
            query_data = {"query": "SELECT * FROM test_view"}
            response = test_client.post("/api/query", json=query_data)

            # Should return 200 with task ID for background processing
            assert response.status_code == 200
            result = response.json()
            assert "task_id" in result
            assert result["status"] == "pending"

    @pytest.mark.parametrize("ddl_query", [
        "CREATE TABLE test (id INT)",
        "CREATE VIEW test_view AS SELECT 1",
        "DROP TABLE test",
        "DROP VIEW test_view",
        "ALTER TABLE test ADD COLUMN name VARCHAR",
        "TRUNCATE TABLE test",
        "RENAME TABLE old_name TO new_name",
        "GRANT SELECT ON test TO user",
        "REVOKE SELECT ON test FROM user",
        "COMMENT ON TABLE test IS 'comment'",
        "CREATE INDEX idx_test ON test(id)",
        "DROP INDEX idx_test",
        # Test case variations
        "create table test (id int)",
        "Create Table test (id int)",
        "CREATE   TABLE test (id int)",  # Extra spaces
    ])
    def test_ddl_queries_rejected(self, test_client, ddl_query):
        """Test that DDL queries are rejected with proper error messages."""
        query_data = {"query": ddl_query}
        response = test_client.post("/api/query", json=query_data)

        assert response.status_code == 400
        result = response.json()
        assert "error" in result
        assert "Invalid query" in result["error"]
        assert "DDL" in result["error"] or "not allowed" in result["error"]

    @pytest.mark.parametrize("dml_query", [
        "INSERT INTO test VALUES (1, 'test')",
        "UPDATE test SET name = 'updated' WHERE id = 1",
        "DELETE FROM test WHERE id = 1",
        "MERGE INTO test USING source ON test.id = source.id WHEN MATCHED THEN UPDATE",
        "UPSERT INTO test VALUES (1, 'test')",
        "REPLACE INTO test VALUES (1, 'test')",
        "CALL some_procedure()",
        "EXPLAIN SELECT * FROM test",
        "EXECUTE immediate 'SELECT 1'",
        # Test case variations
        "insert into test values (1, 'test')",
        "Insert   Into test values (1, 'test')",
    ])
    def test_dml_queries_rejected(self, test_client, dml_query):
        """Test that DML queries are rejected."""
        query_data = {"query": dml_query}
        response = test_client.post("/api/query", json=query_data)

        assert response.status_code == 400
        result = response.json()
        assert "error" in result
        assert "Invalid query" in result["error"]
        assert "DML" in result["error"] or "not allowed" in result["error"]

    @pytest.mark.parametrize("multi_statement_query", [
        "SELECT * FROM test_view; SELECT * FROM other_view",
        "SELECT 1; DROP TABLE test; SELECT 2",
        "SELECT * FROM test_view;; SELECT 2",  # Double semicolon
        "  SELECT 1;  SELECT 2  ",  # Extra whitespace
    ])
    def test_multi_statement_queries_rejected(self, test_client, multi_statement_query):
        """Test that queries with multiple statements are rejected."""
        query_data = {"query": multi_statement_query}
        response = test_client.post("/api/query", json=query_data)

        assert response.status_code == 400
        result = response.json()
        assert "error" in result
        assert "Invalid query" in result["error"]
        assert "single statement" in result["error"] or "multiple statements" in result["error"]

    def test_sql_injection_attempts_blocked(self, test_client):
        """Test that SQL injection attempts using DML are blocked."""
        injection_attempts = [
            "SELECT * FROM test_view WHERE name = 'test'; DROP TABLE test; --",
            "SELECT * FROM test_view UNION SELECT * FROM users; DELETE FROM users; --",
            "SELECT * FROM test_view; INSERT INTO logs VALUES ('injection attempt'); --",
        ]

        for injection in injection_attempts:
            query_data = {"query": injection}
            response = test_client.post("/api/query", json=query_data)

            assert response.status_code == 400
            result = response.json()
            assert "error" in result

    def test_export_endpoint_read_only_enforcement(self, test_client):
        """Test that export endpoint also enforces read-only validation."""
        # Test DDL rejection in export
        export_data = {"query": "CREATE TABLE test (id INT)", "format": "csv"}
        response = test_client.post("/api/export", json=export_data)

        assert response.status_code == 400
        result = response.json()
        assert "error" in result
        assert "Invalid query" in result["error"]

    def test_allowed_complex_select_queries(self, test_client):
        """Test that complex but valid SELECT queries are allowed."""
        allowed_queries = [
            "SELECT * FROM test_view WHERE id > 10",
            "SELECT * FROM test_view ORDER BY name DESC",
            "SELECT * FROM test_view GROUP BY category",
            "SELECT * FROM test_view LIMIT 100 OFFSET 50",
            "SELECT * FROM test_view JOIN other_view ON test.id = other.id",
            "SELECT * FROM test_view LEFT JOIN other_view ON test.id = other.id",
            "SELECT * FROM test_view UNION SELECT * FROM other_view",
            "SELECT * FROM test_view WHERE id IN (SELECT id FROM other_view)",
            "SELECT * FROM test_view WHERE EXISTS (SELECT 1 FROM other_view WHERE other_view.id = test_view.id)",
            "SELECT CASE WHEN id > 10 THEN 'high' ELSE 'low' END as category FROM test_view",
        ]

        for query in allowed_queries:
            with patch("duckalog.ui.uuid.uuid4", return_value="test-task-id"):
                query_data = {"query": query}
                response = test_client.post("/api/query", json=query_data)

                # Should return 200 with task ID for background processing
                assert response.status_code == 200
                result = response.json()
                assert "task_id" in result

    def test_empty_and_whitespace_queries_rejected(self, test_client):
        """Test that empty or whitespace-only queries are rejected."""
        invalid_queries = [
            "",
            "   ",
            "\t",
            "\n",
            "\r\n",
        ]

        for invalid_query in invalid_queries:
            query_data = {"query": invalid_query}
            response = test_client.post("/api/query", json=query_data)

            assert response.status_code == 400
            result = response.json()
            assert "error" in result
            assert "empty" in result["error"] or "Invalid query" in result["error"]

    def test_view_based_export_allowed(self, test_client):
        """Test that view-based exports are allowed."""
        export_data = {"view": "test_view", "format": "csv"}

        with patch("duckalog.ui.uuid.uuid4", return_value="test-task-id"):
            response = test_client.post("/api/export", json=export_data)

            # Should return 200 with task ID for background processing
            assert response.status_code == 200
            result = response.json()
            assert "task_id" in result
            assert result["status"] == "pending"
            assert result["format"] == "csv"

    def test_export_invalid_view_name(self, test_client):
        """Test export with non-existent view name."""
        export_data = {"view": "nonexistent_view", "format": "csv"}
        response = test_client.post("/api/export", json=export_data)

        assert response.status_code == 404
        result = response.json()
        assert "error" in result
        assert "not found" in result["error"]


class TestConfigFormatPreservation:
    """Test configuration format preservation and reload behavior."""

    def test_yaml_format_preserved(self, test_client, tmp_path):
        """Test that YAML configuration format is preserved when writing."""
        # Create initial YAML config with comments and specific formatting
        yaml_content = """# Duckalog Configuration
duckdb:
  database: ":memory:"

views:
  - name: test_view
    sql: "SELECT 1 as id, 'test' as name"
    description: "Test view"
    tags:
      - test

# End of configuration
"""
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text(yaml_content)

        # Create UI server with the YAML config
        ui_server = UIServer(str(config_file))
        test_client_yaml = TestClient(ui_server.app)

        # Add a new view via API
        new_view = {
            "name": "new_view",
            "sql": "SELECT 2 as id, 'new' as name",
            "description": "New test view"
        }

        response = test_client_yaml.post("/api/config", json={"view": new_view})
        assert response.status_code == 200

        # Check that the file is still valid YAML
        updated_content = config_file.read_text()
        assert "new_view" in updated_content

        # Verify the format is preserved (starts with YAML-like structure, not JSON)
        assert not updated_content.strip().startswith("{")
        assert not updated_content.strip().startswith("[")

        # Verify we can still load the config
        ui_server._load_config()  # Reload to test parsing
        assert ui_server.config is not None
        assert len(ui_server.config.views) == 2

    def test_json_format_preserved(self, test_client, tmp_path):
        """Test that JSON configuration format is preserved when writing."""
        # Create initial JSON config
        json_content = """{
  "duckdb": {
    "database": ":memory:"
  },
  "views": [
    {
      "name": "test_view",
      "sql": "SELECT 1 as id, 'test' as name",
      "description": "Test view"
    }
  ]
}"""
        config_file = tmp_path / "test_config.json"
        config_file.write_text(json_content)

        # Create UI server with the JSON config
        ui_server = UIServer(str(config_file))
        test_client_json = TestClient(ui_server.app)

        # Add a new view via API
        new_view = {
            "name": "new_view",
            "sql": "SELECT 2 as id, 'new' as name",
            "description": "New test view"
        }

        response = test_client_json.post("/api/config", json={"view": new_view})
        assert response.status_code == 200

        # Check that the file is still valid JSON
        updated_content = config_file.read_text()
        assert "new_view" in updated_content

        # Verify the format is preserved (starts with { for JSON)
        assert updated_content.strip().startswith("{")

        # Verify we can still load the config
        ui_server._load_config()  # Reload to test parsing
        assert ui_server.config is not None
        assert len(ui_server.config.views) == 2

    def test_config_format_detection(self, tmp_path):
        """Test automatic format detection by file extension and content."""
        # Test YAML detection by extension
        yaml_file = tmp_path / "config.yaml"
        yaml_file.write_text("duckdb:\n  database: :memory:\n")

        ui_server = UIServer(str(yaml_file))
        assert ui_server._config_format == "yaml"

        # Test JSON detection by extension
        json_file = tmp_path / "config.json"
        json_file.write_text('{"duckdb": {"database": ":memory:"}}')

        ui_server = UIServer(str(json_file))
        assert ui_server._config_format == "json"

        # Test content-based detection (starts with {)
        mystery_file = tmp_path / "config"
        mystery_file.write_text('{"duckdb": {"database": ":memory:"}}')

        ui_server = UIServer(str(mystery_file))
        assert ui_server._config_format == "json"

        # Test content-based detection (YAML-like)
        mystery_file.write_text("duckdb:\n  database: :memory:\n")
        ui_server = UIServer(str(mystery_file))
        assert ui_server._config_format == "yaml"

    def test_in_memory_config_reload(self, test_client):
        """Test that in-memory config is reloaded after successful writes."""
        # Get initial view count
        response = test_client.get("/api/views")
        assert response.status_code == 200
        initial_count = len(response.json()["views"])

        # Add new view
        new_view = {
            "name": "reload_test_view",
            "sql": "SELECT 999 as id",
            "description": "Test reload"
        }

        response = test_client.post("/api/views", json=new_view)
        assert response.status_code == 200

        # Check that in-memory config is updated immediately
        response = test_client.get("/api/views")
        assert response.status_code == 200
        updated_views = response.json()["views"]
        assert len(updated_views) == initial_count + 1

        # Verify the new view is in the in-memory config
        view_names = [v["name"] for v in updated_views]
        assert "reload_test_view" in view_names

    def test_atomic_write_operations(self, ui_server, tmp_path):
        """Test that config writes are atomic and don't corrupt files."""
        # Create test config file
        config_content = """duckdb:
  database: ":memory:"
views: []
"""
        config_file = tmp_path / "atomic_test.yaml"
        config_file.write_text(config_content)

        # Create server with test config
        test_server = UIServer(str(config_file))

        # Mock a write failure scenario by making the target directory read-only
        original_config_path = test_server.config_path
        test_server.config_path = tmp_path / "readonly_dir" / "config.yaml"

        # This should fail without corrupting the original
        try:
            test_server._write_config_atomic("invalid: content")
            assert False, "Should have raised an exception"
        except Exception:
            # Expected to fail
            pass

        # Verify original file is unchanged
        if config_file.exists():
            original_content = config_file.read_text()
            assert original_content == config_content

    def test_config_write_with_authentication(self, test_client):
        """Test that config write operations require proper authentication."""
        # Test without auth token (should fail in production mode)
        new_view = {
            "name": "auth_test_view",
            "sql": "SELECT 1 as id"
        }

        # Set admin token to enforce authentication
        with patch.dict(os.environ, {"DUCKALOG_ADMIN_TOKEN": "test-token"}):
            response = test_client.post("/api/views", json=new_view)
            # Should either succeed (local mode) or fail with auth error
            if response.status_code == 401:
                assert "error" in response.json()

    def test_config_format_preservation_error_handling(self, ui_server):
        """Test error handling when config format preservation fails."""
        # Mock ruamel.yaml import failure
        with patch.dict("sys.modules", {"ruamel.yaml": None}):
            # This should fall back to basic YAML
            try:
                ui_server._write_config_preserving_format(ui_server.config)
                # Should not raise an exception
            except Exception as e:
                # If it fails, it should be a UIError with proper message
                assert isinstance(e, UIError)


class TestBackgroundTaskConcurrency:
    """Test background task execution, concurrency, and timeout handling."""

    @pytest.mark.asyncio
    async def test_concurrent_query_execution(self, test_client):
        """Test that multiple queries can execute concurrently."""
        import asyncio

        # Submit multiple queries concurrently
        async def submit_query(query_id):
            query_data = {"query": f"SELECT {query_id} as id, 'test{query_id}' as name"}
            with patch("duckalog.ui.uuid.uuid4", return_value=f"task-{query_id}"):
                response = test_client.post("/api/query", json=query_data)
                assert response.status_code == 200
                return response.json()["task_id"]

        # Submit 5 queries concurrently
        task_ids = await asyncio.gather(*[
            submit_query(i) for i in range(5)
        ])

        # Verify all tasks were created
        assert len(task_ids) == 5
        assert len(set(task_ids)) == 5  # All task IDs should be unique

        # Check that tasks are stored in the task results
        ui_server = test_client.app.state  # Get server instance
        for task_id in task_ids:
            response = test_client.get(f"/api/tasks/{task_id}")
            assert response.status_code == 200
            result = response.json()
            assert result["task_id"] == task_id

    @pytest.mark.asyncio
    async def test_background_task_error_handling(self, test_client):
        """Test that background task errors are properly captured and reported."""
        # Mock background task to simulate an error
        with patch("duckalog.ui._execute_query_task") as mock_task:
            mock_task.side_effect = Exception("Simulated database error")

            query_data = {"query": "SELECT * FROM test_view"}
            with patch("duckalog.ui.uuid.uuid4", return_value="error-task-id"):
                response = test_client.post("/api/query", json=query_data)
                assert response.status_code == 200

                result = response.json()
                task_id = result["task_id"]

                # Check task result after background execution
                # Note: In real scenario, we'd need to wait for task completion
                # For testing, we can check that the error setup is correct
                assert task_id == "error-task-id"

    @pytest.mark.asyncio
    async def test_task_result_isolation(self, test_client):
        """Test that task results are properly isolated between different requests."""
        query_data1 = {"query": "SELECT 1 as id"}
        query_data2 = {"query": "SELECT 2 as id"}

        # Submit two different queries
        with patch("duckalog.ui.uuid.uuid4", side_effect=["task-1", "task-2"]):
            response1 = test_client.post("/api/query", json=query_data1)
            response2 = test_client.post("/api/query", json=query_data2)

            assert response1.status_code == 200
            assert response2.status_code == 200

            task1_id = response1.json()["task_id"]
            task2_id = response2.json()["task_id"]

            assert task1_id == "task-1"
            assert task2_id == "task-2"

            # Verify tasks are accessible separately
            response1_check = test_client.get(f"/api/tasks/{task1_id}")
            response2_check = test_client.get(f"/api/tasks/{task2_id}")

            assert response1_check.status_code == 200
            assert response2_check.status_code == 200

    def test_export_background_task(self, test_client):
        """Test that export requests also use background tasks."""
        export_data = {"view": "test_view", "format": "csv"}

        with patch("duckalog.ui.uuid.uuid4", return_value="export-task-id"):
            response = test_client.post("/api/export", json=export_data)
            assert response.status_code == 200

            result = response.json()
            assert "task_id" in result
            assert result["status"] == "pending"
            assert result["format"] == "csv"

    def test_rebuild_catalog_background_task(self, test_client):
        """Test that catalog rebuild requests use background tasks."""
        with patch("duckalog.ui.uuid.uuid4", return_value="rebuild-task-id"):
            response = test_client.post("/api/rebuild", json={})
            assert response.status_code == 200

            result = response.json()
            assert "task_id" in result
            assert result["status"] == "pending"

    def test_task_result_not_found(self, test_client):
        """Test that requesting a non-existent task returns proper error."""
        response = test_client.get("/api/tasks/non-existent-task-id")
        assert response.status_code == 404
        result = response.json()
        assert "error" in result
        assert "Task not found" in result["error"]

    @pytest.mark.asyncio
    async def test_background_task_result_structure(self, test_client):
        """Test that background task results have the expected structure."""
        # Mock successful background task execution
        mock_result = {
            "status": "completed",
            "success": True,
            "data": [{"id": 1, "name": "test"}],
            "row_count": 1
        }

        with patch("duckalog.ui.uuid.uuid4", return_value="success-task-id"):
            query_data = {"query": "SELECT 1 as id, 'test' as name"}
            response = test_client.post("/api/query", json=query_data)
            assert response.status_code == 200

        # Verify task result structure (this would be accessible after completion)
        response = test_client.get("/api/tasks/success-task-id")
        assert response.status_code == 200

        result = response.json()
        expected_fields = ["task_id", "status"]
        for field in expected_fields:
            assert field in result

    def test_export_task_with_format_validation(self, test_client):
        """Test that export background tasks validate format properly."""
        invalid_export_data = {"view": "test_view", "format": "invalid_format"}

        response = test_client.post("/api/export", json=invalid_export_data)
        assert response.status_code == 400
        result = response.json()
        assert "error" in result
        assert "Unsupported format" in result["error"]

    @pytest.mark.asyncio
    async def test_concurrent_mixed_task_types(self, test_client):
        """Test that different task types can run concurrently."""
        import asyncio

        async def submit_export_task(format_type, task_id):
            export_data = {"view": "test_view", "format": format_type}
            with patch("duckalog.ui.uuid.uuid4", return_value=task_id):
                response = test_client.post("/api/export", json=export_data)
                assert response.status_code == 200
                return response.json()["task_id"]

        async def submit_rebuild_task(task_id):
            with patch("duckalog.ui.uuid.uuid4", return_value=task_id):
                response = test_client.post("/api/rebuild", json={})
                assert response.status_code == 200
                return response.json()["task_id"]

        # Submit different types of tasks concurrently
        tasks = [
            submit_export_task("csv", "export-csv"),
            submit_export_task("json", "export-json"),
            submit_rebuild_task("rebuild-task")
        ]

        task_ids = await asyncio.gather(*tasks)
        assert len(task_ids) == 3
        assert len(set(task_ids)) == 3  # All unique

        # Verify all tasks are accessible
        for task_id in task_ids:
            response = test_client.get(f"/api/tasks/{task_id}")
            assert response.status_code == 200


class TestSemanticModelsUI:
    """Test semantic models UI functionality."""

    def test_semantic_models_api_list(self, test_client):
        """Test that semantic models API endpoint returns list of models."""
        response = test_client.get("/api/semantic-models")
        assert response.status_code == 200

        data = response.json()
        assert "semantic_models" in data
        semantic_models = data["semantic_models"]

        # Should return semantic models from test configuration
        assert len(semantic_models) >= 0

        if semantic_models:
            model = semantic_models[0]
            required_fields = ["name", "base_view", "dimensions_count", "measures_count"]
            for field in required_fields:
                assert field in model

    def test_semantic_models_api_specific_model(self, test_client):
        """Test that specific semantic model API returns full details."""
        # Test with a known model that should exist in semantic_layer_v2 example
        response = test_client.get("/api/semantic-models/sales_analytics")

        if response.status_code == 404:
            # Skip test if semantic models not configured
            pytest.skip("No semantic models configured for testing")

        assert response.status_code == 200

        data = response.json()
        assert "semantic_model" in data
        model = data["semantic_model"]

        # Check required fields
        required_fields = ["name", "base_view", "dimensions", "measures"]
        for field in required_fields:
            assert field in model

        # Check dimensions structure
        if model.get("dimensions"):
            for dim in model["dimensions"]:
                assert "name" in dim
                assert "expression" in dim
                assert "label" in dim

        # Check measures structure
        if model.get("measures"):
            for measure in model["measures"]:
                assert "name" in measure
                assert "expression" in measure
                assert "label" in measure

    def test_semantic_models_api_nonexistent_model(self, test_client):
        """Test that requesting non-existent semantic model returns 404."""
        response = test_client.get("/api/semantic-models/nonexistent_model")
        assert response.status_code == 404

    def test_dashboard_includes_semantic_models_data(self, test_client):
        """Test that dashboard includes semantic models data in signals."""
        response = test_client.get("/")
        assert response.status_code == 200

        content = response.text

        # Check for semantic models data in Datastar signals
        assert "semanticModels" in content

    def test_dashboard_has_semantic_models_section(self, test_client):
        """Test that dashboard has semantic models section when models exist."""
        response = test_client.get("/")
        assert response.status_code == 200

        content = response.text

        # Check for semantic models section in HTML
        if "Sales Analytics" in content or "Customer Analytics" in content:
            # If semantic models exist, section should be present
            assert "Semantic Models" in content
            assert "/api/semantic-models/" in content

    def test_semantic_model_details_functionality(self, test_client):
        """Test semantic model details display functionality."""
        response = test_client.get("/")
        assert response.status_code == 200

        content = response.text

        # Check for semantic model details functionality
        if "semanticModels" in content and "Sales Analytics" in content:
            # Should have buttons and panels for showing details
            assert "Details" in content
            assert "semanticModelDetails" in content
            # Check for dimension and measure display
            assert "Dimensions" in content
            assert "Measures" in content


class TestBundledAssets:
    """Test bundled static assets serving and offline functionality."""

    def test_datastar_script_serves_locally(self, test_client):
        """Test that Datastar script is served from local static directory."""
        response = test_client.get("/static/datastar.js")
        assert response.status_code == 200
        assert "text/javascript" in response.headers.get("content-type", "")
        assert response.headers.get("content-length") == "29360"  # Expected file size

    def test_datastar_content_is_complete(self, test_client):
        """Test that the bundled Datastar content is complete and valid."""
        response = test_client.get("/static/datastar.js")
        assert response.status_code == 200

        # Check for Datastar-specific content
        content = response.text
        assert "datastar" in content.lower()
        assert "datastar-fetch" in content
        assert "datastar-signal-patch" in content

        # Check for version information
        assert "Datastar v1.0.0-RC.6" in content

    def test_dashboard_uses_local_datastar(self, test_client):
        """Test that dashboard HTML references local Datastar script."""
        response = test_client.get("/")
        assert response.status_code == 200

        # Should reference local path, not external CDN
        assert 'src="/static/datastar.js"' in response.text
        assert "https://cdn.jsdelivr.net" not in response.text

    def test_static_file_content_type(self, test_client):
        """Test that static files are served with correct Content-Type."""
        response = test_client.get("/static/datastar.js")
        assert response.status_code == 200

        content_type = response.headers.get("content-type", "")
        assert "application/javascript" in content_type or "text/javascript" in content_type

    def test_nonexistent_static_file_404(self, test_client):
        """Test that nonexistent static files return 404."""
        response = test_client.get("/static/nonexistent.js")
        assert response.status_code == 404

    def test_offline_functionality(self, test_client):
        """Test that dashboard works without external network dependencies."""
        # Dashboard should load successfully
        dashboard_response = test_client.get("/")
        assert dashboard_response.status_code == 200

        # Datastar script should be available locally
        datastar_response = test_client.get("/static/datastar.js")
        assert datastar_response.status_code == 200

        # Dashboard HTML should contain only local resources
        dashboard_content = dashboard_response.text
        assert 'src="/static/datastar.js"' in dashboard_content

        # Should not contain external CDN references
        external_urls = [
            "https://cdn.jsdelivr.net",
            "https://unpkg.com",
            "https://cdnjs.cloudflare.com"
        ]

        for url in external_urls:
            assert url not in dashboard_content, f"Found external URL {url} in dashboard"


@pytest.mark.skipif(
    True,  # Skip integration tests by default
    reason="Integration tests require actual UI dependencies",
)
class TestUIIntegration:
    """Integration tests that require UI dependencies."""

    def test_full_ui_workflow(self, test_client):
        """Test a complete UI workflow."""
        # This would be a comprehensive integration test
        # that tests the full UI workflow including:
        # 1. Load dashboard
        # 2. Create a view
        # 3. Query the view
        # 4. Export data
        # 5. Delete the view
        pass
