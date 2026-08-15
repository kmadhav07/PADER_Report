"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

Dataset Explorer Module.

Page: 3_📊_Explorer.py
"""

import os
import streamlit as st
import pandas as pd
from pipeline.loader import load_icsr_dataset
from analysis.safety_analyzer import DeterministicSafetyAnalyzer

st.title("📊 Dataset Explorer")
st.write("Examine raw data columns, missing values, duplicates, and attribute distributions.")

data_path = st.session_state.get("data_path", os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "Bisoprolol_icsr_sample_1068rows.csv"))

try:
    df = load_icsr_dataset(data_path)
    analyzer = DeterministicSafetyAnalyzer(df)
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

sub1, sub2, sub3, sub4 = st.tabs(["📋 Data Schema & Nulls", "🔁 Duplicates & Cases", "💊 Reactions & Outcomes", "📄 Raw Data Table"])

with sub1:
    st.write("### Dataset Columns & Data Types")
    col_info = pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": [str(df[c].dtype) for c in df.columns],
        "Non-Null Count": [int(df[c].notnull().sum()) for c in df.columns],
        "Missing Count": [int(df[c].isnull().sum()) for c in df.columns]
    })
    st.dataframe(col_info, use_container_width=True)

with sub2:
    st.write("### Case Deduplication Overview")
    total_rows = len(df)
    unique_cases = df['safetyreportid'].nunique() if 'safetyreportid' in df.columns else total_rows
    st.write(f"- **Total Record Rows**: {total_rows:,}")
    st.write(f"- **Unique Safety Report IDs**: {unique_cases:,}")
    st.write(f"- **Multi-Row Records (Multiple Reactions)**: {total_rows - unique_cases:,}")

with sub3:
    st.write("### Reactions & Outcomes Distribution")
    reactions = analyzer.reactions_engine.analyze_reactions(top_n=20)
    outcomes = analyzer.analyze_all()["reaction_analysis"].get("outcomes", {})
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("#### Preferred Terms Frequency")
        df_rx = pd.DataFrame(list(reactions["top_reactions"].items()), columns=["Preferred Term (PT)", "Occurrences"])
        st.dataframe(df_rx, use_container_width=True)

    with col_b:
        st.write("#### Clinical Outcomes Frequency")
        df_out = pd.DataFrame(list(outcomes.items()), columns=["Outcome", "Count"])
        st.dataframe(df_out, use_container_width=True)

with sub4:
    st.write("### Raw ICSR Dataset View")
    st.dataframe(df.head(100), use_container_width=True)
