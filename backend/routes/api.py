"""
API routes for the application
Handles subscription, unsubscription, and health checks
"""
from flask import Blueprint, request, jsonify, current_app
import re

# Create blueprint
api_bp = Blueprint('api', __name__)

# Email validation regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

def validate_email(email: str) -> bool:
    """Validate email format"""
    return bool(EMAIL_REGEX.match(email))

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'News Alert System is running'
    }), 200

@api_bp.route('/subscribe', methods=['POST'])
def subscribe():
    """
    Subscribe a new email address
    Expects JSON: { "email": "user@example.com" }
    """
    try:
        data = request.get_json()

        if not data or 'email' not in data:
            return jsonify({
                'success': False,
                'message': 'Email is required'
            }), 400

        email = data['email'].strip()

        # Validate email format
        if not validate_email(email):
            return jsonify({
                'success': False,
                'message': 'Invalid email format'
            }), 400

        # Get database from app context
        db = current_app.config['database']

        # Add subscriber
        success, message = db.add_subscriber(email)

        if success:
            subscriber_count = db.get_subscriber_count()
            return jsonify({
                'success': True,
                'message': message,
                'subscriber_count': subscriber_count
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@api_bp.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    """
    Unsubscribe an email address
    Expects JSON: { "email": "user@example.com" }
    """
    try:
        data = request.get_json()

        if not data or 'email' not in data:
            return jsonify({
                'success': False,
                'message': 'Email is required'
            }), 400

        email = data['email'].strip()

        # Validate email format
        if not validate_email(email):
            return jsonify({
                'success': False,
                'message': 'Invalid email format'
            }), 400

        # Get database from app context
        db = current_app.config['database']

        # Remove subscriber
        success, message = db.remove_subscriber(email)

        if success:
            return jsonify({
                'success': True,
                'message': message
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        db = current_app.config['database']
        scraper = current_app.config['scraper']
        scheduler = current_app.config['scheduler']

        return jsonify({
            'subscribers': db.get_subscriber_count(),
            'cached_articles': scraper.get_cache_stats(),
            'scheduler': scheduler.get_status()
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@api_bp.route('/trigger-scrape', methods=['POST'])
def trigger_scrape():
    """Manually trigger a scrape (for testing)"""
    try:
        scheduler = current_app.config['scheduler']
        scheduler.scrape_and_notify()

        return jsonify({
            'success': True,
            'message': 'Scrape triggered successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500
