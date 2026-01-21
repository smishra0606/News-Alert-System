"""
Scheduler module for running periodic tasks
Handles automatic scraping and email notifications
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import os

class TaskScheduler:
    """Background task scheduler for automated operations"""

    def __init__(self, scraper, email_service, database):
        """
        Initialize scheduler with dependencies

        Args:
            scraper: NewsScraper instance
            email_service: EmailService instance
            database: Database instance
        """
        self.scraper = scraper
        self.email_service = email_service
        self.database = database
        self.scheduler = BackgroundScheduler()
        self.is_running = False

        # Get interval from environment or default to 10 minutes
        self.interval_minutes = int(os.getenv('SCRAPE_INTERVAL_MINUTES', 10))

    def scrape_and_notify(self):
        """
        Main task: Scrape websites and send notifications if new articles found
        """
        print(f"\n{'='*60}")
        print(f"🤖 Automated scrape started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")

        try:
            # Scrape all websites
            new_articles = self.scraper.scrape_all()

            if new_articles:
                print(f"\n📧 Sending notifications for {len(new_articles)} new articles...")

                # Get all subscribers
                subscribers = self.database.get_all_subscribers()

                if subscribers:
                    # Send email notifications
                    result = self.email_service.send_new_article_notification(
                        subscribers, 
                        new_articles
                    )

                    if result['success']:
                        print(f"✅ Notifications sent: {result['message']}")
                    else:
                        print(f"⚠️  Notification error: {result['message']}")
                else:
                    print("ℹ️  No subscribers to notify")
            else:
                print("ℹ️  No new articles to notify about")

        except Exception as e:
            print(f"❌ Error in scrape_and_notify task: {str(e)}")

        print(f"{'='*60}\n")

    def start(self):
        """Start the scheduler"""
        if not self.is_running:
            # Add the scraping job
            self.scheduler.add_job(
                func=self.scrape_and_notify,
                trigger=IntervalTrigger(minutes=self.interval_minutes),
                id='scrape_and_notify_job',
                name='Scrape websites and send notifications',
                replace_existing=True
            )

            self.scheduler.start()
            self.is_running = True

            print(f"✓ Scheduler started - will run every {self.interval_minutes} minutes")

            # Run immediately on startup
            #print("\n🚀 Running initial scrape...")
            #self.scrape_and_notify()
        else:
            print("⚠️  Scheduler is already running")

    def stop(self):
        """Stop the scheduler"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            print("✓ Scheduler stopped")

    def get_status(self) -> dict:
        """Get scheduler status"""
        jobs = self.scheduler.get_jobs()

        return {
            'is_running': self.is_running,
            'interval_minutes': self.interval_minutes,
            'active_jobs': len(jobs),
            'next_run': str(jobs[0].next_run_time) if jobs else None
        }
