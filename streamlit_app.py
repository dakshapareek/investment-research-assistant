import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Investment Research Agent",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .positive {
        color: #00c853;
    }
    .negative {
        color: #ff1744;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = st.secrets.get("API_URL", "http://localhost:5000")

# Session state initialization
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []
if 'selected_ticker' not in st.session_state:
    st.session_state.selected_ticker = None
if 'comparison_ticker' not in st.session_state:
    st.session_state.comparison_ticker = None

# Helper functions
def fetch_watchlist():
    try:
        response = requests.get(f"{API_BASE_URL}/api/watchlist", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching watchlist: {str(e)}")
        return []

def add_to_watchlist(ticker):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/watchlist",
            json={"ticker": ticker.upper()},
            timeout=10
        )
        if response.status_code == 200:
            st.success(f"✓ Added {ticker.upper()} to watchlist")
            return True
        else:
            st.error(f"Failed to add {ticker}")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

def remove_from_watchlist(ticker):
    try:
        response = requests.delete(
            f"{API_BASE_URL}/api/watchlist/{ticker}",
            timeout=10
        )
        if response.status_code == 200:
            st.success(f"✓ Removed {ticker} from watchlist")
            return True
        return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

def fetch_stock_data(ticker):
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/stock/{ticker}",
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def create_price_chart(historical_data, ticker):
    if not historical_data:
        return None
    
    df = pd.DataFrame(historical_data)
    df['date'] = pd.to_datetime(df['date'])
    
    fig = go.Figure()
    
    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=df['date'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name=ticker
    ))
    
    # Volume bar chart
    fig.add_trace(go.Bar(
        x=df['date'],
        y=df['volume'],
        name='Volume',
        yaxis='y2',
        marker_color='rgba(100, 100, 100, 0.3)'
    ))
    
    fig.update_layout(
        title=f"{ticker} Price History",
        yaxis_title="Price ($)",
        yaxis2=dict(
            title="Volume",
            overlaying='y',
            side='right'
        ),
        xaxis_rangeslider_visible=False,
        height=500,
        hovermode='x unified'
    )
    
    return fig

