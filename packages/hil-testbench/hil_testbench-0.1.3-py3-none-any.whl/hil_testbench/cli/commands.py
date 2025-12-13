from __future__ import annotations

import os
import subprocess
import sys


def daemon_detach() -> None:
    """Detach process to run in background (platform aware)."""
    print("🚀 Starting daemon mode...")  # hil: allow-print
    print("   Logs will be written to logs/<timestamp>")  # hil: allow-print
    print(  # hil: allow-print
        "   Monitor with: python scripts/status.py logs/latest --watch"
    )
    print()  # hil: allow-print
    if sys.platform == "win32":
        args = [sys.executable] + [arg for arg in sys.argv if arg != "--daemon"]
        subprocess.Popen(
            args,
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
        )
        sys.exit(0)
    _detach_unix()


def _detach_unix() -> None:
    if sys.platform == "win32":
        raise RuntimeError("_detach_unix called on Windows platform")
    fork = getattr(os, "fork", None)
    setsid = getattr(os, "setsid", None)
    if fork is None or setsid is None:
        raise RuntimeError("fork/setsid unavailable on this platform")
    try:
        pid = fork()
        if pid > 0:
            sys.exit(0)
    except OSError as exc:
        print(f"Fork failed: {exc}", file=sys.stderr)  # hil: allow-print
        sys.exit(1)
    setsid()
    os.umask(0)
    sys.stdout.flush()
    sys.stderr.flush()
    devnull = os.open(os.devnull, os.O_RDWR)
    os.dup2(devnull, sys.stdin.fileno())
    os.dup2(devnull, sys.stdout.fileno())
    os.dup2(devnull, sys.stderr.fileno())
    os.close(devnull)
