

import streamlit as st
import base64
from streamlit_option_menu import option_menu
from pages.Report import report_page
from pages.View_report import view_page
import os

def show_Incident():

    # LOAD IMAGE
    def img_to_base64(path):
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()

    BASE_DIR = os.path.dirname(__file__)
    IMAGE_PATH = os.path.join(BASE_DIR, "girl1.png")

    girl_b64 = img_to_base64(IMAGE_PATH)

    # CSS
    st.markdown("""
    <style>
    .stApp { background-color: #FF77B1; }
    .top-banner {
        width: 100%; height: 300px; background: #FF77B1;
        position: relative; padding-left: 40px; padding-top: 30px;
    }
    .girl-img {
        position: absolute; right: 50px; top: -20px;
        width: 33vw; max-width: 300px;
    }
    .title { font-size: 100px; font-weight: 900; color: white; }
    .subtitle { font-size: 30px; font-weight: 800; color: white; }
    .top1-banner {
        width: 100%; height: 160px; background: #F41C78;
        top: 15px; position: relative; padding-left: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

    # HEADER
    st.markdown(f"""
        <div class="top-banner">
            <div class="title">सुरक्षाSetu</div>
            <div class="subtitle">Empowering Women Securing Everyone</div>
            <img class="girl-img" src="data:image/png;base64,{girl_b64}" />
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="top1-banner">
            <i class="bi bi-exclamation-triangle-fill" style="font-size:55px;color:white"></i>
            <div>
                <div style="font-size:50px; font-weight:800; margin-top:-24px;color:white">
                    Incident Report
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # MAIN MENU
    selected = option_menu(
        menu_title="File a Report",
        options=["Report an Incident", "View Reports"],
        icons=["ban", "file-earmark-text"],
        orientation="horizontal",
        styles={
            "container": {
                "padding": "10px 50px",
                "background-color": "white",
                "border-radius": "25px",
                "justify-content": "center",
                "margin": "auto",
                "min-height": "500px",
                "width": "90%",
                "display": "flex",
                "align-items": "center"
            },
            "menu-title": {
                "font-size": "50px",
                "font-weight": "700",
                "color": "#F41C78",
                "text-align": "center"
            },
            "icon": {"color": "white", "font-size": "60px"},
            "nav-link": {
                "font-size": "40px",
                "font-weight": "700",
                "color": "white",
                "margin": "10px 30px",
                "width": "550px",
                "height": "300px",
                "border-radius": "20px",
                "background-color": "#F41C78",
                "display": "flex",
                "justify-content": "center",
                "align-items": "center"
            },
            "nav-link-selected": {"background-color": "#FF1C78"},
        },
        key="incident_menu",
    )

    # OPEN PAGES DIRECTLY WITHOUT SETTING SESSION STATE
    if selected == "Report an Incident":
        report_page()

    elif selected == "View Reports":
        view_page()


# main main above

