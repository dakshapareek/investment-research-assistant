import React, { useState, useEffect } from 'react';
import './Subscription.css';

function Subscription() {
  const [email, setEmail] = useState('');
  const [emailSubmitted, setEmailSubmitted] = useState(false);
  const [tickers, setTickers] = useState('');
  const [threshold, setThreshold] = useState(2.0);
  const [subscription, setSubscription] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    // Load subscription from localStorage if exists
    const savedEmail = localStorage.getItem('subscriptionEmail');
    if (savedEmail) {
      setEmail(savedEmail);
      setEmailSubmitted(true);
      checkSubscription(savedEmail);
    }
  }, []);

  const checkSubscription = async (emailToCheck) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:5000/api/subscription/${encodeURIComponent(emailToCheck)}`);
      const data = await response.json();
      
      if (data.success && data.subscription) {
        setSubscription(data.subscription);
        setTickers(data.subscription.tickers.join(', '));
        setThreshold(data.subscription.threshold);
      } else {
        setSubscription(null);
      }
    } catch (error) {
      console.error('Error checking subscription:', error);
      setSubscription(null);
    } finally {
      setLoading(false);
    }
  };

  const handleEmailSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      // Check if email exists
      await checkSubscription(email);
      setEmailSubmitted(true);
      localStorage.setItem('subscriptionEmail', email);
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to check subscription. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  const handleSubscribe = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      // Parse tickers
      const tickerList = tickers
        .split(',')
        .map(t => t.trim().toUpperCase())
        .filter(t => t.length > 0);

      if (tickerList.length === 0) {
        setMessage({ type: 'error', text: 'Please enter at least one ticker symbol' });
        setLoading(false);
        return;
      }

      const response = await fetch('http://localhost:5000/api/subscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          tickers: tickerList,
          threshold: parseFloat(threshold)
        }),
      });

      const data = await response.json();

      if (data.success) {
        setSubscription(data.subscription);
        setMessage({ 
          type: 'success', 
          text: `✓ Successfully subscribed! You'll receive daily alerts when stocks move >${threshold}%` 
        });
      } else {
        setMessage({ type: 'error', text: data.error || 'Subscription failed' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to subscribe. Please try again.' });
      console.error('Subscribe error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUnsubscribe = async () => {
    if (!window.confirm('Are you sure you want to unsubscribe from daily alerts?')) {
      return;
    }

    setLoading(true);
    setMessage(null);

    try {
      const response = await fetch('http://localhost:5000/api/unsubscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          id: subscription.id
        }),
      });

      const data = await response.json();

      if (data.success) {
        setSubscription(null);
        setTickers('');
        setMessage({ type: 'success', text: '✓ Successfully unsubscribed from daily alerts' });
      } else {
        setMessage({ type: 'error', text: data.error || 'Unsubscribe failed' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to unsubscribe. Please try again.' });
      console.error('Unsubscribe error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChangeEmail = () => {
    setEmailSubmitted(false);
    setSubscription(null);
    setTickers('');
    localStorage.removeItem('subscriptionEmail');
  };

  return (
    <div className="subscription-container">
      <div className="subscription-card">
        <div className="subscription-header">
          <div className="subscription-icon">📧</div>
          <h2>Daily Stock Alerts</h2>
          <p>Get automated emails when your stocks move significantly</p>
        </div>

        {message && (
          <div className={`subscription-message ${message.type}`}>
            {message.text}
          </div>
        )}

        {!emailSubmitted ? (
          <form onSubmit={handleEmailSubmit} className="subscription-form">
            <div className="form-group">
              <label htmlFor="email">Enter your email to get started</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your.email@example.com"
                required
              />
              <small>We'll check if you have an existing subscription</small>
            </div>

            <button 
              type="submit" 
              className="btn-subscribe"
              disabled={loading}
            >
              {loading ? 'Checking...' : 'Continue'}
            </button>
          </form>
        ) : loading ? (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Checking your subscription...</p>
          </div>
        ) : subscription ? (
          <div className="subscription-active">
            <div className="email-display">
              <span className="email-label">Email:</span>
              <span className="email-value">{email}</span>
              <button className="btn-change-email" onClick={handleChangeEmail}>
                Change Email
              </button>
            </div>

            <div className="subscription-status">
              <span className="status-badge active">✓ Active Subscription</span>
            </div>

            <div className="subscription-details">
              <div className="detail-row">
                <span className="detail-label">Watching:</span>
                <span className="detail-value">{subscription.tickers.join(', ')}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Alert Threshold:</span>
                <span className="detail-value">{subscription.threshold}% change</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Last Alert:</span>
                <span className="detail-value">
                  {subscription.last_sent 
                    ? new Date(subscription.last_sent).toLocaleDateString()
                    : 'Never'}
                </span>
              </div>
            </div>

            <button 
              className="btn-unsubscribe"
              onClick={handleUnsubscribe}
              disabled={loading}
            >
              {loading ? 'Processing...' : 'Unsubscribe'}
            </button>
          </div>
        ) : (
          <div className="subscription-form-container">
            <div className="email-display">
              <span className="email-label">Email:</span>
              <span className="email-value">{email}</span>
              <button className="btn-change-email" onClick={handleChangeEmail}>
                Change Email
              </button>
            </div>

            <div className="no-subscription-message">
              <p>No active subscription found for this email.</p>
              <p>Subscribe below to start receiving daily stock alerts!</p>
            </div>

            <form onSubmit={handleSubscribe} className="subscription-form">
              <div className="form-group">
                <label htmlFor="tickers">Stock Tickers</label>
                <input
                  type="text"
                  id="tickers"
                  value={tickers}
                  onChange={(e) => setTickers(e.target.value)}
                  placeholder="AAPL, MSFT, GOOGL, TSLA"
                  required
                />
                <small>Comma-separated list of stock symbols</small>
              </div>

              <div className="form-group">
                <label htmlFor="threshold">Alert Threshold (%)</label>
                <input
                  type="number"
                  id="threshold"
                  value={threshold}
                  onChange={(e) => setThreshold(e.target.value)}
                  min="0.1"
                  max="50"
                  step="0.1"
                  required
                />
                <small>Get alerts when stocks move more than this percentage</small>
              </div>

              <button 
                type="submit" 
                className="btn-subscribe"
                disabled={loading}
              >
                {loading ? 'Subscribing...' : 'Subscribe to Daily Alerts'}
              </button>
            </form>
          </div>
        )}

        <div className="subscription-info">
          <h3>How it works:</h3>
          <ul>
            <li>📊 We check your stocks daily at 9 AM</li>
            <li>🚨 You get an email if any stock moves beyond your threshold</li>
            <li>📧 Emails include price changes and key metrics</li>
            <li>🔒 Your email is secure and never shared</li>
            <li>❌ Unsubscribe anytime with one click</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Subscription;
