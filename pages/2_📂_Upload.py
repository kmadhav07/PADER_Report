"""
Dataset Selection & Uploader Module.

Page: 2_📂_Upload.py
"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd
from pipeline.loader import load_icsr_dataset
from pipeline.validator import validate_icsr_dataset

st.title("📂 Dataset Selection & Uploader")
st.write("Select a pre-loaded clinical safety dataset or upload your custom ICSR CSV file to run the reporting pipeline.")

data_dir = os.path.join(project_root, "data")
preloaded_files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]

col_left, col_right = st.columns([1, 1])

with col_left:
    st.write("### 💊 Option A: Select Pre-Loaded Safety Dataset")
    selected_file = st.selectbox(
        "Choose Pharmacovigilance Dataset",
        options=preloaded_files,
        index=0 if "Bisoprolol_icsr_sample_1068rows.csv" in preloaded_files else 0
    )
    if st.button("Use Selected Pre-Loaded Dataset", type="primary"):
        chosen_path = os.path.join(data_dir, selected_file)
        st.session_state["data_path"] = chosen_path
        if "pipeline_gen" in st.session_state:
            del st.session_state["pipeline_gen"]
        st.success(f"Active dataset switched to: **{selected_file}**")

with col_right:
    st.write("### 📤 Option B: Upload Custom ICSR CSV File")
    uploaded_file = st.file_uploader("Upload CSV ICSR File", type=["csv"])
    if uploaded_file is not None:
        custom_save_path = os.path.join(data_dir, f"uploaded_{uploaded_file.name}")
        with open(custom_save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state["data_path"] = custom_save_path
        if "pipeline_gen" in st.session_state:
            del st.session_state["pipeline_gen"]
        st.success(f"Uploaded and set active dataset: **{uploaded_file.name}**")

st.markdown("---")

current_path = st.session_state.get("data_path", os.path.join(data_dir, "Bisoprolol_icsr_sample_1068rows.csv"))
st.write(f"### 🔍 Current Active Dataset Audit: `{os.path.basename(current_path)}`")

try:
    df = load_icsr_dataset(current_path)
    val_info = validate_icsr_dataset(df)
    
    st.write(f"- **Total Rows**: {len(df):,}")
    st.write(f"- **Unique Safety Cases**: {val_info['unique_cases']:,}")
    st.write(f"- **Columns Detected**: {len(df.columns)}")
    st.write(f"- **Schema Validation Status**: `{val_info['status']}`")
    
    st.write("#### Data Sample Preview")
    st.dataframe(df.head(10), use_container_width=True)

except Exception as e:
    st.error(f"Error reading dataset: {e}")
