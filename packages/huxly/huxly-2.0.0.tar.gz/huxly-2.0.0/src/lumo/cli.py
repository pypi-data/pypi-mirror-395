import sys
import json
import shutil
import os
from pathlib import Path
import click
from rich.console import Console

from . import __version__
from .utils import logger
from .modules import performance, security, game_mode, config as cfg, monitoring, ai_assistant, plugins
from .modules.ui import HuxlyUI
from .modules.ai_notifications import HuxlyAINotifier, SystemMonitorAI

console = Console()
ui = HuxlyUI()


@click.group()
@click.version_option(version=__version__)
def main():
    """Huxly 2.0 — Professional PC Utility with AI-Powered Notifications"""
    pass


@main.command()
@click.option("--dry-run", is_flag=True, help="Show changes without applying")
def optimize(dry_run):
    """Perform system optimizations (safe, reversible)."""
    logger.info("Running optimize, dry_run=%s", dry_run)
    ui.print_header()
    ui.print_command_output("System Optimization", "Analyzing your system...", is_json=False)
    
    result = performance.optimize(dry_run=dry_run)
    
    if result.get('success'):
        ui.print_success("Optimization Complete", f"Applied {len(result.get('optimizations', []))} optimizations")
    else:
        ui.print_error("Optimization Failed", result.get('error', 'Unknown error'))
    
    console.print_json(data=result)
    ui.print_footer()


@main.command()
@click.option("--full", is_flag=True, help="Run full security scan")
def scan(full):
    """Security scanning with threat detection."""
    logger.info("Running security scan, full=%s", full)
    ui.print_header()
    ui.print_command_output("Security Scan", "Scanning your system for threats...", is_json=False)
    
    result = security.scan(full=full)
    
    if result.get('threats_found', 0) == 0:
        ui.print_success("System Secure", "No threats detected")
    else:
        ui.print_notification(f"⚠ {result['threats_found']} potential threats found", "warning")
    
    console.print_json(data=result)
    ui.print_footer()


@main.group(name="game-mode")
def game_mode_group():
    """Game mode controls."""
    pass


@game_mode_group.command(name="start")
def game_start():
    """Start game mode."""
    logger.info("Starting game mode")
    ui.print_header()
    result = game_mode.start()
    ui.print_success("Game Mode Activated", "Your system is optimized for gaming")
    ui.print_notification("Gaming optimizations applied - enjoy!", "success")
    console.print_json(data=result)
    ui.print_footer()


@game_mode_group.command(name="stop")
def game_stop():
    """Stop game mode."""
    logger.info("Stopping game mode")
    ui.print_header()
    result = game_mode.stop()
    ui.print_success("Game Mode Deactivated", "System returned to normal")
    ui.print_notification("Normal mode restored", "info")
    console.print_json(data=result)
    ui.print_footer()


@main.command()
def status():
    """Real-time system status and health monitoring."""
    logger.info("Getting system status")
    ui.print_header()
    ui.print_welcome(os.getenv('USERNAME', 'User'))
    
    result = monitoring.get_status()
    
    # Display metrics in clean table format
    metrics = {
        "CPU Usage": {
            "value": f"{result.get('cpu_percent', 0)}%",
            "status": "✓" if result.get('cpu_percent', 0) < 70 else "⚠",
            "color": "green" if result.get('cpu_percent', 0) < 70 else "yellow"
        },
        "Memory": {
            "value": f"{result.get('memory_percent', 0)}%",
            "status": "✓" if result.get('memory_percent', 0) < 80 else "⚠",
            "color": "green" if result.get('memory_percent', 0) < 80 else "yellow"
        },
        "Disk": {
            "value": f"{result.get('disk_percent', 0)}%",
            "status": "✓" if result.get('disk_percent', 0) < 85 else "⚠",
            "color": "green" if result.get('disk_percent', 0) < 85 else "yellow"
        }
    }
    
    ui.print_status("System Metrics", metrics, icon="◆")
    
    # Show alerts if any
    if result.get('alerts'):
        for alert in result['alerts']:
            ui.print_notification(alert, "alert")
    
    console.print_json(data=result)
    ui.print_footer()


