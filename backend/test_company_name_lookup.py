"""Test script to verify company name lookup is working"""
import json
import os

# Test the company name lookup
def test_company_name_lookup():
    # Load ticker database
    db_path = 'ticker_database.json'
    with open(db_path, 'r') as f:
        ticker_db = json.load(f)
    
    # Test tickers
    test_tickers = ['COST', 'AAPL', 'NVDA', 'AMZN', 'BTC-USD']
    
    print("Testing company name lookup:")
    print("=" * 60)
    
    for ticker in test_tickers:
        # Handle crypto
        if '-' in ticker:
            base = ticker.split('-')[0]
            crypto_names = {
                'BTC': 'Bitcoin',
                'ETH': 'Ethereum',
                'DOGE': 'Dogecoin',
                'ADA': 'Cardano',
                'SOL': 'Solana'
            }
            company_name = crypto_names.get(base, ticker)
        else:
            # Look up in database
            company_name = ticker_db.get(ticker, '')
            
            # Clean up company name
            if company_name:
                for suffix in [' Inc', ' Corp', ' Corporation', ' Ltd', ' Limited', ' PLC', ' SA', ' AG']:
                    if suffix in company_name:
                        company_name = company_name.split(suffix)[0]
                        break
        
        print(f"{ticker:10} -> {company_name if company_name else ticker}")
    
    print("=" * 60)

if __name__ == '__main__':
    test_company_name_lookup()
