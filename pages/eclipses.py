import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load dataset
csv_path = "RpoPlan.csv"
df = pd.read_csv(csv_path)

# Strip column names to avoid errors
df.columns = df.columns.str.strip()

# Ensure the required columns exist
if all(col in df.columns for col in ["secondsSinceStart", "eclipseTypeChief", "eclipseTypeDeputy", "relativeRange"]):

    st.subheader("🌑 Eclipse Events vs. Mission Plan")

    # Define eclipse labels and colors
    eclipse_labels = {0: "No Eclipse", 1: "Partial Eclipse", 2: "Full Eclipse"}
    color_map = {0: "green", 1: "orange", 2: "red"}

    # Create base line chart for mission relative range
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["secondsSinceStart"],
        y=df["relativeRange"],
        mode="lines",
        name="Relative Range",
        line=dict(color="blue")
    ))

    # Add shaded areas for eclipse events
    for _, row in df.iterrows():
        if row["eclipseTypeChief"] > 0:  # Eclipse happening
            fig.add_vrect(
                x0=row["secondsSinceStart"],
                x1=row["secondsSinceStart"] + 10,  # Adjust duration if needed
                fillcolor=color_map[row["eclipseTypeChief"]],
                opacity=0.3,
                layer="below",
                line_width=0,
                annotation_text=eclipse_labels[row["eclipseTypeChief"]],
                annotation_position="top left"
            )

    # Update layout
    fig.update_layout(
        title="Eclipse Events vs. Mission Timeline",
        xaxis_title="Mission Time (s)",
        yaxis_title="Relative Range",
        legend_title="Legend"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("⚠️ Required columns are missing from the dataset.")

