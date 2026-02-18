# SEC Filing Integration Guide

## Overview
The Investment Research Platform integrates with the SEC EDGAR database to fetch 10-K and 10-Q filings for fundamental analysis.

## How It Works

### 1. CIK Lookup
The system first converts the stock ticker to a CIK (Central Index Key):
- **Method 1**: SEC's company_tickers.json API (most reliable)
- **Method 2**: SEC EDGAR search page (fallback)

### 2. Filing Retrieval
Once CIK is found:
- Searches for latest 10-K filing (annual report)
- Falls back to 10-Q (quarterly report) if 10-K unavailable
- Extracts Risk Factors and MD&A sections

### 3. Text Extraction
Parses HTML filings to extract:
- **Risk Factors**: Key business risks
- **MD&A**: Management's Discussion and Analysis

## Common Issues

### Issue 1: "No filings found"
**Causes:**
- Company doesn't file with SEC (foreign companies, private companies)
- Ticker symbol incorrect or not recognized
- Recent IPO with no filings yet

**Solutions:**
- Verify ticker symbol is correct
- Check if company is US-based and publicly traded
- Try alternative ticker (e.g., class A vs class B shares)

### Issue 2: "SEC filing data temporarily unavailable"
**Causes:**
- SEC website rate limiting
- Network connectivity issues
- SEC website maintenance
- Invalid User-Agent header

**Solutions:**
- Wait a few minutes and try again
- Check internet connection
- SEC typically performs maintenance on weekends
- The system will show fallback message with guidance

### Issue 3: Rate Limiting
**SEC Rate Limits:**
- 10 requests per second per IP address
- Exceeding this results in 403 errors

**Built-in Protections:**
- 0.1 second delay between requests
- Proper User-Agent header
- Timeout handling

## Supported Companies

### ✅ Will Work
- US publicly traded companies (NYSE, NASDAQ)
- Companies that file 10-K/10-Q with SEC
- Most major US corporations

### ❌ Won't Work
- Foreign companies (unless they file with SEC)
- Private companies
- Companies that only file other forms
- Very recent IPOs (< 1 year)

## Examples

### Companies with Good SEC Data
- AAPL (Apple Inc.)
- MSFT (Microsoft Corporation)
- GOOGL (Alphabet Inc.)
- TSLA (Tesla Inc.)
- AMZN (Amazon.com Inc.)
- META (Meta Platforms Inc.)
- NVDA (NVIDIA Corporation)

### Companies with Limited/No SEC Data
- Foreign companies trading as ADRs
- Recently IPO'd companies
- SPACs before merger completion
- Private companies

## Fallback Behavior

When SEC data is unavailable, the system provides:
- Generic risk factor information
- Guidance to check SEC EDGAR directly
- Link to sec.gov for manual lookup

## Manual SEC Lookup

If automated retrieval fails:

1. Visit https://www.sec.gov/edgar/searchedgar/companysearch.html
2. Enter ticker symbol or company name
3. Look for latest 10-K or 10-Q filing
4. Click "Documents" button
5. Open the main HTML document
6. Search for "Risk Factors" and "MD&A" sections

## Technical Details

### User-Agent Requirement
SEC requires a proper User-Agent header:
```
User-Agent: InvestmentResearch research@example.com
```

### API Endpoints Used
1. **Company Tickers JSON**: `https://www.sec.gov/files/company_tickers.json`
2. **EDGAR Search**: `https://www.sec.gov/cgi-bin/browse-edgar`
3. **Filing Documents**: Various EDGAR document URLs

### Timeout Settings
- CIK lookup: 10 seconds
- Filing retrieval: 10 seconds
- Document parsing: 10 seconds

### Text Extraction
- Risk Factors: Up to 1,500 characters
- MD&A: Up to 1,500 characters
- Regex-based section detection
- HTML parsing with BeautifulSoup

## Troubleshooting Steps

### Step 1: Check Backend Logs
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

### Step 2: Verify Company Files with SEC
1. Go to https://www.sec.gov/edgar/searchedgar/companysearch.html
2. Search for the ticker
3. Confirm 10-K or 10-Q filings exist

### Step 3: Check Rate Limiting
If you see 403 errors:
- Wait 1-2 minutes
- Reduce request frequency
- Check if IP is blocked (rare)

### Step 4: Test with Known Good Ticker
Try AAPL or MSFT to verify system is working

## Improvements in Latest Version

### Enhanced CIK Lookup
- Primary method uses SEC's JSON API
- Fallback to HTML scraping
- Better error messages

### Better Error Handling
- Graceful fallback when data unavailable
- Informative error messages
- Timeout protection

### Rate Limit Protection
- Built-in delays between requests
- Proper headers to identify application
- Retry logic for transient failures

## Future Enhancements

- [ ] Cache CIK lookups to reduce requests
- [ ] Support for 8-K filings (current events)
- [ ] Proxy filing data (DEF 14A)
- [ ] Insider trading data (Form 4)
- [ ] More detailed financial statement parsing
- [ ] Historical filing comparison
- [ ] Automatic filing date tracking

## API Response Format

```json
{
  "fundamental_core": {
    "risk_factors": "Text from Risk Factors section...",
    "mda": "Text from MD&A section..."
  }
}
```

Or on error:
```json
{
  "fundamental_core": {
    "error": "No filings found"
  }
}
```

Or with fallback:
```json
{
  "fundamental_core": {
    "risk_factors": "SEC filing data temporarily unavailable for AAPL. Common risks include...",
    "mda": "Management discussion and analysis not available. For detailed financial analysis..."
  }
}
```

## Best Practices

1. **Don't Spam**: Respect SEC rate limits
2. **Cache Results**: Store filing data to avoid repeated requests
3. **Handle Errors**: Always check for error responses
4. **Provide Context**: Show users when data is unavailable
5. **Link to Source**: Direct users to SEC EDGAR for full filings

## Resources

- **SEC EDGAR**: https://www.sec.gov/edgar.shtml
- **EDGAR Search**: https://www.sec.gov/edgar/searchedgar/companysearch.html
- **SEC Developer Resources**: https://www.sec.gov/developer
- **Company Tickers JSON**: https://www.sec.gov/files/company_tickers.json

## Support

If SEC filing retrieval consistently fails:
1. Check backend logs for specific errors
2. Verify ticker symbol is correct
3. Confirm company files with SEC
4. Check network connectivity
5. Try again after a few minutes (rate limiting)
6. Use manual SEC EDGAR lookup as fallback
