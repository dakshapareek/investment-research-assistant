from flask import Flask, jsonify, request
from flask_cors import CORS
from data_sources.social_client import SocialClient
from data_sources.news_client import NewsClient
from report_generator import ReportGenerator
from deep_analysis import DeepAnalysisEngine
from subscription_service import SubscriptionService
from scheduler import start_scheduler, get_scheduler
import json
import requests
from config import (
    FINANCIAL_MODELING_PREP_API_KEY, 
    ALPHA_VANTAGE_API_KEY,
    GOOGLE_API_KEY,
    OPENAI_API_KEY,
    FINNHUB_API_KEY,
    POLYGON_API_KEY,
    MARKETSTACK_API_KEY,
    EODHD_API_KEY,
    NEWS_API_KEY,
    TWITTER_BEARER_TOKEN,
    FRED_API_KEY
)

app = Flask(__name__)
CORS(app)

# Initialize subscription service
subscription_service = SubscriptionService()

# Initialize deep analysis engine
deep_analyzer = DeepAnalysisEngine()

# Store current model selection (in-memory, resets on restart)
current_model = 'gpt-4o-mini'  # OpenAI model for better efficiency

# Log API initialization status
def log_api_status():
    """Log which APIs are configured"""
    print("\n" + "="*60)
    print("API INITIALIZATION STATUS")
    print("="*60)
    
    # LLM APIs
    print("\n🤖 LLM APIs:")
    print(f"  {'✓' if GOOGLE_API_KEY else '✗'} Google Gemini: {'Configured' if GOOGLE_API_KEY else 'Not configured'}")
    
    # Financial APIs
    print("\n💰 Financial Data APIs:")
    print(f"  {'✓' if FINANCIAL_MODELING_PREP_API_KEY else '✗'} Financial Modeling Prep: {'Configured' if FINANCIAL_MODELING_PREP_API_KEY else 'Not configured'}")
    print(f"  {'✓' if ALPHA_VANTAGE_API_KEY else '✗'} Alpha Vantage: {'Configured' if ALPHA_VANTAGE_API_KEY else 'Not configured'}")
    print(f"  {'✓' if FINNHUB_API_KEY else '✗'} Finnhub: {'Configured' if FINNHUB_API_KEY else 'Not configured'}")
    print(f"  {'✓' if POLYGON_API_KEY else '✗'} Polygon.io: {'Configured' if POLYGON_API_KEY else 'Not configured'}")
    print(f"  {'✓' if MARKETSTACK_API_KEY else '✗'} Marketstack: {'Configured' if MARKETSTACK_API_KEY else 'Not configured'}")
    print(f"  {'✓' if EODHD_API_KEY else '✗'} EODHD: {'Configured' if EODHD_API_KEY else 'Not configured'}")
    
    # News APIs
    print("\n📰 News APIs:")
    print(f"  {'✓' if NEWS_API_KEY else '✗'} NewsAPI.org: {'Configured' if NEWS_API_KEY else 'Not configured'}")
    
    # Social APIs
    print("\n📱 Social Media:")
    print(f"  {'✓' if TWITTER_BEARER_TOKEN else '✗'} Twitter/X: {'Configured' if TWITTER_BEARER_TOKEN else 'Not configured'}")
    print(f"  {'✓' if GOOGLE_API_KEY else '✗'} Web Scraping (Reddit): {'Enabled via Gemini' if GOOGLE_API_KEY else 'Requires Gemini API'}")
    
    # Economic Data
    print("\n📊 Economic Data:")
    print(f"  {'✓' if FRED_API_KEY else '✗'} FRED (Federal Reserve): {'Configured' if FRED_API_KEY else 'Not configured'}")
    
    print("\n" + "="*60)
    
    # Warnings
    if not GOOGLE_API_KEY and not OPENAI_API_KEY:
        print("⚠️  WARNING: No LLM API configured. Using keyword-based analysis and limited social data.")
    
    if not any([FINANCIAL_MODELING_PREP_API_KEY, ALPHA_VANTAGE_API_KEY, FINNHUB_API_KEY, POLYGON_API_KEY, MARKETSTACK_API_KEY, EODHD_API_KEY]):
        print("⚠️  WARNING: No financial API configured. Using Yahoo Finance fallback and mock data.")
    
    print("="*60 + "\n")

