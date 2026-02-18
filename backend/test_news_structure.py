#!/usr/bin/env python3
"""Test script to verify news headline structure"""

import sys
sys.path.insert(0, '.')

from data_sources.news_client import NewsClient
import json

def test_news_structure():
    print("Testing News Client Structure...")
    print("="*60)
    
    # Initialize with correct model
    client = NewsClient(model_name='gemini-2.5-flash-lite')
    
    # Test with AAPL
    ticker = 'AAPL'
    print(f"\nFetching news for {ticker}...")
    news_data = client.get_news_headlines(ticker)
    
    print(f"\nNews Data Structure:")
    print(f"  Source: {news_data.get('source', 'N/A')}")
    print(f"  Summary: {news_data.get('summary', 'N/A')[:100]}...")
    print(f"  Headlines count: {len(news_data.get('headlines', []))}")
    
    print(f"\nFirst 3 Headlines:")
    for i, headline in enumerate(news_data.get('headlines', [])[:3], 1):
        print(f"\n  Headline {i}:")
        if isinstance(headline, dict):
            print(f"    ✓ Type: Object (correct)")
            print(f"    Title: {headline.get('title', 'N/A')[:80]}...")
            print(f"    Source: {headline.get('source', 'N/A')}")
            print(f"    URL: {headline.get('url', 'N/A')}")
            print(f"    Date: {headline.get('date', 'N/A')}")
        else:
            print(f"    ✗ Type: String (incorrect - should be object)")
            print(f"    Value: {str(headline)[:80]}...")
    
    print("\n" + "="*60)
    
    # Check if all headlines are objects
    headlines = news_data.get('headlines', [])
    all_objects = all(isinstance(h, dict) for h in headlines)
    
    if all_objects:
        print("✓ SUCCESS: All headlines are properly structured objects")
        
        # Check if they have URLs
        all_have_urls = all(h.get('url') for h in headlines)
        if all_have_urls:
            print("✓ SUCCESS: All headlines have URLs")
        else:
            print("⚠️  WARNING: Some headlines missing URLs")
    else:
        print("✗ FAILURE: Some headlines are strings instead of objects")
        print("   This will cause news links to not be clickable in the UI")
    
    print("="*60)

if __name__ == '__main__':
    test_news_structure()
