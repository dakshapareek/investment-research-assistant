# 📈 Investment Research Agent - Streamlit Edition

A powerful AI-driven stock analysis platform built with Streamlit and Python.

## 🚀 Quick Start

### Run Locally (2 Minutes)

1. **Start Backend:**
   ```bash
   cd backend
   python app.py
   ```

2. **Start Streamlit:**
   ```bash
   streamlit run streamlit_app.py
   ```

   Or use the batch file:
   ```bash
   run_streamlit.bat
   ```

3. **Open Browser:**
   Visit `http://localhost:8501`

### Deploy to Cloud (10 Minutes)

1. **Deploy Backend to Railway:**
   - Go to [railway.app](https://railway.app)
   - New Project → Deploy from GitHub
   - Select `backend` folder
   - Add environment variables
   - Copy URL

2. **Deploy Streamlit to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - New app → Select repository
   - Main file: `streamlit_app.py`
   - Add secret: `API_URL = "your-backend-url"`
   - Deploy!

**Cost: FREE** (Streamlit Cloud) + $5/month (Railway)

## ✨ Features

- 📊 **Real-time Stock Data** - Live prices, charts, volume
- 📰 **News Aggregation** - Latest articles from trusted sources
- 💬 **Social Sentiment** - Reddit and Twitter analysis
- 🤖 **AI Analysis** - OpenAI-powered sentiment and predictions
- 📈 **Technical Indicators** - RSI, MACD, moving averages
- 🔮 **Price Predictions** - ML-based forecasting
- 📧 **Email Alerts** - Daily reports and notifications
- 🎯 **Watchlist** - Track your favorite stocks

## 📁 Project Structure

```
├── streamlit_app.py          # Main Streamlit application
├── backend/
│   ├── app.py                # Flask API server
│   ├── data_sources/         # API clients
│   ├── report_generator.py   # Report generation
│   └── requirements.txt      # Backend dependencies
├── .streamlit/
│   ├── config.toml           # Theme configuration
│   └── secrets.toml          # API keys (local)
├── requirements_streamlit.txt # Streamlit dependencies
└── run_streamlit.bat         # Quick start script
```

## 🔧 Configuration

### Environment Variables

Create `backend/.env`:
```bash
# Required
OPENAI_API_KEY=your_key
NEWS_API_KEY=your_key

# Optional (for more data sources)
ALPHA_VANTAGE_API_KEY=your_key
FINNHUB_API_KEY=your_key
POLYGON_API_KEY=your_key
```

### Streamlit Secrets

Create `.streamlit/secrets.toml`:
```toml
API_URL = "http://localhost:5000"

# Or for production:
API_URL = "https://your-backend.railway.app"
```

## 📚 Documentation

- **[STREAMLIT_QUICKSTART.md](STREAMLIT_QUICKSTART.md)** - Quick start guide
- **[STREAMLIT_DEPLOY.md](STREAMLIT_DEPLOY.md)** - Deployment guide
- **[STREAMLIT_VS_REACT.md](STREAMLIT_VS_REACT.md)** - Comparison with React
- **[DEPLOY_COMMANDS.md](DEPLOY_COMMANDS.md)** - Command reference
- **[API_SETUP_GUIDE.md](API_SETUP_GUIDE.md)** - API key setup

## 🎯 Supported Assets

- **Stocks:** AAPL, TSLA, NVDA, MSFT, GOOGL, etc.
- **Crypto:** BTC-USD, ETH-USD, DOGE-USD, etc.
- **Forex:** EURUSD=X, GBPUSD=X, JPYUSD=X, etc.

## 🛠️ Tech Stack

### Frontend
- **Streamlit** - Web framework
- **Plotly** - Interactive charts
- **Pandas** - Data manipulation

### Backend
- **Flask** - REST API
- **OpenAI** - Sentiment analysis
- **NewsAPI** - News aggregation
- **Multiple Financial APIs** - Stock data

## 📊 API Endpoints

- `GET /api/watchlist` - Get watchlist
- `POST /api/watchlist` - Add stock
- `DELETE /api/watchlist/{ticker}` - Remove stock
- `GET /api/stock/{ticker}` - Get stock data
- `POST /api/subscribe` - Subscribe to alerts
- `GET /api/subscriptions` - Get subscriptions

## 🔐 Security

- API keys stored in secrets
- CORS configured for security
- Environment variables for sensitive data
- No credentials in code

## 🚀 Deployment Options

### Option 1: Streamlit Cloud + Railway (Recommended)
- **Cost:** FREE + $5/month
- **Time:** 10 minutes
- **Difficulty:** Easy

### Option 2: Docker
- **Cost:** VPS cost ($5-10/month)
- **Time:** 20 minutes
- **Difficulty:** Moderate

### Option 3: AWS/GCP
- **Cost:** Variable
- **Time:** 30+ minutes
- **Difficulty:** Advanced

## 📈 Performance

- Real-time data updates
- Caching for API calls
- Optimized chart rendering
- Lazy loading for large datasets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

MIT License - feel free to use for personal or commercial projects

## 🆘 Support

- Check documentation in the repo
- Open an issue on GitHub
- Visit [Streamlit Forum](https://discuss.streamlit.io)

## 🎉 Credits

Built with:
- [Streamlit](https://streamlit.io)
- [OpenAI](https://openai.com)
- [NewsAPI](https://newsapi.org)
- [Plotly](https://plotly.com)
- Multiple financial data providers

## 📞 Contact

For questions or feedback, open an issue on GitHub.

---

**Made with ❤️ using Streamlit and Python**

🚀 **Deploy now:** [share.streamlit.io](https://share.streamlit.io)
