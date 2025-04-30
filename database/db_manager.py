import sqlite3
import os
from config import DB_PATH

def init_db():
    """Initialize the database with all required tables."""
    # Ensure directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE NOT NULL,
            username TEXT,
            last_interaction TIMESTAMP
        )
    ''')
    
    # Create interactions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            interaction_type TEXT NOT NULL,
            timestamp TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    
    print(f"Database initialized at {DB_PATH}")

def add_user(user_id, username):
    """Adds a new user or updates existing user info."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Check if user exists
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()
    
    if user:
        # Update existing user
        c.execute('''
            UPDATE users SET username = ? WHERE user_id = ?
        ''', (username, user_id))
    else:
        # Add new user
        c.execute('''
            INSERT INTO users (user_id, username, last_interaction)
            VALUES (?, ?, datetime('now'))
        ''', (user_id, username))
    
    conn.commit()
    conn.close()

async def get_user(user_id):
    """Gets a user by ID."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT * FROM users WHERE user_id = ?
    ''', (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def update_last_interaction(user_id):
    """Updates a user's last interaction timestamp."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Check if user exists first
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()
    
    if user:
        c.execute('''
            UPDATE users SET last_interaction = datetime('now') WHERE user_id = ?
        ''', (user_id,))
        conn.commit()
    conn.close()

def log_interaction(user_id, interaction_type):
    """Logs a user interaction."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO interactions (user_id, interaction_type, timestamp)
        VALUES (?, ?, datetime('now'))
    ''', (user_id, interaction_type))
    conn.commit()
    conn.close()

async def get_all_users():
    """Gets all users ordered by last interaction."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    c = conn.cursor()
    c.execute('''
        SELECT user_id, username FROM users ORDER BY last_interaction DESC
    ''')
    users = [(row['user_id'], row['username']) for row in c.fetchall()]
    conn.close()
    return users

async def get_user_interactions(user_id, limit=10):
    """Gets a user's recent interactions."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
        SELECT interaction_type, timestamp FROM interactions 
        WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?
    ''', (user_id, limit))
    interactions = [(row['interaction_type'], row['timestamp']) for row in c.fetchall()]
    conn.close()
    return interactions