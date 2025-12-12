from click.testing import CliRunner

from autopr.cli import cli


def test_cli_gen_and_review():
    runner = CliRunner()
    result = runner.invoke(cli, ["gen", "--diff", "+ added", "--commits", "fix: a"]) 
    assert result.exit_code == 0
    assert "title" in result.output

    r2 = runner.invoke(cli, ["review", "--diff", "print(\"x\")\n# TODO: fix"]) 
    assert r2.exit_code == 0
    assert "findings" in r2.output

    ra = runner.invoke(cli, ["analyze", "--diff", "+def foo():\n+    print('x')\n+    # TODO", "--lang", "python"])
    assert ra.exit_code == 0
    assert "debug_print" in ra.output or "TODO" in ra.output
