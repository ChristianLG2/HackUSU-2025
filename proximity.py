import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Celestial Choreography", layout="wide")

# File paths (Update with correct paths if needed)
csv_files = {
    "rpo_plan": "RpoPlan.csv",
    "maneuver_plan": "ManeuverPlan.csv",
    "ground_contacts": "GroundContacts.csv",
    "payload_events": "PayloadEvents.csv",
    "maneuver_branches": "maneuver_branches.csv"
}

# Load all CSVs into Pandas DataFrames
dfs = {name: pd.read_csv(path) for name, path in csv_files.items()}

# Sidebar for dataset selection
st.sidebar.header("Select Dataset")
selected_dataset = st.sidebar.selectbox("Choose a dataset to preview:", list(dfs.keys()))

# Display selected dataset
st.subheader(f"{selected_dataset.upper()} Dataset (First 5 Rows)")
st.dataframe(dfs[selected_dataset].head())

# Plot 1: Relative Range Over Time (Segmented by Attitude Mode)
st.subheader("📈 Relative Range Over Time (Segmented by Attitude Mode)")
fig1 = px.line(
    dfs["rpo_plan"], 
    x="secondsSinceStart", 
    y="relativeRange", 
    color="attitudeMode",
    title="Relative Range Over Time (Segmented by Attitude Mode)"
)
st.plotly_chart(fig1, use_container_width=True)

# Plot 2: Relative Range with Maneuver Events
st.subheader("📊 Relative Range Over Time with Maneuver Events")
fig2 = px.line(
    dfs["rpo_plan"], 
    x="secondsSinceStart", 
    y="relativeRange", 
    title="Relative Range Over Time"
)

# Add vertical lines for maneuver events
for t in dfs["maneuver_plan"]["secondsSinceStart"]:
    fig2.add_shape(
        go.layout.Shape(
            type="line", 
            x0=t, x1=t, y0=dfs["rpo_plan"]["relativeRange"].min(), 
            y1=dfs["rpo_plan"]["relativeRange"].max(),
            line=dict(color="red", width=1, dash="dash")
        )
    )

st.plotly_chart(fig2, use_container_width=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("📌 *Celestial Choreography Dashboard*")
st.sidebar.markdown("👨‍💻 Developed by Chris")