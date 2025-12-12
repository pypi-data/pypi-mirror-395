from __future__ import annotations

import re


def flag_exists(flag: str, text: str) -> bool:
    """Return True if a line contains the marker '# filestate: <flag>'.

    Matches are performed per-line, allowing optional leading whitespace and
    flexible spacing around the colon. Example valid markers:
    - '# filestate: my-flag'
    - '    #   filestate:   my-flag   '
    The match is case-sensitive for the flag value.
    """
    pattern = rf"^[\t ]*#\s*filestate:\s*{re.escape(flag)}\b"
    return re.search(pattern, text, flags=re.MULTILINE) is not None
