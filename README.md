# 🎬 YouTube AI Automation 2026 - The AI Ledger

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/mcontentcreator71-web/youtube-automation-2026)
[![n8n](https://img.shields.io/badge/n8n-Workflow-orange)](https://n8n.io)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://python.org)

Comprehensive YouTube automation workflow for creating and uploading 3 videos daily (Shorts and Long-form) for a USA audience using n8n, Python, and AI.

## 🚀 Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/mcontentcreator71-web/youtube-automation-2026.git
   cd youtube-automation-2026
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up n8n**
   - Install n8n: `npm install -g n8n`
   - Start n8n: `n8n start`
   - Import `workflow.json` to n8n

4. **Configure credentials**
   - Add Google Gemini API key
   - Add YouTube OAuth credentials
   - Add Reddit API credentials

5. **Deploy to cloud** (optional)
   - See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for cloud deployment options

## 📋 Features

This workflow automates the entire YouTube content creation process:
1. **Data Scraping**: Reddit and news sites for trending AI news
2. **Content Generation**: Google Gemini API for scripts, titles, and descriptions
3. **Video Production**: Automated video creation with voiceover, visuals, and captions
4. **Scheduling & Upload**: Automated uploads at USA peak times (8 AM, 12 PM, 6 PM EST)

## 📁 File Structure

```
.
├── README.md                 # This file
├── requirements.txt         # Python dependencies
├── video_production.py      # Video production script
├── run_video_production.py  # Wrapper script for n8n
├── youtube_upload.py       # YouTube upload script
├── workflow.json            # n8n workflow configuration
├── Dockerfile               # Docker configuration for deployment
└── .gitignore               # Git ignore rules
```

## 🔧 Workflow Components

### 1. Data Scraping & Research
- **Reddit Scraping**: Gets trending posts from AI subreddits
- **News Site Scraping**: Fetches from multiple AI news sources
- **24-Hour Filter**: Only processes news from last 24 hours

### 2. Content Generation
- **Google Gemini**: Generates titles, descriptions, scripts, and image prompts

### 3. Video Production
- **Voiceover**: Google Text-to-Speech (gTTS)
- **Visuals**: MoviePy for video composition
- **Captions**: OpenAI Whisper for automatic transcription

### 4. Upload & Scheduling
- **YouTube Upload**: Automated via YouTube Data API v3
- **Scheduling**: Uploads scheduled for USA peak times

## 📝 License

This project is for personal use. Ensure compliance with:
- YouTube Terms of Service
- Reddit API Terms
- Google API Terms
- Copyright laws for content usage

---

**Channel**: The AI Ledger  
**Automation**: 3 videos daily (Shorts + Long-form)  
**Target Audience**: USA  
**Last Updated**: 2026
