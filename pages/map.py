import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static

# 🔹 Function to Load CSV with Error Handling
def load_csv(file_path):
    try:
        # Auto-detect delimiter and encoding
        df = pd.read_csv(file_path, sep=None, engine="python", encoding="utf-8")

        # Strip column names (removes leading/trailing spaces)
        df.columns = df.columns.str.strip()


        return df
    except Exception as e:
        st.error(f"⚠️ Error loading CSV: {e}")
        return None

# Load RPO Plan CSV
csv_path = "RpoPlan.csv"  # Update if needed
df = load_csv(csv_path)

# 🔹 Step 1: Check if Latitude & Longitude Exist
if df is not None and all(col in df.columns for col in ["latitude", "longitude", "secondsSinceStart"]):

    # Display first few rows for debugging
    st.subheader("📊 First 5 Rows of RpoPlan.csv")
    st.dataframe(df.head())

    # 🔹 Step 2: Plot Deputy Trajectory on a Global Map (Plotly)
    st.subheader("🛰️ Deputy Satellite Trajectory Over Earth")

    fig_map = px.scatter_geo(
        df,
        lat="latitude",
        lon="longitude",
        color="secondsSinceStart",
        title="Deputy Satellite Trajectory",
        projection="orthographic",  # Try "equirectangular" for a flat map
        labels={"secondsSinceStart": "Time Progression"},
        hover_data={"latitude": True, "longitude": True, "secondsSinceStart": True}
    )

    fig_map.update_layout(geo=dict(showland=True, showocean=True, showcountries=True))
    st.plotly_chart(fig_map, use_container_width=True)

    # 🔹 Step 3: Interactive Map (Folium)
    st.subheader("🌍 Interactive Map of Deputy Trajectory")

    # Initialize Folium map at the first position
    start_location = [df["latitude"].iloc[0], df["longitude"].iloc[0]]
    satellite_map = folium.Map(location=start_location, zoom_start=3)

    # Add trajectory points
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=2,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.6,
            popup=f"Time: {row['secondsSinceStart']}s",
        ).add_to(satellite_map)

    # Display the Folium map
    folium_static(satellite_map)

else:
    st.warning("⚠️ Latitude and Longitude columns are still missing. Please check your dataset.")


