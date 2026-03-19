import streamlit as st
import base64
from streamlit_option_menu import option_menu
from pages.Mental import mental_health_page
from pages.Hospital import hospital_page
from pages.Physical import physical
from pages.Police import police_station_page
import os
def health_page():
    def img_to_base64(path):
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()
        
    
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    GIRL_IMG = os.path.join(os.path.dirname(__file__), "hospgirl.png")
    UPLOAD_DIR = os.path.join(PROJECT_ROOT, "uploads")
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    girl_b64 = img_to_base64(GIRL_IMG)


    # -----------------------------
    # LOAD BOOTSTRAP ICONS
    # -----------------------------
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
    """, unsafe_allow_html=True)

    # -----------------------------
    # CSS STYLING (UNCHANGED)
    # -----------------------------
    st.markdown("""
    <style>
    .stApp {
        background-color: #FF77B1;
    }
    .top-banner {
        width: 100%;
        height: 300px;
        background: #FF77B1;
        position: relative;
        padding-left: 40px;
    }
    .girl-img {
        position: absolute;
        right: 50px;
        top: 10px;
        width: 23vw;
        max-width: 500px;
    }
    .title {
        font-size: 100px;
        font-weight: 900;
        color: white;
    
    }
    @media (max-width: 768px) {

        .title {
            font-size: 55px;
            text-align: center;
        }
    }
    .subtitle {
        font-size: 30px;
        font-weight: 800;
        color: white;
    }
                
    /* MOBILE VERSION */
    @media (max-width: 768px) {
        .subtitle {
            font-size: 18px;
            text-align: center;
        }
    }   

    </style>
    """, unsafe_allow_html=True)

    # -----------------------------
    # TOP BANNER
    # -----------------------------
    st.markdown(f"""
    <div class="top-banner">
        <div class="title">सुरक्षाSetu</div>
        <div class="subtitle">Empowering Women Securing Everyone</div>
        <img class="girl-img" src="data:image/png;base64,{girl_b64}" />
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------
    # MENU
    # -----------------------------
    with st.container():
        selected = option_menu(
            menu_title="Health",
            options=[
                "Nearby Hospitals",
                "Physical Health",
                "Mental Health",
                "Police Station"
            ],
            icons=[
                "hospital",
                "person-walking",
                "emoji-smile",
                "shield-lock"
            ],
            orientation="horizontal",
            styles={
                "container": {
                    "padding": "40px",
                    "background-color": "white",
                    "border-radius": "25px",
                    "justify-content": "center",
                    "margin": "auto",
                    "min-height": "450px",
                    "width": "90%",
                    "display": "flex",
                    "align-items": "center"
                },
                "menu-title": {
                    "font-size": "56px",
                    "font-weight": "600",
                    "color": "#000",
                    "text-align": "center",
                    "display": "block",
                    "width": "100%"
                },
                "icon": {
                    "color": "white",
                    "font-size": "55px"
                },
                "nav-link": {
                    "font-size": "28px",
                    "font-weight": "700",
                    "color": "white",
                    "text-align": "center",
                    "margin": "15px",
                    "width": "250px",
                    "height": "250px",
                    "border-radius": "20px",
                    "background-color": "#F41C78",
                    "display": "flex",
                    "flex-direction": "column",
                    "justify-content": "center",
                    "align-items": "center"
                },
                "nav-link-selected": {
                    "background-color": "#FF1C78"
                },
            },
        )

    # -----------------------------
    # CONTENT RENDERING (NO SESSION STATE)
    # -----------------------------
    st.markdown("<br>", unsafe_allow_html=True)

    if selected == "Nearby Hospitals":
        hospital_page()
  

    elif selected == "Physical Health":
        physical()
       

    elif selected == "Mental Health":
        mental_health_page()
      

    elif selected == "Police Station":
        police_station_page()
        

        
