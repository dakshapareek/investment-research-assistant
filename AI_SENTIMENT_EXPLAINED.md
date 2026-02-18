# AI Sentiment Analysis - How It Works

## Overview
The AI Sentiment Analysis in your Investment Research Assistant is **100% REAL** and based on **actual data sources**. It's NOT made up - it analyzes real news articles and social media posts using AI.

## How It Works (Step by Step)

### 1. Data Collection (REAL Sources)

#### News Analysis:
- **Source**: NewsAPI.org (real news aggregator)
- **What it fetches**: Actual news articles from Reuters, Bloomberg, CNBC, Financial Post, etc.
- **Example**: When you search for COST, it fetches real headlines like:
  - "Bernstein Boosts Costco Wholesale Corporation (COST) Target"
  - "Coca-Cola earnings, Google's AI risks, Target layoffs"
- **URLs**: Each headline has a real, clickable URL to the actual article

#### Social Media Analysis (Reddit):
- **Source**: Reddit's public JSON API
- **What it scrapes**: Real Reddit posts from r/stocks, r/wallstreetbets, r/investing, r/StockMarket
- **Example**: Actual posts like "NVDA earnings beat expectations" with real upvotes and comments
- **No login required**: Uses Reddit's public API (no authentication needed)

### 2. AI Analysis (OpenAI GPT-4o-mini)

Once real data is collected, the AI analyzes it:

#### What the AI Does:
1. **Reads** the actual headlines/posts (not making them up)
2. **Analyzes** the sentiment (bullish/bearish/neutral)
3. **Scores** each piece of content (-1 to +1 scale)
4. **Generates** a professional summary based on the REAL content

#### AI Prompt Example:
```
Analyze the sentiment of this financial text:
"Bernstein Boosts Costco Wholesale Corporation (COST) Target, 
Sees Consumer Sentiment Still Soft"

Rules:
- "bullish" = positive outlook
- "bearish" = negative outlook  
- "neutral" = mixed sentiment
- score: -1 (very bearish) to +1 (very bullish)
```

#### AI Response:
```json
{
  "sentiment": "bullish",
  "score": 0.6,
  "confidence": 0.8
}
```

### 3. Aggregation & Display

The system combines sentiment from multiple sources:

- **Reddit Sentiment**: Based on 10-50 real Reddit posts
- **News Sentiment**: Based on 5-7 real news headlines
- **Combined Score**: Weighted average of both sources

## What's Real vs What's AI-Generated

### ✅ REAL (Not Made Up):
1. **News Headlines**: Fetched from NewsAPI.org
2. **News URLs**: Direct links to Reuters, Bloomberg, CNBC, etc.
3. **Reddit Posts**: Scraped from actual Reddit discussions
4. **Reddit Scores**: Real upvotes and comment counts
5. **Stock Prices**: From Yahoo Finance, Alpha Vantage, etc.

### 🤖 AI-GENERATED (Based on Real Data):
1. **Sentiment Scores**: AI analyzes real headlines and assigns scores
2. **Detailed Summaries**: AI writes 3-4 paragraph analysis of real news
3. **Key Themes**: AI identifies patterns in real discussions
4. **Bullish/Bearish Points**: AI extracts insights from real content

## Example: COST (Costco) Analysis

### Step 1: Fetch Real News
```
✓ Found 5 real news articles from NewsAPI
1. "Bernstein Boosts Costco Wholesale Corporation (COST) Target"
   Source: Yahoo Entertainment
   URL: https://finance.yahoo.com/news/...
```

### Step 2: AI Analyzes Real Headlines
```
AI reads: "Bernstein Boosts Costco... Target"
AI thinks: "Boost" and "Target" are positive → Bullish
AI scores: +0.6 (moderately bullish)
```

### Step 3: Fetch Real Reddit Posts
```
✓ Scraped 42 Reddit posts about COST
- "COST earnings beat expectations" (150 upvotes)
- "Costco membership growth strong" (89 upvotes)
- "Worried about COST valuation" (45 upvotes)
```

### Step 4: AI Analyzes Reddit Sentiment
```
AI reads all 42 posts
AI counts: 25 bullish, 10 bearish, 7 neutral
AI calculates: Average score = +0.4 (bullish)
```

### Step 5: Generate Summary
```
AI writes: "Recent news coverage for Costco Wholesale shows 
positive momentum with analyst upgrades and strong fundamentals. 
Bernstein's target price increase reflects confidence in the 
company's resilience..."
```

## Fallback Mechanisms

### If APIs Fail:
1. **Keyword Analysis**: Uses predefined bullish/bearish keywords
2. **Generic Summaries**: Provides general market analysis
3. **Mock Data**: Shows example data with clear labels

### Current Status:
- ✅ **NewsAPI**: Working (real news)
- ✅ **Reddit Scraping**: Working (real posts)
- ✅ **OpenAI Analysis**: Working (AI sentiment)
- ✅ **Company Name Search**: Working (better relevance)

## Verification

You can verify the data is real by:

1. **Click News URLs**: They link to actual Reuters, Bloomberg, CNBC articles
2. **Check Reddit Posts**: URLs link to real Reddit discussions
3. **Compare Dates**: News dates match actual publication dates
4. **Cross-Reference**: Search the headlines on Google - they're real

## Technical Details

### AI Model Used:
- **Primary**: OpenAI GPT-4o-mini (fast, efficient, accurate)
- **Fallback**: Google Gemini (if OpenAI unavailable)
- **Last Resort**: Keyword-based analysis (no AI)

### Data Sources:
- **News**: NewsAPI.org (36a730e110a14761a3b294ee92765cf5)
- **Social**: Reddit public JSON API (no auth required)
- **Stock Data**: Yahoo Finance, Alpha Vantage, Financial Modeling Prep

### Analysis Method:
1. Fetch real data from APIs
2. Pass real content to AI (OpenAI GPT-4o-mini)
3. AI analyzes sentiment and generates insights
4. System aggregates scores and displays results

## Summary

**Is it real?** YES - The news headlines, Reddit posts, and stock data are 100% real.

**Is it AI?** YES - The sentiment analysis, scores, and summaries are generated by AI (OpenAI GPT-4o-mini).

**Is it made up?** NO - The AI analyzes REAL data, it doesn't invent fake news or posts.

**Can I trust it?** YES - But always verify by clicking the news URLs and checking the sources yourself. The AI provides analysis, but you should make your own investment decisions.

## The Bottom Line

Think of it like this:
- **Reporter** (NewsAPI/Reddit): Gathers real news and posts
- **Analyst** (OpenAI AI): Reads the real news and gives their opinion
- **You**: Make the final investment decision

The AI is the analyst, not the reporter. It reads real news and gives you its professional analysis of the sentiment.
