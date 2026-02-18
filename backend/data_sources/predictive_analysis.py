import numpy as np
from datetime import datetime, timedelta
from config import GOOGLE_API_KEY, OPENAI_API_KEY

class PredictiveAnalysis:
    """AI-powered predictive analysis for stock prices"""
    
    def __init__(self, model_name='gpt-4o-mini'):
        self.llm_available = False
        self.model_name = model_name
        self.llm_type = None
        
        # Try OpenAI first
        if OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=OPENAI_API_KEY)
                self.llm_available = True
                self.llm_type = 'OpenAI'
                print(f"✓ OpenAI ({model_name}) initialized for predictive analysis")
            except Exception as e:
                print(f"✗ OpenAI initialization failed: {e}")
        
        # Fallback to Gemini
        if not self.llm_available and GOOGLE_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=GOOGLE_API_KEY)
                self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
                self.llm_available = True
                self.llm_type = 'Gemini'
                print(f"✓ Google Gemini initialized for predictive analysis (OpenAI not available)")
            except Exception as e:
                print(f"✗ Gemini initialization failed: {e}")
    
    def _generate_content(self, prompt, max_tokens=1000):
        """Unified method to generate content"""
        try:
            if self.llm_type == 'OpenAI':
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a financial analyst providing price forecasts."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=0.6
                )
                return response.choices[0].message.content.strip()
            elif self.llm_type == 'Gemini':
                response = self.model.generate_content(prompt)
                return response.text.strip()
        except Exception as e:
            print(f"LLM generation error: {e}")
            raise
    
    def generate_forecast(self, ticker, historical_data, quote, sentiment_data, news_data):
        """Generate price forecast with multiple scenarios"""
        
        # Calculate technical indicators
        technical_analysis = self._calculate_technical_indicators(historical_data)
        
        # Generate price predictions
        predictions = self._generate_predictions(historical_data, technical_analysis)
        
        # Get LLM analysis if available
        llm_forecast = None
        if self.llm_available:
            llm_forecast = self._generate_llm_forecast(
                ticker, historical_data, quote, sentiment_data, 
                news_data, technical_analysis
            )
        
        return {
            'predictions': predictions,
            'technical_analysis': technical_analysis,
            'llm_forecast': llm_forecast,
            'confidence_level': self._calculate_confidence(technical_analysis, sentiment_data)
        }
    
    def _calculate_technical_indicators(self, historical_data):
        """Calculate technical indicators for analysis"""
        closes = np.array([p for p in historical_data.get('close', []) if p is not None])
        
        if len(closes) < 50:
            return {}
        
        # Moving averages
        sma_20 = np.mean(closes[-20:])
        sma_50 = np.mean(closes[-50:])
        sma_200 = np.mean(closes[-200:]) if len(closes) >= 200 else np.mean(closes)
        
        # Trend
        recent_trend = (closes[-1] - closes[-20]) / closes[-20] * 100
        medium_trend = (closes[-1] - closes[-50]) / closes[-50] * 100
        
        # Volatility
        returns = np.diff(closes) / closes[:-1]
        volatility = np.std(returns) * np.sqrt(252) * 100  # Annualized
        
        # RSI (Relative Strength Index)
        rsi = self._calculate_rsi(closes)
        
        # Support and Resistance
        support = np.min(closes[-60:])
        resistance = np.max(closes[-60:])
        
        return {
            'current_price': float(closes[-1]),
            'sma_20': float(sma_20),
            'sma_50': float(sma_50),
            'sma_200': float(sma_200),
            'recent_trend': float(recent_trend),
            'recent_trend_label': 'Strong Bullish' if recent_trend > 5 else 'Bullish' if recent_trend > 0 else 'Strong Bearish' if recent_trend < -5 else 'Bearish',
            'medium_trend': float(medium_trend),
            'volatility': float(volatility),
            'rsi': float(rsi),
            'support': float(support),
            'resistance': float(resistance),
            'trend_direction': 'bullish' if recent_trend > 0 else 'bearish',
            'trend_strength': 'strong' if abs(recent_trend) > 5 else 'moderate' if abs(recent_trend) > 2 else 'weak'
        }
    
    def _calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index"""
        if len(prices) < period + 1:
            return 50.0
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def _generate_predictions(self, historical_data, technical_analysis):
        """Generate price predictions starting from CURRENT PRICE with accurate returns"""
        current_price = technical_analysis.get('current_price', 100)
        volatility = technical_analysis.get('volatility', 20) / 100  # Annual volatility as decimal
        recent_trend = technical_analysis.get('recent_trend', 0) / 100  # 20-day trend as decimal
        
        print(f"  → Generating predictions from current price: ${current_price:.2f}")
        print(f"  → Recent 20-day trend: {recent_trend*100:.2f}%")
        print(f"  → Annual volatility: {volatility*100:.1f}%")
        
        # Time horizons (days)
        horizons = [7, 30, 90, 180]
        
        predictions = []
        
        for days in horizons:
            # Calculate expected return based on historical trend
            # Annualize the 20-day trend
            if recent_trend != 0:
                annualized_trend = recent_trend * (252 / 20)
            else:
                annualized_trend = 0
            
            # Time factor (fraction of year)
            time_factor = days / 252
            
            # Expected return from trend
            trend_return = annualized_trend * time_factor
            
            # Volatility-based range
            vol_range = volatility * np.sqrt(time_factor)
            
            # Bull case: Trend + 1 standard deviation
            bull_return = trend_return + vol_range
            bull_price = current_price * (1 + bull_return)
            
            # Base case: Just the trend (most likely scenario)
            base_return = trend_return
            base_price = current_price * (1 + base_return)
            
            # Bear case: Trend - 1 standard deviation
            bear_return = trend_return - vol_range
            bear_price = current_price * (1 + bear_return)
            
            # Apply reasonable caps to prevent extreme predictions
            max_gain = 0.5 if days <= 30 else (1.0 if days <= 90 else 1.5)  # 50%, 100%, 150%
            max_loss = -0.3 if days <= 30 else (-0.5 if days <= 90 else -0.7)  # -30%, -50%, -70%
            
            bull_return = min(bull_return, max_gain)
            base_return = max(min(base_return, max_gain * 0.6), max_loss * 0.6)
            bear_return = max(bear_return, max_loss)
            
            # Recalculate prices from capped returns
            bull_price = current_price * (1 + bull_return)
            base_price = current_price * (1 + base_return)
            bear_price = current_price * (1 + bear_return)
            
            predictions.append({
                'horizon': f'{days}d',
                'horizon_days': days,
                'current_price': round(current_price, 2),
                'bull_case': round(bull_price, 2),
                'base_case': round(base_price, 2),
                'bear_case': round(bear_price, 2),
                'bull_return': round(bull_return * 100, 2),
                'base_return': round(base_return * 100, 2),
                'bear_return': round(bear_return * 100, 2)
            })
            
            print(f"  → {days}d forecast: ${bear_price:.2f} ({bear_return*100:+.1f}%) to ${bull_price:.2f} ({bull_return*100:+.1f}%)")
        
        # Generate daily predictions for chart
        daily_predictions = self._generate_daily_predictions(
            current_price, annualized_trend, volatility, 90
        )
        
        return {
            'scenarios': predictions,
            'daily_forecast': daily_predictions,
            'current_price': current_price
        }
    
    def _generate_daily_predictions(self, current_price, annualized_trend, volatility, days):
        """Generate daily price predictions starting from CURRENT PRICE"""
        predictions = []
        
        for day in range(1, days + 1):
            # Time factor
            time_factor = day / 252
            
            # Expected return from trend
            trend_return = annualized_trend * time_factor
            
            # Base case prediction (most likely)
            predicted_price = current_price * (1 + trend_return)
            
            # Confidence interval (95% confidence = 1.96 std deviations)
            vol_range = volatility * np.sqrt(time_factor) * 1.96
            upper_bound = current_price * (1 + trend_return + vol_range)
            lower_bound = current_price * (1 + trend_return - vol_range)
            
            # Apply reasonable caps
            max_gain = 1.5  # 150% max for 90 days
            max_loss = -0.7  # -70% max loss
            
            upper_bound = min(upper_bound, current_price * (1 + max_gain))
            lower_bound = max(lower_bound, current_price * (1 + max_loss))
            predicted_price = max(lower_bound, min(predicted_price, upper_bound))
            
            predictions.append({
                'day': day,
                'date': (datetime.now() + timedelta(days=day)).strftime('%Y-%m-%d'),
                'predicted_price': round(predicted_price, 2),
                'upper_bound': round(upper_bound, 2),
                'lower_bound': round(lower_bound, 2),
                'return_pct': round(((predicted_price / current_price) - 1) * 100, 2)
            })
        
        return predictions
    
    def _generate_llm_forecast(self, ticker, historical_data, quote, sentiment_data, news_data, technical_analysis):
        """Generate AI-powered forecast analysis - GROUNDED IN DATA, NO HALLUCINATION"""
        try:
            # Prepare context with ACTUAL data
            current_price = quote.get('price', 0)
            change_percent = quote.get('changePercent', 0)
            sentiment = sentiment_data.get('overall_sentiment', 'neutral')
            rsi = technical_analysis.get('rsi', 50)
            trend = technical_analysis.get('recent_trend', 0)
            volatility = technical_analysis.get('volatility', 0)
            
            prompt = f"""As a financial analyst, provide a realistic price forecast for {ticker} based ONLY on the following ACTUAL data. DO NOT make up numbers or hallucinate.

