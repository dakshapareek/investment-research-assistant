"""Test news search with company names"""
from data_sources.news_client import NewsClient

# Test news search
client = NewsClient()

print("\nTesting news search for COST:")
print("=" * 60)
result = client.get_news_headlines('COST')
print(f"Source: {result.get('source')}")
print(f"Headlines found: {len(result.get('headlines', []))}")
print(f"\nFirst 3 headlines:")
for i, headline in enumerate(result.get('headlines', [])[:3], 1):
    print(f"{i}. {headline.get('title')}")
    print(f"   Source: {headline.get('source')}")
    print(f"   URL: {headline.get('url')[:80]}...")
    print()
