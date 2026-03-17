def ngos_page():

    import streamlit as st
    import requests
    import pandas as pd
    from geopy.distance import geodesic
    from geopy.geocoders import Nominatim
    from streamlit_geolocation import streamlit_geolocation
    import os


    # ---------------- UI / THEME ----------------
    st.markdown("""
    <style>
        .stApp { background-color: #FF77B1; color: white; font-size: 18px; }
        h1 { font-size: 38px !important; font-weight: 800; font-color : #000; }
        h2 { font-size: 30px !important; font-weight: 700; font-color : #000; }
        h3 { font-size: 26px !important; font-color : #000;}
        h4,h5,h6 { font-size: 22px !important; }
        label,p,span,div { font-size: 18px !important; font-weight: 500; color: white !important; }
        .stRadio label, .stSlider label { font-size: 18px !important; }
        .stTextInput input {
            background-color: white !important;
            color: #C2185B !important;
            font-size: 18px !important;
            padding: 10px;
            border-radius: 10px;
            border: 2px solid #C2185B;
        }
        .stButton button {
            background-color: #FF5FA2;
            color: white;
            border-radius: 14px;
            font-size: 18px;
            font-weight: 600;
            padding: 0.7em 1.4em;
        }
        .stDataFrame, .stDataFrame div {
            font-size: 17px !important;
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- TOP BANNER IMAGE (optional) ----------------
    banner_path = "assets/ngo_banner.png"  # Optional banner
    if os.path.exists(banner_path):
        st.image(banner_path, use_container_width=True)

    # ---------------- CONSTANTS ----------------
    OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"
    DEFAULT_RADIUS_KM = 5

    # ---------------- FETCH NGOs ----------------
    def get_nearby_ngos(lat, lon, radius_m):
        query = f"""
        [out:json][timeout:25];
        (
        node["office"="ngo"](around:{radius_m},{lat},{lon});
        node["amenity"="social_facility"](around:{radius_m},{lat},{lon});
        node["amenity"="community_centre"](around:{radius_m},{lat},{lon});
        way["office"="ngo"](around:{radius_m},{lat},{lon});
        );
        out center;
        """
        try:
            response = requests.post(
                OVERPASS_API_URL,
                data=query,
                headers={"User-Agent": "ngo-locator-app"}
            )
            if response.status_code != 200 or not response.text.strip().startswith("{"):
                return []
            data = response.json()
            ngos = []
            for e in data.get("elements", []):
                lat_e = e.get("lat") or e.get("center", {}).get("lat")
                lon_e = e.get("lon") or e.get("center", {}).get("lon")
                if lat_e and lon_e:
                    ngos.append({
                        "name": e.get("tags", {}).get("name", "Unnamed NGO"),
                        "lat": lat_e,
                        "lon": lon_e,
                        "address": e.get("tags", {}).get("addr:street", "Not available")
                    })
            return ngos
        except Exception as e:
            st.error(f"Error fetching NGOs: {e}")
            return []

    # ---------------- UI ----------------
    st.title("🤝 Nearby NGOs (All India)")
    st.subheader("📍 Choose location method")

    method = st.radio(
        "How would you like to provide your location?",
        ["Use Live GPS Location", "Enter City Manually"]
    )

    user_lat = user_lon = None

    # ---------------- LIVE GPS ----------------
    if method == "Use Live GPS Location":
        location = streamlit_geolocation()
        if location and location.get("latitude"):
            user_lat = location["latitude"]
            user_lon = location["longitude"]
            st.success("📌 Live location detected")

    # ---------------- MANUAL CITY ----------------
    else:
        city = st.text_input("Enter city name (anywhere in India)")
        if city:
            geolocator = Nominatim(user_agent="ngo_locator_app")
            loc = geolocator.geocode(city, country_codes="in")
            if loc:
                user_lat, user_lon = loc.latitude, loc.longitude
                st.success(f"📍 {city} located")
            else:
                st.error("City not found")

    # ---------------- RADIUS ----------------
    radius_km = st.slider("Search radius (km)", 1, 20, DEFAULT_RADIUS_KM)

    # ---------------- RESULTS ----------------
    if user_lat and user_lon:
        ngos = get_nearby_ngos(user_lat, user_lon, radius_km * 1000)
        if ngos:
            for n in ngos:
                n["distance_km"] = geodesic((user_lat, user_lon), (n["lat"], n["lon"])).km
            ngos = sorted(ngos, key=lambda x: x["distance_km"])
            df = pd.DataFrame([{
                "NGO Name": n["name"],
                "Address": n["address"],
                "Distance (km)": f"{n['distance_km']:.2f}"
            } for n in ngos])
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No NGOs found nearby. Try increasing radius.")
    else:
        st.info("Provide location to search NGOs.")
# ngos_page()