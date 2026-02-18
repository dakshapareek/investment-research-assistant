# Investment Research Assistant - Demo Script (2-5 minutes)

## 🎬 Demo Flow

### Opening (30 seconds)
"Hi, I'm going to show you an AI-powered Investment Research Assistant that solves a real problem I face as an investor: spending hours researching stocks across multiple sources."

### The Problem (30 seconds)
"Currently, if I want to research a stock like Costco, I need to:
- Check Yahoo Finance for price data
- Read news on Bloomberg, Reuters, CNBC
- Browse Reddit for retail sentiment
- Analyze technical indicators
- Read analyst reports

This takes 30-60 minutes per stock. My system does this in under 30 seconds."

### The Solution Overview (20 seconds)
"I built an agentic workflow with multiple specialized AI agents:
- Stock Data Agent: Fetches real-time prices and charts
- News Agent: Analyzes real headlines from NewsAPI
- Social Media Agent: Scrapes Reddit for sentiment
- Sentiment Analyzer: Uses OpenAI GPT-4o-mini to analyze everything
- Report Generator: Combines insights into actionable reports"

### Live Demo (2-3 minutes)

#### Part 1: Search & Analysis (60 seconds)
**[Screen: Show homepage]**
"Let me search for Costco - ticker symbol COST."

**[Type COST in search bar]**
"The system auto-completes from a database of 100+ tickers."

**[Click on COST]**
"Now watch as multiple agents work in parallel..."

**[Show loading states]**
"You can see:
- Stock Data Agent fetching historical prices
- News Agent querying NewsAPI.org
- Social Agent scraping Reddit
- All happening simultaneously"

#### Part 2: Results Breakdown (90 seconds)

**[Scroll to Stock Chart]**
"First, real-time price data from Yahoo Finance and Alpha Vantage.
Current price: $1,018.48, up 1.96% today.
This chart shows 1-year performance with interactive tooltips."

**[Scroll to AI Sentiment Analysis]**
"Here's where the AI magic happens.
- News Sentiment: Neutral (analyzed 5 real headlines)
- Reddit Sentiment: Bearish (analyzed 42 real posts)
- Combined Score: -0.32 with 70% confidence

The AI read actual headlines like 'Bernstein Boosts Costco Target' and Reddit discussions about valuation concerns."

**[Click a news headline]**
"Every headline links to the actual article - this goes to Yahoo Finance.
The AI didn't make this up; it analyzed real news from Reuters, Bloomberg, CNBC."

**[Scroll to News Summary]**
"The AI generated this 4-paragraph analysis by reading the real headlines.
It identified key themes: analyst upgrades, consumer sentiment, competitive positioning."

**[Scroll to Social Media section]**
"The Reddit analysis shows:
- 42 posts scraped from r/stocks, r/wallstreetbets, r/investing
- Top posts with real upvotes and comment counts
- AI-generated summary of retail investor sentiment"

**[Scroll to Technical Analysis]**
"Technical indicators calculated from real price data:
- RSI: 61.8 (approaching overbought)
- 20-day trend: +4.9% (bullish)
- Support/Resistance levels identified"

#### Part 3: Key Features (30 seconds)

**[Show watchlist]**
"I can save stocks to my watchlist - it persists across sessions.
Includes traditional stocks and crypto like BTC-USD, ETH-USD."

**[Show subscription feature]**
"I can subscribe to daily email alerts when stocks move >2%.
The system sends automated reports every morning at 9 AM."

**[Show data sources panel]**
"Full transparency on data sources:
- Stock prices: Yahoo Finance, Alpha Vantage, MCP
- News: NewsAPI.org (real articles)
- Social: Reddit public API
- AI: OpenAI GPT-4o-mini"

### The Technology (20 seconds)
"Tech stack:
- Frontend: React with interactive charts
- Backend: Python Flask with multiple API integrations
- AI: OpenAI GPT-4o-mini for sentiment analysis
- MCP: Model Context Protocol for stock data
- Real-time data from 8+ financial APIs"

### Results & Impact (20 seconds)
"Results:
- Research time: 60 minutes → 30 seconds (120x faster)
- Data sources: 1-2 → 8+ (comprehensive)
- Sentiment analysis: Manual → AI-powered (objective)
- Cost: Free (using free API tiers)

I use this daily to research stocks before making investment decisions."

### Closing (10 seconds)
"This agentic workflow demonstrates how multiple specialized AI agents can work together to solve real-world problems. Each agent has a specific role, they work in parallel, and the system combines their outputs into actionable insights."

---

## 🎥 Demo Video Script Details

### Camera Setup
- Screen recording with voiceover
- Show browser at 1920x1080
- Zoom in on key sections
- Use cursor highlights for important elements

