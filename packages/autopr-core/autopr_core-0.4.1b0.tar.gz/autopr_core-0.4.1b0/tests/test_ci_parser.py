from autopr import ci_parser


def test_parse_pytest_output_simple():
    log = """
============================= test session starts ==============================
collected 2 items

tests/test_example.py ..                                               [100%]

========================== 2 passed in 0.02s ===========================
"""
    res = ci_parser.parse_pytest_output(log)
    assert res["passed"] == 2
    assert res["failed"] == 0


def test_parse_pytest_output_failures():
    log = """
============================= test session starts ==============================
collected 2 items

tests/test_example.py F.                                               [100%]

================================== FAILURES ===================================
________________________ test_does_thing _____________________________________

    def test_does_thing():
>       assert False
E       AssertionError: assert False

tests/test_example.py:5: AssertionError

======================== 1 failed, 1 passed in 0.01s ==========================
"""
    res = ci_parser.parse_pytest_output(log)
    assert res["failed"] == 1
    assert len(res["failures"]) >= 1
