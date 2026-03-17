def police_station_page():

    import streamlit as st
    from streamlit_geolocation import streamlit_geolocation
    from geopy.distance import geodesic
    from geopy.geocoders import Nominatim
    import requests
    import folium
    from streamlit_folium import st_folium
    import pandas as pd
    from streamlit_folium import folium_static


    # ---------------- PAGE CONFIG ----------------
    # st.set_page_config(layout="wide")

    # ---------------- GLOBAL CSS ----------------
    st.markdown("""
    <style>
    /* App background */
    [data-testid="stAppViewContainer"] {
        background-color: #FF77B1;
    }

    /* Remove white blocks */
    [data-testid="stVerticalBlock"] {
        background: transparent;
    }

    /* Text color */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: white !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #F41C78 !important;
        color: white !important;
        border-radius: 10px;
        font-weight: 600;
        border: none;
    }

    /* Text input */
    .stTextInput input {
        background-color: white !important;
        color: #C2185B !important;
        border: 2px solid #C2185B;
        border-radius: 10px;
        font-weight: 600;
    }

    .stTextInput input::placeholder {
        color: #888888 !important;
    }

    /* Slider */
    .stSlider span {
        color: white !important;
    }

    /* Dataframe */
    .stDataFrame {
        background-color: white;
    }

    /* Fix folium map width */
    iframe {
        width: 100% !important;
    }

    .leaflet-container {
        width: 100% !important;
        height: 500px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- CONSTANTS ----------------
    OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"
    DEFAULT_RADIUS_KM = 5

    # ---------------- FETCH POLICE STATIONS ----------------
    def get_nearby_police(lat, lon, radius_m):
        query = f"""
        [out:json][timeout:25];
        (
            node["amenity"="police"](around:{radius_m},{lat},{lon});
            way["amenity"="police"](around:{radius_m},{lat},{lon});
            relation["amenity"="police"](around:{radius_m},{lat},{lon});
        );
        out center;
        """
        try:
            response = requests.post(OVERPASS_API_URL, data={"data": query})
            data = response.json()
            stations = []

            for element in data.get("elements", []):
                center = element.get("center", {})
                lat_elem = element.get("lat") or center.get("lat")
                lon_elem = element.get("lon") or center.get("lon")

                if lat_elem and lon_elem:
                    stations.append({
                        "name": element.get("tags", {}).get("name", "Unknown"),
                        "lat": lat_elem,
                        "lon": lon_elem,
                        "address": element.get("tags", {}).get("addr:full")
                                   or element.get("tags", {}).get("addr:street")
                                   or "N/A"
                    })
            return stations

        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return []

    # ---------------- MAP DISPLAY ----------------
    def display_map(user_lat, user_lon, stations):
        m = folium.Map(location=[user_lat, user_lon], zoom_start=14)

        folium.Marker(
            [user_lat, user_lon],
            popup="Your Location",
            icon=folium.Icon(color="blue", icon="user")
        ).add_to(m)

        for s in stations:
            folium.Marker(
                [s['lat'], s['lon']],
                popup=f"{s['name']}<br>{s['address']}",
                icon=folium.Icon(color="darkred", icon="shield")
            ).add_to(m)

        # ✅ SAME SIZE & BEHAVIOR AS HOSPITAL MAP
        folium_static(m)

    # ---------------- UI ----------------
    st.title("🚓 Nearby Police Stations (Live Location Enabled)")

    st.subheader("1. Choose your location method")

    if "loc_clicked" not in st.session_state:
        st.session_state.loc_clicked = False

    method = st.radio(
        "Select how you want to provide your location:",
        ["Use Live GPS Location", "Enter City Manually"]
    )

    user_lat = user_lon = None

    # --- LIVE GPS ---
    if method == "Use Live GPS Location":
        st.write("Click below to request live GPS access from your browser.")
        if st.button("📍 Locate Me"):
            st.session_state.loc_clicked = True

        if st.session_state.loc_clicked:
            location = streamlit_geolocation()
            if location and location.get("latitude"):
                user_lat = location["latitude"]
                user_lon = location["longitude"]
                st.success(f"📌 Location: {user_lat:.6f}, {user_lon:.6f}")
            else:
                st.warning("Waiting for GPS permission...")

    # --- MANUAL CITY ---
    else:
        city = st.text_input("Enter city name (e.g., Mumbai, Delhi):")
        if city:
            geolocator = Nominatim(user_agent="police_locator_app")
            loc = geolocator.geocode(city, country_codes="in")
            if loc:
                user_lat, user_lon = loc.latitude, loc.longitude
                st.success(f"{city} → {user_lat:.6f}, {user_lon:.6f}")
            else:
                st.error("City not found.")

    # ---------------- RADIUS ----------------
    st.subheader("2. Select search radius (km)")
    radius_km = st.slider("Search radius", 1, 10, DEFAULT_RADIUS_KM)
    radius_m = radius_km * 1000

    # ---------------- RESULTS ----------------
    if user_lat and user_lon:
        st.subheader(f"🚓 Police Stations within {radius_km} km")
        stations = get_nearby_police(user_lat, user_lon, radius_m)

        if stations:
            for s in stations:
                s["distance_km"] = geodesic(
                    (user_lat, user_lon), (s["lat"], s["lon"])
                ).km

            stations = sorted(stations, key=lambda x: x["distance_km"])

            df = pd.DataFrame([{
                "Name": s["name"],
                "Address": s["address"],
                "Distance (km)": f"{s['distance_km']:.2f}"
            } for s in stations])

            st.dataframe(df, use_container_width=True)

            st.subheader("🗺 Map View")
            display_map(user_lat, user_lon, stations)

        else:
            st.info("No police stations found.")
    else:
        st.info("Provide your location to begin searching.")
# police_station_page()



