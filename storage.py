import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# Load data
df = pd.read_csv("Data/RpoPlan.csv")

# Convert secondsSinceStart to hour groups
df["hour"] = df["secondsSinceStart"] // 3600  # Grouping by hour

# Calculate data collected per hour
hourly_data = df.groupby("hour")["storedData"].agg(lambda x: x.iloc[-1] - x.iloc[0]).reset_index()
hourly_data.rename(columns={"storedData": "dataCollected"}, inplace=True)

# Get storedData at the end of every hour
hourly_storage = df.groupby("hour")["storedData"].last().reset_index()
hourly_storage.rename(columns={"storedData": "storageAtEndOfHour"}, inplace=True)

# Add storageAtEndOfHour as a new column in hourly_data
hourly_data["storageAtEndOfHour"] = hourly_storage["storageAtEndOfHour"]

# Streamlit app setup
st.set_page_config(layout="wide", page_title="Hackathon USU 2025")

# Title
st.markdown("<h1 style='text-align: center; color: #1985a1;'>Hackathon USU 2025</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #1985a1;'>Hourly Storage and Data Summary</h3>", unsafe_allow_html=True)

# Create Plotly figure
fig = go.Figure()

# Line for Data Collected
fig.add_trace(go.Scatter(
    x=hourly_data["hour"],
    y=hourly_data["dataCollected"],
    mode='lines+markers',
    name="Data Collected",
    line=dict(color='white')
))

# Line for Storage at End of Hour
fig.add_trace(go.Scatter(
    x=hourly_data["hour"],
    y=hourly_data["storageAtEndOfHour"],
    mode='lines+markers',
    name="Storage at End of Hour",
    line=dict(color='#1985a1')
))

# Add threshold line at y=1150
fig.add_shape(
    go.layout.Shape(
        type="line",
        x0=min(hourly_data["hour"]),
        y0=1150,
        x1=max(hourly_data["hour"]),
        y1=1150,
        line=dict(color="orange", width=2, dash="dash")
    )
)

# Customize layout
fig.update_layout(
    title="Data Collected and Storage at End of Hour",
    xaxis_title="Hour",
    yaxis_title="Value",
    legend_title="Legend",
    font=dict(color="white"),
    plot_bgcolor="#212529",
    paper_bgcolor="#212529"
)

# Display graph
col1, col2 = st.columns([3, 2])  # Adjust column width ratios
with col1:
    st.plotly_chart(fig, use_container_width=True)

# Display data table
with col2:
    st.markdown("<h4 style='text-align: center; color: #1985a1;'>Hourly Data</h4>", unsafe_allow_html=True)
    st.dataframe(
        hourly_data.style.applymap(
            lambda x: "background-color: orange;" if x > 1000 else "", subset=["storageAtEndOfHour"]
        )
    )
