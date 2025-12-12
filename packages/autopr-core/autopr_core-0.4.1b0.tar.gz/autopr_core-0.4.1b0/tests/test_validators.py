from autopr import validators


def test_validate_generate_output_missing_keys():
    res = {}
    v = validators.validate_generate_output(res)
    assert not v["valid"]
    assert "Missing key:" in v["errors"][0]


def test_validate_review_output_range_confidence():
    good = {"summary": "ok", "findings": [], "confidence": 0.9}
    v = validators.validate_review_output(good)
    assert v["valid"]

    bad = {"summary": "ok", "findings": [], "confidence": 2.0}
    v2 = validators.validate_review_output(bad)
    assert not v2["valid"] or v2["warnings"]
