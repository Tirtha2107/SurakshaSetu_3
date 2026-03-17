

import streamlit as st
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ff77b1;  /* Pink background */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def videos_page():
    st.markdown("## 🎬 Safety Videos")
    st.markdown(
        "Learn how to stay safe and protect yourself with these informative videos. "
        "These resources cover self-defense tips, awareness strategies, and practical safety advice."
    )

    # Video 1
    st.markdown("### 🛡️ Personal Safety Tips")
    st.markdown(
        "This video provides practical tips for staying safe in public spaces, recognizing potential threats, and responding effectively in risky situations."
    )
    st.video("https://youtu.be/wt2kYVhFUxQ?si=YVf57uBm6hlHcXF5")

    st.markdown("---")  # Divider between videos

    # Video 2
    st.markdown("### 🚨 Self-Defense Techniques")
    st.markdown(
        "Learn some basic self-defense techniques that can help you protect yourself during emergencies. "
        "The video demonstrates simple moves anyone can practice safely."
    )
    st.video("https://youtu.be/jME_NYuPeRY?si=gXhmpWXFNoj2420y")

    st.markdown("---")
    st.markdown(
        "💬 **Tip:** Watching these videos and practicing awareness can make a big difference in personal safety. "
        "Always stay alert and trust your instincts."
    )

# Call the function
# videos_page()
