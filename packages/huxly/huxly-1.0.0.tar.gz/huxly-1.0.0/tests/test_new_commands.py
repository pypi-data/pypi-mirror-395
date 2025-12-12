import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import click.testing
from lumo import cli

def test_status_command():
    runner = click.testing.CliRunner()
    result = runner.invoke(cli.main, ['status'])
    assert result.exit_code == 0
    assert 'cpu_percent' in result.output or 'alerts' in result.output

def test_suggest_command():
    runner = click.testing.CliRunner()
    result = runner.invoke(cli.main, ['suggest'])
    assert result.exit_code == 0
    assert 'suggestions' in result.output

def test_plugins_command():
    runner = click.testing.CliRunner()
    result = runner.invoke(cli.main, ['plugins'])
    assert result.exit_code == 0
    assert 'total' in result.output
