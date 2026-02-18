import requests
from bs4 import BeautifulSoup
from config import GOOGLE_API_KEY, OPENAI_API_KEY
import re
import time
import json
import os

class SocialClient:
    def __init__(self, model_name='gpt-4o-mini'):
        self.llm_available = False
        self.model_name = model_name
        self.llm_type = None
        self.ticker_db = self._load_ticker_database()
        
        # Try OpenAI first
        if OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=OPENAI_API_KEY)
                self.llm_available = True
                self.llm_type = 'OpenAI'
                print(f"✓ OpenAI ({model_name}) initialized for social analysis")
            except Exception as e:
                print(f"OpenAI initialization failed in SocialClient: {e}")
        
        # Fallback to Gemini
        if not self.llm_available and GOOGLE_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=GOOGLE_API_KEY)
                self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
                self.llm_available = True
                self.llm_type = 'Gemini'
                print(f"✓ Google Gemini initialized for social analysis (OpenAI not available)")
            except Exception as e:
                print(f"LLM initialization failed in SocialClient: {e}")
    
    def _load_ticker_database(self):
        """Load ticker to company name mappings"""
        try:
            db_path = os.path.join(os.path.dirname(__file__), '..', 'ticker_database.json')
            with open(db_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"  ⚠️  Failed to load ticker database: {e}")
            return {}
    
    def _get_company_name(self, ticker):
        """Get company name from ticker symbol"""
        # Handle crypto and special cases
        if '-' in ticker:
            # Crypto like BTC-USD
            base = ticker.split('-')[0]
            crypto_names = {
                'BTC': 'Bitcoin',
                'ETH': 'Ethereum',
                'DOGE': 'Dogecoin',
                'ADA': 'Cardano',
                'SOL': 'Solana'
            }
            return crypto_names.get(base, ticker)
        
        # Look up in database
        company_name = self.ticker_db.get(ticker, '')
        
        # Clean up company name (remove suffixes like "Inc", "Corp", "Ltd")
        if company_name:
            # Extract main company name before common suffixes
            for suffix in [' Inc', ' Corp', ' Corporation', ' Ltd', ' Limited', ' PLC', ' SA', ' AG']:
                if suffix in company_name:
                    company_name = company_name.split(suffix)[0]
                    break
        
        return company_name if company_name else ticker
    
    def _generate_content(self, prompt, max_tokens=1500):
        """Unified method to generate content with OpenAI or Gemini"""
        try:
            if self.llm_type == 'OpenAI':
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a financial analyst analyzing social media sentiment."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
            
            elif self.llm_type == 'Gemini':
                response = self.model.generate_content(prompt)
                return response.text.strip()
            
            else:
                raise Exception("No LLM available")
        
        except Exception as e:
            print(f"LLM generation error: {e}")
            raise
    
    def analyze_reddit_sentiment(self, ticker, limit=100):
        """Analyze social sentiment using web scraping and LLM"""
        
        # Use LLM with web search for comprehensive social analysis
        if self.llm_available:
            company_name = self._get_company_name(ticker)
            print(f"  → Scraping social media for {ticker} ({company_name})...")
            return self._analyze_social_via_web_search(ticker, company_name)
        
        # Final fallback
        return self._get_fallback_social(ticker)
    
    def _scrape_reddit_posts(self, ticker, company_name):
        """Scrape Reddit posts without login using public JSON API"""
        posts = []
        subreddits = ['stocks', 'wallstreetbets', 'investing', 'StockMarket']
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        print(f"  → Starting Reddit scraping for {ticker} ({company_name})...")
        
        # Use company name for search if available, otherwise use ticker
        search_term = company_name if company_name != ticker else ticker
        
        for subreddit in subreddits:
            try:
                # Use Reddit's public JSON API (no auth required)
                # Search using company name for better relevance
                url = f'https://www.reddit.com/r/{subreddit}/search.json?q={search_term}&restrict_sr=1&sort=new&t=week&limit=25'
                
                print(f"    → Fetching from r/{subreddit} (searching for '{search_term}')...")
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    children = data.get('data', {}).get('children', [])
                    
                    if children:
                        for post in children:
                            post_data = post.get('data', {})
                            title = post_data.get('title', '')
                            selftext = post_data.get('selftext', '')
                            
                            # Check if ticker OR company name is mentioned
                            title_upper = title.upper()
                            selftext_upper = selftext.upper()
                            ticker_upper = ticker.upper()
                            company_upper = company_name.upper()
                            
                            if (ticker_upper in title_upper or ticker_upper in selftext_upper or
                                company_upper in title_upper or company_upper in selftext_upper):
                                posts.append({
                                    'title': title,
                                    'score': post_data.get('score', 0),
                                    'comments': post_data.get('num_comments', 0),
                                    'subreddit': subreddit,
                                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                                    'created': post_data.get('created_utc', 0)
                                })
                        
                        print(f"    ✓ Found {len([p for p in posts if p['subreddit'] == subreddit])} relevant posts from r/{subreddit}")
                    else:
                        print(f"    ⊘ No posts found in r/{subreddit}")
                    
                    time.sleep(2)  # Rate limiting - be respectful
                    
                elif response.status_code == 429:
                    print(f"    ⚠️  Rate limited on r/{subreddit}, waiting...")
                    time.sleep(5)
                else:
                    print(f"    ⚠️  Reddit returned status {response.status_code} for r/{subreddit}")
                    
            except requests.exceptions.Timeout:
                print(f"    ✗ Timeout fetching r/{subreddit}")
            except requests.exceptions.RequestException as e:
                print(f"    ✗ Request error for r/{subreddit}: {str(e)[:50]}")
            except Exception as e:
                print(f"    ✗ Error scraping r/{subreddit}: {str(e)[:50]}")
        
        # Sort by score (most upvoted first)
        posts.sort(key=lambda x: x['score'], reverse=True)
        
        print(f"  ✓ Total Reddit posts scraped: {len(posts)}")
        return posts
    
    def _scrape_twitter_posts(self, ticker):
        """Scrape Twitter/X posts without login (limited public access)"""
        # Note: Twitter/X has restricted public access significantly
        # This is a placeholder for potential future implementation
        # For now, we'll rely on LLM web search
        return []
    
    def _analyze_social_via_web_search(self, ticker, company_name):
        """Use web scraping + LLM to analyze social sentiment from multiple sources"""
        import json
        scraped_posts = []
        
        try:
            # ALWAYS scrape Reddit first
            print(f"  → Starting social media analysis for {ticker} ({company_name})...")
            scraped_posts = self._scrape_reddit_posts(ticker, company_name)
            
            if scraped_posts:
                print(f"  ✓ Successfully scraped {len(scraped_posts)} Reddit posts")
            else:
                print(f"  ⚠️  No Reddit posts found for {ticker} or {company_name}")
            
            # If LLM available, use it to analyze the scraped posts
            if self.llm_available and scraped_posts:
                print(f"  → Analyzing scraped posts with LLM...")
                
                # Build context from scraped posts
                posts_context = "\n\nScraped Reddit posts (sorted by popularity):\n"
                for i, post in enumerate(scraped_posts[:15], 1):
                    posts_context += f"{i}. [{post['subreddit']}] {post['title']}\n"
                    posts_context += f"   Score: {post['score']} upvotes | Comments: {post['comments']}\n"
                
                # Use LLM to analyze scraped data
                prompt = f"""Analyze the social media sentiment for {company_name} ({ticker}) stock based on these Reddit posts:
{posts_context}

Based on these {len(scraped_posts)} Reddit posts, provide a comprehensive 4-paragraph analysis:

Paragraph 1: Overall Social Sentiment
- What is the dominant sentiment (bullish/bearish/neutral)?
- What are retail investors saying about {company_name}?
- Are there any strong opinions or consensus forming?

Paragraph 2: Key Discussion Topics
- What specific aspects of {company_name} are being discussed?
- Are people talking about earnings, products, management, competition?
- What concerns or opportunities are being highlighted?

Paragraph 3: Retail Positioning
- Are retail investors buying, selling, or holding?
- What trading strategies are being discussed?
- Is there momentum or FOMO evident?

Paragraph 4: Sentiment Implications
- How might this social sentiment impact the stock?
- Are there any red flags or positive catalysts mentioned?
- What should investors watch for?

Provide your analysis in JSON format:
{{
    "sentiment": "bullish/bearish/neutral",
    "sentiment_score": -1.0 to 1.0 (where -1 is very bearish, 0 is neutral, 1 is very bullish),
    "confidence": "high/medium/low",
    "mentions": {len(scraped_posts)},
    "detailed_summary": "4 paragraphs separated by \\n\\n",
    "key_topics": ["topic1", "topic2", "topic3", "topic4", "topic5"],
    "bullish_points": ["point1", "point2"],
    "bearish_points": ["point1", "point2"]
}}"""

                try:
                    result_text = self._generate_content(prompt, max_tokens=1500)
                    
                    # Parse JSON response
                    import json
                    if '```json' in result_text:
                        result_text = result_text.split('```json')[1].split('```')[0].strip()
                    elif '```' in result_text:
                        result_text = result_text.split('```')[1].split('```')[0].strip()
                    
                    data = json.loads(result_text)
                    print(f"  ✓ LLM sentiment analysis complete")
                    
                    return {
                        'sentiment': data.get('sentiment', 'neutral').capitalize(),
                        'sentiment_score': data.get('sentiment_score', 0),
                        'confidence': data.get('confidence', 'medium'),
                        'mentions': len(scraped_posts),
                        'detailed_summary': data.get('detailed_summary', ''),
                        'key_topics': data.get('key_topics', []),
                        'bullish_points': data.get('bullish_points', []),
                        'bearish_points': data.get('bearish_points', []),
                        'top_posts': scraped_posts[:5],
                        'source': f'Reddit Scraping ({len(scraped_posts)} posts) + LLM Analysis'
                    }
                    
                except json.JSONDecodeError as e:
                    print(f"  ⚠️  JSON parse error: {str(e)[:50]}")
                    # Return with scraped data but basic analysis
                    return {
                        'sentiment': 'Neutral',
                        'sentiment_score': 0,
                        'confidence': 'low',
                        'mentions': len(scraped_posts),
                        'detailed_summary': result_text if result_text else f'Analyzed {len(scraped_posts)} Reddit posts about {company_name} ({ticker}).',
                        'top_posts': scraped_posts[:5],
                        'source': f'Reddit Scraping ({len(scraped_posts)} posts) + LLM Analysis'
                    }
                    
                except Exception as e:
                    print(f"  ✗ LLM analysis error: {str(e)[:100]}")
                    # Return scraped data without LLM analysis
                    return {
                        'sentiment': 'Neutral',
                        'sentiment_score': 0,
                        'confidence': 'low',
                        'mentions': len(scraped_posts),
                        'detailed_summary': f'Scraped {len(scraped_posts)} Reddit posts about {company_name} ({ticker}). LLM analysis failed: {str(e)[:100]}',
                        'top_posts': scraped_posts[:5],
                        'source': f'Reddit Scraping Only ({len(scraped_posts)} posts)'
                    }
            
            elif scraped_posts:
                # No LLM, just return scraped data
                print(f"  ⚠️  LLM not available, returning scraped data only")
                return {
                    'sentiment': 'Neutral',
                    'sentiment_score': 0,
                    'confidence': 'low',
                    'mentions': len(scraped_posts),
                    'detailed_summary': f'Successfully scraped {len(scraped_posts)} Reddit posts about {company_name} ({ticker}). LLM analysis unavailable - configure GOOGLE_API_KEY in .env for AI-powered sentiment analysis.',
                    'top_posts': scraped_posts[:5],
                    'source': f'Reddit Scraping Only ({len(scraped_posts)} posts)'
                }
            else:
                # No posts scraped
                print(f"  ⚠️  No posts found, using fallback")
                return self._get_fallback_social(ticker)
                
        except Exception as e:
            error_msg = str(e)
            print(f"  ✗ Social analysis error: {error_msg[:100]}")
            
            # If we have scraped posts, return them even if analysis failed
            if scraped_posts:
                return {
                    'sentiment': 'Neutral',
                    'sentiment_score': 0,
                    'confidence': 'low',
                    'mentions': len(scraped_posts),
                    'detailed_summary': f'Scraped {len(scraped_posts)} Reddit posts about {company_name} ({ticker}). Analysis error: {error_msg[:100]}',
                    'top_posts': scraped_posts[:5],
                    'source': f'Reddit Scraping Only ({len(scraped_posts)} posts)'
                }
            
            return self._get_fallback_social(ticker)
    

    
    def _get_fallback_social(self, ticker):
        """Fallback social sentiment when APIs unavailable"""
        
        detailed_summary = f"""Social Media Landscape:
Social media discussions about {ticker} reflect diverse perspectives from retail and institutional investors. Online communities actively debate the stock's fundamentals, technical patterns, and market positioning.

Retail Investor Activity:
Retail traders on platforms like Reddit and StockTwits share analysis, trade ideas, and market commentary about {ticker}. The community sentiment provides insights into grassroots investor positioning and momentum.

Influential Voices:
Notable traders and analysts contribute to the discourse around {ticker}, sharing technical analysis, fundamental research, and trading strategies. These perspectives help shape broader market sentiment.

Sentiment Implications:
Social sentiment serves as a contrarian indicator and momentum gauge for {ticker}. Strong retail interest can drive short-term volatility while sustained institutional backing suggests longer-term conviction.

Note: AI-powered analysis temporarily unavailable. The system uses web scraping to gather Reddit posts but requires Google Gemini API for detailed sentiment analysis. Check your API quota at https://ai.google.dev/rate-limit"""

        return {
            'sentiment': 'Neutral',
            'sentiment_score': 0,
            'mentions': 'unknown',
            'detailed_summary': detailed_summary,
            'top_posts': [],
            'source': 'Fallback Analysis (API Quota Exceeded)'
        }

