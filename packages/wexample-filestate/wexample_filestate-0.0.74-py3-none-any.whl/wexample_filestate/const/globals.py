from __future__ import annotations

# filestate: python-constant-sort
NAME_PATTERN_ANY_ITEM = "^(?!\\.\\.$)(?!^\\.$).+$"  # Ignore . and ..
NAME_PATTERN_NO_LEADING_DOT = "^(?!\\.).+$"  # Ignore every name starting with a dot
