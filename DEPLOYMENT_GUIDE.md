# Investment Research Agent - Deployment Guide

## Deployment Options

### Option 1: Heroku (Easiest - Free Tier Available)

**Best for:** Quick deployment, minimal configuration

#### Backend Deployment

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Prepare Backend**
   ```bash
   cd backend
   
   # Create Procfile
   echo "web: gunicorn app:app" > Procfile
   
   # Add gunicorn to requirements.txt
   echo "gunicorn==21.2.0" >> requirements.txt
   
   # Create runtime.txt (specify Python version)
   echo "python-3.11.0" > runtime.txt
   ```

3. **Deploy to Heroku**
   ```bash
   heroku login
   heroku create your-app-name-backend
   
   # Set environment variables
   heroku config:set OPENAI_API_KEY=your_key
   heroku config:set NEWS_API_KEY=your_key
   heroku config:set ALPHA_VANTAGE_API_KEY=your_key
   # ... add all other API keys from .env
   
   git init
   git add .
   git commit -m "Initial backend deployment"
   git push heroku main
   ```

#### Frontend Deployment

1. **Update API URL**
   ```bash
   cd frontend
   
   # Create .env.production
   echo "REACT_APP_API_URL=https://your-app-name-backend.herokuapp.com" > .env.production
   ```

2. **Build and Deploy**
   ```bash
   npm run build
   
   # Deploy to Heroku
   heroku create your-app-name-frontend
   heroku buildpacks:set mars/create-react-app
   git init
   git add .
   git commit -m "Initial frontend deployment"
   git push heroku main
   ```

---

### Option 2: Vercel (Frontend) + Render (Backend)

**Best for:** Modern deployment, good free tier

#### Backend on Render

1. **Go to [render.com](https://render.com)**
2. **Create New Web Service**
   - Connect your GitHub repo
   - Select `backend` folder
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Add environment variables from `.env`

#### Frontend on Vercel

1. **Go to [vercel.com](https://vercel.com)**
2. **Import Project**
   - Connect GitHub repo
   - Framework: Create React App
   - Root Directory: `frontend`
   - Environment Variables:
     - `REACT_APP_API_URL`: Your Render backend URL

---

### Option 3: AWS (Production-Ready)

**Best for:** Scalability, full control

#### Backend on AWS Elastic Beanstalk

1. **Install AWS CLI and EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB**
   ```bash
   cd backend
   eb init -p python-3.11 investment-research-backend
   eb create production-env
   
   # Set environment variables
   eb setenv OPENAI_API_KEY=your_key NEWS_API_KEY=your_key
   ```

#### Frontend on AWS S3 + CloudFront

1. **Build Frontend**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to S3**
   ```bash
   aws s3 mb s3://your-bucket-name
   aws s3 sync build/ s3://your-bucket-name
   aws s3 website s3://your-bucket-name --index-document index.html
   ```

3. **Setup CloudFront** (optional, for HTTPS and CDN)

---

### Option 4: Docker + DigitalOcean/AWS EC2

**Best for:** Full control, containerization

#### Create Dockerfiles

**Backend Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

**Frontend Dockerfile:**
```dockerfile
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    env_file:
      - ./backend/.env
    restart: always

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - REACT_APP_API_URL=http://your-domain.com:5000
    depends_on:
      - backend
    restart: always
```

#### Deploy to DigitalOcean

1. **Create Droplet** (Ubuntu 22.04)
2. **Install Docker**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```

3. **Deploy**
   ```bash
   git clone your-repo
   cd your-repo
   docker-compose up -d
   ```

---

### Option 5: Railway (Simplest Full-Stack)

**Best for:** Zero-config deployment

1. **Go to [railway.app](https://railway.app)**
2. **New Project → Deploy from GitHub**
3. **Add Backend Service**
   - Root Directory: `backend`
   - Start Command: `gunicorn app:app`
   - Add environment variables
4. **Add Frontend Service**
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Start Command: `npx serve -s build`
   - Add `REACT_APP_API_URL` pointing to backend

---

## Pre-Deployment Checklist

### Backend Preparation

1. **Add gunicorn to requirements.txt**
   ```bash
   cd backend
   echo "gunicorn==21.2.0" >> requirements.txt
   ```

2. **Update CORS settings in app.py**
   ```python
   # Allow your frontend domain
   CORS(app, resources={r"/api/*": {"origins": ["https://your-frontend-domain.com"]}})
   ```

3. **Environment Variables**
   - Never commit `.env` file
   - Set all API keys in deployment platform
   - Update `MCP_SERVER_COMMAND` path if needed

4. **Database** (if adding persistence)
   - Currently using JSON files
   - Consider PostgreSQL for production

### Frontend Preparation

1. **Update API URL**
   ```bash
   cd frontend
   # Create .env.production
   echo "REACT_APP_API_URL=https://your-backend-url.com" > .env.production
   ```

2. **Build optimization**
   ```bash
   npm run build
   # Test the build locally
   npx serve -s build
   ```

---

## Security Considerations

1. **API Keys**
   - Use environment variables
   - Never commit to Git
   - Rotate keys regularly

2. **CORS**
   - Restrict to your frontend domain
   - Don't use `*` in production

3. **HTTPS**
   - Use SSL certificates (Let's Encrypt is free)
   - Most platforms provide this automatically

4. **Rate Limiting**
   - Add Flask-Limiter to prevent abuse
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=lambda: request.remote_addr)
   ```

---

## Monitoring & Maintenance

1. **Logging**
   - Use platform logging (Heroku logs, Railway logs)
   - Consider Sentry for error tracking

2. **Uptime Monitoring**
   - UptimeRobot (free)
   - Pingdom
   - StatusCake

3. **Cost Management**
   - Monitor API usage (OpenAI, NewsAPI)
   - Set up billing alerts
   - Use caching to reduce API calls

---

## Recommended: Railway (Quickest Start)

For your first deployment, I recommend Railway:

1. Sign up at railway.app
2. Connect GitHub
3. Deploy both services
4. Add environment variables
5. Done in ~10 minutes

**Estimated Costs:**
- Railway: $5-20/month (free tier available)
- API costs: $10-50/month depending on usage
- Total: ~$15-70/month

---

## Need Help?

- Heroku: https://devcenter.heroku.com/
- Vercel: https://vercel.com/docs
- Railway: https://docs.railway.app/
- AWS: https://aws.amazon.com/getting-started/
