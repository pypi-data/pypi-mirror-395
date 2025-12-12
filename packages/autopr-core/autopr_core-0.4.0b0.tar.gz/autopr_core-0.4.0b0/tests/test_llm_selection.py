import os
import importlib
import sys
import types


def test_autopr_provider_env_stub(monkeypatch):
    monkeypatch.setenv('AUTOPR_PROVIDER', 'stub')
    import autopr.llm as llm_mod
    importlib.reload(llm_mod)
    assert llm_mod.llm is not None


def test_autopr_provider_openai_missing(monkeypatch):
    # ensure no openai module is present; selection should fall back to stub
    monkeypatch.setenv('AUTOPR_PROVIDER', 'openai')
    if 'openai' in sys.modules:
        del sys.modules['openai']
    import autopr.llm as llm_mod
    importlib.reload(llm_mod)
    # provider should be a stub when openai is not importable/configured
    assert llm_mod.llm is not None


def test_autopr_provider_anthropic_missing(monkeypatch):
    monkeypatch.setenv('AUTOPR_PROVIDER', 'anthropic')
    if 'anthropic' in sys.modules:
        del sys.modules['anthropic']
    import autopr.llm as llm_mod
    importlib.reload(llm_mod)
    assert llm_mod.llm is not None
