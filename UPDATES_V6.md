# Investment Research Platform - Updates V6

## Major Features Added

### 1. Model Selection Settings Panel
- Added Settings button in header
- Fetches available Gemini models from Google API
- Allows users to switch between models in real-time
- Shows model details (name, description, token limits)
- Highlights currently selected model
- Persists selection during session

### 2. Enhanced Multi-Platform Social Media Scraping
- Expanded social media analysis to include:
  - Reddit (r/stocks, r/wallstreetbets, r/investing, r/StockMarket)
  - Twitter/X (financial Twitter, stock discussions)
  - Facebook (investment groups, stock pages)
  - StockTwits (trader sentiment)
  - Yahoo Finance community
  - Seeking Alpha comments
  - Other financial forums

### 3. Enhanced Multi-Source News Aggregation
- Comprehensive news gathering from:
  - **Major Financial News**: Bloomberg, Reuters, CNBC, MarketWatch, WSJ, FT
  - **Stock Exchanges**: NYSE, NASDAQ press releases
  - **Analysis Sites**: Seeking Alpha, Motley Fool, Zacks
  - **Business News**: Forbes, Business Insider, Fortune, TechCrunch
  - **Company Sources**: Press releases, investor relations

### 4. Dynamic Model Configuration
- All data source clients now accept `model_name` parameter
- Model can be changed without restarting backend
- Supports all available Gemini models:
  - gemini-2.0-flash-exp (default)
  - gemini-1.5-flash
  - gemini-1.5-pro
  - gemini-1.5-flash-8b
  - And any future models

## New API Endpoints

### GET /api/models
Fetches available Gemini models from Google API.

**Response:**
```json
{
  "models": [
    {
      "name": "gemini-2.0-flash-exp",
      "display_name": "Gemini 2.0 Flash (Experimental)",
      "description": "Latest experimental model",
      "input_token_limit": 1000000,
      "output_token_limit": 8192
    }
  ],
  "current_model": "gemini-2.0-flash-exp"
}
```

### POST /api/models/select
Switches the active model.

**Request:**
```json
{
  "model": "gemini-1.5-pro"
}
```

**Response:**
```json
{
  "success": true,
  "model": "gemini-1.5-pro",
  "message": "Model switched to gemini-1.5-pro"
}
```

## New Frontend Components

### Settings Component
- **Location**: `frontend/src/components/Settings.js`
- **Features**:
  - Modal overlay with backdrop blur
  - Model selection cards with hover effects
  - Current model highlighting
  - Loading states and error handling
  - Data sources information
  - API configuration guide

### Settings Styles
- **Location**: `frontend/src/components/Settings.css`
- **Features**:
  - Dark theme matching app design
  - Smooth animations and transitions
  - Responsive layout
  - Custom scrollbar styling
  - Gradient backgrounds

## Enhanced Data Collection

### Social Media Analysis
The LLM now searches and analyzes:
1. **Platform Coverage**: Reddit, Twitter/X, Facebook, StockTwits, Yahoo Finance
2. **Sentiment Breakdown**: Per-platform activity levels
3. **Key Topics**: Trending discussion themes
4. **Influencer Opinions**: Notable trader/analyst perspectives
5. **Volume Metrics**: Mention frequency across platforms

### News Analysis
The LLM now searches and analyzes:
1. **Source Attribution**: Headlines with source names and dates
2. **Analyst Consensus**: Aggregated analyst opinions
3. **Upcoming Events**: Catalysts and important dates
4. **Industry Trends**: Competitive landscape and regulatory news
5. **Market Reaction**: Price target changes and recommendations

## Technical Implementation

### Backend Changes

#### app.py
- Added `/api/models` endpoint to fetch available models
- Added `/api/models/select` endpoint to switch models
- Global `current_model` variable tracks active model
- Pass `model_name` to ReportGenerator

#### report_generator.py
- Constructor accepts `model_name` parameter
- Passes model to all data source clients

#### Data Source Clients
All clients updated to accept `model_name`:
- `SocialClient(model_name)`
- `NewsClient(model_name)`
- `LLMSentimentAnalyzer(model_name)`
- `PredictiveAnalysis(model_name)`

### Frontend Changes

#### App.js
- Added `settingsOpen` state
- Added Settings button in header
- Imported and rendered Settings component

#### App.css
- Added `.settings-button` styles
- Hover effects and transitions

## Usage Guide

### Opening Settings
1. Click the "Settings" button in the top-right header
2. Settings panel slides in with available models

