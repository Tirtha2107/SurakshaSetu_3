



def hospital_page():
    import streamlit as st
    from streamlit_geolocation import streamlit_geolocation
    from geopy.distance import geodesic
    from geopy.geocoders import Nominatim
    import requests
    import folium
    from streamlit_folium import folium_static
    import pandas as pd

    # ---------------- Page Config ----------------
    # st.set_page_config(page_title="Nearby Hospitals", layout="wide")

    # ---------------- UI / THEME (NO LOGIC CHANGE) ----------------
    st.markdown("""
    <style>
        /* Background */
        .stApp {
            background-color: #FF77B1;
            color: white;
        }

        /* Headings */
        h1, h2, h3, h4, h5, h6 {
            color: white !important;
            font-weight: 700;
        }

        /* General text */
        label, p, span, div {
            color: white !important;
        }

        /* ---------------- INPUT FIX ---------------- */
        .stTextInput input {
            background-color: #FFFFFF !important;
            color: #C2185B !important;
            border-radius: 10px;
            border: 2px solid #C2185B;
            font-weight: 600;
        }

        .stTextInput input::placeholder {
            color: #999999 !important;
        }

        /* Radio */
        .stRadio label {
            color: white !important;
        }

        /* Slider */
        .stSlider label {
            color: white !important;
        }

        /* Default Buttons */
        .stButton button {
            background-color: #F41C78;
            color: white;
            border-radius: 12px;
            border: none;
            font-weight: 600;
            padding: 0.6em 1.2em;
        }

        .stButton button:hover {
            background-color: #F41C78;
        }

        /* Dark Pink Locate Me Button */
        div[data-testid="stButton"] > button:has(span:contains("Locate Me")) {
            background-color: #F41C78 !important;
        }

        /* Dataframe */
        .stDataFrame {
            background-color: rgba(255,255,255,0.18);
            color: white;
        }

        /* Alerts */
        .stAlert {
            background-color: rgba(255,255,255,0.25);
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

    # -------- Constants --------
    OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"
    DEFAULT_RADIUS_KM = 2

    # -------- Get Hospitals --------
    def get_nearby_hospitals(lat, lon, radius_m):
        query = f"""
        [out:json][timeout:25];
        (
          node["amenity"="hospital"](around:{radius_m},{lat},{lon});
          way["amenity"="hospital"](around:{radius_m},{lat},{lon});
          relation["amenity"="hospital"](around:{radius_m},{lat},{lon});
        );
        out center;
        """
        try:
            response = requests.post(OVERPASS_API_URL, data=query)
            data = response.json()
            hospitals = []

            for element in data.get('elements', []):
                center = element.get('center', {})
                lat_elem = element.get('lat') or center.get('lat')
                lon_elem = element.get('lon') or center.get('lon')

                if lat_elem and lon_elem:
                    hospitals.append({
                        "name": element.get("tags", {}).get("name", "Unknown"),
                        "lat": lat_elem,
                        "lon": lon_elem,
                        "address": element.get("tags", {}).get("addr:street", "N/A")
                    })
            return hospitals

        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return []

    # -------- Map --------
    def display_map(user_lat, user_lon, hospitals):
        m = folium.Map(location=[user_lat, user_lon], zoom_start=14)

        folium.Marker(
            [user_lat, user_lon],
            popup="Your Location",
            icon=folium.Icon(color="blue", icon="user")
        ).add_to(m)

        for h in hospitals:
            folium.Marker(
                [h["lat"], h["lon"]],
                popup=f"{h['name']}<br>{h['address']}",
                icon=folium.Icon(color="red", icon="plus")
            ).add_to(m)

        folium_static(m)

    # ---------------- UI ----------------
    st.title("🏥 Nearby Hospitals (Live Location Enabled)")

    st.subheader("📍 Choose your location method")

    if "loc_clicked" not in st.session_state:
        st.session_state.loc_clicked = False

    method = st.radio(
        "Select how you want to provide your location:",
        ["Use Live GPS Location", "Enter City Manually"]
    )

    user_lat = user_lon = None

    # -------- Live GPS --------
    if method == "Use Live GPS Location":
        if st.button("📍 Locate Me"):
            st.session_state.loc_clicked = True

        if st.session_state.loc_clicked:
            location = streamlit_geolocation()

            if location and location.get("latitude"):
                user_lat = location["latitude"]
                user_lon = location["longitude"]
                st.success("📌 Live GPS location detected")
            else:
                st.warning("Waiting for GPS permission...")

    # -------- Manual City --------
    else:
        city = st.text_input("Enter city name (e.g., Mumbai, Delhi)")

        if city:
            geolocator = Nominatim(user_agent="hospital_locator_app")
            loc = geolocator.geocode(city, country_codes='in')

            if loc:
                user_lat, user_lon = loc.latitude, loc.longitude
                st.success(f"📍 {city} located")
            else:
                st.error("Could not find that city. Try another name.")

    # ---------- RADIUS ----------
    st.subheader("📏 Select search radius (km)")
    radius_km = st.slider("Search radius", 1, 10, DEFAULT_RADIUS_KM)
    radius_m = radius_km * 1000

    # ---------- FETCH & DISPLAY ----------
    if user_lat and user_lon:
        st.subheader(f"🏥 Hospitals within {radius_km} km")

        hospitals = get_nearby_hospitals(user_lat, user_lon, radius_m)

        if hospitals:
            for h in hospitals:
                h["distance_km"] = geodesic(
                    (user_lat, user_lon), (h["lat"], h["lon"])
                ).km

            hospitals = sorted(hospitals, key=lambda x: x["distance_km"])

            df = pd.DataFrame([{
                "Name": h["name"],
                "Address": h["address"],
                "Distance (km)": f"{h['distance_km']:.2f}"
            } for h in hospitals])

            st.dataframe(df, use_container_width=True)

            st.subheader("🗺 Map View")
            display_map(user_lat, user_lon, hospitals)

        else:
            st.info("No hospitals found in this radius.")
    else:
        st.info("Provide your location to begin searching.")
# hospital_page()





