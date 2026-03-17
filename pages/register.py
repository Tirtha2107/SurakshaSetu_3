
# import streamlit as st
# import re
# from pages.db_config import get_connection,DB_PATH

# # st.set_page_config(page_title=" सुरक्षाSetu - Register", layout="centered")

# # --- CSS STYLING ---
# st.markdown(
#     """
#     <style>
#     [data-testid="stSidebar"] { display: none; }
#     .stApp { background-color: #ffffff; }

#     div.stButton > button {
#         background-color: #ff4d88;
#         color: white;
#         border-radius: 10px;
#         padding: 8px 20px;
#         font-size: 16px;
#         border: none;
#         font-weight: 600;
#         width: 100%;
#     }
#     div.stButton > button:hover {
#         background-color: #ff1a66;
#         cursor: pointer;
#     }

#     .stTextInput input,
#     .stTextArea textarea {
#         background-color: #f2f2f2;
#         color: #000000;
#     }

#     [data-testid="stWidgetLabel"] p,
#     [data-testid="stWidgetLabel"] div {
#         color: #000000 !important;
#     }

#     .stTextInput input::placeholder,
#     .stTextArea textarea::placeholder {
#         color: #555555;
#         opacity: 1;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # --- TITLES ---
# st.markdown(
#     "<h1 style='text-align:center; color:#cc0066; font-family:Arial, sans-serif;'>सुरक्षाSetu</h1>",
#     unsafe_allow_html=True,
# )
# st.markdown(
#     "<h3 style='text-align:center; font-family:Arial, sans-serif; color:#333333;'>Register</h3>",
#     unsafe_allow_html=True,
# )
# st.write("")

# # --- VALIDATION FUNCTIONS ---
# def validate_name(value: str) -> bool:
#     return re.match(r"^[A-Za-z ]{2,}$", value) is not None

# def validate_email_strict(email: str) -> str:
#     email = email.strip()
#     pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
#     if not re.match(pattern, email):
#         return "Invalid email format."
#     domain = email.split('@')[1].lower()
#     if domain in ["gmail.co", "yahoo.co", "hotmail.co"]:
#         return f"Invalid domain '{domain}'. Did you mean .com?"
#     return None

# def validate_indian_phone(value: str) -> bool:
#     return re.match(r"^[6-9]\d{9}$", value) is not None

# # --- FORM ---
# st.markdown("<h4 style='color:#000000;'>Basic Details</h4>", unsafe_allow_html=True)

# full_name = st.text_input("Full Name", placeholder="Enter your full name")
# email = st.text_input("Email Address", placeholder="Enter your valid email address")
# password = st.text_input("Password", type="password", placeholder="Create a secure password")
# confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password to confirm")
# age = st.text_input("Age", placeholder="Enter your age (e.g., 25)")
# address = st.text_area("Full Address", placeholder="Enter your complete residential address")

# st.write("")
# st.markdown("<h4 style='color:#000000;'>Emergency Contacts (Any 5)</h4>", unsafe_allow_html=True)

# c1 = st.text_input("Contact 1", placeholder="Enter mobile number for Contact 1")
# c2 = st.text_input("Contact 2", placeholder="Enter mobile number for Contact 2")
# c3 = st.text_input("Contact 3", placeholder="Enter mobile number for Contact 3")
# c4 = st.text_input("Contact 4", placeholder="Enter mobile number for Contact 4")
# c5 = st.text_input("Contact 5", placeholder="Enter mobile number for Contact 5")

# st.write("")
# col1, col2 = st.columns(2)

# with col1:
#     if st.button("Register"):
#         if not full_name.strip() or not email.strip() or not password.strip() or not confirm_password.strip():
#             st.error("Full name, email, and passwords are required.")
#         elif not validate_name(full_name.strip()):
#             st.error("Full name should contain only letters and spaces.")
#         else:
#             email_error = validate_email_strict(email.strip())
#             if email_error:
#                 st.error(email_error)
#             elif len(password) < 6:
#                 st.error("Password must be at least 6 characters long.")
#             elif password != confirm_password:
#                 st.error("Passwords do not match.")
#             else:
#                 contacts = [c1.strip(), c2.strip(), c3.strip(), c4.strip(), c5.strip()]
#                 non_empty_contacts = [c for c in contacts if c]

#                 if not non_empty_contacts:
#                     st.error("Please enter at least one emergency contact.")
#                 else:
#                     invalid_numbers = [c for c in non_empty_contacts if not validate_indian_phone(c)]
#                     if invalid_numbers:
#                         st.error("Contacts must be valid 10-digit Indian numbers (start with 6–9).")
#                     elif len(set(non_empty_contacts)) != len(non_empty_contacts):
#                         st.error("Emergency contact numbers must be unique.")
#                     else:
#                         if age.strip():
#                             if not age.isdigit():
#                                 st.error("Age must be a number.")
#                             elif int(age) <= 0 or int(age) > 120:
#                                 st.error("Please enter a valid age.")
#                             else:
#                                 st.success("Registration Successful!")
#                         else:
#                             # 1. Open the connection to the database
#                             conn = get_connection()
#                             cursor = conn.cursor()

