

def travel():
    import streamlit as st
    import folium
    import requests
    import pandas as pd

    from folium.plugins import MarkerCluster
    from streamlit_folium import folium_static
    from openrouteservice import convert

    # -----------------------------------
    # PAGE CONFIG
    # -----------------------------------
    st.set_page_config(
        page_title="सुरक्षाSetu - Smart Route Planner",
        layout="wide"
    )

    # -----------------------------------
    # 🌸 SURAKSHASETU THEME (UI ONLY)
    # -----------------------------------
    st.markdown("""
    <style>
    .stApp {
        background-color: #FF77B1;
    }

    .header-box {
        background:  #F41C78;
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
    }

    .header-box h1 {
        margin: 0;
        font-size: 45px;
    }

    .header-box p {
        margin: 0;
        font-size: 16px;
        opacity: 0.95;
    }

    div.stButton > button {
        background-color: #F41C78;
        color: white;
        border-radius: 8px;
        font-size: 16px;
        padding: 8px 20px;
    }

    div.stButton > button:hover {
        background-color: #d91665;
        color: white;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    /* Target checkbox text */
    div[data-testid="stCheckbox"] span {
        font-size: 40px !important;
        font-weight: 600;
    }

    /* Increase checkbox size itself */
    div[data-testid="stCheckbox"] input {
        transform: scale(1.4);
    }
    </style>
    """, unsafe_allow_html=True)

    # -----------------------------------
    # HEADER
    # -----------------------------------
    st.markdown("""
    <div class="header-box">
        <h1>सुरक्षाSetu Live Travel</h1>
        <p>Smart Route Planner • Women Safety Focused</p>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------
    # WOMEN SAFETY DATA (LAT / LNG)
    # -----------------------------------
    crime_df = pd.DataFrame({
        "City": [
            "Mumbai","Delhi","Bengaluru","Chennai","Kolkata",
            "Hyderabad","Pune","Ahmedabad","Jaipur","Lucknow",
            "Indore","Bhopal","Patna","Ranchi","Bhubaneswar",
            "Guwahati","Imphal","Shillong","Agartala","Aizawl"
        ],
        "Area": [
            "Andheri East","Dwarka","Whitefield","T Nagar","Salt Lake",
            "Gachibowli","Shivajinagar","Maninagar","Malviya Nagar","Alambagh",
            "Vijay Nagar","MP Nagar","Kankarbagh","Harmu","Saheed Nagar",
            "Dispur","Lamphel","Police Bazaar","Usha Bazar","Chanmari"
        ],
        "Women Related Crime": [
            "Eve Teasing","Sexual Harassment","Stalking","Public Harassment",
            "Domestic Violence","Workplace Harassment","Followed by Stranger",
            "Molestation","Attempted Kidnapping","Threatening Calls",
            "Night Harassment","Cyber Harassment","Domestic Abuse",
            "Street Harassment","Voyeurism","Stalking","Assault",
            "Public Intimidation","Cyber Stalking","Harassment"
        ],
        "Severity": [
            "Medium","High","High","Medium","High",
            "High","Medium","High","Very High","High",
            "Medium","High","High","Medium","High",
            "Medium","High","Medium","High","Medium"
        ],
        "Time Reported": [
            "21:45","22:30","20:15","18:40","23:10",
            "19:50","21:05","22:20","20:30","23:40",
            "21:15","19:25","22:55","20:10","21:35",
            "22:05","19:45","20:20","23:15","21:50"
        ],
        "Latitude": [
            19.12,28.61,12.97,13.08,22.57,
            17.45,18.52,23.02,26.91,26.85,
            22.72,23.26,25.60,23.35,20.30,
            26.15,24.82,25.58,23.83,23.73
        ],
        "Longitude": [
            72.88,77.21,77.59,80.27,88.36,
            78.39,73.86,72.57,75.79,80.95,
            75.86,77.41,85.14,85.32,85.82,
            91.73,93.95,91.88,91.28,92.72
        ]
    })

    # -----------------------------------
    # GENERAL CRIME
    # -----------------------------------
    general_crime_df = pd.DataFrame({
        "City": crime_df["City"],
        "Crime Type": [
            "Eve Teasing","Chain Snatching","Sexual Harassment","Stalking","Domestic Violence",
            "Robbery","Mobile Theft","Public Harassment","Kidnapping Attempt","Molestation",
            "Night Harassment","Workplace Harassment","Street Crime","Theft","Cyber Crime",
            "Harassment","Stalking","Assault","Threatening Calls","Public Intimidation"
        ],
        "Severity": [
            "Medium","High","High","High","High",
            "High","Medium","Medium","Very High","High",
            "Medium","High","Medium","Low","Medium",
            "Medium","High","High","Medium","Medium"
        ],
        "Latitude": crime_df["Latitude"],
        "Longitude": crime_df["Longitude"]
    })

    # -----------------------------------
    # DISASTER DATA
    # -----------------------------------
    disaster_df = pd.DataFrame({
        "City": [
            "Mumbai","Chennai","Kolkata","Pune","Nagpur",
            "Patna","Guwahati","Kochi","Dehradun","Shimla",
            "Srinagar","Leh","Ranchi","Bhubaneswar","Visakhapatnam"
        ],
        "Disaster Type": [
            "Urban Flooding","Cyclone","Heatwave","Heavy Rainfall","Heatwave",
            "River Flood","Flood","Coastal Flood","Landslide","Snowfall",
            "Avalanche","Cold Wave","Thunderstorm","Cyclone Alert","Cyclone Alert"
        ],
        "Severity": [
            "High","Very High","High","Medium","High",
            "Very High","High","Medium","Medium","Low",
            "High","High","Medium","Very High","Very High"
        ],
        "Alert Authority": [
            "IMD","IMD","IMD","IMD","IMD",
            "NDMA","NDMA","IMD","NDMA","State Govt",
            "NDMA","IMD","IMD","IMD","IMD"
        ],
        "Latitude": [
            19.07,13.08,22.57,18.52,21.15,
            25.59,26.14,9.93,30.32,31.10,
            34.08,34.15,23.35,20.30,17.69
        ],
        "Longitude": [
            72.88,80.27,88.36,73.86,79.09,
            85.14,91.73,76.27,78.03,77.17,
            74.79,77.57,85.32,85.82,83.22
        ]
    })

    # -----------------------------------
    # TRAFFIC DATA
    # -----------------------------------
    traffic_df = pd.DataFrame({
        "City": [
            "Delhi","Mumbai","Bengaluru","Chennai","Hyderabad",
            "Pune","Ahmedabad","Jaipur","Chandigarh","Noida",
            "Gurugram","Faridabad","Ghaziabad","Indore","Bhopal"
        ],
        "Violation Type": [
            "Signal Jumping","Over Speeding","Wrong Side Driving","No Helmet","Drunk Driving",
            "Illegal Parking","Over Speeding","Signal Jumping","No Seat Belt","Lane Violation",
            "Drunk Driving","Wrong Parking","No Helmet","Over Speeding","Signal Jumping"
        ],
        "Risk Level": [
            "High","High","Very High","Medium","High",
            "Medium","High","Medium","Low","Medium",
            "High","Medium","Medium","High","Medium"
        ],
        "Latitude": [
            28.61,19.07,12.97,13.08,17.38,
            18.52,23.02,26.91,30.73,28.53,
            28.45,28.40,28.67,22.72,23.26
        ],
        "Longitude": [
            77.21,72.88,77.59,80.27,78.48,
            73.86,72.57,75.79,76.78,77.39,
            77.02,77.31,77.45,75.86,77.41
        ]
    })

    # -----------------------------------
    # HELPERS (LOGIC UNCHANGED)
    # -----------------------------------
    def get_coordinates(place):
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": place, "format": "json"}
        r = requests.get(url, params=params, headers={"User-Agent": "SurakshaSetu"})
        data = r.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
        return None


    def get_route(start_coords, end_coords):
        ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImE3NmIzNGUyZWE1ZDQ4ZWM4N2IxZGQ3N2FhNWI1NTUyIiwiaCI6Im11cm11cjY0In0="
        url = "https://api.openrouteservice.org/v2/directions/driving-car"
        headers = {"Authorization": ORS_API_KEY}
        payload = {
            "coordinates": [
                [start_coords[1], start_coords[0]],
                [end_coords[1], end_coords[0]]
            ]
        }
        r = requests.post(url, json=payload, headers=headers)
        return r.json()

    # -----------------------------------
    # MAIN UI
    # -----------------------------------
    col1, col2 = st.columns(2)
    start_address = col1.text_input("Start Location", "Pune")
    destination_address = col2.text_input("Destination", "Mumbai")

    show_women_alerts = st.checkbox("Women Safety Alerts", True)
    show_crime = st.checkbox("General Crime Alerts", True)
    show_disaster = st.checkbox("Disaster Alerts", True)
    show_traffic = st.checkbox("Traffic Alerts", True)

    if st.button("Plan Route"):

        start_coords = get_coordinates(start_address)
        end_coords = get_coordinates(destination_address)

        if start_coords and end_coords:

            route_data = get_route(start_coords, end_coords)

            if route_data and "routes" in route_data:

                route = route_data["routes"][0]
                geometry = convert.decode_polyline(route["geometry"])
                route_line = [[c[1], c[0]] for c in geometry["coordinates"]]

                m = folium.Map(location=start_coords, zoom_start=6, tiles="CartoDB positron")
                folium.Marker(start_coords, icon=folium.Icon(color="green")).add_to(m)
                folium.Marker(end_coords, icon=folium.Icon(color="blue")).add_to(m)
                folium.PolyLine(route_line, color="#F41C78", weight=5).add_to(m)

                cluster = MarkerCluster().add_to(m)

                if show_women_alerts:
                    for _, r in crime_df.iterrows():
                        color = "darkred" if r["Severity"] in ["High","Very High"] else "pink"
                        folium.Marker(
                            [r["Latitude"], r["Longitude"]],
                            icon=folium.Icon(color=color),
                            tooltip=f"{r['Women Related Crime']} | {r['Severity']} | {r['Time Reported']}"
                        ).add_to(cluster)

                if show_crime:
                    for _, r in general_crime_df.iterrows():
                        folium.Marker(
                            [r["Latitude"], r["Longitude"]],
                            icon=folium.Icon(color="red"),
                            tooltip=f"{r['Crime Type']} | {r['Severity']}"
                        ).add_to(cluster)

                if show_disaster:
                    for _, r in disaster_df.iterrows():
                        folium.Marker(
                            [r["Latitude"], r["Longitude"]],
                            icon=folium.Icon(color="orange"),
                            tooltip=f"{r['Disaster Type']} | {r['Severity']} | {r['Alert Authority']}"
                        ).add_to(cluster)

                if show_traffic:
                    for _, r in traffic_df.iterrows():
                        folium.Marker(
                            [r["Latitude"], r["Longitude"]],
                            icon=folium.Icon(color="purple"),
                            tooltip=f"{r['Violation Type']} | {r['Risk Level']}"
                        ).add_to(cluster)

                folium_static(m, width=1200, height=600)
                st.success("Map loaded successfully ⚡")
