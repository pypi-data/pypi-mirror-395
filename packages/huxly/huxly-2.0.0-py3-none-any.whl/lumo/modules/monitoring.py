"""Real-time monitoring and alerting."""
from pathlib import Path
import json
import psutil
from datetime import datetime

MONITOR_FILE = Path.home() / ".heavenpc" / "monitor.json"

def sample_metrics():
    """Capture current system metrics."""
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent if Path("/").exists() else psutil.disk_usage("C:\\").percent,
        "process_count": len(psutil.pids()),
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
    }

def get_status():
    """Get current system status with alerts."""
    metrics = sample_metrics()
    alerts = []
    if metrics["cpu_percent"] > 80:
        alerts.append(f"High CPU: {metrics['cpu_percent']:.1f}%")
    if metrics["memory_percent"] > 85:
        alerts.append(f"High memory: {metrics['memory_percent']:.1f}%")
    if metrics["disk_percent"] > 90:
        alerts.append(f"Disk almost full: {metrics['disk_percent']:.1f}%")
    metrics["alerts"] = alerts
    return metrics