# Main app
st.markdown('<div class="main-header">📈 Investment Research Agent</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🎯 Watchlist")
    
    # Add ticker input
    new_ticker = st.text_input("Add Stock Ticker", placeholder="e.g., AAPL, TSLA").upper()
    if st.button("➕ Add to Watchlist", use_container_width=True):
        if new_ticker:
            if add_to_watchlist(new_ticker):
                st.session_state.watchlist = fetch_watchlist()
                st.rerun()
    
    st.divider()
    
    # Display watchlist
    watchlist = fetch_watchlist()
    st.session_state.watchlist = watchlist
    
    if watchlist:
        st.subheader("Your Stocks")
        for ticker in watchlist:
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(f"📊 {ticker}", key=f"select_{ticker}", use_container_width=True):
                    st.session_state.selected_ticker = ticker
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_{ticker}"):
                    if remove_from_watchlist(ticker):
                        st.session_state.watchlist = fetch_watchlist()
                        st.rerun()
    else:
        st.info("No stocks in watchlist. Add one above!")
    
    st.divider()
    
    # Settings
    with st.expander("⚙️ Settings"):
        st.text_input("API Base URL", value=API_BASE_URL, key="api_url")
        if st.button("Test Connection"):
            try:
                response = requests.get(f"{API_BASE_URL}/api/watchlist", timeout=5)
                if response.status_code == 200:
                    st.success("✓ Connected!")
                else:
                    st.error("Connection failed")
            except:
                st.error("Cannot reach API")

# Main content
if st.session_state.selected_ticker:
    ticker = st.session_state.selected_ticker
    
    # Fetch data
    with st.spinner(f"Loading data for {ticker}..."):
        data = fetch_stock_data(ticker)
    
    if data:
        # Header with current price
        col1, col2, col3, col4 = st.columns(4)
        
        current_price = data.get('current_price', 0)
        change = data.get('change', 0)
        change_percent = data.get('change_percent', 0)
        
        with col1:
            st.metric(
                label="Current Price",
                value=f"${current_price:.2f}",
                delta=f"{change_percent:.2f}%"
            )
        
        with col2:
            st.metric(
                label="Day Change",
                value=f"${change:.2f}"
            )
        
        with col3:
            st.metric(
                label="Volume",
                value=f"{data.get('volume', 0):,}"
            )
        
        with col4:
            sentiment = data.get('sentiment', {})
            sentiment_score = sentiment.get('score', 0)
            sentiment_label = sentiment.get('label', 'Neutral')
            st.metric(
                label="AI Sentiment",
                value=sentiment_label,
                delta=f"{sentiment_score:.2f}"
            )
        
        # Tabs for different sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Chart", 
            "📰 News", 
            "💬 Social Media", 
            "📈 Analysis",
            "🔮 Predictions"
        ])
        
        with tab1:
            st.subheader(f"{ticker} Price Chart")
            
            # Time range selector
            time_range = st.selectbox(
                "Time Range",
                ["1D", "5D", "1M", "3M", "6M", "1Y", "5Y"],
                index=3
            )
            
            # Create chart
            historical = data.get('historical_data', [])
            if historical:
                fig = create_price_chart(historical, ticker)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No historical data available")
            
            # Comparison feature
            st.divider()
            st.subheader("Compare with Another Stock")
            compare_ticker = st.text_input("Enter ticker to compare", key="compare_input").upper()
            if st.button("Compare") and compare_ticker:
                st.session_state.comparison_ticker = compare_ticker
                st.rerun()
        
        with tab2:
            st.subheader("📰 Latest News")
            news = data.get('news', [])
            
            if news:
                for article in news[:10]:
                    with st.container():
                        st.markdown(f"**{article.get('title', 'No title')}**")
                        st.caption(f"Source: {article.get('source', 'Unknown')} | {article.get('published_at', '')}")
                        st.write(article.get('summary', 'No summary available'))
                        if article.get('url'):
                            st.markdown(f"[Read more]({article['url']})")
                        st.divider()
            else:
                st.info("No news articles available")
        
        with tab3:
            st.subheader("💬 Social Media Sentiment")
            social = data.get('social_media', [])
            
            if social:
                for post in social[:10]:
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.write(post.get('text', ''))
                            st.caption(f"Platform: {post.get('platform', 'Unknown')} | {post.get('created_at', '')}")
                        with col2:
                            sentiment = post.get('sentiment', 'Neutral')
                            if sentiment == 'Positive':
                                st.success(sentiment)
                            elif sentiment == 'Negative':
                                st.error(sentiment)
                            else:
                                st.info(sentiment)
                        st.divider()
            else:
                st.info("No social media data available")
        
        with tab4:
            st.subheader("📈 Deep Analysis")
            analysis = data.get('deep_analysis', {})
            
            if analysis:
                # Technical Analysis
                st.markdown("### Technical Indicators")
                tech = analysis.get('technical', {})
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("RSI", f"{tech.get('rsi', 0):.2f}")
                with col2:
                    st.metric("MACD", f"{tech.get('macd', 0):.2f}")
                with col3:
                    st.metric("Signal", tech.get('signal', 'N/A'))
                
                # Fundamental Analysis
                st.markdown("### Fundamental Metrics")
                fund = analysis.get('fundamental', {})
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("P/E Ratio", f"{fund.get('pe_ratio', 0):.2f}")
                with col2:
                    st.metric("Market Cap", f"${fund.get('market_cap', 0)/1e9:.2f}B")
                with col3:
                    st.metric("52W High", f"${fund.get('week_52_high', 0):.2f}")
                with col4:
                    st.metric("52W Low", f"${fund.get('week_52_low', 0):.2f}")
                
                # AI Summary
                st.markdown("### AI Summary")
                st.info(analysis.get('summary', 'No analysis available'))
            else:
                st.info("No analysis data available")
        
        with tab5:
            st.subheader("🔮 Predictive Analysis")
            predictions = data.get('predictions', {})
            
            if predictions:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Price Predictions")
                    st.metric("7-Day Forecast", f"${predictions.get('7_day', 0):.2f}")
                    st.metric("30-Day Forecast", f"${predictions.get('30_day', 0):.2f}")
                    st.metric("90-Day Forecast", f"${predictions.get('90_day', 0):.2f}")
                
                with col2:
                    st.markdown("### Confidence Levels")
                    st.progress(predictions.get('confidence_7d', 0) / 100)
                    st.caption(f"7-Day: {predictions.get('confidence_7d', 0):.1f}%")
                    st.progress(predictions.get('confidence_30d', 0) / 100)
                    st.caption(f"30-Day: {predictions.get('confidence_30d', 0):.1f}%")
                    st.progress(predictions.get('confidence_90d', 0) / 100)
                    st.caption(f"90-Day: {predictions.get('confidence_90d', 0):.1f}%")
                
                st.markdown("### Model Insights")
                st.write(predictions.get('insights', 'No insights available'))
            else:
                st.info("No prediction data available")
    else:
        st.error(f"Could not load data for {ticker}")
else:
    # Welcome screen
    st.markdown("""
    ## Welcome to Investment Research Agent! 👋
    
    This AI-powered platform helps you make informed investment decisions by analyzing:
    
    - 📊 Real-time stock prices and historical data
    - 📰 Latest news articles from trusted sources
    - 💬 Social media sentiment analysis
    - 📈 Technical and fundamental analysis
    - 🔮 AI-powered price predictions
    
    ### Getting Started
    
    1. Add a stock ticker to your watchlist (sidebar)
    2. Click on any stock to view detailed analysis
    3. Explore different tabs for comprehensive insights
    
    ### Supported Tickers
    
    - Stocks: AAPL, TSLA, NVDA, MSFT, GOOGL, etc.
    - Crypto: BTC-USD, ETH-USD, etc.
    - Forex: EURUSD=X, GBPUSD=X, etc.
    
    **Start by adding your first stock to the watchlist!** 👈
    """)
    
    # Quick add popular stocks
    st.subheader("Popular Stocks")
    cols = st.columns(5)
    popular = ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"]
    
    for i, ticker in enumerate(popular):
        with cols[i]:
            if st.button(f"➕ {ticker}", use_container_width=True):
                if add_to_watchlist(ticker):
                    st.session_state.watchlist = fetch_watchlist()
                    st.rerun()

# Footer
st.divider()
st.caption("💡 Powered by OpenAI, NewsAPI, and multiple financial data sources | Data updates in real-time")
