import os
import requests
from datetime import datetime
from typing import Optional
EXCHANGE_API_KEY = os.getenv("RATE_API_KEY")


def _from_exchangerate_host(base: str, quote: str, date: Optional[str] = None):
    """Call exchangerate.host (free) as a fallback. Returns (rate, source, timestamp)."""
    if date:
        url = f"https://api.exchangerate.host/{date}"
        params = {"base": base.upper(), "symbols": quote.upper()}
    else:
        url = "https://api.exchangerate.host/latest"
        params = {"base": base.upper(), "symbols": quote.upper()}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    rate = None
    if "rates" in data and quote.upper() in data["rates"]:
        rate = float(data["rates"][quote.upper()])
    timestamp = datetime.utcnow()
    return rate, "exchangerate.host", timestamp


def get_rate(base: str, quote: str, date: Optional[str] = None) -> dict:
    """Get rate for base->quote. Try a paid provider if `RATE_API_KEY` present, otherwise fallback to exchangerate.host.

    Returns: {rate, source, timestamp, ttl_seconds}
    Raises: ValueError on missing rate
    """
    base = base.upper()
    quote = quote.upper()
    try:
        rate, source, timestamp = _from_exchangerate_host(base, quote, date)
    except requests.RequestException as e:
        raise ValueError(f"PROVIDER_ERROR: {str(e)}")
    except Exception as e:
        raise ValueError(f"UNEXPECTED_ERROR: {str(e)}")

    if rate is None:
        raise ValueError("RATE_NOT_FOUND")

    return {"rate": rate, "source": source, "timestamp": timestamp.isoformat() + "Z", "ttl_seconds": 3600}
