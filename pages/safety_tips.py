
def safety_tips_page():
    import streamlit as st

    # 🌸 Pink background + font styling
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #ff77b1;
        }

        
        h2 {
            font-size: 32px !important;
            font-weight: 700;
            font-color : #000;
        }

        .stMarkdown p, .stMarkdown li {
            font-size: 20px !important;
            line-height: 1.6;
            font-color : #000;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🛡️ Safety Tips & Precautions")

    # 🔽 Select box
    option = st.selectbox(
        "Select a Safety Category",
        [
            "Personal Safety",
            "Location Safety",
            "Digital & Online Safety",
            "Travel Safety",
            "Home Safety",
            "Emergency Situations",
            "Safety for Students & Young Girls",
            "Mental & Emotional Safety"
        ]
    )

    def show_section(image, title, content):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(image, use_container_width=True)
        with col2:
            st.subheader(title)
            st.markdown(content)

    # 🧩 Sections
    if option == "Personal Safety":
        show_section(
            "images/personal.jpg",
            "🚶 Personal Safety",
            """
            - Stay alert and aware of your surroundings  
            - Avoid using headphones at high volume  
            - Walk confidently and maintain strong body language  
            - Avoid isolated or poorly lit areas  
            - Trust your instincts  
            - Carry a personal safety alarm or pepper spray if allowed  
            """
        )

    elif option == "Location Safety":
        show_section(
            "images/location.jpeg",
            "📍 Location Safety",
            """
            - Share your live location with trusted contacts  
            - Inform family or friends before traveling  
            - Memorize important landmarks  
            - Avoid sharing real-time location on social media  
            """
        )

    elif option == "Digital & Online Safety":
        show_section(
            "images/digital.jpeg",
            "📱 Digital & Online Safety",
            """
            - Never share OTPs or passwords  
            - Avoid clicking suspicious links  
            - Enable 2-factor authentication  
            - Block and report cyberbullying  
            """
        )

    elif option == "Travel Safety":
        show_section(
            "images/travel.jpg",
            "🚌 Travel Safety",
            """
            - Prefer well-lit and crowded transport  
            - Sit near families or the driver  
            - Avoid sleeping alone in public transport  
            - Carry emergency cash and a power bank  
            - Save emergency contacts on speed dial  
            """
        )

    elif option == "Home Safety":
        show_section(
            "images/home.jpeg",
            "🏠 Home Safety",
            """
            - Lock doors and windows properly  
            - Verify identity before opening doors  
            - Inform neighbors if you feel unsafe  
            - Keep emergency numbers visible  
            """
        )

    elif option == "Emergency Situations":
        show_section(
            "images/emergency.jpeg",
            "🚨 Emergency Situations",
            """
            - Shout loudly to attract attention  
            - Use emergency numbers **112, 100, 1091**  
            - Move toward public places  
            - Target eyes, nose, or knees if attacked  
            """
        )

    elif option == "Safety for Students & Young Girls":
        show_section(
            "images/safety.jpeg",
            "👧 Safety for Students & Young Girls",
            """
            - Avoid sharing schedules online  
            - Walk in groups  
            - Report suspicious behavior  
            - Learn basic self-defense  
            """
        )

    elif option == "Mental & Emotional Safety":
        show_section(
            "images/mental.jpeg",
            "❤️ Mental & Emotional Safety",
            """
            - Speak up when uncomfortable  
            - Seek help from trusted people  
            - Abuse is never your fault  
            """
        )

    # 🔔 Footer reminder
    st.markdown(
        """
        <div style="
            background-color: rgba(255,255,255,0.35);
            color: black;
            font-size: 22px;
            font-weight: 600;
            padding: 14px 20px;
            border-radius: 12px;
            margin-top: 30px;
        ">
            🔔 Your safety is a priority. Stay alert, informed, and prepared.
        </div>
        """,
        unsafe_allow_html=True
    )



