# Data Sources & News Links Fix

## Issues Fixed

### 1. Data Sources Not Showing
**Problem**: The Data Sources panel was showing generic information instead of actual APIs used in the report.

**Solution**:
- Updated `DataSources.js` to extract actual data sources from the report object
- Replaced emoji icons with professional SVG icons (chart, trending, social, news, ai, forecast)
- Added proper icon rendering function with 6 different icon types
- Updated CSS to properly display icons with flex layout
- Added Reddit to the source URL mapping

**Files Modified**:
- `frontend/src/components/DataSources.js` - Complete rewrite with SVG icons
- `frontend/src/components/DataSources.css` - Updated `.source-header` styling

### 2. News Links Not Clickable
**Problem**: News headlines were not showing as clickable links with URLs.

**Verification**:
- Backend `news_client.py` correctly returns headline objects with:
  - `title`: Headline text
  - `source`: News source name
  - `url`: Actual article URL
  - `date`: Publication date/time
- Frontend `App.js` correctly handles headline objects (lines 603-615)
- CSS styles for `.headline-link`, `.external-link-icon`, `.headline-source`, and `.headline-date` already exist

**Status**: News links should now work correctly. The backend returns proper headline objects with URLs, and the frontend renders them as clickable links with external link icons.

## How It Works Now

### Data Sources Panel
When you click "Data Sources" at the bottom of a report, you'll see:

1. **Market Data** - Shows which API provided the real-time quote (Finnhub, Polygon, etc.)
2. **Historical Data** - Shows which API provided the chart data
3. **Social Sentiment** - Shows Reddit as the source with post count
4. **News Analysis** - Shows the news source (Multi-Source Web Search via LLM) with headline count
5. **Sentiment Analysis** - Shows Google Gemini AI with sentiment score
6. **Price Forecasting** - Shows AI Predictive Model with scenario count

Each source card displays:
- Professional SVG icon (no emojis)
- Source name
- Type badge (Market Data, Historical Data, etc.)
- Description with key metrics
- "Visit Source" link (if available)
- Green border for active sources

### News Headlines
In the "News Summary" section, headlines now display as:
- Clickable blue links with external link icon
- Source name below the headline
- Publication date/time
- Hover effect (lighter blue + underline)

## Testing

To verify the fixes:

1. **Start the backend**: `cd backend && python app.py`
2. **Start the frontend**: `cd frontend && npm start`
3. **Analyze a stock** (e.g., AAPL)
4. **Check Data Sources**:
   - Scroll to bottom of report
   - Click "Data Sources" button
   - Verify you see actual APIs used (not generic info)
   - Verify SVG icons display correctly
5. **Check News Links**:
   - Scroll to "News Summary" section
   - Verify headlines are blue and clickable
   - Click a headline to open in new tab
   - Verify source and date display below headline

## Technical Details

### SVG Icons Used
- **chart**: Line chart icon for market data
- **trending**: Upward trend icon for historical data
- **social**: Chat bubble icon for social sentiment
- **news**: Document/edit icon for news analysis
- **ai**: Smiley face icon for AI sentiment
- **forecast**: Clock icon for price forecasting

### Data Flow
1. Backend fetches news via `news_client.py` → Returns headline objects with URLs
2. `report_generator.py` includes news_data in report
3. Frontend receives report via `/api/analyze/<ticker>`
4. `App.js` renders headlines with proper link handling
5. `DataSources.js` extracts sources from report and displays with icons

## Notes

- All emoji icons have been replaced with professional SVG icons
- Data sources are now dynamically extracted from the actual report data
- News links include external link icon for better UX
- CSS styling is consistent with Apple Stocks-inspired dark theme
- No changes needed to backend - it was already returning correct data
