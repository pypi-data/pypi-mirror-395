"""Helpers to parse coverage reports and compare before/after coverage.

For now this will parse a simple coverage summary string containing 'TOTAL' line
and a percentage (as produced by coverage.py html/text or pytest-cov summary).
"""
from __future__ import annotations

import re
from typing import Dict, Any


def parse_coverage_summary(text: str) -> Dict[str, Any]:
    """Extract coverage percentage from a coverage report text.

    Returns {'coverage_percent': float} if found, otherwise empty dict.
    Looks for lines like: 'TOTAL  ...  85%'
    """
    # find 'TOTAL' row percentage
    m = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", text)
    if m:
        return {"coverage_percent": float(m.group(1))}

    # fallback: any percent like '85%'
    m2 = re.search(r"(\d+)%", text)
    if m2:
        return {"coverage_percent": float(m2.group(1))}

    return {}


def compare_coverage(before_text: str, after_text: str) -> Dict[str, Any]:
    a = parse_coverage_summary(after_text)
    b = parse_coverage_summary(before_text)
    if "coverage_percent" in a and "coverage_percent" in b:
        delta = a["coverage_percent"] - b["coverage_percent"]
        return {"before": b["coverage_percent"], "after": a["coverage_percent"], "delta": delta}
    return {"before": b.get("coverage_percent"), "after": a.get("coverage_percent"), "delta": None}
