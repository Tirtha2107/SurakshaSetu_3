
# import streamlit as st
# import os
# from google import genai
# import random
# import base64

# def img_to_base64(path):
#     with open(path, "rb") as img:
#         return base64.b64encode(img.read()).decode()
# # ----------------- GEMINI API SETUP -----------------
# API_KEY = os.getenv("GEMINI_API_KEY")
# if not API_KEY:
#     st.error("❌ GEMINI_API_KEY not set. Set it as environment variable!")
#     st.stop()

# # Initialize Gemini client
# client = genai.Client(api_key=API_KEY)
# BASE_DIR = os.path.dirname(__file__)
# IMAGE_PATH = os.path.join(BASE_DIR, "bitgirl.png")

# girl_b64 = img_to_base64(IMAGE_PATH)
# # ----------------- HELPER: IMAGE TO BASE64 -----------------




# # ----------------- CHATBOT PAGE -----------------
# def chatbot_page():
#     # ---------- STYLE ----------
#     st.markdown(f"""
#     <style>

#     /* TOP BANNER */
#     .top-bannerc {{
#         width: 100%;
#         height:180px;
#         background: #F41C78;
#         padding-left: 40px;
#         padding-top: 30px;
#         position: relative;
#         border-radius: 12px;
#         margin-bottom: 20px;
#     }}

#     .banner-title {{
#         font-size: 36px;
#         font-weight: 800;
#         color: white;
#     }}

#     .banner-subtitle {{
#         font-size: 20px;
#         font-weight: 600;
#         color: #ffe4ef;
#     }}

#     .girl-imgc {{
#         position: absolute;
#         right:40px;
#         top:-140px;
#         width:350px;
#     }}

#     .user-box {{ background: #ffd9e6; padding: 8px; border-radius: 8px; }}
#     .bot-box {{ background: #F41C78; color: white; padding: 8px; border-radius: 8px; }}
#     .heading {{ font-size: 28px; font-weight: bold; margin-top: 20px; }}
#     </style>
#     """, unsafe_allow_html=True)

#     # ---------- TOP BANNER ----------
#     st.markdown(f"""
#     <div class="top-bannerc">
#         <div class="banner-title">💬 Women Safety AI Chatbot</div>
#         <div class="banner-subtitle">Ask • Learn • Stay Safe</div>
#         <img class="girl-imgc" src="data:image/png;base64,{girl_b64}">
#     </div>
#     """, unsafe_allow_html=True)

#     # ---------- HEADING ----------
#     st.markdown('<div class="heading">💬 Women Safety AI Chatbot</div>', unsafe_allow_html=True)

#     # ---------- DAILY SAFETY TIP ----------
#     safety_tips = [
#         "Always stay in well‑lit areas when walking alone 🚶‍♀️",
#         "Share your location with a trusted friend 📍",
#         "Trust your instincts; if something feels off, leave ⚠️",
#         "Keep a safety alarm or whistle handy 🔊",
#         "Avoid sharing personal details with strangers online 🌐",
#     ]
#     tip = random.choice(safety_tips)
#     st.info(f"💡 Safety Tip of the Day: {tip}")

#     # ---------- ASK A QUESTION ----------
#     question = st.text_input("Ask a question about women's safety:")

#     if question:
#         st.markdown(f'<div class="user-box"><b>You:</b> {question}</div>', unsafe_allow_html=True)
#         try:
#             response = client.models.generate_content(
#                 model="gemini-2.5-flash",
#                 contents=question
#             )
#             answer_text = response.text
#             st.markdown(f'<div class="bot-box"><b>Chatbot:</b> {answer_text}</div>', unsafe_allow_html=True)
#         except Exception as e:
#             st.error(f"Error: {e}")



safety_keywords = [
    "women safety","girl safety","harassment","eve teasing","molestation",
    "stalking","abuse","domestic violence","unsafe","danger","help","police",
    "self defense","emergency","crime","rape","sexual assault",
    "public transport safety","night travel safety","online harassment",
    "cyber stalking","acid attack","kidnapping","forced marriage",
    "workplace harassment","street harassment","dating safety"
]

import streamlit as st
import os
from google import genai
import random
import base64

def img_to_base64(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

# ----------------- GEMINI API SETUP -----------------
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("❌ GEMINI_API_KEY not set. Set it as environment variable!")
    st.stop()

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

BASE_DIR = os.path.dirname(__file__)
IMAGE_PATH = os.path.join(BASE_DIR, "bitgirl.png")

girl_b64 = img_to_base64(IMAGE_PATH)

# ----------------- CHATBOT PAGE -----------------
def chatbot_page():
    # ---------- STYLE ----------
    st.markdown(f"""
    <style>

    /* TOP BANNER */
    .top-bannerc {{
        width: 100%;
        height:180px;
        background: #F41C78;
        padding-left: 40px;
        padding-top: 30px;
        position: relative;
        border-radius: 12px;
        margin-bottom: 20px;
    }}

    .banner-title {{
        font-size: 36px;
        font-weight: 800;
        color: white;
    }}

    .banner-subtitle {{
        font-size: 20px;
        font-weight: 600;
        color: #ffe4ef;
    }}

    .girl-imgc {{
        position: absolute;
        right:40px;
        top:-140px;
        width:350px;
    }}

    .user-box {{ background: #ffd9e6; padding: 8px; border-radius: 8px; }}
    .bot-box {{ background: #F41C78; color: white; padding: 8px; border-radius: 8px; }}
    .heading {{ font-size: 28px; font-weight: bold; margin-top: 20px; }}
    </style>
    """, unsafe_allow_html=True)

    # ---------- TOP BANNER ----------
    st.markdown(f"""
    <div class="top-bannerc">
        <div class="banner-title">💬 Women Safety AI Chatbot</div>
        <div class="banner-subtitle">Ask • Learn • Stay Safe</div>
        <img class="girl-imgc" src="data:image/png;base64,{girl_b64}">
    </div>
    """, unsafe_allow_html=True)

    # ---------- HEADING ----------
    st.markdown('<div class="heading">💬 Women Safety AI Chatbot</div>', unsafe_allow_html=True)

    # ---------- DAILY SAFETY TIP ----------
    safety_tips = [
        "Always stay in well-lit areas when walking alone 🚶‍♀️",
        "Share your location with a trusted friend 📍",
        "Trust your instincts; if something feels off, leave ⚠️",
        "Keep a safety alarm or whistle handy 🔊",
        "Avoid sharing personal details with strangers online 🌐",
    ]
    tip = random.choice(safety_tips)
    st.info(f"💡 Safety Tip of the Day: {tip}")

    # ---------- ASK A QUESTION ----------
    question = st.text_input("Ask a question about women's safety:")

    if question:
        st.markdown(f'<div class="user-box"><b>You:</b> {question}</div>', unsafe_allow_html=True)
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=question
            )
            answer_text = response.text
            st.markdown(f'<div class="bot-box"><b>Chatbot:</b> {answer_text}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")