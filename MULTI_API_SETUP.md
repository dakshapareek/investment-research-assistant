# 🌐 Multi-API Stock Data Setup

The app now supports **multiple finance APIs** with automatic fallback for maximum reliability!

## 🎯 How It Works

The system tries APIs in this order until one succeeds:

1. **Financial Modeling Prep** (250 requests/day free) ⭐ Recommended
2. **Alpha Vantage** (25 requests/day free)
3. **Finnhub** (60 calls/minute free)
4. **Polygon.io** (5 calls/minute free)
5. **Yahoo Finance** (fallback, no key needed)
6. **Mock Data** (if all fail)

## 📊 API Comparison

| API | Free Tier | Best For | Setup Time |
|-----|-----------|----------|------------|
| **Financial Modeling Prep** | 250 req/day | US stocks, fundamentals | 2 min |
| **Alpha Vantage** | 25 req/day | Real-time data, indicators | 1 min |
| **Finnhub** | 60 req/min | High frequency updates | 2 min |
| **Polygon.io** | 5 req/min | Professional data | 2 min |
| **Yahoo Finance** | Unlimited* | Backup source | 0 min |

*Rate limited, may fail occasionally

## 🚀 Quick Setup (Recommended)

### Option 1: Financial Modeling Prep Only (Best)

1. Go to https://site.financialmodelingprep.com/developer/docs/
2. Sign up (free)
3. Copy your API key
4. Add to `backend/.env`:
```bash
FINANCIAL_MODELING_PREP_API_KEY=your_key_here
```

**Benefits:**
- 250 requests/day (enough for ~25 stocks analyzed)
- Comprehensive data (price, fundamentals, historical)
- Fast and reliable
- No credit card required

### Option 2: Alpha Vantage (Alternative)

1. Go to https://www.alphavantage.co/support/#api-key
2. Enter your email
3. Get instant API key
4. Add to `backend/.env`:
```bash
ALPHA_VANTAGE_API_KEY=your_key_here
```

**Benefits:**
- Instant setup (no signup)
- Real-time data
- Technical indicators
- 25 requests/day

### Option 3: Multiple APIs (Maximum Reliability)

Configure all APIs for automatic fallback:

```bash
# backend/.env
FINANCIAL_MODELING_PREP_API_KEY=your_fmp_key
ALPHA_VANTAGE_API_KEY=your_av_key
FINNHUB_API_KEY=your_finnhub_key
POLYGON_API_KEY=your_polygon_key
```

**Benefits:**
- If one API fails, automatically tries next
- Combined rate limits (250 + 25 + 60 = 335+ requests/day)
- Maximum uptime
- Best data quality

## 📝 Detailed Setup Instructions

### Financial Modeling Prep

**Free Tier:** 250 requests/day

1. Visit https://site.financialmodelingprep.com/developer/docs/
2. Click "Get Your Free API Key"
3. Fill in:
   - Email
   - Password
   - Name
4. Verify email
5. Copy API key from dashboard
6. Add to `.env`: `FINANCIAL_MODELING_PREP_API_KEY=your_key`

**Data Provided:**
- Real-time quotes
- Historical prices (30+ years)
- Fundamentals (P/E, EPS, Market Cap)
- 52-week high/low
- Volume data

### Alpha Vantage

**Free Tier:** 25 requests/day, 5 per minute

1. Visit https://www.alphavantage.co/support/#api-key
2. Enter email address
3. Receive API key instantly
4. Add to `.env`: `ALPHA_VANTAGE_API_KEY=your_key`

**Data Provided:**
- Real-time quotes
- Historical daily data
- Technical indicators
- Forex and crypto

### Finnhub

**Free Tier:** 60 API calls/minute

1. Visit https://finnhub.io/register
2. Sign up with email
3. Verify email
4. Copy API key from dashboard
5. Add to `.env`: `FINNHUB_API_KEY=your_key`

**Data Provided:**
- Real-time quotes
- Company news
- Earnings calendar
- High-frequency updates

### Polygon.io

**Free Tier:** 5 API calls/minute

1. Visit https://polygon.io/dashboard/signup
2. Sign up (free tier)
3. Navigate to API Keys
4. Copy your key
5. Add to `.env`: `POLYGON_API_KEY=your_key`

