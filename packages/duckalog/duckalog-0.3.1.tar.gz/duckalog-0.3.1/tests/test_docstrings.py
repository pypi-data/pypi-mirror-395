"""Docstring quality checks for the public API.

These tests ensure that everything exported via ``duckalog.__all__`` has a
non-empty docstring so that API reference tooling (and interactive users) have
something useful to display.
"""

from __future__ import annotations

from duckalog import __all__ as public_names
import duckalog


def test_public_api_has_docstrings() -> None:
    """Every symbol in ``duckalog.__all__`` should have a non-empty docstring."""

    missing = []
    for name in public_names:
        obj = getattr(duckalog, name)
        doc = getattr(obj, "__doc__", None)
        if not doc or not doc.strip():
            missing.append(name)

    assert not missing, f"Missing docstrings for public API symbols: {missing}"
