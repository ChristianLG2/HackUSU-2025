import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import pyspark.sql.functions as sf
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('space-data').getOrCreate()

maneuver_plan = spark.read.csv("Data/ManeuverPlan.csv")

header_row = maneuver_plan.limit(1).collect()[0]
new_column_names = [str(val) for val in header_row]
old_column_names = maneuver_plan.columns
df_without_header = maneuver_plan.filter(maneuver_plan[old_column_names[0]] != header_row[0])
for old_col, new_col in zip(old_column_names, new_column_names):
    df_without_header = df_without_header.withColumnRenamed(old_col, new_col)
maneuver_plan = df_without_header

maneuver_plan.createOrReplaceTempView('maneuver_plans')

st.set_page_config(page_title="Celestial Choreography", layout="wide")
st.title("Maneuver Plan")

fuel_usage = spark.sql("SELECT maneuverId, timeUtcDay, SUM(dvMagnitude) OVER(ORDER BY timeUtcDay) AS fuel_consumed_total FROM maneuver_plans")
fig = px.line(fuel_usage.toPandas(),x='maneuverId',y='fuel_consumed_total', labels= {'formatted_date': 'Date','fuel_consumed_total':'Fuel Consumed Over time'})

st.text("**Fuel Consumed over Each Manuever**")
st.dataframe(fuel_usage.toPandas().head(10))

for point in fuel_usage.toPandas()['maneuverId']:
    point_y = fuel_usage.toPandas().loc[fuel_usage.toPandas()['maneuverId'] == point, 'fuel_consumed_total'].values[0]  # Get corresponding y-value
    fig.add_trace(go.Scatter(
        x=[point],
        y=[point_y],
        mode='markers',
        marker=dict(size=7, color='black'),
        showlegend = False
    ))

fig.add_annotation(
    x=4,  # X-coordinate to point to
    y=1.4,  # Y-coordinate to point to
    text="Most fuel-expensive Manuever",  # Annotation text
    showarrow=True,  # Show arrow
    arrowhead=2,  # Arrow style (1-8 available)
    ax=0,  # X-offset for text (relative to arrow's head)
    ay=-40,  # Y-offset for text (negative moves text up)
    arrowcolor="red",  # Arrow color
    font=dict(color="red", size=12)  # Text font and size
)

st.plotly_chart(fig, use_container_width=True)