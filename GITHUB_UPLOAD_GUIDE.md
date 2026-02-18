# GitHub Upload Guide - Step by Step

## Option 1: Using GitHub Desktop (Easiest)

### Step 1: Install GitHub Desktop
1. Download from: https://desktop.github.com/
2. Install and sign in with your GitHub account
3. If you don't have a GitHub account, create one at https://github.com/signup

### Step 2: Create Repository
1. Open GitHub Desktop
2. Click "File" → "New Repository"
3. Fill in:
   - **Name**: `investment-research-assistant`
   - **Description**: `AI-powered agentic system for automated stock analysis`
   - **Local Path**: Choose your project folder location
   - **Initialize with README**: Uncheck (we already have one)
4. Click "Create Repository"

### Step 3: Add Your Files
1. Copy all your project files to the repository folder
2. GitHub Desktop will show all files as "changes"
3. In the bottom left, write commit message: "Initial commit - Complete investment research system"
4. Click "Commit to main"

### Step 4: Publish to GitHub
1. Click "Publish repository" button at the top
2. Uncheck "Keep this code private" (so graders can access)
3. Click "Publish Repository"

### Step 5: Get Your Link
1. Click "View on GitHub" button
2. Copy the URL from your browser (e.g., `https://github.com/yourusername/investment-research-assistant`)
3. **This is your submission link!**

---

## Option 2: Using Command Line (Git)

### Step 1: Install Git
- Windows: Download from https://git-scm.com/download/win
- Already installed on Mac/Linux

### Step 2: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `investment-research-assistant`
3. Description: `AI-powered agentic system for automated stock analysis`
4. Public repository
5. Don't initialize with README
6. Click "Create repository"

### Step 3: Upload Your Code
Open terminal/command prompt in your project folder and run:

```bash
# Navigate to your project folder
cd C:\Users\daksh\OneDrive\Desktop\investment-research-agent

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Complete investment research system"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/investment-research-assistant.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Get Your Link
Your link will be: `https://github.com/YOUR_USERNAME/investment-research-assistant`

---

## Option 3: Using GitHub Web Interface (No Git Required)

### Step 1: Create Repository
1. Go to https://github.com/new
2. Repository name: `investment-research-assistant`
3. Description: `AI-powered agentic system for automated stock analysis`
4. Public repository
5. Click "Create repository"

### Step 2: Upload Files
1. Click "uploading an existing file"
2. Drag and drop your entire project folder
3. Or click "choose your files" and select all files
4. Scroll down and click "Commit changes"

**Note**: This method has file size limits and may require multiple uploads for large projects.

---

## Important: Before Uploading

### 1. Remove Sensitive Information
Create a `.gitignore` file in your project root:

```
# Environment variables (contains API keys)
.env
backend/.env

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/

# Node
node_modules/
npm-debug.log
.DS_Store

# IDE
.vscode/
.idea/
*.swp
*.swo
```

### 2. Create .env.example
Copy your `.env` file to `.env.example` and replace actual keys with placeholders:

```bash
# In backend folder
OPENAI_API_KEY=your_openai_api_key_here
NEWS_API_KEY=your_newsapi_key_here
REDDIT_CLIENT_ID=your_reddit_client_id_here
# ... etc
```

This shows graders what keys are needed without exposing yours.

---

## After Uploading - Update Documentation

Once you have your GitHub link, update these files:

### 1. Update PROJECT_SUBMISSION.md
Find this line:
```markdown
**GitHub Repository**: [To be provided by user]
```

Replace with:
```markdown
**GitHub Repository**: https://github.com/YOUR_USERNAME/investment-research-assistant
```

### 2. Update README.md
Add at the top:
```markdown
## 🔗 Links

- **GitHub Repository**: https://github.com/YOUR_USERNAME/investment-research-assistant
- **Live Demo**: [If you deploy it]
```

---

## Verification Checklist

Before submitting, verify:

- ✅ Repository is PUBLIC (not private)
- ✅ All files are uploaded (backend, frontend, docs)
- ✅ README.md is visible on GitHub homepage
- ✅ PROJECT_SUBMISSION.md is accessible
- ✅ .env file is NOT uploaded (use .env.example instead)
- ✅ Link works when opened in incognito/private browser
- ✅ All 30+ documentation files are present

---

## Quick Test

1. Open your GitHub link in an incognito/private browser window
2. You should see:
   - Repository name and description
   - README.md displayed on the homepage
   - All folders (backend, frontend) visible
   - All .md documentation files listed

If you can see everything, graders can too!

---

## Alternative: Google Drive (If GitHub Doesn't Work)

### Step 1: Create Zip File
1. Right-click your project folder
2. Select "Send to" → "Compressed (zipped) folder"
3. Name it: `investment-research-assistant.zip`

### Step 2: Upload to Google Drive
1. Go to https://drive.google.com
2. Click "New" → "File upload"
3. Select your zip file
4. Wait for upload to complete

### Step 3: Share Link
1. Right-click the uploaded file
2. Click "Share"
3. Change to "Anyone with the link"
4. Set permission to "Viewer"
5. Click "Copy link"
6. **This is your submission link!**

---

## Need Help?

If you encounter issues:

1. **GitHub Desktop not working?**
   - Try the web interface method
   - Or use Google Drive as backup

2. **Files too large?**
   - Remove `node_modules` folder (can be reinstalled with `npm install`)
   - Remove `__pycache__` folders
   - Compress images if any

3. **Git errors?**
   - Make sure you're in the correct folder
   - Check if git is installed: `git --version`
   - Try GitHub Desktop instead

---

## What to Submit

**For your assignment submission, provide:**

1. **GitHub Link**: `https://github.com/YOUR_USERNAME/investment-research-assistant`
2. **Key Files to Highlight**:
   - `PROJECT_SUBMISSION.md` - Complete documentation
   - `README.md` - Quick overview
   - `backend/report_generator.py` - Main orchestrator
   - `PERFORMANCE_OPTIMIZATION.md` - Shows 2-3x speedup

**In your submission form, write:**
```
GitHub Repository: https://github.com/YOUR_USERNAME/investment-research-assistant

Key Documentation:
- PROJECT_SUBMISSION.md - Complete project documentation
- README.md - Quick start guide
- 30+ additional markdown files documenting features and iterations

The repository contains a fully functional multi-agent system with:
- Python backend (Flask API)
- React frontend
- 10+ API integrations
- Parallel execution (2-3x performance improvement)
- Comprehensive documentation
```

---

**Once you upload and get your link, just tell me the URL and I'll update all the documentation files for you!**
