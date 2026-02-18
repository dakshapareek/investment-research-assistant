import requests
from datetime import datetime, timedelta
from config import GOOGLE_API_KEY, OPENAI_API_KEY, NEWS_API_KEY
import json
import os

class NewsClient:
    def __init__(self, model_name='gpt-4o-mini'):
        self.llm_available = False
        self.model_name = model_name
        self.news_api_key = NEWS_API_KEY
        self.ticker_db = self._load_ticker_database()
        
        # Initialize LLM for summarization only (not for fetching news)
        if OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=OPENAI_API_KEY)
                self.llm_available = True
                self.llm_type = 'OpenAI'
                print(f"✓ OpenAI ({model_name}) initialized for news summarization")
            except Exception as e:
                print(f"OpenAI initialization failed: {e}")
        elif GOOGLE_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=GOOGLE_API_KEY)
                self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
                self.llm_available = True
                self.llm_type = 'Gemini'
                print(f"✓ Google Gemini initialized for news summarization")
            except Exception as e:
                print(f"LLM initialization failed in NewsClient: {e}")
        
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
    
    def get_news_headlines(self, ticker):
        """Fetch REAL news headlines from NewsAPI"""
        
        try:
            # Try NewsAPI first (real news with URLs)
            if self.news_api_key:
                return self._get_news_from_newsapi(ticker)
            else:
                print("  ⚠️  No NewsAPI key configured, using fallback")
                return self._get_fallback_news(ticker)
                
        except Exception as e:
            print(f"News fetch error: {e}")
            return self._get_fallback_news(ticker)
    
    def _get_news_from_newsapi(self, ticker):
        """Fetch REAL news from NewsAPI.org using company name"""
        try:
            # Get company name for better search results
            company_name = self._get_company_name(ticker)
            print(f"  → Fetching real news for {ticker} ({company_name})...")
            
            # Calculate date range (past 7 days, prioritize recent)
            to_date = datetime.now()
            from_date = to_date - timedelta(days=7)
            
            # Build search query using company name instead of ticker
            # This gives much more relevant results
            if company_name != ticker:
                # Use company name for search
                search_query = f'"{company_name}" AND (stock OR shares OR trading OR earnings OR revenue)'
            else:
                # Fallback to ticker if no company name found
                if len(ticker) <= 4:
                    search_query = f'"{ticker}" AND (stock OR shares OR trading OR NYSE OR NASDAQ)'
                else:
                    search_query = f'{ticker} stock OR {ticker} shares'
            
            print(f"  → Search query: {search_query}")
            
            # Search for company/ticker news
            url = 'https://newsapi.org/v2/everything'
            params = {
                'q': search_query,
                'from': from_date.strftime('%Y-%m-%d'),
                'to': to_date.strftime('%Y-%m-%d'),
                'language': 'en',
                'sortBy': 'relevancy',  # Most relevant first
                'pageSize': 20,  # Get more to filter better
                'apiKey': self.news_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                if articles:
                    # Filter articles to ensure they're actually about the stock
                    filtered_articles = []
                    ticker_upper = ticker.upper()
                    company_upper = company_name.upper()
                    
                    for article in articles:
                        title = article.get('title', '').upper()
                        description = article.get('description', '').upper()
                        
                        # Check if ticker or company name appears in title or description
                        if (ticker_upper in title or ticker_upper in description or
                            company_upper in title or company_upper in description or
                            'STOCK' in title or 'SHARES' in title or 
                            'TRADING' in title or 'EARNINGS' in title):
                            filtered_articles.append(article)
                            if len(filtered_articles) >= 7:
                                break
                    
                    # If we filtered too much, use original articles
                    if len(filtered_articles) < 3 and len(articles) >= 3:
                        filtered_articles = articles[:7]
                    
                    # Convert to our format with REAL URLs
                    headlines = []
                    for article in filtered_articles[:7]:  # Top 7 articles
                        headlines.append({
                            'title': article.get('title', ''),
                            'source': article.get('source', {}).get('name', 'Unknown'),
                            'url': article.get('url', '#'),
                            'date': self._format_date(article.get('publishedAt', ''))
                        })
                    
                    print(f"  ✓ Found {len(headlines)} real news articles from NewsAPI")
                    
                    # Use LLM to summarize REAL news (not generate fake news)
                    detailed_summary = self._summarize_real_news(headlines, ticker, company_name)
                    
                    return {
                        'headlines': headlines,
                        'summary': f'Recent news from {len(headlines)} sources',
                        'detailed_summary': detailed_summary,
                        'sentiment': 'neutral',
                        'source': 'NewsAPI.org'
                    }
            
            print(f"  ⚠️  NewsAPI returned status {response.status_code}")
            return self._get_fallback_news(ticker)
            
        except Exception as e:
            print(f"  ✗ NewsAPI failed: {e}")
            return self._get_fallback_news(ticker)
    
    def _format_date(self, date_str):
        """Format ISO date to readable format"""
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            now = datetime.now(dt.tzinfo)
            diff = now - dt
            
            if diff.days == 0:
                hours = diff.seconds // 3600
                if hours == 0:
                    minutes = diff.seconds // 60
                    return f"{minutes} minutes ago"
                return f"{hours} hours ago"
            elif diff.days == 1:
                return "Yesterday"
            elif diff.days < 7:
                return f"{diff.days} days ago"
            else:
                return dt.strftime('%b %d, %Y')
        except:
            return date_str
    
    def _summarize_real_news(self, headlines, ticker, company_name):
        """Use LLM to summarize REAL news headlines (not generate fake news)"""
        if not self.llm_available or not headlines:
            return f"Recent news coverage for {company_name} ({ticker}). Configure LLM API for detailed analysis."
        
        try:
            # Create prompt with REAL headlines
            headlines_text = "\n".join([
                f"- {h['title']} ({h['source']}, {h['date']})"
                for h in headlines
            ])
            
            prompt = f"""Analyze these REAL news headlines about {company_name} ({ticker}) and write a 3-4 paragraph summary:

{headlines_text}

Write a professional financial analysis covering:
1. Key developments and announcements
2. Market reaction and analyst opinions  
3. Industry context and competitive landscape
4. Forward-looking implications

IMPORTANT: Base your analysis ONLY on the headlines provided above. Do not make up additional news or events."""

            if self.llm_type == 'OpenAI':
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a financial analyst. Summarize only the provided news, do not invent additional information."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=800,
                    temperature=0.5
                )
                return response.choices[0].message.content.strip()
            else:  # Gemini
                response = self.model.generate_content(prompt)
                return response.text.strip()
                
        except Exception as e:
            print(f"  ⚠️  LLM summarization failed: {e}")
            return f"Recent news coverage for {company_name} ({ticker}) from {len(headlines)} sources."
    
    def _get_news_from_web_search(self, ticker):
        """DEPRECATED: LLMs cannot actually search the web"""
        # This method generated fake news - now using NewsAPI instead
        return self._get_fallback_news(ticker)
    
    def _get_fallback_news(self, ticker):
        """Fallback news when APIs unavailable"""
        
        # Generate detailed fallback summary
        detailed_summary = f"""Recent Market Activity:
{ticker} has been actively traded in recent sessions with investors closely monitoring company developments. Market participants are evaluating the stock's performance in the context of broader market trends and sector dynamics.

Analyst Perspectives:
Financial analysts continue to track {ticker}'s fundamentals, including revenue growth, profitability metrics, and competitive positioning. The investment community is assessing the company's strategic initiatives and their potential impact on long-term value creation.

Investor Sentiment:
Market sentiment toward {ticker} reflects a mix of optimism about growth prospects and caution regarding market volatility. Institutional and retail investors are weighing risk-reward considerations as they make portfolio allocation decisions.

Forward Outlook:
Looking ahead, {ticker}'s trajectory will depend on execution of business strategy, market conditions, and ability to navigate industry challenges. Investors should monitor upcoming earnings reports, product launches, and management commentary for insights into future performance.

Note: Configure news APIs or Reddit API in backend/.env for real-time news analysis and social sentiment data."""

        return {
            'headlines': [
                {
                    'title': f'{ticker} trading activity reflects market dynamics',
                    'source': 'Market Analysis',
                    'url': f'https://finance.yahoo.com/quote/{ticker}',
                    'date': 'Recent'
                },
                {
                    'title': f'Investors monitor {ticker} fundamentals and growth prospects',
                    'source': 'Market Analysis',
                    'url': f'https://finance.yahoo.com/quote/{ticker}/analysis',
                    'date': 'Recent'
                },
                {
                    'title': f'Analysts evaluate {ticker} competitive positioning',
                    'source': 'Market Analysis',
                    'url': f'https://finance.yahoo.com/quote/{ticker}/key-statistics',
                    'date': 'Recent'
                },
                {
                    'title': f'Market participants assess {ticker} risk-reward profile',
                    'source': 'Market Analysis',
                    'url': f'https://finance.yahoo.com/quote/{ticker}/profile',
                    'date': 'Recent'
                },
                {
                    'title': f'{ticker} outlook depends on execution and market conditions',
                    'source': 'Market Analysis',
                    'url': f'https://finance.yahoo.com/quote/{ticker}/news',
                    'date': 'Recent'
                }
            ],
            'summary': f'Market analysis for {ticker} (Configure APIs for real-time data)',
            'detailed_summary': detailed_summary,
            'sentiment': 'neutral',
            'key_themes': ['Market Activity', 'Analyst Coverage', 'Investor Sentiment', 'Forward Outlook'],
            'source': 'Fallback Analysis'
        }

