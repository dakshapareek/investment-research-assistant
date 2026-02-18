"""
Subscription Service for Daily Stock Alerts
Manages email subscriptions and sends automated daily reports
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import uuid
from email_service import EmailService
from data_sources.multi_api_client import MultiAPIStockClient

class SubscriptionService:
    """Manage stock alert subscriptions"""
    
    def __init__(self, db_path='subscriptions.json'):
        self.db_path = db_path
        self.email_service = EmailService()
        self.stock_client = MultiAPIStockClient()
        self._load_subscriptions()
    
    def _load_subscriptions(self):
        """Load subscriptions from JSON file"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r') as f:
                    self.subscriptions = json.load(f)
            except Exception as e:
                print(f"Error loading subscriptions: {e}")
                self.subscriptions = []
        else:
            self.subscriptions = []
    
    def _save_subscriptions(self):
        """Save subscriptions to JSON file"""
        try:
            with open(self.db_path, 'w') as f:
                json.dump(self.subscriptions, f, indent=2)
        except Exception as e:
            print(f"Error saving subscriptions: {e}")
    
    def subscribe(self, email: str, tickers: List[str], threshold: float = 2.0) -> Dict:
        """
        Subscribe to daily stock alerts
        
        Args:
            email: Email address to send alerts to
            tickers: List of stock tickers to monitor
            threshold: Price change threshold (%) to trigger alert (default 2%)
        
        Returns:
            Dict with subscription details and unsubscribe token
        """
        # Check if email already subscribed
        existing = self._find_subscription(email)
        if existing:
            # Update existing subscription
            existing['tickers'] = list(set(existing['tickers'] + tickers))
            existing['threshold'] = threshold
            existing['updated_at'] = datetime.now().isoformat()
            self._save_subscriptions()
            
            return {
                'success': True,
                'message': 'Subscription updated',
                'subscription': existing
            }
        
        # Create new subscription
        subscription = {
            'id': str(uuid.uuid4()),
            'email': email,
            'tickers': tickers,
            'threshold': threshold,
            'active': True,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'last_sent': None
        }
        
        self.subscriptions.append(subscription)
        self._save_subscriptions()
        
        return {
            'success': True,
            'message': 'Subscription created',
            'subscription': subscription
        }
    
    def unsubscribe(self, subscription_id: str = None, email: str = None) -> Dict:
        """
        Unsubscribe from daily alerts
        
        Args:
            subscription_id: Subscription ID (from email link)
            email: Email address (alternative to ID)
        
        Returns:
            Dict with success status
        """
        if subscription_id:
            subscription = self._find_subscription_by_id(subscription_id)
        elif email:
            subscription = self._find_subscription(email)
        else:
            return {'success': False, 'error': 'Subscription ID or email required'}
        
        if not subscription:
            return {'success': False, 'error': 'Subscription not found'}
        
        subscription['active'] = False
        subscription['updated_at'] = datetime.now().isoformat()
        self._save_subscriptions()
        
        return {
            'success': True,
            'message': 'Successfully unsubscribed',
            'email': subscription['email']
        }
    
    def get_subscription(self, email: str) -> Optional[Dict]:
        """Get subscription details for an email"""
        return self._find_subscription(email)
    
    def _find_subscription(self, email: str) -> Optional[Dict]:
        """Find subscription by email"""
        for sub in self.subscriptions:
            if sub['email'] == email and sub['active']:
                return sub
        return None
    
    def _find_subscription_by_id(self, sub_id: str) -> Optional[Dict]:
        """Find subscription by ID"""
        for sub in self.subscriptions:
            if sub['id'] == sub_id:
                return sub
        return None
    
    def send_daily_alerts(self) -> Dict:
        """
        Send daily alerts to all active subscriptions
        Called by scheduler
        
        Returns:
            Dict with summary of alerts sent
        """
        print(f"\n{'='*60}")
        print(f"DAILY STOCK ALERTS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        active_subs = [s for s in self.subscriptions if s['active']]
        print(f"Active subscriptions: {len(active_subs)}")
        
        if not active_subs:
            print("No active subscriptions")
            return {'success': True, 'sent': 0, 'failed': 0}
        
        sent = 0
        failed = 0
        
        for subscription in active_subs:
            try:
                # Check if already sent today
                if self._sent_today(subscription):
                    print(f"  ⊘ {subscription['email']}: Already sent today")
                    continue
                
                print(f"\n  → Processing {subscription['email']}...")
                
                # Get stock data for all tickers
                alerts = []
                for ticker in subscription['tickers']:
                    try:
                        quote = self.stock_client.get_quote(ticker)
                        if quote and quote.get('price'):
                            change_pct = abs(quote.get('changePercent', 0))
                            
                            # Check if change exceeds threshold
                            if change_pct >= subscription['threshold']:
                                alerts.append({
                                    'ticker': ticker,
                                    'price': quote['price'],
                                    'change': quote.get('change', 0),
                                    'changePercent': quote.get('changePercent', 0),
                                    'volume': quote.get('volume', 0),
                                    'source': quote.get('source', 'Unknown')
                                })
                                print(f"    ✓ {ticker}: {change_pct:.2f}% change (threshold: {subscription['threshold']}%)")
                    except Exception as e:
                        print(f"    ✗ {ticker}: Error fetching data - {e}")
                
                # Send email if there are alerts
                if alerts:
                    result = self._send_alert_email(subscription, alerts)
                    if result['success']:
                        subscription['last_sent'] = datetime.now().isoformat()
                        self._save_subscriptions()
                        sent += 1
                        print(f"    ✓ Email sent with {len(alerts)} alerts")
                    else:
                        failed += 1
                        print(f"    ✗ Email failed: {result.get('error')}")
                else:
                    print(f"    ⊘ No significant changes (threshold: {subscription['threshold']}%)")
                
            except Exception as e:
                print(f"  ✗ {subscription['email']}: Error - {e}")
                failed += 1
        
        print(f"\n{'='*60}")
        print(f"Summary: {sent} sent, {failed} failed")
        print(f"{'='*60}\n")
        
        return {'success': True, 'sent': sent, 'failed': failed}
    
    def _sent_today(self, subscription: Dict) -> bool:
        """Check if alert was already sent today"""
        if not subscription.get('last_sent'):
            return False
        
        last_sent = datetime.fromisoformat(subscription['last_sent'])
        today = datetime.now().date()
        
        return last_sent.date() == today
    
    def _send_alert_email(self, subscription: Dict, alerts: List[Dict]) -> Dict:
        """Send alert email with stock changes"""
        email = subscription['email']
        threshold = subscription['threshold']
        
        # Create HTML email
        html = self._create_alert_html(alerts, threshold, subscription['id'])
        
        # Send via email service
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        import smtplib
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_service.gmail_email
            msg['To'] = email
            msg['Subject'] = f"🚨 Daily Stock Alert - {len(alerts)} stocks moved >{threshold}%"
            
            html_part = MIMEText(html, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.email_service.smtp_server, self.email_service.smtp_port) as server:
                server.starttls()
                server.login(self.email_service.gmail_email, self.email_service.gmail_password)
                server.send_message(msg)
            
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _create_alert_html(self, alerts: List[Dict], threshold: float, sub_id: str) -> str:
        """Create HTML email for alerts"""
        
        # Sort by absolute change percentage
        alerts.sort(key=lambda x: abs(x['changePercent']), reverse=True)
        
        # Create alert rows
        alert_rows = ""
        for alert in alerts:
            is_positive = alert['changePercent'] >= 0
            color = '#34C759' if is_positive else '#FF3B30'
            arrow = '▲' if is_positive else '▼'
            
            alert_rows += f"""
                <tr>
                    <td style="padding: 15px; border-bottom: 1px solid #e5e7eb;">
                        <strong style="font-size: 18px;">{alert['ticker']}</strong>
                    </td>
                    <td style="padding: 15px; border-bottom: 1px solid #e5e7eb; font-size: 20px; font-weight: 700;">
                        ${alert['price']:.2f}
                    </td>
                    <td style="padding: 15px; border-bottom: 1px solid #e5e7eb; color: {color}; font-size: 18px; font-weight: 700;">
                        {arrow} ${abs(alert['change']):.2f}
                    </td>
                    <td style="padding: 15px; border-bottom: 1px solid #e5e7eb; color: {color}; font-size: 18px; font-weight: 700;">
                        {alert['changePercent']:+.2f}%
                    </td>
                </tr>
            """
        
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px 12px 0 0;
            margin: -30px -30px 30px -30px;
        }}
        .title {{
            font-size: 28px;
            font-weight: 700;
            margin: 0 0 10px 0;
        }}
        .subtitle {{
            font-size: 16px;
            opacity: 0.9;
            margin: 0;
        }}
        .alert-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .alert-table th {{
            background: #f9fafb;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #6b7280;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.5px;
        }}
        .unsubscribe {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            text-align: center;
            color: #6b7280;
            font-size: 14px;
        }}
        .unsubscribe a {{
            color: #007AFF;
            text-decoration: none;
        }}
        .footer {{
            margin-top: 20px;
            text-align: center;
            color: #9ca3af;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">🚨 Daily Stock Alert</div>
            <div class="subtitle">{datetime.now().strftime('%B %d, %Y')}</div>
        </div>
        
        <p style="font-size: 16px; margin-bottom: 20px;">
            The following stocks in your watchlist have moved more than <strong>{threshold}%</strong> today:
        </p>
        
        <table class="alert-table">
            <thead>
                <tr>
                    <th>Ticker</th>
                    <th>Price</th>
                    <th>Change ($)</th>
                    <th>Change (%)</th>
                </tr>
            </thead>
            <tbody>
                {alert_rows}
            </tbody>
        </table>
        
        <div style="background: #f0f9ff; border-left: 4px solid #0ea5e9; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <strong>💡 Tip:</strong> Log in to your Investment Research Platform for detailed analysis and predictions.
        </div>
        
        <div class="unsubscribe">
            <p>You're receiving this because you subscribed to daily stock alerts.</p>
            <p><a href="http://localhost:3000/unsubscribe?id={sub_id}">Unsubscribe from these alerts</a></p>
        </div>
        
        <div class="footer">
            <p>Investment Research Platform</p>
            <p>This is an automated alert. Please do not reply to this email.</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html
