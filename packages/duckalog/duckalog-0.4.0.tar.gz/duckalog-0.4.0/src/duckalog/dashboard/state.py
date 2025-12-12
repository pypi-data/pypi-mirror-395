"""Shared dashboard state and helpers."""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass

import duckdb

from ..config import Config, ViewConfig, load_config
from ..engine import EngineError, build_catalog
from ..logging_utils import log_error


def _now() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone.utc)


@dataclass
class BuildStatus:
    started_at: _dt.datetime
    completed_at: _dt.datetime | None = None
    success: bool | None = None
    message: str | None = None
    summary: str | None = None

    @property
    def duration_seconds(self) -> float | None:
        if self.completed_at is None:
            return None
        return (self.completed_at - self.started_at).total_seconds()


@dataclass
class QueryResult:
    columns: list[str]
    rows: list[tuple]
    truncated: bool
    error: str | None = None


class DashboardContext:
    """Holds catalog context for the dashboard instance."""

    def __init__(self, config: Config, config_path: str | None = None, row_limit: int = 500):
        self.config = config
        self.config_path = str(config_path) if config_path else None
        self.row_limit = row_limit
        self.last_build: BuildStatus | None = None

        # Resolve database path from config
        self.db_path = config.duckdb.database

    @classmethod
    def from_path(cls, config_path: str, *, row_limit: int = 500) -> DashboardContext:
        cfg = load_config(config_path)
        return cls(cfg, config_path=config_path, row_limit=row_limit)

    # --- Catalog metadata helpers -------------------------------------------------
    def view_list(self) -> list[dict[str, str]]:
        results: list[dict[str, str]] = []
        for view in self.config.views:
            results.append(
                {
                    "name": view.name,
                    "source": view.source or "sql",
                    "uri": view.uri or "",
                    "database": view.database or "",
                    "table": view.table or "",
                    "semantic": "yes"
                    if any(m.base_view == view.name for m in self.config.semantic_models)
                    else "no",
                }
            )
        return results

    def get_view(self, name: str) -> ViewConfig | None:
        for view in self.config.views:
            if view.name == name:
                return view
        return None

    def semantic_for_view(self, name: str):
        return [m for m in self.config.semantic_models if m.base_view == name]

    # --- DuckDB interactions ------------------------------------------------------
    def _connect(self):
        return duckdb.connect(self.db_path)

    def run_query(self, sql: str) -> QueryResult:
        try:
            with self._connect() as conn:
                cursor = conn.execute(sql)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
        except Exception as exc:  # pragma: no cover - depends on duckdb internals
            return QueryResult(columns=[], rows=[], truncated=False, error=str(exc))

        truncated = False
        if len(rows) > self.row_limit:
            rows = rows[: self.row_limit]
            truncated = True

        return QueryResult(columns=columns, rows=rows, truncated=truncated, error=None)

    def trigger_build(self) -> BuildStatus:
        status = BuildStatus(started_at=_now())
        self.last_build = status

        try:
            if self.config_path is None:
                raise EngineError("Config path required to run build from dashboard.")
            build_catalog(self.config_path)
            status.success = True
            status.summary = "Catalog build completed"
        except EngineError as exc:
            log_error("Dashboard build failed", error=str(exc))
            status.success = False
            status.message = str(exc)
        finally:
            status.completed_at = _now()

        return status


def summarize_config(context: DashboardContext) -> dict[str, str]:
    cfg = context.config
    db = cfg.duckdb.database
    attachments = (
        len(cfg.attachments.duckdb)
        + len(cfg.attachments.sqlite)
        + len(cfg.attachments.postgres)
        + len(cfg.attachments.duckalog)
    )
    return {
        "config_path": context.config_path or "",
        "database": db,
        "views": str(len(cfg.views)),
        "attachments": str(attachments),
        "semantic_models": str(len(cfg.semantic_models)),
    }
