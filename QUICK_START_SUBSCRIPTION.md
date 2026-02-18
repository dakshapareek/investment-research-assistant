# Quick Start: Daily Stock Alerts

## For Users

### Subscribe in 3 Steps

1. **Click "Alerts" button** in the header (blue button with email icon)

2. **Fill in the form:**
   - Email: `your.email@gmail.com`
   - Tickers: `AAPL, MSFT, GOOGL` (comma-separated)
   - Threshold: `2.0` (percentage)

3. **Click "Subscribe to Daily Alerts"**

Done! You'll receive emails when your stocks move more than 2%.

### Unsubscribe

**Option 1:** Click "Alerts" → Click "Unsubscribe" button

**Option 2:** Click unsubscribe link in any alert email

## For Developers

### Start the Server

```bash
cd backend
python app.py
```

You'll see:
```
✓ Scheduler started successfully
Daily alerts scheduled for: 09:00
```

### Test the System

```bash
# Run automated tests
python backend/test_subscription.py

# Or test manually
curl -X POST http://localhost:5000/api/test-alerts
```

### Change Alert Time

Edit `backend/app.py` line with `start_scheduler`:

```python
start_scheduler(alert_time="15:30")  # 3:30 PM
```

## How It Works

1. **9 AM Daily:** Scheduler checks all subscriptions
2. **Fetch Prices:** Gets current stock prices via MCP/APIs
3. **Check Threshold:** Compares change % to user's threshold
4. **Send Email:** If exceeded, sends formatted HTML email
5. **One Per Day:** Won't send again until next day

## Email Example

```
Subject: 🚨 Daily Stock Alert - 2 stocks moved >2%

AAPL  $182.50  ▲ $4.25   +2.38%
NVDA  $720.15  ▼ $18.50  -2.50%

[Unsubscribe]
```

## API Quick Reference

```bash
# Subscribe
curl -X POST http://localhost:5000/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","tickers":["AAPL"],"threshold":2.0}'

# Check subscription
curl http://localhost:5000/api/subscription/user@example.com

# Test alerts now
curl -X POST http://localhost:5000/api/test-alerts

# Unsubscribe
curl -X POST http://localhost:5000/api/unsubscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}'
```

## Files

- **Backend:** `backend/subscription_service.py`, `backend/scheduler.py`
- **Frontend:** `frontend/src/components/Subscription.js`
- **Database:** `backend/subscriptions.json` (auto-created)
- **Docs:** `SUBSCRIPTION_FEATURE.md` (full documentation)

## Troubleshooting

**No emails?**
- Check Gmail credentials in `.env`
- Verify threshold is set correctly
- Check server logs for errors

**Scheduler not running?**
- Look for "Scheduler started successfully" in logs
- Restart server if needed

**Can't unsubscribe?**
- Use email address or subscription ID
- Check `subscriptions.json` for active status

## Support

See `SUBSCRIPTION_FEATURE.md` for complete documentation.

---

**Status:** ✅ Ready to Use
**Version:** 1.0.0