# Log status on startup
log_api_status()

@app.route('/api/models', methods=['GET'])
def get_available_models():
    """Fetch available Gemini models from Google API"""
    if not GOOGLE_API_KEY:
        return jsonify({'error': 'Google API key not configured'}), 400
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
        
        # Get list of available models
        models = []
        for model in genai.list_models():
            # Only include generative models
            if 'generateContent' in model.supported_generation_methods:
                models.append({
                    'name': model.name.replace('models/', ''),
                    'display_name': model.display_name,
                    'description': model.description if hasattr(model, 'description') else '',
                    'input_token_limit': model.input_token_limit if hasattr(model, 'input_token_limit') else 0,
                    'output_token_limit': model.output_token_limit if hasattr(model, 'output_token_limit') else 0
                })
        
        return jsonify({
            'models': models,
            'current_model': current_model
        })
    except Exception as e:
        print(f"Error fetching models: {e}")
        # Return default models if API call fails
        return jsonify({
            'models': [
                {
                    'name': 'gemini-2.0-flash-exp',
                    'display_name': 'Gemini 2.0 Flash (Experimental)',
                    'description': 'Latest experimental model with improved performance',
                    'input_token_limit': 1000000,
                    'output_token_limit': 8192
                },
                {
                    'name': 'gemini-1.5-flash',
                    'display_name': 'Gemini 1.5 Flash',
                    'description': 'Fast and efficient model',
                    'input_token_limit': 1000000,
                    'output_token_limit': 8192
                },
                {
                    'name': 'gemini-1.5-pro',
                    'display_name': 'Gemini 1.5 Pro',
                    'description': 'Most capable model',
                    'input_token_limit': 2000000,
                    'output_token_limit': 8192
                }
            ],
            'current_model': current_model,
            'source': 'fallback'
        })

