import os
from dotenv import load_dotenv
from pathlib import Path

# Get the directory where this config file is located
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / '.env'

# Load .env file with override to ensure fresh values
load_dotenv(ENV_FILE, override=True)

# LLM APIs
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash-lite')  # Gemini 2.5 Flash Lite
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

# Financial APIs
FINANCIAL_MODELING_PREP_API_KEY = os.getenv('FINANCIAL_MODELING_PREP_API_KEY', '')
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '')
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY', '')
POLYGON_API_KEY = os.getenv('POLYGON_API_KEY', '')
MARKETSTACK_API_KEY = os.getenv('MARKETSTACK_API_KEY', '')
EODHD_API_KEY = os.getenv('EODHD_API_KEY', '')

# News APIs
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
BENZINGA_API_KEY = os.getenv('BENZINGA_API_KEY', '')

# Social Media APIs
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', '')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY', '')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET', '')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'InvestmentResearch/1.0')

# Government Data APIs
BLS_API_KEY = os.getenv('BLS_API_KEY', '')
FRED_API_KEY = os.getenv('FRED_API_KEY', '')

# Email Configuration
GMAIL_EMAIL = os.getenv('GMAIL_EMAIL', '')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD', '')

# MCP Configuration
USE_MCP_FOR_FINANCIAL_DATA = os.getenv('USE_MCP_FOR_FINANCIAL_DATA', 'true').lower() == 'true'
MCP_SERVER_COMMAND = os.getenv('MCP_SERVER_COMMAND', 'python')
MCP_SERVER_ARGS = os.getenv('MCP_SERVER_ARGS', '-m,uv,tool,run,mcp-server-fetch').split(',')

# Output
OUTPUT_DIR = 'reports'
