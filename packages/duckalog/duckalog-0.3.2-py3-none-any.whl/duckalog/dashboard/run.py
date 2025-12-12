"""Entry points for running the dashboard from Python."""

from __future__ import annotations

import uvicorn

from .app import create_app
from .state import DashboardContext


def run_dashboard(config_or_path, *, host: str = "127.0.0.1", port: int = 8787, row_limit: int = 500):
    """Run the dashboard for a given config or config path."""
    if isinstance(config_or_path, str):
        ctx = DashboardContext.from_path(config_or_path, row_limit=row_limit)
    else:
        ctx = DashboardContext(config_or_path, config_path=None, row_limit=row_limit)

    app = create_app(ctx)
    uvicorn.run(app, host=host, port=port)


__all__ = ["run_dashboard"]
