import os
import asyncio
import pytest

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from stock_snapshot_mcp import get_stock_snapshot



def test_get_stock_snapshot_basic():
    """
    Simple integration test: call Alpha Vantage and ensure
    we get the expected structure back for a known symbol.
    """
    if not os.getenv("ALPHAVANTAGE_API_KEY"):
        pytest.skip("ALPHAVANTAGE_API_KEY not set, set it first in .env")

    async def _run():
        snap = await get_stock_snapshot("AAPL", history_days=5)

        assert snap["symbol"] == "AAPL"
        assert "meta" in snap
        assert "quote" in snap
        assert "fundamentals" in snap
        assert "daily_history" in snap

        # basic sanity checks
        assert snap["quote"]["price"] is not None
        assert 1 <= len(snap["daily_history"]) <= 5

    asyncio.run(_run())
