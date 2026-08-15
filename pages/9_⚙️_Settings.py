"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

Settings & Configuration Module.

Page: 9_⚙️_Settings.py
"""

import os
import yaml
import streamlit as st
from config.settings import DEFAULT_MODEL, CONFIG_DIR

st.title("⚙️ System & Model Settings")
st.write("Configure active engine parameters, API keys, and regulatory report schemas.")

st.write("### 🔑 API Key & Engine Setup")
provider_type = st.selectbox(
    "Primary Engine Provider",
    options=["groq", "offline"],
    format_func=lambda x: "Groq LPU API (Primary)" if x == "groq" else "Offline Rule Engine (No API Key Required)"
)

groq_key = st.text_input(
    "Groq API Key",
    value=st.session_state.get("api_key", os.environ.get("GROQ_API_KEY", "")),
    type="password",
    help="Enter key from console.groq.com"
)

if st.button("Save API Configuration", type="primary"):
    st.session_state["provider_type"] = provider_type
    st.session_state["api_key"] = groq_key
    os.environ["GROQ_API_KEY"] = groq_key
    st.success("Configuration updated successfully!")

st.markdown("---")

st.write("### 🎛️ Model Hyperparameters")
col1, col2 = st.columns(2)
with col1:
    model_sel = st.selectbox("Groq Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"])
with col2:
    temp_sel = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.15, step=0.05)

st.markdown("---")

st.write("### 📜 Registered Regulatory Report Schemas")
pader_yaml_path = os.path.join(CONFIG_DIR, "pader_config.yaml")
if os.path.exists(pader_yaml_path):
    with open(pader_yaml_path, "r", encoding="utf-8") as f:
        pader_schema_data = yaml.safe_load(f)
    st.json(pader_schema_data)
