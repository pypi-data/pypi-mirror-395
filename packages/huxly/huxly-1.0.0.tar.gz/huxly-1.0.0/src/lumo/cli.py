import sys
import json
import shutil
from pathlib import Path
import click
from rich.console import Console

from . import __version__
from .utils import logger
from .modules import performance, security, game_mode, config as cfg, monitoring, ai_assistant, plugins

console = Console()


@click.group()
@click.version_option(version=__version__)
def main():
    """Lumo 1.0 — PC Utility by Tyora Inc."""
    pass


@main.command()
@click.option("--dry-run", is_flag=True, help="Show changes without applying")
def optimize(dry_run):
    """Perform system optimizations (safe, reversible)."""
    logger.info("Running optimize, dry_run=%s", dry_run)
    result = performance.optimize(dry_run=dry_run)
    console.print_json(data=result)


@main.command()
@click.option("--full", is_flag=True, help="Run a full scan (slower)" )
def scan(full):
    """Run malware and privacy scan."""
    logger.info("Running scan, full=%s", full)
    result = security.scan(full=full)
    console.print_json(data=result)


@main.group(name="game-mode")
def game_mode_group():
    """Game mode controls."""
    pass


@game_mode_group.command(name="start")
def game_start():
    """Start game mode."""
    logger.info("Starting game mode")
    result = game_mode.start()
    console.print_json(data=result)


@game_mode_group.command(name="stop")
def game_stop():
    """Stop game mode."""
    logger.info("Stopping game mode")
    result = game_mode.stop()
    console.print_json(data=result)


@main.command()
def rollback():
    """Rollback last risky changes."""
    logger.info("Rollback requested")
    result = cfg.rollback()
    console.print_json(data=result)


@main.command()
@click.option("--set", "set_kv", nargs=2, required=False, help="Set config key value")
def config(set_kv):
    """View or edit configuration."""
    if set_kv:
        k, v = set_kv
        logger.info("Set config %s=%s", k, v)
        cfg.set(k, v)
        console.print(f"Set {k}={v}")
        return
    conf = cfg.load()
    console.print_json(data=conf)


@main.command()
def uninstall():
    """Uninstall HeavenPC and remove configs."""
    logger.warn("Uninstall requested — confirming")
    click.confirm("Are you sure you want to uninstall HeavenPC?", abort=True)
    # perform uninstall steps
    installer = Path(__file__).parent.parent / "installer" / "uninstall.sh"
    if installer.exists():
        console.print("Running uninstall script...")
        try:
            shutil.rmtree(Path.home() / ".heavenpc", ignore_errors=True)
            console.print("Removed user data and config.")
        except Exception as e:
            console.print(f"Error removing data: {e}")
    console.print("Uninstall complete — please remove package via pip if desired.")


@main.command(name="status")
def status():
    """Show real-time system status and alerts."""
    logger.info("Status requested")
    result = monitoring.get_status()
    console.print_json(data=result)


@main.command(name="suggest")
def suggest():
    """Get AI-driven suggestions based on current system state."""
    logger.info("AI suggestions requested")
    metrics = monitoring.sample_metrics()
    result = ai_assistant.get_suggestions(metrics)
    console.print_json(data=result)


@main.command(name="plugins")
def list_plugins():
    """List installed plugins."""
    logger.info("Plugins list requested")
    result = plugins.list_plugins()
    console.print_json(data=result)


if __name__ == "__main__":
    main()
