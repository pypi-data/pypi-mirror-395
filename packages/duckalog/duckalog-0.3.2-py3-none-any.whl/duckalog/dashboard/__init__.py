"""Dashboard entry points for duckalog."""

from .app import create_app
from .run import run_dashboard

__all__ = ["create_app", "run_dashboard"]
