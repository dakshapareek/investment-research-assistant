# Investment Research Assistant - Complete Tutorial

## Table of Contents
1. [Problem Statement](#problem-statement)
2. [System Overview](#system-overview)
3. [Architecture & Agent Design](#architecture--agent-design)
4. [Implementation Details](#implementation-details)
5. [Prompt Engineering](#prompt-engineering)
6. [Building Process](#building-process)
7. [Benchmarking & Testing](#benchmarking--testing)
8. [Real Usage & Iteration](#real-usage--iteration)
9. [Reflection & Learnings](#reflection--learnings)
10. [Appendix](#appendix)

---

## 1. Problem Statement

### The Pain Point
As an individual investor, I face a significant challenge: **comprehensive stock research is extremely time-consuming**. 

When researching a single stock, I need to:
- Check multiple financial websites for price data and charts
- Read news articles from Bloomberg, Reuters, CNBC
- Browse Reddit and Twitter for retail investor sentiment
- Analyze technical indicators (RSI, moving averages, support/resistance)
- Review analyst ratings and price targets
- Synthesize all this information into an investment decision

**Current Status Quo:**
- Time per stock: 30-60 minutes
- Sources checked: 3-5 websites manually
- Sentiment analysis: Subjective, based on my reading
- Frequency: Can only research 2-3 stocks per day
- Consistency: Analysis quality varies based on my energy/focus

### Why This Matters to Me
I actively manage a personal investment portfolio and need to research 10-15 stocks weekly. The current manual process consumes 5-10 hours per week, limiting my ability to:
- Respond quickly to market opportunities
- Maintain a diversified watchlist
- Make data-driven decisions consistently
- Research new investment ideas thoroughly

### Why an Agentic Workflow?
An agentic workflow is ideal for this problem because:

1. **Parallel Processing**: Multiple agents can fetch data simultaneously (stock prices, news, social media)
2. **Specialization**: Each agent focuses on one task (news analysis, sentiment scoring, technical analysis)
3. **Scalability**: Can research 10 stocks in the time it takes to research 1 manually
4. **Consistency**: AI-powered analysis removes human bias and fatigue
5. **Real-time**: Automated data fetching ensures up-to-date information

### What the Workflow Does
The Investment Research Assistant automates the entire stock research process:

**Input:** Stock ticker symbol (e.g., "AAPL", "COST", "BTC-USD")

**Process:** 
- 5 specialized agents work in parallel
- Fetch real-time data from 8+ APIs
- AI analyzes sentiment from news and social media
- Generate comprehensive investment report

**Output:**
- Interactive price chart with 1-year history
- AI sentiment analysis (bullish/bearish/neutral)
- Real news headlines with clickable URLs
- Reddit sentiment from 20-50 posts
- Technical indicators (RSI, trends, support/resistance)
- Investment rating (Bull/Neutral/Bear)

**Time:** 20-30 seconds (vs 30-60 minutes manually)

---

## 2. System Overview

### Tech Stack

**Frontend:**
- React 18.2.0
- Recharts for interactive charts
- CSS3 for styling
- LocalStorage for persistence

**Backend:**
- Python 3.9+ with Flask
- OpenAI GPT-4o-mini for AI analysis
- 8+ financial API integrations
- MCP (Model Context Protocol) for stock data

**APIs & Data Sources:**
- **Stock Data**: Yahoo Finance, Alpha Vantage, Financial Modeling Prep, MCP
- **News**: NewsAPI.org (Reuters, Bloomberg, CNBC, Financial Post)
- **Social Media**: Reddit public JSON API
- **AI**: OpenAI GPT-4o-mini
- **Economic Data**: FRED (Federal Reserve)

**Infrastructure:**
- Flask development server
- CORS enabled for local development
- Environment variables for API keys
- JSON file storage for subscriptions

### High-Level Workflow

```
User Input (Ticker) 
    ↓
[Report Generator Agent] - Orchestrates the workflow
    ↓
┌───────────────┬──────────────┬─────────────────┬──────────────────┐
│               │              │                 │                  │
[Stock Data]  [News Agent]  [Social Agent]  [Sentiment Agent]  [Technical]
    │               │              │                 │                  │
    ↓               ↓              ↓                 ↓                  ↓
Yahoo Finance   NewsAPI.org    Reddit API      OpenAI GPT-4o      Calculations
Alpha Vantage   Real URLs      Real Posts      Analyzes Text      RSI, SMA, etc
MCP Server      5-7 articles   20-50 posts     Scores Sentiment   Trends
    │               │              │                 │                  │
    └───────────────┴──────────────┴─────────────────┴──────────────────┘
                                    ↓
                        [Report Aggregator]
                                    ↓
                        Comprehensive Investment Report
                                    ↓
                            User Interface
```

---

## 3. Architecture & Agent Design

### Agent 1: Report Generator (Orchestrator)
**File:** `backend/report_generator.py`

**Purpose:** Coordinates all other agents and combines their outputs

**Responsibilities:**
- Receives ticker symbol from API endpoint
- Spawns parallel tasks for data fetching
- Waits for all agents to complete
- Combines results into unified report
- Handles errors and fallbacks

**Key Methods:**
```python
def generate_report(self, ticker):
    # Orchestrates 4 parallel data fetches
    chart_data = self._fetch_chart_data(ticker)
    quote_data = self._fetch_quote_data(ticker)
    social_data = self._fetch_social_data(ticker)
    news_data = self._fetch_news_data(ticker)
```

**Why This Design:** Central orchestrator pattern ensures consistent report structure and handles agent failures gracefully.

---

### Agent 2: Stock Data Agent
**File:** `backend/data_sources/multi_api_client.py`

**Purpose:** Fetches real-time stock prices and historical data

**Data Sources (Priority Order):**
1. MCP Server (Model Context Protocol)
2. Yahoo Finance (yfinance library)
3. Alpha Vantage API
4. Financial Modeling Prep API
5. Finnhub API
6. Polygon.io API

**Key Features:**
- Automatic fallback if primary source fails
- Handles crypto (BTC-USD), forex (EURUSD=X), indices (^GSPC)
- Caches data to reduce API calls
- Returns standardized format regardless of source

**Sample Output:**
```json
{
  "price": 1018.48,
  "change": 19.62,
  "changePercent": 1.96,
  "dayHigh": 1022.88,
  "dayLow": 993.76,
  "volume": 2661568,
  "source": "Alpha Vantage"
}
```

---

### Agent 3: News Analysis Agent
**File:** `backend/data_sources/news_client.py`

**Purpose:** Fetches and analyzes real news headlines

**Process:**
1. Look up company name from ticker (COST → "Costco Wholesale")
2. Query NewsAPI.org with company name
3. Filter for relevance (must mention company or ticker)
4. Extract top 5-7 articles with real URLs
5. Pass headlines to AI for sentiment analysis

**Key Innovation:** Uses company names instead of ticker symbols for better search results
- Before: Searching "COST" returned irrelevant results about "cost of living"
- After: Searching "Costco Wholesale" returns actual Costco news

**Sample Output:**
```json
{
  "headlines": [
    {
      "title": "Bernstein Boosts Costco Target",
      "source": "Yahoo Entertainment",
      "url": "https://finance.yahoo.com/news/...",
      "date": "5 days ago"
    }
  ],
  "sentiment": "neutral",
  "detailed_summary": "AI-generated 4-paragraph analysis..."
}
```

---

### Agent 4: Social Media Agent
**File:** `backend/data_sources/social_client.py`

**Purpose:** Scrapes Reddit for retail investor sentiment

**Process:**
1. Look up company name from ticker
2. Search 4 subreddits: r/stocks, r/wallstreetbets, r/investing, r/StockMarket
3. Scrape posts from past week using Reddit's public JSON API
4. Filter posts that mention ticker OR company name
5. Sort by upvotes (most popular first)
6. Pass to AI for sentiment analysis

**No Authentication Required:** Uses Reddit's public JSON API

**Sample Output:**
```json
{
  "sentiment": "Bearish",
  "sentiment_score": -0.5,
  "mentions": 42,
  "top_posts": [
    {
      "title": "COST valuation concerns",
      "score": 150,
      "comments": 45,
      "subreddit": "stocks"
    }
  ]
}
```

---

### Agent 5: Sentiment Analysis Agent
**File:** `backend/data_sources/llm_sentiment.py`

**Purpose:** AI-powered sentiment analysis using OpenAI GPT-4o-mini

**What It Analyzes:**
- News headlines (5-7 articles)
- Reddit posts (20-50 posts)
- Combines into overall sentiment score

**AI Model:** OpenAI GPT-4o-mini
- Fast (< 2 seconds per analysis)
- Cost-effective ($0.15 per 1M tokens)
- Accurate sentiment classification

**Fallback:** Keyword-based analysis if AI unavailable

**Sample Prompt:**
```
Analyze the sentiment of this financial text:
"Bernstein Boosts Costco Wholesale Corporation (COST) Target"

Rules:
- "bullish" = positive outlook
- "bearish" = negative outlook  
- "neutral" = mixed sentiment
- score: -1 (very bearish) to +1 (very bullish)
- confidence: 0 (uncertain) to 1 (very certain)

Respond with ONLY JSON:
{"sentiment": "bullish", "score": 0.6, "confidence": 0.8}
```

**Output:**
```json
{
  "overall_sentiment": "neutral",
  "average_score": -0.32,
  "confidence": 0.70,
  "bullish_count": 2,
  "bearish_count": 10,
  "neutral_count": 5
}
```

---

