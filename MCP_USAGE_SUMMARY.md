# MCP Usage in Investment Research Platform

## Current MCP Implementation

### Where MCP is Used

**1. Financial Data Fetching (Stock Quotes & Historical Data)**

Location: `backend/data_sources/multi_api_client.py`

MCP is used as the **PRIMARY** data source for:
- Stock quotes (current price, change, volume)
- Historical price data (charts)

**How it works:**
```
User requests stock data (e.g., AAPL)
    ↓
1. Try MCP Server first (mcp-server-fetch)
    ↓
2. If MCP fails, fallback to direct APIs:
   - Financial Modeling Prep
   - Alpha Vantage
   - Finnhub
   - Polygon.io
   - Marketstack
   - EODHD
   - Yahoo Finance
```

### MCP Server Configuration

**Server:** `mcp-server-fetch`
- **Command:** `uvx mcp-server-fetch`
- **Purpose:** Fetch web content and financial data
- **Status:** ✓ Initialized and running

**Configuration in `.env`:**
```env
USE_MCP_FOR_FINANCIAL_DATA=true
MCP_SERVER_COMMAND=python
MCP_SERVER_ARGS=-m,uv,tool,run,mcp-server-fetch
```

### Startup Logs

When the backend starts, you see:
```
✓ MCP client initialized: uvx mcp-server-fetch
```

This appears twice because:
1. First initialization in `multi_api_client.py` (for stock data)
2. Second initialization in `app.py` (for general use)

### Code Implementation

**File:** `backend/data_sources/multi_api_client.py`

```python
class MultiAPIStockClient:
    def __init__(self):
        # Initialize MCP client if enabled
        self.mcp_client = None
        if USE_MCP_FOR_FINANCIAL_DATA:
            from mcp_financial_client import MCPFinancialClientSync
            self.mcp_client = MCPFinancialClientSync(
                server_command=MCP_SERVER_COMMAND,
                server_args=MCP_SERVER_ARGS
            )
    
    def get_quote(self, ticker):
        # Try MCP first if enabled
        if self.mcp_client:
            try:
                data = self.mcp_client.get_stock_quote(ticker)
                if data and data.get('price'):
                    return data
            except Exception as e:
                print(f"✗ MCP failed: {e}")
        
        # Fallback to direct APIs...
```

### MCP Client Implementation

**File:** `backend/mcp_financial_client.py`

This file contains:
- `MCPFinancialClient` - Async MCP client
- `MCPFinancialClientSync` - Synchronous wrapper for Flask

**Key Methods:**
- `get_stock_quote(ticker)` - Get current stock price
- `get_historical_data(ticker, days)` - Get historical prices
- `search_ticker(query)` - Search for stock symbols

## Where MCP is NOT Used

### Email Service
- **Current:** Direct SMTP (Gmail App Password)
- **Why:** MCP doesn't have email/SMTP servers
- **Status:** Working reliably, no need to change

### News Fetching
- **Current:** Direct NewsAPI.org API calls
- **Why:** NewsAPI provides structured data with URLs
- **Status:** Working well with real news and links

### Social Media (Reddit/Twitter)
- **Current:** Direct API calls and web scraping
- **Why:** Requires authentication and specific APIs
- **Status:** Working with existing implementation

### LLM Operations
- **Current:** Direct OpenAI and Gemini API calls
- **Why:** LLM APIs are optimized for direct use
- **Status:** Recently migrated to OpenAI (gpt-4o-mini)

## Benefits of Current MCP Usage

1. **Unified Interface**: Single MCP server for multiple data sources
2. **Automatic Fallback**: If MCP fails, system falls back to direct APIs
3. **Easy Configuration**: Enable/disable MCP with one environment variable
4. **Future-Proof**: Easy to add more MCP servers for other data sources

## MCP Server Details

**mcp-server-fetch** is a general-purpose MCP server that can:
- Fetch web content
- Parse HTML
- Extract structured data
- Make HTTP requests

It's being used to fetch financial data from various sources through a unified interface.

## How to Verify MCP is Working

1. **Check Startup Logs:**
   ```
   ✓ MCP client initialized: uvx mcp-server-fetch
   ```

2. **Analyze a Stock:**
   - Search for any stock (e.g., AAPL)
   - Click "Analyze"
   - Check backend logs for:
     ```
     Trying MCP for AAPL...
     ✓ Successfully fetched from MCP
     ```

3. **If MCP Fails:**
   - You'll see: `✗ MCP failed: [error]`
   - System automatically falls back to direct APIs
   - No user-facing errors

## Configuration Options

### Enable/Disable MCP

In `backend/.env`:
```env
# Enable MCP
USE_MCP_FOR_FINANCIAL_DATA=true

# Disable MCP (use direct APIs only)
USE_MCP_FOR_FINANCIAL_DATA=false
```

### Change MCP Server

```env
# Default (recommended)
MCP_SERVER_COMMAND=python
MCP_SERVER_ARGS=-m,uv,tool,run,mcp-server-fetch

# Alternative: Use uvx directly
MCP_SERVER_COMMAND=uvx
MCP_SERVER_ARGS=mcp-server-fetch
```

## Future MCP Enhancements

Potential areas to expand MCP usage:

1. **SEC Filings**: Use MCP to fetch and parse SEC documents
2. **Economic Data**: Fetch FRED data through MCP
3. **News Aggregation**: Use MCP to scrape multiple news sources
4. **Social Sentiment**: Use MCP for Reddit/Twitter scraping
5. **Real-time Data**: WebSocket connections through MCP

## Summary

**MCP is currently used for:**
- ✓ Stock quotes (current prices)
- ✓ Historical price data
- ✓ As primary data source with automatic fallback

**MCP is NOT used for:**
- ✗ Email sending (uses SMTP)
- ✗ News fetching (uses NewsAPI)
- ✗ LLM operations (uses OpenAI/Gemini)
- ✗ Social media (uses direct APIs)

The current implementation provides a good balance between MCP integration and direct API usage, with automatic fallback ensuring reliability.
