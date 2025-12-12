from fastapi.testclient import TestClient

from autopr.main import app


client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_generate_returns_expected_keys():
    payload = {"diff": "+ added line", "commits": ["feat: add foo"], "issue": "#123"}
    r = client.post("/generate", json=payload)
    assert r.status_code == 200
    body = r.json()
    # ensure keys exist and are of the expected type
    assert isinstance(body.get("title"), str)
    assert isinstance(body.get("what_changed"), str)
    assert isinstance(body.get("why"), str)
    assert isinstance(body.get("files_impacted"), list)
    assert isinstance(body.get("tests"), str)
    assert isinstance(body.get("risk_level"), str)
    assert isinstance(body.get("rollback_plan"), str)


def test_review_finds_simple_patterns():
    payload = {"diff": "print(\"debug\")\n# TODO: remove later"}
    r = client.post("/review", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body.get("summary"), str)
    assert isinstance(body.get("findings"), list)
    # findings item shape
    if body.get("findings"):
        f = body["findings"][0]
        assert "type" in f and "message" in f
    # confidence should be float-like
    assert isinstance(body.get("confidence"), (float, int))


def test_openapi_contains_response_schemas():
    r = client.get("/openapi.json")
    assert r.status_code == 200
    spec = r.json()
    comps = spec.get("components", {}).get("schemas", {})
    assert "GenerateResponse" in comps
    assert "ReviewResponse" in comps


def test_review_includes_static_findings():
    payload = {"diff": "+def foo():\n+    print('debug')\n+    # TODO: remove later"}
    r = client.post("/review", json=payload)
    assert r.status_code == 200
    body = r.json()
    types = {f.get("type") for f in body.get("findings", [])}
    assert "debug_print" in types or "todo" in types
