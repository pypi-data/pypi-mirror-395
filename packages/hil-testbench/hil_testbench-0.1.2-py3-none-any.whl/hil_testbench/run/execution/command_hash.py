from __future__ import annotations

"""Utilities for generating stable command hashes."""

import hashlib


def short_command_hash(command: str, *, length: int = 12) -> str:
    """Return a short, deterministic identifier for a shell command."""

    digest = hashlib.blake2s(command.encode("utf-8"), digest_size=16).hexdigest()
    return digest[:length]
