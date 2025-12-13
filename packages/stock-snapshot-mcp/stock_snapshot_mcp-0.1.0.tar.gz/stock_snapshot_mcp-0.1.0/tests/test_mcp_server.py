import os
import json
import asyncio
from pathlib import Path

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def test_mcp_server_get_stock_snapshot():
    """
    End-to-end MCP test:

    - start the stdio MCP server (server.py via python)
    - initialize the session
    - list tools and check get_stock_snapshot is there
    - call the tool for AAPL
    - parse the JSON and assert basic fields
    """
    if not os.getenv("ALPHAVANTAGE_API_KEY"):
        pytest.skip("ALPHAVANTAGE_API_KEY not set, set it first in .env")

    # Resolve path to src/stock_snapshot_mcp/server.py
    server_path = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "stock_snapshot_mcp"
        / "server.py"
    )

    async def _run():
        server_params = StdioServerParameters(
            command="python",
            args=[str(server_path)],
            env=None,  # rely on current env / .env loading
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # 1) initialize
                await session.initialize()

                # 2) list tools
                tools_result = await session.list_tools()
                tools = tools_result.tools
                assert any(t.name == "get_stock_snapshot" for t in tools)

                # 3) call the tool
                result = await session.call_tool(
                    "get_stock_snapshot",
                    arguments={"symbol": "AAPL", "history_days": 5},
                )

                text_contents = [
                    c for c in result.content
                    if getattr(c, "type", None) == "text"
                ]
                assert text_contents, "Tool should return at least one text content item"

                data = json.loads(text_contents[0].text)

                # 4) basic payload checks
                assert data["symbol"] == "AAPL"
                assert "quote" in data
                assert data["quote"]["price"] is not None
                assert isinstance(data["daily_history"], list)
                assert 1 <= len(data["daily_history"]) <= 5

    asyncio.run(_run())
