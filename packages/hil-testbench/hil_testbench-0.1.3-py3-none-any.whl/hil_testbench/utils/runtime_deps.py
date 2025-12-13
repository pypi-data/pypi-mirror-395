"""Runtime dependency helpers for optional heavy packages."""

from __future__ import annotations

from importlib import import_module
from typing import Any

_PARAMIKO_MODULE = "paramiko"


def _load_paramiko() -> Any:
    return import_module(_PARAMIKO_MODULE)


def require_paramiko() -> Any:
    """Import and return the `paramiko` module, raising a friendly error."""

    try:
        return _load_paramiko()
    except ImportError as exc:  # pragma: no cover - simple import guard
        raise RuntimeError(
            "Missing runtime dependency 'paramiko'. Install it with: "
            "python -m pip install 'paramiko>=3.0.0'"
        ) from exc


def get_paramiko() -> Any | None:
    """Return the `paramiko` module if available, otherwise `None`."""

    try:
        return _load_paramiko()
    except ImportError:
        return None
