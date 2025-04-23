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
internal_chargeability = st.sidebar.number_input("Internal Team Chargeability (decimal)", 0.0, 1.0, 0.88)
external_chargeability = st.sidebar.number_input("External Team Chargeability (decimal)", 0.0, 1.0, 0.95)

internal_team_count = st.sidebar.number_input("Internal Tech Team Headcount", 0, 1000, 36)
external_team_count = st.sidebar.number_input("External Tech Team Headcount", 0, 1000, 23)

client_tech_demand = st.sidebar.number_input("Client Tech Demand (FTEs)", 0, 1000, 47)

internal_mgmt_count = st.sidebar.number_input("Internal Mgmt Team Headcount", 0, 1000, 26)
external_mgmt_count = st.sidebar.number_input("External Mgmt Headcount", 0, 1000, 10)

total_team_demand = st.sidebar.number_input("Total Team Demand (Optional)", 0, 1000, 0)

# --- Calculations ---
tech_fte_supply = (internal_chargeability * internal_team_count) + (external_chargeability * external_team_count)
tech_fte_delta = tech_fte_supply - client_tech_demand
mgmt_ftes = (internal_chargeability * internal_mgmt_count) + (external_chargeability * external_mgmt_count)
total_team_ftes = tech_fte_supply + mgmt_ftes

# Calculate deltas for internal tech team vs client tech demand and total tech team capacity vs client tech demand
internal_tech_capacity = internal_chargeability * internal_team_count  # Internal Tech Capacity (Headcount * Chargeability)
internal_fte_delta = internal_tech_capacity - client_tech_demand  # Capacity minus client tech demand

# Total Tech Team FTEs minus client tech demand
total_fte_delta = tech_fte_supply - client_tech_demand

# --- Dashboard Summary ---
st.subheader("📋 Dashboard Summary")

col1, col2, col3 = st.columns(3)
col1.metric("Tech FTE Capacity", f"{tech_fte_supply:.2f}")
col2.metric("Tech Capacity vs Demand FTE Delta", f"{tech_fte_delta:.2f}")
col3.metric("Mgmt FTE Capacity", f"{mgmt_ftes:.2f}")

# Added Client Tech Demand Metric
col4, col5 = st.columns(2)
col4.metric("Total Team FTE Capacity (Tech + Mgmt)", f"{total_team_ftes:.2f}")

# Aligning Client Tech Demand with other metrics in the columns
col6, _ = st.columns([3, 1])
col6.metric("Client Tech Demand (FTEs)", f"{client_tech_demand:.2f}")

# Added the new deltas for the dashboard
col7, col8 = st.columns(2)
col7.metric("Internal Tech vs Client Tech Demand FTE Delta", f"{internal_fte_delta:.2f}")

# --- Program Headcount Chart ---
st.subheader("📊 Program Headcount Breakdown")

headcount_data = pd.DataFrame({
    "Category": ["Internal Team", "External Team", "Internal Mgmt", "External Mgmt"],
    "Headcount": [internal_team_count, external_team_count, internal_mgmt_count, external_mgmt_count]
})

# Generate gradient colors for each category (purple shades)
purple_colors = ['#6A1B9A', '#8E24AA', '#9C4D97', '#AB47BC']

fig, ax = plt.subplots()
bars = ax.bar(headcount_data["Category"], headcount_data["Headcount"], color=purple_colors)

# Add data labels above each bar
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, f'{yval:.0f}', ha='center', va='bottom', fontsize=12)

ax.set_ylabel("Headcount")
ax.set_title("Program Headcount")
st.pyplot(fig)

# --- Program Delivery FTE Delta Chart ---
st.subheader("📊 Program Delivery FTE Delta")

# Generate data for the deltas
fte_deltas = pd.DataFrame({
    "Category": ["Internal Tech FTE Delta", "Total Tech FTE Delta"],
    "FTE Delta": [internal_fte_delta, total_fte_delta]
})

fig, ax = plt.subplots()

# Bar plot for FTE Deltas
bars = ax.bar(fte_deltas["Category"], fte_deltas["FTE Delta"], color=['#BDBDBD', '#757575'])

# Add data labels above each bar
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, f'{yval:.2f}', ha='center', va='bottom', fontsize=12)

ax.set_ylabel("FTE Delta")
ax.set_title("Program Delivery FTE Delta")
st.pyplot(fig)

# --- Export Section ---
st.subheader("⬇️ Export Data")

export_data = {
    "Metric": [
        "Internal Chargeability", "External Chargeability",
        "Internal Team Headcount", "External Team Headcount",
        "Client Tech Demand", "Internal Mgmt", "External Mgmt",
        "Tech FTE Supply", "Tech FTE Delta",
        "Mgmt FTEs", "Total Team FTEs", "Total FTE Delta",
        "Internal Tech FTE Delta (vs Client Tech Demand)",
        "Total Tech FTE Delta (vs Client Tech Demand)"
    ],
    "Value": [
        internal_chargeability, external_chargeability,
        internal_team_count, external_team_count,
        client_tech_demand, internal_mgmt_count, external_mgmt_count,
        tech_fte_supply, tech_fte_delta,
        mgmt_ftes, total_team_ftes, total_fte_delta if total_fte_delta else "N/A",
        internal_fte_delta, total_fte_delta
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
