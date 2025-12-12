import sys
from pathlib import Path

# Ensure local src/ is on sys.path for tests
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import click.testing
from lumo import cli


def test_help_shows_commands():
    runner = click.testing.CliRunner()
    result = runner.invoke(cli.main, ['--help'])
    assert result.exit_code == 0
    output = result.output
    assert 'optimize' in output
    assert 'scan' in output
    assert 'game-mode' in output


def test_optimize_dry_run():
    runner = click.testing.CliRunner()
    result = runner.invoke(cli.main, ['optimize', '--dry-run'])
    assert result.exit_code == 0
    assert 'memory_percent' in result.output or result.output.strip() != ''