@app.route('/api/models/select', methods=['POST'])
def select_model():
    """Set the current model to use"""
    global current_model
    data = request.json
    model_name = data.get('model')
    
    if not model_name:
        return jsonify({'error': 'Model name required'}), 400
    
    current_model = model_name
    
    # Update all clients with new model
    try:
        from data_sources.llm_sentiment import LLMSentimentAnalyzer
        from data_sources.social_client import SocialClient
        from data_sources.news_client import NewsClient
        from data_sources.predictive_analysis import PredictiveAnalysis
        
        # Reinitialize with new model
        print(f"\n🔄 Switching to model: {model_name}")
        
        return jsonify({
            'success': True,
            'model': model_name,
            'message': f'Model switched to {model_name}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze/<ticker>', methods=['GET'])
def analyze_ticker(ticker):
    """Generate full analysis report for a ticker"""
    try:
        generator = ReportGenerator(model_name=current_model)
        report = generator.generate_report(ticker.upper())
        
        # Add model info
        report['model_used'] = current_model
        
        # Debug: Print headline structure
        if 'news_summary' in report and 'headlines' in report['news_summary']:
            print(f"\n[DEBUG] Headlines structure for {ticker}:")
            for i, h in enumerate(report['news_summary']['headlines'][:2], 1):
                print(f"  Headline {i}: type={type(h).__name__}")
                if isinstance(h, dict):
                    print(f"    Keys: {list(h.keys())}")
                    print(f"    URL: {h.get('url', 'N/A')}")
                else:
                    print(f"    Value: {str(h)[:50]}")
        
        return jsonify(report)
    except Exception as e:
        print(f"Error in analyze_ticker: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/deep-analyze/<ticker>', methods=['POST'])
def deep_analyze_ticker(ticker):
    """Perform deep analysis (medium or long mode)"""
    try:
        data = request.json or {}
        mode = data.get('mode', 'medium')  # medium or long
        report_data = data.get('report_data', None)
        
        if mode not in ['medium', 'long']:
            return jsonify({'error': 'Invalid mode. Use medium or long'}), 400
        
        # Perform deep analysis
        deep_analysis = deep_analyzer.analyze(
            ticker=ticker.upper(),
            mode=mode,
            report_data=report_data,
            model_name=current_model
        )
        
        return jsonify(deep_analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/watchlist', methods=['GET'])
def get_watchlist():
    """Get tickers from watchlist.txt"""
    try:
        with open('watchlist.txt', 'r') as f:
            tickers = [line.strip() for line in f if line.strip()]
        return jsonify({'tickers': tickers})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/watchlist', methods=['POST'])
def add_to_watchlist():
    """Add ticker to watchlist"""
    ticker = request.json.get('ticker', '').upper()
    if not ticker:
        return jsonify({'error': 'Ticker required'}), 400
    
    try:
        with open('watchlist.txt', 'a') as f:
            f.write(f'\n{ticker}')
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/<query>', methods=['GET'])
def search_ticker(query):
    """Search for ticker symbols and company names with fuzzy matching"""
    if not query or len(query) < 1:
        return jsonify({'results': []})
    
    query_original = query
    query = query.upper()
    results = []
    
    print(f"\n🔍 Searching for ticker: '{query}'")
    
    try:
        # Try local database FIRST with fuzzy matching
        try:
            print(f"  → Searching local database with fuzzy matching...")
            with open('ticker_database.json', 'r') as f:
                ticker_db = json.load(f)
            
            # Exact matches first
            exact_matches = []
            fuzzy_matches = []
            
            for symbol, name in ticker_db.items():
                symbol_upper = symbol.upper()
                name_upper = name.upper()
                
                # Exact match on symbol
                if query == symbol_upper:
                    exact_matches.append({
                        'symbol': symbol,
                        'name': name,
                        'exchange': 'US',
                        'type': 'stock',
                        'match_type': 'exact_symbol'
                    })
                # Exact match on company name
                elif query == name_upper:
                    exact_matches.append({
                        'symbol': symbol,
                        'name': name,
                        'exchange': 'US',
                        'type': 'stock',
                        'match_type': 'exact_name'
                    })
                # Fuzzy match - symbol starts with query
                elif symbol_upper.startswith(query):
                    fuzzy_matches.append({
                        'symbol': symbol,
                        'name': name,
                        'exchange': 'US',
                        'type': 'stock',
                        'match_type': 'symbol_prefix',
                        'score': 90
                    })
                # Fuzzy match - symbol contains query
                elif query in symbol_upper:
                    fuzzy_matches.append({
                        'symbol': symbol,
                        'name': name,
                        'exchange': 'US',
                        'type': 'stock',
                        'match_type': 'symbol_contains',
                        'score': 70
                    })
                # Fuzzy match - company name starts with query
                elif name_upper.startswith(query):
                    fuzzy_matches.append({
                        'symbol': symbol,
                        'name': name,
                        'exchange': 'US',
                        'type': 'stock',
                        'match_type': 'name_prefix',
                        'score': 85
                    })
                # Fuzzy match - company name contains query
                elif query in name_upper:
                    fuzzy_matches.append({
                        'symbol': symbol,
                        'name': name,
                        'exchange': 'US',
                        'type': 'stock',
                        'match_type': 'name_contains',
                        'score': 60
                    })
            
            # Sort fuzzy matches by score
            fuzzy_matches.sort(key=lambda x: x.get('score', 0), reverse=True)
            
            # Combine results: exact matches first, then fuzzy matches
            results = exact_matches + fuzzy_matches
            
            if results:
                print(f"  ✓ Local database returned {len(results)} results ({len(exact_matches)} exact, {len(fuzzy_matches)} fuzzy)")
                return jsonify({'results': results[:10], 'source': 'Local Database (Cached)'})
        except Exception as e:
            print(f"  ✗ Local search failed: {e}")
        
        # Fallback to Financial Modeling Prep API if not in local DB
        if FINANCIAL_MODELING_PREP_API_KEY and not results:
            try:
                print(f"  → Trying Financial Modeling Prep API...")
                url = f'https://financialmodelingprep.com/api/v3/search?query={query}&limit=10&apikey={FINANCIAL_MODELING_PREP_API_KEY}'
                response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    for item in data:
                        results.append({
                            'symbol': item.get('symbol', ''),
                            'name': item.get('name', ''),
                            'exchange': item.get('exchangeShortName', ''),
                            'type': item.get('type', 'stock')
                        })
                    
                    # Cache successful searches
                    if results:
                        _update_ticker_cache(results)
                    
                    print(f"  ✓ FMP API returned {len(results)} results")
                    return jsonify({'results': results[:10], 'source': 'Financial Modeling Prep API'})
                else:
                    print(f"  ✗ FMP returned status {response.status_code}")
            except Exception as e:
                print(f"  ✗ FMP search failed: {e}")
        else:
            if not FINANCIAL_MODELING_PREP_API_KEY and not results:
                print(f"  ⊘ Financial Modeling Prep not configured")
        
        # Try Alpha Vantage as fallback
        if ALPHA_VANTAGE_API_KEY and not results:
            try:
                print(f"  → Trying Alpha Vantage API...")
                url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={ALPHA_VANTAGE_API_KEY}'
                response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    matches = data.get('bestMatches', [])
                    for match in matches:
                        results.append({
                            'symbol': match.get('1. symbol', ''),
                            'name': match.get('2. name', ''),
                            'exchange': match.get('4. region', ''),
                            'type': match.get('3. type', 'Equity')
                        })
                    
                    # Cache successful searches
                    if results:
                        _update_ticker_cache(results)
                    
                    print(f"  ✓ Alpha Vantage API returned {len(results)} results")
                    return jsonify({'results': results[:10], 'source': 'Alpha Vantage API'})
                else:
                    print(f"  ✗ Alpha Vantage returned status {response.status_code}")
            except Exception as e:
                print(f"  ✗ Alpha Vantage search failed: {e}")
        else:
            if not ALPHA_VANTAGE_API_KEY and not results:
                print(f"  ⊘ Alpha Vantage not configured")
        
        # No results found - do web search to check if it's a private company
        if not results:
            print(f"  → No ticker found, performing web search for '{query_original}'...")
            web_info = _web_search_company(query_original)
            if web_info:
                return jsonify({
                    'results': [],
                    'source': 'web_search',
                    'web_info': web_info,
                    'message': f'No ticker found for "{query_original}"'
                })
            
            print(f"  ✗ No results found for '{query}'")
            return jsonify({'results': [], 'source': 'none', 'message': 'No matching symbols found'})
        
        return jsonify({'results': results, 'source': 'cache'})
        
    except Exception as e:
        print(f"  ✗ Search error: {e}")
        return jsonify({'results': [], 'error': str(e), 'source': 'error'})

def _web_search_company(query):
    """Search the web to find information about a company that doesn't have a ticker"""
    try:
        from openai import OpenAI
        
        if not OPENAI_API_KEY:
            return None
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Use OpenAI to search for company information
        prompt = f"""Search for information about "{query}" as a company or business. Determine:

1. Does this company exist?
2. Is it a publicly traded company or a private company?
3. If private, provide a brief 2-3 sentence description of what the company does.
4. If it doesn't exist or is not a real company, state that clearly.

Format your response as JSON:
{{
    "exists": true/false,
    "is_public": true/false,
    "is_private": true/false,
    "description": "brief description",
    "reason": "why no ticker is available"
}}"""

        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": "You are a financial research assistant. Provide factual information about companies."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.3
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Try to parse JSON response
        import json
        try:
            # Extract JSON from response
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0].strip()
            
            result = json.loads(result_text)
            print(f"  ✓ Web search found: {result.get('description', 'No info')[:100]}")
            return result
        except:
            # Fallback to text response
            return {
                'exists': True,
                'is_public': False,
                'is_private': True,
                'description': result_text[:300],
                'reason': 'Information retrieved from web search'
            }
            
    except Exception as e:
        print(f"  ✗ Web search failed: {e}")
        return None

def _update_ticker_cache(results):
    """Update local ticker database with new search results"""
    try:
        # Load existing database
        try:
            with open('ticker_database.json', 'r') as f:
                ticker_db = json.load(f)
        except:
            ticker_db = {}
        
        # Add new tickers
        updated = False
        for result in results:
            symbol = result.get('symbol', '')
            name = result.get('name', '')
            if symbol and name and symbol not in ticker_db:
                ticker_db[symbol] = name
                updated = True
        
        # Save if updated
        if updated:
            with open('ticker_database.json', 'w') as f:
                json.dump(ticker_db, f, indent=2)
            print(f"✓ Updated ticker cache with {len(results)} new entries")
    except Exception as e:
        print(f"Failed to update ticker cache: {e}")

@app.route('/api/email-report', methods=['POST'])
def email_report():
    """Send investment report via email"""
    try:
        from email_service import EmailService
        
        data = request.json
        email = data.get('email')
        report_data = data.get('report')
        
        if not email:
            return jsonify({'error': 'Email address required'}), 400
        
        if not report_data:
            return jsonify({'error': 'Report data required'}), 400
        
        # Validate email format
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return jsonify({'error': 'Invalid email address'}), 400
        
        print(f"\n📧 Email report request for {report_data.get('ticker', 'N/A')} to {email}")
        
        # Send email
        email_service = EmailService()
        result = email_service.send_report(email, report_data)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        print(f"✗ Email endpoint error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    """Subscribe to daily stock alerts"""
    try:
        data = request.json
        email = data.get('email')
        tickers = data.get('tickers', [])
        threshold = data.get('threshold', 2.0)
        
        if not email:
            return jsonify({'error': 'Email address required'}), 400
        
        if not tickers:
            return jsonify({'error': 'At least one ticker required'}), 400
        
        # Validate email format
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return jsonify({'error': 'Invalid email address'}), 400
        
        result = subscription_service.subscribe(email, tickers, threshold)
        return jsonify(result)
        
    except Exception as e:
        print(f"✗ Subscribe error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/unsubscribe', methods=['POST'])
def unsubscribe():
    """Unsubscribe from daily alerts"""
    try:
        data = request.json
        subscription_id = data.get('id')
        email = data.get('email')
        
        result = subscription_service.unsubscribe(subscription_id, email)
        return jsonify(result)
        
    except Exception as e:
        print(f"✗ Unsubscribe error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/subscription/<email>', methods=['GET'])
def get_subscription(email):
    """Get subscription details"""
    try:
        subscription = subscription_service.get_subscription(email)
        if subscription:
            return jsonify({'success': True, 'subscription': subscription})
        else:
            return jsonify({'success': False, 'message': 'No active subscription found'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-alerts', methods=['POST'])
def test_alerts():
    """Manually trigger daily alerts (for testing)"""
    try:
        scheduler = get_scheduler()
        result = scheduler.run_now()
        return jsonify(result)
    except Exception as e:
        print(f"✗ Test alerts error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Start the alert scheduler
    print("\n🚀 Starting Investment Research Platform...")
    start_scheduler(alert_time="09:00")  # Send alerts at 9 AM daily
    
    app.run(debug=True, port=5000, use_reloader=False)  # use_reloader=False to prevent double scheduler
