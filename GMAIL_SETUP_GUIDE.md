# Gmail Email Setup Guide

## Overview
Send investment reports directly to email addresses using Gmail SMTP. Reports are beautifully formatted in HTML with all analysis, predictions, and recommendations.

## Features
- 📧 Send reports via email with one click
- 🎨 Professional HTML formatting
- 📊 Includes all analysis sections
- 🔒 Secure Gmail App Password authentication
- ✅ Email validation
- 📱 Mobile-friendly emails

## Setup Instructions

### Step 1: Enable 2-Factor Authentication on Gmail
Gmail App Passwords require 2-factor authentication to be enabled.

1. Go to your Google Account: https://myaccount.google.com/
2. Click "Security" in the left sidebar
3. Under "Signing in to Google", click "2-Step Verification"
4. Follow the prompts to enable 2-factor authentication
5. Verify with your phone number

### Step 2: Generate Gmail App Password

1. Go to: https://myaccount.google.com/apppasswords
   - Or navigate: Google Account → Security → 2-Step Verification → App passwords

2. You may need to sign in again

3. Under "Select app", choose "Mail"

4. Under "Select device", choose "Other (Custom name)"

5. Enter a name like "Investment Research App"

6. Click "Generate"

7. Google will display a 16-character password like: `abcd efgh ijkl mnop`

8. **Copy this password immediately** - you won't be able to see it again!

### Step 3: Configure Backend

1. Open `backend/.env` file

2. Add your Gmail credentials:
```env
# Email Configuration (Gmail)
GMAIL_EMAIL=your_email@gmail.com
GMAIL_APP_PASSWORD=abcdefghijklmnop
```

**Important Notes:**
- Use your full Gmail address (e.g., `john.doe@gmail.com`)
- Remove spaces from the app password (use `abcdefghijklmnop`, not `abcd efgh ijkl mnop`)
- This is NOT your regular Gmail password
- Keep this password secure and never commit it to version control

### Step 4: Restart Backend

```bash
cd backend
python app.py
```

You should see:
```
📧 Email Service: Configured
```

### Step 5: Test Email Functionality

1. Analyze any stock (e.g., AAPL)
2. Click the "📧 Email Report" button
3. Enter your email address
4. Click "Send Email"
5. Check your inbox (and spam folder)

## Email Content

### What's Included in the Email

1. **Header Section**
   - Stock ticker symbol
   - Current price
   - Price change (with color coding)

2. **Executive Summary**
   - Investment rating (Bull/Bear/Neutral)
   - Recommendation text

3. **AI Price Forecast**
   - Technical indicators (Trend, RSI, Volatility)
   - Confidence level
   - Price targets table (7d, 30d, 90d, 180d)
   - Bull/Base/Bear scenarios

4. **Market Sentiment**
   - Overall sentiment (Bullish/Bearish/Neutral)
   - Sentiment score

5. **News Summary**
   - Latest news analysis

6. **Disclaimer**
   - Investment disclaimer
   - Timestamp

### Email Example

```
Subject: Investment Report: AAPL - February 15, 2026

┌─────────────────────────────────────┐
│ AAPL                                │
│ $175.43                             │
│ ▲ $2.15 (1.24%)                     │
├─────────────────────────────────────┤
│ Executive Summary                   │
│ [Strong Bull]                       │
│ High conviction BUY - favorable...  │
├─────────────────────────────────────┤
│ AI Price Forecast                   │
│ Trend: BULLISH | RSI: 65.3         │
│                                     │
│ 7d:  $178.50 (+1.8%)               │
│ 30d: $185.20 (+5.6%)               │
│ 90d: $195.80 (+11.6%)              │
└─────────────────────────────────────┘
```

## Troubleshooting

### Error: "Gmail credentials not configured"

**Solution:**
- Check that `GMAIL_EMAIL` and `GMAIL_APP_PASSWORD` are set in `.env`
- Restart the backend server
- Verify no typos in the credentials

### Error: "Authentication failed"

**Possible Causes:**
1. App password is incorrect
2. 2-factor authentication not enabled
3. Spaces in the app password

**Solution:**
- Generate a new app password
- Remove all spaces from the password
- Ensure 2FA is enabled on your Google account

### Error: "SMTP connection failed"

**Possible Causes:**
1. Firewall blocking port 587
2. Network issues
3. Gmail SMTP temporarily unavailable

**Solution:**
- Check your internet connection
- Try again in a few minutes
- Check if port 587 is open

### Emails Going to Spam

