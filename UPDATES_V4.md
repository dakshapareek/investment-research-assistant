# Investment Research Platform - Updates V4

## Changes Made

### 1. Updated Gemini Model
- Changed all Gemini model references from `gemini-1.5-flash` to `gemini-flash-latest`
- Updated files:
  - `backend/data_sources/llm_sentiment.py`
  - `backend/data_sources/social_client.py`
  - `backend/deep_analysis.py`
  - `backend/data_sources/news_client.py`
  - `backend/data_sources/predictive_analysis.py`

### 2. Removed Macro Tailwinds Section
- Removed BLS (Bureau of Labor Statistics) integration
- Removed CPI and unemployment data display
- Removed macro economic analysis from rating calculation
- Updated files:
  - `backend/report_generator.py` - Removed BLSClient import and macro data methods
  - `frontend/src/App.js` - Removed Macro Tailwinds UI section
  - `backend/app.py` - Removed BLS imports

### 3. Removed SEC Filing Section
- Removed SEC EDGAR integration
- Removed 10-K/10-Q filing analysis
- Removed fundamental core section from reports
- Updated files:
  - `backend/report_generator.py` - Removed SECClient import and SEC data methods
  - `frontend/src/App.js` - Removed SEC Filings UI section
  - `backend/app.py` - Removed SEC imports

### 4. Enhanced Social Pulse with Web Scraping
- Implemented Reddit web scraping without login using public JSON API
- Scrapes from r/stocks, r/wallstreetbets, r/investing, r/StockMarket
- Uses LLM (Google Gemini) to analyze scraped social media data
- No longer requires Reddit API credentials (PRAW)
- Added placeholder for Twitter/X scraping (limited due to platform restrictions)
- Updated files:
  - `backend/data_sources/social_client.py` - Complete rewrite with web scraping
  - `frontend/src/components/DataSources.js` - Updated to show web scraping source

## New Features

### Reddit Web Scraping
- Uses Reddit's public JSON API (no authentication required)
- Scrapes recent posts mentioning the ticker from multiple subreddits
- Extracts post titles, scores, comments, and URLs
- Rate-limited to respect Reddit's servers (1 second delay between requests)
- Combines scraped data with LLM analysis for comprehensive sentiment

### Simplified Data Sources
The platform now focuses on:
1. **Stock Data** - Real-time quotes and historical prices from multiple APIs
2. **Social Pulse** - Reddit web scraping + LLM analysis
3. **News Analysis** - Web search + LLM-powered sentiment
4. **AI Predictions** - Technical analysis and price forecasting

## Configuration

### Required API Keys
- `GOOGLE_API_KEY` - For LLM analysis, web search, and sentiment (highly recommended)
- At least one financial API key:
  - `FINANCIAL_MODELING_PREP_API_KEY`
  - `ALPHA_VANTAGE_API_KEY`
  - `FINNHUB_API_KEY`
  - `POLYGON_API_KEY`

### No Longer Required
- ~~`REDDIT_CLIENT_ID`~~ - Removed (using web scraping instead)
- ~~`REDDIT_CLIENT_SECRET`~~ - Removed (using web scraping instead)
- ~~`BLS_API_KEY`~~ - Removed (macro section removed)

## Benefits

1. **Simpler Setup** - Fewer API keys required
2. **No Reddit Login** - Web scraping works without authentication
3. **Focused Analysis** - Streamlined to core investment data
4. **Better Performance** - Removed slow BLS and SEC API calls
5. **More Reliable** - Web scraping is more stable than Reddit API

## How It Works

### Social Pulse Flow
1. User requests analysis for a ticker
2. System scrapes Reddit's public JSON endpoints for recent posts
3. Scraped posts are sent to Google Gemini for sentiment analysis
4. LLM generates comprehensive 4-paragraph analysis
5. Results displayed with sentiment score and confidence level

### Data Collection
- Reddit posts are scraped from public JSON API
- No login or authentication required
- Respects rate limits with delays
- Falls back to LLM web search if scraping fails

## Next Steps

To use the updated platform:

1. **Update your `.env` file:**
   ```bash
   # Required
   GOOGLE_API_KEY=your_gemini_api_key
   
   # At least one financial API
   FINANCIAL_MODELING_PREP_API_KEY=your_fmp_key
   # OR
   ALPHA_VANTAGE_API_KEY=your_av_key
   
   # No longer needed (can remove)
   # REDDIT_CLIENT_ID=...
   # REDDIT_CLIENT_SECRET=...
   ```

2. **Restart the backend server:**
   ```bash
   cd backend
   python app.py
   ```

3. **Test the new features:**
   - Search for a stock (e.g., AAPL)
   - Check the Social Pulse section for scraped Reddit data
   - Verify the source shows "Web Scraping + LLM"

## Technical Details

### Web Scraping Implementation
- Uses `requests` library to fetch Reddit JSON
- Parses public search results from subreddits
- Extracts structured data (title, score, comments, URL)
- Implements rate limiting to avoid being blocked
- Graceful fallback to LLM web search if scraping fails

### LLM Integration
- Google Gemini analyzes scraped posts
- Generates sentiment scores (-1.0 to 1.0)
- Provides confidence levels (0 to 1)
- Creates detailed 4-paragraph summaries
- Identifies key discussion topics

## Troubleshooting

### If Social Pulse shows "Fallback Analysis"
- Check that `GOOGLE_API_KEY` is configured
- Verify Gemini API is working
- Check internet connection for web scraping

### If scraping fails
- Reddit may be rate-limiting your IP
- Try again after a few minutes
- System will automatically fall back to LLM web search

## Files Modified

### Backend
- `backend/report_generator.py` - Removed BLS and SEC, simplified rating
- `backend/data_sources/social_client.py` - Complete rewrite with web scraping
- `backend/app.py` - Updated imports and logging
- `backend/data_sources/llm_sentiment.py` - Updated model name
- `backend/data_sources/news_client.py` - Updated model name
- `backend/data_sources/predictive_analysis.py` - Updated model name
- `backend/deep_analysis.py` - Updated model name

### Frontend
- `frontend/src/App.js` - Removed Macro and SEC sections
- `frontend/src/components/DataSources.js` - Updated data sources list

## Summary

This update simplifies the platform by removing complex integrations (BLS, SEC, Reddit API) and replacing them with more reliable web scraping and LLM analysis. The result is a faster, simpler, and more maintainable investment research tool that focuses on the most valuable data sources.
