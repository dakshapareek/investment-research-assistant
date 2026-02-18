# MCP (Model Context Protocol) Setup Guide

## Overview
This guide shows you how to integrate MCP servers into your Investment Research Platform for enhanced financial data access.

## What is MCP?

Model Context Protocol (MCP) is a standardized way for applications to access tools and data sources. Think of it as a universal adapter for different services.

### Benefits of Using MCP

1. **Standardized Interface**: One way to access multiple data sources
2. **Modularity**: Easy to add/remove data providers
3. **Flexibility**: Switch between providers without code changes
4. **Future-Proof**: New MCP servers can be added easily

## Where We Use MCP

### 1. Financial Data (Primary Use Case)
- Stock quotes and prices
- Historical data
- Company fundamentals
- Market data

### 2. Web Search (Optional)
- News articles
- Market sentiment
- Research reports

### 3. Database Operations (Future)
- Analysis history
- User preferences
- Watchlists

## Installation

### Step 1: Install MCP Python Package

```bash
cd backend
pip install mcp
```

### Step 2: Install UV (Python Package Manager)

MCP servers typically use `uvx` to run. Install UV:

**Windows:**
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Or using pip:**
```bash
pip install uv
```

### Step 3: Verify Installation

```bash
uvx --version
```

## Available MCP Servers for Financial Data

### 1. MCP Server Fetch (General Purpose)
```bash
uvx mcp-server-fetch
```

**Capabilities:**
- Web scraping
- API calls
- Data fetching

### 2. Yahoo Finance MCP Server (Recommended)
```bash
uvx mcp-server-yahoo-finance
```

**Capabilities:**
- Real-time stock quotes
- Historical data
- Company information
- Market data

### 3. Alpha Vantage MCP Server
```bash
uvx mcp-server-alpha-vantage
```

**Capabilities:**
- Stock data
- Forex data
- Crypto data
- Technical indicators

## Configuration

### Option 1: Use MCP for Financial Data

Update `backend/config.py`:

```python
# MCP Configuration
USE_MCP_FOR_FINANCIAL_DATA = True
MCP_SERVER_COMMAND = "uvx"
MCP_SERVER_ARGS = ["mcp-server-yahoo-finance"]
```

### Option 2: Hybrid Approach (Recommended)

Use MCP as primary, fallback to direct APIs:

```python
# Try MCP first
try:
    data = mcp_client.get_stock_quote(ticker)
    if data:
        return data
except:
    pass

# Fallback to direct API
return yahoo_finance_api.get_quote(ticker)
```

## Integration with Your App

### Update multi_api_client.py

Add MCP as the first data source:

```python
from mcp_financial_client import MCPFinancialClientSync

class MultiAPIStockClient:
    def __init__(self):
        self.mcp_client = MCPFinancialClientSync()
        # ... existing code
    
    def get_quote(self, ticker):
        # Try MCP first
        if USE_MCP_FOR_FINANCIAL_DATA:
            try:
                data = self.mcp_client.get_stock_quote(ticker)
                if data:
                    return data
            except:
                pass
        
        # Fallback to existing APIs
        # ... existing code
```

## Testing MCP Integration

### Test 1: Check MCP Server

```bash
# Test if MCP server is accessible
uvx mcp-server-yahoo-finance --help
```

### Test 2: Test from Python

```python
from mcp_financial_client import MCPFinancialClientSync

client = MCPFinancialClientSync(
    server_command="uvx",
    server_args=["mcp-server-yahoo-finance"]
)

# Get quote
quote = client.get_stock_quote("AAPL")
print(quote)

# Get historical data
historical = client.get_historical_data("AAPL", days=30)
print(historical)
```

### Test 3: Test from Flask

```bash
# Start backend
python backend/app.py

# Test endpoint
curl http://localhost:5000/api/analyze/AAPL
```

Check logs for:
```
✓ Connected to MCP server
  Available tools: ['get_stock_quote', 'get_historical_data']
```

## MCP Server Configuration File

Create `.kiro/settings/mcp.json` (optional, for Kiro IDE integration):

```json
{
  "mcpServers": {
    "yahoo-finance": {
      "command": "uvx",
      "args": ["mcp-server-yahoo-finance"],
      "env": {},
      "disabled": false,
      "autoApprove": ["get_stock_quote", "get_historical_data"]
    },
    "alpha-vantage": {
      "command": "uvx",
      "args": ["mcp-server-alpha-vantage"],
      "env": {
        "ALPHA_VANTAGE_API_KEY": "your_key_here"
      },
      "disabled": true,
      "autoApprove": []
    }
  }
}
```

## Advantages of MCP Approach

### 1. Modularity
```
Before: App → Yahoo API (hardcoded)
After:  App → MCP Client → MCP Server → Yahoo API
```

Easy to switch providers:
```python
# Switch from Yahoo to Alpha Vantage
MCP_SERVER_ARGS = ["mcp-server-alpha-vantage"]
```

### 2. Consistency
All data sources return the same format through MCP.

### 3. Extensibility
Add new data sources without changing app code:
```bash
# Add new MCP server
uvx mcp-server-new-provider
```

### 4. Separation of Concerns
- App logic separate from data fetching
- Data fetching separate from API details
- Easy to test and maintain

## Troubleshooting

### Error: "uvx: command not found"

**Solution:**
```bash
# Install UV
pip install uv

# Or download installer
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Error: "MCP server not found"

**Solution:**
```bash
# Install the MCP server
uvx mcp-server-yahoo-finance --help

# This will download and cache it
```

### Error: "Connection timeout"

**Solution:**
- Check internet connection
- Verify MCP server is running
- Try increasing timeout in code

### Error: "Tool not found"

**Solution:**
- List available tools:
```python
tools = await session.list_tools()
print([tool.name for tool in tools.tools])
```
- Use correct tool name

## Performance Considerations

### MCP Overhead
- **Startup**: ~100-200ms (server initialization)
- **Per Request**: ~10-50ms (protocol overhead)
- **Total**: Similar to direct API calls

### Optimization Tips

1. **Connection Pooling**: Reuse MCP connections
2. **Caching**: Cache MCP responses
3. **Async**: Use async for multiple requests
4. **Fallback**: Keep direct API as backup

## Migration Path

### Phase 1: Add MCP (Current)
- Install MCP client
- Add as optional data source
- Test alongside existing APIs

### Phase 2: Make MCP Primary
- Use MCP as first choice
- Fallback to direct APIs
- Monitor performance

### Phase 3: MCP Only (Future)
- Remove direct API code
- Use only MCP servers
- Simpler codebase

## Summary

MCP integration provides:
- ✓ Standardized data access
- ✓ Easy provider switching
- ✓ Modular architecture
- ✓ Future-proof design

**Current Status:**
- Email: SMTP (direct, no MCP needed)
- Financial Data: Can use MCP (recommended)
- News: Can use MCP (optional)
- Social: Direct scraping (no MCP available)

**Next Steps:**
1. Install UV and MCP package
2. Test MCP financial server
3. Integrate with multi_api_client
4. Monitor and optimize
