# Quick Fix: Get Real Data for BTC-USD

## You CAN See BTC-USD!

Looking at your screenshot, **BTC-USD and ETH-USD ARE in your watchlist!** ✓

The issue is just that it's using mock data instead of real prices.

## Why Mock Data?

**OpenAI is NOT for stock prices!** It's only for text analysis (summaries, sentiment).

For stock/crypto prices, you need **financial data APIs**:
- Finnhub (you have this)
- Polygon (you have this)  
- Yahoo Finance (free, no key needed)

These APIs are either:
1. Not working properly
2. Rate-limited
3. Using wrong format for crypto

## Quick Fix: Uncomment Alpha Vantage

You have an Alpha Vantage key that's commented out!

**In `backend/.env`, change line 38:**

```env
# FROM THIS:
#ALPHA_VANTAGE_API_KEY=OM5O4B7WNS5MZ7IE

# TO THIS:
ALPHA_VANTAGE_API_KEY=OM5O4B7WNS5MZ7IE
```

Then restart backend:
```bash
cd backend
python app.py
```

## Better Fix: Get CoinGecko (Best for Crypto)

1. Go to: https://www.coingecko.com/en/api/pricing
2. Sign up for free tier (10-50 calls/minute)
3. Get API key
4. Add to `.env`:
   ```env
   COINGECKO_API_KEY=your_key_here
   ```

## Test Your Current APIs

Run this to see which APIs work:

```bash
cd backend
python -c "from data_sources.multi_api_client import MultiAPIStockClient; c = MultiAPIStockClient(); print(c.get_quote('BTC-USD'))"
```

## Mock Data is Fine for Now

The mock data is realistic:
- BTC-USD: $95,000
- ETH-USD: $3,500
- All features work
- Just not real-time

## Summary

1. ✓ **BTC-USD IS in your watchlist** (see your screenshot!)
2. ✗ **Using mock data** because financial APIs aren't working
3. ✓ **OpenAI key is there** but it's for text, not prices
4. 🔧 **Quick fix**: Uncomment Alpha Vantage key
5. 🔧 **Better fix**: Get CoinGecko API key

The app is working correctly - you just need real-time data APIs configured!
