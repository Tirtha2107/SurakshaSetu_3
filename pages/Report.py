def report_page():
    import streamlit as st
    import base64
    import sqlite3
    import os
    from datetime import datetime
    from pages.db_config import get_connection, DB_PATH

    # ---------------------------------
    # PAGE CONFIG (CALL ONLY ONCE)
    # ---------------------------------
    # st.set_page_config(
    #     page_title="Women's Incident Reporter",
    #     layout="wide",
    #     initial_sidebar_state="collapsed"
    # )

    # ---------------------------------
    # PATHS
    # ---------------------------------
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IMAGE_PATH = os.path.join(os.path.dirname(__file__), "girl3.png")
    UPLOAD_DIR = os.path.join(PROJECT_ROOT, "uploads")
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # ---------------------------------
    # IMAGE TO BASE64
    # ---------------------------------
    def img_to_base64(path):
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()

    girl_b64 = img_to_base64(IMAGE_PATH)

    # ---------------------------------
    # CSS
    # ---------------------------------
    st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        [data-testid="stSidebar"] {display: none;}
        .block-container {padding-top: 0rem;}

        .stApp {
            background-color: #FF77B1;
        }
        .topr-banner {
            background:#F41C78;
            padding: 25px;
            border-radius: 18px;
            color: white;
            text-align: center;
            margin-bottom: 35px;
            position: relative;
            height: 200px;
        }

        .bannerr-title {
            font-size: 48px;
            font-weight: 800;
        }

        .bannerr-subtitle {
            font-size: 20px;
            margin-top: 5px;
        }

        .custom-label {
            font-size: 26px;
            font-weight: 600;
            color:#000000;
            margin-bottom: 4px;
        }

        .rept-img {
            position: absolute;
            right: 30px;
            top: -40px;
            width: 290px;
        }

        input, textarea {
            font-size: 18px !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # ---------------------------------
    # DATABASE
    # ---------------------------------
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            title TEXT,
            description TEXT,
            location TEXT,
            file_path TEXT,
            timestamp TEXT,
            status TEXT DEFAULT 'pending'
        )
    """)
    conn.commit()
    conn.close()

    # ---------------------------------
    # HEADER
    # ---------------------------------
    st.markdown(f"""
    <div class="topr-banner">
        <div class="bannerr-title">Report an Incident – सुरक्षाSetu</div>
        <div class="bannerr-subtitle">Confidential • Safe • Supportive</div>
        <img class="rept-img" src="data:image/png;base64,{girl_b64}">
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------
    # FORM
    # ---------------------------------
    st.markdown("<div class='custom-label'>Name</div>", unsafe_allow_html=True)
    name = st.text_input("", placeholder="Enter your name...", label_visibility="collapsed")

    st.markdown("<div class='custom-label'>Select Incident Category</div>", unsafe_allow_html=True)
    category = st.selectbox(
        "",
        ["Harassment", "Domestic Violence", "Stalking", "Workplace Misconduct", "Other"],
        label_visibility="collapsed"
    )

    st.markdown("<div class='custom-label'>Incident Title</div>", unsafe_allow_html=True)
    title = st.text_input("", placeholder="Brief title...", label_visibility="collapsed")

    st.markdown("<div class='custom-label'>Describe What Happened</div>", unsafe_allow_html=True)
    description = st.text_area("", placeholder="Who, what, when, where...", label_visibility="collapsed")

    st.markdown("<div class='custom-label'>Location</div>", unsafe_allow_html=True)
    location = st.text_input("", placeholder="Street, Area, City", label_visibility="collapsed")

    st.markdown("<div class='custom-label'>Upload Photo / Video (Optional)</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "",
        type=["jpg", "jpeg", "png", "mp4", "mov"],
        label_visibility="collapsed"
    )

    submit = st.button("Submit Report")

    # ---------------------------------
    # SUBMIT LOGIC
    # ---------------------------------
    if submit:
        if not (name and title and description and location):
            st.error("⚠ Please fill all required fields.")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = ""

        if uploaded_file:
            save_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            file_path = f"uploads/{uploaded_file.name}"

        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            INSERT INTO reports
            (name, category, title, description, location, file_path, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
        """, (name, category, title, description, location, file_path, timestamp))
        conn.commit()
        conn.close()

        st.success("✅ Incident Report Submitted Successfully!")