### Key Moments to Capture
1. **Search autocomplete** - Shows ticker database integration
2. **Parallel loading** - Shows agents working simultaneously
3. **Real URLs** - Click a news link to prove it's real
4. **AI analysis** - Highlight the sentiment scores
5. **Interactive chart** - Hover to show tooltips
6. **Watchlist persistence** - Add/remove stocks
7. **Email subscription** - Show the subscription flow

### Talking Points Emphasis
- "REAL data" - Emphasize multiple times
- "30 seconds vs 60 minutes" - The key value prop
- "Multiple agents working in parallel" - The agentic workflow
- "OpenAI GPT-4o-mini" - The AI technology
- "I use this daily" - Personal validation

### Visual Aids
- Circle/highlight key numbers (sentiment scores, prices)
- Arrow pointing to "Real URLs"
- Zoom in on AI-generated summaries
- Show side-by-side: Before (manual research) vs After (automated)

---

## 📊 Demo Data Recommendations

### Best Stocks to Demo
1. **COST (Costco)** - Good news coverage, active Reddit discussions
2. **NVDA (NVIDIA)** - High sentiment, lots of social buzz
3. **AAPL (Apple)** - Well-known, comprehensive data
4. **BTC-USD (Bitcoin)** - Shows crypto support

### Avoid
- Obscure tickers with no news
- Stocks with API rate limit issues
- Tickers not in the database

---

## 🎯 Key Messages

1. **Problem**: Stock research is time-consuming and fragmented
2. **Solution**: Agentic workflow with specialized AI agents
3. **Technology**: Real APIs + OpenAI AI + React frontend
4. **Results**: 120x faster, more comprehensive, AI-powered insights
5. **Validation**: Used daily for real investment decisions

---

## 📝 Demo Checklist

Before recording:
- [ ] Backend server running (`python backend/app.py`)
- [ ] Frontend server running (`npm start` in frontend/)
- [ ] All API keys configured in `.env`
- [ ] Test COST ticker to ensure data loads
- [ ] Clear browser cache for clean demo
- [ ] Close unnecessary browser tabs
- [ ] Set browser zoom to 100%
- [ ] Disable browser notifications
- [ ] Test audio levels
- [ ] Prepare backup ticker (NVDA) in case COST fails

During recording:
- [ ] Speak clearly and at moderate pace
- [ ] Pause briefly between sections
- [ ] Show, don't just tell (click things, scroll, interact)
- [ ] Emphasize "real data" and "AI-powered"
- [ ] Keep energy high and enthusiastic
- [ ] Stay within 2-5 minute timeframe

After recording:
- [ ] Review for audio quality
- [ ] Check that all key points were covered
- [ ] Verify URLs are visible when clicked
- [ ] Ensure sentiment scores are clearly shown
- [ ] Add captions/subtitles if needed
- [ ] Export at 1080p minimum

---

## 🔗 Demo Video URL

**Upload to:** YouTube (unlisted) or Loom
**Title:** "AI-Powered Investment Research Assistant - Agentic Workflow Demo"
**Description:** 
```
An agentic workflow that automates stock research using multiple specialized AI agents. 

The system:
- Fetches real-time stock data from Yahoo Finance & Alpha Vantage
- Analyzes real news from NewsAPI.org (Reuters, Bloomberg, CNBC)
- Scrapes Reddit for retail investor sentiment
- Uses OpenAI GPT-4o-mini to analyze sentiment
- Generates comprehensive investment reports in 30 seconds

Tech Stack: React, Python Flask, OpenAI GPT-4o-mini, MCP, 8+ financial APIs

Reduces research time from 60 minutes to 30 seconds (120x faster).
```

**Tags:** AI, Agentic Workflow, Stock Research, OpenAI, Investment Analysis, Financial Technology, React, Python, Machine Learning

---

## 💡 Pro Tips

1. **Practice the demo 2-3 times** before recording
2. **Have a backup plan** if APIs fail (show screenshots)
3. **Keep it conversational** - talk like you're explaining to a friend
4. **Show real value** - emphasize time savings and comprehensiveness
5. **Be honest** - mention limitations (API rate limits, AI accuracy)
6. **End with impact** - "I use this daily" is powerful validation

---

## 🎬 Alternative Demo Formats

### Short Version (2 minutes)
- Problem (20s)
- Quick demo of COST (60s)
- Key features (30s)
- Results (10s)

### Long Version (5 minutes)
- Problem (45s)
- Solution overview (30s)
- Full demo with 2 stocks (2m 30s)
- Technology deep dive (45s)
- Results & impact (30s)

### Technical Version (for developers)
- Architecture overview
- Show code structure
- Explain agent design
- Demonstrate API integrations
- Discuss prompt engineering

Choose based on your audience and assignment requirements.
