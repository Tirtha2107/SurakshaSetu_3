

# import os
# import sqlite3

# # PROJECT ROOT (Surakshasetu folder)
# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# # Move up 1 level because db_config is inside pages/
# PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

# DB_DIR = os.path.join(PROJECT_ROOT, "database")
# os.makedirs(DB_DIR, exist_ok=True)

# DB_PATH = os.path.join(DB_DIR, "incidents.db")

# def get_connection():
#     return sqlite3.connect(DB_PATH)


import os
import sqlite3

# -------------------------------------------------
# PROJECT ROOT (SurakshaSetu folder)
# db_config.py is inside /pages/, so go up one level
# -------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database directory
DB_DIR = os.path.join(PROJECT_ROOT, "database")
os.makedirs(DB_DIR, exist_ok=True)

# Single shared database file
DB_PATH = os.path.join(DB_DIR, "suraksha_setu.db")


def get_connection():
    """Returns a SQLite database connection (thread-safe for Streamlit)."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    """Create required tables if they do not exist."""
    conn = get_connection()
    c = conn.cursor()

    # ---------------- USERS TABLE ----------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            age INTEGER,
            address TEXT,
            contact1 TEXT,
            contact2 TEXT,
            contact3 TEXT,
            contact4 TEXT,
            contact5 TEXT
        )
    """)

    # ---------------- FEEDBACK TABLE ----------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            user_type TEXT,
            usage TEXT,
            features TEXT,
            overall_rating INTEGER,
            design_rating INTEGER,
            speed_rating INTEGER,
            alert_accuracy INTEGER,
            liked TEXT,
            issues TEXT,
            suggestions TEXT,
            bug_reported TEXT,
            bug_description TEXT,
            bug_time TEXT,
            timestamp TEXT
        )
    """)

    # ---------------- INCIDENT TABLE (example) ----------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            description TEXT,
            location TEXT,
            image_path TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# Initialize DB & tables automatically
init_db()
