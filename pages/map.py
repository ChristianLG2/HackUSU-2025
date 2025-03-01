import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
csv_path = "RpoPlan.csv"
df = pd.read_csv(csv_path)

# DEBUG: Show available columns
st.write("🔍 Available Columns:", df.columns.tolist())

# Fix potential issues with spaces or incorrect capitalization
df.columns = df.columns.str.strip()
df.rename(columns={"Latitude": "latitude", "Longitude": "longitude"}, inplace=True)

# Verify if lat/lon exist
if all(col in df.columns for col in ["latitude", "longitude", "secondsSinceStart"]):

    # Scatter plot on a world map
    st.subheader("🛰️ Deputy Satellite Trajectory Over Earth")

    fig_map = px.scatter_geo(
        df,
        lat="latitude",
        lon="longitude",
        color="secondsSinceStart",
        title="Deputy Satellite Trajectory",
        projection="orthographic",
        labels={"secondsSinceStart": "Time Progression"},
        hover_data={"latitude": True, "longitude": True, "secondsSinceStart": True}
    )

    fig_map.update_layout(geo=dict(showland=True, showocean=True, showcountries=True))
    st.plotly_chart(fig_map, use_container_width=True)

else:
    st.warning("⚠️ Latitude and Longitude columns are still missing.")

