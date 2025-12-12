"""Centralized constants for filestate inline markers used in TOML comments.

These markers allow protecting items from automated modifications, e.g. in
pyproject.toml dependency arrays.

Usage example in TOML (tomlkit preserves inline comments):

[project]
dependencies = [
  "pytest",  # filestate: keep
]
"""

from __future__ import annotations

# Base tag that must appear in the inline comment to be considered by filestate tooling
FILESTATE_TAG: str = "filestate:"

# Known actions
# filestate: python-constant-sort
FILESTATE_IGNORE: str = "ignore"
FILESTATE_KEEP: str = "keep"

# Convenience collection of recognized actions
FILESTATE_ACTIONS: tuple[str, ...] = (FILESTATE_KEEP, FILESTATE_IGNORE)
