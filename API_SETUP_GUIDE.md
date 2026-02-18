# 🔑 API Setup Guide

Complete guide to setting up all API keys for the Investment Research Assistant.

## 📋 Quick Start

1. Copy `.env.example` to `.env` in the `backend` folder
2. Follow the instructions below to get API keys
3. Paste keys into your `.env` file
4. Restart the backend server

```bash
cd backend
cp .env.example .env
# Edit .env with your API keys
python app.py
```

---

## 🤖 LLM APIs (For Sentiment Analysis)

### OpenAI GPT-4 (Recommended)
**Best for**: Accurate sentiment analysis, nuanced understanding

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Add to `.env`: `OPENAI_API_KEY=sk-your_key_here`

**Pricing**: Pay-as-you-go, ~$0.03 per 1K tokens
**Free Tier**: $5 credit for new accounts

---

### Anthropic Claude (Alternative)
**Best for**: Privacy-focused, detailed analysis

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up for an account
3. Navigate to API Keys
4. Create a new key
5. Add to `.env`: `ANTHROPIC_API_KEY=your_key_here`

**Pricing**: Pay-as-you-go
**Free Tier**: Limited trial credits

---

### Google Gemini (Free Option)
**Best for**: Free usage, good performance

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key
5. Add to `.env`: `GOOGLE_API_KEY=your_key_here`

**Pricing**: Free tier available
**Free Tier**: 60 requests per minute

---

## 📱 Social Media APIs

### Reddit API (Required for Social Sentiment)
**Best for**: Retail investor sentiment, community discussions

1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Scroll down and click "Create App" or "Create Another App"
3. Fill in:
   - **Name**: Investment Research Bot
   - **Type**: Select "script"
   - **Description**: Personal investment research
   - **Redirect URI**: http://localhost:8080
4. Click "Create app"
5. Copy the values:
   - **Client ID**: Under the app name (random string)
   - **Client Secret**: Click "edit" to see it
6. Add to `.env`:
   ```
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_secret
   REDDIT_USER_AGENT=InvestmentResearch/1.0
   ```

**Pricing**: Free
**Rate Limits**: 60 requests per minute

---

### Twitter/X API v2 (Optional)
**Best for**: Real-time sentiment, breaking news

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Sign up for a developer account (requires approval)
3. Create a new project and app
4. Navigate to "Keys and tokens"
5. Generate Bearer Token
6. Add to `.env`: `TWITTER_BEARER_TOKEN=your_token_here`

**Pricing**: Free tier available
**Free Tier**: 500K tweets/month (read-only)
**Note**: Approval process can take 1-2 days

---

## 💹 Financial Data APIs

### Alpha Vantage (Free Stock Data)
**Best for**: Historical prices, fundamentals

1. Go to [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Enter your email
3. Receive API key instantly
4. Add to `.env`: `ALPHA_VANTAGE_API_KEY=your_key_here`

**Pricing**: Free
**Free Tier**: 25 requests per day, 5 per minute

---

### Finnhub (Real-time Data)
**Best for**: Real-time quotes, news, earnings

1. Go to [Finnhub](https://finnhub.io/register)
2. Sign up with email
3. Verify email
4. Copy API key from dashboard
5. Add to `.env`: `FINNHUB_API_KEY=your_key_here`

**Pricing**: Free tier available
**Free Tier**: 60 API calls/minute

---

### Polygon.io (Professional Data)
**Best for**: High-quality market data

1. Go to [Polygon.io](https://polygon.io/dashboard/signup)
2. Sign up for free account
3. Navigate to API Keys
4. Copy your key
5. Add to `.env`: `POLYGON_API_KEY=your_key_here`

**Pricing**: Free tier available
**Free Tier**: 5 API calls/minute, delayed data

---

## 📰 News APIs

### NewsAPI.org (News Headlines)
**Best for**: General financial news

1. Go to [NewsAPI](https://newsapi.org/register)
2. Sign up with email
3. Verify email
4. Copy API key from dashboard
5. Add to `.env`: `NEWS_API_KEY=your_key_here`

**Pricing**: Free for development
**Free Tier**: 100 requests/day, 1-day delayed data

---

### Benzinga (Premium News)
**Best for**: Professional-grade news and analysis

1. Go to [Benzinga](https://www.benzinga.com/apis/)
2. Contact sales for API access
3. Receive API key
4. Add to `.env`: `BENZINGA_API_KEY=your_key_here`

**Pricing**: Paid plans starting at $99/month
**Free Tier**: Trial available

---

## 🏛️ Government Data APIs

### BLS API (Labor Statistics)
**Best for**: CPI, unemployment data

1. Go to [BLS Registration](https://data.bls.gov/registrationEngine/)
2. Fill in registration form
3. Verify email
4. Receive API key
5. Add to `.env`: `BLS_API_KEY=your_key_here`

**Pricing**: Free
**Free Tier**: 500 requests/day (vs 25 without key)

---

### FRED API (Economic Data)
**Best for**: Federal Reserve economic indicators

1. Go to [FRED API](https://fred.stlouisfed.org/docs/api/api_key.html)
2. Click "Request API Key"
3. Sign in or create account
4. Fill in application
5. Receive key instantly
6. Add to `.env`: `FRED_API_KEY=your_key_here`

**Pricing**: Free
**Rate Limits**: Generous, no strict limits

---

## ✅ Recommended Minimum Setup

For basic functionality, get these keys:

1. **Reddit API** (Free, instant) - Social sentiment
2. **Alpha Vantage** (Free, instant) - Stock data
3. **NewsAPI** (Free, instant) - News headlines
4. **Google Gemini** (Free, instant) - LLM sentiment

**Total Time**: ~15 minutes
**Total Cost**: $0

---

## 🚀 Premium Setup

For professional-grade analysis:

1. **OpenAI GPT-4** ($) - Best sentiment analysis
2. **Finnhub** (Free tier) - Real-time data
3. **Reddit API** (Free) - Social sentiment
4. **Twitter API** (Free tier) - Real-time sentiment
5. **Polygon.io** (Free tier) - Market data
6. **BLS API** (Free) - Economic data

**Total Time**: ~30 minutes
**Total Cost**: ~$10-20/month (OpenAI usage)

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** to version control
2. **Use environment variables** in production
3. **Rotate keys regularly** (every 90 days)
4. **Set up rate limiting** to avoid overages
5. **Monitor API usage** in provider dashboards
6. **Use separate keys** for dev/prod environments

---

## 🐛 Troubleshooting

### "API key invalid" error
- Check for extra spaces in `.env` file
- Ensure key is copied completely
- Verify key is active in provider dashboard

### "Rate limit exceeded" error
- Wait for rate limit to reset
- Upgrade to paid tier
- Implement caching to reduce calls

### "Module not found" error
- Run `pip install -r requirements.txt`
- Restart backend server

### Charts not showing
- Check browser console for errors
- Verify API keys are set correctly
- Try with mock data first (no keys needed)

---

## 📞 Support

- **Reddit API**: [r/redditdev](https://www.reddit.com/r/redditdev/)
- **OpenAI**: [help.openai.com](https://help.openai.com/)
- **Twitter**: [developer.twitter.com/support](https://developer.twitter.com/en/support)
- **General**: Check provider documentation

---

## 🔄 Updating Keys

After adding/updating keys in `.env`:

1. Save the file
2. Restart the backend server:
   ```bash
   # Stop current server (Ctrl+C)
   python app.py
   ```
3. Refresh the frontend
4. Test with a stock analysis

Keys are loaded on server startup, so restart is required for changes to take effect.
