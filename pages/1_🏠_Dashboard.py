"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

Executive Dashboard Module.

Page: 1_🏠_Dashboard.py
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
from analysis.safety_analyzer import DeterministicSafetyAnalyzer
from pipeline.loader import load_icsr_dataset

st.title("🏠 Executive Safety Dashboard")

data_path = st.session_state.get("data_path", os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "Bisoprolol_icsr_sample_1068rows.csv"))

try:
    raw_df = load_icsr_dataset(data_path)
    analyzer = DeterministicSafetyAnalyzer(raw_df)
    stats = analyzer.summary_metrics()
    seriousness = analyzer.reactions_engine.analyze_seriousness()
    demographics = analyzer.demographics_engine.analyze()
    reactions = analyzer.reactions_engine.analyze_reactions()
except Exception as e:
    st.error(f"Error loading safety analytics: {e}")
    st.stop()

# Key Performance Indicators
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Dataset Status", "Loaded ✅", f"{os.path.basename(data_path)}")
with col2:
    st.metric("Reporting Interval", f"{stats['reporting_period_start']}", f"to {stats['reporting_period_end']}")
with col3:
    st.metric("Unique ICSR Cases", f"{stats['total_cases']:,}", f"{stats['total_rows']:,} raw records")
with col4:
    st.metric("Serious Cases", f"{stats['serious_cases']:,}", f"{stats['serious_percentage']}% of total")

st.markdown("---")

c1, c2 = st.columns(2)
with c1:
    st.write("### 📌 Active Pipeline Overview")
    st.write(f"- **Product**: {stats.get('product_name')}")
    st.write(f"- **Application**: {stats.get('application_number')}")
    st.write(f"- **MAH Holder**: {stats.get('mah_holder')}")
    st.write(f"- **Active Provider Engine**: `{st.session_state.get('provider_type', 'groq').upper()}`")
    st.write(f"- **15-Day Expedited Alert Cases**: `{stats.get('expedited_15day_alert_cases'):,}`")

with c2:
    st.write("### 🌍 Top Reporter Countries")
    countries = demographics.get("countries", {})
    df_c = pd.DataFrame(list(countries.items())[:6], columns=["Country", "Case Count"])
    st.dataframe(df_c, use_container_width=True)

st.markdown("---")

st.write("### ⚡ Top 5 Reported Adverse Reactions (Preferred Terms)")
top_pts = list(reactions.get("top_reactions", {}).items())[:5]
df_top = pd.DataFrame(top_pts, columns=["MedDRA Preferred Term (PT)", "Total Reports"])
fig = px.bar(df_top, x="Total Reports", y="MedDRA Preferred Term (PT)", orientation="h", color="Total Reports", color_continuous_scale="Blues")
fig.update_layout(yaxis=dict(autorange="reversed"), height=300)
st.plotly_chart(fig, use_container_width=True)
