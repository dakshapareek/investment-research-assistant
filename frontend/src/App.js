import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StockChart from './components/StockChart';
import DataSources from './components/DataSources';
import Subscription from './components/Subscription';
import './App.css';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [ticker, setTicker] = useState('');
  const [tickerName, setTickerName] = useState('');
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [watchlist, setWatchlist] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [showSearchResults, setShowSearchResults] = useState(false);
  const [searchLoading, setSearchLoading] = useState(false);
  const [subscriptionOpen, setSubscriptionOpen] = useState(false);
  const [emailModalOpen, setEmailModalOpen] = useState(false);
  const [emailAddress, setEmailAddress] = useState('');
  const [emailSending, setEmailSending] = useState(false);
  const [emailMessage, setEmailMessage] = useState('');
  const [quickWatchlist, setQuickWatchlist] = useState([
    { symbol: 'AAPL', name: 'Apple' },
    { symbol: 'NVDA', name: 'NVIDIA' },
    { symbol: 'TSLA', name: 'Tesla' },
    { symbol: 'BTC-USD', name: 'Bitcoin' },
    { symbol: 'ETH-USD', name: 'Ethereum' }
  ]);
  const [editingWatchlist, setEditingWatchlist] = useState(false);

  useEffect(() => {
    fetchWatchlist();
    // Load quick watchlist from localStorage
    const savedQuickWatch = localStorage.getItem('quickWatchlist');
    if (savedQuickWatch) {
      try {
        const parsed = JSON.parse(savedQuickWatch);
        // Merge with defaults if crypto not present
        const hasCrypto = parsed.some(item => item.symbol.includes('-'));
        if (!hasCrypto) {
          // Add crypto to existing watchlist
          const updated = [
            ...parsed,
            { symbol: 'BTC-USD', name: 'Bitcoin' },
            { symbol: 'ETH-USD', name: 'Ethereum' }
          ];
          setQuickWatchlist(updated);
          localStorage.setItem('quickWatchlist', JSON.stringify(updated));
        } else {
          setQuickWatchlist(parsed);
        }
      } catch (e) {
        console.error('Error loading quick watchlist:', e);
      }
    }
  }, []);

  const fetchWatchlist = async () => {
    try {
      const response = await axios.get(`${API_URL}/watchlist`);
      setWatchlist(response.data.tickers || []);
    } catch (error) {
      console.error('Error fetching watchlist:', error);
    }
  };

  const searchTickers = async (query) => {
    if (!query || query.length < 1) {
      setSearchResults([]);
      setShowSearchResults(false);
      return;
    }

    setSearchLoading(true);
    try {
      const response = await axios.get(`${API_URL}/search/${query}`);
      const data = response.data;
      
      if (data.results && data.results.length > 0) {
        setSearchResults(data.results);
        setShowSearchResults(true);
      } else if (data.web_info) {
        // Company found via web search but no ticker
        const webInfo = data.web_info;
        let message = '';
        
        if (webInfo.is_private) {
          message = `Private Company: ${webInfo.description}`;
        } else if (!webInfo.exists) {
          message = 'Company not found or does not exist';
        } else {
          message = webInfo.description || 'No ticker available';
        }
        
        setSearchResults([{
          symbol: query.toUpperCase(),
          name: webInfo.is_private ? 'Private Company' : 'No Ticker Available',
          exchange: message,
          type: 'web-info',
          web_info: webInfo
        }]);
        setShowSearchResults(true);
      } else {
        // Show "no results" message with helpful hint
        const isCrypto = query.includes('-');
        const isForex = query.includes('=');
        const isIndex = query.startsWith('^');
        
        let hint = 'Try a different search term';
        if (isCrypto) {
          hint = 'Crypto format detected. Click to analyze anyway.';
        } else if (isForex) {
          hint = 'Forex format detected. Click to analyze anyway.';
        } else if (isIndex) {
          hint = 'Index format detected. Click to analyze anyway.';
        }
        
        setSearchResults([{
          symbol: query.toUpperCase(),
          name: 'No matching symbols found',
          exchange: hint,
          type: 'not-found'
        }]);
        setShowSearchResults(true);
      }
    } catch (error) {
      console.error('Error searching tickers:', error);
      setSearchResults([{
        symbol: query.toUpperCase(),
        name: 'Search unavailable',
        exchange: 'Try entering ticker directly',
        type: 'error'
      }]);
      setShowSearchResults(true);
    } finally {
      setSearchLoading(false);
    }
  };

  const handleTickerChange = (e) => {
    const value = e.target.value;
    setTicker(value);
    
    // Debounce search
    if (value.length >= 1) {
      const timeoutId = setTimeout(() => {
        searchTickers(value);
      }, 300);
      return () => clearTimeout(timeoutId);
    } else {
      setSearchResults([]);
      setShowSearchResults(false);
    }
  };

  const selectTicker = (symbol, name, type, webInfo) => {
    // Don't allow analyzing web-info results (private companies)
    if (type === 'error' || type === 'web-info') {
      return;
    }
    
    setTicker(symbol);
    setTickerName(name || symbol); // Store the stock name
    setSearchResults([]);
    setShowSearchResults(false);
    
    // Auto-analyze if it's a valid result (not a "not-found" message)
    if (type !== 'not-found') {
      analyzeStock(symbol);
    }
  };

  const analyzeStock = async (symbol) => {
    setLoading(true);
    setReport(null);
    try {
      const response = await axios.get(`${API_URL}/analyze/${symbol}`);
      setReport(response.data);
    } catch (error) {
      console.error('Error analyzing stock:', error);
      setReport({ error: 'Failed to generate report' });
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (ticker.trim()) {
      const upperTicker = ticker.toUpperCase();
      setTickerName(tickerName || upperTicker); // Use existing name or ticker as fallback
      analyzeStock(upperTicker);
    }
  };

  const getRatingColor = (rating) => {
    if (rating?.includes('Bull')) return '#10b981';
    if (rating?.includes('Bear')) return '#ef4444';
    return '#6b7280';
  };

  const handleEmailReport = async () => {
    if (!emailAddress) {
      setEmailMessage('Please enter an email address');
      return;
    }

    setEmailSending(true);
    setEmailMessage('');

    try {
      const response = await axios.post(`${API_URL}/email-report`, {
        email: emailAddress,
        report: report
      });

      if (response.data.success) {
        setEmailMessage(`✓ Report sent successfully to ${emailAddress}!`);
        setTimeout(() => {
          setEmailModalOpen(false);
          setEmailAddress('');
          setEmailMessage('');
        }, 2000);
      } else {
        setEmailMessage(`✗ ${response.data.error || 'Failed to send email'}`);
      }
    } catch (error) {
      console.error('Error sending email:', error);
      setEmailMessage(`✗ ${error.response?.data?.error || 'Failed to send email. Check backend configuration.'}`);
    } finally {
      setEmailSending(false);
    }
  };

  const addToQuickWatch = (symbol, name) => {
    if (!symbol) return;
    
    // Preserve original case for crypto/forex (contains hyphen) or convert to uppercase
    const processedSymbol = symbol.includes('-') ? symbol.toUpperCase() : symbol.toUpperCase().trim();
    const displayName = name?.trim() || processedSymbol;
    
    // Check if already exists
    if (quickWatchlist.some(item => item.symbol === processedSymbol)) {
      alert('This stock is already in your watchlist');
      return;
    }
    
    const newList = [...quickWatchlist, { symbol: processedSymbol, name: displayName }];
    setQuickWatchlist(newList);
    localStorage.setItem('quickWatchlist', JSON.stringify(newList));
    
    // Show success message
    alert(`${processedSymbol} added to watchlist!`);
  };

  const removeFromQuickWatch = (symbol) => {
    const newList = quickWatchlist.filter(item => item.symbol !== symbol);
    setQuickWatchlist(newList);
    localStorage.setItem('quickWatchlist', JSON.stringify(newList));
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="header-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 3v18h18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M18 9l-5 5-3-3-4 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <div className="header-text">
            <h1>Investment Research Platform</h1>
            <p>AI-Powered Stock Analysis & Market Intelligence</p>
          </div>
          <button className="subscription-button" onClick={() => setSubscriptionOpen(true)}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <polyline points="22,6 12,13 2,6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            Alerts
          </button>
        </div>
      </header>

      {subscriptionOpen && (
        <div className="modal-overlay" onClick={() => setSubscriptionOpen(false)}>
          <div className="modal-content subscription-modal" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setSubscriptionOpen(false)}>×</button>
            <Subscription />
          </div>
        </div>
      )}

      <div className="container">
        <div className="search-section">
          <form onSubmit={handleSubmit} className="search-form">
            <div className="search-input-wrapper">
              <input
                type="text"
                value={ticker}
                onChange={handleTickerChange}
                onFocus={() => ticker && setShowSearchResults(true)}
                onBlur={() => setTimeout(() => setShowSearchResults(false), 200)}
                placeholder="Search ticker or company (e.g., AAPL, Microsoft)"
                className="search-input"
                autoComplete="off"
              />
              {showSearchResults && searchResults.length > 0 && (
                <div className="search-results-dropdown">
                  {searchLoading && <div className="search-loading">Searching...</div>}
                  {searchResults.map((result, idx) => (
                    <div
                      key={idx}
                      className={`search-result-item ${result.type === 'not-found' || result.type === 'error' || result.type === 'web-info' ? 'result-warning' : ''}`}
                      onClick={() => selectTicker(result.symbol, result.name, result.type, result.web_info)}
                    >
                      <div className="result-symbol">{result.symbol}</div>
                      <div className="result-name">{result.name}</div>
                      {result.exchange && (
                        <div className="result-exchange">{result.exchange}</div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
            {ticker && !loading && (
              <button 
                type="button"
                className="add-to-watchlist-button"
                onClick={() => addToQuickWatch(ticker, tickerName)}
                title="Add to watchlist"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="2"/>
                  <path d="M12 8v8M8 12h8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                </svg>
              </button>
            )}
            <button type="submit" className="search-button" disabled={loading}>
              {loading ? 'Analyzing...' : 'Analyze'}
            </button>
          </form>

          {/* Keep an Eye On Box */}
          <div className="keep-eye-on-box">
            <div className="keep-eye-header">
              <h3>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style={{marginRight: '8px', verticalAlign: 'middle'}}>
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="2"/>
                </svg>
                Keep an Eye On
              </h3>
              <button 
                className="edit-watchlist-btn"
                onClick={() => setEditingWatchlist(!editingWatchlist)}
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  {editingWatchlist ? (
                    <path d="M5 13l4 4L19 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  ) : (
                    <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  )}
                </svg>
                {editingWatchlist ? 'Done' : 'Edit'}
              </button>
            </div>
            
            {editingWatchlist && (
              <p className="edit-hint">Click × to remove stocks. Use the search bar above to add new stocks.</p>
            )}
            
            <div className="popular-stocks">
              {quickWatchlist.map((stock) => (
                <div key={stock.symbol} className="stock-chip-wrapper">
                  <button 
                    className="stock-chip"
                    onClick={() => !editingWatchlist && analyzeStock(stock.symbol)}
                    disabled={loading || editingWatchlist}
                  >
                    <span className="chip-symbol">{stock.symbol}</span>
                    <span className="chip-name">{stock.name}</span>
                  </button>
                  {editingWatchlist && (
                    <button 
                      className="remove-chip-btn"
                      onClick={() => removeFromQuickWatch(stock.symbol)}
                      title="Remove"
                    >
                      ×
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Analyzing {ticker}...</p>
            <p className="loading-subtext">Fetching market data, news, and sentiment in parallel</p>
          </div>
        )}

        {report && !loading && (
          <div className="report">
            {report.error ? (
              <div className="error">{report.error}</div>
            ) : (
              <>
                <div className="report-header">
                  <h2>{report.ticker}</h2>
                  <div style={{display: 'flex', gap: '1rem', alignItems: 'center'}}>
                    <div
                      className="rating"
                      style={{ backgroundColor: getRatingColor(report.executive_summary?.rating) }}
                    >
                      {report.executive_summary?.rating}
                    </div>
                    <button className="email-report-btn" onClick={() => setEmailModalOpen(true)}>
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                        <path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                      Email Report
                    </button>
                  </div>
                </div>

                {/* Stock Chart Section - Now with Dual View */}
                {report.chart_data && report.quote && (
                  <>
                    {/* Data Source Warning */}
                    {(report.chart_data.source === 'Mock Data (Configure API keys for real data)' || 
                      report.quote.source === 'Mock Data') && (
                      <div className="data-warning">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style={{marginRight: '8px'}}>
                          <path d="M12 9v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="#FF9500" strokeWidth="2" strokeLinecap="round"/>
                        </svg>
                        <div>
                          <strong>Using Mock Data</strong>
                          <p>Configure API keys in backend/.env for real market data. See API_SETUP_GUIDE.md for instructions.</p>
                        </div>
                      </div>
                    )}
                    
                    <StockChart 
                      chartData={report.chart_data} 
                      quote={report.quote}
                      predictions={report.predictions}
                    />
                  </>
                )}

                <section className="report-section">
                  <div className="section-header">
                    <svg className="section-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
                      <path d="M9 11l3 3L22 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    <h3>Executive Summary</h3>
                  </div>
                  <p className="recommendation">{report.executive_summary?.recommendation}</p>
                </section>

                {/* Combined LLM Sentiment Analysis */}
                {report.combined_sentiment && (
                  <section className="report-section sentiment-section">
                    <div className="section-header">
                      <svg className="section-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
                        <path d="M8 14s1.5 2 4 2 4-2 4-2" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                        <line x1="9" y1="9" x2="9.01" y2="9" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                        <line x1="15" y1="9" x2="15.01" y2="9" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      </svg>
                      <h3>AI Sentiment Analysis</h3>
                    </div>
                    {report.combined_sentiment.sources && report.combined_sentiment.sources[0]?.details?.llm_used && (
                      <div className="ai-badge">
                        ✨ Powered by Google Gemini AI
                      </div>
                    )}
                    <div className="sentiment-overview">
                      <div className={`sentiment-badge ${report.combined_sentiment.overall_sentiment}`}>
                        {report.combined_sentiment.overall_sentiment.toUpperCase()}
                      </div>
                      <div className="sentiment-score">
                        Score: {report.combined_sentiment.average_score} 
                        <span className="confidence"> (Confidence: {(report.combined_sentiment.confidence * 100).toFixed(0)}%)</span>
                      </div>
                    </div>
                    
                    {report.combined_sentiment.sources && report.combined_sentiment.sources.length > 0 && (
                      <div className="sentiment-sources">
                        {report.combined_sentiment.sources.map((source, idx) => (
                          <div key={idx} className="source-card">
                            <h4>{source.source}</h4>
                            <div className={`source-sentiment ${source.sentiment}`}>
                              {source.sentiment}
                            </div>
                            <div className="source-details">
                              <span>Score: {source.score}</span>
                              <span>Confidence: {(source.confidence * 100).toFixed(0)}%</span>
                            </div>
                            {source.details && (
                              <div className="source-stats">
                                <span>Bullish: {source.details.bullish_count}</span>
                                <span>Bearish: {source.details.bearish_count}</span>
                                <span>Neutral: {source.details.neutral_count}</span>
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    )}
                  </section>
                )}

                <section className="report-section">
                  <div className="section-header">
                    <svg className="section-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
                      <path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    <h3>Social Pulse</h3>
                  </div>
                  {report.social_pulse?.error ? (
                    <p className="error-text">{report.social_pulse.error}</p>
                  ) : (
                    <>
                      <div className="data-grid">
                        <div className="data-item">
                          <span className="label">Sentiment:</span>
                          <span className="value">{report.social_pulse?.sentiment || 'N/A'}</span>
                        </div>
                        <div className="data-item">
                          <span className="label">Mentions:</span>
                          <span className="value">{report.social_pulse?.mentions || 0}</span>
                        </div>
                        <div className="data-item">
                          <span className="label">Score:</span>
                          <span className="value">{report.social_pulse?.sentiment_score || 0}</span>
                        </div>
                      </div>
                      {report.social_pulse?.top_posts && report.social_pulse.top_posts.length > 0 && (
                        <div className="top-posts">
                          <h4>Top Posts</h4>
                          {report.social_pulse.top_posts.map((post, idx) => (
                            <div key={idx} className="post">
                              <p>{post.title}</p>
                              <span className="post-meta">
                                r/{post.subreddit} • {post.score} upvotes • {post.comments} comments
                              </span>
                            </div>
                          ))}
                        </div>
                      )}
                      {(!report.social_pulse?.top_posts || report.social_pulse.top_posts.length === 0) && (
                        <p className="info-text">Configure Reddit API credentials in backend/.env to see social sentiment data</p>
                      )}
                      {report.social_pulse?.detailed_summary && (
                        <div className="detailed-summary">
                          <h4>Detailed Analysis</h4>
                          <p className="summary-text">{report.social_pulse.detailed_summary}</p>
                        </div>
                      )}
                    </>
                  )}
                </section>

                <section className="report-section">
                  <div className="section-header">
                    <svg className="section-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
                      <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    <h3>News Summary</h3>
                  </div>
                  <p>{report.news_summary?.summary}</p>
                  {report.news_summary?.detailed_summary && (
                    <div className="detailed-summary">
                      <h4>In-Depth Analysis</h4>
                      <p className="summary-text">{report.news_summary.detailed_summary}</p>
                    </div>
                  )}
                  {report.news_summary?.headlines && report.news_summary.headlines.length > 0 && (
                    <div className="headlines-section">
                      <h4>Recent Headlines</h4>
                      <ul className="headlines">
                        {report.news_summary.headlines.map((headline, idx) => {
                          // Check if headline is an object with URL or just a string
                          if (typeof headline === 'object' && headline !== null) {
                            // It's an object, render as link
                            const url = headline.url || '#';
                            const title = headline.title || String(headline);
                            return (
                              <li key={idx} className="headline-item">
                                <a href={url} target="_blank" rel="noopener noreferrer" className="headline-link">
                                  {title}
                                  <svg className="external-link-icon" width="14" height="14" viewBox="0 0 24 24" fill="none">
                                    <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                                  </svg>
                                </a>
                                {headline.source && <span className="headline-source">{headline.source}</span>}
                                {headline.date && <span className="headline-date">{headline.date}</span>}
                              </li>
                            );
                          } else {
                            // Fallback for string headlines
                            const headlineText = typeof headline === 'string' ? headline : String(headline);
                            return <li key={idx} className="headline-item">{headlineText}</li>;
                          }
                        })}
                      </ul>
                    </div>
                  )}
                </section>

                <div className="report-footer">
                  <small>Generated: {new Date(report.generated_at).toLocaleString()}</small>
                </div>

                {/* Data Sources */}
                <DataSources report={report} />
              </>
            )}
          </div>
        )}
      </div>

      {/* Email Modal */}
      {emailModalOpen && (
        <div className="modal-overlay" onClick={() => setEmailModalOpen(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>📧 Email Report</h3>
              <button className="modal-close" onClick={() => setEmailModalOpen(false)}>×</button>
            </div>
            <div className="modal-body">
              <p>Send the {report?.ticker} investment report to your email</p>
              <input
                type="email"
                className="email-input"
                placeholder="Enter your email address"
                value={emailAddress}
                onChange={(e) => setEmailAddress(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleEmailReport()}
              />
              {emailMessage && (
                <div className={`email-message ${emailMessage.includes('✓') ? 'success' : 'error'}`}>
                  {emailMessage}
                </div>
              )}
            </div>
            <div className="modal-footer">
              <button className="modal-btn cancel" onClick={() => setEmailModalOpen(false)}>
                Cancel
              </button>
              <button 
                className="modal-btn send" 
                onClick={handleEmailReport}
                disabled={emailSending}
              >
                {emailSending ? 'Sending...' : 'Send Email'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
