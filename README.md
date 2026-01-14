# 📡 News Monitoring and Email Alert System

A production-ready web application that automatically monitors 60+ telecom industry news sources and sends email notifications to subscribers when new articles are published.

## 🌟 Features

- **Automated Monitoring**: Scrapes 60+ news sources from major telecom companies
- **Email Notifications**: Sends instant alerts via Resend API
- **Clean Web Interface**: Simple subscription management
- **Background Scheduler**: Automatic scraping every 10 minutes
- **Production Ready**: Fully deployable on cloud platforms
- **Secure**: No password storage, API-based email service

## 🏢 Monitored Companies (35+)

Ericsson, Nokia, Huawei, Cisco, Samsung, ZTE, Motorola, Ciena, CommScope, Juniper, HPE, ADTRAN, Lumentum, Extreme Networks, Viavi, NETGEAR, Ubiquiti, Tejas Networks, Fujitsu, Radisys, ALE, HFCL, STL, Matrix, Paramount Cables, Comba, and many more...

## 📋 Prerequisites

- Python 3.8 or higher
- Resend API account (free tier available)
- Git (for deployment)

## 🚀 Quick Start - Local Development

### Step 1: Clone or Download the Project

```bash
cd news-alert-system
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Resend API key:
```env
RESEND_API_KEY=re_your_actual_api_key_here
FROM_EMAIL=noreply@yourdomain.com
```

**How to get Resend API Key:**
1. Go to https://resend.com/
2. Sign up for free account
3. Navigate to API Keys section
4. Create new API key
5. Copy and paste into `.env`

**Setting up verified domain (Optional for production):**
- For testing, use `onboarding@resend.dev` as FROM_EMAIL
- For production, add and verify your domain in Resend dashboard

### Step 5: Run the Application

```bash
python backend/app.py
```

The application will:
- ✅ Initialize database
- ✅ Start Flask server on http://localhost:5000
- ✅ Start background scheduler
- ✅ Perform initial scrape

### Step 6: Test the System

1. Open browser: http://localhost:5000
2. Enter your email and subscribe
3. Check console logs for scraping activity
4. Wait for new articles to be detected

## 🗂️ Project Structure

```
news-alert-system/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── database.py            # SQLite database management
│   ├── scraper.py             # Web scraping logic
│   ├── email_service.py       # Email sending (Resend API)
│   ├── scheduler.py           # Background task scheduler
│   └── routes/
│       ├── __init__.py
│       └── api.py             # API endpoints
├── frontend/
│   ├── index.html             # Main page
│   ├── success.html           # Success page
│   ├── style.css              # Styling
│   └── script.js              # Frontend logic
├── data/
│   ├── subscribers.db         # SQLite database (auto-created)
│   └── scraper_cache.json     # Article cache (auto-created)
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── Procfile                   # Deployment configuration
└── README.md                  # This file
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/subscribe` | POST | Subscribe email |
| `/api/unsubscribe` | POST | Unsubscribe email |
| `/api/stats` | GET | System statistics |
| `/api/trigger-scrape` | POST | Manual scrape trigger |

### Example API Usage

**Subscribe:**
```bash
curl -X POST http://localhost:5000/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}'
```

**Unsubscribe:**
```bash
curl -X POST http://localhost:5000/api/unsubscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}'
```

**Check Stats:**
```bash
curl http://localhost:5000/api/stats
```

## 🌐 Deployment to Render

### Option 1: Deploy from GitHub

1. **Push to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/news-alert-system.git
git push -u origin main
```

2. **Create Render Account:**
   - Go to https://render.com/
   - Sign up for free account

3. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: news-alert-system
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn backend.app:app`

4. **Add Environment Variables:**
   - Go to "Environment" tab
   - Add:
     ```
     RESEND_API_KEY=re_your_key_here
     FROM_EMAIL=noreply@yourdomain.com
     FLASK_ENV=production
     SECRET_KEY=your-random-secret-key
     SCRAPE_INTERVAL_MINUTES=10
     ```

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Access your app at: `https://your-app-name.onrender.com`

