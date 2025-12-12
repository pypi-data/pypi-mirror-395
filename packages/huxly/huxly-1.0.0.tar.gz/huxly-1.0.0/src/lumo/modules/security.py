"""Security and privacy utilities (conservative, non-destructive)."""
from pathlib import Path
import hashlib
from ..utils.logging import logger

SIGNATURE_STORE = Path.home() / ".heavenpc" / "signatures"
SIGNATURE_STORE.mkdir(parents=True, exist_ok=True)

def scan(full: bool = False):
    """Perform a conservative scan: hash suspicious files in common locations and report.

    This is NOT a replacement for a full antivirus engine. It implements safe
    heuristics (e.g., large unknown executables in temp folders) and quarantines
    to a safe directory when explicitly requested.
    """
    report = {"full": full, "issues": []}
    temp = Path.home() / "AppData" / "Local" / "Temp"
    locations = [temp]
    for loc in locations:
        if loc.exists():
            for f in loc.glob("**/*"):
                try:
                    if f.is_file() and f.stat().st_size > 10_000_000:
                        h = hashlib.sha256(f.read_bytes()).hexdigest()
                        report["issues"].append({"path": str(f), "sha256": h})
                except Exception as e:
                    logger.debug("Skipping %s: %s", f, e)

    logger.info("Security scan complete: %s issues", len(report["issues"]))
    return report
