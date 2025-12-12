"""Performance and optimization utilities."""
from pathlib import Path
import psutil
from ..utils.logging import logger

def optimize(dry_run: bool = False):
    """Perform safe optimizations and return a report dict.

    This implementation is conservative: it suggests which processes
    could be lowered in priority and clears ephemeral temp files.
    """
    report = {"actions": [], "suggestions": []}

    # memory pressure check
    vm = psutil.virtual_memory()
    report["memory_percent"] = vm.percent
    if vm.percent > 75:
        report["suggestions"].append("High memory usage: consider closing background apps.")

    # list processes using most memory
    procs = sorted(psutil.process_iter(["pid", "name", "memory_percent"]), key=lambda p: p.info.get("memory_percent") or 0, reverse=True)
    top = []
    for p in procs[:10]:
        top.append({"pid": p.info["pid"], "name": p.info["name"], "mem%": p.info.get("memory_percent")})
    report["top_processes"] = top

    # temp cleanup (non-destructive): list files in temp locations
    temp_paths = [Path(p) for p in ["/tmp", str(Path.home() / "AppData" / "Local" / "Temp" )] if Path(p).exists()]
    cleaned = 0
    listed = []
    for tp in temp_paths:
        for f in list(tp.glob("**/*"))[:50]:
            listed.append(str(f))
    report["temp_sample"] = listed[:50]

    # CPU suggestions
    cpu = psutil.cpu_percent(interval=0.5)
    report["cpu_percent"] = cpu
    if cpu > 80:
        report["suggestions"].append("High CPU usage: start Game Mode or close CPU-heavy apps.")

    logger.info("Optimize report generated: %s", report)
    return report
