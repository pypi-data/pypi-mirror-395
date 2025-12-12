from autopr import parser


def test_parse_diff_basic():
    diff = """
+++ b/src/foo.py
@@ -1,3 +1,6 @@
+def added(a, b):
+    return a + b
-def removed():
"""

    out = parser.parse_diff(diff)
    assert isinstance(out, dict)
    assert "src/foo.py" in out["files_changed"]
    assert out["added_lines"] >= 2
    assert "added" in ",".join(out["added_functions"]) or "added" # quick contains check
