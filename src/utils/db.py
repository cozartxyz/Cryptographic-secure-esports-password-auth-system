import sqlite3

DB_PATH = "database/users.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            failed_attempts INTEGER DEFAULT 0,
            lockout_until DATETIME
        )
    ''')

    # Create login_logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            hashed_ip TEXT NOT NULL,
            timezone TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