ACTUAL CURRENT DATA:
- Current Price: ${current_price:.2f}
- Today's Change: {change_percent:+.2f}%
- 20-day Trend: {trend:+.2f}%
- RSI (14-day): {rsi:.1f}
- Volatility (Annual): {volatility:.1f}%
- Market Sentiment: {sentiment}
- Support Level: ${technical_analysis.get('support', 0):.2f}
- Resistance Level: ${technical_analysis.get('resistance', 0):.2f}

INSTRUCTIONS:
1. Base your analysis ONLY on the data provided above
2. DO NOT invent price targets or percentages
3. Use the actual trend ({trend:+.2f}%) and volatility ({volatility:.1f}%) in your analysis
4. Be realistic - stocks don't typically move more than 20-30% in a few months
5. Acknowledge uncertainty and market risks

Provide a 3-paragraph forecast covering:
1. Technical outlook based on ACTUAL indicators (RSI, trend, support/resistance)
2. Sentiment and market positioning based on ACTUAL sentiment data
3. Realistic expectations for the next 1-3 months based on ACTUAL volatility and trend

Write in professional analyst tone. Be conservative and realistic."""

            forecast_text = self._generate_content(prompt, max_tokens=1000)
            
            # Validate the forecast doesn't contain unrealistic claims
            if any(word in forecast_text.lower() for word in ['100%', '200%', '500%', 'guaranteed', 'definitely']):
                print(f"  ⚠️  LLM forecast contained unrealistic claims, using fallback")
                return self._generate_fallback_forecast(technical_analysis, sentiment_data)
            
            return forecast_text
            
        except Exception as e:
            print(f"LLM forecast generation error: {e}")
            return self._generate_fallback_forecast(technical_analysis, sentiment_data)
    
    def _generate_fallback_forecast(self, technical_analysis, sentiment_data):
        """Generate fallback forecast without LLM"""
        current_price = technical_analysis.get('current_price', 0)
        trend = technical_analysis.get('trend_direction', 'neutral')
        rsi = technical_analysis.get('rsi', 50)
        
        forecast = f"Technical analysis suggests a {trend} outlook. "
        
        if rsi > 70:
            forecast += "RSI indicates overbought conditions, suggesting potential pullback. "
        elif rsi < 30:
            forecast += "RSI indicates oversold conditions, suggesting potential bounce. "
        else:
            forecast += "RSI is in neutral territory. "
        
        forecast += f"Key support at ${technical_analysis.get('support', 0):.2f} "
        forecast += f"and resistance at ${technical_analysis.get('resistance', 0):.2f}. "
        
        if trend == 'bullish':
            forecast += "Uptrend suggests continued strength if support holds. "
        else:
            forecast += "Downtrend suggests caution until trend reversal confirmed. "
        
        return forecast
    
    def _calculate_confidence(self, technical_analysis, sentiment_data):
        """Calculate confidence level for predictions"""
        confidence = 50  # Base confidence
        
        # Technical factors
        rsi = technical_analysis.get('rsi', 50)
        if 30 < rsi < 70:
            confidence += 10  # Neutral RSI is good
        
        trend = technical_analysis.get('recent_trend', 0)
        if abs(trend) > 5:
            confidence += 10  # Strong trend
        
        # Sentiment factors
        sentiment = sentiment_data.get('overall_sentiment', 'neutral')
        if sentiment in ['bullish', 'bearish']:
            confidence += 10  # Clear sentiment
        
        sentiment_confidence = sentiment_data.get('confidence', 0)
        confidence += sentiment_confidence * 20
        
        return min(confidence, 95)  # Cap at 95%
