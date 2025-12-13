from typer.testing import CliRunner

from opsgeniecli.cli import app

runner = CliRunner()


def test_commands():
    result = runner.invoke(app=app, args=["--help"])
    assert result.exit_code == 0
    assert "on-call" in result.stdout
    assert "config" in result.stdout
