from data_sources.social_client import SocialClient
from data_sources.news_client import NewsClient
from data_sources.stock_data_client import StockDataClient
from data_sources.llm_sentiment import LLMSentimentAnalyzer
from data_sources.predictive_analysis import PredictiveAnalysis
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class ReportGenerator:
    def __init__(self, model_name='gemini-2.5-flash-lite'):
        self.model_name = model_name
        self.social = SocialClient(model_name=model_name)
        self.news = NewsClient(model_name=model_name)
        self.stock_data = StockDataClient()
        self.sentiment_analyzer = LLMSentimentAnalyzer(model_name=model_name)
        self.predictive_analyzer = PredictiveAnalysis(model_name=model_name)
    
    def generate_report(self, ticker):
        """Generate comprehensive investment report with parallel data fetching"""
        print(f"\n{'='*60}")
        print(f"GENERATING REPORT FOR {ticker}")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        # Fetch all data in parallel
        print(f"[PARALLEL] Fetching all data sources simultaneously...")
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit all tasks at once
            future_chart = executor.submit(self._get_stock_chart, ticker)
            future_quote = executor.submit(self._get_quote_data, ticker)
            future_social = executor.submit(self._get_social_data, ticker)
            future_news = executor.submit(self._get_news_data, ticker)
            
            # Collect results as they complete
            futures = {
                'chart': future_chart,
                'quote': future_quote,
                'social': future_social,
                'news': future_news
            }
            
            results = {}
            for name, future in futures.items():
                try:
                    results[name] = future.result(timeout=30)  # 30 second timeout per task
                    print(f"  ✓ {name.capitalize()} data complete")
                except Exception as e:
                    print(f"  ✗ {name.capitalize()} data failed: {e}")
                    results[name] = {'error': str(e)}
        
        stock_chart = results.get('chart', {'error': 'Failed to fetch'})
        quote_data = results.get('quote', {'error': 'Failed to fetch'})
        social_data = results.get('social', {'error': 'Failed to fetch'})
        news_data = results.get('news', {'error': 'Failed to fetch'})
        
        fetch_time = time.time() - start_time
        print(f"\n  ⚡ Data fetching completed in {fetch_time:.2f}s")
        
        print(f"\n[ANALYSIS] Combining sentiment data...")
        # Combined LLM sentiment analysis
        try:
            combined_sentiment = self.sentiment_analyzer.get_sentiment_summary(
                reddit_data=social_data.get('top_posts', []),
                news_data=news_data.get('headlines', [])
            )
            print(f"  ✓ Sentiment analysis complete")
        except Exception as e:
            print(f"  ✗ Sentiment analysis failed: {e}")
            combined_sentiment = {
                'overall_sentiment': 'neutral',
                'average_score': 0,
                'confidence': 0,
                'sources': []
            }
        
        print(f"\n[PREDICTIONS] Generating price forecasts...")
        # Generate predictive analysis
        predictions = None
        if stock_chart and not stock_chart.get('error') and quote_data and not quote_data.get('error'):
            try:
                predictions = self.predictive_analyzer.generate_forecast(
                    ticker=ticker,
                    historical_data=stock_chart,
                    quote=quote_data,
                    sentiment_data=combined_sentiment,
                    news_data=news_data
                )
                print(f"  ✓ Predictions generated")
            except Exception as e:
                print(f"  ✗ Prediction generation failed: {e}")
        else:
            print(f"  ⚠️  Skipping predictions (missing chart or quote data)")
        
        print(f"\n[RATING] Calculating investment rating...")
        # Generate rating
        rating = self._calculate_rating(social_data, combined_sentiment)
        print(f"  ✓ Rating: {rating}")
        
        total_time = time.time() - start_time
        print(f"\n{'='*60}")
        print(f"REPORT GENERATION COMPLETE in {total_time:.2f}s")
        print(f"{'='*60}\n")
        
        return {
            'ticker': ticker,
            'generated_at': datetime.now().isoformat(),
            'quote': quote_data,
            'chart_data': stock_chart,
            'predictions': predictions,
            'executive_summary': {
                'rating': rating,
                'recommendation': self._get_recommendation(rating)
            },
            'combined_sentiment': combined_sentiment,
            'social_pulse': social_data,
            'news_summary': news_data
        }
    
    def _get_stock_chart(self, ticker):
        """Fetch stock chart data"""
        try:
            print(f"  → Fetching historical data...")
            data = self.stock_data.get_stock_data(ticker)
            if data:
                performance = self.stock_data.calculate_performance(data['close'])
                data['performance'] = performance
                source = data.get('source', 'Unknown')
                print(f"  ✓ Chart data retrieved from {source}")
                
                # Log sample data for verification
                if data.get('close') and len(data['close']) > 0:
                    print(f"  → Sample prices: First=${data['close'][0]:.2f}, Last=${data['close'][-1]:.2f}")
            return data
        except Exception as e:
            print(f"  ✗ Chart data failed: {e}")
            return {'error': str(e)}
    
    def _get_quote_data(self, ticker):
        """Fetch current quote data"""
        try:
            print(f"  → Fetching current quote...")
            quote = self.stock_data.get_quote(ticker)
            print(f"  ✓ Quote retrieved: ${quote.get('price', 'N/A')}")
            return quote
        except Exception as e:
            print(f"  ✗ Quote failed: {e}")
            return {'error': str(e)}

    
    def _get_social_data(self, ticker):
        """Fetch social sentiment data"""
        try:
            print(f"  → Analyzing social sentiment...")
            reddit_data = self.social.analyze_reddit_sentiment(ticker)
            print(f"  ✓ Social data: {reddit_data.get('sentiment', 'N/A')} ({reddit_data.get('source', 'Unknown')})")
            
            # Get posts for LLM analysis (only if we have posts)
            posts = reddit_data.get('top_posts', [])
            
            # Perform LLM sentiment analysis only if we have posts
            if posts:
                try:
                    print(f"  → Running LLM sentiment on {len(posts)} posts...")
                    llm_sentiment = self.sentiment_analyzer.analyze_reddit_posts(posts)
                    reddit_data['llm_sentiment'] = llm_sentiment
                    print(f"  ✓ LLM sentiment complete")
                except Exception as e:
                    print(f"  ⚠️  LLM sentiment skipped: {str(e)[:100]}")
            
            return reddit_data
        except Exception as e:
            print(f"  ✗ Social data failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                'error': str(e), 
                'sentiment': 'Neutral', 
                'sentiment_score': 0, 
                'mentions': 0, 
                'top_posts': [],
                'source': 'Error fallback'
            }
    
    def _get_news_data(self, ticker):
        """Fetch news data"""
        try:
            print(f"  → Fetching news headlines...")
            news = self.news.get_news_headlines(ticker)
            print(f"  ✓ News retrieved: {len(news.get('headlines', []))} headlines ({news.get('source', 'Unknown')})")
            
            # Perform LLM sentiment analysis on headlines (only if we have headlines)
            headlines = news.get('headlines', [])
            if headlines:
                try:
                    print(f"  → Running LLM sentiment on {len(headlines)} headlines...")
                    llm_sentiment = self.sentiment_analyzer.analyze_news_headlines(headlines)
                    news['llm_sentiment'] = llm_sentiment
                    print(f"  ✓ News LLM sentiment complete")
                except Exception as e:
                    print(f"  ⚠️  News LLM sentiment skipped: {str(e)[:100]}")
            
            return news
        except Exception as e:
            print(f"  ✗ News fetch failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                'error': str(e), 
                'headlines': [], 
                'summary': 'News unavailable',
                'source': 'Error fallback'
            }
    
    def _calculate_rating(self, social, combined_sentiment):
        """Calculate bull/bear rating"""
        score = 0
        
        # LLM sentiment score (weighted heavily)
        sentiment_score = combined_sentiment.get('average_score', 0)
        if sentiment_score > 0.3:
            score += 3
        elif sentiment_score > 0.1:
            score += 1
        elif sentiment_score < -0.3:
            score -= 3
        elif sentiment_score < -0.1:
            score -= 1
        
        # Traditional social sentiment
        sentiment = social.get('sentiment', '')
        if 'Bullish' in sentiment:
            score += 1
        elif 'Bearish' in sentiment:
            score -= 1
        
        if score >= 3:
            return 'Strong Bull'
        elif score >= 1:
            return 'Moderate Bull'
        elif score <= -2:
            return 'Bear'
        else:
            return 'Neutral'
    
    def _get_recommendation(self, rating):
        """Get investment recommendation"""
        recommendations = {
            'Strong Bull': 'High conviction BUY - favorable sentiment and momentum',
            'Moderate Bull': 'BUY with caution - monitor developments',
            'Neutral': 'HOLD - wait for clearer signals',
            'Bear': 'AVOID or SELL - unfavorable conditions'
        }
        return recommendations.get(rating, 'Insufficient data')
