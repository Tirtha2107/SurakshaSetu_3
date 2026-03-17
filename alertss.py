# import streamlit as st
# import folium
# from folium.plugins import MarkerCluster, HeatMap
# from streamlit_folium import st_folium
# from datetime import datetime

# # -----------------------------
# # PAGE CONFIG
# # -----------------------------
# st.set_page_config(
#     page_title="SurakshaSetu – Live Safety Map",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# st.title("🛡️ SurakshaSetu – Live Safety Alerts Map")

# # -----------------------------
# # SIDEBAR FILTERS
# # -----------------------------
# st.sidebar.header("🔔 Alert Filters")

# show_sos = st.sidebar.checkbox("🚨 SOS Alerts", True)
# show_crime = st.sidebar.checkbox("⚠️ Unsafe / Crime Areas", True)
# show_weather = st.sidebar.checkbox("🌧️ Weather / Flood Alerts", True)
# show_traffic = st.sidebar.checkbox("🚦 Traffic / Road Issues", True)
# show_safe = st.sidebar.checkbox("🏥 Safe Places", True)
# show_heatmap = st.sidebar.checkbox("🔥 Risk Heatmap", True)

# radius_km = st.sidebar.slider("Alert Radius (km)", 1, 10, 5)

# # -----------------------------
# # USER LOCATION (Demo)
# # Pune coordinates (change if needed)
# # -----------------------------
# user_lat = 18.5204
# user_lon = 73.8567

# # -----------------------------
# # SAMPLE LIVE ALERT DATA
# # -----------------------------
# sos_alerts = [
#     {"lat": 18.523, "lon": 73.858, "msg": "🚨 SOS Triggered", "time": "2 mins ago"},
# ]

# crime_alerts = [
#     {"lat": 18.517, "lon": 73.852, "msg": "⚠️ Harassment Reported"},
#     {"lat": 18.525, "lon": 73.860, "msg": "⚠️ High Risk Area"},
# ]

# weather_alerts = [
#     {"lat": 18.530, "lon": 73.850, "radius": 800, "msg": "🌧️ Heavy Rain Zone"},
# ]

# traffic_alerts = [
#     {"lat": 18.515, "lon": 73.862, "msg": "🚧 Road Block"},
# ]

# safe_places = [
#     {"lat": 18.519, "lon": 73.855, "msg": "🚓 Police Station"},
#     {"lat": 18.522, "lon": 73.860, "msg": "🏥 Hospital"},
# ]

# # Heatmap points (lat, lon)
# risk_points = [
#     [18.517, 73.852],
#     [18.518, 73.853],
#     [18.519, 73.854],
#     [18.525, 73.860],
# ]

# # -----------------------------
# # CREATE MAP
# # -----------------------------
# m = folium.Map(
#     location=[user_lat, user_lon],
#     zoom_start=14,
#     tiles="CartoDB dark_matter"
# )

# # User location
# folium.Marker(
#     [user_lat, user_lon],
#     popup="📍 You are here",
#     icon=folium.Icon(color="blue", icon="user")
# ).add_to(m)

# cluster = MarkerCluster().add_to(m)

# # -----------------------------
# # ADD ALERT MARKERS
# # -----------------------------
# if show_sos:
#     for a in sos_alerts:
#         folium.Marker(
#             [a["lat"], a["lon"]],
#             popup=f"{a['msg']}<br>⏱ {a['time']}",
#             icon=folium.Icon(color="red", icon="exclamation-sign")
#         ).add_to(cluster)

# if show_crime:
#     for a in crime_alerts:
#         folium.Marker(
#             [a["lat"], a["lon"]],
#             popup=a["msg"],
#             icon=folium.Icon(color="darkred", icon="warning-sign")
#         ).add_to(cluster)

# if show_weather:
#     for a in weather_alerts:
#         folium.Circle(
#             location=[a["lat"], a["lon"]],
#             radius=a["radius"],
#             popup=a["msg"],
#             color="blue",
#             fill=True,
#             fill_opacity=0.3
#         ).add_to(m)

# if show_traffic:
#     for a in traffic_alerts:
#         folium.Marker(
#             [a["lat"], a["lon"]],
#             popup=a["msg"],
#             icon=folium.Icon(color="orange", icon="road")
#         ).add_to(cluster)

# if show_safe:
#     for a in safe_places:
#         folium.Marker(
#             [a["lat"], a["lon"]],
#             popup=a["msg"],
#             icon=folium.Icon(color="green", icon="plus-sign")
#         ).add_to(cluster)

# if show_heatmap:
#     HeatMap(risk_points, radius=25).add_to(m)

# # -----------------------------
# # DISPLAY MAP
# # -----------------------------
# st_folium(m, width=1400, height=650)

