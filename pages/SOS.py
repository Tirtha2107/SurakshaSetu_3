def sos_page():
    import streamlit as st
    from twilio.rest import Client
    from streamlit_geolocation import streamlit_geolocation
    import time

    st.title("🚨 Emergency SOS")
    st.warning("Press the SOS button to alert your emergency contacts.")

    # Get Location
    location = streamlit_geolocation()

    if location and location["latitude"]:
        lat = location["latitude"]
        lon = location["longitude"]
        location_link = f"https://maps.google.com/?q={lat},{lon}"
    else:
        location_link = "Location unavailable"

    # Show Map
    if location and location["latitude"]:
        st.subheader("📍 Your Current Location")
        st.map({"lat":[lat], "lon":[lon]})

    # SOS Button
    if st.button("🚨 ACTIVATE SOS", use_container_width=True):

        st.error("🚨 SOS ACTIVATED")


        account_sid = "ACa42b9b2c37fad3f6885b10fd5a361c7c"
        auth_token = "178b29761feefb01e13c2f1daf0873d6"


        client = Client(account_sid, auth_token)

        from_number = "+13022615581"

        numbers = [
            "+919326940651"
        ]

        sms_message = f"""
🚨 SOS ALERT from SurakshaSetu 🚨
Emergency! 
📍 Live Location:
{location_link}
please reach immediately.
"""

        for number in numbers:
            try:

                # Send SMS
                client.messages.create(
                    body=sms_message,
                    from_=from_number,
                    to=number
                )

                # Make Call
                client.calls.create(
                    to=number,
                    from_=from_number,
                    twiml=f"""
<Response>
<Say voice="alice">
Emergency alert from Suraksha Setu.
Your family member is in danger.
Please check the message for the live location.
The location link has been sent via SMS.
</Say>
</Response>
"""
                )

                time.sleep(1)

            except Exception as e:
                st.error(e)

        st.success("✅ SOS Alert Sent Successfully")