from __future__ import annotations

from typing import Dict, Any, List

from .llm import llm
from . import analysis, lint, validators
from . import ci_parser, coverage_utils, issue_validator


def review_pr(diff: str, commits: list[str] | None = None, issue_text: str | None = None, test_log: str | None = None, coverage_before: str | None = None, coverage_after: str | None = None) -> Dict[str, Any]:
    # LLM review (may return dict or raw)
    raw = llm.review_code(diff)
    if isinstance(raw, dict):
        review = raw
    else:
        # try to coerce
        try:
            review = {"summary": str(raw), "findings": [], "confidence": 0.0}
        except Exception:
            review = {"summary": "", "findings": [], "confidence": 0.0}

    # deterministic static analysis
    static_findings = analysis.analyze_diff(diff, language="python")
    # lint findings
    lint_findings = lint.run_basic_lint(diff)

    findings: List[Dict[str, Any]] = []
    for f in review.get("findings", []):
        # already expected shape or massage
        findings.append({"type": f.get("type", "ai"), "message": f.get("message", str(f)), "severity": f.get("severity") if isinstance(f, dict) else None})

    # add static & lint findings
    for sf in static_findings:
        findings.append({"type": sf.get("type", "static"), "message": sf.get("message", ""), "severity": sf.get("severity")})
    for lf in lint_findings:
        findings.append({"type": lf.get("type", "lint"), "message": lf.get("message", ""), "severity": lf.get("severity")})

    # parse test output if provided
    test_summary = None
    if test_log:
        test_summary = ci_parser.parse_pytest_output(test_log)

    # compare coverage if both texts provided
    coverage_summary = None
    if coverage_before is not None and coverage_after is not None:
        coverage_summary = coverage_utils.compare_coverage(coverage_before, coverage_after)

    # evaluate issue alignment heuristics when issue_text or commits provided
    issue_alignment = None
    if issue_text and commits:
        issue_alignment = issue_validator.simple_issue_alignment(issue_text, diff, commits)

    # lint findings
    conf = float(review.get("confidence", 0.0)) if isinstance(review.get("confidence", 0.0), (int, float)) else 0.0

    out = {"summary": review.get("summary", ""), "findings": findings, "confidence": conf}

    # validate shape, attach validation info
    val = validators.validate_review_output(out)
    out["_validation"] = val
    if test_summary is not None:
        out["_tests"] = test_summary
    if coverage_summary is not None:
        out["_coverage"] = coverage_summary
    if issue_alignment is not None:
        out["_issue_alignment"] = issue_alignment
    return out
