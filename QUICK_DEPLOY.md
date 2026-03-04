# Quick Deploy - 3 Easiest Options

## Option 1: Railway (Recommended - 10 minutes)

### Why Railway?
- Zero configuration needed
- Free tier available ($5 credit/month)
- Automatic HTTPS
- Easy environment variable management
- GitHub integration

### Steps:

1. **Sign up at [railway.app](https://railway.app)**

2. **Push your code to GitHub** (if not already)
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

3. **Deploy Backend**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Click "Add Service" → "GitHub Repo"
   - Root Directory: `backend`
   - Railway auto-detects Python and uses Procfile
   - Add environment variables:
     - Click "Variables" tab
     - Add all keys from your `.env` file
     - `OPENAI_API_KEY`, `NEWS_API_KEY`, etc.
   - Click "Deploy"
   - Copy the generated URL (e.g., `https://your-app.railway.app`)

4. **Deploy Frontend**
   - In same project, click "New Service"
   - Select your repository again
   - Root Directory: `frontend`
   - Add environment variable:
     - `REACT_APP_API_URL`: Your backend URL from step 3
   - Click "Deploy"

5. **Done!** Your app is live at the frontend URL

**Cost:** Free tier ($5/month credit) covers light usage

---

## Option 2: Vercel (Frontend) + Render (Backend)

### Backend on Render (5 minutes)

1. **Go to [render.com](https://render.com)** and sign up

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Name: `investment-research-backend`
   - Root Directory: `backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Instance Type: Free

3. **Add Environment Variables**
   - Scroll to "Environment Variables"
   - Add all from your `.env` file
   - Click "Create Web Service"
   - Copy the URL (e.g., `https://your-app.onrender.com`)

### Frontend on Vercel (3 minutes)

1. **Go to [vercel.com](https://vercel.com)** and sign up

2. **Import Project**
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - Framework Preset: Create React App
   - Root Directory: `frontend`
   - Environment Variables:
     - `REACT_APP_API_URL`: Your Render backend URL
   - Click "Deploy"

3. **Done!** Your app is live

**Cost:** Both have generous free tiers

---

## Option 3: Docker on Your Own Server

### If you have a VPS (DigitalOcean, AWS EC2, etc.)

1. **SSH into your server**
   ```bash
   ssh user@your-server-ip
   ```

2. **Install Docker**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   ```

3. **Clone and deploy**
   ```bash
   git clone your-repo-url
   cd your-repo
   
   # Copy and update .env
   cp backend/.env.example backend/.env
   nano backend/.env  # Add your API keys
   
   # Deploy
   docker-compose up -d
   ```

4. **Access your app**
   - Frontend: `http://your-server-ip:3000`
   - Backend: `http://your-server-ip:5000`

5. **Optional: Setup domain and HTTPS**
   - Point domain to your server IP
   - Install Nginx and Certbot for SSL

**Cost:** VPS costs ($5-10/month for DigitalOcean droplet)

---

## Comparison

| Platform | Setup Time | Free Tier | Best For |
|----------|------------|-----------|----------|
| Railway | 10 min | $5/month credit | Easiest, all-in-one |
| Vercel + Render | 8 min | Yes (both) | Separate services |
| Docker VPS | 20 min | No (VPS cost) | Full control |

---

## My Recommendation

**Start with Railway** because:
- Fastest setup (literally 10 minutes)
- No credit card required for free tier
- Automatic HTTPS and custom domains
- Easy to scale later
- Great for demos and MVPs

Once you need more control or have higher traffic, migrate to AWS/GCP.

---

## After Deployment

1. **Test your app**
   - Visit the frontend URL
   - Try searching for a stock
   - Check if data loads correctly

2. **Monitor usage**
   - Check Railway/Render dashboard for logs
   - Monitor API usage (OpenAI, NewsAPI)
   - Set up billing alerts

3. **Update environment**
   - Frontend: Update `REACT_APP_API_URL` if backend URL changes
   - Backend: Keep API keys secure, never commit `.env`

---

## Troubleshooting

**Backend not starting?**
- Check logs in Railway/Render dashboard
- Verify all environment variables are set
- Check if `gunicorn` is in requirements.txt

**Frontend can't connect to backend?**
- Verify `REACT_APP_API_URL` is correct
- Check CORS settings in `backend/app.py`
- Ensure backend is running (check logs)

**API errors?**
- Verify API keys are correct
- Check API rate limits
- Review backend logs for specific errors

---

## Need Help?

- Railway: https://docs.railway.app/
- Render: https://render.com/docs
- Vercel: https://vercel.com/docs

Or check the full `DEPLOYMENT_GUIDE.md` for more options.
