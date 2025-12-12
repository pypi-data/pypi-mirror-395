"""Lightweight AST-based static analysis for Python diffs.

This module provides a small set of deterministic checks that are fast to run
and helpful when reviewing diffs:

- TODO comments detected in added lines
- print(...) calls (likely debug prints)
- unused imports (imports that are never referenced)
- comparisons to None using ==/!= (prefer `is`/`is not`)
- functions using risky APIs (open, requests, subprocess) without try/except

The analyzer is intentionally conservative and returns structured "findings" so
they can be merged with LLM results in the review API.
"""
from __future__ import annotations

import ast
from typing import List, Dict, Any


def _extract_added_lines(diff: str) -> str:
    # If input looks like a unified diff, gather lines that start with '+' (not '+++')
    if '\n+' in diff:
        lines = []
        for ln in diff.splitlines():
            if ln.startswith('+') and not ln.startswith('+++'):
                # strip leading +
                lines.append(ln[1:])
        return '\n'.join(lines)
    return diff


def analyze_python_code(code: str) -> List[Dict[str, Any]]:
    """Analyze a python code snippet and return findings.

    code may be a whole file or a diff; the analyzer will use only the added lines
    if it detects a diff-like format.
    """
    text = _extract_added_lines(code)
    findings: List[Dict[str, Any]] = []

    # Quick textual checks for TODOs and debug prints
    for i, ln in enumerate(text.splitlines(), start=1):
        if 'TODO' in ln:
            findings.append({"type": "todo", "message": "TODO found in added code", "line": i, "severity": "low"})

    # Parse AST for deeper checks
    try:
        tree = ast.parse(text)
    except SyntaxError:
        # If parsing fails (partial snippets), return textual findings already found
        return findings

    # Collect import names
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.asname or alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imported.add(alias.asname or alias.name)

    # Collect used names
    used = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used.add(node.id)

    # unused imports
    for name in imported:
        if name not in used:
            findings.append({"type": "unused_import", "message": f"Imported `{name}` is not used", "severity": "low"})

    # find print calls
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'print':
            findings.append({"type": "debug_print", "message": "Found print() call — remove debug prints before merging", "line": getattr(node, 'lineno', None), "severity": "low"})

    # comparisons to None using ==/!=
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            for comparator in node.comparators:
                if isinstance(comparator, ast.Constant) and comparator.value is None:
                    # operator list can contain ast.Eq/NotEq
                    for op in node.ops:
                        if isinstance(op, (ast.Eq, ast.NotEq)):
                            findings.append({
                                "type": "none_equality_comparison",
                                "message": "Use `is`/`is not` when comparing to None",
                                "line": getattr(node, 'lineno', None),
                                "severity": "low",
                            })

    # detect risky API use inside functions without try/except
    risky_names = {"open", "requests", "subprocess", "socket"}

    class FuncVisitor(ast.NodeVisitor):
        def __init__(self):
            self.findings = []

        def visit_FunctionDef(self, node: ast.FunctionDef):
            # search for risky calls
            risky_calls = []
            has_try = False

            for child in ast.walk(node):
                if isinstance(child, ast.Try):
                    has_try = True
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Name) and child.func.id in risky_names:
                        risky_calls.append((child.func.id, getattr(child, 'lineno', None)))
                    if isinstance(child.func, ast.Attribute) and isinstance(child.func.value, ast.Name) and child.func.value.id in risky_names:
                        risky_calls.append((ast.unparse(child.func), getattr(child, 'lineno', None)))

            if risky_calls and not has_try:
                for name, lineno in risky_calls:
                    self.findings.append({
                        "type": "missing_error_handling",
                        "message": f"Function uses {name} without try/except — consider handling potential errors",
                        "line": lineno,
                        "severity": "medium",
                    })

    fv = FuncVisitor()
    fv.visit(tree)
    findings.extend(fv.findings)

    return findings


def analyze_diff(diff_text: str, language: str = "python") -> List[Dict[str, Any]]:
    """Dispatch to language-specific analyzers.

    For now, only Python is implemented. The function accepts the diff content and
    returns a list of findings.
    """
    if language.lower() != "python":
        return []
    return analyze_python_code(diff_text)
