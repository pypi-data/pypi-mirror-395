"""Build an offline install bundle and optionally ship it to a remote host.

This module lives inside the package so it is included in PyPI artifacts.
It mirrors the functionality of the previous tools/build_and_ship_offline.sh helper.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tarfile
from pathlib import Path


def _run(cmd: list[str], *, cwd: str | None = None) -> None:
    """Run a command and raise if it fails."""
    subprocess.run(cmd, check=True, cwd=cwd)


def build_bundle(
    *,
    pkg: str,
    extras: str | None,
    bundle_dir: Path,
    tarball: Path,
    python_bin: str,
) -> None:
    """Download dependencies and build a wheel for the local project."""
    bundle_dir.mkdir(parents=True, exist_ok=True)
    extra_suffix = f"[{extras}]" if extras else ""

    # Download dependencies
    _run(
        [
            python_bin,
            "-m",
            "pip",
            "download",
            "--dest",
            str(bundle_dir),
            f"{pkg}{extra_suffix}",
        ]
    )

    # Build wheel for the local project
    _run(
        [
            python_bin,
            "-m",
            "pip",
            "wheel",
            "--no-deps",
            "--wheel-dir",
            str(bundle_dir),
            f".{extra_suffix}",
        ]
    )

    # Create tarball
    with tarfile.open(tarball, "w:gz") as tar:
        for item in bundle_dir.iterdir():
            tar.add(item, arcname=item.name)


def ship_bundle(
    *,
    tarball: Path,
    dest: str,
    dest_dir: str,
) -> None:
    """Copy the tarball to the remote host and extract it."""
    # Prepare remote directory
    _run(["ssh", dest, "mkdir", "-p", dest_dir])

    # Copy tarball
    _run(["scp", str(tarball), f"{dest}:{dest_dir}/"])

    # Extract
    remote_tar = f"{dest_dir}/{tarball.name}"
    _run(["ssh", dest, "tar", "-xzf", remote_tar, "-C", dest_dir])


def install_remote(
    *,
    dest: str,
    dest_dir: str,
    pkg: str,
    extras: str | None,
    remote_pip: str,
) -> None:
    """Install from the remote bundle without hitting PyPI."""
    extra_suffix = f"[{extras}]" if extras else ""
    cmd = f"{remote_pip} install --no-index --find-links='{dest_dir}' '{pkg}{extra_suffix}'"
    _run(["ssh", dest, cmd])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build offline bundle for hil-testbench and optionally ship/install remotely."
    )
    parser.add_argument("--dest", help="user@host for remote transfer (required to ship/install)")
    parser.add_argument(
        "--remote-install",
        action="store_true",
        help="Install on the remote host after transfer.",
    )
    parser.add_argument(
        "--pkg",
        default="hil-testbench",
        help="Package name to bundle (default: hil-testbench).",
    )
    parser.add_argument("--extras", help="Extras to include, e.g. dev")
    parser.add_argument(
        "--bundle-dir",
        default="offline_bundle",
        help="Local directory to store downloaded wheels.",
    )
    parser.add_argument(
        "--tarball",
        default="offline_bundle.tar.gz",
        help="Tarball name for the bundle.",
    )
    parser.add_argument(
        "--dest-dir",
        default="/tmp/offline_bundle",
        help="Remote directory to place the bundle.",
    )
    parser.add_argument(
        "--python-bin",
        default=shutil.which("python3") or "python3",
        help="Local Python executable to use.",
    )
    parser.add_argument(
        "--remote-pip",
        default="python3 -m pip",
        help="Remote pip command to use for installation.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    bundle_dir = Path(args.bundle_dir).resolve()
    tarball = Path(args.tarball).resolve()

    build_bundle(
        pkg=args.pkg,
        extras=args.extras,
        bundle_dir=bundle_dir,
        tarball=tarball,
        python_bin=args.python_bin,
    )

    if args.dest:
        ship_bundle(tarball=tarball, dest=args.dest, dest_dir=args.dest_dir)
        if args.remote_install:
            install_remote(
                dest=args.dest,
                dest_dir=args.dest_dir,
                pkg=args.pkg,
                extras=args.extras,
                remote_pip=args.remote_pip,
            )


if __name__ == "__main__":
    main()
