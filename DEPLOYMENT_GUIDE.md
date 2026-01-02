# 🚀 Deployment Guide - YouTube Automation 2026

Complete guide for deploying your YouTube automation workflow to cloud platforms.

## 📋 Prerequisites

- ✅ GitHub repository created (see `GITHUB_SETUP.md`)
- ✅ Workflow exported from n8n as `workflow.json`
- ✅ All files pushed to GitHub

---

## 🎯 Quick Deploy Options

### **1. Cyclic.sh (Easiest - 2-3 Minutes) ⭐⭐⭐⭐⭐**

**Why Choose:**
- ✅ Easiest setup
- ✅ One-click GitHub deploy
- ✅ Always-on
- ✅ Completely free
- ✅ No credit card needed

**Steps:**

1. **Sign Up**
   - Go to [cyclic.sh](https://www.cyclic.sh)
   - Click "Get Started"
   - Sign in with GitHub
   - Authorize Cyclic

2. **Create App**
   - Click "New App"
   - Select "GitHub" as source
   - Choose your repository: `youtube-automation-2026`
   - Click "Connect"

3. **Configure**
   - Cyclic auto-detects your app
   - Add environment variables:
     ```
     N8N_BASIC_AUTH_ACTIVE=true
     N8N_BASIC_AUTH_USER=admin
     N8N_BASIC_AUTH_PASSWORD=your_secure_password
     N8N_HOST=0.0.0.0
     N8N_PORT=5678
     ```
   - Add your API keys:
     ```
     GEMINI_API_KEY=your_gemini_key
     YOUTUBE_CLIENT_ID=your_youtube_client_id
     YOUTUBE_CLIENT_SECRET=your_youtube_secret
     REDDIT_CLIENT_ID=your_reddit_id
     REDDIT_CLIENT_SECRET=your_reddit_secret
     ```

4. **Deploy**
   - Click "Deploy" or "Create"
   - Wait 2-3 minutes
   - Get your URL: `your-app.cyclic.app`

5. **Import Workflow**
   - Access n8n at your URL
   - Login with Basic Auth (admin/your_password)
   - Import `workflow.json`
   - Configure credentials in n8n
   - Activate workflow

**Done!** 🎉

---

### **2. Fly.io (Most Resources - 10-15 Minutes) ⭐⭐⭐⭐⭐**

**Why Choose:**
- ✅ Most resources (3 VMs, 3GB storage)
- ✅ Always-on
- ✅ Docker support
- ✅ Very reliable
- ✅ Completely free

**Steps:**

1. **Sign Up**
   - Go to [fly.io](https://fly.io)
   - Sign up (free, no credit card)

2. **Install CLI**
   ```powershell
   # Windows PowerShell
   iwr https://fly.io/install.ps1 -useb | iex
   ```

3. **Login**
   ```bash
   fly auth login
   ```

4. **Launch App**
   ```bash
   cd "G:\Youtube Automation for 2026"
   fly launch
   ```
   - Follow prompts:
     - App name: `youtube-automation-2026` (or choose your own)
     - Region: Choose closest to you
     - PostgreSQL: No (unless you need it)
     - Redis: No (unless you need it)

5. **Configure Environment Variables**
   ```bash
   fly secrets set N8N_BASIC_AUTH_ACTIVE=true
   fly secrets set N8N_BASIC_AUTH_USER=admin
   fly secrets set N8N_BASIC_AUTH_PASSWORD=your_secure_password
   fly secrets set GEMINI_API_KEY=your_gemini_key
   # Add all other API keys
   ```

6. **Deploy**
   ```bash
   fly deploy
   ```

7. **Get URL**
   ```bash
   fly status
   ```
   - Access n8n at: `https://your-app.fly.dev`

8. **Import Workflow**
   - Access n8n
   - Import `workflow.json`
   - Configure credentials
   - Activate workflow

**Done!** 🎉

---

### **3. Render.com (Reliable & Easy - 5 Minutes) ⭐⭐⭐⭐**

**Why Choose:**
- ✅ Very reliable
- ✅ Easy setup
- ✅ One-click deploy
- ✅ Free tier available

**Steps:**

1. **Sign Up**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Verify email

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub
   - Select repository: `youtube-automation-2026`

3. **Configure**
   - **Name:** `youtube-automation-2026`
   - **Region:** Choose closest
   - **Branch:** `main`
   - **Root Directory:** Leave blank
   - **Runtime:** Docker (auto-detected from Dockerfile)
   - **Build Command:** (auto-detected)
   - **Start Command:** (auto-detected)

4. **Add Environment Variables**
   - Click "Advanced" → "Add Environment Variable"
   - Add all required variables (same as Cyclic)

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes
   - Get URL: `your-app.onrender.com`

6. **Import Workflow**
   - Access n8n
   - Import `workflow.json`
   - Configure credentials
   - Activate workflow

**Done!** 🎉

---

## 🔧 Post-Deployment Configuration

### 1. Import Workflow to Cloud n8n

1. Access your deployed n8n instance
2. Login with Basic Auth
3. Go to Workflows → Import from File
4. Upload `workflow.json`
5. Workflow imported!

### 2. Configure Credentials in n8n

1. **Google Gemini**
   - Go to Credentials → Add Credential
   - Select "Google Gemini Chat Model"
   - Enter API key
   - Save

2. **YouTube**
   - Go to Credentials → Add Credential
   - Select "YouTube OAuth2 API"
   - Enter Client ID and Secret
   - Authorize access

3. **Reddit**
   - Go to Credentials → Add Credential
   - Select "Reddit OAuth2 API"
   - Enter Client ID and Secret
   - Authorize access

### 3. Update Workflow Nodes

1. Open imported workflow
2. Update credential assignments:
   - "Generate Content with Gemini" → Assign Gemini credential
   - "Upload to YouTube" → Assign YouTube credential
   - Reddit nodes → Assign Reddit credential

### 4. Test Workflow

1. Click "Execute Workflow" (manual test)
2. Check execution logs
3. Verify video production works
4. Verify YouTube upload works

### 5. Activate Workflow

1. Toggle "Active" switch in workflow
2. Workflow now runs automatically on schedule!
3. Runs 3x daily (8 AM, 12 PM, 6 PM EST)

---

## 🔒 Security Best Practices

### Environment Variables

Store all sensitive data as environment variables:

```bash
# n8n Configuration
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=strong_password_here

# API Keys
GEMINI_API_KEY=your_key
YOUTUBE_CLIENT_ID=your_id
YOUTUBE_CLIENT_SECRET=your_secret
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
```

### Never Commit:
- ❌ API keys
- ❌ OAuth credentials
- ❌ Passwords
- ❌ Token files

---

## 📊 Monitoring

### Check Workflow Execution

1. **n8n Dashboard**
   - Go to Executions
   - View execution history
   - Check for errors

2. **Platform Logs**
   - Cyclic: Dashboard → Logs
   - Fly.io: `fly logs`
   - Render: Dashboard → Logs

3. **YouTube Channel**
   - Check for new uploads
   - Verify videos are public
   - Check video quality

---

## 🐛 Troubleshooting

### Workflow Not Running

1. Check if workflow is **Active**
2. Check schedule trigger configuration
3. Check execution logs for errors

### Video Production Fails

1. Check Python dependencies installed
2. Check FFmpeg available
3. Check file permissions
4. Check logs for specific errors

### YouTube Upload Fails

1. Verify OAuth credentials valid
2. Check API quota not exceeded
3. Verify video file exists
4. Check video format (MP4)

### API Errors

1. Verify API keys are correct
2. Check API quotas/limits
3. Verify credentials not expired
4. Check rate limits

---

## ✅ Deployment Checklist

- [ ] GitHub repository created and files pushed
- [ ] Workflow exported as `workflow.json`
- [ ] Cloud platform account created
- [ ] App deployed successfully
- [ ] Environment variables configured
- [ ] n8n accessible via URL
- [ ] Workflow imported to cloud n8n
- [ ] Credentials configured in n8n
- [ ] Workflow tested manually
- [ ] Workflow activated
- [ ] Monitoring set up

---

## 🎯 Next Steps

1. **Monitor First Execution**
   - Watch first scheduled run
   - Verify all steps work
   - Check YouTube for upload

2. **Optimize**
   - Fine-tune Gemini prompts
   - Adjust video quality
   - Optimize upload times

3. **Scale**
   - Add more content sources
   - Increase upload frequency
   - Add analytics tracking

---

**Your workflow is now running 24/7 in the cloud!** 🚀
