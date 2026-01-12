# 🚀 Complete Deployment Guide

This guide will walk you through deploying the News Alert System from scratch.

## Table of Contents

1. [Local Setup](#local-setup)
2. [Getting Resend API Key](#getting-resend-api-key)
3. [Testing Locally](#testing-locally)
4. [Deploying to Render](#deploying-to-render)
5. [Post-Deployment Checklist](#post-deployment-checklist)

---

## 1. Local Setup

### Step 1.1: Install Python

**Windows:**
1. Download Python from https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"
5. Verify: Open CMD and type `python --version`

**Mac:**
```bash
# Using Homebrew
brew install python3

# Verify
python3 --version
```

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Step 1.2: Download Project

**Option A - Download ZIP:**
1. Download project ZIP file
2. Extract to desired location
3. Open terminal/command prompt in that folder

**Option B - Git Clone:**
```bash
git clone <repository-url>
cd news-alert-system
```

### Step 1.3: Create Virtual Environment

**Windows Command Prompt:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

✅ You'll see `(venv)` in your terminal prompt

### Step 1.4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- BeautifulSoup (web scraping)
- Resend (email service)
- APScheduler (background tasks)
- And other dependencies

---

## 2. Getting Resend API Key

### Step 2.1: Create Resend Account

1. Go to https://resend.com/
2. Click "Sign Up" or "Get Started"
3. Sign up with:
   - Email address
   - Or GitHub account
   - Or Google account

### Step 2.2: Verify Email

1. Check your email inbox
2. Click verification link
3. Complete account setup

### Step 2.3: Create API Key

1. After logging in, go to **API Keys** section
2. Click "**Create API Key**"
3. Settings:
   - **Name**: News Alert System
   - **Permission**: Full Access (or Send Only)
   - **Domain**: All domains (for testing)
4. Click "**Create**"
5. **IMPORTANT**: Copy the API key immediately
   - It starts with `re_`
   - Example: `re_123abc456def789ghi`
   - You can only see it once!

### Step 2.4: (Optional) Setup Verified Domain

**For Testing:**
- Use `onboarding@resend.dev` as sender
- No domain verification needed
- Limited to 100 emails/day

**For Production:**
1. Go to **Domains** section in Resend
2. Click "**Add Domain**"
3. Enter your domain (e.g., `yourdomain.com`)
4. Add DNS records shown by Resend:
   - SPF record
   - DKIM records
   - DMARC record (optional)
5. Wait for verification (can take 24-48 hours)
6. Use `noreply@yourdomain.com` as sender

### Step 2.5: Configure Environment Variables

1. **Copy example file:**
```bash
cp .env.example .env
```

2. **Edit `.env` file:**

**For Testing (Quick Start):**
```env
RESEND_API_KEY=re_your_actual_api_key_here
FROM_EMAIL=onboarding@resend.dev
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-later
SCRAPE_INTERVAL_MINUTES=10
```

**For Production:**
```env
RESEND_API_KEY=re_your_actual_api_key_here
FROM_EMAIL=noreply@yourdomain.com
FLASK_ENV=production
SECRET_KEY=generate-a-secure-random-key-here
SCRAPE_INTERVAL_MINUTES=10
```

**Generate Secure SECRET_KEY (Python):**
```python
import secrets
print(secrets.token_hex(32))
```

---

## 3. Testing Locally

### Step 3.1: Start the Application

**Make sure virtual environment is activated!**

```bash
python backend/app.py
```

You should see:
```
🚀 Initializing News Alert System...
============================================================
✓ Database initialized successfully
✓ Email service initialized
✓ Scheduler started - will run every 10 minutes

🚀 Running initial scrape...
🔍 Starting scrape of 60 websites...
  Scraping: Ericsson Customer Cases...
  Scraping: Nokia Case Studies...
  ...
```

### Step 3.2: Access the Web Interface

Open browser: http://localhost:5000

You should see:
- 📡 Telecom Industry News Alerts header
- Features section
- Subscription form

### Step 3.3: Test Subscription

1. Enter your email address
2. Click "Subscribe"
3. Check for success message
4. You should be redirected to success page

### Step 3.4: Verify Database

**Check subscriber was added:**
```bash
# Windows
sqlite3 data/subscribers.db "SELECT * FROM subscribers;"

# Or using Python
python
>>> from backend.database import Database
>>> db = Database()
>>> print(db.get_all_subscribers())
['your@email.com']
>>> exit()
```

### Step 3.5: Test Email Notification

**Option A - Wait for scheduled scrape:**
- Wait 10 minutes
- New articles will trigger emails
- Check your inbox

**Option B - Manual trigger:**
```bash
curl -X POST http://localhost:5000/api/trigger-scrape
```

Or open another terminal and use Python:
```python
from backend.scheduler import TaskScheduler
from backend.scraper import NewsScraper
from backend.email_service import EmailService
from backend.database import Database

db = Database()
scraper = NewsScraper()
email_service = EmailService()
scheduler = TaskScheduler(scraper, email_service, db)

scheduler.scrape_and_notify()
```

### Step 3.6: Check Logs

Monitor the console output for:
- ✅ Scraping progress
- ✅ New articles found
- ✅ Email sending status
- ❌ Any errors

---

## 4. Deploying to Render

### Step 4.1: Prepare for Deployment

**Create `.gitignore` file (already included):**
```
.env
__pycache__/
*.db
venv/
```

**Commit your code:**
```bash
git init
git add .
git commit -m "Initial commit - News Alert System"
```

### Step 4.2: Push to GitHub

1. **Create GitHub repository:**
   - Go to https://github.com/
   - Click "New repository"
   - Name: `news-alert-system`
   - Make it public or private
   - Don't initialize with README (we have one)

2. **Push code:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/news-alert-system.git
git branch -M main
git push -u origin main
```

### Step 4.3: Create Render Account

1. Go to https://render.com/
2. Click "**Get Started**" or "**Sign Up**"
3. Sign up with GitHub (recommended)
4. Authorize Render to access your GitHub

### Step 4.4: Create New Web Service

1. Click "**New +**" button (top right)
2. Select "**Web Service**"
3. Choose your repository:
   - Search for `news-alert-system`
   - Click "**Connect**"

### Step 4.5: Configure Service

**Basic Settings:**
- **Name**: `news-alert-system` (or your preferred name)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Runtime**: `Python 3`

**Build Settings:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn backend.app:app --bind 0.0.0.0:$PORT --timeout 120`

**Instance Type:**
- Select "**Free**" (for testing)
- Or "**Starter**" for better performance

### Step 4.6: Add Environment Variables

Click "**Advanced**" → "**Add Environment Variable**"

Add these one by one:

| Key | Value |
|-----|-------|
| `RESEND_API_KEY` | `re_your_actual_key_here` |
| `FROM_EMAIL` | `onboarding@resend.dev` or `noreply@yourdomain.com` |
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | Your secure random key |
| `SCRAPE_INTERVAL_MINUTES` | `10` |
| `DATABASE_PATH` | `data/subscribers.db` |

### Step 4.7: Create Service

1. Click "**Create Web Service**"
2. Wait for deployment (3-5 minutes)
3. Watch the build logs

**Successful deployment shows:**
```
==> Building...
Installing dependencies...
==> Deploying...
==> Your service is live 🎉
```

### Step 4.8: Get Your URL

After deployment:
- You'll get a URL like: `https://news-alert-system.onrender.com`
- Click to open your live application!

---

## 5. Post-Deployment Checklist

### ✅ Verify Deployment

**Check homepage:**
```bash
curl https://your-app.onrender.com/
```

**Check health endpoint:**
```bash
curl https://your-app.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "News Alert System is running"
}
```

**Check stats:**
```bash
curl https://your-app.onrender.com/api/stats
```

### ✅ Test Subscription

1. Open `https://your-app.onrender.com`
2. Subscribe with your email
3. Check for success page
4. Verify email received

### ✅ Monitor Logs

In Render dashboard:
1. Click your service
2. Go to "**Logs**" tab
3. Watch for:
   - Scraping activity
   - Email sending
   - Errors (if any)

### ✅ Configure Custom Domain (Optional)

1. In Render dashboard → "**Settings**"
2. Scroll to "**Custom Domain**"
3. Click "**Add Custom Domain**"
4. Enter your domain
5. Add CNAME record to DNS:
   - Host: `www` or `news`
   - Value: `your-app.onrender.com`
6. Wait for DNS propagation (15 minutes - 48 hours)

### ✅ Set Up Monitoring

**Uptime Monitoring:**
1. Use Render's built-in health checks
2. Or use external: https://uptimerobot.com/
3. Monitor: `https://your-app.onrender.com/api/health`

**Email Monitoring:**
1. Check Resend dashboard regularly
2. Monitor bounce rates
3. Check for blocked emails

---

## 🐛 Common Issues and Solutions

### Issue: Build fails on Render

**Solution:**
1. Check `requirements.txt` is correct
2. Verify Python version compatibility
3. Check build logs for specific error
4. Ensure all dependencies are listed

### Issue: Application starts but crashes

**Solution:**
1. Check all environment variables are set
2. Verify Resend API key is correct
3. Check logs for Python errors
4. Ensure Procfile is correct

### Issue: Emails not sending

**Solution:**
1. Verify Resend API key in Render environment variables
2. Check FROM_EMAIL is correct
3. For production, verify domain in Resend
4. Check Resend dashboard for errors
5. Verify you haven't exceeded rate limits

### Issue: Scheduler not running

**Solution:**
1. Check logs for scheduler errors
2. Verify `SCRAPE_INTERVAL_MINUTES` is set
3. Ensure application has enough memory
4. Check if free tier has limitations

### Issue: Database errors

**Solution:**
1. Ensure `data/` directory is created
2. Check write permissions
3. On Render, database resets on each deploy (use persistent disk for production)
4. Consider upgrading to paid plan for persistent storage

---

## 📊 Monitoring Your Deployment

### Daily Checks

1. **Open Logs:**
   - Render Dashboard → Your Service → Logs
   - Look for errors or warnings

2. **Check Stats:**
```bash
curl https://your-app.onrender.com/api/stats
```

3. **Verify Scraping:**
   - Check scraper cache size growing
   - Verify new articles being detected

### Weekly Checks

1. **Review Resend Dashboard:**
   - Check email delivery rates
   - Monitor bounce rates
   - Check for blocked emails

2. **Database Backup:**
```bash
# Download database from Render
render ssh
cd data
cat subscribers.db > backup.db
exit
```

3. **Update Dependencies:**
```bash
pip list --outdated
```

---

## 🎉 Success!

Your News Alert System is now:
- ✅ Running 24/7 on Render
- ✅ Monitoring 60+ telecom news sources
- ✅ Sending automatic email notifications
- ✅ Accessible from anywhere in the world

**Next Steps:**
1. Share your URL with users
2. Monitor logs for first few days
3. Collect feedback
4. Add more features!

---

## 🆘 Need Help?

1. Check **README.md** for detailed documentation
2. Review Render documentation: https://render.com/docs
3. Check Resend documentation: https://resend.com/docs
4. Review application logs for errors

---

**Happy Deploying! 🚀**
