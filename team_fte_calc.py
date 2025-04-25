import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

# --- Setup ---
st.set_page_config(page_title="Team FTE Calculator", layout="wide")
st.title("📊 Team FTE Calculator")

st.sidebar.header("📥 Input Variables")

# --- Inputs from Sidebar ---
internal_chargeability = st.sidebar.number_input("Internal Engineer Team Estimated Chargeability (decimal)", 0.0, 1.0, 0.88)
external_chargeability = st.sidebar.number_input("External Engineer Team Estimated Chargeability (decimal)", 0.0, 1.0, 0.95)

internal_team_count = st.sidebar.number_input("Internal Engineer Team Headcount", 0, 1000, 36)
external_team_count = st.sidebar.number_input("External Engineer Team Headcount", 0, 1000, 23)

client_engineer_demand = st.sidebar.number_input("Client Engineer Demand (FTEs)", 0, 1000, 47)

internal_nonengineer_count = st.sidebar.number_input("Internal PM Team Headcount", 0, 1000, 26)
external_nonengineer_count = st.sidebar.number_input("External PM Team Headcount", 0, 1000, 10)

total_team_demand = st.sidebar.number_input("Total Team Demand (Optional)", 0, 1000, 0)

# --- Calculations ---
engineer_fte_availability = (internal_chargeability * internal_team_count) + (external_chargeability * external_team_count)
engineer_fte_delta = engineer_fte_availability - client_engineer_demand
nonengineer_ftes = (internal_chargeability * internal_nonengineer_count) + (external_chargeability * external_nonengineer_count)
total_team_ftes = engineer_fte_availability + nonengineer_ftes

# Additional calcs
internal_engineer_availability = internal_chargeability * internal_team_count
internal_fte_delta = internal_engineer_availability - client_engineer_demand

total_engineer_headcount = internal_team_count + external_team_count
total_nonengineer_headcount = internal_nonengineer_count + external_nonengineer_count
internal_engineer_headcount_delta = internal_team_count - client_engineer_demand
total_engineer_headcount_delta = total_engineer_headcount - client_engineer_demand

# Helper for delta formatting
def format_delta(val):
    return f"+{val:.2f}" if val > 0 else f"{val:.2f}"

# --- Dashboard Summary ---
st.subheader("📋 Dashboard Summary")

with st.container():
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Engineer FTE Availability", f"{engineer_fte_availability:.2f}")
    col2.metric("Total Engineer Availability vs Demand FTE Delta", None, format_delta(engineer_fte_delta), delta_color="normal")
    col3.metric("Total PM FTE Availability", f"{nonengineer_ftes:.2f}")

with st.container():
    col4, col5, col6 = st.columns(3)
    col4.metric("Total Team FTE Availability", f"{total_team_ftes:.2f}")
    col5.metric("Client Engineer Demand (FTEs)", f"{client_engineer_demand:.2f}")
    col6.metric("Internal Engineer Availability vs Demand FTE Delta", None, format_delta(internal_fte_delta), delta_color="normal")

with st.container():
    col7, col8, col9 = st.columns(3)
    col7.metric("Total Engineer Headcount", total_engineer_headcount)
    col8.metric("Total PM Headcount", total_nonengineer_headcount)
    col9.metric("Internal Engineer Headcount vs Demand", None, format_delta(internal_engineer_headcount_delta), delta_color="normal")

with st.container():
    col10, _, _ = st.columns(3)
    col10.metric("Total Engineer Headcount vs Demand", None, format_delta(total_engineer_headcount_delta), delta_color="normal")

# Adding Internal Engineer Headcount Total Metric
with st.container():
    col11, _, _ = st.columns(3)
    col11.metric("Total Internal Engineer Headcount", internal_team_count)
# --- Program Headcount Chart ---
st.subheader("📊 Program Headcount Breakdown")

headcount_data = pd.DataFrame({
    "Category": ["Internal Engineer", "External Engineer", "Internal PM", "External PM"],
    "Headcount": [internal_team_count, external_team_count, internal_nonengineer_count, external_nonengineer_count]
})

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(headcount_data["Category"], headcount_data["Headcount"], color=['#6A1B9A', '#8E24AA', '#9C4D97', '#AB47BC'])

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, f'{yval:.0f}', ha='center', va='bottom', fontsize=12)

ax.set_ylabel("Headcount")
ax.set_title("Program Headcount")
plt.xticks(rotation=20, ha='right')
st.pyplot(fig)

# --- Engineer Availability Delta Chart ---
st.subheader("📊 Engineer Capacity Delta")

fte_deltas = pd.DataFrame({
    "Category": ["Internal Engineer Headcount vs Demand", "Total Engineer Headcount vs Demand"],
    "FTE Delta": [internal_engineer_headcount_delta, total_engineer_headcount_delta]
})

fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.bar(fte_deltas["Category"], fte_deltas["FTE Delta"], color=['#BDBDBD', '#757575'])

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.2 if yval >= 0 else yval - 0.4, f'{yval:.2f}', ha='center', va='bottom', fontsize=12)

ax.set_ylabel("FTE Delta")
ax.set_title("Engineer Capacity Delta")
plt.xticks(rotation=15, ha='right')
st.pyplot(fig)

# --- Engineer Availability vs Demand Delta Chart ---
st.subheader("📊 Engineer Availability vs Demand Delta")

availability_deltas = pd.DataFrame({
    "Category": [
        "Internal Engineer Availability vs Demand",
        "Total Engineer Availability vs Demand"
    ],
    "Availability Delta": [internal_fte_delta, engineer_fte_delta]
})

fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.bar(availability_deltas["Category"], availability_deltas["Availability Delta"], color=['#90CAF9', '#42A5F5'])

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2,
            yval + 0.2 if yval >= 0 else yval - 0.4,
            f'{yval:.2f}', ha='center', va='bottom', fontsize=12)

ax.set_ylabel("FTE Delta")
ax.set_title("Engineer Availability vs Demand Delta")
plt.xticks(rotation=15, ha='right')
st.pyplot(fig)

# --- Export Section ---
st.subheader("⬇️ Export Data")

export_data = {
    "Metric": [
        "Internal Chargeability", "External Chargeability",
        "Internal Engineer Headcount", "External Engineer Headcount",
        "Client Engineer Demand", "Internal PM", "External PM",
        "Total Engineer FTE Availability", "Engineer FTE Delta",
        "PM FTEs", "Total Team FTEs",
        "Internal Engineer FTE Delta (vs Client Demand)",
        "Total Engineer Headcount Delta", "Internal Engineer Headcount Delta"
    ],
    "Value": [
        internal_chargeability, external_chargeability,
        internal_team_count, external_team_count,
        client_engineer_demand, internal_nonengineer_count, external_nonengineer_count,
        engineer_fte_availability, engineer_fte_delta,
        nonengineer_ftes, total_team_ftes,
        internal_fte_delta, total_engineer_headcount_delta, internal_engineer_headcount_delta
    ]
}

df_export = pd.DataFrame(export_data)

file_format = st.radio("Choose file format:", ("CSV", "Excel"))

if file_format == "CSV":
    csv = df_export.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", data=csv, file_name="fte_summary.csv", mime="text/csv")
else:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_export.to_excel(writer, index=False, sheet_name="FTE Summary")
        writer.save()
    st.download_button("Download Excel", data=output.getvalue(), file_name="fte_summary.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