### Option 2: Deploy without GitHub

1. Install Render CLI
2. Run: `render deploy`
3. Follow prompts

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `RESEND_API_KEY` | Resend API key (required) | - |
| `FROM_EMAIL` | Sender email address | noreply@yourdomain.com |
| `FLASK_ENV` | Environment (development/production) | production |
| `SECRET_KEY` | Flask secret key | auto-generated |
| `DATABASE_PATH` | Database file path | data/subscribers.db |
| `SCRAPE_INTERVAL_MINUTES` | Scraping frequency | 10 |
| `PORT` | Server port | 5000 |

### Changing Scrape Interval

Edit `.env`:
```env
SCRAPE_INTERVAL_MINUTES=5  # Check every 5 minutes
```

### Adding More Websites

Edit `backend/scraper.py` → `NewsScraperConfig.WEBSITES`:
```python
["Company Name", "https://example.com/news", "news"],
```

## 🧪 Testing

### Test Email Service
```python
from backend.email_service import EmailService
from backend.database import Database

email_service = EmailService()
result = email_service.send_test_email("your@email.com")
print(result)
```

### Test Scraper
```python
from backend.scraper import NewsScraper

scraper = NewsScraper()
articles = scraper.scrape_all()
print(f"Found {len(articles)} new articles")
```

### Manual Trigger Scrape
```bash
curl -X POST http://localhost:5000/api/trigger-scrape
```

## 🔒 Security Best Practices

✅ **Implemented:**
- Email validation with regex
- Duplicate email prevention
- API key in environment variables
- Input sanitization
- CORS protection
- SQL injection prevention (parameterized queries)

⚠️ **For Production:**
- Use HTTPS (Render provides this automatically)
- Set strong SECRET_KEY
- Verify your domain in Resend
- Monitor rate limits
- Add rate limiting middleware (optional)

## 📊 How Article Detection Works

1. **Initial Scrape**: On first run, scrapes all websites and caches results
2. **Cache Storage**: Each article gets unique ID (MD5 hash of title + URL)
3. **Subsequent Scrapes**: Compares new results with cache
4. **New Article Detection**: If article ID not in cache → NEW
5. **Notification**: Sends email to all subscribers
6. **Cache Update**: Adds new articles to cache

**Cache File Location**: `data/scraper_cache.json`

## 🐛 Troubleshooting

### Error: "RESEND_API_KEY not found"
- Make sure `.env` file exists
- Check API key is correct
- Restart the application

### Error: "Database locked"
- Close all connections to database
- Delete `data/subscribers.db` and restart

### No emails being sent
- Check Resend dashboard for errors
- Verify API key is active
- Check FROM_EMAIL is verified domain or use `onboarding@resend.dev`

### Scraper finds no articles
- Check website is accessible
- Some sites may block scrapers (add delays or headers)
- Verify website structure hasn't changed

### Application crashes on Render
- Check build logs
- Verify all environment variables are set
- Ensure Procfile is correct

## 📈 Monitoring and Maintenance

### Check System Stats
```bash
curl http://localhost:5000/api/stats
```

Response:
```json
{
  "subscribers": 25,
  "cached_articles": {
    "total_articles": 150,
    "last_updated": "2026-03-12T10:30:00"
  },
  "scheduler": {
    "is_running": true,
    "interval_minutes": 10,
    "active_jobs": 1,
    "next_run": "2026-03-12 10:40:00"
  }
}
```

### View Logs (Local)
- Console output shows all scraping activity
- Check for errors in red

### View Logs (Render)
- Go to your service dashboard
- Click "Logs" tab
- Filter by severity

## 📧 Support

For issues or questions:
1. Check troubleshooting section
2. Review logs for errors
3. Verify all environment variables
4. Test with simple endpoints first

## 🙏 Acknowledgments

- **Resend** - Email API service
- **Flask** - Web framework
- **BeautifulSoup** - Web scraping
- **APScheduler** - Background tasks

---

