# 📈 Stock Snapshot MCP  

*A minimal, educational MCP server for stock snapshots using the free Alpha Vantage API.*

**Stock Snapshot MCP** is a tiny, easy-to-read reference implementation of a  
[Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server.

It exposes a **single, clean tool**:
```get_stock_snapshot(symbol, history_days=60)```


This tool queries the free Alpha Vantage API and returns:

- Company metadata (name, sector, industry, exchange, currency)  
- Latest quote (price, change, percent, previous close, volume)  
- Basic fundamentals (PE ratio, EPS, market cap, ROE, profit margin — if available)  
- Recent OHLCV price history (daily candles)

This project is ideal for:

- People learning MCP through a small, realistic example  
- Developers building **RAG-ready financial research agents**  
- Students who want a simple MCP server to extend or customize  
- Anyone experimenting with Claude / ChatGPT MCP integrations  
- Mini-projects where clean, structured stock data is useful  

> **Note:** This project is *not* affiliated with Alpha Vantage.  
> It is designed solely as an educational reference.  
> **Not for real trading or investment decisions.**

---

## ✨ Features

- 📦 **Lightweight Python package** (`pip install stock-snapshot-mcp`)
- 🔌 **MCP server (stdio)** compatible with Claude Desktop, ChatGPT MCP, and other tools
- 🔍 Clean JSON output suitable for LLM reasoning & agent pipelines

---

## ⚙️ Installation

### **1. Install the package**
```bash
pip install stock-snapshot-mcp
```
### **2. Set your Alpha Vantage API key**

Create a .env file or export it:
```bash
export ALPHAVANTAGE_API_KEY=your_key_here
```
---

## 🚀 Running the MCP server

Once installed:
```bash
stock-snapshot-mcp
```

This launches the MCP server over stdio, ready to be used by MCP-compatible clients.
To see logs:
```bash
STOCK_SNAPSHOT_MCP_LOG=info stock-snapshot-mcp
```

---

## 🧪 Testing locally (Python)

You can call the helper function directly:
```python
from stock_snapshot_mcp import get_stock_snapshot
import asyncio

async def main():
    snap = await get_stock_snapshot("AAPL", history_days=5)
    print(snap)

asyncio.run(main())
```

---

## 🧪 Example: manual MCP client

For debugging or learning MCP, you can run:

```bash
python examples/manual_mcp_client.py
````

---


## 🖥️ Using with Claude Desktop (example config)

Place this inside Claude’s configuration file:

**macOS**

`~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**

`%APPDATA%\Claude\claude_desktop_config.json`

Add:
```json
{
  "mcpServers": {
    "stock-snapshot-mcp": {
      "command": "stock-snapshot-mcp",
      "env": {
        "ALPHAVANTAGE_API_KEY": "your_key_here"
      }
    }
  }
}
```

Restart Claude Desktop → you should see Stock Snapshot MCP under "Connected Servers".

Then you can ask Claude:

> Call `get_stock_snapshot` for AAPL and summarize the fundamentals.

---

## 📤 Using with ChatGPT MCP (OpenAI Desktop / browser)

Add a new MCP connection:
- Command: `stock-snapshot-mcp`
- Environment:
  - `ALPHAVANTAGE_API_KEY=your_key_here`
And that’s it.

---

## 📚 Tool Definition (JSON Schema)

```php
get_stock_snapshot(
  symbol: string (required),
  history_days: integer (optional, 1–100, default: 60)
)
```

Output fields
```css
{
  "symbol": "AAPL",
  "meta": {
    "name": "Apple Inc",
    "sector": "TECHNOLOGY",
    "industry": "CONSUMER ELECTRONICS",
    "currency": "USD",
    "exchange": "NASDAQ"
  },
  "quote": {
    "price": 278.78,
    "change": -1.92,
    "change_percent": -0.684,
    "previous_close": 280.7,
    "latest_trading_day": "2025-12-05",
    "volume": 47265845
  },
  "fundamentals": {
    "market_cap": 4137203794000,
    "pe_ratio_ttm": 37.32,
    "eps_ttm": 7.47,
    "roe_ttm": 1.714,
    "profit_margin": 0.269
  },
  "daily_history": [ ... ]
}
```

---

## 🧱 Project Structure
```pgsql
stock-snapshot-mcp/
  ├─ src/
  │   └─ stock_snapshot_mcp/
  │        ├─ __init__.py             # Public API
  │        ├─ alpha_vantage_client.py # API wrapper
  │        └─ server.py               # MCP stdio server
  ├─ tests/
  │   └─ test_smoke.py
  ├─ examples/
  │   ├─ claude_desktop_config.json
  │   └─ chat_prompt_examples.md
  ├─ .env.example
  ├─ pyproject.toml
  ├─ README.md
  ├─ LICENSE
  └─ .gitignore
 ```

---

## 🛑 Disclaimer

This project:

- is not affiliated with Alpha Vantage 
- is not financial advice 
- is provided for educational and research purposes only

---

## 📜 License

MIT License — free to use, modify, and learn from.
