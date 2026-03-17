def view_page():
    import streamlit as st
    import sqlite3
    import pandas as pd
    import os
    import base64
    from pages.db_config import DB_PATH   # ✅ use SAME DB as Report.py


    # st.set_page_config(
    #     page_title="Women's Incident Reporter",
    #     layout="wide",
    #     initial_sidebar_state="collapsed"
    # )


    # -------------------------------
    # FIXED PROJECT ROOT + UPLOADS
    # -------------------------------
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_DIR = os.path.join(PROJECT_ROOT, "uploads")
    IMAGE_PATH = os.path.join(os.path.dirname(__file__), "girl4.png")

    def img_to_base64(path):
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()

    girl_b64 = img_to_base64(IMAGE_PATH)
    # -------------------------------
    # Ensure table exists
    # -------------------------------
    conn = sqlite3.connect(DB_PATH)
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

    # -------------------------------
    # Load ONLY approved reports
    # -------------------------------
    def load_reports():
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(
            """
            SELECT * FROM reports 
            WHERE LOWER(TRIM(status))='approved'
            ORDER BY id DESC
            """,
            conn
        )
        conn.close()
        return df

    df = load_reports()

    # -------------------------------
    # Styling
    # -------------------------------
    st.markdown("""
        <style>
                
            #MainMenu, footer, header {visibility: hidden;}
            [data-testid="stSidebar"] {display: none;}
            .block-container {padding-top: 0rem;}

            .stApp {
                background-color: #FF77B1;
            }
            .topv-banner {
            background:#F41C78;
            padding: 25px;
            border-radius: 18px;
            color: white;
            text-align: center;
            margin-bottom: 35px;
            position: relative;
            height: 200px;
            }

            .bannerv-title {
                font-size: 48px;
                font-weight: 800;
            }

            .label-text {
                font-weight: 700;
                font-size: 30px;
                color: #333;
            }
            .info-text {
                font-size: 30px;
                color: white;
                margin-bottom: 8px;
            }
            .view-img {
            position: absolute;
            right: -60px;
            top: -40px;
            width:400px;
           }
        </style>
    """, unsafe_allow_html=True)

    # -------------------------------
    # Display Approved Reports
    # -------------------------------
    if df.empty:
        st.info("No approved incident reports yet.")
    else:
        for _, row in df.iterrows():
            with st.container():
                st.markdown('<div class="incident-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([4, 1])

                # Report Details
                with col1:

                    st.markdown(f"""
                        <div class="topv-banner">
                            <div class="bannerv-title">View Reports – सुरक्षाSetu</div>
                            <img class="view-img" src="data:image/png;base64,{girl_b64}">
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"<div class='report-title'>{row.get('title','')}</div>", unsafe_allow_html=True)
                    st.markdown(f"<span class='label-text'>Reported By:</span> <span class='info-text'>{row.get('name','')}</span>", unsafe_allow_html=True)
                    st.markdown(f"<span class='label-text'>Category:</span> <span class='info-text'>{row.get('category','')}</span>", unsafe_allow_html=True)
                    st.markdown(f"<span class='label-text'>Description:</span> <span class='info-text'>{row.get('description','')}</span>", unsafe_allow_html=True)
                    st.markdown(f"<span class='label-text'>Location:</span> <span class='info-text'>{row.get('location','')}</span>", unsafe_allow_html=True)
                    st.markdown(f"<span class='label-text'>Timestamp:</span> <span class='info-text'>{row.get('timestamp','')}</span>", unsafe_allow_html=True)

                

                # with col2:
                #     girl_img = os.path.join(os.path.dirname(__file__), "girl3.png")

                #     if os.path.exists(girl_img):
                #         st.image(girl_img, width=200)
                #     else:
                #         st.warning(f"Image not found at: {girl_img}")
                #     st.write(os.path.abspath(girl_img))



                # -------------------------------
                # Attachment Handling
                # -------------------------------
                file_path_value = row.get("file_path") or ""

                if file_path_value:
                    if os.path.isabs(file_path_value):
                        full_path = file_path_value
                    else:
                        full_path = os.path.join(PROJECT_ROOT, file_path_value)

                    if os.path.exists(full_path):
                        _, ext = os.path.splitext(full_path)
                        ext = ext.lower().lstrip('.')

                        if ext in ("jpg", "jpeg", "png", "gif", "webp"):
                            st.write("---")
                            st.write("Attached Evidence:")
                            st.image(full_path, width=300)

                        elif ext in ("mp4", "mov", "avi", "mkv", "webm"):
                            st.write("---")
                            st.write("Attached Evidence:")
                            st.video(full_path)

                        else:
                            st.write("---")
                            st.write("Attached File:")
                            with open(full_path, "rb") as f:
                                st.download_button("Download File", f, file_name=os.path.basename(full_path))

                    else:
                        st.warning("⚠ File path saved but file not found: " + full_path)

                st.markdown("</div>", unsafe_allow_html=True)
                st.write("")


# # Run Page

# def view_page():
#     import streamlit as st
#     import sqlite3
#     import pandas as pd
#     import os
#     import base64
#     from pages.db_config import DB_PATH

#     # ---------------- PATHS ----------------
#     PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     UPLOAD_DIR = os.path.join(PROJECT_ROOT, "uploads")
#     GIRL_IMG = os.path.join(os.path.dirname(__file__), "girl4.png")

#     # ---------------- PAGE CONFIG ----------------
#     st.set_page_config(page_title="Approved Incident Reports", layout="wide")

#     # ---------------- GLOBAL CSS ----------------
#     st.markdown("""
#     <style>
#         #MainMenu, footer, header {visibility: hidden;}
#         [data-testid="stSidebar"] {display: none;}

#         .stApp {
#             background-color: #FF77B1;
#         }

#         h1, h2, h3, h4, p, span, div {
#             color: white !important;
#         }

#         .top-banner {
#             background: #F41C78;
#             padding: 25px 40px;
#             border-radius: 18px;
#             margin-bottom: 30px;
#         }

#         .top-banner h1 {
#             font-size: 46px;
#             font-weight: 800;
#             margin: 0;
#         }

#         .incident-card {
#             background: rgba(255,255,255,0.15);
#             padding: 25px;
#             border-radius: 16px;
#             margin-bottom: 25px;
#         }

#         .report-title {
#             font-size: 34px;
#             font-weight: 800;
#             color: #FFFFFF;
#             margin-bottom: 12px;
#         }

#         .label-text {
#             font-size: 22px;
#             font-weight: 700;
#             color: #FFD6E7;
#         }

#         .info-text {
#             font-size: 22px;
#             font-weight: 500;
#             color: white;
#         }

#         .media-title {
#             font-size: 20px;
#             font-weight: 700;
#             margin-top: 10px;
#         }
#     </style>
#     """, unsafe_allow_html=True)

#     # ---------------- HERO IMAGE ----------------
#     if os.path.exists(GIRL_IMG):
#         with open(GIRL_IMG, "rb") as f:
#             girl_base64 = base64.b64encode(f.read()).decode()
#         st.markdown(
#             f"""
#             <div style="position:absolute; right:40px; top:-20px;">
#                 <img src="data:image/png;base64,{girl_base64}" width="320">
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#     # ---------------- HEADER ----------------
#     st.markdown("""
#         <div class="top-banner">
#             <h1>📄 Approved Incident Reports</h1>
#             <p>Verified reports shared for awareness and safety</p>
#         </div>
#     """, unsafe_allow_html=True)

#     # ---------------- ENSURE TABLE ----------------
#     conn = sqlite3.connect(DB_PATH)
#     conn.execute("""
#         CREATE TABLE IF NOT EXISTS reports (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT,
#             category TEXT,
#             title TEXT,
#             description TEXT,
#             location TEXT,
#             file_path TEXT,
#             timestamp TEXT,
#             status TEXT DEFAULT 'pending'
#         )
#     """)
#     conn.commit()
#     conn.close()

#     # ---------------- LOAD APPROVED REPORTS ----------------
#     def load_reports():
#         conn = sqlite3.connect(DB_PATH)
#         df = pd.read_sql_query("""
#             SELECT * FROM reports
#             WHERE LOWER(TRIM(status))='approved'
#             ORDER BY id DESC
#         """, conn)
#         conn.close()
#         return df

#     df = load_reports()

#     # ---------------- DISPLAY REPORTS ----------------
#     if df.empty:
#         st.info("ℹ️ No approved incident reports yet.")
#         return

#     for _, row in df.iterrows():
#         with st.container():
#             st.markdown("<div class='incident-card'>", unsafe_allow_html=True)

#             st.markdown(
#                 f"<div class='report-title'>{row.get('title','')}</div>",
#                 unsafe_allow_html=True
#             )

#             st.markdown(
#                 f"<span class='label-text'>Reported By:</span> "
#                 f"<span class='info-text'>{row.get('name','')}</span>",
#                 unsafe_allow_html=True
#             )

#             st.markdown(
#                 f"<span class='label-text'>Category:</span> "
#                 f"<span class='info-text'>{row.get('category','')}</span>",
#                 unsafe_allow_html=True
#             )

#             st.markdown(
#                 f"<span class='label-text'>Description:</span><br>"
#                 f"<span class='info-text'>{row.get('description','')}</span>",
#                 unsafe_allow_html=True
#             )

#             st.markdown(
#                 f"<span class='label-text'>Location:</span> "
#                 f"<span class='info-text'>{row.get('location','')}</span>",
#                 unsafe_allow_html=True
#             )

#             st.markdown(
#                 f"<span class='label-text'>Reported On:</span> "
#                 f"<span class='info-text'>{row.get('timestamp','')}</span>",
#                 unsafe_allow_html=True
#             )

#             # ---------------- ATTACHMENTS ----------------
#             file_path = row.get("file_path") or ""
#             if file_path:
#                 full_path = file_path if os.path.isabs(file_path) else os.path.join(PROJECT_ROOT, file_path)

#                 if os.path.exists(full_path):
#                     ext = os.path.splitext(full_path)[1].lower()

#                     st.markdown("<div class='media-title'>📎 Attached Evidence</div>", unsafe_allow_html=True)

#                     if ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
#                         st.image(full_path, width=350)

#                     elif ext in [".mp4", ".mov", ".avi", ".mkv", ".webm"]:
#                         st.video(full_path)

#                     else:
#                         with open(full_path, "rb") as f:
#                             st.download_button(
#                                 "⬇ Download File",
#                                 f,
#                                 file_name=os.path.basename(full_path)
#                             )
#                 else:
#                     st.warning("⚠ Attachment not found on server.")

#             st.markdown("</div>", unsafe_allow_html=True)
#             st.write("")
