


import streamlit as st
import base64

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Get Started",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Remove sidebar + padding
# -----------------------------
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
.block-container {
    padding: 0 !important;
}

/* FORCE CENTER BUTTON */
div[data-testid="stButton"] {
    position: fixed;
    top: 92%;
    left: 97%;
    transform: translate(-50%, -50%);
    z-index: 1000;
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
# Button (CENTERED)
# -----------------------------
if st.button("Get Started", key="get_started_center"):
    st.switch_page("pages/login.py")
