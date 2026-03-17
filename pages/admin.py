import streamlit as st
import pandas as pd
import os
from pages.db_config import get_connection, DB_PATH

# st.set_page_config(page_title="SurakshaSetu | Admin", layout="wide")

# ---------------------------
# SURAKSHASETU THEME CSS
# ---------------------------
st.markdown("""
<style>
.stApp {
    background-color: #ffffff;
}
    #MainMenu, footer, header {visibility: hidden;}

    .top-banner {
        background:#F41C78;
        padding: 25px;
        border-radius: 16px;
        color: white;
        margin-bottom: 30px;
    }

    .top-banner h1 {
        font-size: 44px;
        margin: 0;
        font-weight: 800;
    }

    .top-banner p {
        font-size: 18px;
        margin-top: 6px;
        opacity: 0.95;
    }

    .section-title {
        font-size: 30px;
        font-weight: 700;
        color: #F41C78;
        margin-bottom: 10px;
    }

    button[kind="primary"] {
        background-color: #F41C78 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# TOP BANNER
# ---------------------------
st.markdown("""
<div class="top-banner">
    <h1>सुरक्षाSetu Admin Dashboard</h1>
    <p>Monitor incident reports & user feedback securely</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# PROJECT ROOT + DB PATH
# ---------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(PROJECT_ROOT, "database")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "incidents.db")

# ---------------------------
# OPEN DATABASE
# ---------------------------
conn = get_connection()
c = conn.cursor()

# ---------------------------
# ENSURE TABLE EXISTS
# ---------------------------
c.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        title TEXT,
        description TEXT,
        location TEXT,
        timestamp TEXT,
        status TEXT DEFAULT 'pending',
        file_path TEXT
    )
""")
conn.commit()

# ---------------------------
# FETCH PENDING REPORTS
# ---------------------------
try:
    df = pd.read_sql_query(
        "SELECT * FROM reports WHERE status='pending' ORDER BY id DESC",
        conn
    )
except Exception as e:
    st.error("❌ Database error: " + str(e))
    st.stop()

# ---------------------------
# INCIDENT REPORTS
# ---------------------------
st.markdown("<div class='section-title'>🚨 Pending Incident Reports</div>", unsafe_allow_html=True)

if df.empty:
    st.info("No pending reports.")
else:
    for _, row in df.iterrows():
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader(f"📌 {row['title']} (ID: {row['id']})")
        st.write(f"👩 **Name:** {row['name']}")
        st.write(f"📂 **Category:** {row['category']}")
        st.write(f"📝 **Description:** {row['description']}")
        st.write(f"📍 **Location:** {row['location']}")
        st.write(f"⏰ **Time:** {row['timestamp']}")
        st.write(f"📌 **Status:** {row['status']}")

        if row["file_path"]:
            full_path = os.path.join(PROJECT_ROOT, row["file_path"])
            if os.path.exists(full_path):
                if full_path.lower().endswith(("jpg", "jpeg", "png")):
                    st.image(full_path, width=320)
                else:
                    st.video(full_path)

        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"✅ Approve {row['id']}", key=f"approve_{row['id']}"):
                conn.execute(
                    "UPDATE reports SET status='approved' WHERE id=?",
                    (row['id'],)
                )
                conn.commit()
                st.rerun()

        with col2:
            if st.button(f"❌ Reject {row['id']}", key=f"reject_{row['id']}"):
                conn.execute(
                    "UPDATE reports SET status='rejected' WHERE id=?",
                    (row['id'],)
                )
                conn.commit()
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# USER FEEDBACK
# =====================================================
st.markdown("<div class='section-title'>💬 User Feedback</div>", unsafe_allow_html=True)

try:
    feedback_df = pd.read_sql_query(
        "SELECT * FROM feedback ORDER BY id DESC",
        conn
    )
except Exception as e:
    st.error("❌ Feedback table error: " + str(e))
    conn.close()
    st.stop()

if feedback_df.empty:
    st.info("No feedback submitted yet.")
else:
    for _, fb in feedback_df.iterrows():
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.markdown(f"### 👤 {fb['name']}  |  🕒 {fb['timestamp']}")
        st.write(f"📧 **Email:** {fb['email']}")
        st.write(f"👩 **User Type:** {fb['user_type']}")
        st.write(f"📊 **Usage:** {fb['usage']}")
        st.write(f"🧩 **Features Used:** {fb['features']}")

        st.write(
            f"⭐ **Ratings:** "
            f"Overall {fb['overall_rating']} | "
            f"UI {fb['design_rating']} | "
            f"Speed {fb['speed_rating']} | "
            f"Accuracy {fb['alert_accuracy']}"
        )

        if fb['liked']:
            st.write(f"👍 **Liked:** {fb['liked']}")
        if fb['issues']:
            st.write(f"⚠ **Issues:** {fb['issues']}")
        if fb['suggestions']:
            st.write(f"💡 **Suggestions:** {fb['suggestions']}")

        if fb['bug_reported'] == "Yes":
            st.warning("🐞 Bug Reported")
            st.write(f"📝 {fb['bug_description']}")
            st.write(f"⏰ {fb['bug_time']}")

        st.markdown("</div>", unsafe_allow_html=True)

conn.close()
