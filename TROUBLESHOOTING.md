# 🔧 Troubleshooting Guide

## Stock Price Issues

### Yahoo Finance API Failing

**Symptoms:**
- Backend logs show "Yahoo Finance quote failed for [TICKER], using fallback"
- Prices shown are mock/demo data
- Charts display but with simulated data

**Causes:**
1. Yahoo Finance rate limiting
2. Network connectivity issues
3. Yahoo Finance API changes
4. Firewall/proxy blocking requests

**Solutions:**

#### Option 1: Use Alternative APIs (Recommended)

Configure one of these free alternatives in `backend/.env`:

**Alpha Vantage** (Free, 25 requests/day):
```bash
ALPHA_VANTAGE_API_KEY=your_key_here
```
Get key: https://www.alphavantage.co/support/#api-key

**Finnhub** (Free, 60 calls/minute):
```bash
FINNHUB_API_KEY=your_key_here
```
Get key: https://finnhub.io/register

**Polygon.io** (Free tier available):
```bash
POLYGON_API_KEY=your_key_here
```
Get key: https://polygon.io/dashboard/signup

#### Option 2: Wait and Retry

Yahoo Finance has rate limits. Wait 5-10 minutes and try again.

#### Option 3: Use Mock Data

The app automatically falls back to realistic mock data when APIs fail. This is useful for:
- Testing the UI
- Demonstrating features
- Development without API keys

Mock data includes:
- Realistic price movements (random walk)
- Proper market cap calculations
- Volume data
- P/E ratios

### Incorrect Price Values

**Issue:** Chart shows correct prices but UI stats show wrong values

**Fix Applied:** 
- Backend now returns `open` price separately
- Frontend uses `quote.open` instead of calculating from current price
- Fallback calculation: `price - change` if open not available

**Verify Fix:**
1. Restart backend: `python backend/app.py`
2. Refresh frontend
3. Analyze a stock
4. Check that Open, High, Low values are different

### Currency Display

**Issue:** Prices showing in wrong currency (₹ instead of $)

**Fix Applied:**
- All currency symbols changed to $ (USD)
- Market cap formatting uses $ prefix
- Tooltip displays $ for prices

**US Stocks Supported:**
- NYSE stocks (e.g., JPM, WMT, V)
- NASDAQ stocks (e.g., AAPL, MSFT, GOOGL)
- All major US exchanges

## Chart Issues

### Charts Not Displaying

**Symptoms:**
- Empty chart area
- "No chart data available" message
- Console errors

**Solutions:**

1. **Check Backend Connection**
```bash
# Test backend is running
curl http://localhost:5000/api/watchlist
```

2. **Check Browser Console**
- Open DevTools (F12)
- Look for errors in Console tab
- Check Network tab for failed requests

3. **Verify Data Structure**
- Backend should return `chart_data` with `timestamps` and `close` arrays
- Check backend logs for errors

4. **Clear Browser Cache**
- Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Clear site data in DevTools

### Interactive Features Not Working

**Issue:** Time range buttons not responding

**Solutions:**
1. Check React state updates in browser DevTools
2. Verify `timeRange` state is changing
3. Check console for JavaScript errors

## API Configuration Issues

### "API key invalid" Error

**Solutions:**
1. Check `.env` file for typos
2. Ensure no extra spaces around keys
3. Verify key format (e.g., OpenAI keys start with `sk-`)
4. Test key in provider's dashboard
5. Regenerate key if needed

### Reddit API Not Working

**Common Issues:**

1. **Wrong credentials**
   - Client ID is under app name (short string)
   - Client Secret is longer string
   - User Agent must be set

2. **App type wrong**
   - Must be "script" type, not "web app"
   - Redirect URI: http://localhost:8080

3. **Rate limiting**
   - Free tier: 60 requests/minute
   - Wait and retry

### News API Issues

**Issue:** No news headlines showing

**Solutions:**
1. Verify API key in `.env`
2. Check free tier limits (100 requests/day)
3. Use alternative news sources
4. App works without news API (optional feature)

## Backend Issues

### "Module not found" Error

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Port Already in Use

**Error:** `Address already in use: 5000`

**Solutions:**

**Windows:**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

**Alternative:** Change port in `backend/app.py`:
```python
app.run(debug=True, port=5001)
```

### Import Errors

**Error:** `ImportError: cannot import name 'X'`

**Solutions:**
1. Check Python version: `python --version` (need 3.8+)
2. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
3. Check for circular imports
4. Verify file structure matches imports

## Frontend Issues

### "npm install" Fails

