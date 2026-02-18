# Edge Cases Support - Crypto, Forex, Indices

## Overview

The Investment Research Platform now supports various asset types beyond traditional stocks, including cryptocurrencies, forex pairs, and market indices.

## Supported Asset Types

### 1. Stocks (Traditional)
**Format**: `SYMBOL`
**Examples**:
- `AAPL` - Apple Inc.
- `MSFT` - Microsoft
- `GOOGL` - Alphabet (Google)
- `TSLA` - Tesla
- `NVDA` - NVIDIA

### 2. Cryptocurrencies
**Format**: `CRYPTO-USD` or `CRYPTO-USDT`
**Examples**:
- `BTC-USD` - Bitcoin to USD
- `ETH-USD` - Ethereum to USD
- `SOL-USD` - Solana to USD
- `ADA-USD` - Cardano to USD
- `DOGE-USD` - Dogecoin to USD
- `XRP-USD` - Ripple to USD
- `MATIC-USD` - Polygon to USD
- `AVAX-USD` - Avalanche to USD

### 3. Forex Pairs
**Format**: `CURRENCY1CURRENCY2=X`
**Examples**:
- `EURUSD=X` - Euro to USD
- `GBPUSD=X` - British Pound to USD
- `USDJPY=X` - USD to Japanese Yen
- `AUDUSD=X` - Australian Dollar to USD
- `USDCAD=X` - USD to Canadian Dollar

### 4. Market Indices
**Format**: `^INDEX`
**Examples**:
- `^GSPC` - S&P 500
- `^DJI` - Dow Jones Industrial Average
- `^IXIC` - NASDAQ Composite
- `^RUT` - Russell 2000
- `^VIX` - CBOE Volatility Index
- `^FTSE` - FTSE 100 (UK)
- `^N225` - Nikkei 225 (Japan)

### 5. ETFs
**Format**: `SYMBOL`
**Examples**:
- `SPY` - SPDR S&P 500 ETF
- `QQQ` - Invesco QQQ (NASDAQ-100)
- `VOO` - Vanguard S&P 500 ETF
- `VTI` - Vanguard Total Stock Market ETF
- `IWM` - iShares Russell 2000 ETF
- `GLD` - SPDR Gold Shares
- `SLV` - iShares Silver Trust

### 6. Commodities
**Format**: Varies by platform
**Examples**:
- `GC=F` - Gold Futures
- `SI=F` - Silver Futures
- `CL=F` - Crude Oil Futures
- `NG=F` - Natural Gas Futures

## Default Watchlist

The platform now comes with a diverse default watchlist:
- `AAPL` - Apple (Tech Stock)
- `NVDA` - NVIDIA (Semiconductor)
- `TSLA` - Tesla (EV/Auto)
- `BTC-USD` - Bitcoin (Crypto)
- `ETH-USD` - Ethereum (Crypto)

## How to Add Edge Cases

### Method 1: Search Bar
1. Type the symbol in the search bar (e.g., `BTC-USD`)
2. Click the eye icon button
3. Symbol is added to watchlist

### Method 2: Direct Entry
1. Type the exact symbol format
2. Click "Analyze" to test it
3. If it works, add it to watchlist

## Symbol Format Rules

### Cryptocurrencies
- **Must include hyphen**: `BTC-USD` (not `BTCUSD`)
- **Case insensitive**: `btc-usd` → `BTC-USD`
- **Common pairs**: `-USD`, `-USDT`, `-EUR`, `-BTC`

### Forex
- **Use =X suffix**: `EURUSD=X`
- **6 characters + =X**: Currency pair + equals + X
- **No spaces or hyphens**

### Indices
- **Use ^ prefix**: `^GSPC`
- **Case sensitive**: Must use uppercase after ^

### ETFs & Stocks
- **Standard format**: Just the symbol
- **Case insensitive**: `spy` → `SPY`

## API Support

Different APIs support different asset types:

### Yahoo Finance (Fallback)
✓ Stocks
✓ Cryptocurrencies (with -USD)
✓ Forex (with =X)
✓ Indices (with ^)
✓ ETFs
✓ Commodities (with =F)

### Finnhub
✓ Stocks
✓ Cryptocurrencies
✓ Forex
✓ Indices (limited)

### Polygon
✓ Stocks
✓ Cryptocurrencies
✓ Forex
✓ Indices

### Alpha Vantage
✓ Stocks
✓ Cryptocurrencies (separate endpoint)
✓ Forex (separate endpoint)

## Analysis Differences

