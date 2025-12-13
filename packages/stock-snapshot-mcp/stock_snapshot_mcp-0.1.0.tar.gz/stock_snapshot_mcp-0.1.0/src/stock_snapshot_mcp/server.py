import asyncio
import json
import logging

# Support both package and direct-script execution
try:
    from .alpha_vantage_client import get_stock_snapshot
except ImportError:  # when run as `python server.py`
    from alpha_vantage_client import get_stock_snapshot

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("stock-snapshot-mcp")

server = Server("stock-snapshot-mcp")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_stock_snapshot",
            description=(
                "Return a stock snapshot from Alpha Vantage, including meta info, "
                "latest quote, basic fundamentals (if available), and recent "
                "daily OHLCV history. Educational / demo use only."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Ticker symbol, e.g. AAPL, MSFT, TSLA",
                    },
                    "history_days": {
                        "type": "integer",
                        "description": "Number of most recent daily candles to return (max ~100).",
                        "minimum": 1,
                        "maximum": 100,
                    },
                },
                "required": ["symbol"],
                "additionalProperties": False,
            },
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    logger.info("call_tool: name=%s arguments=%s", name, arguments)

    if name != "get_stock_snapshot":
        raise ValueError(f"Unknown tool: {name}")

    symbol = arguments.get("symbol")
    if not symbol:
        raise ValueError("Missing required argument: symbol")

    history_days = int(arguments.get("history_days", 60))
    snapshot = await get_stock_snapshot(symbol, history_days=history_days)

    return [
        types.TextContent(
            type="text",
            text=json.dumps(snapshot),
        )
    ]


async def _run_stdio() -> None:
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="stock-snapshot-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def main() -> None:
    """Console entrypoint for MCP stdio server."""
    asyncio.run(_run_stdio())


if __name__ == "__main__":
    main()
