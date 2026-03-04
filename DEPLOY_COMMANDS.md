# Deployment Commands Cheat Sheet

## 🚀 Streamlit Deployment (Recommended - 10 Minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements_streamlit.txt
```

### Step 2: Test Locally

**Terminal 1 - Start Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Start Streamlit:**
```bash
streamlit run streamlit_app.py
```

**Or use the batch file:**
```bash
run_streamlit.bat
```

Visit: `http://localhost:8501`

### Step 3: Deploy Backend to Railway

```bash
# Push to GitHub first
git add .
git commit -m "Ready for deployment"
git push origin main

# Then go to railway.app and:
# 1. New Project → Deploy from GitHub
# 2. Select repository
# 3. Root Directory: backend
# 4. Add environment variables from backend/.env
# 5. Copy the generated URL
```

### Step 4: Deploy Streamlit to Streamlit Cloud

```bash
# Go to share.streamlit.io
# 1. Sign in with GitHub
# 2. New app → Select your repository
# 3. Main file: streamlit_app.py
# 4. Advanced settings → Add secrets:

API_URL = "https://your-backend.railway.app"

# 5. Deploy!
```

**Done! Your app is live! 🎉**

---

## 📱 React Deployment (Alternative - 20 Minutes)

### Step 1: Deploy Backend

**Railway:**
```bash
cd backend
git init
git add .
git commit -m "Backend deployment"

# Go to railway.app
# New Project → Deploy from GitHub
# Select backend folder
# Add environment variables
```

**Or Render:**
```bash
# Go to render.com
# New Web Service
# Root Directory: backend
# Build: pip install -r requirements.txt
# Start: gunicorn app:app
# Add environment variables
```

### Step 2: Build Frontend

```bash
cd frontend

# Create production environment file
echo REACT_APP_API_URL=https://your-backend-url.com > .env.production

# Build
npm install
npm run build
```

### Step 3: Deploy Frontend

**Vercel:**
```bash
npm install -g vercel
cd frontend
vercel --prod
```

**Or Netlify:**
```bash
npm install -g netlify-cli
cd frontend
netlify deploy --prod --dir=build
```

---

## 🐳 Docker Deployment

### Build and Run Locally

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Deploy to DigitalOcean/AWS

```bash
# SSH into server
ssh user@your-server-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone repository
git clone your-repo-url
cd your-repo

# Copy environment file
cp backend/.env.example backend/.env
nano backend/.env  # Add your API keys

# Deploy
docker-compose up -d

# Check status
docker-compose ps
```

---

## 🔧 Maintenance Commands

### Update Streamlit App

```bash
# Make changes to streamlit_app.py
git add .
git commit -m "Update app"
git push origin main

# Streamlit Cloud auto-deploys!
```

### Update Backend

```bash
cd backend
# Make changes
git add .
git commit -m "Update backend"
git push origin main

# Railway/Render auto-deploys!
```

### View Logs

**Streamlit Cloud:**
- Go to app dashboard → Click "Manage app" → View logs

**Railway:**
```bash
# In Railway dashboard → Select service → View logs
```

**Docker:**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Restart Services

**Streamlit Cloud:**
- Dashboard → Reboot app

**Railway:**
- Dashboard → Service → Restart

**Docker:**
```bash
docker-compose restart
```

---

## 🔐 Environment Variables

### Backend (.env)

```bash
# Required
OPENAI_API_KEY=your_key
NEWS_API_KEY=your_key

# Optional (for additional features)
ALPHA_VANTAGE_API_KEY=your_key
FINNHUB_API_KEY=your_key
POLYGON_API_KEY=your_key
MARKETSTACK_API_KEY=your_key
EODHD_API_KEY=your_key
FMP_API_KEY=your_key
FRED_API_KEY=your_key
TWITTER_BEARER_TOKEN=your_key

# MCP Server
USE_MCP_FOR_FINANCIAL_DATA=true
MCP_SERVER_COMMAND=C:\Users\daksh\.local\bin\uvx.exe

# Email (optional)
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_app_password
```

### Streamlit Secrets

```toml
# .streamlit/secrets.toml (local)
# Or Streamlit Cloud dashboard (production)

API_URL = "https://your-backend-url.com"

# Optional: Add API keys if running integrated backend
OPENAI_API_KEY = "your_key"
NEWS_API_KEY = "your_key"
```

### React Environment

```bash
# frontend/.env.production
REACT_APP_API_URL=https://your-backend-url.com
```

---

## 🧪 Testing Commands

### Test Backend

```bash
cd backend

# Test API connection
python check_data_source.py

# Test specific features
python test_news_search.py
python test_social_search.py
python test_mcp_server.py

# Test integration
python test_integration.py
```

### Test Frontend

**React:**
```bash
cd frontend
npm test
npm run build  # Test build
```

**Streamlit:**
```bash
streamlit run streamlit_app.py
# Open http://localhost:8501 and test manually
```

---

## 📊 Monitoring

### Check API Usage

**OpenAI:**
- https://platform.openai.com/usage

**NewsAPI:**
- https://newsapi.org/account

**Alpha Vantage:**
- Check email for daily usage reports

### Check Deployment Status

**Streamlit Cloud:**
- https://share.streamlit.io/

**Railway:**
- https://railway.app/dashboard

**Vercel:**
- https://vercel.com/dashboard

---

## 🆘 Troubleshooting Commands

### Backend Not Starting

```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
cd backend
pip install -r requirements.txt --force-reinstall

# Check for errors
python app.py
```

### Frontend Not Building

```bash
# Clear cache
cd frontend
rm -rf node_modules package-lock.json
npm install

# Try building
npm run build
```

### Streamlit Issues

```bash
# Clear cache
streamlit cache clear

# Reinstall
pip uninstall streamlit
pip install streamlit

# Check version
streamlit --version
```

### Docker Issues

```bash
# Remove all containers
docker-compose down -v

# Rebuild from scratch
docker-compose build --no-cache

# Check logs
docker-compose logs -f
```

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Run Streamlit locally | `streamlit run streamlit_app.py` |
| Run React locally | `cd frontend && npm start` |
| Run backend locally | `cd backend && python app.py` |
| Build React | `cd frontend && npm run build` |
| Deploy with Docker | `docker-compose up -d` |
| View logs | `docker-compose logs -f` |
| Stop all services | `docker-compose down` |
| Update dependencies | `pip install -r requirements.txt` |

---

## 📝 Deployment Checklist

- [ ] Backend deployed and running
- [ ] Backend URL obtained
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] Frontend deployed
- [ ] API URL configured in frontend
- [ ] Test all features
- [ ] Monitor logs for errors
- [ ] Set up billing alerts
- [ ] Document deployment URLs

---

## 🚀 Recommended: Streamlit + Railway

**Fastest deployment path:**

1. Deploy backend to Railway (5 min)
2. Deploy Streamlit to Streamlit Cloud (5 min)
3. Total: 10 minutes, $0-5/month

**Commands:**
```bash
# 1. Push to GitHub
git add .
git commit -m "Deploy"
git push origin main

# 2. Go to railway.app → Deploy backend
# 3. Go to share.streamlit.io → Deploy Streamlit
# 4. Done!
```

---

Need help? Check the detailed guides:
- `STREAMLIT_DEPLOY.md` - Streamlit deployment
- `DEPLOYMENT_GUIDE.md` - All deployment options
- `STREAMLIT_QUICKSTART.md` - Quick start guide
