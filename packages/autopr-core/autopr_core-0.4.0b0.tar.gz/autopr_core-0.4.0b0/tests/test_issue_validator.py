from autopr import issue_validator


def test_simple_issue_alignment_full_overlap():
    issue = "Fix add function for negative numbers"
    diff = "+def add(a, b):\n+    if a < 0: a = 0\n+    return a + b\n"
    commits = ["fix: handle negative numbers in add"]
    res = issue_validator.simple_issue_alignment(issue, diff, commits)
    assert res["score"] > 0
    assert isinstance(res["matched"], list)


def test_simple_issue_alignment_no_overlap():
    issue = "Implement user login"
    diff = "+def add(a,b):\n    return a+b\n"
    commits = ["feat: add math helper"]
    res = issue_validator.simple_issue_alignment(issue, diff, commits)
    assert res["score"] == 0.0
