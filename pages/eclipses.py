import streamlit as st
import pandas as pd

# Load dataset
csv_path = "Data/RpoPlan.csv"
df = pd.read_csv(csv_path)

# Strip column names to remove unwanted spaces
df.columns = df.columns.str.strip()

# Required columns
required_columns = [
    "secondsSinceStart", "eclipseTypeChief", "eclipseTypeDeputy", 
    "sensorAngleToSun", "sensorAngleToMoon", "sensorAngleToEarth",
    "earthHalfAngle"
]

# Check if all required columns exist
if all(col in df.columns for col in required_columns):

    # Define visibility thresholds
    sun_visibility_limit = 40  # Degrees - Sensors don't perform well if below this
    moon_visibility_limit = 12  # Degrees
    earth_visibility_limit = 10  # Degrees off Earth's limb

    # Identify times when visibility is blocked due to Sun, Moon, or Earth
    blocked_times = df[
        (df["sensorAngleToSun"] < sun_visibility_limit) |
        (df["sensorAngleToMoon"] < moon_visibility_limit) |
        (df["sensorAngleToEarth"] < df["earthHalfAngle"] + earth_visibility_limit)
    ][["secondsSinceStart", "sensorAngleToSun", "sensorAngleToMoon", "sensorAngleToEarth", "earthHalfAngle"]]

    # Identify eclipse periods
    eclipse_events = df[
        (df["eclipseTypeChief"] > 0) | (df["eclipseTypeDeputy"] > 0)
    ][["secondsSinceStart", "eclipseTypeChief", "eclipseTypeDeputy"]]

    # Display results in Streamlit
    st.subheader("🌑 Eclipse Events Over Time")
    st.dataframe(eclipse_events)

    st.subheader("🔴 Visibility Blocked Periods (Sun/Moon/Earth)")
    st.dataframe(blocked_times)

else:
    missing_cols = [col for col in required_columns if col not in df.columns]
    st.warning(f"⚠️ Missing columns: {missing_cols}. Please check your dataset.")


