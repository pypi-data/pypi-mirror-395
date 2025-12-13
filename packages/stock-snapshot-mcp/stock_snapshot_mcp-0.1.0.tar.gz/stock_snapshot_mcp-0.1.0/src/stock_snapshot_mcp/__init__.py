"""
stock_snapshot_mcp

A minimal MCP server + helpers that wrap the free Alpha Vantage API
into a single `get_stock_snapshot` tool for LLMs and agents.

Exports:
- get_stock_snapshot: high-level helper for meta, quote, fundamentals, and
  recent daily OHLCV history.
"""

from .alpha_vantage_client import (
    get_stock_snapshot,
    get_global_quote,
    get_company_overview,
    get_daily_series,
)

__all__ = [
    "get_stock_snapshot",
    "get_global_quote",
    "get_company_overview",
    "get_daily_series",
]

__version__ = "0.1.0"
