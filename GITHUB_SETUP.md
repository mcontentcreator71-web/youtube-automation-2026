# 🚀 GitHub Repository Setup Guide

This guide will help you create a GitHub repository and push your YouTube automation workflow files.

## 📋 Step 1: Export Your n8n Workflow

Before pushing to GitHub, you need to export your n8n workflow:

### Option A: Export from n8n UI

1. **Open your n8n instance**
   - Go to `http://localhost:5678` (or your n8n URL)
   - Login to n8n

2. **Open your workflow**
   - Click on "Workflows" in the left sidebar
   - Find "Youtube AI Automation 2026"
   - Click to open it

3. **Export the workflow**
   - Click the **three dots (⋮)** menu in the top right
   - Select **"Download"** or **"Export"**
   - Save the file as `workflow.json` in your project folder

### Option B: Export via API

If you know your workflow ID, you can export it via API:

```bash
# Replace WORKFLOW_ID with your actual workflow ID
curl http://localhost:5678/api/v1/workflows/WORKFLOW_ID > workflow.json
```

**Your workflow ID is:** `wqQWoDqXHaEHJ0dU` (from previous setup)

---

## 📋 Step 2: Create GitHub Repository

### Method 1: Using GitHub Website (Easiest)

1. **Go to GitHub**
   - Visit [github.com](https://github.com)
   - Sign in to your account: [mcontentcreator71-web](https://github.com/mcontentcreator71-web)

2. **Create New Repository**
   - Click the **"+"** icon in the top right
   - Select **"New repository"**
   - Repository name: `youtube-automation-2026`
   - Description: `Automated YouTube video creation and upload workflow using n8n`
   - Choose **Public** or **Private** (your choice)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
   - Click **"Create repository"**

3. **Copy the repository URL**
   - You'll see a page with setup instructions
   - Copy the repository URL (e.g., `https://github.com/mcontentcreator71-web/youtube-automation-2026.git`)

### Method 2: Using GitHub CLI (Advanced)

```bash
# Install GitHub CLI first: https://cli.github.com/
gh repo create youtube-automation-2026 --public --description "Automated YouTube video creation and upload workflow"
```

---

## 📋 Step 3: Initialize Git and Push Files

### Open PowerShell in your project folder:

```powershell
# Navigate to your project folder
cd "G:\Youtube Automation for 2026"

# Initialize Git repository
git init

# Add all files (except those in .gitignore)
git add .

# Create first commit
git commit -m "Initial commit: YouTube automation workflow with n8n"

# Add remote repository (replace with your actual repo URL)
git remote add origin https://github.com/mcontentcreator71-web/youtube-automation-2026.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### If you get authentication errors:

**Option 1: Use Personal Access Token**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` scope
3. Use token as password when pushing

**Option 2: Use GitHub Desktop**
- Download [GitHub Desktop](https://desktop.github.com/)
- Add repository
- Commit and push via GUI

---

## 📋 Step 4: Verify Upload

1. Go to your repository: `https://github.com/mcontentcreator71-web/youtube-automation-2026`
2. Verify all files are there:
   - ✅ `video_production.py`
   - ✅ `run_video_production.py`
   - ✅ `youtube_upload.py`
   - ✅ `requirements.txt`
   - ✅ `Dockerfile`
   - ✅ `.gitignore`
   - ✅ `README.md`
   - ✅ `workflow.json` (if you exported it)

---

## 📋 Step 5: Deploy to Cloud Platform

Now that your code is on GitHub, you can deploy to any platform:

### Deploy to Cyclic.sh (Easiest - 2-3 minutes)

1. Go to [cyclic.sh](https://www.cyclic.sh)
2. Sign up with GitHub
3. Click "New App"
4. Select your repository: `youtube-automation-2026`
5. Cyclic will auto-detect and deploy
6. Add environment variables:
   - `N8N_BASIC_AUTH_ACTIVE=true`
   - `N8N_BASIC_AUTH_USER=admin`
   - `N8N_BASIC_AUTH_PASSWORD=yourpassword`
   - Add your API keys (YouTube, Gemini, etc.)
7. Deploy!

### Deploy to Fly.io (Most Resources)

1. Go to [fly.io](https://fly.io)
2. Sign up
3. Install CLI:
   ```powershell
   iwr https://fly.io/install.ps1 -useb | iex
   ```
4. Login:
   ```bash
   fly auth login
   ```
5. Launch:
   ```bash
   fly launch
   ```
6. Follow prompts and deploy!

### Deploy to Render.com

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your repository
5. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `n8n start`
6. Add environment variables
7. Deploy!

---

## 🔒 Important: Security Notes

### Never commit these files:
- ❌ `client_secrets.json` (Google OAuth credentials)
- ❌ `youtube_credentials.pickle` (YouTube tokens)
- ❌ `.env` files (API keys)
- ❌ `venv/` folder (Python virtual environment)
- ❌ Video files (`videos/` folder)

These are already in `.gitignore` and won't be uploaded.

### Use Environment Variables:
Store all sensitive data as environment variables in your cloud platform:
- Google Gemini API key
- YouTube OAuth credentials
- Reddit API credentials
- Any other API keys

---

## ✅ Checklist

Before deploying, make sure:

- [ ] Workflow exported from n8n as `workflow.json`
- [ ] GitHub repository created
- [ ] All files committed and pushed
- [ ] `.gitignore` is working (no sensitive files uploaded)
- [ ] Environment variables ready for cloud platform
- [ ] Cloud platform account created (Cyclic/Fly.io/Render)

---

## 🎯 Next Steps

1. **Export workflow** from n8n → `workflow.json`
2. **Create GitHub repo** → `youtube-automation-2026`
3. **Push files** to GitHub
4. **Deploy** to cloud platform (Cyclic/Fly.io/Render)
5. **Import workflow** in cloud n8n instance
6. **Configure credentials** in cloud n8n
7. **Activate workflow** → Runs 24/7!

---

## 📞 Need Help?

If you encounter issues:

1. **Git errors**: Check [GitHub Docs](https://docs.github.com/)
2. **Deployment errors**: Check platform documentation
3. **Workflow errors**: Check n8n execution logs

**You're all set!** 🚀
