def test_get_rate_latest():
import pytest

from backend import tools


def fake_get_rate(base, quote, date=None):
    return {"rate": 0.85, "source": "mock", "timestamp": "2025-11-19T00:00:00Z", "ttl_seconds": 3600}


def test_get_rate_latest(monkeypatch):
    # Mock external provider to ensure deterministic tests
    monkeypatch.setattr(tools.get_rate, "_from_exchangerate_host", lambda b, q, d=None: (0.85, "mock", None))
    result = tools.get_rate.get_rate("USD", "EUR")
    assert "rate" in result
    assert result["rate"] == 0.85
