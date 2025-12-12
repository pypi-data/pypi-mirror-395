"""Simple linting fallback and small checks for diffs/snippets.

This module tries to provide quick deterministic lint-like findings without
relying on external tools. If a real linter (e.g. ruff) is installed and on
PATH, we can extend to call it; for now we provide conservative, fast checks.
"""
from __future__ import annotations

from typing import List, Dict, Any


def run_basic_lint(code: str) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []

    for i, ln in enumerate(code.splitlines(), start=1):
        if len(ln) > 120:
            findings.append({"type": "long_line", "message": "Line exceeds 120 characters", "line": i, "severity": "low"})
        if ln.endswith(" "):
            findings.append({"type": "trailing_whitespace", "message": "Trailing whitespace", "line": i, "severity": "low"})
        if "import *" in ln:
            findings.append({"type": "wildcard_import", "message": "Wildcard import found; avoid using import *", "line": i, "severity": "medium"})

    # detect obvious 'eval(' calls
    if "eval(" in code:
        findings.append({"type": "unsafe_eval", "message": "Use of eval() detected; this can be dangerous", "severity": "high"})

    return findings