### Stocks
- Full analysis with SEC filings
- Social sentiment from Reddit
- News from financial sources
- Predictive analysis
- Technical indicators

### Cryptocurrencies
- Price data and charts
- Social sentiment (crypto subreddits)
- News from crypto sources
- Technical indicators
- No SEC filings (not applicable)

### Forex
- Price data and charts
- Economic news
- Technical indicators
- No social sentiment (less relevant)
- No SEC filings (not applicable)

### Indices
- Price data and charts
- Market-wide news
- Technical indicators
- No social sentiment
- No SEC filings (not applicable)

## Examples

### Adding Bitcoin
```
1. Type: BTC-USD
2. Click eye icon
3. Added to watchlist
4. Click chip to analyze
```

### Adding S&P 500
```
1. Type: ^GSPC
2. Click eye icon
3. Added to watchlist
4. Click chip to analyze
```

### Adding EUR/USD
```
1. Type: EURUSD=X
2. Click eye icon
3. Added to watchlist
4. Click chip to analyze
```

## Troubleshooting

### Symbol Not Found
- Check the format (hyphen, =X, ^ prefix)
- Try Yahoo Finance format
- Search online for the correct symbol

### No Data Available
- Some APIs don't support all asset types
- System will fall back to mock data
- Try a different symbol format

### Analysis Incomplete
- Some features (SEC filings) only work for stocks
- Crypto/forex get limited analysis
- This is expected behavior

## Popular Symbols by Category

### Tech Stocks
- AAPL, MSFT, GOOGL, AMZN, META, NVDA, AMD, INTC

### Crypto
- BTC-USD, ETH-USD, BNB-USD, SOL-USD, ADA-USD, XRP-USD

### Indices
- ^GSPC (S&P 500), ^DJI (Dow), ^IXIC (NASDAQ), ^RUT (Russell 2000)

### Forex
- EURUSD=X, GBPUSD=X, USDJPY=X, AUDUSD=X

### ETFs
- SPY, QQQ, VOO, VTI, IWM, GLD, SLV

### Commodities
- GC=F (Gold), SI=F (Silver), CL=F (Oil), NG=F (Natural Gas)

## Code Changes

### frontend/src/App.js

**Updated default watchlist:**
```javascript
const [quickWatchlist, setQuickWatchlist] = useState([
  { symbol: 'AAPL', name: 'Apple' },
  { symbol: 'NVDA', name: 'NVIDIA' },
  { symbol: 'TSLA', name: 'Tesla' },
  { symbol: 'BTC-USD', name: 'Bitcoin' },
  { symbol: 'ETH-USD', name: 'Ethereum' }
]);
```

**Updated addToQuickWatch:**
```javascript
// Preserve hyphens for crypto/forex
const processedSymbol = symbol.includes('-') ? 
  symbol.toUpperCase() : 
  symbol.toUpperCase().trim();
```

## Backend Support

The backend already supports these formats through:
- `multi_api_client.py` - Tries multiple APIs
- `stock_data_client.py` - Handles all ticker formats
- Yahoo Finance fallback - Universal support

No backend changes needed - it already works!

## Testing

### Test Crypto
1. Add `BTC-USD` to watchlist
2. Click to analyze
3. Verify chart shows Bitcoin price
4. Check news mentions Bitcoin

### Test Forex
1. Add `EURUSD=X` to watchlist
2. Click to analyze
3. Verify chart shows EUR/USD rate
4. Check data is current

### Test Index
1. Add `^GSPC` to watchlist
2. Click to analyze
3. Verify chart shows S&P 500
4. Check market-wide news

## Limitations

1. **SEC Filings**: Only available for US stocks
2. **Social Sentiment**: Best for stocks, limited for crypto
3. **News Quality**: Varies by asset type
4. **API Coverage**: Not all APIs support all types
5. **Real-time Data**: May have delays (15-20 min)

## Future Enhancements

- Crypto-specific sentiment from Twitter/Reddit
- Forex economic calendar integration
- Index constituent analysis
- Commodity supply/demand data
- Options chain data
- Futures data

## Summary

The platform now supports:
✓ Traditional stocks (AAPL, MSFT, etc.)
✓ Cryptocurrencies (BTC-USD, ETH-USD, etc.)
✓ Forex pairs (EURUSD=X, etc.)
✓ Market indices (^GSPC, ^DJI, etc.)
✓ ETFs (SPY, QQQ, etc.)
✓ Commodities (GC=F, CL=F, etc.)

Just use the correct symbol format and the system handles the rest!
