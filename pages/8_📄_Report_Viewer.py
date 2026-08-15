"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

Report Viewer & Exporter Module.

Page: 8_📄_Report_Viewer.py
"""

import os
import streamlit as st
from pipeline.generator import ReportPipeline
from exporters.markdown_exporter import export_to_markdown
from exporters.html_exporter import export_to_html
from exporters.docx_exporter import export_to_docx
from exporters.pdf_exporter import export_to_pdf

st.title("📄 Report Preview & Multi-Format Exporter")
st.write("Preview the rendered PADER regulatory document and download in your choice of standard formats.")

data_path = st.session_state.get("data_path", os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "Bisoprolol_icsr_sample_1068rows.csv"))
provider_type = st.session_state.get("provider_type", "groq")
api_key = st.session_state.get("api_key", os.environ.get("GROQ_API_KEY", ""))

if "pipeline_gen" not in st.session_state:
    st.session_state["pipeline_gen"] = ReportPipeline(data_path, provider_type=provider_type, api_key=api_key)

gen = st.session_state["pipeline_gen"]

if not gen.sections_content:
    st.info("💡 Report sections have not been generated yet.")
    if st.button("⚡ Generate PADER Report Sections Now", type="primary"):
        with st.spinner("Generating sections via Groq API..."):
            gen.generate_full_report()
            st.success("Report sections generated!")
            st.rerun()
    st.stop()

full_md = gen.assemble_final_markdown()

out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
os.makedirs(out_dir, exist_ok=True)

md_file = os.path.join(out_dir, "PADER_Bisoprolol_Report.md")
html_file = os.path.join(out_dir, "PADER_Bisoprolol_Report.html")
docx_file = os.path.join(out_dir, "PADER_Bisoprolol_Report.docx")
pdf_file = os.path.join(out_dir, "PADER_Bisoprolol_Report.pdf")

export_to_markdown(full_md, md_file)
export_to_html(full_md, html_file)
export_to_docx(full_md, docx_file)
export_to_pdf(full_md, pdf_file)

# Export Action Grid
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.download_button(
        "📥 Markdown (.md)",
        data=full_md,
        file_name="PADER_Bisoprolol_Report.md",
        mime="text/markdown"
    )

with col2:
    with open(html_file, "r", encoding="utf-8") as f:
        html_bytes = f.read()
    st.download_button(
        "🌐 HTML (.html)",
        data=html_bytes,
        file_name="PADER_Bisoprolol_Report.html",
        mime="text/html"
    )

with col3:
    with open(docx_file, "rb") as f:
        docx_bytes = f.read()
    st.download_button(
        "📘 Word Document (.docx)",
        data=docx_bytes,
        file_name="PADER_Bisoprolol_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

with col4:
    with open(pdf_file, "rb") as f:
        pdf_bytes = f.read()
    st.download_button(
        "📕 PDF Report (.pdf)",
        data=pdf_bytes,
        file_name="PADER_Bisoprolol_Report.pdf",
        mime="application/pdf"
    )

st.markdown("---")
st.markdown("### Document Preview")
st.markdown(full_md)
