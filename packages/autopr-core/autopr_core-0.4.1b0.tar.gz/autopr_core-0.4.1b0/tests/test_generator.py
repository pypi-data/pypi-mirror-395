from autopr.generator import generate_pr_from


def test_generate_pr_from_stub():
    diff = "+def add(x, y):\n+  return x + y\n"
    commits = ["feat: add add function"]
    res = generate_pr_from(diff, commits, issue="#99")
    assert isinstance(res, dict)
    # ensure keys exist
    for k in ("title", "what_changed", "why", "files_impacted", "tests", "risk_level", "rollback_plan"):
        assert k in res
    # should include context from parser
    assert "_context" in res and isinstance(res["_context"], dict)
