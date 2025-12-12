import sys
import json
import types


def _make_fake_openai_module(response_text_for_first_call, response_text_for_second_call=None):
    fake = types.SimpleNamespace()

    class ChatChoiceMessage:
        def __init__(self, content):
            self.content = content

    class ChatChoice:
        def __init__(self, content):
            self.message = ChatChoiceMessage(content)

    class ChatCompletion:
        call_count = 0

        @staticmethod
        def create(model, messages, temperature):
            ChatCompletion.call_count += 1
            # first call returns first response, second call second
            if ChatCompletion.call_count == 1:
                txt = response_text_for_first_call
            else:
                txt = response_text_for_second_call or response_text_for_first_call
            return types.SimpleNamespace(choices=[ChatChoice(txt)])

    fake.ChatCompletion = ChatCompletion
    fake.Completion = types.SimpleNamespace(create=lambda **kwargs: types.SimpleNamespace(choices=[ChatChoice(response_text_for_first_call)]))
    return fake


def test_openai_provider_title_and_description(monkeypatch):
    # create a fake openai that returns a simple result for title then a JSON blob for description
    title_text = "Fix: helper edgecases"
    desc_json = json.dumps({
        "title": "Fix: helper edgecases",
        "what_changed": "Updated helper to handle None",
        "why": "Bug fix",
        "files_impacted": ["autopr/llm.py"],
        "tests": "Added unit tests",
        "risk_level": "low",
        "rollback_plan": "Revert commit"
    })

    fake = _make_fake_openai_module(title_text, desc_json)
    monkeypatch.setitem(sys.modules, "openai", fake)

    from autopr.providers import OpenAIProvider

    p = OpenAIProvider(api_key="fake", model="fake-model")
    title = p.generate_pr_title("+ added line", ["feat: add"], "#1")
    assert title == title_text

    desc = p.generate_pr_description("+ added line", ["feat: add"], "#1")
    assert isinstance(desc, dict)
    assert desc.get("title") == title_text


def test_openai_provider_review_parses_json(monkeypatch):
    review_json = json.dumps({"summary": "ok", "findings": [], "confidence": 0.8})
    fake = _make_fake_openai_module(review_json)
    monkeypatch.setitem(sys.modules, "openai", fake)

    from autopr.providers import OpenAIProvider

    p = OpenAIProvider(api_key="fake")
    r = p.review_code("print('x')\n# TODO")
    assert isinstance(r, dict)
    assert r.get("summary") == "ok"


def test_anthropic_provider_title_and_description(monkeypatch):
    # create fake anthropic module with Client that has a create method returning dict
    mod = types.SimpleNamespace()

    class FakeClient:
        def __init__(self, api_key=None):
            self.api_key = api_key

        def create(self, model, prompt):
            # if prompt contains 'title', return a short text
            if 'one-line' in prompt or 'one-line title' in prompt:
                return {"completion": "Fix: something"}
            # otherwise return JSON
            return {
                "completion": json.dumps({
                    "title": "Fix: something",
                    "what_changed": "changed",
                    "why": "reason",
                    "files_impacted": ["a.py"],
                    "tests": "none",
                    "risk_level": "low",
                    "rollback_plan": "revert"
                })
            }

    mod.Client = FakeClient
    monkeypatch.setitem(sys.modules, "anthropic", mod)

    from autopr.providers import AnthropicProvider

    p = AnthropicProvider(api_key="fake", model="fake")
    t = p.generate_pr_title("+ added", ["fix: a"], None)
    assert t.startswith("Fix:")

    d = p.generate_pr_description("+ added", ["fix: a"], None)
    assert isinstance(d, dict)
    assert d.get("title", "").startswith("Fix:")
