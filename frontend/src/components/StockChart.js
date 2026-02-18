import React, { useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import './StockChart.css';

const StockChart = ({ chartData, quote, predictions }) => {
  const [timeRange, setTimeRange] = useState('1Y');
  const [showPredictions, setShowPredictions] = useState(true);

  if (!chartData || !chartData.timestamps) {
    return <div className="chart-error">No chart data available</div>;
  }

  const filterDataByRange = (range) => {
    // Historical data
    const historicalData = chartData.timestamps.map((timestamp, index) => ({
      date: new Date(timestamp * 1000),
      dateStr: new Date(timestamp * 1000).toLocaleDateString(),
      actualPrice: chartData.close[index],
      volume: chartData.volume[index],
      high: chartData.high[index],
      low: chartData.low[index],
      isPrediction: false,
      isHistorical: true
    })).filter(d => d.actualPrice !== null);

    // Add current real-time price as the most recent point if it's newer than last historical
    if (quote && quote.price) {
      const lastHistoricalDate = historicalData.length > 0 ? historicalData[historicalData.length - 1].date : null;
      const now = new Date();
      
      // Only add if we have historical data and current price is from today
      if (lastHistoricalDate) {
        const lastHistoricalDateOnly = new Date(lastHistoricalDate.getFullYear(), lastHistoricalDate.getMonth(), lastHistoricalDate.getDate());
        const todayDateOnly = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        
        // If last historical data is from a previous day, add today's current price
        if (lastHistoricalDateOnly < todayDateOnly) {
          historicalData.push({
            date: now,
            dateStr: now.toLocaleDateString(),
            actualPrice: quote.price,
            volume: quote.volume || null,
            high: quote.dayHigh || quote.price,
            low: quote.dayLow || quote.price,
            isPrediction: false,
            isHistorical: true,
            isCurrentPrice: true
          });
        } else {
          // If last historical is from today, update it with current price
          historicalData[historicalData.length - 1] = {
            ...historicalData[historicalData.length - 1],
            actualPrice: quote.price,
            high: quote.dayHigh || historicalData[historicalData.length - 1].high,
            low: quote.dayLow || historicalData[historicalData.length - 1].low,
            volume: quote.volume || historicalData[historicalData.length - 1].volume,
            isCurrentPrice: true
          };
        }
      }
    }

    // Get the last actual price and date for connecting predictions
    const lastHistorical = historicalData[historicalData.length - 1];
    
    // Add prediction data if available and enabled
    let predictionData = [];
    if (predictions && showPredictions && predictions.predictions?.daily_forecast) {
      predictionData = predictions.predictions.daily_forecast.map(pred => ({
        date: new Date(pred.date),
        dateStr: new Date(pred.date).toLocaleDateString(),
        predictedPrice: pred.predicted_price,
        upperBound: pred.upper_bound,
        lowerBound: pred.lower_bound,
        isPrediction: true,
        isHistorical: false
      }));
      
      // Add a connecting point at the boundary (last historical point)
      if (lastHistorical && predictionData.length > 0) {
        predictionData.unshift({
          date: lastHistorical.date,
          dateStr: lastHistorical.dateStr,
          actualPrice: lastHistorical.actualPrice,
          predictedPrice: lastHistorical.actualPrice,
          upperBound: lastHistorical.actualPrice,
          lowerBound: lastHistorical.actualPrice,
          isPrediction: false,
          isHistorical: true,
          isConnector: true
        });
      }
    }

    const fullData = [...historicalData, ...predictionData];

    const now = new Date();
    let cutoffDate;

    switch(range) {
      case '1D':
        cutoffDate = new Date(now.getTime() - 1 * 24 * 60 * 60 * 1000);
        break;
      case '1W':
        cutoffDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
        break;
      case '1M':
        cutoffDate = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
        break;
      case '3M':
        cutoffDate = new Date(now.getTime() - 90 * 24 * 60 * 60 * 1000);
        break;
      case '6M':
        cutoffDate = new Date(now.getTime() - 180 * 24 * 60 * 60 * 1000);
        break;
      case '1Y':
        cutoffDate = new Date(now.getTime() - 365 * 24 * 60 * 60 * 1000);
        break;
      case 'ALL':
        return fullData;
      default:
        return fullData;
    }

    return fullData.filter(d => d.date >= cutoffDate);
  };

  const data = filterDataByRange(timeRange);
  const performance = chartData.performance || {};
  const isPositive = quote?.change >= 0;

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="custom-tooltip">
          <p className="tooltip-date">{data.dateStr}</p>
          {data.isPrediction ? (
            <>
              <p className="tooltip-label">🔮 Forecast</p>
              <p className="tooltip-price prediction">Predicted: ${data.predictedPrice?.toFixed(2)}</p>
              {data.upperBound && <p className="tooltip-detail">Upper: ${data.upperBound?.toFixed(2)}</p>}
              {data.lowerBound && <p className="tooltip-detail">Lower: ${data.lowerBound?.toFixed(2)}</p>}
            </>
          ) : (
            <>
              <p className="tooltip-label">📊 {data.isCurrentPrice ? 'Current Price' : 'Actual'}</p>
              <p className="tooltip-price">${data.actualPrice?.toFixed(2)}</p>
              {data.high && <p className="tooltip-detail">High: ${data.high?.toFixed(2)}</p>}
              {data.low && <p className="tooltip-detail">Low: ${data.low?.toFixed(2)}</p>}
              {data.volume && <p className="tooltip-detail">Vol: {formatVolume(data.volume)}</p>}
            </>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="stock-chart-container apple-style">
      <div className="chart-header">
        <div className="price-section">
          <div className="symbol-name">
            <h2>{quote?.symbol || 'N/A'}</h2>
            <span className="company-name">Stock Analysis</span>
            {quote?.source && (
              <span className="data-source-badge" title="Data source">
                📡 {quote.source}
              </span>
            )}
          </div>
          <div className="price-display">
            <h1 className="current-price">${quote?.price?.toFixed(2) || 'N/A'}</h1>
            <div className={`price-change ${isPositive ? 'positive' : 'negative'}`}>
              <span className="change-icon">{isPositive ? '▲' : '▼'}</span>
              <span className="change-value">${Math.abs(quote?.change || 0).toFixed(2)}</span>
              <span className="change-percent">({Math.abs(quote?.changePercent || 0).toFixed(2)}%)</span>
            </div>
          </div>
          <div className="trend-note">
            <small>Chart color shows today's change: {isPositive ? 'Up today (Green)' : 'Down today (Red)'}</small>
          </div>
        </div>

        <div className="time-range-selector">
          {['1D', '1W', '1M', '3M', '6M', '1Y', 'ALL'].map(range => (
            <button
              key={range}
              className={`range-btn ${timeRange === range ? 'active' : ''}`}
              onClick={() => setTimeRange(range)}
            >
              {range}
            </button>
          ))}
          {predictions && (
            <button
              className={`range-btn prediction-toggle ${showPredictions ? 'active' : ''}`}
              onClick={() => setShowPredictions(!showPredictions)}
              title="Toggle price predictions"
            >
              🔮 Forecast
            </button>
          )}
        </div>
      </div>

      <div className="chart-wrapper apple-chart">
        <ResponsiveContainer width="100%" height={450}>
          <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={isPositive ? "#34C759" : "#FF3B30"} stopOpacity={0.4}/>
                <stop offset="95%" stopColor={isPositive ? "#34C759" : "#FF3B30"} stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="colorPrediction" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#007AFF" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#007AFF" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
            <XAxis 
              dataKey="dateStr" 
              stroke="#8E8E93"
              tick={{ fontSize: 11, fill: '#8E8E93' }}
              tickLine={false}
              axisLine={false}
              interval={Math.floor(data.length / 6)}
            />
            <YAxis 
              stroke="#8E8E93"
              tick={{ fontSize: 11, fill: '#8E8E93' }}
              tickLine={false}
              axisLine={false}
              domain={['auto', 'auto']}
              tickFormatter={(value) => `$${value.toFixed(0)}`}
            />
            <Tooltip content={<CustomTooltip />} />
            
            {/* Historical Actual Prices */}
            <Area 
              type="monotone" 
              dataKey="actualPrice" 
              stroke={isPositive ? "#34C759" : "#FF3B30"}
              strokeWidth={2.5}
              fill="url(#colorPrice)"
              animationDuration={800}
              connectNulls={false}
              name="Actual Price"
            />
            
            {/* Prediction Lines and Confidence Bands */}
            {showPredictions && predictions && (
              <>
                {/* Upper confidence bound */}
                <Area 
                  type="monotone" 
                  dataKey="upperBound" 
                  stroke="transparent"
                  fill="rgba(0, 122, 255, 0.15)"
                  connectNulls={true}
                  name="Upper Bound"
                />
                {/* Lower confidence bound */}
                <Area 
                  type="monotone" 
                  dataKey="lowerBound" 
                  stroke="transparent"
                  fill="rgba(0, 122, 255, 0.15)"
                  connectNulls={true}
                  name="Lower Bound"
                />
                {/* Predicted price line */}
                <Area 
                  type="monotone" 
                  dataKey="predictedPrice" 
                  stroke="#007AFF"
                  strokeWidth={2.5}
                  strokeDasharray="5 5"
                  fill="url(#colorPrediction)"
                  connectNulls={true}
                  name="Predicted Price"
                />
              </>
            )}
          </AreaChart>
        </ResponsiveContainer>
        
        {/* Legend */}
        {showPredictions && predictions && (
          <div className="chart-legend">
            <div className="legend-item">
              <div className="legend-line actual" style={{background: isPositive ? '#34C759' : '#FF3B30'}}></div>
              <span>Actual Price (Historical)</span>
            </div>
            <div className="legend-item">
              <div className="legend-line predicted"></div>
              <span>Predicted Price (Forecast)</span>
            </div>
            <div className="legend-item">
              <div className="legend-box confidence"></div>
              <span>95% Confidence Range</span>
            </div>
          </div>
        )}
      </div>

      <div className="stats-grid apple-stats">
        <div className="stat-row">
          <div className="stat-item">
            <span className="stat-label">Open</span>
            <span className="stat-value">${quote?.open?.toFixed(2) || (quote?.price - quote?.change)?.toFixed(2) || 'N/A'}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">High</span>
            <span className="stat-value">${quote?.dayHigh?.toFixed(2) || 'N/A'}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Low</span>
            <span className="stat-value">${quote?.dayLow?.toFixed(2) || 'N/A'}</span>
          </div>
        </div>
        
        <div className="stat-row">
          <div className="stat-item">
            <span className="stat-label">Mkt Cap</span>
            <span className="stat-value">{formatMarketCap(quote?.marketCap)}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">P/E Ratio</span>
            <span className="stat-value">{quote?.pe?.toFixed(2) || 'N/A'}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">52W High</span>
            <span className="stat-value">${quote?.fiftyTwoWeekHigh?.toFixed(2) || 'N/A'}</span>
          </div>
        </div>

        <div className="stat-row">
          <div className="stat-item">
            <span className="stat-label">Volume</span>
            <span className="stat-value">{formatVolume(quote?.volume)}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Avg Vol</span>
            <span className="stat-value">{formatVolume(quote?.avgVolume)}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">52W Low</span>
            <span className="stat-value">${quote?.fiftyTwoWeekLow?.toFixed(2) || 'N/A'}</span>
          </div>
        </div>
      </div>

      <div className="performance-banner">
        <div className="perf-item">
          <span className="perf-label">1Y Return</span>
          <span className={`perf-value ${performance.total_return >= 0 ? 'positive' : 'negative'}`}>
            {performance.total_return >= 0 ? '+' : ''}{performance.total_return?.toFixed(2)}%
          </span>
        </div>
        <div className="perf-item">
          <span className="perf-label">Volatility</span>
          <span className="perf-value">{performance.volatility?.toFixed(2)}%</span>
        </div>
        <div className="perf-item">
          <span className="perf-label">Year High</span>
          <span className="perf-value">${performance.max_price?.toFixed(2)}</span>
        </div>
        <div className="perf-item">
          <span className="perf-label">Year Low</span>
          <span className="perf-value">${performance.min_price?.toFixed(2)}</span>
        </div>
      </div>
    </div>
  );
};

const formatMarketCap = (value) => {
  if (!value) return 'N/A';
  if (value >= 1e12) return `$${(value / 1e12).toFixed(2)}T`;
  if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`;
  if (value >= 1e6) return `$${(value / 1e6).toFixed(2)}M`;
  return `$${value}`;
};

const formatVolume = (value) => {
  if (!value) return 'N/A';
  if (value >= 1e9) return `${(value / 1e9).toFixed(2)}B`;
  if (value >= 1e6) return `${(value / 1e6).toFixed(2)}M`;
  if (value >= 1e3) return `${(value / 1e3).toFixed(2)}K`;
  return value;
};

export default StockChart;
