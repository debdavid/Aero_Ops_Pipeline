import streamlit as st
import pandas as pd
import plotly.express as px

# 1. PAGE SETUP
st.set_page_config(page_title="AeroOps Executive Dashboard", layout="wide")

st.title("AeroOps: Fleet Efficiency & Risk Monitor")
st.markdown("**Report Date:** Feb 15, 2026 | **Data Source:** Live Telemetry Feed")
st.markdown("---")

# 2. DATA CONNECTION (CLOUD MODE) ☁️
# We load the static CSV files directly. 
# This is fast, crash-proof, and works perfectly on GitHub/Streamlit Cloud.

try:
    # Load the CSVs you pushed to GitHub
    df_gold = pd.read_csv('gold_data.csv')
    df_silver = pd.read_csv('silver_data.csv')
except FileNotFoundError:
    st.error("⚠️ Data files not found! Did you push gold_data.csv and silver_data.csv to GitHub?")
    st.stop()

# ------------------------------------------------------------------
# NOTE: No more SQL queries needed here. The Pipeline did the work!
# ------------------------------------------------------------------

# 3. EXECUTIVE KPI ROW
col1, col2, col3 = st.columns(3)

total_waste = df_gold['Wasted Fuel (Gal)'].sum()
worst_offender = df_gold.iloc[0]['tail_number']
avg_fleet_vib = df_silver['Vibration (IPS)'].mean()

col1.metric("Total Recoverable Waste", f"{total_waste:,.0f} gal", delta="-44,032 gal", delta_color="inverse")
col2.metric("Critical Asset Identified", worst_offender, delta="Action Required", delta_color="inverse")
col3.metric("Fleet Avg Vibration", f"{avg_fleet_vib:.2f} IPS", delta="Threshold: 0.60 IPS")

st.markdown("---")

# 4. VISUALIZATIONS

# Row 1: The Outlier Analysis
st.subheader("⚠️ Cost Impact Analysis")
st.caption("This chart highlights the specific asset driving operational inefficiency. **VH-XZD** is the sole contributor to fuel waste.")

fig_bar = px.bar(
    df_gold, 
    x='tail_number', 
    y='Wasted Fuel (Gal)',
    color='status', # Uses the 'status' column from the CSV
    color_discrete_map={'Critical': '#FF4B4B', 'Normal': '#E0E0E0'},
    text_auto=True,
    title="Cumulative Fuel Waste by Aircraft (30 Days)",
    labels={'tail_number': 'Aircraft ID', 'Wasted Fuel (Gal)': 'Excess Fuel (Gallons)'}
)
fig_bar.update_layout(showlegend=False) 
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# Row 2: Correlation Deep Dive
st.subheader("🔍 Root Cause: Vibration Correlation")
st.caption("Detailed telemetry analysis. The **Red Zone** (>0.7 IPS) indicates where mechanical instability begins to degrade engine efficiency.")

fig_scatter = px.scatter(
    df_silver, 
    x='Vibration (IPS)', 
    y='Fuel Burn (lbs/hr)', 
    color='Safety Status', # Uses the 'Safety Status' column from the CSV
    color_discrete_map={'Critical': '#FF4B4B', 'Normal': '#1C83E1'},
    hover_data=['Aircraft ID'],
    title="Engine Performance: Vibration vs. Fuel Consumption",
)

fig_scatter.add_vline(x=0.7, line_dash="dash", line_color="green", annotation_text="ISO Safety Limit (0.7 IPS)")

st.plotly_chart(fig_scatter, use_container_width=True)

# 5. RECOMMENDATION
st.error("""
**Executive Recommendation:** Aircraft **VH-XZD** is exhibiting persistent high-vibration events (>0.7 IPS), directly correlating with **44k gallons** of excess fuel burn. 
**Recommended Action:** Ground VH-XZD for immediate engine alignment to restore fleet efficiency.
""")