**Data Provided:**
- Previous day's data
- Aggregated bars
- Professional-grade data
- Options data (paid)

## 🔍 Testing Your Setup

### Test Single API

```bash
cd backend
python -c "
from data_sources.multi_api_client import MultiAPIStockClient
client = MultiAPIStockClient()
quote = client.get_quote('AAPL')
print(f'Price: ${quote[\"price\"]}')
print(f'Source: {quote[\"source\"]}')
"
```

### Test All APIs

Analyze a stock in the app and check backend logs:

```
Trying Financial Modeling Prep for AAPL...
✓ Successfully fetched from Financial Modeling Prep
```

## 📊 Data Source Indicator

The UI now shows which API provided the data:

```
AAPL Stock Analysis 📡 Financial Modeling Prep
```

This helps you:
- Verify data source
- Monitor API usage
- Debug issues
- Track reliability

## 🎯 Best Practices

### For Development
- Use Financial Modeling Prep (250 req/day)
- Test with 5-10 stocks
- Monitor rate limits

### For Production
- Configure all APIs for redundancy
- Implement caching (future feature)
- Monitor API dashboards
- Consider paid tiers for higher limits

### Rate Limit Management

**Daily Limits:**
- FMP: 250 requests
- Alpha Vantage: 25 requests
- Finnhub: Unlimited (60/min)
- Polygon: Unlimited (5/min)

**Tips:**
- Analyze stocks one at a time
- Don't refresh too frequently
- Use watchlist strategically
- Cache results when possible

## 🐛 Troubleshooting

### "All APIs failed" Message

**Causes:**
1. No API keys configured
2. Rate limits exceeded
3. Network issues
4. Invalid API keys

**Solutions:**
1. Configure at least one API key
2. Wait for rate limit reset
3. Check internet connection
4. Verify keys in provider dashboards

### Specific API Errors

**Financial Modeling Prep:**
- Error: "Invalid API key"
- Solution: Check key format, regenerate if needed

**Alpha Vantage:**
- Error: "Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute"
- Solution: Wait 1 minute between requests

**Finnhub:**
- Error: "You don't have access to this resource"
- Solution: Verify API key, check free tier limits

**Polygon:**
- Error: "Forbidden"
- Solution: Check API key, verify free tier access

### Backend Logs

Check which APIs are being tried:

```bash
cd backend
python app.py
```

Look for:
```
Trying Financial Modeling Prep for AAPL...
✓ Successfully fetched from Financial Modeling Prep
```

Or:
```
Trying Financial Modeling Prep for AAPL...
✗ Financial Modeling Prep failed: Invalid API key
Trying Alpha Vantage for AAPL...
✓ Successfully fetched from Alpha Vantage
```

## 💡 Pro Tips

1. **Start with FMP**: Best free tier (250 req/day)
2. **Add Alpha Vantage**: Good backup (25 req/day)
3. **Monitor usage**: Check API dashboards regularly
4. **Upgrade when needed**: Consider paid tiers for production
5. **Use mock data**: Great for UI testing without API calls

## 🔄 Fallback Behavior

The system automatically:
1. Tries each API in order
2. Skips APIs without keys
3. Falls back to next API on failure
4. Uses mock data if all fail
5. Logs which API succeeded

## 📈 Upgrade Paths

### When to Upgrade

- Analyzing >10 stocks/day → Upgrade FMP ($19/month)
- Need real-time data → Upgrade Alpha Vantage ($49/month)
- High-frequency updates → Upgrade Finnhub ($59/month)
- Professional trading → Upgrade Polygon ($199/month)

### Recommended Upgrades

**For Serious Investors:**
- Financial Modeling Prep Pro: $19/month
- 750 requests/day
- Real-time data
- All features

**For Traders:**
- Finnhub Starter: $59/month
- Unlimited requests
- Real-time WebSocket
- News and events

**For Professionals:**
- Polygon Starter: $199/month
- Real-time data
- Options data
- Historical data

## 🎉 Success!

Once configured, you'll see:
- Real stock prices (not mock data)
- Accurate market data
- Data source badges
- Reliable updates

The app automatically handles:
- API failures
- Rate limiting
- Data formatting
- Error recovery

No more "Yahoo Finance failed" messages! 🚀
