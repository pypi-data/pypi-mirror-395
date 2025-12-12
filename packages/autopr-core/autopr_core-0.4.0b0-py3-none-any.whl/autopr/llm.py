import os
from typing import Dict, Any

from .providers import OpenAIProvider, AnthropicProvider, StubProvider


def _choose_provider() -> Any:
    provider = os.getenv("AUTOPR_PROVIDER", "stub").lower()
    if provider == "openai":
        try:
            return OpenAIProvider()
        except Exception:
            # fallback to stub if library missing or misconfigured
            return StubProvider()
    if provider == "anthropic":
        try:
            return AnthropicProvider()
        except Exception:
            return StubProvider()

    return StubProvider()


llm = _choose_provider()