**Solution:**
1. Mark the email as "Not Spam"
2. Add the sender to your contacts
3. Create a filter to always inbox these emails

### Error: "Invalid email address"

**Solution:**
- Check email format (must be valid email)
- Remove extra spaces
- Use a proper email domain

## Security Best Practices

### 1. Use App Passwords (Not Regular Password)
✓ App passwords are more secure
✓ Can be revoked without changing main password
✗ Never use your regular Gmail password

### 2. Keep Credentials Secure
✓ Add `.env` to `.gitignore`
✓ Never commit credentials to version control
✓ Use environment variables in production

### 3. Revoke Unused App Passwords
- Go to: https://myaccount.google.com/apppasswords
- Remove app passwords you're not using
- Generate new ones if compromised

### 4. Monitor Account Activity
- Check: https://myaccount.google.com/notifications
- Review recent security events
- Enable alerts for suspicious activity

## Advanced Configuration

### Custom Email Templates

Edit `backend/email_service.py` to customize the HTML template:

```python
def _create_html_report(self, report):
    # Modify HTML structure here
    html = f"""
    <!DOCTYPE html>
    <html>
    ...
    </html>
    """
    return html
```

### Add Attachments

To add PDF or CSV attachments:

```python
from email.mime.base import MIMEBase
from email import encoders

# Create attachment
attachment = MIMEBase('application', 'pdf')
attachment.set_payload(pdf_data)
encoders.encode_base64(attachment)
attachment.add_header('Content-Disposition', f'attachment; filename=report.pdf')
msg.attach(attachment)
```

### Multiple Recipients

To send to multiple emails:

```python
msg['To'] = ', '.join(['email1@example.com', 'email2@example.com'])
```

### Custom SMTP Server

To use a different email provider:

```python
# For Outlook/Hotmail
smtp_server = "smtp-mail.outlook.com"
smtp_port = 587

# For Yahoo
smtp_server = "smtp.mail.yahoo.com"
smtp_port = 587

# For custom domain
smtp_server = "smtp.yourdomain.com"
smtp_port = 587
```

## API Endpoint

### Send Email Report

**Endpoint:** `POST /api/email-report`

**Request Body:**
```json
{
  "email": "recipient@example.com",
  "report": {
    "ticker": "AAPL",
    "quote": {...},
    "executive_summary": {...},
    "predictions": {...},
    "combined_sentiment": {...},
    "news_summary": {...}
  }
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Report sent to recipient@example.com"
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Gmail credentials not configured"
}
```

## Testing

### Test Email Sending

```bash
curl -X POST http://localhost:5000/api/email-report \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "report": {
      "ticker": "AAPL",
      "quote": {"price": 175.43, "change": 2.15, "changePercent": 1.24},
      "executive_summary": {"rating": "Strong Bull", "recommendation": "BUY"}
    }
  }'
```

### Verify Email Delivery

1. Check recipient inbox
2. Check spam/junk folder
3. Verify email formatting
4. Test on mobile device
5. Check all links work

## Limitations

### Gmail Sending Limits

- **Free Gmail:** 500 emails per day
- **Google Workspace:** 2,000 emails per day
- **Per-minute limit:** ~20 emails

If you exceed limits:
- Wait 24 hours for reset
- Upgrade to Google Workspace
- Use a different email service

### Email Size Limits

- Maximum email size: 25 MB
- Recommended: Keep under 1 MB
- Large reports may be truncated

## Alternative Email Providers

### SendGrid (Recommended for Production)

```python
import sendgrid
from sendgrid.helpers.mail import Mail

sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
message = Mail(
    from_email='noreply@yourdomain.com',
    to_emails='recipient@example.com',
    subject='Investment Report',
    html_content=html_body
)
response = sg.send(message)
```

### AWS SES (Simple Email Service)

```python
import boto3

ses = boto3.client('ses', region_name='us-east-1')
response = ses.send_email(
    Source='noreply@yourdomain.com',
    Destination={'ToAddresses': ['recipient@example.com']},
    Message={
        'Subject': {'Data': 'Investment Report'},
        'Body': {'Html': {'Data': html_body}}
    }
)
```

## Summary

Email functionality allows you to:
- ✓ Send professional investment reports via email
- ✓ Share analysis with clients or team members
- ✓ Keep records of research in your inbox
- ✓ Access reports on any device

**Setup Time:** 5-10 minutes
**Cost:** Free (using Gmail)
**Difficulty:** Easy

Just generate a Gmail App Password, add it to `.env`, and start sending reports!
