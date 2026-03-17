
def crime():
    import streamlit as st
    import pandas as pd
    import numpy as np
    import base64
    import os


    from sklearn.preprocessing import LabelEncoder
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import r2_score

    # ------------------------------------
    # PAGE CONFIG
    # ------------------------------------
    st.set_page_config(
        page_title="SurakshaSetu | Crime Prediction",
        layout="wide"
    )

    def img_to_base64(path):
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()



    BASE_DIR = os.path.dirname(__file__)
    IMAGE_PATH = os.path.join(BASE_DIR, "crime.png")

    girl_b64 = img_to_base64(IMAGE_PATH)


    st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    .block-container {padding-top: 0rem;}

    .top-crime-banner {
        width: 100%;
        height: 200px;
        background: #F41C78;
        padding-left: 40px;
        padding-top: 30px;
        position: relative;
    }

    .banner-title {
        font-size: 46px;
        font-weight: 800;
        color: white;
    }

    .banner-subtitle {
        font-size: 22px;
        font-weight: 600;
        color: #ffe4ef;
    }

    .guardian-img {
        position: absolute;
        right: 40px;
        top: -60px;
        width: 300px;
    }

    @media (max-width: 900px) {
        .guardian-img { display: none; }
    }

    </style>
    """, unsafe_allow_html=True)
    # ------------------------------------
    # SURAKSHASETU THEME + FONT SIZE (CSS)
    # ------------------------------------
    st.markdown(
        """
        <style>
        /* -------- BACKGROUND -------- */
        .stApp {
            background-color: #FF77B1;
        }

        /* -------- GLOBAL TEXT -------- */
        html, body, [class*="css"] {
            font-size: 20px;
            font-weight: 700;
        }

        
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="top-crime-banner">
        <div class="banner-title">ML Women Crime Prediction – सुरक्षाSetu</div>
        <div class="banner-subtitle">
            Predict • Prevent • Protect
        </div>
        <img class="guardian-img" src="data:image/png;base64,{girl_b64}">
    </div>
    """, unsafe_allow_html=True)
    

    # ------------------------------------
    # LOAD DATA
    # ------------------------------------
    @st.cache_data
    def load_data():
        return pd.read_csv("women_crime_state_completed.csv")

    df = load_data()

    # ------------------------------------
    # USER SELECTION
    # ------------------------------------
    level = st.selectbox("Select Level", ["State", "City"])

    if level == "State":
        states = sorted(df[df["Level"] == "State"]["State"].unique())
        selected_state = st.selectbox("Select State", states)
        filtered_df = df[(df["Level"] == "State") & (df["State"] == selected_state)]
        city_name = "None"

    else:
        cities = sorted(df[df["Level"] == "City"]["City"].unique())
        selected_city = st.selectbox("Select City", cities)
        filtered_df = df[(df["Level"] == "City") & (df["City"] == selected_city)]
        selected_state = filtered_df.iloc[0]["State"]
        city_name = selected_city

    # ------------------------------------
    # YEAR SELECTION
    # ------------------------------------
    future_year = st.slider("Select Year", 2021, 2030, 2025)

    # ------------------------------------
    # DATA PREPARATION
    # ------------------------------------
    model_df = df.copy()
    model_df["City"] = model_df["City"].fillna("None")

    le_state = LabelEncoder()
    le_city = LabelEncoder()
    le_level = LabelEncoder()

    model_df["State_enc"] = le_state.fit_transform(model_df["State"])
    model_df["City_enc"] = le_city.fit_transform(model_df["City"])
    model_df["Level_enc"] = le_level.fit_transform(model_df["Level"])

    X = model_df[["Year", "State_enc", "City_enc", "Level_enc"]]
    y = model_df["Total_Crimes"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ------------------------------------
    # RANDOM FOREST MODEL
    # ------------------------------------
    rf_model = RandomForestRegressor(
        n_estimators=300,
        random_state=42
    )

    rf_model.fit(X_train, y_train)

    # ------------------------------------
    # ENCODING SELECTED LOCATION
    # ------------------------------------
    state_enc = le_state.transform([selected_state])[0]
    city_enc = le_city.transform([city_name])[0]
    level_enc = le_level.transform([level])[0]

    # ------------------------------------
    # TREND DATA
    # ------------------------------------
    years_range = list(range(2021, future_year + 1))
    trend_data = []

    for yr in years_range:
        if yr in filtered_df["Year"].values:
            crime_val = filtered_df[filtered_df["Year"] == yr]["Total_Crimes"].values[0]
        else:
            future_input = np.array([[yr, state_enc, city_enc, level_enc]])
            crime_val = int(rf_model.predict(future_input)[0])

        trend_data.append({"Year": yr, "Total_Crimes": crime_val})

    trend_df = pd.DataFrame(trend_data).set_index("Year")

    # ------------------------------------
    # OUTPUT
    # ------------------------------------
    st.subheader("Crime Trend (2021 → Selected Year)")
    st.line_chart(trend_df)

    # ------------------------------------
    # FINAL RESULT
    # ------------------------------------
    final_value = trend_df.iloc[-1]["Total_Crimes"]
    location = selected_state if level == "State" else f"{selected_city}, {selected_state}"

    st.metric(
        label=f"{location} – {future_year}",
        value=f"{int(final_value):,} cases"
    )

    # ------------------------------------
    # RISK LEVEL
    # ------------------------------------
    st.subheader("🚨Risk Level")

    if final_value < 5000:
        st.success("LOW RISK")
    elif final_value < 20000:
        st.warning("MEDIUM RISK")
    else:
        st.error("HIGH RISK")

    # ------------------------------------
    # DISCLAIMER
    # ------------------------------------
    st.info(
        "⚠️ Predictions are based on NCRB historical data (2021–2023).\n"
        "Future values are ML estimates for awareness & safety planning."
    )


## main above

