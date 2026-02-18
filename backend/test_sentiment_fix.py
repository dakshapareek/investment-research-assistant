#!/usr/bin/env python3
"""Test sentiment analysis fix"""

from data_sources.llm_sentiment import LLMSentimentAnalyzer

def test_sentiment_analysis():
    print("="*60)
    print("TESTING SENTIMENT ANALYSIS")
    print("="*60)
    
    analyzer = LLMSentimentAnalyzer()
    
    # Test 1: Single text analysis
    print("\n1. Testing single text analysis...")
    text = "NVDA stock is going to the moon! 🚀 Great earnings, strong buy!"
    result = analyzer.analyze_text(text)
    
    print(f"   Text: {text}")
    print(f"   ✓ Sentiment: {result['sentiment']}")
    print(f"   ✓ Score: {result['score']}")
    print(f"   ✓ Confidence: {result['confidence']}")
    print(f"   ✓ LLM Used: {result.get('llm_used', False)}")
    
    # Test 2: Batch analysis
    print("\n2. Testing batch analysis...")
    texts = [
        "AAPL is looking bullish, great fundamentals",
        "Bearish on TSLA, too much risk",
        "MSFT neutral, waiting for earnings",
        "GOOGL strong buy, AI momentum",
        "META concerns about regulation"
    ]
    
    result = analyzer.analyze_batch(texts)
    print(f"   Texts analyzed: {len(texts)}")
    print(f"   ✓ Overall Sentiment: {result['overall_sentiment']}")
    print(f"   ✓ Average Score: {result['average_score']}")
    print(f"   ✓ Confidence: {result['confidence']}")
    print(f"   ✓ Bullish: {result['bullish_count']}, Bearish: {result['bearish_count']}, Neutral: {result['neutral_count']}")
    print(f"   ✓ LLM Used: {result.get('llm_used', False)}")
    
    # Test 3: Reddit posts analysis
    print("\n3. Testing Reddit posts analysis...")
    reddit_posts = [
        {'title': 'NVDA to the moon! 🚀', 'score': 1500, 'comments': 200},
        {'title': 'Just bought more NVDA shares', 'score': 800, 'comments': 150},
        {'title': 'NVDA earnings beat expectations', 'score': 2000, 'comments': 300},
        {'title': 'Worried about NVDA valuation', 'score': 300, 'comments': 80},
        {'title': 'NVDA AI dominance continues', 'score': 1200, 'comments': 180}
    ]
    
    result = analyzer.analyze_reddit_posts(reddit_posts)
    print(f"   Posts analyzed: {result['posts_analyzed']}")
    print(f"   ✓ Overall Sentiment: {result['overall_sentiment']}")
    print(f"   ✓ Average Score: {result['average_score']}")
    print(f"   ✓ Confidence: {result['confidence']}")
    print(f"   ✓ Bullish: {result['bullish_count']}, Bearish: {result['bearish_count']}, Neutral: {result['neutral_count']}")
    
    # Test 4: Combined sentiment
    print("\n4. Testing combined sentiment summary...")
    news_headlines = [
        "Apple reports record Q4 earnings",
        "AAPL stock upgraded by Morgan Stanley",
        "iPhone sales exceed expectations",
        "Concerns about Apple's China exposure",
        "Apple announces new AI features"
    ]
    
    result = analyzer.get_sentiment_summary(
        reddit_data=reddit_posts,
        news_data=news_headlines
    )
    
    print(f"   ✓ Overall Sentiment: {result['overall_sentiment']}")
    print(f"   ✓ Average Score: {result['average_score']}")
    print(f"   ✓ Confidence: {result['confidence']}")
    print(f"   ✓ Sources: {len(result['sources'])}")
    
    for source in result['sources']:
        print(f"      - {source['source']}: {source['sentiment']} (score: {source['score']}, confidence: {source['confidence']})")
    
    print("\n" + "="*60)
    print("SENTIMENT ANALYSIS TEST COMPLETE")
    print("="*60)
    
    if result['average_score'] != 0:
        print("\n✅ SUCCESS: Sentiment analysis is working!")
        print(f"   Score: {result['average_score']} (non-zero)")
        print(f"   Confidence: {result['confidence']}")
    else:
        print("\n⚠️  WARNING: Sentiment score is 0")
        print("   This might indicate LLM is not working properly")

if __name__ == "__main__":
    try:
        test_sentiment_analysis()
    except Exception as e:
        print(f"\n✗ Test error: {e}")
        import traceback
        traceback.print_exc()
