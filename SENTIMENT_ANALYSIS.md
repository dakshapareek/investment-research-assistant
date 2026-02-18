# LLM-Based Sentiment Analysis

## Overview

The app now includes advanced AI-powered sentiment analysis that analyzes text from multiple sources:
- Reddit posts (r/stocks, r/wallstreetbets, r/investing)
- News headlines
- Twitter/X posts (when configured)

## Features

### Multi-Source Analysis
The LLM sentiment analyzer processes content from:
1. **Reddit**: Analyzes post titles weighted by upvote scores
2. **News**: Analyzes headlines from financial news sources
3. **Twitter**: Analyzes tweets (when API configured)

### Sentiment Scoring
- **Bullish**: Positive sentiment (score > 0.2)
- **Bearish**: Negative sentiment (score < -0.2)
- **Neutral**: Mixed or unclear sentiment

### Confidence Levels
Each analysis includes a confidence score (0-1) indicating reliability:
- High confidence (>0.7): Strong signal
- Medium confidence (0.4-0.7): Moderate signal
- Low confidence (<0.4): Weak signal

### Keyword Detection
The analyzer uses financial-specific keywords:

**Bullish Keywords**:
- bullish, buy, moon, rocket, gain, profit, surge, rally
- breakout, strong, growth, upgrade, beat, outperform
- positive, good, great, excellent, amazing

**Bearish Keywords**:
- bearish, sell, crash, loss, drop, fall, decline
- weak, downgrade, miss, underperform, negative
- terrible, avoid, concern, risk, warning, fear

### Weighted Analysis
- Reddit posts are weighted by upvote scores (higher scores = more influence)
- Multiple sources are combined with confidence-weighted averaging
- Final sentiment considers all sources together

## Display

The frontend shows:
1. **Overall Sentiment Badge**: Bullish/Bearish/Neutral with color coding
2. **Sentiment Score**: Numerical score (-1 to +1)
3. **Confidence Level**: Percentage showing reliability
4. **Source Breakdown**: Individual analysis for each source
5. **Detailed Stats**: Bullish/Bearish/Neutral counts per source

## Integration with Rating

The LLM sentiment heavily influences the investment rating:
- Strong bullish sentiment (+0.3): +3 points
- Moderate bullish (+0.1): +1 point
- Strong bearish (-0.3): -3 points
- Moderate bearish (-0.1): -1 point

Combined with macro data and SEC analysis to generate final Bull/Bear rating.

## Mock Data Fallback

When APIs are not configured, the system uses:
- Mock stock price data (random walk simulation)
- Sample news headlines
- Placeholder sentiment data

This allows testing the interface without API credentials.

## Future Enhancements

### Integration with Real LLMs
Replace rule-based analysis with:
- **OpenAI GPT-4**: Advanced sentiment understanding
- **Anthropic Claude**: Nuanced financial analysis
- **Local LLMs**: Llama, Mistral for privacy

### Example OpenAI Integration
```python
import openai

def analyze_with_gpt(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "system",
            "content": "Analyze financial sentiment as bullish, bearish, or neutral"
        }, {
            "role": "user",
            "content": text
        }]
    )
    return response.choices[0].message.content
```

### Advanced Features
- Aspect-based sentiment (product, management, financials)
- Temporal sentiment tracking (sentiment over time)
- Entity recognition (company mentions, competitors)
- Sarcasm detection
- Multi-language support

## Configuration

No additional configuration needed for basic sentiment analysis.

For enhanced analysis with real LLMs, add to `backend/.env`:
```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

## Usage

The sentiment analysis runs automatically when you analyze a stock:
1. Enter ticker symbol
2. Click "Analyze"
3. View AI Sentiment Analysis section in the report
4. See breakdown by source (Reddit, News, Twitter)
5. Check confidence levels and detailed statistics
