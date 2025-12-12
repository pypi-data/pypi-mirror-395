from autopr import analysis


def test_todo_and_print_and_unused_import():
    diff = """
+import os
+import json
+
+def foo():
+    print('debug')
+    # TODO: remove debug
+    return 1
"""

    findings = analysis.analyze_diff(diff, language='python')
    types = {f['type'] for f in findings}
    assert 'todo' in types
    assert 'debug_print' in types
    assert 'unused_import' in types


def test_none_equality_and_missing_try():
    code = """
def read_file(path):
    f = open(path)
    data = f.read()
    return data

def check(val):
    if val == None:
        return True
    return False
"""
    findings = analysis.analyze_diff(code, language='python')
    types = {f['type'] for f in findings}
    assert 'missing_error_handling' in types
    assert 'none_equality_comparison' in types
