from __future__ import annotations

import json
from typing import Any, Dict, List

from .parser import parse_diff
from . import prompts
from .llm import llm


def _ensure_dict(obj: Any) -> Dict[str, Any]:
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, str):
        try:
            return json.loads(obj)
        except Exception:
            return {"raw": obj}
    return {"raw": str(obj)}


def generate_pr_from(diff: str, commits: List[str], issue: str | None = None) -> Dict[str, Any]:
    """Generate a structured PR description.

    Steps:
      - parse diff into short structured context
      - render a tighter prompt using context
      - call the configured llm provider
      - ensure the result is a dict and contains expected keys
    """
    context = parse_diff(diff)

    prompt = (
        prompts.PR_DESCRIPTION_PROMPT
        + "\nContext Summary:\n{summary}\nFiles changed:\n{files}\nAdded functions:\n{funcs}\nAdded classes:\n{classes}\n"
    ).format(
        diff=diff,
        commits="\n".join(commits),
        issue=issue or "",
        summary=context.get("summary", ""),
        files=", ".join(context.get("files_changed", [])),
        funcs=", ".join(context.get("added_functions", [])),
        classes=", ".join(context.get("added_classes", [])),
    )

    # call provider
    raw = llm.generate_pr_description(diff, commits, issue)
    result = _ensure_dict(raw)

    # normalize expected keys (best-effort)
    keys = ["title", "what_changed", "why", "files_impacted", "tests", "risk_level", "rollback_plan"]
    normalized = {k: result.get(k, "") if k != "files_impacted" else result.get(k, []) for k in keys}

    # If result is empty or only raw, try to call LLM by sending the prompt string directly
    if not any(normalized.values()) or (len(normalized.get("title", "")) == 0 and isinstance(result.get("raw"), str)):
        # fallback: ask LLM with prompt
        resp = llm._chat(prompt) if hasattr(llm, "_chat") else None
        if resp:
            parsed = _ensure_dict(resp)
            for k in keys:
                if not normalized.get(k):
                    normalized[k] = parsed.get(k, normalized[k]) if isinstance(parsed, dict) else normalized[k]

    # Attach parser context metadata
    normalized["_context"] = context
    return normalized
