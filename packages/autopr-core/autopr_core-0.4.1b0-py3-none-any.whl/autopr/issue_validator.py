"""Validate whether a PR/branch likely resolves a linked issue.

This module provides a heuristic validator that checks for overlap between
issue text and the PR diff/commits. For more advanced checks, a provider-backed
LLM can be used (not mandatory) to score alignment.
"""
from __future__ import annotations

import re
from typing import Dict, Any, List


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[A-Za-z0-9_]+", (text or "").lower())


def simple_issue_alignment(issue_text: str, diff: str, commits: List[str]) -> Dict[str, Any]:
    """Return a heuristic alignment score between issue and diff/commits.

    Steps:
      - tokenize issue, diff, commits
      - compute intersection size / union size (Jaccard-like)
      - return score (0.0-1.0) and matched tokens
    """
    issue_tokens = set(_tokenize(issue_text))
    diff_tokens = set(_tokenize(diff))
    commits_tokens = set()
    for c in commits:
        commits_tokens.update(_tokenize(c))

    combined = diff_tokens.union(commits_tokens)
    if not issue_tokens or not combined:
        return {"score": 0.0, "matched": []}

    matched = list(issue_tokens.intersection(combined))
    score = len(matched) / max(1, len(issue_tokens.union(combined)))
    return {"score": float(score), "matched": matched}
