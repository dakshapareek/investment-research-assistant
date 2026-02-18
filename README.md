# Investment Research Assistant 📈

An AI-powered agentic system that automates comprehensive stock analysis by gathering data from multiple sources in parallel, performing sentiment analysis, and generating actionable investment insights in seconds.

## Quick Answers to Submission Questions

### 1. Problem & Agentic Approach (2-3 sentences)

Individual investors struggle to make informed decisions due to information overload and the time-consuming nature of analyzing multiple data sources (market data, news, social sentiment, SEC filings). The status quo requires manually checking various websites and synthesizing disparate information, which takes 2-4 hours per stock. An agentic workflow is ideal because it autonomously gathers data from multiple sources in parallel, applies AI-powered analysis, and synthesizes findings into actionable recommendations—completing in 3-5 seconds what would take humans hours.

### 2. Path Chosen

**Path A: Skills/Agentic Pack (Markdown files, and potentially some extra agents files)**

Custom-built multi-agent system with Python backend, React frontend, LLM integration, and MCP protocol support.

### 3. System Artifact

**Repository Structure**:
```
investment-research-agent/
├── backend/          # Flask API + Agent orchestration
├── frontend/         # React web interface
├── *.md             # 30+ documentation files
└── PROJECT_SUBMISSION.md  # Complete documentation
```

**Key Files**:
- `PROJECT_SUBMISSION.md` - Complete project documentation
- `backend/report_generator.py` - Main orchestrator
- `backend/data_sources/` - Specialized agents
- `PERFORMANCE_OPTIMIZATION.md` - 2-3x speedup details
- `SEARCH_IMPROVEMENTS.md` - Fuzzy search + web search

### 4. Documentation File

See **`PROJECT_SUBMISSION.md`** for comprehensive documentation including:
- ✅ Problem Statement
- ✅ System Design
- ✅ Prompt Documentation
- ✅ Building Process
- ✅ Real Usage & Iteration
- ✅ Benchmark Methodology & Findings
- ✅ Reflection

### 5. Optional Notes

**Key Innovations**:
- **Parallel Execution**: 2-3x faster than sequential (3-5s vs 8-14s)
- **Real Data Priority**: Uses NewsAPI, Reddit APIs (not LLM-generated)
- **MCP Integration**: Future-proof standardized protocol
- **Fuzzy Search**: Finds stocks by partial name or ticker
- **Web Search**: Identifies private companies (e.g., SpaceX)
- **Graceful Degradation**: Works even when APIs fail

**Production Ready**:
- 30+ documentation files
- Comprehensive error handling
- Email reports & daily alerts
- Interactive charts & visualizations

## Features

### Core Capabilities
- 🔍 **Smart Search**: Fuzzy matching for tickers and company names
- 📊 **Real-Time Data**: Live quotes from 7+ financial APIs with fallback
- 📰 **News Analysis**: Real headlines from NewsAPI.org with AI summaries
- 💬 **Social Sentiment**: Reddit analysis with LLM-powered insights
- 📈 **Price Predictions**: AI-generated forecasts with confidence levels
- 📧 **Email Reports**: Send analysis directly to inbox
- 🔔 **Daily Alerts**: Subscribe for automated morning reports
- 🌐 **MCP Protocol**: Standardized data fetching

### Technical Highlights
- **Parallel Data Gathering**: All sources fetched simultaneously
- **Multi-API Fallback**: 7+ financial data sources
- **LLM Integration**: OpenAI GPT-4o-mini for analysis
- **Dual Chart View**: Compare two stocks side-by-side
- **Private Company Detection**: Web search for non-public companies

## Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Required API Keys
- `OPENAI_API_KEY` - For AI analysis (required)
- `NEWS_API_KEY` - For real news (required)
- `REDDIT_CLIENT_ID` - For social sentiment (optional)
- Financial APIs - For market data (optional, has fallbacks)

See `API_SETUP_GUIDE.md` for detailed instructions.

## Architecture

### Multi-Agent System
```
┌─────────────────────────────────────────────┐
│         Report Generator (Orchestrator)      │
└─────────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
    ┌───▼───┐   ┌──▼──┐   ┌───▼────┐
    │ Stock │   │News │   │ Social │
    │ Data  │   │Agent│   │ Agent  │
    └───┬───┘   └──┬──┘   └───┬────┘
        │          │          │
        └──────────┼──────────┘
                   │
            ┌──────▼──────┐
            │ LLM Analysis│
            │  (OpenAI)   │
            └──────┬──────┘
                   │
            ┌──────▼──────┐
            │   Report    │
            │  Synthesis  │
            └─────────────┘
```

### Data Flow
1. **User Query** → Search/Validation
2. **Parallel Fetch** → Stock, News, Social (simultaneously)
3. **AI Analysis** → Sentiment, Predictions, Summaries
4. **Synthesis** → Comprehensive report
5. **Visualization** → Charts, tables, insights

## Performance

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Report Generation | 8-14s | 3-5s | **2-3x faster** |
| Search Response | 0.5-1s | 0.2-0.4s | **2x faster** |
| User Wait Time | 8-14s | 3-5s | **62% reduction** |

## Documentation

### Setup & Configuration
- `API_SETUP_GUIDE.md` - API key configuration
- `MCP_SETUP_GUIDE.md` - MCP server setup
- `GMAIL_SETUP_GUIDE.md` - Email configuration

### Features
- `SEARCH_IMPROVEMENTS.md` - Fuzzy search + web search
- `PERFORMANCE_OPTIMIZATION.md` - Parallel execution
- `DUAL_CHART_FEATURE.md` - Compare stocks
- `SUBSCRIPTION_FEATURE.md` - Daily alerts

### Technical
- `PROJECT_SUBMISSION.md` - Complete documentation
- `DATA_SOURCES_SUMMARY.md` - API integrations
- `AI_SENTIMENT_EXPLAINED.md` - LLM analysis
- `MCP_INTEGRATION_COMPLETE.md` - MCP protocol

## Tech Stack

**Backend**:
- Python 3.8+
- Flask (API server)
- OpenAI API (LLM)
- NewsAPI.org (News)
- Reddit API (Social)
- MCP Protocol (Data fetching)
- ThreadPoolExecutor (Parallel execution)

**Frontend**:
- React 18
- Recharts (Visualizations)
- Axios (API calls)

**APIs Integrated**:
- Financial: MCP, FMP, Alpha Vantage, Finnhub, Polygon, Marketstack, EODHD, Yahoo Finance
- News: NewsAPI.org
- Social: Reddit
- AI: OpenAI GPT-4o-mini

## Project Stats

- **Development Time**: ~16 days
- **Lines of Code**: ~7,000
- **Documentation Files**: 30+
- **APIs Integrated**: 10+
- **Performance Gain**: 2-3x faster
- **Success Rate**: 95%+ for major stocks

## License

MIT License - See LICENSE file for details

## Contact

For questions or support, please refer to the documentation files or create an issue.

---

**Status**: ✅ Production Ready  
**Last Updated**: February 17, 2026  
**Version**: 3.0
