from __future__ import annotations

import argparse
import pathlib
import sys
from datetime import datetime


def handle_shutdown(args: argparse.Namespace) -> None:
    session_arg = args.shutdown
    if session_arg is None:
        return
    _shutdown_specific(session_arg)


def _shutdown_specific(path_str: str) -> None:
    session_dir = pathlib.Path(path_str)
    if not session_dir.exists():
        print(  # hil: allow-print
            f"Error: Session directory not found: {path_str}", file=sys.stderr
        )
        sys.exit(1)
    _emit_shutdown(session_dir)


def _emit_shutdown(session_dir: pathlib.Path, announce: bool = False) -> None:
    shutdown_file = session_dir / "shutdown.signal"
    with open(shutdown_file, "w", encoding="utf-8") as handle:
        handle.write(f"Shutdown requested at {datetime.now().isoformat()}\n")
    print(f"Shutdown signal sent to {session_dir}")  # hil: allow-print
    print(  # hil: allow-print
        "The daemon will gracefully shutdown immediately (KeyboardInterrupt)."
    )
    sys.exit(0)
