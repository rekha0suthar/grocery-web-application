import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_sqlalchemy import SQLAlchemy

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

def get_db_connection():
    """Get database connection"""
    try:
        if DATABASE_URL:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        else:
            # Fallback to local SQLite for development
            import sqlite3
            conn = sqlite3.connect('storedata.db')
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def get_cursor():
    """Get database cursor with dict-like access"""
    conn = get_db_connection()
    if conn:
        if DATABASE_URL:
            return conn.cursor(cursor_factory=RealDictCursor)
        else:
            # For SQLite, we'll use regular cursor
            return conn.cursor()
    return None

# Initialize SQLAlchemy
db = SQLAlchemy()
