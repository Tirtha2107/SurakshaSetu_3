

def feedback_page():
    import streamlit as st
    import sqlite3
    from datetime import datetime
    from pages.db_config import get_connection, DB_PATH


    # ---------------- SURAKSHASETU THEME CSS ----------------
    st.markdown("""
    <style>
    .stApp {
        background-color: #FF77B1;
    }
        #MainMenu, footer, header {visibility: hidden;}
        [data-testid="stSidebar"] {display: none;}

        .topf-banner {
            background:#F41C78;
            padding: 25px;
            border-radius: 18px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
        }

        .topf-banner h1 {
            font-size: 50px;
            font-weight: 800;
            margin-bottom: 6px;
        }

        .topf-banner p {
            font-size: 18px;
            opacity: 0.95;
        }

        .label {
            font-size: 25px;
            font-weight: 600;
            margin-top: 16px;
        }

        input, textarea {
            font-size: 17px !important;
        }

        button {
            background-color: #F41C78 !important;
            color: white !important;
            font-size: 18px !important;
            border-radius: 10px !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- TOP BANNER ----------------
    st.markdown("""
    <div class="topf-banner">
        <h1>सुरक्षाSetu Feedback</h1>
        <p>Your voice helps us create a safer future</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- DB TABLE ----------------
    conn = get_connection()
    conn.execute("""
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
    conn.commit()
    conn.close()

    # ---------------- FEEDBACK FORM CARD ----------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown("<div class='label'>Name *</div>", unsafe_allow_html=True)
    name = st.text_input("", placeholder="Enter your name", label_visibility="collapsed")

    st.markdown("<div class='label'>Email (Optional)</div>", unsafe_allow_html=True)
    email = st.text_input("", placeholder="Enter email", label_visibility="collapsed")

    st.markdown("<div class='label'>You are a</div>", unsafe_allow_html=True)
    user_type = st.selectbox(
        "",
        ["Student", "Professional", "Working Woman", "Other"],
        label_visibility="collapsed"
    )

    st.markdown("<div class='label'>How often do you use SurakshaSetu?</div>", unsafe_allow_html=True)
    usage = st.radio("", ["Daily", "Weekly", "Occasionally"], label_visibility="collapsed")

    st.markdown("<div class='label'>Features Used</div>", unsafe_allow_html=True)
    features = st.multiselect(
        "",
        [
            "Live Safety Alerts",
            "Smart Route Planning",
            "Nearby Emergency Services",
            "Guardian Mode",
            "ChatBot",
            "Health",
            "Information",
            "SOS"
        ],
        label_visibility="collapsed"
    )

    st.markdown("<div class='label'>Ratings (1 = Poor, 5 = Excellent)</div>", unsafe_allow_html=True)
    overall = st.slider("Overall Experience", 1, 5, 3)
    design = st.slider("Design & UI", 1, 5, 3)
    speed = st.slider("App Speed", 1, 5, 3)
    accuracy = st.slider("Alert Accuracy", 1, 5, 3)

    st.markdown("<div class='label'>What did you like the most?</div>", unsafe_allow_html=True)
    liked = st.text_area("", placeholder="Your thoughts...", label_visibility="collapsed")

    st.markdown("<div class='label'>Issues Faced (if any)</div>", unsafe_allow_html=True)
    issues = st.text_area("", placeholder="Any problem?", label_visibility="collapsed")

    st.markdown("<div class='label'>Suggestions for Improvement</div>", unsafe_allow_html=True)
    suggestions = st.text_area("", placeholder="Your suggestion...", label_visibility="collapsed")

    st.markdown("<div class='label'>Bug Report</div>", unsafe_allow_html=True)
    bug_reported = st.checkbox("I faced a technical issue")

    bug_desc = ""
    bug_time = ""

    if bug_reported:
        bug_desc = st.text_area("Describe the bug")
        bug_time = str(st.time_input("Time of issue"))

    submit = st.button("🚀 Submit Feedback")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- SUBMIT LOGIC ----------------
    if submit:
        if not name.strip():
            st.error("⚠ Name is required.")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_connection()   # ✅ FIXED: same DB as table creation
        conn.execute("""
            INSERT INTO feedback (
                name, email, user_type, usage, features,
                overall_rating, design_rating, speed_rating, alert_accuracy,
                liked, issues, suggestions,
                bug_reported, bug_description, bug_time, timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, email, user_type, usage, ", ".join(features),
            overall, design, speed, accuracy,
            liked, issues, suggestions,
            "Yes" if bug_reported else "No",
            bug_desc, bug_time, timestamp
        ))
        conn.commit()
        conn.close()

        st.success("✅ Thank you! Your feedback has been saved securely.")
