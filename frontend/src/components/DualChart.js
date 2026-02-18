import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import './DualChart.css';

const DualChart = ({ chartData, quote, predictions }) => {
  const [viewMode, setViewMode] = useState('combined'); // 'combined', 'actual', 'comparison'

  if (!chartData || !chartData.timestamps) {
    return <div className="chart-error">No chart data available</div>;
  }

  // Prepare historical actual data
  const historicalData = chartData.timestamps.map((timestamp, index) => ({
    date: new Date(timestamp * 1000),
    dateStr: new Date(timestamp * 1000).toLocaleDateString(),
    actualPrice: chartData.close[index],
  })).filter(d => d.actualPrice !== null);

  // Add current price if available
  if (quote && quote.price) {
    const lastHistoricalDate = historicalData.length > 0 ? historicalData[historicalData.length - 1].date : null;
    const now = new Date();
    
    if (lastHistoricalDate) {
      const lastHistoricalDateOnly = new Date(lastHistoricalDate.getFullYear(), lastHistoricalDate.getMonth(), lastHistoricalDate.getDate());
      const todayDateOnly = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      
      if (lastHistoricalDateOnly < todayDateOnly) {
        historicalData.push({
          date: now,
          dateStr: now.toLocaleDateString(),
          actualPrice: quote.price,
        });
      } else {
        historicalData[historicalData.length - 1].actualPrice = quote.price;
      }
    }
  }

  // Prepare prediction data
  let predictionData = [];
  if (predictions && predictions.predictions?.daily_forecast) {
    predictionData = predictions.predictions.daily_forecast.map(pred => ({
      date: new Date(pred.date),
      dateStr: new Date(pred.date).toLocaleDateString(),
      predictedPrice: pred.predicted_price,
      upperBound: pred.upper_bound,
      lowerBound: pred.lower_bound,
    }));
  }

  // Combine data for comparison view
  const combinedData = [...historicalData];
  
  // Add predictions starting from last historical point
  if (predictionData.length > 0 && historicalData.length > 0) {
    const lastHistorical = historicalData[historicalData.length - 1];
    
    // Add connector point
    combinedData.push({
      date: lastHistorical.date,
      dateStr: lastHistorical.dateStr,
      actualPrice: lastHistorical.actualPrice,
      predictedPrice: lastHistorical.actualPrice,
    });
    
    // Add prediction points
    predictionData.forEach(pred => {
      combinedData.push({
        date: pred.date,
        dateStr: pred.dateStr,
        predictedPrice: pred.predictedPrice,
        upperBound: pred.upperBound,
        lowerBound: pred.lowerBound,
      });
    });
  }

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="dual-tooltip">
          <p className="tooltip-date">{data.dateStr}</p>
          {data.actualPrice && (
            <p className="tooltip-actual">Actual: ${data.actualPrice?.toFixed(2)}</p>
          )}
          {data.predictedPrice && (
            <p className="tooltip-predicted">Predicted: ${data.predictedPrice?.toFixed(2)}</p>
          )}
          {data.actualPrice && data.predictedPrice && (
            <p className="tooltip-diff">
              Diff: ${Math.abs(data.actualPrice - data.predictedPrice).toFixed(2)} 
              ({((Math.abs(data.actualPrice - data.predictedPrice) / data.actualPrice) * 100).toFixed(2)}%)
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="dual-chart-container">
      <div className="dual-chart-header">
        <div className="view-mode-selector">
          <button
            className={`mode-btn ${viewMode === 'combined' ? 'active' : ''}`}
            onClick={() => setViewMode('combined')}
          >
            Combined View
          </button>
          <button
            className={`mode-btn ${viewMode === 'split' ? 'active' : ''}`}
            onClick={() => setViewMode('split')}
          >
            Split View
          </button>
        </div>
      </div>

      {viewMode === 'combined' ? (
        <div className="chart-wrapper">
          <ResponsiveContainer width="100%" height={500}>
            <LineChart data={combinedData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis 
                dataKey="dateStr" 
                stroke="#8E8E93"
                tick={{ fontSize: 11, fill: '#8E8E93' }}
                interval={Math.floor(combinedData.length / 8)}
              />
              <YAxis 
                stroke="#8E8E93"
                tick={{ fontSize: 11, fill: '#8E8E93' }}
                domain={['auto', 'auto']}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              
              {/* Actual Price Line */}
              <Line 
                type="monotone" 
                dataKey="actualPrice" 
                stroke="#34C759"
                strokeWidth={3}
                dot={false}
                name="Actual Price"
                connectNulls={false}
              />
              
              {/* Predicted Price Line */}
              <Line 
                type="monotone" 
                dataKey="predictedPrice" 
                stroke="#007AFF"
                strokeWidth={2.5}
                strokeDasharray="5 5"
                dot={false}
                name="Predicted Price"
                connectNulls={true}
              />
              
              {/* Confidence Bounds */}
              <Line 
                type="monotone" 
                dataKey="upperBound" 
                stroke="#007AFF"
                strokeWidth={1}
                strokeOpacity={0.3}
                dot={false}
                name="Upper Bound"
                connectNulls={true}
              />
              <Line 
                type="monotone" 
                dataKey="lowerBound" 
                stroke="#007AFF"
                strokeWidth={1}
                strokeOpacity={0.3}
                dot={false}
                name="Lower Bound"
                connectNulls={true}
              />
            </LineChart>
          </ResponsiveContainer>
          
          <div className="chart-legend-custom">
            <div className="legend-item">
              <div className="legend-line actual-line"></div>
              <span>Actual Historical Prices</span>
            </div>
            <div className="legend-item">
              <div className="legend-line predicted-line"></div>
              <span>AI Predicted Prices</span>
            </div>
            <div className="legend-item">
              <div className="legend-line confidence-line"></div>
              <span>95% Confidence Range</span>
            </div>
          </div>
        </div>
      ) : (
        <div className="split-charts">
          {/* Actual Prices Chart */}
          <div className="chart-half">
            <h4>📊 Actual Historical Prices</h4>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={historicalData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis 
                  dataKey="dateStr" 
                  stroke="#8E8E93"
                  tick={{ fontSize: 10, fill: '#8E8E93' }}
                  interval={Math.floor(historicalData.length / 6)}
                />
                <YAxis 
                  stroke="#8E8E93"
                  tick={{ fontSize: 10, fill: '#8E8E93' }}
                  domain={['auto', 'auto']}
                />
                <Tooltip 
                  contentStyle={{ 
                    background: 'rgba(28, 28, 30, 0.98)', 
                    border: '1px solid rgba(255,255,255,0.2)',
                    borderRadius: '8px'
                  }}
                />
                <Line 
                  type="monotone" 
                  dataKey="actualPrice" 
                  stroke="#34C759"
                  strokeWidth={3}
                  dot={false}
                  name="Actual Price"
                />
              </LineChart>
            </ResponsiveContainer>
            <div className="chart-description">
              <p>Real market prices showing actual stock performance over time.</p>
            </div>
          </div>

          {/* Predicted vs Actual Chart */}
          <div className="chart-half">
            <h4>🔮 Predicted vs Actual Comparison</h4>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={combinedData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis 
                  dataKey="dateStr" 
                  stroke="#8E8E93"
                  tick={{ fontSize: 10, fill: '#8E8E93' }}
                  interval={Math.floor(combinedData.length / 6)}
                />
                <YAxis 
                  stroke="#8E8E93"
                  tick={{ fontSize: 10, fill: '#8E8E93' }}
                  domain={['auto', 'auto']}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="actualPrice" 
                  stroke="#34C759"
                  strokeWidth={2}
                  dot={false}
                  name="Actual"
                  connectNulls={false}
                />
                <Line 
                  type="monotone" 
                  dataKey="predictedPrice" 
                  stroke="#007AFF"
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  dot={false}
                  name="Predicted"
                  connectNulls={true}
                />
              </LineChart>
            </ResponsiveContainer>
            <div className="chart-description">
              <p>Compare AI predictions with actual outcomes to see forecast accuracy.</p>
            </div>
          </div>
        </div>
      )}

      {/* Accuracy Metrics */}
      {predictions && (
        <div className="accuracy-metrics">
          <h4>Prediction Accuracy Insights</h4>
          <div className="metrics-grid">
            <div className="metric-card">
              <span className="metric-label">Confidence Level</span>
              <span className="metric-value">{predictions.confidence_level}%</span>
            </div>
            <div className="metric-card">
              <span className="metric-label">Forecast Horizon</span>
              <span className="metric-value">90 Days</span>
            </div>
            <div className="metric-card">
              <span className="metric-label">Model</span>
              <span className="metric-value">AI-Powered</span>
            </div>
          </div>
          <p className="accuracy-note">
            💡 Predictions are based on historical trends, volatility, and market sentiment. 
            Actual prices may diverge due to unexpected market events, news, or economic changes.
          </p>
        </div>
      )}
    </div>
  );
};

export default DualChart;
