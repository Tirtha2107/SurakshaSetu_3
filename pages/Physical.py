def physical():
    import streamlit as st
    import pandas as pd
    import datetime
    import random
    import time

    # ------------------- COLORS -------------------
    LIGHT_PINK = "#FF77B1"
    DARK_PINK = "#F41C78"
    BUTTON_HOVER_PINK = "#F41C78"

    # ------------------- SESSION STATE (NAMESPACED) -------------------
    if "physical_page" not in st.session_state:
        st.session_state.physical_page = "main"

    if "steps_done" not in st.session_state:
        st.session_state.steps_done = 0
    if "water_intake" not in st.session_state:
        st.session_state.water_intake = 0
    if "activity_log" not in st.session_state:
        st.session_state.activity_log = pd.DataFrame(columns=["Date", "Activity", "Minutes"])
    if "exercise_log" not in st.session_state:
        st.session_state.exercise_log = pd.DataFrame(columns=["Date", "Exercise", "Completed"])
    if "water_log" not in st.session_state:
        st.session_state.water_log = pd.DataFrame(columns=["Date", "Water_ml"])
    if "tip_streak" not in st.session_state:
        st.session_state.tip_streak = 0
    if "tip_history" not in st.session_state:
        st.session_state.tip_history = []
    if "custom_contacts" not in st.session_state:
        st.session_state.custom_contacts = {}
    if "last_period" not in st.session_state:
        st.session_state.last_period = datetime.date.today()
    if "cycle_length" not in st.session_state:
        st.session_state.cycle_length = 28
    if "symptoms" not in st.session_state:
        st.session_state.symptoms = ""

    # ------------------- CSS -------------------
    st.markdown(f"""
    <style>
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
        transition: 0.2s;
    }}
    .stButton>button:hover {{
        background-color: {BUTTON_HOVER_PINK};
        transform: scale(1.05);
    }}
    h1, h2 {{ color: {DARK_PINK}; font-weight: 800; }}
    </style>
    """, unsafe_allow_html=True)

    # =================== MAIN MENU ===================
    if st.session_state.physical_page == "main":
        st.markdown("<h1>💪 Physical Health</h1>", unsafe_allow_html=True)
        st.write("Select a feature to explore:")

        c1, c2 = st.columns(2)
        c3, c4 = st.columns(2)
        c5, c6 = st.columns(2)

        def nav(col, label, page):
            with col:
                if st.button(label):
                    st.session_state.physical_page = page

        nav(c1, "🏃‍♀️ Activity Tracker", "activity")
        nav(c2, "🧘‍♀️ Exercise Library", "exercise")
        nav(c3, "💧 Water & Diet", "water")
        nav(c4, "🩸 Menstrual Cycle", "menstrual")
        nav(c5, "📚 Health Tips", "tips")
        nav(c6, "🚨 Emergency Check", "emergency")

    # =================== ACTIVITY ===================
    elif st.session_state.physical_page == "activity":
        st.markdown("<h2>🏃‍♀️ Activity Tracker</h2>", unsafe_allow_html=True)

        steps = st.number_input("Steps today:", 0, 50000, st.session_state.steps_done, 100)
        st.session_state.steps_done = steps
        goal = st.number_input("Daily goal:", 1000, 50000, 10000, 500)

        st.progress(min(steps / goal, 1.0))
        st.info(f"🔥 Calories burned: {steps * 0.04:.1f} kcal")

        if st.button("⬅ Back"):
            st.session_state.physical_page = "main"

    # =================== EXERCISE ===================
    elif st.session_state.physical_page == "exercise":
        st.markdown("<h2>🧘‍♀️ Exercise Library</h2>", unsafe_allow_html=True)

        ex = st.selectbox("Exercise Type", ["Yoga", "Meditation", "Cardio"])
        diff = st.radio("Difficulty", ["Easy", "Medium", "Hard"])

        videos = {
            "Yoga": {
                "Easy": "https://www.youtube.com/watch?v=v7AYKMP6rOE",
                "Medium": "https://www.youtube.com/watch?v=4pKly2JojMw",
                "Hard": "https://youtu.be/Eml2xnoLpYE"
            },
            "Meditation": {
                "Easy": "https://www.youtube.com/watch?v=inpok4MKVLM",
                "Medium": "https://www.youtube.com/watch?v=ZToicYcHIOU",
                "Hard": "https://www.youtube.com/watch?v=O-6f5wQXSu8"
            },
            "Cardio": {
                "Easy": "https://www.youtube.com/watch?v=ml6cT4AZdqI",
                "Medium": "https://www.youtube.com/watch?v=50kH47ZztHs",
                "Hard": "https://www.youtube.com/watch?v=IT94xC35u6k"
            }
        }

        st.video(videos[ex][diff])

        if st.button("⬅ Back"):
            st.session_state.physical_page = "main"

  

    # =================== WATER ===================
    elif st.session_state.physical_page == "water":
        st.markdown("<h2>💧 Water & Diet</h2>", unsafe_allow_html=True)

        target_water = st.number_input(
            "Daily Water Target (ml):",
            500,
            5000,
            2000,
            step=100
        )

        st.write("### Current Water Intake")
        st.write(f"💧 **{st.session_state.water_intake} ml**")

        # -------- QUICK BUTTONS --------
        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button("+250 ml"):
                st.session_state.water_intake += 250
                st.rerun()

        with c2:
            if st.button("+500 ml"):
                st.session_state.water_intake += 500
                st.rerun()

        with c3:
            if st.button("Reset"):
                st.session_state.water_intake = 0
                st.rerun()

        water = st.session_state.water_intake

        # -------- STATUS --------
        remaining = target_water - water

        st.subheader("💧 Hydration Status")

        if remaining > 0:
            st.warning(f"You should drink **{remaining} ml** more water today.")
            st.info("💡 Tip: Drink water every 30 minutes.")

        elif remaining == 0:
            st.success("✅ Perfect! You reached your daily water goal.")

        else:
            extra = abs(remaining)
            st.success(f"🎉 You drank **{extra} ml extra water** today.")

        # -------- PROGRESS BAR --------
        progress = min(water / target_water, 1.0)
        st.progress(progress)

        # -------- HYDRATION LEVEL --------
        if water < target_water * 0.5:
            st.error("⚠ Hydration Level: Low")

        elif water < target_water:
            st.warning("🙂 Hydration Level: Good")

        else:
            st.success("💧 Hydration Level: Excellent")

        tips = [
            "Drink a glass of water after waking up.",
            "Carry a water bottle with you.",
            "Eat fruits like watermelon and cucumber.",
            "Drink water before meals.",
            "Set reminders every hour to drink water."
        ]

        st.info("💡 Hydration Tip: " + random.choice(tips))

        if st.button("⬅ Back"):
            st.session_state.physical_page = "main"


    # =================== MENSTRUAL ===================
    elif st.session_state.physical_page == "menstrual":
        st.markdown("<h2>🩸 Menstrual Cycle Tracker</h2>", unsafe_allow_html=True)

        # -------- INPUTS --------
        last = st.date_input("Last Period Date", st.session_state.last_period)
        cycle = st.number_input("Cycle Length (days)", 21, 35, st.session_state.cycle_length)

        st.session_state.last_period = last
        st.session_state.cycle_length = cycle

        # -------- NEXT PERIOD --------
        next_period = last + datetime.timedelta(days=cycle)
        st.success(f"📅 Next Expected Period: {next_period}")

        # -------- OVULATION --------
        ovulation_day = next_period - datetime.timedelta(days=14)
        st.info(f"🌸 Predicted Ovulation Day: {ovulation_day}")

        # -------- FERTILE WINDOW --------
        fertile_start = ovulation_day - datetime.timedelta(days=2)
        fertile_end = ovulation_day + datetime.timedelta(days=2)

        st.write(f"💗 Fertile Window: {fertile_start} to {fertile_end}")

        # -------- DAYS REMAINING --------
        today = datetime.date.today()
        days_left = (next_period - today).days

        if days_left > 0:
            st.warning(f"⏳ {days_left} days left until your next period.")
        else:
            st.error("⚠ Your expected period date has arrived or passed.")

        # -------- CURRENT CYCLE DAY --------
        cycle_day = (today - last).days + 1
        st.write(f"📊 Current Cycle Day: {cycle_day}")

        # -------- PHASE DETECTION --------
        if cycle_day <= 5:
            phase = "Menstrual Phase"
            message = "Your period is ongoing. Rest well and stay hydrated."

        elif cycle_day <= 13:
            phase = "Follicular Phase"
            message = "Energy levels may increase. Good time for exercise."

        elif cycle_day == 14:
            phase = "Ovulation Phase"
            message = "Ovulation period. Fertility is highest."

        elif cycle_day <= cycle:
            phase = "Luteal Phase"
            message = "Body preparing for next cycle. Eat balanced food."

        else:
            phase = "Cycle Restart"
            message = "Your next cycle may begin soon."

        st.success(f"🌸 Current Phase: {phase}")
        st.info(message)

        # -------- SYMPTOMS TRACKER --------
        st.subheader("🩺 Track Symptoms")

        symptoms = st.text_area(
            "Enter symptoms (cramps, mood swings, headache, etc.)",
            st.session_state.symptoms
        )

        if st.button("Save Symptoms"):
            st.session_state.symptoms = symptoms
            st.success("Symptoms saved successfully!")

        # -------- PERIOD HEALTH TIPS --------
        tips = [
            "Drink warm water to reduce cramps.",
            "Light yoga can help reduce menstrual pain.",
            "Eat iron-rich foods like spinach and dates.",
            "Stay hydrated during your cycle.",
            "Use a heating pad to reduce cramps."
        ]

        st.info("💡 Period Tip: " + random.choice(tips))

        if st.button("⬅ Back"):
            st.session_state.physical_page = "main"

    

    # =================== TIPS ===================
    elif st.session_state.physical_page == "tips":
        st.markdown("<h2>📚 Health Tips</h2>", unsafe_allow_html=True)

        # -------- RANDOM HEALTH TIP (OLD FEATURE) --------
        st.subheader("🌟 Quick Health Tip")

        tips = [
            "Drink water regularly 💧",
            "Walk at least 30 minutes daily 🚶‍♀️",
            "Stretch your body every morning 🧘‍♀️",
            "Sleep 7–8 hours every night 😴",
            "Eat fresh fruits and vegetables 🍎🥦",
            "Take small breaks while working 💻"
        ]

        if st.button("Show Random Health Tip"):
            tip = random.choice(tips)
            st.info(tip)
            st.session_state.tip_streak += 1
            st.session_state.tip_history.append(tip)

        # -------- AI HEALTH TIP GENERATOR --------
        st.subheader("🤖 AI Health Tip Generator")

        mood = st.selectbox(
            "How are you feeling today?",
            ["Happy", "Tired", "Stressed", "Low Energy"]
        )

        goal = st.selectbox(
            "Your health goal",
            ["Stay Fit", "Lose Weight", "Improve Sleep", "Reduce Stress"]
        )

        if st.button("Generate AI Tip"):

            if mood == "Tired":
                tip = "Take a short walk and drink water. Light stretching can improve energy."

            elif mood == "Stressed":
                tip = "Practice deep breathing or meditation for 5 minutes."

            elif mood == "Low Energy":
                tip = "Eat a healthy snack like fruits or nuts and drink water."

            else:
                tip = "Great! Continue maintaining your healthy habits."

            if goal == "Lose Weight":
                tip += " Try doing cardio exercise for 30 minutes."

            elif goal == "Improve Sleep":
                tip += " Avoid screens before sleeping."

            elif goal == "Reduce Stress":
                tip += " Listening to calm music may help."

            elif goal == "Stay Fit":
                tip += " Continue regular exercise and balanced diet."

            st.success("💡 AI Suggestion:")
            st.write(tip)

            st.session_state.tip_streak += 1
            st.session_state.tip_history.append(tip)

        # -------- TIP STREAK --------
        st.write(f"🔥 Tips viewed today: {st.session_state.tip_streak}")

        # -------- TIP HISTORY --------
        if st.session_state.tip_history:
            st.subheader("📜 Tip History")
            for t in st.session_state.tip_history[-5:]:
                st.write("•", t)

        # -------- MOTIVATIONAL QUOTES --------
        quotes = [
            "Health is the greatest wealth.",
            "Take care of your body. It's the only place you have to live.",
            "A healthy outside starts from the inside.",
            "Small healthy habits make a big difference."
        ]

        st.info("🌟 Motivation: " + random.choice(quotes))

        if st.button("⬅ Back"):
            st.session_state.physical_page = "main"



    # =================== EMERGENCY ===================
    elif st.session_state.physical_page == "emergency":
        st.markdown("<h2>🚨 Emergency</h2>", unsafe_allow_html=True)

        contacts = {
            "Police": "100",
            "Ambulance": "102",
            "Women Helpline": "1091",
            "Emergency": "112"
        }

        for k, v in contacts.items():
            st.markdown(f"[📞 {k}: {v}](tel:{v})")

        if st.button("⬅ Back"):
            st.session_state.physical_page = "main"

      