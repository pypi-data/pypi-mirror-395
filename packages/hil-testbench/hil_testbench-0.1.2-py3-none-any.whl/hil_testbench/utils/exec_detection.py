"""Helpers for checking binary availability and capabilities."""

from __future__ import annotations

import shutil
import subprocess
from collections.abc import Sequence


def is_binary_available(binary: str) -> bool:
    """Return True if the binary is discoverable on PATH."""

    return shutil.which(binary) is not None


def supports_flags(binary: str, flags: Sequence[str], timeout: float = 2.0) -> bool:
    """Return True if running the binary with the provided flags succeeds."""

    if not is_binary_available(binary):
        return False

    try:
        result = subprocess.run(
            [binary, *flags],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError, ValueError):
        return False

    return result.returncode == 0


def probe_version_output(binary: str, timeout: float = 2.0) -> str:
    """Return stdout+stderr from `<binary> --version` (empty on failure)."""

    if not is_binary_available(binary):
        return ""

    try:
        result = subprocess.run(
            [binary, "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError, ValueError):
        return ""

    return (result.stdout or "") + (result.stderr or "")
