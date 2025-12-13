"""CLI handler for --prune-logs command."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from datetime import datetime, timedelta
from typing import Any

from hil_testbench.config.run_config import RunConfig


def handle_prune_logs(args: argparse.Namespace, run_config: RunConfig) -> None:
    """Handle --prune-logs command.

    Modes:
        auto: Prune directories exceeding limits (default)
        dry-run: Show what would be pruned without deleting
        force: Prune without prompting
    """
    if args.prune_logs is None:
        return

    mode = args.prune_logs
    log_dir = os.path.abspath(run_config.log_dir)

    dirs_info = _load_log_directories(log_dir)
    to_prune = _select_directories_to_prune(dirs_info, run_config)

    if not to_prune:
        _exit_no_prune(dirs_info, run_config)

    planned_size_mb = _calc_size_mb(to_prune)
    _print_summary(log_dir, dirs_info, to_prune, planned_size_mb)

    if mode == "dry-run":
        _print_dry_run(to_prune)
        sys.exit(0)

    prunable_dirs, protected_count = _filter_protected_directories(to_prune)
    if protected_count:
        print(  # hil: allow-print
            f"Note: {protected_count} directories protected (have active processes)"
        )

    if not prunable_dirs:
        _exit_with_message("All prunable directories are protected.")

    if mode != "force":
        _confirm_deletion(len(prunable_dirs))

    deleted, failed = _delete_directories(prunable_dirs)
    freed_mb = _calc_size_mb(prunable_dirs)
    _print_completion(deleted, failed, freed_mb)
    sys.exit(0)


def _calc_size_mb(entries: list[dict[str, Any]]) -> float:
    total_size = sum(entry["size"] for entry in entries)
    return total_size / (1024 * 1024) if entries else 0.0


def _load_log_directories(log_dir: str) -> list[dict[str, Any]]:
    if not os.path.exists(log_dir):
        _exit_with_message(f"Log directory does not exist: {log_dir}")

    dirs_info = _scan_log_directories(log_dir)
    if not dirs_info:
        _exit_with_message("No log directories found.")
    return dirs_info


def _exit_with_message(message: str) -> None:
    print(message)  # hil: allow-print
    sys.exit(0)


def _exit_no_prune(dirs_info: list[dict[str, Any]], run_config: RunConfig) -> None:
    print(  # hil: allow-print
        f"No directories to prune. "
        f"({len(dirs_info)} directories, "
        f"limit: {run_config.max_log_dirs} dirs, {run_config.max_log_age_days} days)"
    )
    sys.exit(0)


def _print_summary(
    log_dir: str,
    dirs_info: list[dict[str, Any]],
    to_prune: list[dict[str, Any]],
    size_mb: float,
) -> None:
    print("\n📁 Log Directory Cleanup")  # hil: allow-print
    print(f"   Directory: {log_dir}")  # hil: allow-print
    print(f"   Total directories: {len(dirs_info)}")  # hil: allow-print
    print(f"   To be pruned: {len(to_prune)}")  # hil: allow-print
    print(f"   Space to free: {size_mb:.1f} MB")  # hil: allow-print
    print()  # hil: allow-print


def _print_dry_run(entries: list[dict[str, Any]]) -> None:
    print("Directories that would be pruned:")  # hil: allow-print
    for entry in entries:
        age_days = (datetime.now() - entry["mtime"]).days
        protected = "🔒 PROTECTED" if entry["protected"] else ""
        print(  # hil: allow-print
            f"  {entry['name']:<30} {entry['size'] / 1024:.0f} KB  {age_days} days old  {protected}"
        )
    print("\n(dry-run mode - no directories deleted)")  # hil: allow-print


def _filter_protected_directories(
    entries: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int]:
    prunable = [entry for entry in entries if not entry["protected"]]
    protected_count = len(entries) - len(prunable)
    return prunable, protected_count


def _confirm_deletion(count: int) -> None:
    response = input(f"Delete {count} directories? [y/N]: ").strip().lower()
    if response != "y":
        _exit_with_message("Cancelled.")


def _delete_directories(entries: list[dict[str, Any]]) -> tuple[int, int]:
    deleted = 0
    failed = 0
    for entry in entries:
        try:
            shutil.rmtree(entry["path"])
            deleted += 1
            print(f"  ✓ Deleted: {entry['name']}")  # hil: allow-print
        except OSError as exc:
            failed += 1
            print(f"  ✗ Failed: {entry['name']} - {exc}")  # hil: allow-print
    return deleted, failed


def _print_completion(deleted: int, failed: int, size_mb: float) -> None:
    print()  # hil: allow-print
    print(  # hil: allow-print
        f"Cleanup complete: {deleted} deleted, {failed} failed, {size_mb:.1f} MB freed"
    )


def _scan_log_directories(log_dir: str) -> list[dict[str, Any]]:
    """Scan log directory and return info about each execution directory."""
    try:
        entries = os.listdir(log_dir)
    except OSError:
        return []

    dirs_info: list[dict[str, Any]] = []
    for entry in entries:
        info = _build_directory_info(log_dir, entry)
        if info:
            dirs_info.append(info)

    dirs_info.sort(key=lambda info: info["mtime"], reverse=True)
    return dirs_info


def _build_directory_info(log_dir: str, entry: str) -> dict[str, Any] | None:
    if entry in ("latest-run", "latest-run.tmp"):
        return None

    dir_path = os.path.join(log_dir, entry)
    if not os.path.isdir(dir_path):
        return None

    try:
        stat = os.stat(dir_path)
    except OSError:
        return None

    try:
        size = _directory_size(dir_path)
    except OSError:
        return None

    protected = _is_protected(dir_path)

    return {
        "name": entry,
        "path": dir_path,
        "ctime": datetime.fromtimestamp(stat.st_ctime),
        "mtime": datetime.fromtimestamp(stat.st_mtime),
        "size": size,
        "protected": protected,
    }


def _directory_size(dir_path: str) -> int:
    total_size = 0
    for dirpath, _dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(file_path)
            except OSError:
                continue
    return total_size


def _select_directories_to_prune(dirs_info: list[dict], run_config: RunConfig) -> list[dict]:
    """Select directories to prune based on count and age limits."""
    to_prune: set[str] = set()

    # Apply count-based selection
    if run_config.max_log_dirs > 0 and len(dirs_info) > run_config.max_log_dirs:
        excess = dirs_info[run_config.max_log_dirs :]
        to_prune.update(d["path"] for d in excess)

    # Apply age-based selection (use mtime for consistent cross-platform behavior)
    if run_config.max_log_age_days > 0:
        cutoff = datetime.now() - timedelta(days=run_config.max_log_age_days)
        for d in dirs_info:
            if d["mtime"] < cutoff:
                to_prune.add(d["path"])

    return [d for d in dirs_info if d["path"] in to_prune]


def _is_protected(dir_path: str) -> bool:
    """Return True when the log directory shows in-use markers."""

    reuse_lock = os.path.join(dir_path, ".hil_reuse.lock")
    return os.path.exists(reuse_lock)


__all__ = ["handle_prune_logs"]
