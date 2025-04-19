# Database.py
import sqlite3
import hashlib
from datetime import datetime

# Initialize database
def init_db():
    conn = sqlite3.connect('summarizer.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         username TEXT UNIQUE NOT NULL,
         password TEXT NOT NULL,
         email TEXT)
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS summaries
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         user_id INTEGER,
         original_text TEXT,
         summary TEXT,
         timestamp DATETIME,
         source_type TEXT,
         FOREIGN KEY (user_id) REFERENCES users (id))
    ''')
    conn.commit()
    conn.close()

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Verify user
def verify_user(username, password):
    conn = sqlite3.connect('summarizer.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", 
              (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result is not None

# Register user
def register_user(username, password, email):
    conn = sqlite3.connect('summarizer.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                  (username, hash_password(password), email))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

# Get user id
def get_user_id(username):
    conn = sqlite3.connect('summarizer.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

# Save summary
def save_summary(user_id, original_text, summary, source_type='text'):
    conn = sqlite3.connect('summarizer.db')
    c = conn.cursor()
    c.execute("""
        INSERT INTO summaries (user_id, original_text, summary, timestamp, source_type)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, original_text, summary, datetime.now(), source_type))
    conn.commit()
    conn.close()

# Get user history
def get_user_history(user_id):
    conn = sqlite3.connect('summarizer.db')
    c = conn.cursor()
    c.execute("""
        SELECT original_text, summary, timestamp
        FROM summaries
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, (user_id,))
    results = c.fetchall()
    conn.close()
    return results

# Update password
def update_password(username, new_password):
    conn = sqlite3.connect('summarizer.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE users SET password=? WHERE username=?",
                  (hash_password(new_password), username))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

# Initialize database when module is imported
init_db()