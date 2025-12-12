from __future__ import annotations

from typing import Any, Dict


def validate_generate_output(result: Dict[str, Any]) -> Dict[str, Any]:
    """Very small validation & normalization for generated PR descriptions.

    Ensures expected keys exist and types are reasonable, returns a dict with
    "valid": bool and optional "errors"/"warnings".
    """
    expected = {
        "title": str,
        "what_changed": str,
        "why": str,
        "files_impacted": list,
        "tests": str,
        "risk_level": str,
        "rollback_plan": str,
    }

    errors = []
    warnings = []

    for k, t in expected.items():
        if k not in result:
            errors.append(f"Missing key: {k}")
        else:
            if not isinstance(result[k], t):
                warnings.append(f"Key {k} expected type {t.__name__}, got {type(result[k]).__name__}")

    # title length check
    title = result.get("title", "")
    if isinstance(title, str) and len(title) > 80:
        warnings.append("Title longer than 80 chars")

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}


def validate_review_output(result: Dict[str, Any]) -> Dict[str, Any]:
    expected = {"summary": str, "findings": list, "confidence": (float, int)}
    errors = []
    warnings = []

    for k, t in expected.items():
        if k not in result:
            errors.append(f"Missing key: {k}")
        else:
            if not isinstance(result[k], t):
                warnings.append(f"Key {k} expected type {t}, got {type(result[k])}")

    conf = result.get("confidence", 0.0)
    try:
        c = float(conf)
        if c < 0.0 or c > 1.0:
            warnings.append("confidence outside 0.0-1.0 range")
    except Exception:
        warnings.append("confidence not a float")

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}
