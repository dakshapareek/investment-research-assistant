import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import GMAIL_EMAIL, GMAIL_APP_PASSWORD

class EmailService:
    """Send investment reports via Gmail"""
    
    def __init__(self):
        self.gmail_email = GMAIL_EMAIL
        self.gmail_password = GMAIL_APP_PASSWORD
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_report(self, to_email, report_data):
        """Send investment report via email"""
        try:
            if not self.gmail_email or not self.gmail_password:
                return {
                    'success': False,
                    'error': 'Gmail credentials not configured. Add GMAIL_EMAIL and GMAIL_APP_PASSWORD to .env file.'
                }
            
            # Create email
            msg = MIMEMultipart('alternative')
            msg['From'] = self.gmail_email
            msg['To'] = to_email
            msg['Subject'] = f"Investment Report: {report_data.get('ticker', 'Stock')} - {datetime.now().strftime('%B %d, %Y')}"
            
            # Create HTML email body
            html_body = self._create_html_report(report_data)
            
            # Attach HTML
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Send email
            print(f"Sending email to {to_email}...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.gmail_email, self.gmail_password)
                server.send_message(msg)
            
            print(f"✓ Email sent successfully to {to_email}")
            return {
                'success': True,
                'message': f'Report sent to {to_email}'
            }
            
        except Exception as e:
            print(f"✗ Email sending failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_html_report(self, report):
        """Create HTML formatted email report"""
        ticker = report.get('ticker', 'N/A')
        quote = report.get('quote', {})
        exec_summary = report.get('executive_summary', {})
        predictions = report.get('predictions', {})
        sentiment = report.get('combined_sentiment', {})
        social = report.get('social_pulse', {})
        news = report.get('news_summary', {})
        
        # Price info
        price = quote.get('price', 0)
        change = quote.get('change', 0)
        change_pct = quote.get('changePercent', 0)
        is_positive = change >= 0
        
        # Rating
        rating = exec_summary.get('rating', 'N/A')
        recommendation = exec_summary.get('recommendation', 'N/A')
        
        # Predictions
        tech_analysis = predictions.get('technical_analysis', {}) if predictions else {}
        scenarios = predictions.get('predictions', {}).get('scenarios', []) if predictions else []
        
        # Sentiment
        overall_sentiment = sentiment.get('overall_sentiment', 'neutral')
        sentiment_score = sentiment.get('average_score', 0)
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .header {{
            border-bottom: 3px solid #007AFF;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .ticker {{
            font-size: 32px;
            font-weight: 700;
            color: #000;
            margin-bottom: 10px;
        }}
        .price {{
            font-size: 48px;
            font-weight: 700;
            color: #000;
            margin: 10px 0;
        }}
        .change {{
            font-size: 24px;
            font-weight: 600;
            padding: 8px 16px;
            border-radius: 8px;
            display: inline-block;
        }}
        .change.positive {{
            color: #34C759;
            background: rgba(52, 199, 89, 0.1);
        }}
        .change.negative {{
            color: #FF3B30;
            background: rgba(255, 59, 48, 0.1);
        }}
        .rating {{
            display: inline-block;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 700;
            color: white;
            margin: 20px 0;
        }}
        .rating.bull {{
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        }}
        .rating.bear {{
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        }}
        .rating.neutral {{
            background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
        }}
        .section {{
            margin: 30px 0;
            padding: 20px;
            background: #f9fafb;
            border-radius: 8px;
            border-left: 4px solid #007AFF;
        }}
        .section-title {{
            font-size: 20px;
            font-weight: 700;
            color: #000;
            margin-bottom: 15px;
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin: 15px 0;
        }}
        .metric {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e5e7eb;
        }}
        .metric-label {{
            font-size: 12px;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}
        .metric-value {{
            font-size: 20px;
            font-weight: 700;
            color: #000;
        }}
        .forecast-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        .forecast-table th {{
            background: #007AFF;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        .forecast-table td {{
            padding: 12px;
            border-bottom: 1px solid #e5e7eb;
        }}
        .forecast-table tr:hover {{
            background: #f9fafb;
        }}
        .sentiment-badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 14px;
        }}
        .sentiment-badge.bullish {{
            background: rgba(52, 199, 89, 0.2);
            color: #10b981;
        }}
        .sentiment-badge.bearish {{
            background: rgba(239, 68, 68, 0.2);
            color: #ef4444;
        }}
        .sentiment-badge.neutral {{
            background: rgba(107, 114, 128, 0.2);
            color: #6b7280;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            text-align: center;
            color: #6b7280;
            font-size: 14px;
        }}
        .disclaimer {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            color: #856404;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="ticker">{ticker}</div>
            <div class="price">${price:.2f}</div>
            <div class="change {'positive' if is_positive else 'negative'}">
                {'▲' if is_positive else '▼'} ${abs(change):.2f} ({abs(change_pct):.2f}%)
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">📊 Executive Summary</div>
            <div class="rating {'bull' if 'Bull' in rating else 'bear' if 'Bear' in rating else 'neutral'}">
                {rating}
            </div>
            <p style="margin-top: 15px; font-size: 16px; line-height: 1.8;">{recommendation}</p>
        </div>
"""
        
        # Add predictions if available
        if scenarios:
            html += f"""
        <div class="section">
            <div class="section-title">🔮 AI Price Forecast</div>
            <div class="metric-grid">
                <div class="metric">
                    <div class="metric-label">20-Day Trend</div>
                    <div class="metric-value" style="color: {'#34C759' if tech_analysis.get('trend_direction') == 'bullish' else '#FF3B30'}">
                        {tech_analysis.get('trend_direction', 'N/A').upper()}
                    </div>
                </div>
                <div class="metric">
                    <div class="metric-label">RSI (14-day)</div>
                    <div class="metric-value">{tech_analysis.get('rsi', 0):.1f}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Volatility</div>
                    <div class="metric-value">{tech_analysis.get('volatility', 0):.1f}%</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Confidence</div>
                    <div class="metric-value">{predictions.get('confidence_level', 0)}%</div>
                </div>
            </div>
            
            <table class="forecast-table">
                <thead>
                    <tr>
                        <th>Timeframe</th>
                        <th>Bull Case</th>
                        <th>Base Case</th>
                        <th>Bear Case</th>
                    </tr>
                </thead>
                <tbody>
"""
            for scenario in scenarios[:4]:  # Show first 4 scenarios
                html += f"""
                    <tr>
                        <td><strong>{scenario.get('horizon', 'N/A')}</strong></td>
                        <td style="color: #34C759;">${scenario.get('bull_case', 0):.2f} (+{scenario.get('bull_return', 0):.1f}%)</td>
                        <td>${scenario.get('base_case', 0):.2f} ({scenario.get('base_return', 0):+.1f}%)</td>
                        <td style="color: #FF3B30;">${scenario.get('bear_case', 0):.2f} ({scenario.get('bear_return', 0):.1f}%)</td>
                    </tr>
"""
            html += """
                </tbody>
            </table>
        </div>
"""
        
        # Add sentiment
        html += f"""
        <div class="section">
            <div class="section-title">💭 Market Sentiment</div>
            <div style="margin: 15px 0;">
                <span class="sentiment-badge {overall_sentiment}">{overall_sentiment.upper()}</span>
                <span style="margin-left: 15px; font-size: 18px; font-weight: 600;">
                    Score: {sentiment_score:.2f}
                </span>
            </div>
        </div>
"""
        
        # Add news summary
        if news.get('summary'):
            html += f"""
        <div class="section">
            <div class="section-title">📰 News Summary</div>
            <p style="font-size: 15px; line-height: 1.8;">{news.get('summary', 'N/A')}</p>
        </div>
"""
        
        # Add disclaimer and footer
        html += f"""
        <div class="disclaimer">
            <strong>⚠️ Disclaimer:</strong> This report is for informational purposes only and should not be considered financial advice. 
            Always conduct your own research and consult with a qualified financial advisor before making investment decisions.
        </div>
        
        <div class="footer">
            <p>Generated by Investment Research Platform</p>
            <p>{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html

