import React, { useState } from 'react';
import './DataSources.css';

const DataSources = ({ report }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const getSourceUrl = (sourceName) => {
    if (!sourceName) return '#';
    
    // Handle MCP Server with provider info
    if (sourceName.startsWith('MCP Server')) {
      return 'https://modelcontextprotocol.io';
    }
    
    const sourceMap = {
      'Financial Modeling Prep': 'https://financialmodelingprep.com',
      'Alpha Vantage': 'https://www.alphavantage.co',
      'Finnhub': 'https://finnhub.io',
      'Polygon': 'https://polygon.io',
      'Marketstack': 'https://marketstack.com',
      'EODHD': 'https://eodhistoricaldata.com',
      'Yahoo Finance': 'https://finance.yahoo.com',
      'Multi-Source Web Search via LLM': 'https://ai.google.dev',
      'Reddit': 'https://www.reddit.com'
    };
    
    return sourceMap[sourceName] || '#';
  };

  const renderIcon = (iconType) => {
    const icons = {
      chart: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path d="M3 3v18h18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M18 9l-5 5-3-3-4 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      ),
      trending: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
          <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <polyline points="17 6 23 6 23 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      ),
      social: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      ),
      news: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      ),
      ai: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
          <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
          <path d="M8 14s1.5 2 4 2 4-2 4-2" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          <line x1="9" y1="9" x2="9.01" y2="9" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          <line x1="15" y1="9" x2="15.01" y2="9" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
        </svg>
      ),
      forecast: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
          <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
          <polyline points="12 6 12 12 16 14" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      )
    };
    
    return icons[iconType] || icons.chart;
  };

  // Extract actual data sources from report
  const getDataSources = () => {
    const sources = [];
    
    // Stock Data Source
    if (report?.quote) {
      sources.push({
        name: report.quote.source || 'Stock Data API',
        type: 'Market Data',
        url: getSourceUrl(report.quote.source),
        description: `Real-time quote: $${report.quote.price?.toFixed(2) || 'N/A'}`,
        used: true,
        iconType: 'chart'
      });
    }
    
    // Historical Data Source
    if (report?.chart_data && report.chart_data.source) {
      sources.push({
        name: report.chart_data.source,
        type: 'Historical Data',
        url: getSourceUrl(report.chart_data.source),
        description: `${report.chart_data.close?.length || 0} days of historical prices`,
        used: true,
        iconType: 'trending'
      });
    }
    
    // Social Media Source
    if (report?.social_pulse && report.social_pulse.source) {
      sources.push({
        name: report.social_pulse.source,
        type: 'Social Sentiment',
        url: 'https://www.reddit.com',
        description: `${report.social_pulse.mentions || 0} posts analyzed`,
        used: true,
        iconType: 'social'
      });
    }
    
    // News Source
    if (report?.news_summary && report.news_summary.source) {
      sources.push({
        name: report.news_summary.source,
        type: 'News Analysis',
        url: getSourceUrl(report.news_summary.source),
        description: `${report.news_summary.headlines?.length || 0} recent headlines`,
        used: true,
        iconType: 'news'
      });
    }
    
    // AI Sentiment
    if (report?.combined_sentiment) {
      sources.push({
        name: 'Google Gemini AI',
        type: 'Sentiment Analysis',
        url: 'https://ai.google.dev',
        description: `AI-powered analysis (Score: ${report.combined_sentiment.average_score?.toFixed(2) || 0})`,
        used: true,
        iconType: 'ai'
      });
    }
    
    // Predictions
    if (report?.predictions) {
      sources.push({
        name: 'AI Predictive Model',
        type: 'Price Forecasting',
        url: '#',
        description: `${report.predictions.predictions?.scenarios?.length || 0} forecast scenarios`,
        used: true,
        iconType: 'forecast'
      });
    }
    
    return sources;
  };

  const sources = getDataSources();
  const activeSources = sources.filter(s => s.used);

  return (
    <div className="data-sources-container">
      <button 
        className="sources-toggle"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <svg className="sources-icon-svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M4 19.5A2.5 2.5 0 016.5 17H20" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
        <span className="sources-text">
          Data Sources ({activeSources.length})
        </span>
        <span className={`expand-icon ${isExpanded ? 'expanded' : ''}`}>▼</span>
      </button>

      {isExpanded && (
        <div className="sources-panel">
          <h3>Data Sources & Citations</h3>
          <p className="sources-disclaimer">
            This report aggregates data from multiple sources. Always verify information independently before making investment decisions.
          </p>
          
          <div className="sources-grid">
            {sources.map((source, idx) => (
              <div 
                key={idx} 
                className={`source-card ${source.used ? 'active' : 'inactive'}`}
              >
                <div className="source-header">
                  <span className="source-icon">{renderIcon(source.iconType)}</span>
                  <div className="source-title">
                    <h4>{source.name}</h4>
                    <span className={`source-badge ${source.used ? 'used' : 'unused'}`}>
                      {source.used ? '✓ USED' : 'Not Used'}
                    </span>
                  </div>
                </div>
                <div className="source-type">{source.type}</div>
                <p className="source-description">{source.description}</p>
                {source.url !== '#' && (
                  <a 
                    href={source.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="source-link"
                  >
                    Visit Source →
                  </a>
                )}
              </div>
            ))}
          </div>

          <div className="api-setup-notice">
            <h4>Want More Data?</h4>
            <p>
              Configure Google Gemini API key to unlock AI-powered analysis and web scraping capabilities.
              See <code>API_SETUP_GUIDE.md</code> for detailed instructions.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default DataSources;
