import os
import json
from typing import Any, Dict

from . import prompts


class BaseProvider:
    """Abstract provider that concrete adapters should implement."""

    def generate_pr_title(self, diff: str, commits: list[str], issue: str | None) -> str:
        raise NotImplementedError()

    def generate_pr_description(self, diff: str, commits: list[str], issue: str | None) -> Dict[str, Any]:
        raise NotImplementedError()

    def review_code(self, diff: str) -> Dict[str, Any]:
        raise NotImplementedError()


class OpenAIProvider(BaseProvider):
    def __init__(self, api_key: str | None = None, model: str | None = None):
        # lazy import so module import doesn't fail in tests without package
        import openai

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found")

        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o")

    def _chat(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {e}")

    def generate_pr_title(self, diff: str, commits: list[str], issue: str | None) -> str:
        prompt = prompts.TITLE_PROMPT.format(diff=diff, commits="\n".join(commits), issue=issue or "")
        return self._chat(prompt).strip()

    def generate_pr_description(self, diff: str, commits: list[str], issue: str | None) -> Dict[str, Any]:
        prompt = prompts.PR_DESCRIPTION_PROMPT.format(diff=diff, commits="\n".join(commits), issue=issue or "")
        text = self._chat(prompt)
        try:
            return json.loads(text)
        except Exception:
            return {"raw": text}

    def review_code(self, diff: str) -> Dict[str, Any]:
        prompt = prompts.REVIEW_PROMPT.format(diff=diff)
        text = self._chat(prompt)
        try:
            return json.loads(text)
        except Exception:
            return {"raw": text}


class AnthropicProvider(BaseProvider):
    def __init__(self, api_key: str | None = None, model: str | None = None):
        # lazy import
        import anthropic

        self._anthropic = anthropic
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Client(api_key=api_key) if api_key else None
        self.model = model or os.getenv("ANTHROPIC_MODEL", "claude-2")

    def _chat(self, prompt: str) -> str:
        # anthopic clients vary across versions; support a couple of shapes
        if self.client is None:
            raise RuntimeError("Anthropic client is not configured (missing ANTHROPIC_API_KEY)")

        # Try a chat-like method
        if hasattr(self.client, "create_chat_completion"):
            resp = self.client.create_chat_completion(model=self.model, messages=[{"role": "user", "content": prompt}])
            # try to extract content
            if hasattr(resp, "content"):
                return resp.content
            return resp["completion"] if isinstance(resp, dict) and "completion" in resp else str(resp)

        # fallback to classic complete/complete method
        if hasattr(self.client, "complete"):
            resp = self.client.complete(prompt=prompt, model=self.model, max_tokens=800)
            if hasattr(resp, "completion"):
                return resp.completion
            return resp["completion"] if isinstance(resp, dict) and "completion" in resp else str(resp)

        # final fallback: attempt to call .create
        if hasattr(self.client, "create"):
            resp = self.client.create(model=self.model, prompt=prompt)
            # resp might be a dict
            if isinstance(resp, dict) and "completion" in resp:
                return resp["completion"]
            return str(resp)

        raise RuntimeError("Unsupported Anthropic client interface")

    def generate_pr_title(self, diff: str, commits: list[str], issue: str | None) -> str:
        prompt = prompts.TITLE_PROMPT.format(diff=diff, commits="\n".join(commits), issue=issue or "")
        return self._chat(prompt).strip()

    def generate_pr_description(self, diff: str, commits: list[str], issue: str | None) -> Dict[str, Any]:
        prompt = prompts.PR_DESCRIPTION_PROMPT.format(diff=diff, commits="\n".join(commits), issue=issue or "")
        text = self._chat(prompt)
        try:
            return json.loads(text)
        except Exception:
            return {"raw": text}

    def review_code(self, diff: str) -> Dict[str, Any]:
        prompt = prompts.REVIEW_PROMPT.format(diff=diff)
        text = self._chat(prompt)
        try:
            return json.loads(text)
        except Exception:
            return {"raw": text}


class StubProvider(BaseProvider):
    """Very small stub provider retained for offline usage and tests.

    Kept for backwards compatibility with the existing llm.LLMStub.
    """

    def generate_pr_title(self, diff: str, commits: list[str], issue: str | None) -> str:
        return f"[AUTO] Update based on commits ({', '.join(commits)})"

    def generate_pr_description(self, diff: str, commits: list[str], issue: str | None) -> Dict[str, Any]:
        return {
            "title": self.generate_pr_title(diff, commits, issue),
            "what_changed": f"Summary from diff snippet: {diff[:200]}",
            "why": "Auto-generated reason extracted from commits.",
            "files_impacted": ["file1.py", "file2.py"],
            "tests": "Unit tests added/updated",
            "risk_level": "low",
            "rollback_plan": "Revert commit if necessary",
        }

    def review_code(self, diff: str) -> Dict[str, Any]:
        findings = []
        if "TODO" in diff:
            findings.append({"type": "todo", "message": "Found TODOs in changes", "severity": "low"})
        if "print(" in diff:
            findings.append({"type": "debug", "message": "Possible debug prints detected", "severity": "low"})

        return {"summary": "Minimal automated review", "findings": findings, "confidence": 0.65}
