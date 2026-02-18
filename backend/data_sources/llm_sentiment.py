import os
from config import GOOGLE_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY

class LLMSentimentAnalyzer:
    """LLM-based sentiment analysis for social media and news"""
    
    def __init__(self, model_name='gpt-4o-mini'):
        self.llm_available = False
        self.llm_type = None
        self.model_name = model_name
        
        # Try OpenAI first (better quality and efficiency)
        if OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=OPENAI_API_KEY)
                self.model_name = model_name  # gpt-4o-mini, gpt-4o, or gpt-3.5-turbo
                self.llm_available = True
                self.llm_type = 'OpenAI'
                print(f"✓ OpenAI ({model_name}) initialized for sentiment analysis")
            except Exception as e:
                print(f"✗ OpenAI initialization failed: {e}")
        
        # Fallback to Google Gemini if OpenAI not available
        if not self.llm_available and GOOGLE_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=GOOGLE_API_KEY)
                self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
                self.llm_available = True
                self.llm_type = 'Google Gemini'
                print(f"✓ Google Gemini initialized for sentiment analysis (OpenAI not available)")
            except Exception as e:
                print(f"✗ Google Gemini initialization failed: {e}")
        
        # Fallback to keyword-based if no LLM available
        if not self.llm_available:
            print("ℹ Using keyword-based sentiment analysis (configure OPENAI_API_KEY or GOOGLE_API_KEY for AI analysis)")
            self._init_keywords()
    
    def _generate_content(self, prompt, max_tokens=1000):
        """Unified method to generate content using OpenAI or Gemini"""
        try:
            if self.llm_type == 'OpenAI':
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
            else:  # Gemini
                response = self.model.generate_content(prompt)
                return response.text.strip()
        except Exception as e:
            raise Exception(f"Content generation failed: {e}")
    
    def _init_keywords(self):
        """Initialize keyword lists for fallback analysis"""
        self.positive_keywords = [
            'bullish', 'buy', 'moon', 'rocket', 'gain', 'profit', 'up', 'surge',
            'rally', 'breakout', 'strong', 'growth', 'upgrade', 'beat', 'outperform',
            'positive', 'good', 'great', 'excellent', 'amazing', 'love', 'best'
        ]
        self.negative_keywords = [
            'bearish', 'sell', 'crash', 'loss', 'down', 'drop', 'fall', 'decline',
            'weak', 'downgrade', 'miss', 'underperform', 'negative', 'bad', 'worst',
            'terrible', 'avoid', 'concern', 'risk', 'warning', 'fear'
        ]
    
    def analyze_text(self, text):
        """Analyze sentiment of a single text using LLM or keywords"""
        if not text:
            return {'sentiment': 'neutral', 'score': 0, 'confidence': 0}
        
        if self.llm_available:
            return self._analyze_with_llm(text)
        else:
            return self._analyze_with_keywords(text)
    
    def _analyze_with_llm(self, text):
        """Analyze sentiment using Google Gemini"""
        try:
            prompt = f"""Analyze the sentiment of this financial text and respond ONLY with a JSON object in this exact format:
{{"sentiment": "bullish" or "bearish" or "neutral", "score": number between -1 and 1, "confidence": number between 0 and 1}}

Text: {text[:500]}

Rules:
- "bullish" = positive outlook on stock/market
- "bearish" = negative outlook on stock/market  
- "neutral" = mixed or unclear sentiment
- score: -1 (very bearish) to +1 (very bullish)
- confidence: 0 (uncertain) to 1 (very certain)

Respond with ONLY the JSON object, no other text."""

            result_text = self._generate_content(prompt, max_tokens=200)
            
            # Extract JSON from response
            import json
            import re
            
            # Try to find JSON in response
            json_match = re.search(r'\{[^}]+\}', result_text)
            if json_match:
                result = json.loads(json_match.group())
                return {
                    'sentiment': result.get('sentiment', 'neutral'),
                    'score': float(result.get('score', 0)),
                    'confidence': float(result.get('confidence', 0.5)),
                    'llm_used': True
                }
            
            # Fallback to keyword analysis if JSON parsing fails
            return self._analyze_with_keywords(text)
            
        except Exception as e:
            error_msg = str(e)
            if '429' in error_msg or 'quota' in error_msg.lower():
                print(f"⚠️  Gemini API quota exceeded - using keyword analysis")
            else:
                print(f"⚠️  LLM analysis error: {error_msg[:100]}")
            return self._analyze_with_keywords(text)
    
    def _analyze_with_keywords(self, text):
        """Fallback keyword-based analysis"""
        if not hasattr(self, 'positive_keywords'):
            self._init_keywords()
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.positive_keywords if word in text_lower)
        negative_count = sum(1 for word in self.negative_keywords if word in text_lower)
        
        total = positive_count + negative_count
        if total == 0:
            return {'sentiment': 'neutral', 'score': 0, 'confidence': 0.5, 'llm_used': False}
        
        score = (positive_count - negative_count) / total
        
        if score > 0.3:
            sentiment = 'bullish'
        elif score < -0.3:
            sentiment = 'bearish'
        else:
            sentiment = 'neutral'
        
        confidence = min(abs(score), 1.0)
        
        return {
            'sentiment': sentiment,
            'score': round(score, 2),
            'confidence': round(confidence, 2),
            'llm_used': False
        }
    
    def analyze_batch(self, texts):
        """Analyze sentiment of multiple texts"""
        if not texts:
            return {
                'overall_sentiment': 'neutral',
                'average_score': 0,
                'bullish_count': 0,
                'bearish_count': 0,
                'neutral_count': 0,
                'confidence': 0,
                'llm_used': self.llm_available
            }
        
        # For LLM, analyze in batches for efficiency
        if self.llm_available and len(texts) > 5:
            return self._analyze_batch_with_llm(texts)
        
        # Analyze each text individually
        results = [self.analyze_text(text) for text in texts]
        
        bullish = sum(1 for r in results if r['sentiment'] == 'bullish')
        bearish = sum(1 for r in results if r['sentiment'] == 'bearish')
        neutral = sum(1 for r in results if r['sentiment'] == 'neutral')
        
        avg_score = sum(r['score'] for r in results) / len(results)
        avg_confidence = sum(r['confidence'] for r in results) / len(results)
        
        if bullish > bearish and bullish > neutral:
            overall = 'bullish'
        elif bearish > bullish and bearish > neutral:
            overall = 'bearish'
        else:
            overall = 'neutral'
        
        return {
            'overall_sentiment': overall,
            'average_score': round(avg_score, 2),
            'bullish_count': bullish,
            'bearish_count': bearish,
            'neutral_count': neutral,
            'confidence': round(avg_confidence, 2),
            'total_analyzed': len(texts),
            'llm_used': self.llm_available
        }
    
    def _analyze_batch_with_llm(self, texts):
        """Analyze multiple texts in one LLM call for efficiency"""
        try:
            # Combine texts with numbering
            combined_text = "\n\n".join([f"{i+1}. {text[:200]}" for i, text in enumerate(texts[:10])])
            
            prompt = f"""Analyze the overall sentiment of these {len(texts[:10])} financial texts and respond ONLY with a JSON object:

{combined_text}

Respond with ONLY this JSON format:
{{"overall_sentiment": "bullish" or "bearish" or "neutral", "average_score": number between -1 and 1, "confidence": number between 0 and 1, "bullish_count": number, "bearish_count": number, "neutral_count": number}}

Rules:
- Count how many texts are bullish, bearish, or neutral
- Calculate average sentiment score
- Provide overall confidence level"""

            result_text = self._generate_content(prompt, max_tokens=500)
            
            import json
            import re
            
            json_match = re.search(r'\{[^}]+\}', result_text)
            if json_match:
                result = json.loads(json_match.group())
                return {
                    'overall_sentiment': result.get('overall_sentiment', 'neutral'),
                    'average_score': float(result.get('average_score', 0)),
                    'bullish_count': int(result.get('bullish_count', 0)),
                    'bearish_count': int(result.get('bearish_count', 0)),
                    'neutral_count': int(result.get('neutral_count', 0)),
                    'confidence': float(result.get('confidence', 0.5)),
                    'total_analyzed': len(texts),
                    'llm_used': True
                }
        except Exception as e:
            print(f"Batch LLM analysis error: {e}")
        
        # Fallback to individual analysis
        results = [self.analyze_text(text) for text in texts]
        bullish = sum(1 for r in results if r['sentiment'] == 'bullish')
        bearish = sum(1 for r in results if r['sentiment'] == 'bearish')
        neutral = sum(1 for r in results if r['sentiment'] == 'neutral')
        avg_score = sum(r['score'] for r in results) / len(results)
        avg_confidence = sum(r['confidence'] for r in results) / len(results)
        
        if bullish > bearish and bullish > neutral:
            overall = 'bullish'
        elif bearish > bullish and bearish > neutral:
            overall = 'bearish'
        else:
            overall = 'neutral'
        
        return {
            'overall_sentiment': overall,
            'average_score': round(avg_score, 2),
            'bullish_count': bullish,
            'bearish_count': bearish,
            'neutral_count': neutral,
            'confidence': round(avg_confidence, 2),
            'total_analyzed': len(texts),
            'llm_used': False
        }
    
    def analyze_reddit_posts(self, posts):
        """Analyze sentiment from Reddit posts with detailed summary"""
        if not posts:
            return self.analyze_batch([])
        
        texts = []
        for post in posts:
            title = post.get('title', '')
            score = post.get('score', 0)
            weight = max(1, min(score // 10, 5))
            texts.extend([title] * weight)
        
        result = self.analyze_batch(texts)
        result['posts_analyzed'] = len(posts)
        
        # Generate detailed summary using LLM
        if self.llm_available and posts:
            result['detailed_summary'] = self._generate_reddit_summary(posts, result)
        
        return result
    
    def _generate_reddit_summary(self, posts, sentiment_result):
        """Generate detailed Reddit analysis summary using LLM"""
        try:
            top_posts_text = "\n".join([f"- {post['title']} ({post['score']} upvotes)" for post in posts[:5]])
            
            prompt = f"""Write a detailed 3-4 paragraph analysis of Reddit sentiment for this stock based on these posts:

{top_posts_text}

Overall Sentiment: {sentiment_result['overall_sentiment']}
Bullish: {sentiment_result['bullish_count']}, Bearish: {sentiment_result['bearish_count']}, Neutral: {sentiment_result['neutral_count']}

Write a professional analysis covering:
1. Overall community sentiment and key themes
2. Notable discussions and concerns
3. Retail investor positioning and conviction level
4. Potential risks from social media hype or FUD

Write in paragraph form, 3-4 paragraphs, professional tone."""

            summary = self._generate_content(prompt, max_tokens=800)
            return summary
        except Exception as e:
            print(f"Reddit summary generation error: {e}")
            return self._generate_fallback_reddit_summary(posts, sentiment_result)
    
    def _generate_fallback_reddit_summary(self, posts, sentiment_result):
        """Fallback Reddit summary without LLM"""
        sentiment = sentiment_result['overall_sentiment']
        total = len(posts)
        
        summary = f"Analysis of {total} Reddit posts shows {sentiment} sentiment. "
        
        if sentiment == 'bullish':
            summary += f"The community appears optimistic with {sentiment_result['bullish_count']} positive discussions. "
            summary += "Retail investors are showing strong conviction and accumulation interest. "
        elif sentiment == 'bearish':
            summary += f"The community shows concern with {sentiment_result['bearish_count']} negative discussions. "
            summary += "Retail investors appear cautious and some are considering reducing positions. "
        else:
            summary += "The community sentiment is mixed with divided opinions. "
        
        summary += f"Top discussions focus on recent price action and fundamental developments. "
        summary += "Monitor for potential volatility from retail trading activity."
        
        return summary
    
    def analyze_news_headlines(self, headlines):
        """Analyze sentiment from news headlines with detailed summary"""
        # Extract title text from headline dicts if needed
        if headlines and isinstance(headlines[0], dict):
            headline_texts = [h.get('title', str(h)) for h in headlines]
        else:
            headline_texts = headlines
        
        result = self.analyze_batch(headline_texts)
        
        # Generate detailed summary using LLM
        if self.llm_available and headline_texts:
            result['detailed_summary'] = self._generate_news_summary(headline_texts, result)
        
        return result
    
    def _generate_news_summary(self, headlines, sentiment_result):
        """Generate detailed news analysis summary using LLM"""
        try:
            headlines_text = "\n".join([f"- {h}" for h in headlines[:10]])
            
            prompt = f"""Write a detailed 3-4 paragraph analysis of news sentiment for this stock based on these headlines:

{headlines_text}

Overall Sentiment: {sentiment_result['overall_sentiment']}

Write a professional analysis covering:
1. Key news themes and market narratives
2. Institutional and analyst perspectives
3. Potential catalysts or concerns from news flow
4. Market implications and investor takeaways

Write in paragraph form, 3-4 paragraphs, professional financial analysis tone."""

            summary = self._generate_content(prompt, max_tokens=800)
            return summary
        except Exception as e:
            print(f"News summary generation error: {e}")
            return self._generate_fallback_news_summary(headlines, sentiment_result)
    
    def _generate_fallback_news_summary(self, headlines, sentiment_result):
        """Fallback news summary without LLM"""
        sentiment = sentiment_result['overall_sentiment']
        total = len(headlines)
        
        summary = f"Analysis of {total} recent news headlines indicates {sentiment} sentiment. "
        
        if sentiment == 'bullish':
            summary += "Media coverage highlights positive developments and strong fundamentals. "
            summary += "Analysts are generally optimistic about near-term prospects. "
        elif sentiment == 'bearish':
            summary += "Media coverage focuses on challenges and headwinds facing the company. "
            summary += "Analysts express caution about near-term performance. "
        else:
            summary += "Media coverage presents a balanced view with mixed perspectives. "
        
        summary += "Key themes include recent earnings, market positioning, and competitive dynamics. "
        summary += "Investors should monitor upcoming catalysts and management commentary."
        
        return summary
    
    def analyze_tweets(self, tweets):
        """Analyze sentiment from tweets"""
        texts = [tweet.get('text', '') for tweet in tweets if tweet.get('text')]
        return self.analyze_batch(texts)
    
    def get_sentiment_summary(self, reddit_data=None, news_data=None, twitter_data=None):
        """Get combined sentiment summary from all sources"""
        sources = []
        
        if reddit_data:
            reddit_sentiment = self.analyze_reddit_posts(reddit_data)
            sources.append({
                'source': 'Reddit',
                'sentiment': reddit_sentiment['overall_sentiment'],
                'score': reddit_sentiment['average_score'],
                'confidence': reddit_sentiment['confidence'],
                'details': reddit_sentiment
            })
        
        if news_data:
            news_sentiment = self.analyze_news_headlines(news_data)
            sources.append({
                'source': 'News',
                'sentiment': news_sentiment['overall_sentiment'],
                'score': news_sentiment['average_score'],
                'confidence': news_sentiment['confidence'],
                'details': news_sentiment
            })
        
        if twitter_data:
            twitter_sentiment = self.analyze_tweets(twitter_data)
            sources.append({
                'source': 'Twitter',
                'sentiment': twitter_sentiment['overall_sentiment'],
                'score': twitter_sentiment['average_score'],
                'confidence': twitter_sentiment['confidence'],
                'details': twitter_sentiment
            })
        
        if not sources:
            return {
                'overall_sentiment': 'neutral',
                'average_score': 0,
                'confidence': 0,
                'sources': []
            }
        
        # Calculate weighted average
        total_score = sum(s['score'] * s['confidence'] for s in sources)
        total_confidence = sum(s['confidence'] for s in sources)
        
        avg_score = total_score / total_confidence if total_confidence > 0 else 0
        
        if avg_score > 0.2:
            overall = 'bullish'
        elif avg_score < -0.2:
            overall = 'bearish'
        else:
            overall = 'neutral'
        
        return {
            'overall_sentiment': overall,
            'average_score': round(avg_score, 2),
            'confidence': round(total_confidence / len(sources), 2),
            'sources': sources
        }
