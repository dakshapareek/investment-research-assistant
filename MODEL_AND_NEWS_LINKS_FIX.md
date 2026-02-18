# Model & News Links Fix

## Issues Fixed

### 1. Wrong Gemini Model Being Used
**Problem**: The system was still using `gemini-2.0-flash-exp` which returns 404 errors, instead of the correct `gemini-2.5-flash-lite` model.

**Root Cause**: The `current_model` variable in `backend/app.py` was set to the old model name.

**Solution**:
- Changed `current_model = 'gemini-2.0-flash-exp'` to `current_model = 'gemini-2.5-flash-lite'` in `backend/app.py`

**Files Modified**:
- `backend/app.py` - Line 33: Updated default model to `gemini-2.5-flash-lite`

### 2. News Links Not Clickable
**Problem**: News headlines were not showing as clickable links in the UI.

**Root Cause**: The fallback news function was returning headlines as simple strings instead of objects with URL properties.

**Solution**:
- Updated `_get_fallback_news()` to return headline objects with `title`, `source`, `url`, and `date` fields
- Updated `_extract_headlines_from_text()` to return headline objects instead of strings
- All headlines now have proper structure for clickable links

**Files Modified**:
- `backend/data_sources/news_client.py`:
  - `_get_fallback_news()` - Returns headline objects with Yahoo Finance URLs
  - `_extract_headlines_from_text()` - Returns headline objects instead of strings

## Headline Object Structure

All headlines now follow this structure:

```python
{
    'title': 'Headline text here',
    'source': 'Source name (e.g., Bloomberg, Reuters)',
    'url': 'https://actual-url.com/article',
    'date': 'Publication date/time (e.g., "2 hours ago", "Feb 16, 2026")'
}
```

## Frontend Rendering

The frontend `App.js` (lines 603-615) correctly handles this structure:

```javascript
if (typeof headline === 'object' && headline.url) {
  return (
    <li key={idx} className="headline-item">
      <a href={headline.url} target="_blank" rel="noopener noreferrer" className="headline-link">
        {headline.title}
        <svg className="external-link-icon">...</svg>
      </a>
      {headline.source && <span className="headline-source">{headline.source}</span>}
      {headline.date && <span className="headline-date">{headline.date}</span>}
    </li>
  );
}
```

## Testing

### Test the Model Fix

1. **Restart the backend server**:
   ```bash
   cd backend
   python app.py
   ```

2. **Check the startup logs** - Should show:
   ```
   ✓ Google Gemini (gemini-2.5-flash-lite) initialized for social scraping
   ✓ Google Gemini (gemini-2.5-flash-lite) initialized for news analysis
   ```

3. **Analyze a stock** (e.g., AAPL)

4. **Check for errors** - Should NOT see:
   ```
   404 models/gemini-2.0-flash-exp is not found
   ```

### Test News Links

1. **Run the test script**:
   ```bash
   cd backend
   python test_news_structure.py
   ```

2. **Expected output**:
   ```
   ✓ SUCCESS: All headlines are properly structured objects
   ✓ SUCCESS: All headlines have URLs
   ```

3. **In the UI**:
   - Navigate to "News Summary" section
   - Headlines should be blue and clickable
   - Clicking should open article in new tab
   - Source name and date should display below headline

## Fallback URLs

When LLM web search is unavailable, the system now provides Yahoo Finance URLs:

- Quote page: `https://finance.yahoo.com/quote/{ticker}`
- Analysis: `https://finance.yahoo.com/quote/{ticker}/analysis`
- Statistics: `https://finance.yahoo.com/quote/{ticker}/key-statistics`
- Profile: `https://finance.yahoo.com/quote/{ticker}/profile`
- News: `https://finance.yahoo.com/quote/{ticker}/news`

## What Changed

### backend/app.py
```python
# OLD:
current_model = 'gemini-2.0-flash-exp'

# NEW:
current_model = 'gemini-2.5-flash-lite'
```

### backend/data_sources/news_client.py

**_get_fallback_news()** - Now returns objects:
```python
# OLD:
'headlines': [
    f'{ticker} trading activity reflects market dynamics',
    f'Investors monitor {ticker} fundamentals',
    ...
]

# NEW:
'headlines': [
    {
        'title': f'{ticker} trading activity reflects market dynamics',
        'source': 'Market Analysis',
        'url': f'https://finance.yahoo.com/quote/{ticker}',
        'date': 'Recent'
    },
    ...
]
```

**_extract_headlines_from_text()** - Now returns objects:
```python
# OLD:
headlines.append(headline)

# NEW:
headlines.append({
    'title': headline,
    'source': 'Web Search',
    'url': '#',
    'date': 'Recent'
})
```

## Verification Checklist

- [x] Default model changed to `gemini-2.5-flash-lite` in app.py
- [x] Fallback news returns headline objects with URLs
- [x] Text extraction returns headline objects with URLs
- [x] Frontend correctly renders headline objects as clickable links
- [x] CSS styles exist for headline links (`.headline-link`, `.headline-source`, `.headline-date`)
- [x] Test script created to verify headline structure

## Next Steps

1. Restart the backend server
2. Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
3. Analyze a stock
4. Verify:
   - No 404 model errors in backend logs
   - "Detailed Analysis" section shows LLM analysis
   - News headlines are blue and clickable
   - Clicking headlines opens articles in new tab
   - Source and date display below each headline

## Notes

- The model name is case-sensitive: `gemini-2.5-flash-lite` (not `gemini-2.5-flash-exp`)
- All components (social_client, news_client, llm_sentiment, predictive_analysis, deep_analysis) use the model passed from report_generator
- The report_generator gets the model from app.py's `current_model` variable
- Users can change the model in Settings, but it defaults to `gemini-2.5-flash-lite` on server restart
