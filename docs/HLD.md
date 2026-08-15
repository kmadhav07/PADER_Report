# High-Level Design (HLD) Document — RegIntel AI

Author: **Madhav Kumar**  
Role: **AI Engineer**  
Project: **Pharmacovigilance Safety Reporting Platform (PADER Engine)**  
Standard: **FDA 21 CFR 314.80(c)(2)**

---

## 1. System Overview

RegIntel AI is a modular Python application designed to process Individual Case Safety Reports (ICSRs) and generate FDA-compliant Periodic Adverse Drug Experience Reports (PADERs).

The system decouples data processing from presentation, using Streamlit strictly as a UI frontend.

---

## 2. Layer Decomposition

```
[ Presentation Layer ]  ── Streamlit Multi-Page UI (app.py & pages/)
         │
         ▼
[ Business Pipeline ]   ── Report Pipeline Orchestrator (pipeline/generator.py)
         │
         ├──────► [ Analytics Core ]    ── Deterministic Safety Analyzer (analysis/)
         ├──────► [ Context Scoper ]    ── Evidence Packet Builder (pipeline/evidence.py)
         ├──────► [ LLM Layer ]         ── Groq API LPU Engine (llm/groq_client.py)
         ├──────► [ Audit Subsystem ]   ── Grounding Checker & XAI (evaluation/)
         └──────► [ Document Exporters] ── PDF, DOCX, HTML, MD Exporters (exporters/)
```

### Component Roles:
- **Presentation Layer**: Streamlit UI shell with 10 pages for Dashboard, Upload, Explorer, Analytics, Generator, Review, Evidence Viewer, Exporter, Settings, and Logs.
- **Business Pipeline**: Orchestrates dataset loading, validation, analytics execution, evidence scoping, prompt assembly, and section generation.
- **Analytics Core**: Pure Python (`pandas`) modules for case deduplication, seriousness criteria breakdown, MedDRA Preferred Term frequency ranking, and monthly trends.
- **Context Scoper**: Builds section-scoped JSON evidence packets to prevent context saturation and numerical hallucinations.
- **LLM Layer**: Polymorphic provider abstraction supporting Groq API (`llama-3.3-70b-versatile`), Gemini, HuggingFace, and an offline rule-based fallback engine.
- **Audit Subsystem**: Cross-checks generated prose numbers against pre-computed evidence stats and calculates BLEU-2, ROUGE-L, and SHAP feature importance.
- **Document Exporters**: Converts Markdown output into styled PDF files (via ReportLab tables), Word documents (`.docx`), and interactive HTML.

---

## 3. Data Integrity & Auditability

- **SHA-256 Dataset Hash**: Calculated on data load and embedded in report metadata for regulatory audit trails.
- **Human Sign-Off**: Interface for medical reviewers to inspect evidence side-by-side with generated text, edit inline, and approve sections.
