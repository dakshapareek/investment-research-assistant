# Streamlit Quick Start Guide

## Test Locally (2 Minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements_streamlit.txt
```

### Step 2: Start Backend (Terminal 1)
```bash
cd backend
python app.py
```

Backend will run at: `http://localhost:5000`

### Step 3: Start Streamlit (Terminal 2)
```bash
streamlit run streamlit_app.py
```

Streamlit will open at: `http://localhost:8501`

**Or use the batch file:**
```bash
# Make sure backend is running first!
run_streamlit.bat
```

---

## Deploy to Streamlit Cloud (5 Minutes)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Add Streamlit app"
git push origin main
```

### Step 2: Deploy Backend
Choose one option:

**Option A: Railway (Recommended)**
1. Go to [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Select `backend` folder
4. Add environment variables from `backend/.env`
5. Copy the URL (e.g., `https://your-app.railway.app`)

**Option B: Render**
1. Go to [render.com](https://render.com)
2. New Web Service → Connect GitHub
3. Root Directory: `backend`
4. Start Command: `gunicorn app:app`
5. Add environment variables
6. Copy the URL

### Step 3: Deploy Streamlit
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. New app → Select your repository
4. Main file: `streamlit_app.py`
5. Advanced settings → Secrets:
   ```toml
   API_URL = "https://your-backend-url.com"
   ```
6. Deploy!

### Step 4: Done! 🎉
Your app is live at: `https://your-app.streamlit.app`

---

## Features

The Streamlit app includes:

✅ **Interactive Dashboard**
- Real-time stock data
- Price charts with Plotly
- Watchlist management
- Multi-tab interface

✅ **Analysis Tools**
- News aggregation
- Social media sentiment
- Technical indicators
- AI predictions

✅ **User-Friendly**
- Clean, modern UI
- Responsive design
- Easy navigation
- Quick stock search

---

## Comparison: React vs Streamlit

| Feature | React Frontend | Streamlit |
|---------|---------------|-----------|
| Setup Time | 30 min | 5 min |
| Deployment | 2 services | 1 service |
| Customization | High | Medium |
| Learning Curve | Steep | Easy |
| Cost | $10-20/month | FREE |
| Best For | Production | Demos, MVPs |

---

## Tips

1. **Caching**: Add `@st.cache_data` to expensive functions
2. **Secrets**: Never commit `.streamlit/secrets.toml`
3. **Performance**: Use `st.spinner()` for loading states
4. **Updates**: Streamlit auto-reloads on file changes

---

## Troubleshooting

**"Connection refused"**
- Make sure backend is running
- Check `API_URL` in secrets

**"Module not found"**
- Run: `pip install -r requirements_streamlit.txt`

**"Slow loading"**
- Add caching with `@st.cache_data`
- Reduce API calls

---

## Next Steps

1. Test locally ✓
2. Deploy backend ✓
3. Deploy Streamlit ✓
4. Share your app! 🚀

Need help? Check `STREAMLIT_DEPLOY.md` for detailed instructions.
