

def live():
    import streamlit as st
    import folium
    from folium.plugins import HeatMap, Fullscreen
    from streamlit_folium import st_folium
    from streamlit_geolocation import streamlit_geolocation
    import random

    # -----------------------------
    # 2. CUSTOM STYLING
    # -----------------------------
    st.markdown("""
    <style>
        .stApp { 
            background-color: #FF77B1; 
        }

        .stat-box {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-left: 5px solid #F41C78;
        }

        h2, h3, p, div { 
            color: white; 
        }

        .stat-value { 
            font-size: 26px; 
            font-weight: 800; 
            color: #333333; 
        }

        .stat-label { 
            font-size: 14px; 
            color: #666666; 
            font-weight: 600;
        }

        .stSlider > div > div > div > div {
            background-color: #F41C78;
        }

        /* 🔴 Locate Me Button Color */
        div.stButton > button {
            background-color: #E53935 !important;
            color: white !important;
            font-weight: 700;
            border-radius: 8px;
        }

        div.stButton > button:hover {
            background-color: #C62828 !important;
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # -----------------------------
    # 3. SESSION STATE
    # -----------------------------
    if "user_location" not in st.session_state:
        st.session_state.user_location = None
        st.session_state.loc_clicked = False

    # -----------------------------
    # 4. MOCK ALERT DATA
    # -----------------------------
    def get_data(lat, lon, radius_km):
        spread = (radius_km / 111.0) * 0.8

        def offset():
            return random.uniform(-spread, spread)

        return {
            "sos": [
                {"lat": lat + offset(), "lon": lon + offset(), "msg": "🚨 SOS Alert"},
                {"lat": lat + offset(), "lon": lon + offset(), "msg": "🚨 SOS Alert"}
            ],
            "crime": [
                {"lat": lat + offset(), "lon": lon + offset(), "msg": "⚠️ Theft"},
                {"lat": lat + offset(), "lon": lon + offset(), "msg": "⚠️ Harassment"},
                {"lat": lat + offset(), "lon": lon + offset(), "msg": "⚠️ Poor Lighting"},
                {"lat": lat + offset(), "lon": lon + offset(), "msg": "⚠️ Pickpocketing"}
            ],
            "safe": [
                {"lat": lat + offset(), "lon": lon + offset(), "msg": "🚓 Police Station"},
                {"lat": lat + offset(), "lon": lon + offset(), "msg": "🏥 Hospital"}
            ],
            "heat": [[lat + offset(), lon + offset()] for _ in range(30)]
        }

    # -----------------------------
    # 5. MAIN MAP RENDER
    # -----------------------------
    def render_live_map():

        st.markdown(
            "<h2 style='text-align:center;font-weight:900;"
            "text-shadow:2px 2px 4px rgba(0,0,0,0.3);'>"
            "🛡️ Live Safety Intelligence</h2>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([1, 3])

        # ---------------- LEFT PANEL ----------------
        with col1:
            st.markdown("### 📡 Live Location")

            if st.button("📍 Locate Me"):
                st.session_state.loc_clicked = True

            if st.session_state.loc_clicked:
                location = streamlit_geolocation()

                if location and location.get("latitude") and location.get("longitude"):
                    st.session_state.user_location = (
                        location["latitude"],
                        location["longitude"]
                    )
                    st.success("✅ Live location detected")
                else:
                    st.warning("⏳ Waiting for location permission...")

            if not st.session_state.user_location:
                st.info("📍 Click **Locate Me** to load the map")
                return

            user_lat, user_lon = st.session_state.user_location

            radius_km = st.slider("🔍 Scan Radius (km)", 1, 10, 3)

            data = get_data(user_lat, user_lon, radius_km)

            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{len(data['sos'])}</div>
                <div class="stat-label">🚨 Active SOS Alerts</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{len(data['crime'])}</div>
                <div class="stat-label">⚠️ Crime Reports</div>
            </div>
            <div class="stat-box" style="border-left-color:#00c4ff;">
                <div class="stat-value">{len(data['safe'])}</div>
                <div class="stat-label">🏥 Safe Locations</div>
            </div>
            """, unsafe_allow_html=True)

            st.info("ℹ️ Toggle map layers for SOS, Crime, Safe zones & Heatmap")

        # ---------------- RIGHT PANEL ----------------
        with col2:
            m = folium.Map(
                location=[user_lat, user_lon],
                zoom_start=13,
                tiles="CartoDB dark_matter"
            )

            fg_sos = folium.FeatureGroup(name="🚨 SOS Alerts")
            fg_crime = folium.FeatureGroup(name="⚠️ Crime Reports")
            fg_safe = folium.FeatureGroup(name="🏥 Safe Places")
            fg_heat = folium.FeatureGroup(name="🔥 Heatmap")

            for item in data["sos"]:
                folium.Marker(
                    [item["lat"], item["lon"]],
                    popup=item["msg"],
                    icon=folium.Icon(color="red", icon="bell", prefix="fa")
                ).add_to(fg_sos)

                folium.CircleMarker(
                    [item["lat"], item["lon"]],
                    radius=15,
                    color="red",
                    fill=True,
                    fill_opacity=0.4
                ).add_to(fg_sos)

            for item in data["crime"]:
                folium.Marker(
                    [item["lat"], item["lon"]],
                    popup=item["msg"],
                    icon=folium.Icon(color="orange", icon="warning-sign")
                ).add_to(fg_crime)

            for item in data["safe"]:
                folium.Marker(
                    [item["lat"], item["lon"]],
                    popup=item["msg"],
                    icon=folium.Icon(color="green", icon="home")
                ).add_to(fg_safe)

            HeatMap(data["heat"], radius=25).add_to(fg_heat)

            fg_sos.add_to(m)
            fg_crime.add_to(m)
            fg_safe.add_to(m)
            fg_heat.add_to(m)

            folium.Marker(
                [user_lat, user_lon],
                popup="You",
                icon=folium.Icon(color="blue", icon="user", prefix="fa")
            ).add_to(m)

            folium.Circle(
                [user_lat, user_lon],
                radius=radius_km * 1000,
                color="#00c4ff",
                fill=True,
                fill_opacity=0.05
            ).add_to(m)

            folium.LayerControl(collapsed=False).add_to(m)
            Fullscreen().add_to(m)

            st_folium(m, height=600, width="100%", returned_objects=[])

    render_live_map()
