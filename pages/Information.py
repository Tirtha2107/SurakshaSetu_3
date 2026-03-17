

import streamlit as st
import base64
from streamlit_option_menu import option_menu
from pages.feedback import feedback_page
from pages.safety_tips import safety_tips_page
from pages.videos import videos_page
from pages.chatbot import chatbot_page
from pages.ngos import ngos_page
import os

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Suraksha Setu",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def info_page():


    def img_to_base64(path):
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()

    BASE_DIR = os.path.dirname(__file__)
    IMAGE_PATH = os.path.join(BASE_DIR, "girlinfo.png")

    girl_b64 = img_to_base64(IMAGE_PATH)


    # -------- CSS + BOOTSTRAP ICONS --------
    st.markdown("""
    <link rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">

    <style>
    .stApp {
        background-color: #FF77B1;
    }

    .top-banner {
        width: 100%;
        height: 300px;
        background: #FF77B1;
        position: relative;
        padding-left: 50px;
        padding-top: 50px;
    }

    .girl-img {
        position: absolute;
        right: 60px;
        top: -1px;
        width: 36vw;
        max-width: 320px;
    }

    .title {
        font-size: 100px;
        font-weight: 900;
        color: white;
    }

    .subtitle {
        font-size: 30px;
        font-weight: 700;
        color: white;
    }

    </style>
    """, unsafe_allow_html=True)

    # -------- HEADER --------
    st.markdown(f"""
        <div class="top-banner">
            <div class="title">सुरक्षाSetu</div>
            <div class="subtitle">Empowering Women Securing Everyone</div>
            <img class="girl-img" src="data:image/png;base64,{girl_b64}">
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------
    # OPTION MENU (HORIZONTAL FIX)
    # ---------------------------------
    selected = option_menu(
        menu_title="Information Section",
        options=[
            "Safety Tips",
            "Videos",
            "Chatbot",
            "Support NGOs",
            "Feedback"
        ],
        icons = ["shield-check", "camera-video", "chat-dots","people-fill","pencil-square"],
        orientation="horizontal",
        styles={
            "container": {
                "padding": "30px",
                "background-color": "white",
                "border-radius": "25px",
                "width": "100%",
                "display": "flex",
                "min-height": "500px",
                "justify-content": "center",
                "flex-wrap": "nowrap"   # 🔥 CRITICAL FIX
            },
            "menu-title": {
                "font-size": "48px",
                "font-weight": "700",
                "color": "#000",
                "text-align": "center",
                "width": "100%"
            },
            "icon": {
                "color": "white",
                "font-size": "45px"
            },
            "nav-link": {
                "font-size": "26px",
                "font-weight": "700",
                "color": "white",
                "text-align": "center",
                "margin": "15px",
                "width": "220px",
                "height": "220px",
                "border-radius": "20px",
                "background-color": "#F41C78",
                "display": "flex",
                "flex-direction": "column",
                "justify-content": "center",
                "align-items": "center"
            },
            "nav-link-selected": {
                "background-color": "#FF1C78",
            },
        },
        key="incident_menu"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------
    # PAGE CONTENT
    # ---------------------------------
    if selected == "Safety Tips":
        safety_tips_page()
        

    elif selected == "Videos":
        videos_page()

    elif selected ==  "Chatbot":
        chatbot_page()

    elif selected ==  "Support NGOs":
        ngos_page()
    
    elif selected ==  "Feedback":
        st.subheader( "Support ")
        feedback_page()