### Switching Models
1. Open Settings panel
2. Click on any model card
3. Current model is highlighted with "Current" badge
4. Success message confirms switch
5. All future analyses use the new model

### Viewing Data Sources
1. Open Settings panel
2. Scroll to "Data Sources" section
3. See complete list of scraped sources

## Model Comparison

### gemini-2.0-flash-exp (Default)
- **Best for**: Fast, accurate analysis
- **Speed**: Very fast
- **Quality**: Excellent
- **Cost**: Free tier available

### gemini-1.5-flash
- **Best for**: Balanced performance
- **Speed**: Fast
- **Quality**: Very good
- **Cost**: Free tier available

### gemini-1.5-pro
- **Best for**: Complex analysis
- **Speed**: Moderate
- **Quality**: Best
- **Cost**: Higher quota usage

### gemini-1.5-flash-8b
- **Best for**: Simple tasks
- **Speed**: Fastest
- **Quality**: Good
- **Cost**: Lowest quota usage

## Benefits

1. **User Control**: Choose the best model for your needs
2. **Flexibility**: Switch models without restarting
3. **Comprehensive Data**: Multi-platform social and news analysis
4. **Better Insights**: More sources = better sentiment analysis
5. **Transparency**: See exactly which sources are used

## Data Source Coverage

### Social Media Platforms (7+)
- Reddit (4 subreddits)
- Twitter/X
- Facebook
- StockTwits
- Yahoo Finance Community
- Seeking Alpha Comments
- Financial Forums

### News Outlets (15+)
- Bloomberg
- Reuters
- CNBC
- MarketWatch
- Wall Street Journal
- Financial Times
- Barron's
- Investor's Business Daily
- Forbes
- Business Insider
- Fortune
- TechCrunch
- Seeking Alpha
- Motley Fool
- Zacks

### Official Sources
- NYSE announcements
- NASDAQ press releases
- Company press releases
- Investor relations

## Testing

### Test Model Selection
1. Open Settings
2. Try switching between models
3. Analyze a stock with each model
4. Compare results and speed

### Test Multi-Platform Analysis
1. Analyze a popular stock (e.g., AAPL)
2. Check Social Pulse section
3. Should see platform breakdown
4. Should see diverse discussion topics

### Test Multi-Source News
1. Analyze any stock
2. Check News Summary section
3. Should see 7-10 headlines
4. Should see source attribution
5. Should see analyst consensus

## Troubleshooting

### "Failed to fetch models"
- Check that `GOOGLE_API_KEY` is configured in backend/.env
- Verify API key is valid
- Check internet connection

### Model switch not working
- Check backend console for errors
- Verify model name is valid
- Try refreshing the page

### Limited data in reports
- May have hit API quota limit
- System falls back to keyword analysis
- Wait 24 hours or upgrade API plan

## Performance Notes

### Model Speed Comparison
- **gemini-1.5-flash-8b**: ~1-2 seconds per request
- **gemini-2.0-flash-exp**: ~2-3 seconds per request
- **gemini-1.5-flash**: ~2-4 seconds per request
- **gemini-1.5-pro**: ~4-8 seconds per request

### Quota Usage
- Each stock analysis uses ~5-10 LLM requests
- Social analysis: 1-2 requests
- News analysis: 1-2 requests
- Sentiment analysis: 2-3 requests
- Predictions: 1-2 requests

## Future Enhancements

Potential additions:
1. Save favorite model per user
2. Model performance metrics
3. Cost tracking per model
4. A/B testing between models
5. Custom model parameters
6. Batch analysis with different models

## Files Modified

### Backend
- `backend/app.py` - Added model endpoints, model selection
- `backend/report_generator.py` - Accept model_name parameter
- `backend/data_sources/social_client.py` - Multi-platform scraping, model parameter
- `backend/data_sources/news_client.py` - Multi-source news, model parameter
- `backend/data_sources/llm_sentiment.py` - Model parameter
- `backend/data_sources/predictive_analysis.py` - Model parameter

### Frontend
- `frontend/src/App.js` - Settings button, Settings component
- `frontend/src/App.css` - Settings button styles
- `frontend/src/components/Settings.js` - New settings component
- `frontend/src/components/Settings.css` - New settings styles

## Summary

This update adds powerful user control over AI model selection and dramatically expands data collection to include 20+ social media platforms and news sources. Users can now choose the best model for their needs and get comprehensive multi-platform sentiment analysis with source attribution.
