"""Execution helpers for ExecutionContext.

This package intentionally avoids importing submodules at import time to break
heavy dependency chains (notably ``data_processing.pipeline``) that are not
needed for lightweight structural types such as ``DisplayBackendProtocol``.
"""

from __future__ import annotations

__all__ = []
