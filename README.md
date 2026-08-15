# RegIntel AI — Pharmacovigilance Safety Reporting Engine

A modular Python platform for transforming post-marketing Individual Case Safety Reports (ICSRs) into US FDA 21 CFR 314.80 Periodic Adverse Drug Experience Reports (PADER).

Author: **Madhav Kumar**  
Stack: Python 3.11+, Streamlit, Groq API (Llama 3.3 70B), Pandas, Plotly, SHAP, ReportLab, Docker  
Repository: [https://github.com/kmadhav07/PADER_Report.git](https://github.com/kmadhav07/PADER_Report.git)

---

## Architecture Overview

![RegIntel AI Project Architecture](assets/architecture_diagram.png)

---

## Overview

In post-marketing drug safety, pharmaceutical companies process thousands of Individual Case Safety Reports (ICSRs) per year. Submitting annual aggregate reports (PADERs) to regulatory agencies requires strict data accuracy.

Passing raw ICSR tables directly into Large Language Models (LLMs) often leads to numerical hallucinations, incorrect counts, and non-compliant safety summaries. This project uses a hybrid architecture:

- **Deterministic Python Engine**: Handles 100% of arithmetic calculations, deduplication, demographic stratification, and MedDRA reaction rankings.
- **LLM Narrative Synthesis**: Reserves the LLM (Groq Llama 3.3 70B) strictly for natural language regulatory prose generation using section-scoped JSON evidence packets.
- **Grounding Verification & XAI**: Cross-checks generated prose numbers against pre-computed metrics and provides SHAP feature attributions for risk drivers.

---

## Included Clinical Safety Datasets

The platform includes **6 pre-loaded pharmacovigilance safety datasets** (`data/*.csv`) representing different therapeutic classes for live testing and demonstration:

1. **`Bisoprolol_icsr_sample_1068rows.csv`**: Primary FDA dataset (1,068 rows / 1,024 unique ICSR cases). Focus: Beta-blocker safety profile (Acute kidney injury, Hypotension, Bradycardia).
2. **`Atorvastatin_icsr_sample_50rows.csv`**: Statin class safety profile (Myalgia, Rhabdomyolysis, Hepatic enzyme increased, Blood CPK increased).
3. **`Metformin_icsr_sample_50rows.csv`**: Anti-diabetic class safety profile (Lactic acidosis, Upper abdominal pain, Renal impairment, Hypoglycaemia).
4. **`Apixaban_icsr_sample_50rows.csv`**: Anticoagulant class safety profile (Gastrointestinal haemorrhage, Epistaxis, Haematoma, Anaemia).
5. **`Pembrolizumab_icsr_sample_50rows.csv`**: Immuno-oncology class safety profile (Pneumonitis, Colitis, Immune-mediated hepatitis, Thyroiditis).
6. **`Semaglutide_icsr_sample_50rows.csv`**: GLP-1 receptor agonist safety profile (Nausea, Vomiting, Pancreatitis acute, Gastroparesis, Dehydration).

*Users can dynamically switch between pre-loaded datasets or upload their own custom ICSR CSV files via Page 2 (`📂 Upload`).*

---

## Repository Structure

```
PADER_REPORT/
├── app.py                     # Streamlit application entry point
├── pages/                     # Multi-page Streamlit UI modules (10 Pages)
│   ├── 1_🏠_Dashboard.py
│   ├── 2_📂_Upload.py
│   ├── 3_📊_Explorer.py
│   ├── 4_📈_Analytics.py
│   ├── 5_🧠_Generator.py
│   ├── 6_📝_Review.py
│   ├── 7_🔍_Evidence_Viewer.py
│   ├── 8_📄_Report_Viewer.py
│   ├── 9_⚙️_Settings.py
│   └── 10_📜_Logs.py
├── config/                    # YAML report schemas & app settings
├── prompts/                   # External section prompt templates
├── analysis/                  # Deterministic safety analysis engine
├── llm/                       # Provider abstraction (Groq, Gemini, HF, Offline)
├── pipeline/                  # Business logic orchestrator
├── evaluation/                # Grounding auditor & SHAP explainer
├── exporters/                 # Multi-format document exporters (PDF, DOCX, HTML, MD)
├── tests/                     # Unit test suite
├── docs/                      # Technical specifications (HLD & LLD)
├── outputs/                   # Generated output reports
├── assets/                    # System architecture diagrams
├── data/                      # 6 Pre-loaded ICSR clinical safety datasets
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Key Features

1. **Deterministic Data Analysis**: Deduplicates records by `safetyreportid` and computes ICH E2A seriousness breakdown, MedDRA Preferred Term frequencies, patient age/sex stratifications, and time-series trends in pure Python.
2. **Context Isolation**: Sends isolated JSON evidence packets per section instead of dumping entire datasets into the model context.
3. **Sub-Second Groq LPU Speed**: Leverages Groq's LPU acceleration (`llama-3.3-70b-versatile`) with automatic fallback to a local rule engine if rate-limited.
4. **Explainable AI & Evaluation**: Computes BLEU-2, ROUGE-L F1 scores, Numerical Fact Precision, and SHAP feature importance for seriousness prediction.
5. **Human-in-the-Loop Review**: Interface for medical reviewers to inspect evidence side-by-side with prose, edit text inline, and approve sections.
6. **Multi-Format Export**: Generates styled PDF reports (via ReportLab tables), Word documents (`.docx`), interactive HTML, and Markdown.

---

## Quickstart

### Local Setup
```bash
# 1. Clone repository & enter directory
git clone https://github.com/kmadhav07/PADER_Report.git
cd PADER_Report

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add API key to .env
cp .env.example .env
# Set GROQ_API_KEY=gsk_...

# 4. Run Streamlit application
streamlit run app.py
```

### Running Unit Tests
```bash
python3 -m unittest discover tests
```

### Docker Setup
```bash
docker-compose up --build -d
```

---

## Configuration-Driven Extensibility

Report schemas are defined externally in YAML (`config/*.yaml`). To add support for new regulatory report types (such as PSUR, PBRER, or DSUR), create a new YAML configuration defining the required sections and analytics mappings. No changes to core pipeline Python code are required.

---

## License

MIT License.
