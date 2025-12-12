# Lumo 1.0

**by Tyora Inc.**

Lumo 1.0 is a **terminal-first cross-platform utility** to optimize, secure, and enhance PC experiences for gamers and power users. Fully functional, production-ready, no external APIs required.

## Quick Start

### Install from PyPI
```powershell
pip install huxly
```

### First commands
```powershell
lumo --help                    # Show all commands
lumo status                    # Real-time system status
lumo optimize --dry-run        # Suggest optimizations
lumo scan                      # Scan for security issues
lumo game-mode start           # Boost gaming performance
lumo suggest                   # Get AI recommendations
```

## Features

✓ **Performance** — CPU/RAM/process optimization with safe suggestions  
✓ **Security** — Conservative malware scanning and privacy cleanup  
✓ **Gaming** — FPS & network optimization (non-invasive)  
✓ **Monitoring** — Real-time system metrics & alerts  
✓ **AI Assistant** — Personalized suggestions based on load  
✓ **Rollback** — Undo risky changes automatically  
✓ **Config** — JSON-based settings management  
✓ **Plugins** — Extensible API for custom features  
✓ **Logging** — All actions tracked to `~/.heavenpc/logs/`  
✓ **Cross-platform** — Windows, Linux, macOS with unified CLI

## Commands

| Command | Purpose |
|---------|---------|
| `heavenpc optimize` | Suggest & apply safe optimizations |
| `heavenpc scan` | Detect suspicious files & clean privacy |
| `heavenpc game-mode start\|stop` | Enable/disable gaming tweaks |
| `heavenpc status` | Show CPU, RAM, disk, alerts |
| `heavenpc suggest` | Get AI-driven recommendations |
| `heavenpc config` | View/edit settings |
| `heavenpc plugins` | List installed plugins |
| `heavenpc rollback` | Undo last change |
| `heavenpc uninstall` | Remove HeavenPC + user data |

## Examples

### Optimize before gaming
```powershell
heavenpc game-mode start
heavenpc status
```

### Clean & secure
```powershell
heavenpc optimize
heavenpc scan
```

### Check system health
```powershell
heavenpc status
heavenpc suggest
```

### Automation (PowerShell)
```powershell
$status = heavenpc status | ConvertFrom-Json
if ($status.alerts) { 
    Write-Host "Alerts: $($status.alerts)" 
}
```

## Safety & Design

- **Conservative** — Suggests actions; never destructive without confirmation
- **Reversible** — Full rollback history; undo anytime
- **No external dependencies** — Works offline, no API keys or accounts
- **Modular** — Each feature independent; easy to extend
- **Tested** — 16+ unit tests; 100% coverage on core modules
- **Logged** — All operations recorded to `~/.heavenpc/logs/heavenpc.log`

## System Requirements

- Python 3.8+
- `click` ≥8.0, `psutil` ≥5.9, `rich` ≥12.0
- Windows 10+, Ubuntu 18+, macOS 10.13+
- Admin/sudo for some operations (prompted)

## Documentation

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** — System design, modules, extension
- **[USAGE.md](docs/USAGE.md)** — Detailed CLI guide & scripting examples

## Development

```bash
# Clone & install
git clone <repo> && cd heavenpc
pip install -e .

# Run tests
pytest tests/ -v

# Build standalone binary
pip install pyinstaller
./installer/build_pyinstaller.sh
# Binary: dist/heavenpc
```

## License

Specify license before public release. For now, experimental/research use only.

## Contributing

- Keep modules focused & testable
- Add pytest tests for all features
- Use `rich` for CLI output; `logger.info()` for logs
- Follow existing CLI patterns (Click, JSON)

## Security Notes

HeavenPC is conservative by design:
- Scans use heuristics, not external AV engines
- No system-level changes without user confirmation
- All changes logged and reversible
- No telemetry or cloud dependencies

Report security issues privately before opening public issues.

---

**Status**: Beta — All core features implemented and tested. Seeking community feedback before v1.0 release.

