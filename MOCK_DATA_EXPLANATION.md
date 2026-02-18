# Why You're Seeing Mock Data

## TL;DR

You're seeing "Using Mock Data" because:
1. **OpenAI API is NOT used for stock prices** - it's only for text analysis
2. Your financial API keys (Finnhub, Polygon, etc.) are either invalid or rate-limited
3. Yahoo Finance (free fallback) might be blocked or rate-limited

## What Each API Does

### LLM APIs (Text Analysis Only)
- **Google Gemini** ✓ You have this
  - Used for: Sentiment analysis, news summaries, predictions
  - NOT used for: Stock prices, charts
  
- **OpenAI** ✓ You have this
  - Currently NOT used (Gemini is default)
  - Could be used for: Same as Gemini
  - NOT used for: Stock prices, charts

### Financial Data APIs (Stock Prices & Charts)
- **Finnhub** ✓ You have key: `d698um1r01qjmno4eqi0d698um1r01qjmno4eqig`
  - Should work for stocks
  - Crypto format: `BINANCE:BTCUSDT` (not `BTC-USD`)
  
- **Polygon** ✓ You have key: `rlSYQTfIqf1cc5Qj5ojym3ce8ilOgB9N`
  - Should work for stocks and crypto
  
- **Marketstack** ✓ You have key: `549f93b414e0d396f965c70f8a8ca829`
  - Limited to 100 requests/month (free tier)
  - Might be exhausted

- **Yahoo Finance** (Free, no key needed)
  - Fallback for everything
  - Should work for `BTC-USD`
  - Might be rate-limited

## Why Mock Data?

### Possible Reasons:

1. **API Keys Invalid**
   - Keys might be expired
   - Keys might be for wrong tier
   - Keys might have typos

2. **Rate Limits Exceeded**
   - Finnhub: 60 calls/minute
   - Polygon: Depends on tier
   - Marketstack: 100/month (free)
   - Yahoo: Soft limits, blocks after too many requests

3. **Network Issues**
   - Firewall blocking API requests
   - Proxy issues
   - DNS issues

4. **API Format Issues**
   - `BTC-USD` works on Yahoo
   - `BINANCE:BTCUSDT` works on Finnhub
   - System tries all, falls back to mock

## How to Fix

### Option 1: Use Yahoo Finance (Free, No Key)

Yahoo Finance should work without any API key. If it's not working:

1. Check backend logs when analyzing BTC-USD
2. Look for "Yahoo Finance error" messages
3. Might be temporarily rate-limited

### Option 2: Get Fresh API Keys

**For Crypto (BTC-USD, ETH-USD):**

1. **CoinGecko** (Best for crypto, free tier)
   ```
   Get key: https://www.coingecko.com/en/api/pricing
   Free: 10-50 calls/minute
   ```

2. **CryptoCompare** (Good for crypto)
   ```
   Get key: https://min-api.cryptocompare.com/
   Free: 100,000 calls/month
   ```

3. **Binance API** (Direct from exchange)
   ```
   Get key: https://www.binance.com/en/my/settings/api-management
   Free: High limits
   ```

**For Stocks:**

1. **Alpha Vantage** (You have this commented out)
   ```
   Uncomment: ALPHA_VANTAGE_API_KEY=OM5O4B7WNS5MZ7IE
   Free: 25 requests/day
   ```

2. **Financial Modeling Prep** (Best free tier)
   ```
   Get key: https://site.financialmodelingprep.com/developer/docs/
   Free: 250 requests/day
   ```

### Option 3: Check Current Keys

Run this test to see which APIs work:

```bash
cd backend
python -c "
from data_sources.multi_api_client import MultiAPIStockClient
client = MultiAPIStockClient()

# Test stock
print('Testing AAPL...')
quote = client.get_quote('AAPL')
print(f'Source: {quote.get(\"source\")}')
print(f'Price: {quote.get(\"price\")}')

# Test crypto
print('\nTesting BTC-USD...')
quote = client.get_quote('BTC-USD')
print(f'Source: {quote.get(\"source\")}')
print(f'Price: {quote.get(\"price\")}')
"
```

### Option 4: Enable Alpha Vantage

You have an Alpha Vantage key commented out. Uncomment it:

```env
# Change this:
#ALPHA_VANTAGE_API_KEY=OM5O4B7WNS5MZ7IE

# To this:
ALPHA_VANTAGE_API_KEY=OM5O4B7WNS5MZ7IE
```

Then restart the backend.

## Mock Data is OK for Testing

The mock data includes realistic prices for:
- Stocks: AAPL ($175), MSFT ($380), NVDA ($720), etc.
- Crypto: BTC-USD ($95,000), ETH-USD ($3,500)
- Indices: ^GSPC ($5,800), ^DJI ($42,000)

All features work with mock data:
✓ Charts (simulated historical data)
✓ Analysis
✓ Predictions
✓ Sentiment
✓ News

Only difference: Prices aren't real-time.

## Recommended Solution

### For Production Use:

1. **Get CoinGecko API key** (for crypto)
   - Free tier: 10-50 calls/minute
   - Supports BTC-USD, ETH-USD, etc.
   - https://www.coingecko.com/en/api/pricing

2. **Get Financial Modeling Prep key** (for stocks)
   - Free tier: 250 requests/day
   - Best free stock API
   - https://site.financialmodelingprep.com/developer/docs/

3. **Keep Yahoo Finance as fallback**
   - Already configured
   - No key needed
   - Works for everything

### For Development/Testing:

Mock data is fine! It's realistic and all features work.

## Summary

**Current Status:**
- ✓ Gemini API working (for AI analysis)
- ✓ OpenAI API available (not used)
- ✗ Financial APIs not working (hence mock data)
- ✓ BTC-USD and ETH-USD in watchlist
- ✓ All features functional with mock data

**To Get Real Data:**
1. Test current API keys (see Option 3 above)
2. Or get fresh keys (CoinGecko + FMP recommended)
3. Or just use mock data for now (it works!)

**OpenAI Note:**
OpenAI is for text generation, not stock prices. Even with OpenAI, you'd still need financial APIs for price data.
