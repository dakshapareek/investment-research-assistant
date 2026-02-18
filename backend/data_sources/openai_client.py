"""OpenAI client for LLM operations"""
from openai import OpenAI
from config import OPENAI_API_KEY

class OpenAIClient:
    """Unified OpenAI client for all LLM operations"""
    
    def __init__(self, model='gpt-4o-mini'):
        """
        Initialize OpenAI client
        
        Args:
            model: OpenAI model to use
                - gpt-4o-mini: Fast, cheap, good quality (recommended)
                - gpt-4o: Best quality, more expensive
                - gpt-3.5-turbo: Fastest, cheapest, lower quality
        """
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model
        print(f"✓ OpenAI client initialized with model: {model}")
    
    def generate_text(self, prompt, max_tokens=2000, temperature=0.7):
        """
        Generate text completion
        
        Args:
            prompt: Text prompt
            max_tokens: Maximum tokens to generate
            temperature: Creativity (0.0-2.0, higher = more creative)
        
        Returns:
            Generated text string
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a financial analyst assistant providing accurate, data-driven insights."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"OpenAI API error: {e}")
            raise
    
    def analyze_sentiment(self, text, context=""):
        """
        Analyze sentiment of text
        
        Args:
            text: Text to analyze
            context: Additional context (e.g., "stock market", "crypto")
        
        Returns:
            dict with sentiment, score, confidence
        """
        prompt = f"""Analyze the sentiment of the following text in the context of {context if context else 'financial markets'}.

Text: {text}

Provide your analysis in JSON format:
{{
    "sentiment": "bullish/bearish/neutral",
    "score": 0.0 to 1.0 (0=very bearish, 0.5=neutral, 1=very bullish),
    "confidence": 0.0 to 1.0,
    "reasoning": "brief explanation"
}}"""

        try:
            response = self.generate_text(prompt, max_tokens=500, temperature=0.3)
            
            # Parse JSON response
            import json
            # Remove markdown code blocks if present
            if '```json' in response:
                response = response.split('```json')[1].split('```')[0].strip()
            elif '```' in response:
                response = response.split('```')[1].split('```')[0].strip()
            
            return json.loads(response)
        
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return {
                "sentiment": "neutral",
                "score": 0.5,
                "confidence": 0.0,
                "reasoning": f"Error: {str(e)}"
            }
    
    def summarize_text(self, text, max_length=200):
        """
        Summarize text
        
        Args:
            text: Text to summarize
            max_length: Maximum words in summary
        
        Returns:
            Summary string
        """
        prompt = f"""Summarize the following text in {max_length} words or less. Focus on key points and actionable insights.

Text: {text}

Summary:"""

        return self.generate_text(prompt, max_tokens=max_length * 2, temperature=0.5)
    
    def generate_forecast(self, data, ticker):
        """
        Generate price forecast analysis
        
        Args:
            data: Historical and current data dict
            ticker: Stock ticker symbol
        
        Returns:
            Forecast text
        """
        prompt = f"""As a financial analyst, provide a price forecast for {ticker} based on the following data:

Current Price: ${data.get('current_price', 'N/A')}
Recent Trend: {data.get('trend', 'N/A')}
Volatility: {data.get('volatility', 'N/A')}%
RSI: {data.get('rsi', 'N/A')}
Sentiment: {data.get('sentiment', 'N/A')}

Provide a 3-4 paragraph analysis covering:
1. Technical analysis and current market position
2. Risk factors and volatility considerations
3. Price targets for 1-week, 1-month, and 3-month horizons
4. Overall recommendation and confidence level

Be specific with numbers and realistic with projections."""

        return self.generate_text(prompt, max_tokens=1000, temperature=0.6)