**Solutions:**
1. Delete `node_modules` and `package-lock.json`
2. Run `npm install` again
3. Try `npm install --legacy-peer-deps`
4. Update Node.js to latest LTS version

### Build Warnings

**Warning:** `'X' is defined but never used`

**Solution:** These are non-critical. App still works. To fix:
- Remove unused imports
- Use variables or remove them

### Blank Page After Build

**Solutions:**
1. Check browser console for errors
2. Verify backend is running
3. Check CORS settings
4. Clear browser cache

## Performance Issues

### Slow API Responses

**Causes:**
- Multiple API calls per request
- Rate limiting delays
- Network latency

**Solutions:**
1. Implement caching (future feature)
2. Use faster APIs (Finnhub, Polygon)
3. Reduce data fetching frequency
4. Enable only needed data sources

### High Memory Usage

**Solutions:**
1. Limit chart data points
2. Clear old data periodically
3. Restart backend server
4. Use production build for frontend

## Data Quality Issues

### Sentiment Analysis Not Accurate

**Causes:**
- Using rule-based analysis (keyword matching)
- Limited training data
- Bot activity on social media

**Solutions:**
1. Configure real LLM (OpenAI, Claude, Gemini)
2. Adjust keyword lists in `llm_sentiment.py`
3. Increase confidence thresholds
4. Filter bot posts more aggressively

### SEC Filings Not Loading

**Symptoms:**
- "No filings found" error
- "SEC filing data temporarily unavailable" message
- Risk Factors and MD&A sections show fallback text

**Causes:**
1. SEC EDGAR rate limiting (10 requests/second)
2. Company doesn't file with SEC (foreign/private companies)
3. Ticker symbol not recognized
4. Network connectivity issues
5. SEC website maintenance

**Solutions:**

#### Step 1: Verify Company Files with SEC
1. Visit https://www.sec.gov/edgar/searchedgar/companysearch.html
2. Search for your ticker symbol
3. Check if 10-K or 10-Q filings exist
4. If no filings found, company may not file with SEC

#### Step 2: Check Backend Logs
Look for messages like:
```
Fetching SEC filing for AAPL...
✓ Found CIK: 0000320193
✓ Successfully retrieved SEC filing
```

Or errors:
```
✗ Could not find CIK for XYZ
✗ SEC returned status 403
✗ No valid filings found
```

#### Step 3: Wait and Retry
- SEC has rate limits (10 requests/second)
- Wait 1-2 minutes if you see 403 errors
- Try again with a different ticker

#### Step 4: Use Manual Lookup
If automated retrieval fails:
1. Go to https://www.sec.gov/edgar/searchedgar/companysearch.html
2. Enter ticker symbol
3. Find latest 10-K or 10-Q
4. Read Risk Factors and MD&A sections manually

**Companies That Work:**
- ✅ US publicly traded companies (AAPL, MSFT, GOOGL, TSLA)
- ✅ Companies with recent 10-K/10-Q filings
- ❌ Foreign companies (unless they file with SEC)
- ❌ Private companies
- ❌ Very recent IPOs (< 1 year)

**See SEC_FILING_GUIDE.md for detailed information**

## Getting Help

### Check Logs

**Backend logs:**
```bash
# Run backend with verbose output
python backend/app.py
```

**Frontend logs:**
- Open browser DevTools (F12)
- Check Console tab
- Check Network tab for failed requests

### Common Log Messages

**"Yahoo Finance quote failed"**
- Normal when API is unavailable
- App uses fallback mock data
- Configure alternative APIs

**"Reddit API not configured"**
- Normal if Reddit credentials not set
- Social sentiment will show placeholder
- See API_SETUP_GUIDE.md

**"Generating report for [TICKER]"**
- Normal operation
- Report generation in progress

### Still Having Issues?

1. Check all markdown documentation files
2. Verify all prerequisites installed
3. Test with simple ticker (AAPL, MSFT)
4. Try with mock data (no API keys)
5. Check GitHub issues for similar problems

### Reset Everything

**Nuclear option** - start fresh:

```bash
# Backend
cd backend
rm -rf __pycache__
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install

# Restart both servers
```

## Best Practices

### Development
- Use mock data for UI testing
- Test with one ticker at a time
- Monitor API usage in dashboards
- Keep API keys in `.env` only

### Production
- Use paid API tiers for reliability
- Implement caching
- Set up monitoring
- Use production builds
- Enable rate limiting

### API Usage
- Respect rate limits
- Cache responses when possible
- Use multiple providers for redundancy
- Monitor costs regularly
