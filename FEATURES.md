# Investment Research Assistant - Features

## 🎯 Zerodha-like Trading Interface

### Stock Charts & Performance
- Real-time stock price charts with area visualization
- 1-year historical price data
- Interactive tooltips showing price at any point
- Performance metrics:
  - Current price with live change percentage
  - Day High/Low
  - 52-Week High/Low
  - P/E Ratio
  - Market Cap
  - Volume
  - 1Y Return %
  - Volatility Index

### Data Sources Integration

1. **Stock Market Data** (Yahoo Finance API)
   - Live stock quotes
   - Historical price data
   - Volume analysis
   - Financial ratios

2. **BLS API** (Bureau of Labor Statistics)
   - CPI (Consumer Price Index)
   - Unemployment Rate
   - Macro economic analysis

3. **SEC EDGAR**
   - 10-K/10-Q filings
   - Risk Factors analysis
   - MD&A (Management Discussion & Analysis)

4. **Social Sentiment** (Reddit)
   - r/stocks, r/wallstreetbets, r/investing
   - Sentiment scoring
   - Bot detection
   - Top posts tracking
   - Mention count

5. **News Aggregation**
   - Latest headlines
   - Sentiment summary

## 📊 Investment Report Sections

1. **Executive Summary**
   - Bull/Bear rating (Strong Bull, Moderate Bull, Neutral, Bear)
   - Investment recommendation

2. **Stock Chart**
   - Interactive price chart
   - Performance metrics
   - Volume analysis

3. **Macro Tailwinds**
   - CPI data
   - Unemployment data
   - Economic environment analysis

4. **Fundamental Core**
   - SEC filing insights
   - Risk factors
   - Management discussion

5. **Social Pulse**
   - Reddit sentiment analysis
   - Mention tracking
   - Top community posts
   - Bot activity detection

6. **News Summary**
   - Recent headlines
   - Market sentiment

7. **Risk Assessment**
   - Key risk factors
   - Warning signals

## 🚀 Usage

### Running the App
```bash
# Backend
cd backend
python app.py

# Frontend
cd frontend
npm start
```

### Accessing the App
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

### Analyzing Stocks
1. Enter ticker symbol (AAPL, MSFT, TSLA, etc.)
2. Click "Analyze" or select from watchlist
3. View comprehensive report with charts

### Configuring APIs
Edit `backend/.env`:
```
# Reddit API (for social sentiment)
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=InvestmentResearch/1.0

# Optional: BLS API key for higher rate limits
BLS_API_KEY=your_bls_key
```

## 🎨 UI Features

- Dark theme inspired by Zerodha Kite
- Responsive design
- Real-time data visualization
- Color-coded sentiment indicators
- Interactive charts with Recharts
- Smooth animations and transitions

## 📈 Performance Metrics

- Total Return (1Y)
- Volatility Index
- Volume Analysis
- Price Range Analysis
- Market Cap Tracking

## 🔒 Data Privacy

- No user data stored
- API calls made server-side
- Secure credential management via .env
