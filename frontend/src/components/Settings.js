import React, { useState, useEffect } from 'react';
import './Settings.css';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const Settings = ({ isOpen, onClose }) => {
  const [models, setModels] = useState([]);
  const [currentModel, setCurrentModel] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  useEffect(() => {
    if (isOpen) {
      fetchModels();
    }
  }, [isOpen]);

  const fetchModels = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${API_URL}/models`);
      setModels(response.data.models || []);
      setCurrentModel(response.data.current_model || '');
    } catch (err) {
      setError('Failed to fetch models. Make sure Google API key is configured.');
      console.error('Error fetching models:', err);
    } finally {
      setLoading(false);
    }
  };

  const selectModel = async (modelName) => {
    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      const response = await axios.post(`${API_URL}/models/select`, {
        model: modelName
      });
      setCurrentModel(modelName);
      setSuccess(`Successfully switched to ${modelName}`);
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError('Failed to switch model');
      console.error('Error selecting model:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="settings-overlay" onClick={onClose}>
      <div className="settings-panel" onClick={(e) => e.stopPropagation()}>
        <div className="settings-header">
          <h2>Settings</h2>
          <button className="close-button" onClick={onClose}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            </svg>
          </button>
        </div>

        <div className="settings-content">
          <section className="settings-section">
            <h3>AI Model Selection</h3>
            <p className="section-description">
              Choose which Google Gemini model to use for analysis. Different models offer varying levels of performance, speed, and capabilities.
            </p>

            {error && <div className="error-message">{error}</div>}
            {success && <div className="success-message">{success}</div>}

            {loading && <div className="loading-spinner">Loading models...</div>}

            {!loading && models.length > 0 && (
              <div className="models-list">
                {models.map((model) => (
                  <div
                    key={model.name}
                    className={`model-card ${currentModel === model.name ? 'active' : ''}`}
                    onClick={() => selectModel(model.name)}
                  >
                    <div className="model-header">
                      <div className="model-name">
                        {model.display_name || model.name}
                        {currentModel === model.name && (
                          <span className="current-badge">Current</span>
                        )}
                      </div>
                      <div className="model-id">{model.name}</div>
                    </div>
                    {model.description && (
                      <div className="model-description">{model.description}</div>
                    )}
                    <div className="model-specs">
                      {model.input_token_limit > 0 && (
                        <span className="spec">
                          Input: {(model.input_token_limit / 1000).toFixed(0)}K tokens
                        </span>
                      )}
                      {model.output_token_limit > 0 && (
                        <span className="spec">
                          Output: {(model.output_token_limit / 1000).toFixed(0)}K tokens
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {!loading && models.length === 0 && !error && (
              <div className="no-models">
                <p>No models available. Please configure your Google API key in backend/.env</p>
              </div>
            )}
          </section>

          <section className="settings-section">
            <h3>Data Sources</h3>
            <p className="section-description">
              The platform scrapes data from multiple sources using web search:
            </p>
            <ul className="sources-list">
              <li>
                <strong>Social Media:</strong> Reddit, Twitter/X, Facebook, StockTwits, Yahoo Finance Community
              </li>
              <li>
                <strong>News Outlets:</strong> Bloomberg, Reuters, CNBC, MarketWatch, WSJ, Financial Times
              </li>
              <li>
                <strong>Analysis Sites:</strong> Seeking Alpha, Motley Fool, Zacks, Yahoo Finance
              </li>
              <li>
                <strong>Official Sources:</strong> NYSE, NASDAQ, Company Press Releases
              </li>
            </ul>
          </section>

          <section className="settings-section">
            <h3>API Configuration</h3>
            <p className="section-description">
              Configure API keys in <code>backend/.env</code> file:
            </p>
            <ul className="config-list">
              <li><code>GOOGLE_API_KEY</code> - Required for AI analysis</li>
              <li><code>FINANCIAL_MODELING_PREP_API_KEY</code> - Stock data</li>
              <li><code>ALPHA_VANTAGE_API_KEY</code> - Stock data fallback</li>
            </ul>
          </section>
        </div>
      </div>
    </div>
  );
};

export default Settings;
