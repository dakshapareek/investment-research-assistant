import requests
from datetime import datetime, timedelta
from data_sources.multi_api_client import MultiAPIStockClient

class StockDataClient:
    """Fetch stock price data and financial metrics with multi-API support"""
    
    def __init__(self):
        self.multi_api = MultiAPIStockClient()
        
    def get_stock_data(self, ticker, period='1y', interval='1d'):
        """Get historical stock data using multi-API client"""
        return self.multi_api.get_historical_data(ticker, days=365)
    
    def get_quote(self, ticker):
        """Get current stock quote using multi-API client with fallback"""
        return self.multi_api.get_quote(ticker)
    
    def calculate_performance(self, prices):
        """Calculate performance metrics"""
        if not prices or len(prices) < 2:
            return {}
        
        # Filter out None values
        valid_prices = [p for p in prices if p is not None]
        if not valid_prices:
            return {}
        
        current = valid_prices[-1]
        start = valid_prices[0]
        
        return {
            'total_return': ((current - start) / start * 100) if start else 0,
            'max_price': max(valid_prices),
            'min_price': min(valid_prices),
            'volatility': self._calculate_volatility(valid_prices)
        }
    
    def _calculate_volatility(self, prices):
        """Calculate price volatility (standard deviation)"""
        if len(prices) < 2:
            return 0
        
        mean = sum(prices) / len(prices)
        variance = sum((p - mean) ** 2 for p in prices) / len(prices)
        return (variance ** 0.5) / mean * 100