@main.command()
def suggest():
    """Get AI-powered system optimization suggestions."""
    logger.info("Getting AI suggestions")
    ui.print_header()
    ui.print_command_output("AI Assistant", "Analyzing your system for optimization opportunities...", is_json=False)
    
    metrics = monitoring.sample_metrics()
    result = ai_assistant.get_suggestions(metrics)
    
    if result.get('suggestions'):
        for i, suggestion in enumerate(result['suggestions'], 1):
            ui.print_notification(suggestion, "info")
    
    console.print_json(data=result)
    ui.print_footer()


@main.command()
@click.option("--set", "set_kv", nargs=2, required=False, help="Set config key value")
def config(set_kv):
    """View or edit configuration."""
    ui.print_header()
    
    if set_kv:
        k, v = set_kv
        logger.info("Set config %s=%s", k, v)
        cfg.set(k, v)
        ui.print_success("Configuration Updated", f"Set {k}={v}")
        ui.print_footer()
        return
    
    conf = cfg.load()
    ui.print_command_output("Configuration", json.dumps(conf, indent=2), is_json=True)
    ui.print_footer()


@main.command()
def rollback():
    """Rollback recent optimizations to previous state."""
    logger.info("Rollback requested")
    ui.print_header()
    ui.print_command_output("Rollback", "Restoring previous system state...", is_json=False)
    
    result = cfg.rollback()
    
    if result.get('success'):
        ui.print_success("Rollback Complete", "System restored to previous state")
    else:
        ui.print_error("Rollback Failed", result.get('error', 'No changes to rollback'))
    
    console.print_json(data=result)
    ui.print_footer()


@main.command(name="plugins")
def list_plugins():
    """List installed plugins and extensions."""
    logger.info("Plugins list requested")
    ui.print_header()
    
    result = plugins.list_plugins()
    ui.print_command_output("Installed Plugins", json.dumps(result, indent=2), is_json=True)
    ui.print_footer()


@main.command()
def notify():
    """Test and demonstrate AI notification system."""
    logger.info("Testing notifications")
    ui.print_header()
    
    api_key = os.getenv('OPEN_ROUTER_API_KEY', '')
    if not api_key:
        ui.print_error("Configuration", "OPEN_ROUTER_API_KEY environment variable not set")
        ui.print_notification("Set OPEN_ROUTER_API_KEY to enable AI notifications", "warning")
    else:
        ui.print_success("Configuration", "API key found - testing notifications...")
    
    notifier = HuxlyAINotifier(api_key)
    monitor = SystemMonitorAI(notifier)
    
    # Test various notifications
    ui.print_separator()
    ui.print_notification(monitor.send_welcome(), "success")
    ui.print_separator()
    
    # Simulate alerts
    test_alerts = [
        ('cpu', {'cpu_percent': 85, 'top_process': 'Chrome (25%)'}),
        ('memory', {'memory_percent': 82, 'memory_gb': 14.2}),
        ('disk', {'disk_percent': 88}),
    ]
    
    for alert_type, metrics in test_alerts:
        notif = notifier.send_notification(alert_type, metrics)
        ui.print_notification(notif, "alert")
        ui.print_separator()
    
    ui.print_footer()


@main.command()
def startup():
    """Simulate system startup with welcome notification."""
    logger.info("Startup command")
    ui.print_header()
    
    api_key = os.getenv('OPEN_ROUTER_API_KEY', '')
    notifier = HuxlyAINotifier(api_key)
    
    # Send startup notification
    startup_notif = notifier.send_notification('startup', {})
    ui.print_notification(startup_notif, "success")
    
    ui.print_welcome(os.getenv('USERNAME', 'User'))
    ui.print_notification("Huxly is now running and protecting your system", "success")
    ui.print_footer()


@main.command()
def uninstall():
    """Uninstall Huxly and clean up all data."""
    logger.info("Uninstall requested")
    ui.print_header()
    ui.print_error("Uninstall Huxly", "This will remove Huxly from your system")
    
    if click.confirm("Are you sure you want to uninstall Huxly?"):
        result = cfg.uninstall()
        ui.print_success("Uninstalled", "Huxly has been removed from your system")
        try:
            shutil.rmtree(Path.home() / ".huxly", ignore_errors=True)
            ui.print_notification("All user data cleaned up", "success")
        except:
            pass
    else:
        ui.print_notification("Uninstall cancelled", "info")
    
    ui.print_footer()


if __name__ == "__main__":
    main()
