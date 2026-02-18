# Investment Research Platform - Updates V8

## New Features Added

### 1. Clickable News Links
News headlines now include actual URLs that users can click to read the full articles.

**Features:**
- External link icon next to each headline
- Opens in new tab
- Source attribution displayed
- Date information when available
- Hover effects for better UX

**Implementation:**
- Backend LLM now searches for and returns actual URLs
- Frontend displays headlines as clickable links
- Fallback to plain text if URL not available

### 2. "Keep an Eye On" Box
Added a prominent box with popular stocks for quick analysis.

**Features:**
- Displays 3 popular stocks: AAPL (Apple), NVDA (NVIDIA), TSLA (Tesla)
- One-click analysis
- Eye icon for visual appeal
- Disabled state during analysis
- Hover effects with gradient background

**Why These Stocks:**
- **AAPL (Apple)**: Most valuable company, tech leader
- **NVDA (NVIDIA)**: AI/GPU leader, high growth
- **TSLA (Tesla)**: EV leader, high volatility, popular with retail

## Technical Implementation

### Backend Changes

#### news_client.py
Updated the LLM prompt to request actual URLs:

```python
"headlines": [
    {
        "title": "headline text",
        "source": "source name",
        "url": "https://actual-url.com/article",
        "date": "date"
    },
    ...
]
```

The LLM now searches for real news articles and returns working URLs.

### Frontend Changes

#### App.js

**News Section Update:**
```javascript
{report.news_summary.headlines.map((headline, idx) => {
  if (typeof headline === 'object' && headline.url) {
    return (
      <li key={idx} className="headline-item">
        <a href={headline.url} target="_blank" rel="noopener noreferrer">
          {headline.title}
          <svg className="external-link-icon">...</svg>
        </a>
        <span className="headline-source">{headline.source}</span>
        <span className="headline-date">{headline.date}</span>
      </li>
    );
  }
})}
```

**Keep an Eye On Box:**
```javascript
<div className="keep-eye-on-box">
  <h3>
    <svg>...</svg>
    Keep an Eye On
  </h3>
  <div className="popular-stocks">
    <button onClick={() => analyzeStock('AAPL')}>
      <span className="chip-symbol">AAPL</span>
      <span className="chip-name">Apple</span>
    </button>
    // ... more stocks
  </div>
</div>
```

#### App.css

**New Styles Added:**
- `.keep-eye-on-box` - Container with gradient background
- `.stock-chip` - Individual stock buttons
- `.headline-link` - Clickable news links
- `.external-link-icon` - Link indicator icon
- `.headline-source` - Source attribution
- `.headline-date` - Date display

## User Experience

### News Links Flow
1. User analyzes a stock
2. News section displays headlines
3. Each headline is clickable with external link icon
4. Click opens article in new tab
5. Source and date shown below headline

### Keep an Eye On Flow
1. User sees "Keep an Eye On" box below search
2. Three popular stocks displayed as chips
3. Click any stock to instantly analyze
4. Button disabled during analysis
5. Results appear below

## Visual Design

### Keep an Eye On Box
- **Background**: Gradient purple/blue with transparency
- **Border**: Glowing purple border
- **Icon**: Eye icon in purple
- **Chips**: Card-style buttons with hover effects

### News Links
- **Color**: Blue (#3b82f6) for links
- **Hover**: Lighter blue with underline
- **Icon**: External link arrow
- **Metadata**: Gray text for source/date

## Benefits

### For Users
1. **Direct Access**: Click to read full articles
2. **Source Verification**: See where news comes from
3. **Quick Analysis**: One-click popular stocks
4. **Better Context**: Date information for news
5. **Improved Trust**: Real URLs from credible sources

### For Platform
1. **Transparency**: Users can verify news sources
2. **Engagement**: Quick access to popular stocks
3. **Credibility**: Real links to major outlets
4. **User Retention**: Easy navigation to trending stocks

## News Sources

The LLM searches and returns URLs from:
- Bloomberg
- Reuters
- CNBC
- MarketWatch
- Wall Street Journal
- Financial Times
- Seeking Alpha
- Yahoo Finance
- Forbes
- Business Insider
- And more...

## Popular Stocks Selection

### AAPL (Apple)
- Market cap: ~$3 trillion
- Sector: Technology
- Why: Most valuable company, stable, widely followed

### NVDA (NVIDIA)
- Market cap: ~$2 trillion
- Sector: Semiconductors/AI
- Why: AI boom leader, high growth, institutional favorite

### TSLA (Tesla)
- Market cap: ~$600 billion
- Sector: Automotive/Energy
- Why: EV leader, high volatility, retail favorite

## Customization Options

### Adding More Stocks
To add more popular stocks, edit `App.js`:

```javascript
<button onClick={() => analyzeStock('MSFT')}>
  <span className="chip-symbol">MSFT</span>
  <span className="chip-name">Microsoft</span>
</button>
```

### Changing Stock Selection
Consider adding:
- **MSFT**: Microsoft (tech giant)
- **GOOGL**: Google (search/AI)
- **AMZN**: Amazon (e-commerce)
- **META**: Meta (social media)
- **BTC-USD**: Bitcoin (crypto)

## Error Handling

### News Links
- If URL not available, displays as plain text
- Graceful fallback to string headlines
- No broken links

### Keep an Eye On
- Buttons disabled during analysis
- Prevents multiple simultaneous requests
- Visual feedback on disabled state

## Future Enhancements

Potential additions:
1. **Trending Stocks**: Dynamic list based on volume/mentions
2. **Sector Rotation**: Show hot sectors
3. **Earnings Calendar**: Upcoming earnings
4. **Customizable Watchlist**: User-selected favorites
5. **News Filtering**: Filter by source/date
6. **Social Sharing**: Share news links
7. **Bookmark Headlines**: Save for later

## Testing

### Test News Links
1. Analyze any stock (e.g., AAPL)
2. Scroll to News Summary section
3. Click any headline link
4. Should open article in new tab
5. Verify URL is from credible source

### Test Keep an Eye On
1. Look for box below search bar
2. Click AAPL chip
3. Should analyze Apple stock
4. Button should be disabled during analysis
5. Try other stocks (NVDA, TSLA)

## Accessibility

### News Links
- Proper `rel="noopener noreferrer"` for security
- External link icon for visual indication
- Keyboard accessible
- Screen reader friendly

### Stock Chips
- Disabled state properly indicated
- Keyboard navigation supported
- Clear labels (symbol + name)
- Focus states visible

## Performance

### News Links
- No performance impact
- Links load instantly
- External sites load separately

### Keep an Eye On
- Minimal overhead
- Same analysis as search
- No additional API calls

## Files Modified

### Backend
- `backend/data_sources/news_client.py` - Updated prompt to request URLs

### Frontend
- `frontend/src/App.js` - Added Keep an Eye On box, updated news display
- `frontend/src/App.css` - Added styles for new features

## Summary

This update adds two major UX improvements:
1. **Clickable news links** with source attribution for transparency and easy access to full articles
2. **"Keep an Eye On" box** with popular stocks (AAPL, NVDA, TSLA) for quick one-click analysis

Users can now verify news sources by clicking through to original articles and quickly analyze trending stocks without typing. The interface is more engaging, transparent, and user-friendly.
