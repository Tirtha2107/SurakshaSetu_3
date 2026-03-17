
def mental_health_page():
    import streamlit as st
    import pandas as pd
    import requests
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
    import folium
    from streamlit_folium import folium_static
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    import datetime
    import base64
    import os

    # ---------------- COLORS ----------------
    LIGHT_PINK = "##FF77B1"
    DARK_PINK = "#E91E63"
    BUTTON_HOVER_PINK = "#D81B60"

    # ---------------- SESSION ----------------
    if "mental_page" not in st.session_state:
        st.session_state.mental_page = "main"

    if "journal_entries" not in st.session_state:
        st.session_state.journal_entries = []

    # ---------------- CSS ----------------

    # st.set_page_config(
    #     page_title="Mental Health",
    #     layout="wide",
    #     initial_sidebar_state="collapsed"
    # )

    st.markdown(f"""
    <style>
    body {{ background-color: {LIGHT_PINK}; }}
    .stApp {{ background-color: {LIGHT_PINK}; }}
    .stButton>button {{
        background-color: {DARK_PINK};
        color: white !important;
        padding: 16px 28px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: 600;
        width: 100%;
        margin-bottom: 15px;
        border: none;
    }}
    .stButton>button:hover {{
        background-color: {BUTTON_HOVER_PINK};
        transform: scale(1.04);
    }}
    h1, h2, h3 {{ color: {DARK_PINK}; font-weight: 800; }}
    </style>
    """, unsafe_allow_html=True)

    # ================= MAIN PAGE =================
    if st.session_state.mental_page == "main":
        st.markdown("<h1>🧠 Mental Health</h1>", unsafe_allow_html=True)
        st.write("Select a feature to explore:")

        c1, c2 = st.columns(2)
        c3, c4 = st.columns(2)

        if c1.button("🧠 Mental Health Quiz"):
            st.session_state.mental_page = "quiz"

        if c2.button("🤝 Support Circle"):
            st.session_state.mental_page = "support"

        if c3.button("🌿 Mindfulness"):
            st.session_state.mental_page = "mindfulness"

        if c4.button("📓 Mood Journal"):
            st.session_state.mental_page = "journal"

    # # ================= QUIZ =================

    # ================= QUIZ =================
    elif st.session_state.mental_page == "quiz":


        def img_to_base64(path):
            with open(path, "rb") as img:
                return base64.b64encode(img.read()).decode()

        BASE_DIR = os.path.dirname(__file__)
        IMAGE_PATH = os.path.join(BASE_DIR, "girl7.png")

        girl_b64 = img_to_base64(IMAGE_PATH)


        

        st.markdown("""
        <style>
            .girl-img {
                position: absolute;
                right: 50px;
                top: -90px;
                width: 17vw;
                max-width: 400px;
            }
            .top5-banner {
                width: 100%;
                height: 300px;
                background: #F41C78;
                position: relative;
                padding-left:10px;
            }
            .title {
                font-size:80px;
                font-weight: 600;
                color: white;
            }
            .subtitle {
                font-size: 25px;
                font-weight: 600;
                color: white;
            }
            div.stButton > button {
                width: 100% !important;
                height: 70px !important;
                font-size: 30px;
                background:#F41C78;
                color: white;
                font-weight: 600 !important;
                border-radius: 12px !important;
            }
            div[data-testid="column"] {
                padding: 6px;
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="top5-banner">
            <div class="title">Mental Health Assessment</div>
            <div class="subtitle">Your mental health matters—start your journey today</div>
            <img class="girl-img" src="data:image/png;base64,{girl_b64}" />
        </div>
        """, unsafe_allow_html=True)

        test_choice = st.selectbox(
            "Select Assessment Type",
            ["Stress Level Check", "Anxiety Screening", "Depression Screening"]
        )

        options = {
            "Not at all": 0,
            "Several days": 1,
            "More than half the days": 2,
            "Nearly every day": 3
        }




            # ================= STRESS =================
        if test_choice == "Stress Level Check":
            st.success("You selected Stress Level Check")

            questions = [
                "I feel overwhelmed by daily responsibilities",
                "I find it hard to relax",
                "I feel nervous or stressed",
                "I feel I have control over my life"
            ]

            if "stress_answers" not in st.session_state:
                st.session_state.stress_answers = {}

            for i, q in enumerate(questions):
                st.markdown(f"<p style='font-size:30px;color:white;'>{q}</p>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                c3, c4 = st.columns(2)

                if c1.button("Not at all", key=f"s{i}0"): st.session_state.stress_answers[q] = "Not at all"
                if c2.button("Several days", key=f"s{i}1"): st.session_state.stress_answers[q] = "Several days"
                if c3.button("More than half", key=f"s{i}2"): st.session_state.stress_answers[q] = "More than half the days"
                if c4.button("Nearly every day", key=f"s{i}3"): st.session_state.stress_answers[q] = "Nearly every day"

            if st.button("View Result"):
                score = sum(options[v] for v in st.session_state.stress_answers.values())
                if score <= 4:
                    st.success("💚 Low Stress")
                elif score <= 8:
                    st.warning("💛 Moderate Stress")
                else:
                    st.error("❤️ High Stress")

        # ================= ANXIETY =================
        elif test_choice == "Anxiety Screening":
            st.warning("You selected Anxiety Screening")

            questions = [
                "Feeling nervous or anxious",
                "Not being able to stop worrying",
                "Trouble relaxing",
                "Feeling restless",
                "Feeling afraid something bad may happen"
            ]

            if "anxiety_answers" not in st.session_state:
                st.session_state.anxiety_answers = {}

            for i, q in enumerate(questions):
                st.markdown(f"<p style='font-size:30px;color:white;'>{q}</p>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                c3, c4 = st.columns(2)

                if c1.button("Not at all", key=f"a{i}0"): st.session_state.anxiety_answers[q] = "Not at all"
                if c2.button("Several days", key=f"a{i}1"): st.session_state.anxiety_answers[q] = "Several days"
                if c3.button("More than half", key=f"a{i}2"): st.session_state.anxiety_answers[q] = "More than half the days"
                if c4.button("Nearly every day", key=f"a{i}3"): st.session_state.anxiety_answers[q] = "Nearly every day"

            if st.button("View Result"):
                score = sum(options[v] for v in st.session_state.anxiety_answers.values())
                if score <= 4:
                    st.success("💚 Minimal Anxiety")
                elif score <= 9:
                    st.warning("💛 Mild Anxiety")
                elif score <= 14:
                    st.error("🧡 Moderate Anxiety")
                else:
                    st.error("❤️ Severe Anxiety")

        # ================= DEPRESSION =================
        elif test_choice == "Depression Screening":
            st.error("You selected Depression Screening")

            questions = [
                "Little interest or pleasure in activities",
                "Feeling down or hopeless",
                "Trouble sleeping",
                "Low energy",
                "Negative thoughts about yourself"
            ]

            if "depression_answers" not in st.session_state:
                st.session_state.depression_answers = {}

            for i, q in enumerate(questions):
                st.markdown(f"<p style='font-size:30px;color:white;'>{q}</p>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                c3, c4 = st.columns(2)

                if c1.button("Not at all", key=f"d{i}0"): st.session_state.depression_answers[q] = "Not at all"
                if c2.button("Several days", key=f"d{i}1"): st.session_state.depression_answers[q] = "Several days"
                if c3.button("More than half", key=f"d{i}2"): st.session_state.depression_answers[q] = "More than half the days"
                if c4.button("Nearly every day", key=f"d{i}3"): st.session_state.depression_answers[q] = "Nearly every day"

            if st.button("View Result"):
                score = sum(options[v] for v in st.session_state.depression_answers.values())
                if score <= 4:
                    st.success("💚 Minimal Symptoms")
                elif score <= 9:
                    st.warning("💛 Mild Symptoms")
                elif score <= 14:
                    st.error("🧡 Moderate Symptoms")
                else:
                    st.error("❤️ Severe Symptoms")

        st.info("⚠️ This is not a diagnosis. Awareness only.")

        if st.button("⬅ Back", key="mental_back_quiz"):
            st.session_state.mental_page = "main"



    
       
    # ================= SUPPORT CIRCLE =================
    elif st.session_state.mental_page == "support":
        st.markdown("<h2>🤝 Support Circle</h2>", unsafe_allow_html=True)

        st.markdown("""
        <p style="font-size:18px; line-height:1.8;">
        Mental health is as important as physical health.  
        Reaching out for help shows <b>strength, not weakness</b>.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("### 🎥 Learn About Mental Health")
        st.video("https://www.youtube.com/watch?v=DxIDKZHW3-E")

        # -------- COUNSELLOR + HOSPITAL FINDER --------
        st.markdown("### 🧑‍⚕️ Find Mental Health Support Near You")
        city = st.text_input("🏙 Enter City Name (Mumbai, Pune, Delhi, etc.)")

        if city:
            geolocator = Nominatim(
                user_agent="women_safety_mental_health_app",
                timeout=10
            )

            try:
                location = geolocator.geocode(city)
            except (GeocoderTimedOut, GeocoderUnavailable):
                location = None

            if location is None:
                st.error("⚠️ Unable to connect to map service. Try again later.")
                st.stop()

            lat, lon = location.latitude, location.longitude

            # -------- OVERPASS QUERY --------
            query = f"""
            [out:json];
            (
              node["healthcare"="psychologist"](around:2000,{lat},{lon});
              node["healthcare"="psychiatrist"](around:2000,{lat},{lon});
              node["healthcare"="mental_health"](around:2000,{lat},{lon});
              node["amenity"="clinic"](around:2000,{lat},{lon});
              node["amenity"="hospital"](around:2000,{lat},{lon});
            );
            out body;
            """

            try:
                response = requests.post(
                    "https://overpass-api.de/api/interpreter",
                    data=query,
                    timeout=25
                ).json()
            except:
                st.error("⚠️ Unable to fetch locations right now.")
                st.stop()

            m = folium.Map(location=[lat, lon], zoom_start=12)
            results = []

            for place in response.get("elements", []):
                tags = place.get("tags", {})
                name = tags.get("name", "Mental Health Centre")
                phone = tags.get("phone", tags.get("contact:phone", "Not Available"))
                lat_p, lon_p = place["lat"], place["lon"]

                results.append([name, phone, city])

                folium.Marker(
                    [lat_p, lon_p],
                    popup=f"<b>{name}</b><br>📞 {phone}",
                    icon=folium.Icon(color="pink", icon="plus-sign")
                ).add_to(m)

            folium_static(m)

            if results:
                st.markdown("### 📋 Available Centres ")
                st.table(pd.DataFrame(
                    results,
                    columns=["Centre / Hospital Name", "Contact", "City"]
                ))
            else:
                st.warning("⚠️ No specific counsellors found, showing nearby hospitals instead.")

        if st.button("⬅ Back", key="mental_back_support"):
            st.session_state.mental_page = "main"



    # ================= MINDFULNESS =================
    elif st.session_state.mental_page == "mindfulness":
        st.markdown("<h2>🌿 Mindfulness</h2>", unsafe_allow_html=True)

        st.markdown("""
        <p style="font-size:18px;">
        Mindfulness helps you slow down, breathe, and stay present 🌸
        </p>
        """, unsafe_allow_html=True)

        st.video("https://www.youtube.com/watch?v=inpok4MKVLM")

        st.markdown("""
        ### 🧘 Simple Practices
        - Deep breathing (5 minutes)
        - Gratitude reflection
        - Body scan before sleep
        - Mindful walking
        """)

        if st.button("⬅ Back", key="mental_back_mindfulness"):
            st.session_state.mental_page = "main"

        
    # ================= JOURNAL =================
    elif st.session_state.mental_page == "journal":
        st.markdown("<h2>📓 Mood Journal</h2>", unsafe_allow_html=True)

        mood = st.selectbox(
            "How are you feeling today?",
            ["😊 Happy", "😐 Neutral", "😔 Sad", "😡 Angry", "😰 Anxious"]
        )

        text = st.text_area("Write your thoughts:")

        if st.button("💾 Save Entry"):
            st.session_state.journal_entries.append({
                "date": datetime.date.today().strftime("%d-%m-%Y"),
                "mood": mood,
                "text": text
            })
            st.success("Journal entry saved!")

        if st.session_state.journal_entries:
            st.table(pd.DataFrame(st.session_state.journal_entries))

        if st.button("📄 Export Journal as PDF"):
            file_name = "Mood_Journal.pdf"
            c = canvas.Canvas(file_name, pagesize=A4)
            y = 800

            for e in st.session_state.journal_entries:
                c.drawString(40, y, f"{e['date']} | {e['mood']}")
                y -= 20
                c.drawString(40, y, e["text"])
                y -= 40
                if y < 100:
                    c.showPage()
                    y = 800

            c.save()

            with open(file_name, "rb") as f:
                st.download_button("⬇ Download PDF", f, file_name)
    
        if st.button("⬅ Back", key="mental_back_journal"):
            st.session_state.mental_page = "main"


        







