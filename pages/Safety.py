import streamlit as st
import base64
from streamlit_option_menu import option_menu
from pages.alertsys import guardian
from pages.Live_travel import travel
from pages.crime_prediction import crime
from pages.live_alert import live
# ---------------------------------
# PAGE CONFIG
# ---------------------------------
# st.set_page_config(
#     page_title="Suraksha Setu",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

def safety_page():

    # -------- IMAGE TO BASE64 --------
    def img_to_base64(path):
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()

    girl_b64 = img_to_base64("safeegirl.png")

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
        padding-top: 30px;
    }

    .girl-img {
        position: absolute;
        right: 60px;
        top: 20px;
        width: 23vw;
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
        menu_title="Safety Section",
        options=[
            "Live Alerts",
            "Live Travel",
            "Guardian Alert",
            "Crime Prediction"
        ],
        icons=[
            "bell-fill",
            "geo-alt",
            "telephone-fill",
            "graph-up"
        ],
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
    if selected == "Live Alerts":
        st.subheader("🚨 Live Alerts")
        live()

    elif selected == "Live Travel":
        st.subheader("📍 Live Travel")
        travel()

    elif selected == "Guardian Alert":
        st.subheader("🛡 Guardian Alert")
        guardian()

    elif selected == "Crime Prediction":
        st.subheader("Crime Prediction")
        crime()



# import streamlit as st
# import base64
# from streamlit_option_menu import option_menu
# from deep_translator import GoogleTranslator

# from pages.alertsys import guardian
# from pages.Live_travel import travel
# from pages.crime_prediction import crime

# # -----------------------------
# # TRANSLATION FUNCTION
# # -----------------------------
# def translate_text(text, lang_code):
#     try:
#         return GoogleTranslator(source='auto', target=lang_code).translate(text)
#     except Exception:
#         return text

# def safety_page():

#     # -------- LANGUAGE (FROM SESSION OR DEFAULT) --------
#     lang = st.session_state.get("lang", "English")
#     lang_code = 'en' if lang == "English" else 'hi' if lang == "हिन्दी" else 'mr'


#     # -------- IMAGE TO BASE64 --------
#     def img_to_base64(path):
#         with open(path, "rb") as img:
#             return base64.b64encode(img.read()).decode()

#     girl_b64 = img_to_base64("girl1.png")

#     # -------- CSS --------
#     st.markdown("""
#     <link rel="stylesheet"
#     href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">

#     <style>
#     .stApp { background-color: #FF77B1; }
#     .top-banner {
#         width: 100%;
#         height: 300px;
#         position: relative;
#         padding-left: 50px;
#         padding-top: 30px;
#     }
#     .girl-img {
#         position: absolute;
#         right: 60px;
#         top: -20px;
#         width: 35vw;
#         max-width: 320px;
#     }
#     .title {
#         font-size: 100px;
#         font-weight: 900;
#         color: white;
#     }
#     .subtitle {
#         font-size: 30px;
#         font-weight: 700;
#         color: white;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     # -------- HEADER --------
#     st.markdown(f"""
#         <div class="top-banner">
#             <div class="title">सुरक्षाSetu</div>
#             <div class="subtitle">
#                 {translate_text("Empowering Women Securing Everyone", lang_code)}
#             </div>
#             <img class="girl-img" src="data:image/png;base64,{girl_b64}">
#         </div>
#     """, unsafe_allow_html=True)

#     st.markdown("<br>", unsafe_allow_html=True)

#     # ---------------------------------
#     # OPTION MENU (TRANSLATED)
#     # ---------------------------------
#     selected = option_menu(
#         menu_title=translate_text("Safety Section", lang_code),
#         options=[
#             translate_text("Live Alerts", lang_code),
#             translate_text("Live Travel", lang_code),
#             translate_text("Guardian Alert", lang_code),
#             translate_text("Crime Prediction", lang_code)
#         ],
#         icons=[
#             "bell-fill",
#             "geo-alt",
#             "telephone-fill",
#             "graph-up"
#         ],
#         orientation="horizontal",
#         styles={
#             "container": {
#                 "padding": "30px",
#                 "background-color": "white",
#                 "border-radius": "25px",
#                 "width": "100%",
#                 "display": "flex",
#                 "min-height": "500px",
#                 "justify-content": "center",
#                 "flex-wrap": "nowrap"
#             },
#             "menu-title": {
#                 "font-size": "48px",
#                 "font-weight": "700",
#                 "color": "#000",
#                 "text-align": "center",
#                 "width": "100%"
#             },
#             "icon": {
#                 "color": "white",
#                 "font-size": "45px"
#             },
#             "nav-link": {
#                 "font-size": "26px",
#                 "font-weight": "700",
#                 "color": "white",
#                 "text-align": "center",
#                 "margin": "15px",
#                 "width": "220px",
#                 "height": "220px",
#                 "border-radius": "20px",
#                 "background-color": "#F41C78",
#                 "display": "flex",
#                 "flex-direction": "column",
#                 "justify-content": "center",
#                 "align-items": "center"
#             },
#             "nav-link-selected": {
#                 "background-color": "#FF1C78",
#             },
#         },
#         key="incident_menu"
#     )

#     st.markdown("<br>", unsafe_allow_html=True)

#     # ---------------------------------
#     # PAGE CONTENT (TRANSLATED)
#     # ---------------------------------
#     if selected == translate_text("Live Alerts", lang_code):
#         st.subheader("🚨 " + translate_text("Live Alerts", lang_code))
#         st.write(translate_text("Real-time safety alerts will appear here.", lang_code))

#     elif selected == translate_text("Live Travel", lang_code):
#         st.subheader("📍 " + translate_text("Live Travel", lang_code))
#         travel()

#     elif selected == translate_text("Guardian Alert", lang_code):
#         st.subheader("🛡 " + translate_text("Guardian Alert", lang_code))
#         guardian()

#     elif selected == translate_text("Crime Prediction", lang_code):
#         st.subheader("📊 " + translate_text("Crime Prediction", lang_code))
#         crime()



