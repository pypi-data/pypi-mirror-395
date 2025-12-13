import asyncio
import json
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    project_root = Path(__file__).resolve().parents[1]
    server_path = project_root / "src" / "stock_snapshot_mcp" / "server.py"

    server_params = StdioServerParameters(
        command="python",
        args=[str(server_path)],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1) Initialize
            await session.initialize()
            print("✅ Initialized MCP session")

            # 2) List tools
            tools_result = await session.list_tools()
            print("\n=== RAW TOOLS RESULT ===")
            print(tools_result)

            # Extract tools list in a safe way
            if hasattr(tools_result, "tools"):
                tools_list = tools_result.tools
            else:
                tools_list = tools_result

            print("\n=== TOOLS (pretty) ===")
            try:
                serialized = []
                for t in tools_list:
                    if hasattr(t, "model_dump"):
                        serialized.append(t.model_dump())
                    else:
                        serialized.append(str(t))
                print(json.dumps(serialized, indent=2))
            except TypeError:
                print(tools_list)

            # 3) Call our tool: get_stock_snapshot
            print("\nCalling get_stock_snapshot for AAPL ...")
            result = await session.call_tool(
                "get_stock_snapshot",
                arguments={"symbol": "AAPL", "history_days": 5},
            )

            print("\n=== RAW TOOL CALL RESULT ===")
            print(result)

            # 4) Try to parse any JSON text content returned by the tool
            print("\n=== PARSED SNAPSHOT (if JSON present) ===")
            try:
                # result.content: list of content items
                contents = getattr(result, "content", result)
                for content in contents:
                    c_type = getattr(content, "type", None)
                    c_text = getattr(content, "text", None)
                    if c_type == "text" and isinstance(c_text, str):
                        try:
                            data = json.loads(c_text)
                            print(json.dumps(data, indent=2))
                        except json.JSONDecodeError:
                            print("Non-JSON text content:")
                            print(c_text)
            except Exception as e:
                print("Error while parsing tool result:", e)


if __name__ == "__main__":
    asyncio.run(main())
