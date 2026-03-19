import streamlit as st
import base64
from pages.Health import health_page
from pages.Safety import safety_page
from pages.Incident_Report import show_Incident
from pages.Information import info_page
from pages.SOS import sos_page
import os
# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Suraksha Setu",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# HIDE STREAMLIT UI
# -----------------------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def go(page):
    st.session_state.page = page

# -----------------------------
# IMAGE
# -----------------------------
def img_to_base64(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()



BASE_DIR = os.path.dirname(__file__)
IMAGE_PATH = os.path.join(BASE_DIR, "girl60.png")

girl_b64 = img_to_base64(IMAGE_PATH)


# -----------------------------
# GLOBAL BACKGROUND + HEADER CSS
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #FF77B1;
}

/* HEADER */
.top-banner {
    width: 100%;
    height: 300px;
    min-height:40vh;
    padding: 30px 40px;
    position: relative;
}

.girl-img {
    position: absolute;
    right: 50px;
    top: -60px;
    width: 34vw;
    max-width: 500px;
}

.title {
    font-size: 110px;
    font-weight: 900;
    color: white;
}

.subtitle {
    font-size: 40px;
    font-weight: 700;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HOME-ONLY BUTTON CSS
# -----------------------------
if st.session_state.page == "home":
    st.markdown("""
    <style>
    /* BIG HOME BUTTONS */
    div.stButton > button {
        height: 220px;
        font-size: 28px;
        font-weight: 700;
        background-color: #F41C78;
        color: white;
        border-radius: 25px;
        border: none;
        white-space: pre-line;
        line-height: 1.2;
        transition: all 0.25s ease;
    }

    div.stButton > button:hover {
        background-color: #FF1C78;
        transform: scale(1.05);
    }

    /* BUTTON LABEL */
    button p {
        font-size: 40px !important;
        font-weight: 800 !important;
        line-height: 1.2 !important;
    }

    button:hover p {
        color: white;
        transform: scale(1.08);
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# BACK BUTTON CSS (SAFE)
# -----------------------------
st.markdown("""
<style>
.back-btn button {
    height: 26px !important;
    padding: 0 8px !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    background-color: white !important;
    color: #F41C78 !important;
    border-radius: 6px !important;
    border: 1.5px solid #F41C78 !important;
    line-height: 1 !important;
}

.back-btn button:hover {
    background-color: #F41C78 !important;
    color: white !important;
    transform: none !important;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# BACK BUTTON
# -----------------------------
def back_button():
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅"):
        go("home")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# HOME
# -----------------------------
def render_home():

    st.markdown(f"""
    <div class="top-banner">
        <div class="title">सुरक्षाSetu</div>
        <div class="subtitle">Empowering Women Securing Everyone</div>
        <img class="girl-img" src="data:image/png;base64,{girl_b64}">
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1], gap="small")

    with col1:
        if st.button("\nSafety", use_container_width=True):
            go("safety")

    with col2:
        if st.button("\nSurakshaCare", use_container_width=True):
            go("health")

    with col3:
        if st.button("\nSOS", use_container_width=True):
            go("sos")

    with col4:
        if st.button("\nIncident", use_container_width=True):
            go("incident")

    with col5:
        if st.button("\nInformation", use_container_width=True):
            go("info")

# -----------------------------
# ROUTING
# -----------------------------
if st.session_state.page == "home":
    render_home()

elif st.session_state.page == "safety":
    back_button()
    safety_page()

elif st.session_state.page == "health":
    back_button()
    health_page()

elif st.session_state.page == "incident":
    back_button()
    show_Incident()

elif st.session_state.page == "info":
    back_button()
    info_page()

elif st.session_state.page == "sos":
    back_button()
    sos_page()


# # main