#                             try:
#                                 # 2. Prepare the SQL command to save data
#                                 # The '?' are placeholders to prevent hackers from breaking your DB (SQL Injection)
#                                 cursor.execute("""
#                                 INSERT INTO users (full_name, email, password, age, address, contact1, contact2, contact3, contact4, contact5)
#                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#                                 """, (full_name, email, password, age, address, c1, c2, c3, c4, c5))

#                                 # 3. Save the changes
#                                 conn.commit()
#                                 st.success("Registration Successful! Please go to the Login page.")

#                             except Exception as e:
#                                 # If the email already exists (UNIQUE constraint), this will show an error
#                                 st.error(f"Registration failed: {e}")
#                             finally:
#                                 # 4. Always close the connection
#                                 conn.close()

# with col2:
#     if st.button("Back to Login"):
#         st.switch_page("pages/login.py")


import streamlit as st
import re
from pages.db_config import get_connection, DB_PATH

# st.set_page_config(page_title=" सुरक्षाSetu - Register", layout="centered")

# --- CSS STYLING ---
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { display: none; }
    .stApp { background-color: #ffffff; }

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

    .stTextInput input,
    .stTextArea textarea {
        background-color: #f2f2f2;
        color: #000000;
    }

    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] div {
        color: #000000 !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #555555;
        opacity: 1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- TITLES ---
st.markdown(
    "<h1 style='text-align:center; color:#cc0066; font-family:Arial, sans-serif;'>सुरक्षाSetu</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h3 style='text-align:center; font-family:Arial, sans-serif; color:#333333;'>Register</h3>",
    unsafe_allow_html=True,
)
st.write("")

# --- VALIDATION FUNCTIONS ---
def validate_name(value: str) -> bool:
    return re.match(r"^[A-Za-z ]{2,}$", value) is not None

def validate_email_strict(email: str) -> str:
    email = email.strip()
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return "Invalid email format."
    domain = email.split('@')[1].lower()
    if domain in ["gmail.co", "yahoo.co", "hotmail.co"]:
        return f"Invalid domain '{domain}'. Did you mean .com?"
    return None

def validate_indian_phone(value: str) -> bool:
    return re.match(r"^[6-9]\d{9}$", value) is not None

# --- FORM ---
st.markdown("<h4 style='color:#000000;'>Basic Details</h4>", unsafe_allow_html=True)

full_name = st.text_input("Full Name", placeholder="Enter your full name")
email = st.text_input("Email Address", placeholder="Enter your valid email address")
password = st.text_input("Password", type="password", placeholder="Create a secure password")
confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password to confirm")
age = st.text_input("Age", placeholder="Enter your age (e.g., 25)")
address = st.text_area("Full Address", placeholder="Enter your complete residential address")

st.write("")
st.markdown("<h4 style='color:#000000;'>Emergency Contacts (Any 5)</h4>", unsafe_allow_html=True)

c1 = st.text_input("Contact 1", placeholder="Enter mobile number for Contact 1")
c2 = st.text_input("Contact 2", placeholder="Enter mobile number for Contact 2")
c3 = st.text_input("Contact 3", placeholder="Enter mobile number for Contact 3")
c4 = st.text_input("Contact 4", placeholder="Enter mobile number for Contact 4")
c5 = st.text_input("Contact 5", placeholder="Enter mobile number for Contact 5")

st.write("")
col1, col2 = st.columns(2)

with col1:
    if st.button("Register"):
        if not full_name.strip() or not email.strip() or not password.strip() or not confirm_password.strip():
            st.error("Full name, email, and passwords are required.")
        elif not validate_name(full_name.strip()):
            st.error("Full name should contain only letters and spaces.")
        else:
            email_error = validate_email_strict(email.strip())
            if email_error:
                st.error(email_error)
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                contacts = [c1.strip(), c2.strip(), c3.strip(), c4.strip(), c5.strip()]
                non_empty_contacts = [c for c in contacts if c]

                if not non_empty_contacts:
                    st.error("Please enter at least one emergency contact.")
                else:
                    invalid_numbers = [c for c in non_empty_contacts if not validate_indian_phone(c)]
                    if invalid_numbers:
                        st.error("Contacts must be valid 10-digit Indian numbers (start with 6–9).")
                    elif len(set(non_empty_contacts)) != len(non_empty_contacts):
                        st.error("Emergency contact numbers must be unique.")
                    else:
                        # ✅ FIXED AGE VALIDATION (NO LOGIC CHANGE ELSEWHERE)
                        if age.strip():
                            if not age.isdigit():
                                st.error("Age must be a number.")
                                st.stop()
                            elif int(age) <= 0 or int(age) > 120:
                                st.error("Please enter a valid age.")
                                st.stop()

                        # ✅ DATABASE INSERT (ALWAYS RUNS AFTER VALIDATION)
                        conn = get_connection()
                        cursor = conn.cursor()

                        try:
                            cursor.execute("""
                            INSERT INTO users 
                            (full_name, email, password, age, address, contact1, contact2, contact3, contact4, contact5)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (full_name, email, password, age, address, c1, c2, c3, c4, c5))

                            conn.commit()
                            st.success("Registration Successful! Please go to the Login page.")

                        except Exception as e:
                            st.error(f"Registration failed: {e}")

                        finally:
                            conn.close()

with col2:
    if st.button("Back to Login"):
        st.switch_page("pages/login.py")
