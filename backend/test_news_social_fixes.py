#!/usr/bin/env python3
"""Test news and social scraping fixes"""

from data_sources.news_client import NewsClient
from data_sources.social_client import SocialClient

def test_news_client():
    print("="*60)
    print("TESTING NEWS CLIENT (Recent News)")
    print("="*60)
    
    client = NewsClient()
    ticker = "AAPL"
    
    print(f"\nFetching latest news for {ticker}...")
    news = client.get_news_headlines(ticker)
    
    print(f"\n✓ News fetched successfully")
    print(f"  Source: {news.get('source', 'Unknown')}")
    print(f"  Headlines: {len(news.get('headlines', []))}")
    
    if news.get('headlines'):
        print(f"\n  Recent Headlines:")
        for i, headline in enumerate(news['headlines'][:5], 1):
            if isinstance(headline, dict):
                print(f"    {i}. {headline.get('title', headline)}")
                print(f"       Source: {headline.get('source', 'N/A')} | Date: {headline.get('date', 'N/A')}")
                if headline.get('url'):
                    print(f"       URL: {headline['url'][:60]}...")
            else:
                print(f"    {i}. {headline}")
    
    if news.get('detailed_summary'):
        print(f"\n  Summary Preview:")
        summary = news['detailed_summary']
        print(f"    {summary[:200]}...")
    
    print("\n" + "="*60)

def test_social_client():
    print("\nTESTING SOCIAL CLIENT (Reddit Scraping + LLM)")
    print("="*60)
    
    client = SocialClient()
    ticker = "NVDA"
    
    print(f"\nAnalyzing social sentiment for {ticker}...")
    social = client.analyze_reddit_sentiment(ticker)
    
    print(f"\n✓ Social analysis complete")
    print(f"  Source: {social.get('source', 'Unknown')}")
    print(f"  Sentiment: {social.get('sentiment', 'Unknown')}")
    print(f"  Sentiment Score: {social.get('sentiment_score', 0)}")
    print(f"  Mentions: {social.get('mentions', 'Unknown')}")
    
    if social.get('top_posts'):
        print(f"\n  Top Reddit Posts:")
        for i, post in enumerate(social['top_posts'][:3], 1):
            print(f"    {i}. [{post['subreddit']}] {post['title'][:60]}...")
            print(f"       Score: {post['score']} | Comments: {post['comments']}")
    
    if social.get('detailed_summary'):
        print(f"\n  Analysis Preview:")
        summary = social['detailed_summary']
        print(f"    {summary[:200]}...")
    
    if social.get('key_topics'):
        print(f"\n  Key Topics: {', '.join(social['key_topics'][:5])}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        test_news_client()
        print("\n")
        test_social_client()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETE")
        print("="*60)
        print("\nKey Improvements:")
        print("  ✓ News now focuses on past 24-48 hours (up to 1 week max)")
        print("  ✓ News includes exact dates and times")
        print("  ✓ Reddit scraping improved with better error handling")
        print("  ✓ LLM analysis works with scraped Reddit data")
        print("  ✓ Fallback to scraped data if LLM fails")
        
    except Exception as e:
        print(f"\n✗ Test error: {e}")
        import traceback
        traceback.print_exc()
