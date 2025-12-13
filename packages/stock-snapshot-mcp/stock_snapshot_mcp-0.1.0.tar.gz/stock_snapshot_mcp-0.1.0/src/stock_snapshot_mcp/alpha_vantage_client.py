import os
import time
import asyncio
from typing import Dict, Any, List, Optional

import httpx
from dotenv import load_dotenv

load_dotenv()

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

if not ALPHAVANTAGE_API_KEY:
    raise RuntimeError("ALPHAVANTAGE_API_KEY not set")

# Free API has strict limits – be gentle.
_MIN_SECONDS_BETWEEN_CALLS = 0.6
_last_call_ts = 0.0


async def _av_get(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Throttled Alpha Vantage GET helper.

    If Alpha Vantage says "premium endpoint", raise a RuntimeError that clearly
    indicates which function caused it.
    """
    global _last_call_ts
    now = time.time()
    elapsed = now - _last_call_ts
    if elapsed < _MIN_SECONDS_BETWEEN_CALLS:
        await asyncio.sleep(_MIN_SECONDS_BETWEEN_CALLS - elapsed)

    params = {**params, "apikey": ALPHAVANTAGE_API_KEY}

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(BASE_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

    _last_call_ts = time.time()

    # Alpha Vantage often returns "Note" or "Information" on error / premium-only
    if "Note" in data or "Information" in data:
        msg = data.get("Note") or data.get("Information")
        fn = params.get("function")
        raise RuntimeError(f"Alpha Vantage error for function {fn}: {msg}")
    return data


# ---------------------- LOW-LEVEL ENDPOINT HELPERS ----------------------


async def get_global_quote(symbol: str) -> Dict[str, Any]:
    """
    Lightweight quote
    """
    return await _av_get({"function": "GLOBAL_QUOTE", "symbol": symbol})


async def get_company_overview(symbol: str) -> Dict[str, Any]:
    """
    Company fundamentals. If Alpha Vantage ever moves this to premium,
    we'll handle that higher up and just skip fundamentals.
    """
    return await _av_get({"function": "OVERVIEW", "symbol": symbol})


async def get_daily_series(symbol: str, outputsize: str = "compact") -> Dict[str, Any]:
    """
    Use TIME_SERIES_DAILY instead of TIME_SERIES_DAILY_ADJUSTED to avoid premium-only issues.
    """
    return await _av_get(
        {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": outputsize,  # 'compact' ~100 days; 'full' = full history
        }
    )


# --------------------------- SAFE CAST HELPERS --------------------------


def _safe_float(x: Optional[str]) -> Optional[float]:
    try:
        return float(x)
    except Exception:
        return None


def _safe_int(x: Optional[str]) -> Optional[int]:
    try:
        return int(float(x))
    except Exception:
        return None


def _parse_percent(p: Optional[str]) -> Optional[float]:
    if not p:
        return None
    try:
        return float(p.strip().replace("%", ""))
    except Exception:
        return None


# --------------------------- HIGH-LEVEL API -----------------------------


async def get_stock_snapshot(symbol: str, history_days: int = 60) -> Dict[str, Any]:
    """
    High-level helper that combines quote, overview, and daily history
    into one normalized JSON structure.

    If fundamentals (OVERVIEW) hit a premium-only restriction, simply
    omit them instead of crashing.
    """
    symbol = symbol.upper().strip()

    # 1) Quote
    quote_raw = await get_global_quote(symbol)
    quote = quote_raw.get("Global Quote", {})

    # 2) Fundamentals (may be free; if not, disclude)
    try:
        overview_raw = await get_company_overview(symbol)
    except RuntimeError as e:
        # If this is a premium-only issue, just log it and proceed without fundamentals
        if "premium endpoint" in str(e).lower():
            overview_raw = {}
        else:
            raise
    overview = overview_raw or {}

    # 3) Daily prices (use TIME_SERIES_DAILY, free for EOD data)
    daily_raw = await get_daily_series(symbol, outputsize="compact")
    series = (
        daily_raw.get("Time Series (Daily)")
        or daily_raw.get("Time Series (Daily) ".strip())
        or {}
    )

    # Normalize daily history into sorted list (newest first)
    daily_history: List[Dict[str, Any]] = []
    for date_str, vals in series.items():
        daily_history.append(
            {
                "date": date_str,
                "open": _safe_float(vals.get("1. open")),
                "high": _safe_float(vals.get("2. high")),
                "low": _safe_float(vals.get("3. low")),
                "close": _safe_float(vals.get("4. close")),
                # TIME_SERIES_DAILY doesn't have adjusted_close; reuse close
                "adjusted_close": _safe_float(vals.get("4. close")),
                "volume": _safe_int(vals.get("5. volume")),
            }
        )

    daily_history.sort(key=lambda x: x["date"], reverse=True)
    if history_days and history_days > 0:
        daily_history = daily_history[:history_days]

    return {
        "symbol": symbol,
        "meta": {
            "name": overview.get("Name"),
            "sector": overview.get("Sector"),
            "industry": overview.get("Industry"),
            "currency": overview.get("Currency"),
            "exchange": overview.get("Exchange"),
        },
        "quote": {
            "price": _safe_float(quote.get("05. price")),
            "change": _safe_float(quote.get("09. change")),
            "change_percent": _parse_percent(quote.get("10. change percent")),
            "previous_close": _safe_float(quote.get("08. previous close")),
            "latest_trading_day": quote.get("07. latest trading day"),
            "volume": _safe_int(quote.get("06. volume")),
        },
        "fundamentals": {
            "market_cap": _safe_int(overview.get("MarketCapitalization")),
            "pe_ratio_ttm": _safe_float(overview.get("PERatio")),
            "eps_ttm": _safe_float(overview.get("EPS")),
            "roe_ttm": _safe_float(overview.get("ReturnOnEquityTTM")),
            "profit_margin": _safe_float(overview.get("ProfitMargin")),
        },
        "daily_history": daily_history,
    }

