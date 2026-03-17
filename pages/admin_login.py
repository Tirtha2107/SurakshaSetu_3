import streamlit as st
import hashlib

# ---------------------------
# HASH PASSWORD FUNCTION
# ---------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------------------
# ADMIN CREDENTIALS (ADD MORE IF NEEDED)
# ---------------------------
admins = {
    "admin": hash_password("admin123"),   # username : hashed password
}

# ---------------------------
# LOGIN FUNCTION
# ---------------------------
def admin_login():
    st.set_page_config(page_title="Admin Login", layout="centered")

    st.title("🔐 Admin Login")
    st.write("Enter your credentials to access the Admin Panel")

    # If already logged in
    if "admin_logged_in" in st.session_state and st.session_state.admin_logged_in:
        st.success("Already logged in!")
        st.stop()

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in admins:
            if hash_password(password) == admins[username]:
                st.session_state.admin_logged_in = True
                st.session_state.admin_username = username
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("❌ Incorrect Password")
        else:
            st.error("❌ Username not found")
