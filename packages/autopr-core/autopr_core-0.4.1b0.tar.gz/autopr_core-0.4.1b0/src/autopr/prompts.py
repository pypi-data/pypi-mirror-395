"""Prompt templates used by AutoPR LLM adapters.

Templates are intentionally small and designed to be deterministic — they ask
the LLM to return JSON where appropriate so parsing is predictable.
"""

TITLE_PROMPT = (
    "You are an assistant that writes concise PR titles. Given a code diff and commit messages, produce a one-line title (max 60 characters).\n"
    "Diff:\n{diff}\n\nCommit messages:\n{commits}\n\nIssue: {issue}\n\n"
    "Return only the title text with no explanation."
)

PR_DESCRIPTION_PROMPT = (
    "You are an assistant that writes a detailed PR description as JSON. Given a code diff, commits, and an optional issue, return a JSON object with the following keys: title, what_changed, why, files_impacted (array), tests (string), risk_level (low/medium/high), rollback_plan.\n\n"
    "Diff:\n{diff}\n\nCommits:\n{commits}\n\nIssue: {issue}\n\n"
    "Provide only valid JSON (no surrounding markdown).")

REVIEW_PROMPT = (
    "You are an automated code reviewer. Given a code diff, return a JSON object describing: summary, findings (array of objects with keys: type, message, severity), and confidence (0.0-1.0).\n\n"
    "Diff:\n{diff}\n\nReturn only valid JSON."
)
