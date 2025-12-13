from typer.testing import CliRunner
from dhruv.cli import app

runner = CliRunner()

def test_hello_command():
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "Hello from Dhruv!" in result.stdout
