

import streamlit as st
import re
from pages.db_config import get_connection

# st.set_page_config(page_title=" सुरक्षाSetu - Login", layout="centered")

# --- CSS STYLING ---
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { 
        display: none; 
    }

    .stApp {
        background-color: #ffffff;
    }

    div.stButton > button {
        background-color: #ff4d88;
        color: white;
        border-radius: 10px;
        padding: 8px 20px;
        font-size: 16px;
        border: none;
        font-weight: 600;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #ff1a66;
        cursor: pointer;
    }

    .stTextInput input {
        background-color: #f2f2f2;
        color: #000000;
    }

    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #000000 !important;
        font-weight: 600;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #cc0066 !important;
        border-bottom-color: #cc0066 !important;
    }

    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] div {
        color: #000000 !important;
    }

    .stTextInput input::placeholder {
        color: #555555;
        opacity: 1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- TITLE ---
st.markdown(
    "<h1 style='text-align:center; color:#F41C78; font-family:Arial, sans-serif;'>सुरक्षाSetu</h1>",
    unsafe_allow_html=True,
)

# --- VALIDATION LOGIC ---
def validate_email_strict(email: str) -> str:
    email = email.strip()
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return "Invalid email format."

    domain_part = email.split('@')[1].lower()
    typo_domains = ["gmail.co", "yahoo.co", "hotmail.co", "outlook.co"]
    if domain_part in typo_domains:
        return f"Did you mean .com? ({domain_part} is invalid)"

    return None

def validate_indian_phone(phone: str) -> bool:
    return re.match(r"^[6-9]\d{9}$", phone) is not None

# --- TABS ---
tab_user, tab_admin = st.tabs(["User Login", "Admin Login"])

# ================= USER LOGIN =================
with tab_user:
    st.markdown("<br>", unsafe_allow_html=True)

    u_username = st.text_input(
        "Email or Phone Number",
        placeholder="Enter your email or 10-digit mobile number",
        key="user_input"
    )
    u_password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your user password",
        key="user_pass"
    )

    st.write("")
    c1, c2 = st.columns(2)

    with c1:
        if st.button("User Login"):
            if not u_username.strip():
                st.error("Username is required.")
            elif not u_password.strip():
                st.error("Password is required.")
            else:
                input_val = u_username.strip()

                # -------- EMAIL LOGIN --------
                if "@" in input_val:
                    error_msg = validate_email_strict(input_val)
                    if error_msg:
                        st.error(error_msg)
                    else:
                        conn = get_connection()
                        cursor = conn.cursor()

                        cursor.execute("""
                            SELECT * FROM users 
                            WHERE email=? AND password=?
                        """, (input_val, u_password))

                        user_record = cursor.fetchone()
                        conn.close()

                        if user_record:
                            st.success(f"Welcome back, {user_record[1]}!")
                            st.switch_page("pages/home4.py")
                        else:
                            st.error("Invalid email or password.")

                # -------- PHONE LOGIN --------
                else:
                    if not input_val.isdigit():
                        st.error("Phone number must contain digits only.")
                    elif len(input_val) != 10:
                        st.error("Phone number must be exactly 10 digits.")
                    elif not validate_indian_phone(input_val):
                        st.error("Invalid Indian Number. Must start with 6–9.")
                    else:
                        conn = get_connection()
                        cursor = conn.cursor()

                        cursor.execute("""
                            SELECT * FROM users 
                            WHERE (contact1=? OR contact2=? OR contact3=? OR contact4=? OR contact5=?)
                            AND password=?
                        """, (input_val, input_val, input_val, input_val, input_val, u_password))

                        user_record = cursor.fetchone()
                        conn.close()

                        if user_record:
                            st.success(f"Welcome back, {user_record[1]}!")
                            st.switch_page("pages/home4.py")
                        else:
                            st.error("Account not found. Please check your credentials.")

    with c2:
        if st.button("New User? Register"):
            st.switch_page("pages/register.py")

# ================= ADMIN LOGIN =================
with tab_admin:
    st.markdown("<br>", unsafe_allow_html=True)

    a_username = st.text_input(
        "Admin ID",
        placeholder="Enter Admin ID",
        key="admin_input"
    )
    a_password = st.text_input(
        "Admin Key",
        type="password",
        placeholder="Enter Admin Key",
        key="admin_pass"
    )

    st.write("")
    if st.button("Admin Login"):
        if not a_username.strip() or not a_password.strip():
            st.error("Admin credentials required.")
        else:
            if a_username == "admin" and a_password == "admin123":
                st.success("Welcome Admin!")
                st.switch_page("pages/admin.py")
            else:
                st.error("Invalid Admin credentials.")
