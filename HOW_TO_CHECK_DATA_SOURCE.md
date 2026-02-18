# How to Check if Data is from MCP or Direct API

## Method 1: Backend Console Logs (Most Reliable)

### When MCP is ENABLED:
```
✓ MCP client initialized: C:\Users\daksh\.local\bin\uvx.exe mcp-server-fetch
...
Trying MCP for AAPL...
✓ Successfully fetched from MCP
```

### When MCP is DISABLED (Current):
```
🚀 Starting Investment Research Platform...
(No MCP initialization message)
...
Trying Yahoo Finance for AAPL...
✓ Successfully fetched from Yahoo Finance
```

### During Stock Data Fetch:
```
[HISTORICAL DATA] Fetching 365 days for COST...
  → Trying MCP...                          ← MCP attempt
✗ MCP sync get_historical_data failed     ← MCP failed
  → Trying Yahoo Finance...                ← Fallback
  ✓ Yahoo Finance: Got 270 data points    ← Success
```

## Method 2: Frontend "Data Sources" Panel

### Location:
Click the **"Data Sources"** button at the bottom of any stock analysis report.

### What You'll See:

#### Stock Quote Source:
```
📊 Market Data
   Alpha Vantage
   Real-time quote: $263.88
```

#### Historical Data Source:
```
📈 Historical Data
   Yahoo Finance
   270 days of historical prices
```

#### News Source:
```
📰 News Analysis
   NewsAPI.org
   7 recent headlines
```

#### Social Media Source:
```
💬 Social Sentiment
   Reddit Scraping (42 posts) + LLM Analysis
   42 Reddit posts analyzed
```

### If MCP Were Active:
```
📊 Market Data
   MCP Server (Yahoo Finance)    ← Would show "MCP Server"
   Real-time quote: $263.88
```

## Method 3: API Response JSON

### Check the Raw API Response:

Open browser DevTools (F12) → Network tab → Click on `/api/analyze/AAPL` → Response

Look for the `source` field:

```json
{
  "quote": {
    "symbol": "AAPL",
    "price": 263.88,
    "source": "Alpha Vantage"    ← Direct API
  },
  "chart_data": {
    "timestamps": [...],
    "close": [...],
    "source": "Yahoo Finance"     ← Direct API
  },
  "news_summary": {
    "headlines": [...],
    "source": "NewsAPI.org"       ← Direct API
  },
  "social_pulse": {
    "sentiment": "Neutral",
    "source": "Reddit Scraping (42 posts) + LLM Analysis"
  }
}
```

### If MCP Were Active:
```json
{
  "quote": {
    "source": "MCP Server (Yahoo Finance)"    ← MCP
  },
  "chart_data": {
    "source": "MCP Server (Yahoo Finance)"    ← MCP
  }
}
```

## Method 4: Check Configuration File

### Open `backend/.env`:

```env
USE_MCP_FOR_FINANCIAL_DATA=false    ← MCP is DISABLED
```

If it says `true`, MCP is enabled (but may still fall back to direct APIs if it fails).

## Method 5: Test with curl

### Run this command:
```bash
curl http://127.0.0.1:5000/api/analyze/AAPL
```

### Look for the `source` field in the response:
```json
{
  "quote": {
    "source": "Alpha Vantage"    ← Direct API
  }
}
```

## Quick Reference Table

| Indicator | MCP Enabled & Working | MCP Enabled but Failed | MCP Disabled |
|-----------|----------------------|----------------------|--------------|
| **Console Log** | `✓ MCP client initialized`<br>`✓ Successfully fetched from MCP` | `✓ MCP client initialized`<br>`✗ MCP sync failed`<br>`✓ Successfully fetched from Yahoo Finance` | No MCP messages |
| **Source Field** | `"MCP Server (Yahoo Finance)"` | `"Yahoo Finance"` or `"Alpha Vantage"` | `"Yahoo Finance"` or `"Alpha Vantage"` |
| **Data Sources Panel** | Shows "MCP Server" | Shows "Yahoo Finance", "Alpha Vantage", etc. | Shows "Yahoo Finance", "Alpha Vantage", etc. |
| **Speed** | ~2-3 seconds | ~3-4 seconds (MCP attempt + fallback) | ~1-2 seconds (direct) |

## Current Status Check

### Run this command to see current status:
```bash
cd backend
python -c "from config import USE_MCP_FOR_FINANCIAL_DATA; print(f'MCP Enabled: {USE_MCP_FOR_FINANCIAL_DATA}')"
```

### Expected Output:
```
MCP Enabled: False
```

## Live Example

### 1. Start the backend server:
```bash
cd backend
python app.py
```

### 2. Watch the console output:
```
🚀 Starting Investment Research Platform...
(No MCP initialization = MCP is disabled)
```

### 3. Make a request:
```bash
curl http://127.0.0.1:5000/api/analyze/AAPL
```

### 4. Check the console:
```
[HISTORICAL DATA] Fetching 365 days for AAPL...
  → Trying Yahoo Finance...        ← Direct API (no MCP attempt)
  ✓ Yahoo Finance: Got 270 data points
```

### 5. Check the response:
```json
{
  "chart_data": {
    "source": "Yahoo Finance"      ← Direct API
  }
}
```

## Summary

**Currently, your data is coming from:**
- ✅ **Yahoo Finance** (historical data)
- ✅ **Alpha Vantage** (stock quotes)
- ✅ **NewsAPI.org** (news headlines)
- ✅ **Reddit** (social media posts)
- ✅ **OpenAI GPT-4o-mini** (sentiment analysis)

**NOT from MCP** because it's disabled in `.env`.

## To Enable MCP and Test

1. Edit `backend/.env`:
   ```env
   USE_MCP_FOR_FINANCIAL_DATA=true
   ```

2. Restart server:
   ```bash
   cd backend
   python app.py
   ```

3. Watch console for:
   ```
   ✓ MCP client initialized: C:\Users\daksh\.local\bin\uvx.exe mcp-server-fetch
   ```

4. Make a request and check console:
   ```
   Trying MCP for AAPL...
   ✗ MCP sync get_stock_quote failed: (error message)
   Trying Yahoo Finance for AAPL...
   ✓ Successfully fetched from Yahoo Finance
   ```

5. Check the `source` field in response - it will show which source actually worked.
