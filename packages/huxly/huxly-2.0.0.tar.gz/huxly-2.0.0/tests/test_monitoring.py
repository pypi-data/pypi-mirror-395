import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lumo.modules import monitoring, ai_assistant

def test_sample_metrics():
    metrics = monitoring.sample_metrics()
    assert "cpu_percent" in metrics
    assert "memory_percent" in metrics
    assert "timestamp" in metrics

def test_get_status():
    status = monitoring.get_status()
    assert "alerts" in status
    assert "cpu_percent" in status

def test_ai_suggestions():
    metrics = {"cpu_percent": 85, "memory_percent": 50, "disk_percent": 30}
    result = ai_assistant.get_suggestions(metrics)
    assert "suggestions" in result
    assert len(result["suggestions"]) > 0
    assert "CPU" in result["suggestions"][0]
