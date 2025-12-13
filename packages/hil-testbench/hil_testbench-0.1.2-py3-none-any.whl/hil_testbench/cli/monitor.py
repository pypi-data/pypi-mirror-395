from __future__ import annotations

import argparse
import subprocess
import sys


def handle_monitor(args: argparse.Namespace) -> None:
    if not args.monitor:
        return
    print("Launching status monitor for latest session...")  # hil: allow-print
    subprocess.run(["python", "scripts/status.py", "logs/latest", "--watch"], check=False)
    sys.exit(0)
