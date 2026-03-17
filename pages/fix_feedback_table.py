import sqlite3
from db_config import get_connection

conn = get_connection()
cursor = conn.cursor()

# Add missing columns safely
columns = [
    "name TEXT",
    "email TEXT",
    "user_type TEXT",
    "usage TEXT",
    "features TEXT",
    "overall_rating INTEGER",
    "design_rating INTEGER",
    "speed_rating INTEGER",
    "alert_accuracy INTEGER",
    "liked TEXT",
    "issues TEXT",
    "suggestions TEXT",
    "bug_reported TEXT",
    "bug_description TEXT",
    "bug_time TEXT",
    "timestamp TEXT"
]

for col in columns:
    try:
        cursor.execute(f"ALTER TABLE feedback ADD COLUMN {col}")
    except sqlite3.OperationalError:
        pass  # column already exists

conn.commit()
conn.close()

print("✅ feedback table fixed successfully")
