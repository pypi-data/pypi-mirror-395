import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lumo.utils import platform, logging


def test_get_platform():
    p = platform.get_platform()
    assert p in ['windows', 'linux', 'darwin']


def test_is_admin():
    # Just verify it runs without exception; admin status varies by environment
    result = platform.is_admin()
    assert isinstance(result, bool)


def test_logger_exists():
    assert logging.logger is not None
    assert logging.LOG_FILE.parent.exists()
