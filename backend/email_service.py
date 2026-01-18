"""
Email service module using Resend API
Sends notification emails to subscribers
"""
import os
from typing import List, Dict
import resend

class EmailService:
    """Email service for sending notifications using Resend API"""

    def __init__(self):
        """Initialize email service with API key"""
        self.api_key = os.getenv('RESEND_API_KEY')
        self.from_email = os.getenv('FROM_EMAIL', 'noreply@yourdomain.com')

        if not self.api_key:
            print("⚠️  WARNING: RESEND_API_KEY not found in environment variables")
        else:
            resend.api_key = self.api_key
            print("✓ Email service initialized")

    def send_new_article_notification(self, 
                                     subscribers: List[str], 
                                     articles: List[Dict]) -> Dict:
        """
        Send email notification about new articles to all subscribers

        Args:
            subscribers: List of email addresses
            articles: List of article dictionaries with title, url, source, category

        Returns:
            Dictionary with success status and message
        """
        if not self.api_key:
            return {
                'success': False,
                'message': 'Email service not configured (missing API key)',
                'sent_count': 0
            }

        if not subscribers:
            return {
                'success': False,
                'message': 'No subscribers to send to',
                'sent_count': 0
            }

        if not articles:
            return {
                'success': False,
                'message': 'No articles to send',
                'sent_count': 0
            }

        # Build email content
        subject = self._build_subject(articles)
        html_content = self._build_html_email(articles)
        text_content = self._build_text_email(articles)

        # Send emails
        sent_count = 0
        failed_count = 0

        for email in subscribers:
            try:
                params = {
                    "from": self.from_email,
                    "to": [email],
                    "subject": subject,
                    "html": html_content,
                    "text": text_content
                }

                response = resend.Emails.send(params)
                sent_count += 1
                print(f"  ✓ Email sent to {email}")

            except Exception as e:
                failed_count += 1
                print(f"  ✗ Failed to send email to {email}: {str(e)}")

        return {
            'success': sent_count > 0,
            'message': f'Sent to {sent_count} subscribers, {failed_count} failed',
            'sent_count': sent_count,
            'failed_count': failed_count
        }

    def _build_subject(self, articles: List[Dict]) -> str:
        """Build email subject line"""
        count = len(articles)
        if count == 1:
            return f"New Article: {articles[0]['title'][:50]}"
        else:
            return f"{count} New Telecom Industry Updates"

    def _build_html_email(self, articles: List[Dict]) -> str:
        """Build HTML email content"""
        articles_html = ""

        # Group articles by category
        categories = {}
        for article in articles:
            cat = article.get('category', 'other')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(article)

        # Category labels
        category_labels = {
            'news': '📰 News',
            'blog': '✍️ Blog Posts',
            'case_study': '📊 Case Studies'
        }

        for category, items in categories.items():
            label = category_labels.get(category, category.title())
            articles_html += f"<h3 style='color: #0066cc; margin-top: 25px;'>{label}</h3>"

            for article in items:
                articles_html += f"""
                <div style="margin-bottom: 20px; padding: 15px; background-color: #f9f9f9; border-left: 4px solid #0066cc;">
                    <h4 style="margin: 0 0 8px 0;">
                        <a href="{article['url']}" style="color: #0066cc; text-decoration: none;">
                            {article['title']}
                        </a>
                    </h4>
                    <p style="margin: 0; color: #666; font-size: 14px;">
                        <strong>Source:</strong> {article['source']}
                    </p>
                </div>
                """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background-color: #0066cc; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0;">
                <h1 style="margin: 0;">📡 Telecom Industry Updates</h1>
            </div>

            <div style="background-color: white; padding: 30px; border: 1px solid #ddd; border-top: none;">
                <p style="font-size: 16px; color: #333;">
                    Hello! We've detected <strong>{len(articles)}</strong> new article(s) from the telecom industry:
                </p>

                {articles_html}

                <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">

                <p style="color: #666; font-size: 14px; text-align: center;">
                    You're receiving this email because you subscribed to telecom industry updates.<br>
                    <a href="#" style="color: #0066cc;">Unsubscribe</a>
                </p>
            </div>
        </body>
        </html>
        """

        return html

    def _build_text_email(self, articles: List[Dict]) -> str:
        """Build plain text email content"""
        text = f"TELECOM INDUSTRY UPDATES\n"
        text += f"{'='*50}\n\n"
        text += f"We've detected {len(articles)} new article(s):\n\n"

        # Group by category
        categories = {}
        for article in articles:
            cat = article.get('category', 'other')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(article)

        for category, items in categories.items():
            text += f"\n{category.upper().replace('_', ' ')}:\n"
            text += f"{'-'*50}\n"

            for i, article in enumerate(items, 1):
                text += f"\n{i}. {article['title']}\n"
                text += f"   Source: {article['source']}\n"
                text += f"   Link: {article['url']}\n"

        text += f"\n{'='*50}\n"
        text += f"You're receiving this because you subscribed to telecom updates.\n"

        return text

    def send_test_email(self, to_email: str) -> Dict:
        """Send a test email to verify configuration"""
        if not self.api_key:
            return {
                'success': False,
                'message': 'Email service not configured'
            }

        try:
            params = {
                "from": self.from_email,
                "to": [to_email],
                "subject": "Test Email - News Alert System",
                "html": "<h1>Test Email</h1><p>Your email service is configured correctly!</p>",
                "text": "Test Email - Your email service is configured correctly!"
            }

            response = resend.Emails.send(params)

            return {
                'success': True,
                'message': 'Test email sent successfully'
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to send test email: {str(e)}'
            }
