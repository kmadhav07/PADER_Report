"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

Human Review & Sign-Off Hub.

Page: 6_📝_Review.py
"""

import os
import streamlit as st
from pipeline.generator import ReportPipeline

st.title("📝 Human-in-the-Loop Review Workspace")
st.write("Review AI narratives side-by-side with ground-truth evidence, edit prose inline, verify audit checks, and approve sections.")

data_path = st.session_state.get("data_path", os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "Bisoprolol_icsr_sample_1068rows.csv"))
provider_type = st.session_state.get("provider_type", "groq")
api_key = st.session_state.get("api_key", os.environ.get("GROQ_API_KEY", ""))

if "pipeline_gen" not in st.session_state:
    st.session_state["pipeline_gen"] = ReportPipeline(data_path, provider_type=provider_type, api_key=api_key)

gen = st.session_state["pipeline_gen"]
sections = gen.config.get("sections", [])

if not gen.sections_content:
    st.info("💡 Report sections have not been generated yet.")
    if st.button("⚡ Generate PADER Report Sections Now", type="primary"):
        with st.spinner("Generating sections via Groq API..."):
            gen.generate_full_report()
            st.success("Report sections generated!")
            st.rerun()
    st.stop()

active_sec_id = st.selectbox(
    "Select Section to Audit & Sign-Off",
    options=list(gen.sections_content.keys()),
    format_func=lambda x: next((s["title"] for s in sections if s["id"] == x), x)
)

curr_text = gen.sections_content[active_sec_id]
audit_res = gen.section_audits.get(active_sec_id, {})
is_approved = gen.section_approvals.get(active_sec_id, False)

# Audit Summary Bar
c_a1, c_a2, c_a3 = st.columns(3)
with c_a1:
    st.metric("Grounding Score", f"{audit_res.get('grounding_score', 100.0)}%")
with c_a2:
    st.metric("Grounding Status", "PASSED ✅" if audit_res.get("passed", True) else "FLAGGED ⚠️")
with c_a3:
    status_html = '<span class="badge-approved">Approved ✅</span>' if is_approved else '<span class="badge-pending">Pending Sign-off ⏳</span>'
    st.markdown(f"**Sign-off Status**: {status_html}", unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.write("#### 📝 Editable Section Narrative")
    edited_text = st.text_area("Narrative Text", value=curr_text, height=360, key=f"edit_narrative_{active_sec_id}")
    if edited_text != curr_text:
        gen.update_section_text(active_sec_id, edited_text)
        st.success("Updated narrative saved & re-audited!")

with col2:
    st.write("#### 🛡️ Grounding & Evidence Audit")
    st.write("**Verified Grounded Claims:**")
    if audit_res.get("matches"):
        for m in audit_res["matches"]:
            st.success(f"• {m}")
    else:
        st.info("No numerical statements in this section.")

    if audit_res.get("discrepancies"):
        st.write("**Discrepancies / Unverified Claims:**")
        for d in audit_res["discrepancies"]:
            st.error(f"• {d}")

    st.write("**Extracted Numbers in Text:**")
    st.write(audit_res.get("audited_numbers", []))

st.markdown("---")

c_btn1, c_btn2, c_btn3 = st.columns(3)
with c_btn1:
    if st.button("✅ Approve Section", type="primary"):
        gen.set_section_approval(active_sec_id, True)
        st.success(f"Section '{active_sec_id}' approved!")
        st.rerun()

with c_btn2:
    if st.button("⚠️ Reject / Flag Section", type="secondary"):
        gen.set_section_approval(active_sec_id, False)
        st.warning(f"Section '{active_sec_id}' flagged.")
        st.rerun()

with c_btn3:
    if st.button("🔄 Regenerate Section", type="secondary"):
        with st.spinner("Regenerating section..."):
            gen.generate_section(active_sec_id)
            st.success("Section regenerated!")
            st.rerun()
