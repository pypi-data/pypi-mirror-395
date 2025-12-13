"""Network helpers for streaming tasks."""

from __future__ import annotations

import re
import socket
import subprocess
import time
from typing import Literal


def kill_port(port: int, protocol: Literal["tcp", "udp"] = "tcp") -> str:
    """Return a command string to free a port safely."""

    return f"fuser -kn {protocol} {port} >/dev/null 2>&1 || true"


def detect_version(binary: str, version_regex: str) -> tuple[int, ...] | None:
    """Parse a binary's version from --version output using a regex."""

    try:
        result = subprocess.run(
            [binary, "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    output = (result.stdout or "") + (result.stderr or "")
    match = re.search(version_regex, output)
    if not match:
        return None
    try:
        return tuple(int(part) for part in match.groups())
    except ValueError:
        return None


def bits_to_human(bits_per_sec: float) -> str:
    """Convert bits/sec to a human-readable string."""

    units = [
        ("Tbits/sec", 1_000_000_000_000),
        ("Gbits/sec", 1_000_000_000),
        ("Mbits/sec", 1_000_000),
        ("Kbits/sec", 1_000),
        ("bits/sec", 1),
    ]
    for name, size in units:
        if bits_per_sec >= size:
            return f"{bits_per_sec / size:.1f} {name}"
    return f"{bits_per_sec:.1f} bits/sec"


def is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    """Return True if a TCP port is reachable on host within timeout."""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            return sock.connect_ex((host, port)) == 0
        except OSError:
            return False


def wait_for_port_state(
    host: str,
    port: int,
    *,
    expect_open: bool,
    timeout: float = 5.0,
    poll_interval: float = 0.2,
) -> bool:
    """Wait for a port to reach the desired open/closed state within timeout."""

    deadline = time.time() + timeout
    while time.time() < deadline:
        if is_port_open(host, port) is expect_open:
            return True
        time.sleep(poll_interval)
    return False
