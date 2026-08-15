"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

AI Report Generation & Evidence Scoper Module.

Page: 5_🧠_Generator.py
"""

import os
import streamlit as st
from pipeline.generator import ReportPipeline
from config.settings import CONFIG_DIR

st.title("🧠 AI Report Generation & Evidence Scoper")
st.write("Generate individual PADER report sections independently or run full automated report generation.")

data_path = st.session_state.get("data_path", os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "Bisoprolol_icsr_sample_1068rows.csv"))
provider_type = st.session_state.get("provider_type", "groq")
api_key = st.session_state.get("api_key", os.environ.get("GROQ_API_KEY", ""))

if "pipeline_gen" not in st.session_state:
    st.session_state["pipeline_gen"] = ReportPipeline(data_path, provider_type=provider_type, api_key=api_key)

gen = st.session_state["pipeline_gen"]
sections = gen.config.get("sections", [])

st.info(f"Active Engine: `{provider_type.upper()}` | Dataset: `{os.path.basename(data_path)}`")

selected_sec_id = st.selectbox(
    "Select Section to Inspect Evidence Packet",
    options=[s["id"] for s in sections],
    format_func=lambda x: next(s["title"] for s in sections if s["id"] == x)
)

sec_info = next(s for s in sections if s["id"] == selected_sec_id)

col1, col2 = st.columns([1, 1])
with col1:
    st.write("#### Regulatory System Instruction")
    st.info(sec_info.get("description", ""))
    st.write("#### Required Evidence Inputs")
    st.write(sec_info.get("requires_analysis", []))
    custom_inst = st.text_area("Optional Custom Prompt Suffix", help="e.g. Emphasize serious acute kidney injury cases")

with col2:
    st.write("#### Assembled Section Evidence Packet (JSON)")
    scoped = {k: gen.evidence_packet[k] for k in sec_info.get("requires_analysis", []) if k in gen.evidence_packet}
    st.json(scoped)

st.markdown("---")

c_b1, c_b2 = st.columns([1, 2])
with c_b1:
    if st.button("🚀 Generate Selected Section", type="secondary"):
        with st.spinner(f"Generating {sec_info['title']}..."):
            txt = gen.generate_section(selected_sec_id, custom_instruction=custom_inst)
            st.success(f"Generated {sec_info['title']}!")
            st.markdown(txt)

with c_b2:
    if st.button("⚡ Generate Complete PADER Report (All 8 Sections)", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, sec in enumerate(sections):
            status_text.text(f"Generating: {sec['title']} ({idx+1}/{len(sections)})")
            gen.generate_section(sec["id"])
            progress_bar.progress((idx + 1) / len(sections))
        
        status_text.text("✅ Full PADER Report Generation Complete!")
        st.success("All 8 sections generated and audited for numerical grounding.")
