"""Parse CI and test logs and produce a concise summary.

This parser focuses on pytest output (the textual summary) and extracts
counts of passed, failed, and errored tests, plus captured failure snippets.
"""
from __future__ import annotations

import re
from typing import Dict, Any, List


def parse_pytest_output(log: str) -> Dict[str, Any]:
    """Parse pytest textual output into a structured summary.

    Returns a dict with keys:
      - total: int
      - passed: int
      - failed: int
      - errors: int
      - skipped: int
      - failures: list of dict {name, message}
    """
    res = {"total": 0, "passed": 0, "failed": 0, "errors": 0, "skipped": 0, "failures": []}

    # Quick patterns
    summary_re = re.compile(r"=+\s+([0-9]+) passed,?\s*([0-9]+)? failed,?\s*([0-9]+)? errors?,?\s*([0-9]+)? skipped,?.*=+")
    # The above might not always match, so also hunt for tokens
    t_passed = re.search(r"([0-9]+) passed", log)
    t_failed = re.search(r"([0-9]+) failed", log)
    t_errors = re.search(r"([0-9]+) errors?", log)
    t_skipped = re.search(r"([0-9]+) skipped", log)

    if t_passed:
        res["passed"] = int(t_passed.group(1))
    if t_failed:
        res["failed"] = int(t_failed.group(1))
    if t_errors:
        res["errors"] = int(t_errors.group(1))
    if t_skipped:
        res["skipped"] = int(t_skipped.group(1))

    res["total"] = res["passed"] + res["failed"] + res["errors"] + res["skipped"]

    # Extract failure blocks - look for the 'FAILURES' section
    if "FAILURES" in log:
        lines = log.splitlines()
        try:
            start = next(i for i, l in enumerate(lines) if "FAILURES" in l)
        except StopIteration:
            start = 0

        # scan from start for header lines that mark a test failure (lines of underscores + test name)
        i = start
        current = None
        while i < len(lines):
            ln = lines[i].rstrip()
            # match lines like: '____ test_name ____'
            m = re.match(r"_{2,}\s*(?P<name>test[\w\-\[\]:.]+)\s*_{2,}", ln)
            if m:
                # start a new failure capture
                name = m.group('name')
                # gather message lines until next separator or blank
                j = i + 1
                message_lines = []
                while j < len(lines) and lines[j].strip() and not lines[j].startswith('=') and not re.match(r"_{2,}", lines[j]):
                    message_lines.append(lines[j].strip())
                    j += 1
                res["failures"].append({"name": name, "message": " ".join(message_lines)})
                i = j
                continue
            i += 1

    else:
        # fallback: find simple 'FAILED name - message' patterns
        for line in log.splitlines():
            m = re.match(r"FAILED\s+([^\s:]+).*?-\s*(.*)$", line)
            if m:
                res["failures"].append({"name": m.group(1), "message": m.group(2)})

    return res
