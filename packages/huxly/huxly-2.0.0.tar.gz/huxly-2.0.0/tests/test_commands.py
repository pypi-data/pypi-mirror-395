import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import click.testing
from lumo import cli


def test_scan_command():
    runner = click.testing.CliRunner()
    result = runner.invoke(cli.main, ['scan'])
    assert result.exit_code == 0
    assert 'issues' in result.output


def test_game_mode_start():
    runner = click.testing.CliRunner()
    result = runner.invoke(cli.main, ['game-mode', 'start'])
    assert result.exit_code == 0
    assert 'started' in result.output


def test_game_mode_stop():
    runner = click.testing.CliRunner()
    result = runner.invoke(cli.main, ['game-mode', 'stop'])
    assert result.exit_code == 0
    assert 'stopped' in result.output


def test_config_view():
    runner = click.testing.CliRunner()
    result = runner.invoke(cli.main, ['config'])
    assert result.exit_code == 0
    assert 'auto_optimize' in result.output


def test_rollback_no_history():
    runner = click.testing.CliRunner()
    result = runner.invoke(cli.main, ['rollback'])
    assert result.exit_code == 0
    # no_history is expected if no changes have been recorded
    assert 'rolled_back' in result.output or 'no_history' in result.output
