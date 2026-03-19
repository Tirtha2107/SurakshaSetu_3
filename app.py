


# import streamlit as st
# import base64

# # -----------------------------
# # Page config
# # -----------------------------
# st.set_page_config(
#     page_title="Get Started",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # -----------------------------
# # Remove sidebar + padding
# # -----------------------------
# st.markdown("""
# <style>
# [data-testid="stSidebar"] { display: none; }
# .block-container {
#     padding: 0 !important;
# }

# /* FORCE CENTER BUTTON */
# div[data-testid="stButton"] {
#     position: fixed;
#     top: 92%;
#     left: 97%;
#     transform: translate(-50%, -50%);
#     z-index: 1000;
# }
# </style>
# """, unsafe_allow_html=True)

# # -----------------------------
# # Load image
# # -----------------------------
# def get_base64(path):
#     with open(path, "rb") as f:
#         return base64.b64encode(f.read()).decode()

# img_b64 = get_base64("backimg.png")

# # -----------------------------
# # Background image
# # -----------------------------
# st.markdown(f"""
# <style>
# .hero {{
#     position: relative;
#     width: 100%;
#     height: 100vh;
# }}

# .hero img {{
    # width: 100%;
    # height: auto;
    # display: block;
    # object-fit: contain;
# }}
# </style>

# <div class="hero">
#     <img src="data:image/png;base64,{img_b64}">
# </div>
# """, unsafe_allow_html=True)

# # -----------------------------
# # Button (CENTERED)
# # -----------------------------
# if st.button("Get Started", key="get_started_center"):
    
#     st.switch_page("pages/login.py")


import streamlit as st
import base64

import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
<style>

/* ===== MOBILE RESPONSIVE FIX FOR ALL PAGES ===== */

@media (max-width: 768px) {

    /* Make every column full width */
    div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        margin-bottom: 15px !important;
    }

    /* Fix big titles like सुरक्षाSetu */
    h1 {
        font-size: 30px !important;
        text-align: center !important;
    }

    /* Fix section titles like Health / Safety */
    h2, h3 {
        font-size: 22px !important;
        text-align: center !important;
    }

    /* Make ALL buttons responsive (cards are buttons in Streamlit) */
    button {
        width: 100% !important;
        font-size: 16px !important;
        padding: 14px !important;
        border-radius: 14px !important;
    }

    /* Make images fit mobile screen */
    img {
        max-width: 100% !important;
        height: auto !important;
    }

    /* Reduce spacing so cards don't look stretched */
    .block-container {
        padding-top: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
}

</style>
""", unsafe_allow_html=True)
# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Get Started",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Remove sidebar + padding + FIX BUTTON
# -----------------------------
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
.block-container {
    padding: 0 !important;
}

/* FIXED BUTTON (BOTTOM CENTER) */
.stButton > button {
    position: fixed;
    bottom: 40px;
    left: 50%;
    transform: translateX(-50%);
    
    width: 220px;
    max-width: 90%;
    height: 50px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 12px;
    
    background-color: white;
            
    color: #ff4b6e;
    border: none;
    
    z-index: 9999;
}

/* Hover effect */
.stButton > button:hover {
    background-color: white;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load image
# -----------------------------
def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_b64 = get_base64("backimg.png")

# -----------------------------
# Background image
# -----------------------------
st.markdown(f"""
<style>
.hero {{
    position: relative;
    width: 100%;
    height: 100vh;
}}

.hero img {{
    width: 100%;
    height: auto;
    display: block;
    object-fit: contain;
}}
            
</style>

<div class="hero">
    <img src="data:image/png;base64,{img_b64}">
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Button
# -----------------------------
if st.button("Get Started", key="get_started_center"):
    st.switch_page("pages/login.py")