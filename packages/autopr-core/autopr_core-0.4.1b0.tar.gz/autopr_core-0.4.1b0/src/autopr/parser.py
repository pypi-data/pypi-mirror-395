"""Diff and commit parser utilities for PR generation.

The parser extracts a lightweight, structured summary from unified diffs and
commit messages. It's intentionally conservative to keep unit tests deterministic.
"""
from __future__ import annotations

import re
from typing import Dict, List


def parse_diff(diff_text: str) -> Dict[str, object]:
    """Parse a unified diff or snippet and extract high level info.

    Returns a dict with keys:
      - files_changed: list of filenames mentioned in diff headers (if found)
      - added_lines: int
      - removed_lines: int
      - added_functions: list of detected function names in added lines
      - added_classes: list of detected class names in added lines
      - summary: short textual summary
    """
    files = []
    added = 0
    removed = 0
    added_code = []

    for line in diff_text.splitlines():
        # diff header line format: '+++ b/path/to/file' or '--- a/path'
        m = re.match(r'^(?:\+\+\+|---)\s+([ab]/)?(.+)$', line)
        if m:
            fname = m.group(2).strip()
            files.append(fname)
            continue

        if line.startswith('+') and not line.startswith('+++'):
            added += 1
            added_code.append(line[1:])
        elif line.startswith('-') and not line.startswith('---'):
            removed += 1

    # detect simple function/class patterns in added_code
    added_functions = []
    added_classes = []
    func_re = re.compile(r'^\s*def\s+([a-zA-Z0-9_]+)\s*\(')
    cls_re = re.compile(r'^\s*class\s+([A-Za-z0-9_]+)\s*\(?')
    for ln in added_code:
        fm = func_re.match(ln)
        if fm:
            added_functions.append(fm.group(1))
        cm = cls_re.match(ln)
        if cm:
            added_classes.append(cm.group(1))

    files_changed = list(dict.fromkeys(files))  # dedupe preserving order

    summary_parts = []
    if files_changed:
        summary_parts.append(f"{len(files_changed)} files changed: {', '.join(files_changed[:3])}{'...' if len(files_changed)>3 else ''}")
    if added_functions:
        summary_parts.append(f"added functions: {', '.join(added_functions[:3])}{'...' if len(added_functions)>3 else ''}")
    if added_classes:
        summary_parts.append(f"added classes: {', '.join(added_classes[:3])}{'...' if len(added_classes)>3 else ''}")

    summary = "; ".join(summary_parts) or "Small changes"

    return {
        "files_changed": files_changed,
        "added_lines": added,
        "removed_lines": removed,
        "added_functions": added_functions,
        "added_classes": added_classes,
        "summary": summary,
    }
