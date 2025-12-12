"""Configuration management and rollback storage."""
from pathlib import Path
import json

CONFIG_DIR = Path.home() / ".heavenpc"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = CONFIG_DIR / "config.json"
ROLLBACK_FILE = CONFIG_DIR / "rollback.json"

DEFAULTS = {
    "auto_optimize": False,
    "send_anonymous_stats": False,
}

def load():
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except Exception:
            return DEFAULTS.copy()
    return DEFAULTS.copy()

def set(k, v):
    conf = load()
    # basic type inference
    if v.lower() in ("true", "false"):
        vv = v.lower() == "true"
    else:
        try:
            vv = int(v)
        except Exception:
            vv = v
    conf[k] = vv
    CONFIG_FILE.write_text(json.dumps(conf, indent=2))

def save_rollback(action):
    history = []
    if ROLLBACK_FILE.exists():
        try:
            history = json.loads(ROLLBACK_FILE.read_text())
        except Exception:
            history = []
    history.append(action)
    ROLLBACK_FILE.write_text(json.dumps(history, indent=2))

def rollback():
    if not ROLLBACK_FILE.exists():
        return {"status": "no_history"}
    try:
        history = json.loads(ROLLBACK_FILE.read_text())
        last = history.pop()
        ROLLBACK_FILE.write_text(json.dumps(history, indent=2))
        return {"status": "rolled_back", "action": last}
    except Exception as e:
        return {"status": "error", "error": str(e)}