# # -----------------------------
# # FOOTER INFO
# # -----------------------------
# st.markdown(
#     f"""
#     ⏰ **Last Updated:** {datetime.now().strftime('%d %b %Y, %I:%M %p')}  
#     🛡️ SurakshaSetu – *Empowering Women • Securing Everyone*
#     """
# )


def Live_Alerts():
    import streamlit as st
    from streamlit_geolocation import streamlit_geolocation
    import folium
    from streamlit_folium import st_folium
    import pandas as pd
    import random

    st.set_page_config(page_title="Live Alerts & Location", layout="wide")
    st.title("📍 Live Emergency & Crime Alerts")

    # --- Dummy alerts generator (replace with real API) ---
    def get_real_alerts(center_lat, center_lon, n=15):
        alert_types = ['Fire', 'Crime', 'Flood', 'Traffic', 'Medical Emergency']
        alerts = []
        for _ in range(n):
            alert_type = random.choice(alert_types)
            lat = center_lat + random.uniform(-0.02, 0.02)
            lon = center_lon + random.uniform(-0.02, 0.02)
            alerts.append({
                "type": alert_type,
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "details": f"[{alert_type}] Reported at {lat:.4f}, {lon:.4f}."
            })
        return alerts

    # --- Session state defaults ---
    if "user_location" not in st.session_state:
        st.session_state.user_location = None   # [lat, lon] or None
        st.session_state.alerts = []
        st.session_state.loc_clicked = False

    # --- Locate Me button (user must click to request browser geolocation) ---
    st.markdown("Click the button below to let the browser share your location.")
    if st.button("📍 Locate Me"):
        st.session_state.loc_clicked = True

    # If user clicked, request browser location (streamlit_geolocation shows the browser prompt)
    if st.session_state.loc_clicked:
        location = streamlit_geolocation()
        if location and location.get("latitude") is not None and location.get("longitude") is not None:
            lat = location["latitude"]
            lon = location["longitude"]
            # Save and fetch alerts
            changed = (st.session_state.user_location is None) or (abs(lat - st.session_state.user_location[0]) > 1e-3 or abs(lon - st.session_state.user_location[1]) > 1e-3)
            st.session_state.user_location = [lat, lon]
            if changed or not st.session_state.alerts:
                st.session_state.alerts = get_real_alerts(lat, lon)
            st.success(f"Location received: {lat:.6f}, {lon:.6f}")
        else:
            st.warning("Waiting for browser to provide location. Make sure you click 'Allow' in the prompt.")

    # Show map & controls only if we have a location
    if st.session_state.user_location:
        current_user_lat, current_user_lon = st.session_state.user_location

        # Simple refresh button to re-fetch alerts (avoids full page rerun)
        if st.button("🔄 Refresh Alerts"):
            st.session_state.alerts = get_real_alerts(current_user_lat, current_user_lon)

        # Filters (main page)
        all_alert_types = ['Fire', 'Crime', 'Flood', 'Traffic', 'Medical Emergency']
        selected_alert_types = st.multiselect(
            "Select alert types to display:",
            options=all_alert_types,
            default=all_alert_types
        )

        filtered_alerts = [a for a in st.session_state.alerts if a["type"] in selected_alert_types]

        # Build map
        m = folium.Map(location=[current_user_lat, current_user_lon], zoom_start=14)
        folium.Marker(
            [current_user_lat, current_user_lon],
            tooltip="Your Current Location",
            icon=folium.Icon(color="green", icon="user", prefix='fa')
        ).add_to(m)

        color_map = {"Fire": "red", "Crime": "blue", "Flood": "orange", "Traffic": "purple", "Medical Emergency": "darkred"}
        icon_map = {"Fire": "fire", "Crime": "exclamation-triangle", "Flood": "tint", "Traffic": "car", "Medical Emergency": "heartbeat"}

        for alert in filtered_alerts:
            folium.Marker(
                [alert["latitude"], alert["longitude"]],
                tooltip=f"{alert['type']} Alert",
                popup=folium.Popup(alert["details"], max_width=300),
                icon=folium.Icon(
                    color=color_map.get(alert["type"], "gray"),
                    icon=icon_map.get(alert["type"], "info"),
                    prefix='fa'
                )
            ).add_to(m)

        st.subheader("🗺 Map of Live Alerts")
        st_folium(m, width=1000, height=500)

        st.subheader("🧾 Recent Alerts Nearby")
        with st.expander(f"View details for {len(filtered_alerts)} alerts"):
            if filtered_alerts:
                df = pd.DataFrame(filtered_alerts)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No alerts of the selected types found in this area.")
    else:
        st.info("Map will appear after you click '📍 Locate Me' and allow location access.")

Live_Alerts()