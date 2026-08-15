"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

Analytics Module — Plotly Safety Data Visualizations.

Page: 4_📈_Analytics.py
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
from pipeline.loader import load_icsr_dataset
from analysis.safety_analyzer import DeterministicSafetyAnalyzer

st.title("📈 Advanced Safety Analytics & Visualizations")

data_path = st.session_state.get("data_path", os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "Bisoprolol_icsr_sample_1068rows.csv"))

try:
    df = load_icsr_dataset(data_path)
    analyzer = DeterministicSafetyAnalyzer(df)
    seriousness = analyzer.reactions_engine.analyze_seriousness()
    demographics = analyzer.demographics_engine.analyze()
    reactions = analyzer.reactions_engine.analyze_reactions(top_n=15)
    monthly = analyzer.monthly_trends()
except Exception as e:
    st.error(f"Error loading analytics: {e}")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    st.write("### 1. Top 10 Adverse Reactions (MedDRA PT)")
    df_pts = pd.DataFrame(list(reactions["top_reactions"].items())[:10], columns=["Adverse Event (PT)", "Cases"])
    fig1 = px.bar(df_pts, x="Cases", y="Adverse Event (PT)", orientation="h", color="Cases", color_continuous_scale="Viridis")
    fig1.update_layout(yaxis=dict(autorange="reversed"), height=380)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.write("### 2. Seriousness Criteria (Donut Chart)")
    df_ser = pd.DataFrame(list(seriousness.items()), columns=["Criteria", "Count"])
    fig2 = px.pie(df_ser, names="Criteria", values="Count", hole=0.4, color_discrete_sequence=px.colors.sequential.Plotly3)
    fig2.update_layout(height=380)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.write("### 3. Patient Sex Distribution (Pie Chart)")
    sex_data = demographics["sex"]
    df_sex = pd.DataFrame(list(sex_data.items()), columns=["Sex", "Cases"])
    fig3 = px.pie(df_sex, names="Sex", values="Cases", color_discrete_sequence=px.colors.qualitative.Set2)
    fig3.update_layout(height=350)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.write("### 4. Geographic Origin Distribution")
    countries = demographics["countries"]
    df_c = pd.DataFrame(list(countries.items())[:8], columns=["Country", "Cases"])
    fig4 = px.bar(df_c, x="Country", y="Cases", color="Cases", color_continuous_scale="Magma")
    fig4.update_layout(height=350)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

st.write("### 5. Time-Series Monthly Case Receipts")
if monthly:
    df_t = pd.DataFrame(list(monthly.items()), columns=["Month", "Cases"])
    fig5 = px.line(df_t, x="Month", y="Cases", markers=True, title="Monthly Submissions Trend")
    fig5.update_layout(height=350)
    st.plotly_chart(fig5, use_container_width=True)
