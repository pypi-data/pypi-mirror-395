"""Plugin system for extensible functionality."""
from pathlib import Path
import json
import importlib.util

PLUGIN_DIR = Path.home() / ".heavenpc" / "plugins"
PLUGIN_DIR.mkdir(parents=True, exist_ok=True)

class Plugin:
    """Base class for HeavenPC plugins."""
    name = "UnknownPlugin"
    version = "0.0.1"
    
    def execute(self):
        raise NotImplementedError

def load_plugins():
    """Load all plugins from the plugins directory."""
    plugins = {}
    for pf in PLUGIN_DIR.glob("*.py"):
        try:
            spec = importlib.util.spec_from_file_location(pf.stem, pf)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "plugin"):
                plugins[pf.stem] = module.plugin
        except Exception as e:
            pass
    return plugins

def list_plugins():
    """List available plugins."""
    plugins = load_plugins()
    return {
        "total": len(plugins),
        "plugins": [{"name": name, "version": getattr(p, "version", "unknown")} for name, p in plugins.items()]
    }
