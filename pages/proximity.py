import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Celestial Choreography", layout="wide")

# File paths (update with correct paths if needed)
csv_files = {
    "rpo_plan": "RpoPlan.csv",
    "maneuver_plan": "ManeuverPlan.csv",
    "ground_contacts": "GroundContacts.csv",
    "payload_events": "PayloadEvents.csv",
    "maneuver_branches": "maneuver_branches.csv"
}

# Load all CSVs into Pandas DataFrames with error handling
dfs = {}
for name, path in csv_files.items():
    try:
        dfs[name] = pd.read_csv(path)
    except Exception as e:
        st.error(f"Error loading {name} from {path}: {e}")

# Strip whitespace from all column names
for df in dfs.values():
    df.columns = df.columns.str.strip()

# Sidebar for dataset selection
st.sidebar.header("Select Dataset")
selected_dataset = st.sidebar.selectbox("Choose a dataset to preview:", list(dfs.keys()))

# Display selected dataset preview
st.subheader(f"{selected_dataset.upper()} Dataset (First 5 Rows)")
st.dataframe(dfs[selected_dataset].head())

# Get the rpo_plan DataFrame
rpo_plan = dfs.get("rpo_plan")
if rpo_plan is None:
    st.error("rpo_plan dataset not found. Please check your CSV files.")
    st.stop()

# Determine which y-axis column to use:
# Prefer 'relativeRange' if it exists; if not, fall back to 'storedData'
if 'relativeRange' in rpo_plan.columns:
    y_col = 'relativeRange'
    y_label = "Relative Range (m)"
elif 'storedData' in rpo_plan.columns:
    y_col = 'storedData'
    y_label = "Stored Data (MB)"
else:
    st.error("Neither 'relativeRange' nor 'storedData' columns found in the rpo_plan dataset.")
    st.stop()

# Plot 1: Relative Range Over Time (Segmented by Attitude Mode)
st.subheader("📈 Relative Range Over Time (Segmented by Attitude Mode)")
# Check if the column 'attitudeMode' exists for segmentation; if not, no color grouping
color_arg = "attitudeMode" if "attitudeMode" in rpo_plan.columns else None
fig1 = px.line(
    rpo_plan,
    x="secondsSinceStart",
    y=y_col,
    color=color_arg,
    title="Relative Range Over Time (Segmented by Attitude Mode)",
    labels={"secondsSinceStart": "Time Since Start (s)", y_col: y_label}
)
st.plotly_chart(fig1, use_container_width=True)

# Plot 2: Relative Range with Maneuver Events
st.subheader("📊 Relative Range Over Time with Maneuver Events")
fig2 = px.line(
    rpo_plan,
    x="secondsSinceStart",
    y=y_col,
    title="Relative Range Over Time with Maneuver Events",
    labels={"secondsSinceStart": "Time Since Start (s)", y_col: y_label}
)

# Add vertical dashed lines for each maneuver event time
maneuver_plan = dfs.get("maneuver_plan")
if maneuver_plan is not None and "secondsSinceStart" in maneuver_plan.columns:
    for t in maneuver_plan["secondsSinceStart"]:
        fig2.add_shape(
            type="line",
            x0=t, x1=t,
            y0=rpo_plan[y_col].min(),
            y1=rpo_plan[y_col].max(),
            line=dict(color="red", width=1, dash="dash")
        )
else:
    st.warning("Maneuver plan data not found or missing 'secondsSinceStart' column. Skipping maneuver events overlay.")

st.plotly_chart(fig2, use_container_width=True)

# 🚨 Add Table for Proximity Violations (when below 100m)
st.subheader("🚨 Proximity Violations (Below 100m Limit)")
proximity_limit = 100  # Define safety threshold

if "relativeRange" in rpo_plan.columns:
    proximity_violations = rpo_plan[rpo_plan["relativeRange"] < proximity_limit][["secondsSinceStart", "relativeRange"]]
    st.dataframe(proximity_violations)
else:
    st.warning("⚠️ 'relativeRange' column not found. Cannot display proximity violations.")

# Footer in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("📌 *Celestial Choreography Dashboard*")