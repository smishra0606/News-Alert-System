"""
Database module for managing subscribers
Handles all database operations using SQLite
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Optional, Tuple

class Database:
    def __init__(self, db_path: str = 'data/subscribers.db'):
        """Initialize database connection"""
        self.db_path = db_path
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.Connection(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create subscribers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )
        ''')

        # Create index on email for faster lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_email 
            ON subscribers(email)
        ''')

        conn.commit()
        conn.close()
        print("✓ Database initialized successfully")

    def add_subscriber(self, email: str) -> Tuple[bool, str]:
        """
        Add a new subscriber
        Returns: (success: bool, message: str)
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                'INSERT INTO subscribers (email) VALUES (?)',
                (email.lower().strip(),)
            )

            conn.commit()
            conn.close()
            return True, "Successfully subscribed!"

        except sqlite3.IntegrityError:
            return False, "This email is already subscribed."
        except Exception as e:
            return False, f"Error adding subscriber: {str(e)}"

    def remove_subscriber(self, email: str) -> Tuple[bool, str]:
        """
        Remove a subscriber (soft delete by marking inactive)
        Returns: (success: bool, message: str)
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                'UPDATE subscribers SET is_active = 0 WHERE email = ?',
                (email.lower().strip(),)
            )

            if cursor.rowcount == 0:
                conn.close()
                return False, "Email not found in subscribers list."

            conn.commit()
            conn.close()
            return True, "Successfully unsubscribed!"

        except Exception as e:
            return False, f"Error removing subscriber: {str(e)}"

    def get_all_subscribers(self) -> List[str]:
        """Get all active subscriber emails"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                'SELECT email FROM subscribers WHERE is_active = 1'
            )

            emails = [row['email'] for row in cursor.fetchall()]
            conn.close()
            return emails

        except Exception as e:
            print(f"Error fetching subscribers: {str(e)}")
            return []

    def get_subscriber_count(self) -> int:
        """Get count of active subscribers"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                'SELECT COUNT(*) as count FROM subscribers WHERE is_active = 1'
            )

            count = cursor.fetchone()['count']
            conn.close()
            return count

        except Exception as e:
            print(f"Error getting subscriber count: {str(e)}")
            return 0

    def email_exists(self, email: str) -> bool:
        """Check if email exists in database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                'SELECT id FROM subscribers WHERE email = ? AND is_active = 1',
                (email.lower().strip(),)
            )

            exists = cursor.fetchone() is not None
            conn.close()
            return exists

        except Exception as e:
            print(f"Error checking email existence: {str(e)}")
            return False
