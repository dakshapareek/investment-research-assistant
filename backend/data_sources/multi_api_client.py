import requests
from datetime import datetime, timedelta
from config import (
    FINANCIAL_MODELING_PREP_API_KEY,
    ALPHA_VANTAGE_API_KEY,
    FINNHUB_API_KEY,
    POLYGON_API_KEY,
    MARKETSTACK_API_KEY,
    EODHD_API_KEY,
    USE_MCP_FOR_FINANCIAL_DATA,
    MCP_SERVER_COMMAND,
    MCP_SERVER_ARGS
)

class MultiAPIStockClient:
    """Multi-source stock data client with automatic fallback and MCP support"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Initialize MCP client if enabled
        self.mcp_client = None
        if USE_MCP_FOR_FINANCIAL_DATA:
            try:
                from mcp_financial_client import MCPFinancialClientSync
                self.mcp_client = MCPFinancialClientSync(
                    server_command=MCP_SERVER_COMMAND,
                    server_args=MCP_SERVER_ARGS
                )
                print(f"✓ MCP client initialized: {MCP_SERVER_COMMAND} {' '.join(MCP_SERVER_ARGS)}")
            except Exception as e:
                print(f"⚠️  MCP client initialization failed: {e}")
                print(f"   Falling back to direct APIs")
        
        self.apis = [
            ('Financial Modeling Prep', self._fetch_fmp),
            ('Alpha Vantage', self._fetch_alpha_vantage),
            ('Finnhub', self._fetch_finnhub),
            ('Polygon', self._fetch_polygon),
            ('Marketstack', self._fetch_marketstack),
            ('EODHD', self._fetch_eodhd),
            ('Yahoo Finance', self._fetch_yahoo)
        ]
    
    def get_quote(self, ticker):
        """Get stock quote with MCP priority and automatic fallback"""
        
        # Try MCP first if enabled
        if self.mcp_client:
            try:
                print(f"Trying MCP for {ticker}...")
                data = self.mcp_client.get_stock_quote(ticker)
                if data and data.get('price'):
                    print(f"✓ Successfully fetched from MCP")
                    return data
                else:
                    print(f"✗ MCP returned no data, trying fallback APIs...")
            except Exception as e:
                print(f"✗ MCP failed: {e}, trying fallback APIs...")
        
        # Try each API in order
        for api_name, api_func in self.apis:
            try:
                print(f"  → Trying {api_name}...")
                data = api_func(ticker)
                if data and data.get('price'):
                    print(f"  ✓ {api_name}: Success")
                    data['source'] = api_name
                    return data
                else:
                    print(f"  ✗ {api_name}: No data")
            except Exception as e:
                print(f"  ✗ {api_name}: {str(e)}")
                continue
        
        # If all APIs fail, return mock data
        print(f"  ⚠️  All APIs failed, using mock data")
        return self._get_mock_quote(ticker)
    
    def _fetch_fmp(self, ticker):
        """Financial Modeling Prep API (250 requests/day free)"""
        if not FINANCIAL_MODELING_PREP_API_KEY:
            return None
        
        url = f'https://financialmodelingprep.com/api/v3/quote/{ticker}'
        params = {'apikey': FINANCIAL_MODELING_PREP_API_KEY}
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                quote = data[0]
                return {
                    'symbol': quote.get('symbol'),
                    'price': quote.get('price'),
                    'open': quote.get('open'),
                    'previousClose': quote.get('previousClose'),
                    'change': quote.get('change'),
                    'changePercent': quote.get('changesPercentage'),
                    'dayHigh': quote.get('dayHigh'),
                    'dayLow': quote.get('dayLow'),
                    'volume': quote.get('volume'),
                    'marketCap': quote.get('marketCap'),
                    'pe': quote.get('pe'),
                    'eps': quote.get('eps'),
                    'fiftyTwoWeekHigh': quote.get('yearHigh'),
                    'fiftyTwoWeekLow': quote.get('yearLow'),
                    'avgVolume': quote.get('avgVolume')
                }
        return None
    
    def _fetch_alpha_vantage(self, ticker):
        """Alpha Vantage API (25 requests/day free)"""
        if not ALPHA_VANTAGE_API_KEY:
            return None
        
        url = 'https://www.alphavantage.co/query'
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': ticker,
            'apikey': ALPHA_VANTAGE_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'Global Quote' in data:
                quote = data['Global Quote']
                price = float(quote.get('05. price', 0))
                change = float(quote.get('09. change', 0))
                
                return {
                    'symbol': quote.get('01. symbol'),
                    'price': price,
                    'open': float(quote.get('02. open', price)),
                    'previousClose': float(quote.get('08. previous close', price)),
                    'change': change,
                    'changePercent': float(quote.get('10. change percent', '0').replace('%', '')),
                    'dayHigh': float(quote.get('03. high', price)),
                    'dayLow': float(quote.get('04. low', price)),
                    'volume': int(quote.get('06. volume', 0)),
                    'marketCap': None,
                    'pe': None,
                    'eps': None,
                    'fiftyTwoWeekHigh': None,
                    'fiftyTwoWeekLow': None,
                    'avgVolume': None
                }
        return None
    
    def _fetch_finnhub(self, ticker):
        """Finnhub API (60 calls/minute free)"""
        if not FINNHUB_API_KEY:
            return None
        
        url = f'https://finnhub.io/api/v1/quote'
        params = {
            'symbol': ticker,
            'token': FINNHUB_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('c'):  # current price
                price = data.get('c')
                prev_close = data.get('pc', price)
                change = price - prev_close
                
                return {
                    'symbol': ticker,
                    'price': price,
                    'open': data.get('o', price),
                    'previousClose': prev_close,
                    'change': change,
                    'changePercent': (change / prev_close * 100) if prev_close else 0,
                    'dayHigh': data.get('h', price),
                    'dayLow': data.get('l', price),
                    'volume': None,
                    'marketCap': None,
                    'pe': None,
                    'eps': None,
                    'fiftyTwoWeekHigh': None,
                    'fiftyTwoWeekLow': None,
                    'avgVolume': None
                }
        return None
    
    def _fetch_polygon(self, ticker):
        """Polygon.io API (5 calls/minute free)"""
        if not POLYGON_API_KEY:
            return None
        
        # Get previous day's data
        url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/prev'
        params = {'apiKey': POLYGON_API_KEY}
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('results') and len(data['results']) > 0:
                result = data['results'][0]
                close = result.get('c')
                open_price = result.get('o')
                
                return {
                    'symbol': ticker,
                    'price': close,
                    'open': open_price,
                    'previousClose': close,
                    'change': close - open_price,
                    'changePercent': ((close - open_price) / open_price * 100) if open_price else 0,
                    'dayHigh': result.get('h'),
                    'dayLow': result.get('l'),
                    'volume': result.get('v'),
                    'marketCap': None,
                    'pe': None,
                    'eps': None,
                    'fiftyTwoWeekHigh': None,
                    'fiftyTwoWeekLow': None,
                    'avgVolume': None
                }
        return None
    
    def _fetch_marketstack(self, ticker):
        """Marketstack API (100 requests/month free)"""
        if not MARKETSTACK_API_KEY:
            return None
        
        try:
            url = f'http://api.marketstack.com/v1/eod/latest'
            params = {
                'access_key': MARKETSTACK_API_KEY,
                'symbols': ticker
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and len(data['data']) > 0:
                    quote = data['data'][0]
                    close = quote.get('close')
                    open_price = quote.get('open')
                    
                    if close:
                        change = close - open_price if open_price else 0
                        change_pct = (change / open_price * 100) if open_price else 0
                        
                        return {
                            'symbol': quote.get('symbol'),
                            'price': close,
                            'open': open_price,
                            'previousClose': close,
                            'change': change,
                            'changePercent': change_pct,
                            'dayHigh': quote.get('high'),
                            'dayLow': quote.get('low'),
                            'volume': quote.get('volume'),
                            'marketCap': None,
                            'pe': None,
                            'eps': None,
                            'fiftyTwoWeekHigh': None,
                            'fiftyTwoWeekLow': None,
                            'avgVolume': None
                        }
        except Exception as e:
            print(f"Marketstack error: {e}")
        
        return None
    
    def _fetch_eodhd(self, ticker):
        """EODHD API (20 requests/day free)"""
        if not EODHD_API_KEY:
            return None
        
        try:
            url = f'https://eodhistoricaldata.com/api/real-time/{ticker}.US'
            params = {
                'api_token': EODHD_API_KEY,
                'fmt': 'json'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                price = data.get('close')
                
                if price:
                    open_price = data.get('open', price)
                    prev_close = data.get('previousClose', price)
                    change = price - prev_close
                    change_pct = (change / prev_close * 100) if prev_close else 0
                    
                    return {
                        'symbol': ticker,
                        'price': price,
                        'open': open_price,
                        'previousClose': prev_close,
                        'change': change,
                        'changePercent': change_pct,
                        'dayHigh': data.get('high', price),
                        'dayLow': data.get('low', price),
                        'volume': data.get('volume', 0),
                        'marketCap': None,
                        'pe': None,
                        'eps': None,
                        'fiftyTwoWeekHigh': None,
                        'fiftyTwoWeekLow': None,
                        'avgVolume': None
                    }
        except Exception as e:
            print(f"EODHD error: {e}")
        
        return None
    
    def _fetch_yahoo(self, ticker):
        """Yahoo Finance API (fallback)"""
        try:
            url = f'https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}'
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'quoteResponse' in data and 'result' in data['quoteResponse'] and data['quoteResponse']['result']:
                    quote = data['quoteResponse']['result'][0]
                    price = quote.get('regularMarketPrice')
                    
                    if price:
                        return {
                            'symbol': quote.get('symbol'),
                            'price': price,
                            'open': quote.get('regularMarketOpen', price),
                            'previousClose': quote.get('regularMarketPreviousClose', price),
                            'change': quote.get('regularMarketChange', 0),
                            'changePercent': quote.get('regularMarketChangePercent', 0),
                            'dayHigh': quote.get('regularMarketDayHigh', price),
                            'dayLow': quote.get('regularMarketDayLow', price),
                            'volume': quote.get('regularMarketVolume', 0),
                            'marketCap': quote.get('marketCap', 0),
                            'pe': quote.get('trailingPE'),
                            'eps': quote.get('epsTrailingTwelveMonths'),
                            'fiftyTwoWeekHigh': quote.get('fiftyTwoWeekHigh', price),
                            'fiftyTwoWeekLow': quote.get('fiftyTwoWeekLow', price),
                            'avgVolume': quote.get('averageDailyVolume3Month', 0)
                        }
        except Exception as e:
            print(f"Yahoo Finance error: {e}")
        
        return None
    
    def _get_mock_quote(self, ticker):
        """Generate realistic mock quote"""
        base_prices = {
            'AAPL': 175.43, 'MSFT': 380.12, 'GOOGL': 140.85,
            'AMZN': 155.67, 'TSLA': 210.34, 'META': 450.89,
            'NVDA': 720.45, 'JPM': 165.23, 'V': 260.78, 'WMT': 165.90,
            'BTC-USD': 95000.00, 'ETH-USD': 3500.00, 'SOL-USD': 180.00,
            '^GSPC': 5800.00, '^DJI': 42000.00, 'SPY': 580.00
        }
        
        price = base_prices.get(ticker, 150.00)
        change = price * 0.012
        open_price = price - (change * 0.5)
        
        return {
            'symbol': ticker,
            'price': price,
            'open': open_price,
            'previousClose': price - change,
            'change': change,
            'changePercent': (change / (price - change)) * 100,
            'dayHigh': price * 1.015,
            'dayLow': price * 0.992,
            'volume': 52000000,
            'marketCap': price * 16000000000,
            'pe': 25.8,
            'eps': price / 25.8,
            'fiftyTwoWeekHigh': price * 1.25,
            'fiftyTwoWeekLow': price * 0.75,
            'avgVolume': 55000000,
            'source': 'Mock Data'
        }
    
    def get_historical_data(self, ticker, days=365):
        """Get historical data with MCP priority and automatic fallback"""
        print(f"\n[HISTORICAL DATA] Fetching {days} days for {ticker}...")
        
        # Try MCP first if enabled
        if self.mcp_client:
            try:
                print(f"  → Trying MCP...")
                data = self.mcp_client.get_historical_data(ticker, days)
                if data and len(data.get('close', [])) > 0:
                    print(f"  ✓ MCP: Got {len(data['close'])} data points")
                    return data
                else:
                    print(f"  ✗ MCP returned no data, trying fallback APIs...")
            except Exception as e:
                print(f"  ✗ MCP failed: {e}, trying fallback APIs...")
        
        # Try FMP
        if FINANCIAL_MODELING_PREP_API_KEY:
            try:
                print(f"  → Trying Financial Modeling Prep...")
                data = self._fetch_fmp_historical(ticker, days)
                if data:
                    print(f"  ✓ FMP: Got {len(data['close'])} data points")
                    data['source'] = 'Financial Modeling Prep'
                    return data
            except Exception as e:
                print(f"  ✗ FMP failed: {e}")
        
        # Try Alpha Vantage
        if ALPHA_VANTAGE_API_KEY:
            try:
                print(f"  → Trying Alpha Vantage...")
                data = self._fetch_av_historical(ticker)
                if data:
                    print(f"  ✓ Alpha Vantage: Got {len(data['close'])} data points")
                    data['source'] = 'Alpha Vantage'
                    return data
            except Exception as e:
                print(f"  ✗ Alpha Vantage failed: {e}")
        
        # Try Yahoo Finance directly
        try:
            print(f"  → Trying Yahoo Finance...")
            data = self._fetch_yahoo_historical(ticker, days)
            if data:
                print(f"  ✓ Yahoo Finance: Got {len(data['close'])} data points")
                data['source'] = 'Yahoo Finance'
                return data
        except Exception as e:
            print(f"  ✗ Yahoo Finance failed: {e}")
        
        # If all fail, return mock data
        print(f"  ⚠️  All APIs failed, using mock data")
        data = self._get_mock_historical(ticker, days)
        data['source'] = 'Mock Data (Configure API keys for real data)'
        return data
    
    def _fetch_yahoo_historical(self, ticker, days=365):
        print(f"  ⚠️  All APIs failed, using mock data")
        data = self._get_mock_historical(ticker, days)
        data['source'] = 'Mock Data (Configure API keys for real data)'
        return data
    
    def _fetch_yahoo_historical(self, ticker, days=365):
        """Get historical data from Yahoo Finance (most reliable free source)"""
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days + 30)  # Extra buffer
        
        period1 = int(start_date.timestamp())
        period2 = int(end_date.timestamp())
        
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}'
        params = {
            'period1': period1,
            'period2': period2,
            'interval': '1d',
            'events': 'history'
        }
        
        response = requests.get(url, headers=self.headers, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                result = data['chart']['result'][0]
                
                if 'timestamp' in result and 'indicators' in result:
                    timestamps = result['timestamp']
                    quote = result['indicators']['quote'][0]
                    
                    # Extract data
                    closes = quote.get('close', [])
                    opens = quote.get('open', [])
                    highs = quote.get('high', [])
                    lows = quote.get('low', [])
                    volumes = quote.get('volume', [])
                    
                    # Filter out None values and ensure all arrays are same length
                    valid_data = []
                    for i in range(len(timestamps)):
                        if (i < len(closes) and closes[i] is not None and
                            i < len(opens) and opens[i] is not None):
                            valid_data.append({
                                'timestamp': timestamps[i],
                                'close': closes[i],
                                'open': opens[i],
                                'high': highs[i] if i < len(highs) and highs[i] else closes[i],
                                'low': lows[i] if i < len(lows) and lows[i] else closes[i],
                                'volume': volumes[i] if i < len(volumes) and volumes[i] else 0
                            })
                    
                    if valid_data:
                        return {
                            'timestamps': [d['timestamp'] for d in valid_data],
                            'close': [d['close'] for d in valid_data],
                            'open': [d['open'] for d in valid_data],
                            'high': [d['high'] for d in valid_data],
                            'low': [d['low'] for d in valid_data],
                            'volume': [d['volume'] for d in valid_data]
                        }
        
        return None
    
    def _fetch_fmp_historical(self, ticker, days):
        """Get historical data from FMP"""
        url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}'
        params = {'apikey': FINANCIAL_MODELING_PREP_API_KEY}
        
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if 'historical' in data:
                historical = data['historical'][:days]
                
                timestamps = []
                closes = []
                volumes = []
                highs = []
                lows = []
                
                for item in reversed(historical):
                    date = datetime.strptime(item['date'], '%Y-%m-%d')
                    timestamps.append(int(date.timestamp()))
                    closes.append(item['close'])
                    volumes.append(item['volume'])
                    highs.append(item['high'])
                    lows.append(item['low'])
                
                return {
                    'timestamps': timestamps,
                    'close': closes,
                    'volume': volumes,
                    'high': highs,
                    'low': lows,
                    'open': [item['open'] for item in reversed(historical)]
                }
        return None
    
    def _fetch_av_historical(self, ticker):
        """Get historical data from Alpha Vantage"""
        url = 'https://www.alphavantage.co/query'
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': ticker,
            'outputsize': 'full',
            'apikey': ALPHA_VANTAGE_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if 'Time Series (Daily)' in data:
                time_series = data['Time Series (Daily)']
                
                timestamps = []
                closes = []
                volumes = []
                highs = []
                lows = []
                opens = []
                
                for date_str in sorted(time_series.keys()):
                    date = datetime.strptime(date_str, '%Y-%m-%d')
                    day_data = time_series[date_str]
                    
                    timestamps.append(int(date.timestamp()))
                    closes.append(float(day_data['4. close']))
                    volumes.append(int(day_data['5. volume']))
                    highs.append(float(day_data['2. high']))
                    lows.append(float(day_data['3. low']))
                    opens.append(float(day_data['1. open']))
                
                return {
                    'timestamps': timestamps[-365:],
                    'close': closes[-365:],
                    'volume': volumes[-365:],
                    'high': highs[-365:],
                    'low': lows[-365:],
                    'open': opens[-365:]
                }
        return None
    
    def _get_mock_historical(self, ticker, days):
        """Generate mock historical data"""
        import random
        
        base_prices = {
            'AAPL': 175.0, 'MSFT': 380.0, 'GOOGL': 140.0,
            'AMZN': 155.0, 'TSLA': 210.0, 'META': 450.0,
            'NVDA': 720.0, 'JPM': 165.0, 'V': 260.0, 'WMT': 165.0
        }
        
        base_price = base_prices.get(ticker, 150.0)
        timestamps = []
        closes = []
        volumes = []
        highs = []
        lows = []
        opens = []
        
        for i in range(min(days, 252)):
            timestamp = int((datetime.now() - timedelta(days=252-i)).timestamp())
            timestamps.append(timestamp)
            
            change = random.uniform(-0.025, 0.03)
            base_price = base_price * (1 + change)
            close = round(base_price, 2)
            
            closes.append(close)
            opens.append(round(close * random.uniform(0.99, 1.01), 2))
            highs.append(round(close * 1.015, 2))
            lows.append(round(close * 0.985, 2))
            volumes.append(random.randint(40000000, 80000000))
        
        return {
            'timestamps': timestamps,
            'close': closes,
            'volume': volumes,
            'high': highs,
            'low': lows,
            'open': opens
        }
