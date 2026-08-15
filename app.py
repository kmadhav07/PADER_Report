"""
RegIntel AI — Safety Reporting Platform

Main entry point for Streamlit application shell.
"""

import sys
import os

# Ensure project root is on sys.path for robust module imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="RegIntel AI — Safety Reporting Platform",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Application Global Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #1e3a8a 100%);
        padding: 20px 28px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .badge-approved { background-color: #dcfce7; color: #15803d; padding: 4px 10px; border-radius: 12px; font-size: 0.85em; font-weight: 600; }
    .badge-pending { background-color: #fef3c7; color: #b45309; padding: 4px 10px; border-radius: 12px; font-size: 0.85em; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

DEFAULT_DATA_PATH = os.path.join(project_root, "data", "Bisoprolol_icsr_sample_1068rows.csv")

if "data_path" not in st.session_state:
    st.session_state["data_path"] = DEFAULT_DATA_PATH

if "provider_type" not in st.session_state:
    st.session_state["provider_type"] = "groq"

if "api_key" not in st.session_state:
    st.session_state["api_key"] = os.environ.get("GROQ_API_KEY", "")

# Header Banner
st.markdown("""
<div class="main-header">
    <h2 style='margin:0; font-size:1.8rem;'>⚕️ RegIntel AI — Pharmacovigilance Platform</h2>
    <p style='margin-top:4px; font-size:0.95rem; opacity:0.85;'>
        Automated Regulatory Safety Reporting System (FDA 21 CFR 314.80)
    </p>
</div>
""", unsafe_allow_html=True)

st.info("👈 Select a module from the **sidebar navigation** (Dashboard, Upload, Explorer, Analytics, Generator, Review Hub, Evidence Viewer, Exporter, Settings).")
