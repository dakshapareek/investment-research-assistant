# Streamlit Deployment Guide

## 🚀 Deploy to Streamlit Cloud (Easiest - 5 Minutes!)

### Why Streamlit Cloud?
- **100% FREE** for public apps
- Zero configuration needed
- Automatic HTTPS
- Direct GitHub integration
- Built-in secrets management
- No credit card required

---

## Quick Deploy Steps

### 1. Prepare Your Repository

Your app is ready! Just make sure you have:
- ✅ `streamlit_app.py` (main app file)
- ✅ `requirements_streamlit.txt` (dependencies)
- ✅ `.streamlit/config.toml` (theme settings)
- ✅ Backend running somewhere (see options below)

### 2. Push to GitHub

```bash
# If not already on GitHub
git add .
git commit -m "Add Streamlit app"
git push origin main
```

### 3. Deploy on Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**

2. **Sign in with GitHub**

3. **Click "New app"**

4. **Configure deployment:**
   - Repository: Select your repo
   - Branch: `main`
   - Main file path: `streamlit_app.py`
   - Python version: 3.11

5. **Add Secrets** (click "Advanced settings"):
   ```toml
   API_URL = "https://your-backend-url.com"
   
   # Optional: If you want to run backend integrated
   OPENAI_API_KEY = "your-key"
   NEWS_API_KEY = "your-key"
   ALPHA_VANTAGE_API_KEY = "your-key"
   # ... add all your API keys
   ```

6. **Click "Deploy"**

7. **Done!** Your app will be live at `https://your-app.streamlit.app`

---

## Backend Options

You have 3 options for the backend:

### Option A: Keep Flask Backend Separate (Recommended)

Deploy your Flask backend to Railway/Render (see DEPLOYMENT_GUIDE.md), then:

1. Get your backend URL (e.g., `https://your-app.railway.app`)
2. Add it to Streamlit secrets:
   ```toml
   API_URL = "https://your-app.railway.app"
   ```

**Pros:** Separation of concerns, easier to scale
**Cons:** Need to deploy two services

### Option B: Integrated Backend (All-in-One)

Run Flask backend within Streamlit app:

1. **Create `backend_runner.py`:**
   ```python
   import subprocess
   import os
   
   def start_backend():
       os.chdir('backend')
       subprocess.Popen(['python', 'app.py'])
   ```

2. **Update `streamlit_app.py`** (add at top):
   ```python
   from backend_runner import start_backend
   start_backend()
   ```

3. **Update requirements:**
   ```bash
   cat backend/requirements.txt >> requirements_streamlit.txt
   ```

**Pros:** Single deployment
**Cons:** More resource-intensive, harder to debug

### Option C: Serverless Backend

Use Streamlit's built-in caching and run everything in Streamlit:

1. Move all backend logic into Streamlit
2. Use `@st.cache_data` for API calls
3. No separate Flask server needed

**Pros:** Simplest deployment
**Cons:** Need to refactor code significantly

---

## Local Testing

Before deploying, test locally:

### 1. Install dependencies
```bash
pip install -r requirements_streamlit.txt
```

### 2. Start backend (in one terminal)
```bash
cd backend
python app.py
```

### 3. Start Streamlit (in another terminal)
```bash
streamlit run streamlit_app.py
```

### 4. Open browser
Visit `http://localhost:8501`

---

## Configuration

### Update API URL

**For local development:**
Edit `.streamlit/secrets.toml`:
```toml
API_URL = "http://localhost:5000"
```

**For production:**
Add in Streamlit Cloud dashboard under "Secrets":
```toml
API_URL = "https://your-backend.railway.app"
```

### Custom Domain

1. Go to Streamlit Cloud dashboard
2. Click on your app
3. Settings → Custom domain
4. Follow instructions to point your domain

---

## Deployment Checklist

- [ ] Backend deployed and accessible
- [ ] Backend URL added to Streamlit secrets
- [ ] All API keys added to secrets
- [ ] CORS enabled in backend for Streamlit domain
- [ ] App tested locally
- [ ] Code pushed to GitHub
- [ ] Streamlit app deployed
- [ ] App tested in production

---

## Update Backend CORS

Your backend needs to allow requests from Streamlit:

**Edit `backend/app.py`:**
```python
from flask_cors import CORS

# Update CORS to include Streamlit domain
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:8501",  # Local Streamlit
            "https://*.streamlit.app",  # Streamlit Cloud
            "https://your-custom-domain.com"  # Your domain
        ]
    }
})
```

---

## Troubleshooting

### "Cannot connect to backend"
- Check if backend is running
- Verify `API_URL` in secrets
- Check backend logs for errors
- Ensure CORS is configured correctly

### "Module not found"
- Check `requirements_streamlit.txt` has all dependencies
- Redeploy app after updating requirements

### "App is slow"
- Add caching with `@st.cache_data`
- Consider upgrading Streamlit Cloud plan
- Optimize API calls

### "Secrets not working"
- Secrets are case-sensitive
- Restart app after updating secrets
- Check for typos in secret names

---

## Cost Comparison

| Platform | Cost | Best For |
|----------|------|----------|
| Streamlit Cloud | FREE | Public apps, demos |
| Streamlit Cloud (Private) | $20/month | Private apps |
| Railway (Backend) | $5/month | Backend hosting |
| **Total** | **$0-25/month** | Full stack |

---

## Advanced: Custom Deployment

### Deploy to Your Own Server

1. **Install Streamlit:**
   ```bash
   pip install streamlit
   ```

2. **Run with custom port:**
   ```bash
   streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
   ```

3. **Use systemd for auto-restart:**
   ```ini
   [Unit]
   Description=Streamlit App
   After=network.target

   [Service]
   User=your-user
   WorkingDirectory=/path/to/app
   ExecStart=/usr/bin/streamlit run streamlit_app.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

4. **Setup Nginx reverse proxy:**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
       }
   }
   ```

---

## Next Steps

1. **Deploy backend** (Railway/Render recommended)
2. **Deploy Streamlit app** (Streamlit Cloud)
3. **Test thoroughly**
4. **Share your app!**

Your app will be live at: `https://your-app.streamlit.app`

---

## Resources

- Streamlit Docs: https://docs.streamlit.io
- Streamlit Cloud: https://share.streamlit.io
- Community Forum: https://discuss.streamlit.io
- Railway: https://railway.app
- Render: https://render.com

---

## Example: Complete Deployment

Here's what I recommend:

1. **Backend on Railway** (5 min)
   - Deploy Flask backend
   - Get URL: `https://investment-backend.railway.app`

2. **Frontend on Streamlit Cloud** (5 min)
   - Deploy Streamlit app
   - Add secret: `API_URL = "https://investment-backend.railway.app"`
   - Get URL: `https://investment-research.streamlit.app`

3. **Total time: 10 minutes**
4. **Total cost: $0-5/month**

**You're done!** 🎉
