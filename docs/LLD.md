# Low-Level Design (LLD) Document — RegIntel AI

Author: **Madhav Kumar**  
Role: **AI Engineer**  
Project: **Pharmacovigilance Safety Reporting Platform (PADER Engine)**

---

## 1. Class & Module Specifications

### A. Analytics Modules (`analysis/`)
- `DemographicsAnalyzer`: Analyzes gender ratios, age group stratifications (<18, 18-64, 65+), and reporter country distributions.
- `ReactionsAnalyzer`: Aggregates MedDRA Preferred Terms (PTs), serious reactions, and ICH E2A seriousness criteria counts.
- `DeterministicSafetyAnalyzer`: Master class wrapping demographics and reactions sub-analyzers into a unified evidence dictionary.

### B. LLM Subsystem (`llm/`)
- `BaseLLMProvider`: Abstract base class defining the provider interface (`generate()`).
- `GroqSafetyClient`: Client for Groq LPU API (`llama-3.3-70b-versatile`). Includes retry logic and automatic fallback to `OfflineFallbackProvider`.
- `LLMRouter`: Router facade mapping generation calls to the configured LLM provider.

### C. Pipeline Subsystem (`pipeline/`)
- `loader.py`: Loads and normalizes raw ICSR dataset records.
- `validator.py`: Validates schema completeness and logs missing value distributions.
- `analyzer.py`: Orchestrates deterministic safety analytics calls.
- `evidence.py`: Generates section-scoped JSON evidence packets and dataset SHA-256 integrity hashes.
- `prompt_builder.py`: Loads system prompts from `prompts/*.txt` and constructs user task prompts.
- `generator.py`: Orchestrates section-by-section and full report generation workflows.

### D. Verification & Evaluation (`evaluation/`)
- `GroundingChecker`: Verifies numerical claims in generated prose against calculated evidence stats.
- `XAIEvaluator`: Computes BLEU-2, ROUGE-L F1, Numerical Fact Precision, and sentence attribution maps.
- `SafetySHAPExplainer`: Fits a RandomForest model on ICSR features and calculates SHAP values for hospitalization risk prediction.

### E. Exporter Subsystem (`exporters/`)
- `markdown_exporter.py`: Writes Markdown output to disk.
- `html_exporter.py`: Converts Markdown to styled HTML with CSS badges.
- `docx_exporter.py`: Converts Markdown pipe tables to native Word tables via `python-docx`.
- `pdf_exporter.py`: Parses Markdown pipe tables into styled ReportLab `Table` objects with gridlines and cell styling.

---

## 2. Configuration Schemas

- `config/settings.py`: Defines base paths, default model parameters, and default dataset locations.
- `config/pader_config.yaml`: Defines PADER report type, section order, required analytics keys, and prompt template mappings.
- `config/psur_config.yaml`: Demonstrates framework extensibility for PSUR reporting.
