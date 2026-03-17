def guardian():

    import streamlit as st
    import time
    from twilio.rest import Client
    import base64
    import re
    import os

    st.set_page_config(
        page_title="Guardian Alert",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # =============================
    # TWILIO CONFIG
    # =============================
    ACCOUNT_SID = "ACa42b9b2c37fad3f6885b10fd5a361c7c"
    AUTH_TOKEN = "178b29761feefb01e13c2f1daf0873d6"
    TWILIO_NUMBER = "+13022615581"

    def send_sms_alert(to_number, message):
        try:
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            client.messages.create(
                body=message,
                from_=TWILIO_NUMBER,
                to=to_number
            )
            return True
        except Exception as e:
            st.error(f"SMS Error: {e}")
            return False

    def img_to_base64(path):
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()

   

    BASE_DIR = os.path.dirname(__file__)
    IMAGE_PATH = os.path.join(BASE_DIR, "girl8.png")

    girl_b64 = img_to_base64(IMAGE_PATH)


    # =============================
    # PHONE VALIDATION
    # =============================
    def is_valid_indian_number(number):
        pattern = r"^\+91[6-9]\d{9}$"
        return re.match(pattern, number)

    # =============================
    # CSS
    # =============================
    st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    .block-container {padding-top: 0rem;}

    .top-guardian-banner {
        width: 100%;
        height: 200px;
        background: #F41C78;
        padding-left: 40px;
        padding-top: 30px;
        position: relative;
    }

    .banner-title {
        font-size: 46px;
        font-weight: 800;
        color: white;
    }

    .banner-subtitle {
        font-size: 22px;
        font-weight: 600;
        color: #ffe4ef;
    }

    .guardian-img {
        position: absolute;
        right: 40px;
        top: -60px;
        width: 300px;
    }

    @media (max-width: 900px) {
        .guardian-img { display: none; }
    }

    .custom-label {
        font-size: 28px;
        font-weight: 700;
        color: #000000;
        margin-bottom: 6px;
    }

    input {
        font-size: 18px !important;
        border-radius: 14px !important;
        padding: 14px !important;
    }

    .stButton > button {
        background: #F41C78;
        color: white;
        font-size: 22px;
        font-weight:300;
        height:10px;
        border-radius: 16px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

    # =============================
    # HEADER
    # =============================
    st.markdown(f"""
    <div class="top-guardian-banner">
        <div class="banner-title">Suraksha Arrival Check-In</div>
        <div class="banner-subtitle">
            Confirm your arrival safely 
        </div>
        <img class="guardian-img" src="data:image/png;base64,{girl_b64}">
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # =============================
    # FORM
    # =============================
    st.markdown("<div class='custom-label'>Destination</div>", unsafe_allow_html=True)
    destination = st.text_input("", label_visibility="collapsed")

    st.markdown("<div class='custom-label'>Expected Travel Time (minutes)</div>", unsafe_allow_html=True)
    travel_time = st.slider("", 1, 120, 10, label_visibility="collapsed")

    st.markdown("<div class='custom-label'>Trusted Contact Mobile Number</div>", unsafe_allow_html=True)
    trusted_contact = st.text_input(
        "",
        placeholder="+91XXXXXXXXXX",
        label_visibility="collapsed"
    )

    col1, col2 = st.columns(2)
    with col1:
        start = st.button("Start Journey", use_container_width=True)
    with col2:
        cancel = st.button("Cancel Journey", use_container_width=True)

    # =============================
    # START LOGIC WITH VALIDATION
    # =============================
    if start:
        if not destination:
            st.error("❌ Please enter destination")
        elif not trusted_contact:
            st.error("❌ Please enter mobile number")
        elif not is_valid_indian_number(trusted_contact):
            st.error("❌ Mobile number must be in format +91XXXXXXXXXX (10 digits)")
        else:
            st.session_state.start_time = time.time()
            st.session_state.travel_time = travel_time * 60
            st.session_state.active = True
            st.success("💖 Journey started. Please confirm when you arrive.")

    if cancel:
        st.session_state.active = False
        st.info("Journey cancelled")

    # =============================
    # STATUS & ARRIVAL
    # =============================
    status_box = st.empty()

    if st.session_state.get("active", False):

        elapsed = time.time() - st.session_state.start_time
        remaining = int((st.session_state.travel_time - elapsed) / 60)

        if elapsed < st.session_state.travel_time:
            status_box.info(
                f"⏳ Waiting for arrival confirmation ({max(remaining, 0)} min left)"
            )

            if st.button("✅ I Reached Safely", use_container_width=True):

                st.session_state.active = False

                arrival_message = (
                    f"Suraksha Setu Update:\n"
                    f"The user has safely reached the destination.\n"
                    f"Destination: {destination}"
                )

                send_sms_alert(trusted_contact, arrival_message)

                status_box.success("🎉 Arrival confirmed. Guardian notified.")

        else:
            st.session_state.active = False

            message = (
                f"🚨 SURAKSHA SETU ALERT 🚨\n"
                f"No arrival confirmation received.\n"
                f"Destination: {destination}\n"
                f"Please contact immediately."
            )

            send_sms_alert(trusted_contact, message)
            status_box.warning("⚠️ No confirmation received. Alert sent to trusted contact.")

    
