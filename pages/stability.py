import streamlit as st
import pandas as pd
import plotly.express as px

# Load datasets
csv_files = {
    "maneuver_plan": "ManeuverPlan.csv",
    "ground_contacts": "GroundContacts.csv",
}

dfs = {}
for name, path in csv_files.items():
    try:
        dfs[name] = pd.read_csv(path)
        dfs[name].columns = dfs[name].columns.str.strip()  # Clean column names
    except Exception as e:
        st.warning(f"⚠️ {name} missing or failed to load: {e}")

st.title("🚀 Mission Efficiency Analysis")

# 📌 **Fuel Usage & Maneuver Efficiency**
maneuver_plan = dfs.get("maneuver_plan")

if maneuver_plan is not None:
    if "dVMagnitude" in maneuver_plan.columns:
        st.subheader("⛽ Fuel Usage Over Time (ΔV)")
        fig1 = px.line(
            maneuver_plan,
            x="secondsSinceStart",
            y="dVMagnitude",
            title="Total ΔV Usage Over Time",
            labels={"secondsSinceStart": "Mission Time (s)", "dVMagnitude": "ΔV Magnitude (m/s)"},
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning("⚠️ `ManeuverPlan.csv` loaded but `dVMagnitude` column not found.")

# 📡 **Communication Windows & Ground Contacts**
ground_contacts = dfs.get("ground_contacts")

if ground_contacts is not None:
    if "groundSite" in ground_contacts.columns:
        st.subheader("📡 Ground Contact Windows")
        fig2 = px.scatter(
            ground_contacts,
            x="startSeconds",
            y="groundSite",
            title="Ground Station Contacts Over Time",
            labels={"startSeconds": "Mission Time (s)", "groundSite": "Ground Station"},
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("⚠️ `GroundContacts.csv` loaded but `groundSite` column not found.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("📌 *Mission Efficiency Dashboard*")


