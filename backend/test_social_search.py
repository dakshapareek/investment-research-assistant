"""Test social media search with company names"""
from data_sources.social_client import SocialClient

# Test social search
client = SocialClient()

print("\nTesting social media search for COST:")
print("=" * 60)
result = client.analyze_reddit_sentiment('COST')
print(f"Source: {result.get('source')}")
print(f"Sentiment: {result.get('sentiment')}")
print(f"Mentions: {result.get('mentions')}")
print(f"\nTop 3 posts:")
for i, post in enumerate(result.get('top_posts', [])[:3], 1):
    print(f"{i}. [{post.get('subreddit')}] {post.get('title')[:80]}...")
    print(f"   Score: {post.get('score')} | Comments: {post.get('comments')}")
    print()
