"""
Main Flask application
Entry point for the News Alert System
"""
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import atexit

# Load environment variables
load_dotenv()

from backend.database import Database
from backend.scraper import NewsScraper
from backend.email_service import EmailService
from backend.scheduler import TaskScheduler
from backend.routes.api import api_bp

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DATABASE_PATH'] = os.getenv('DATABASE_PATH', 'data/subscribers.db')

# Initialize components
print("\n🚀 Initializing News Alert System...")
print("="*60)

database = Database(app.config['DATABASE_PATH'])
scraper = NewsScraper()
email_service = EmailService()
scheduler = TaskScheduler(scraper, email_service, database)

# Store in app config for access in routes
app.config['database'] = database
app.config['scraper'] = scraper
app.config['email_service'] = email_service
app.config['scheduler'] = scheduler

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

# Serve frontend
@app.route('/')
def serve_index():
    """Serve the main page"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/success')
def serve_success():
    """Serve the success page"""
    return send_from_directory(app.static_folder, 'success.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory(app.static_folder, path)

# Start scheduler when app starts
@app.before_request
def start_scheduler():
    """Start the scheduler before first request"""
    if not scheduler.is_running:
        scheduler.start()

# Cleanup on shutdown
def shutdown_scheduler():
    """Stop scheduler on shutdown"""
    scheduler.stop()

atexit.register(shutdown_scheduler)

print("="*60)
print("✅ News Alert System initialized successfully!")
print("="*60)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
