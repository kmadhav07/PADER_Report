# Architecture Reference — RegIntel AI

Author: **Madhav Kumar**  
System: **Pharmacovigilance Safety Reporting Platform (PADER Engine)**

---

## System Architecture Diagram

![RegIntel AI System Architecture](assets/architecture_diagram.png)

---

## 1. Architectural Design Principles

This project follows a clean, modular Python architecture. Streamlit is used exclusively as a presentation frontend, keeping all business logic, data processing, and LLM orchestration decoupled.

```
+-------------------------------------------------------+
|                Streamlit Presentation Layer           |
|                (app.py & pages/ 1..10)                |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
|               Business Logic & Pipeline               |
|                (pipeline/generator.py)                |
+-------------------------------------------------------+
       |                   |                  |
       v                   v                  v
+--------------+    +--------------+   +--------------+
| Analytics    |    | LLM Layer    |   | Exporters    |
| (analysis/)  |    | (llm/)       |   | (exporters/) |
+--------------+    +--------------+   +--------------+
```

---

## 2. End-to-End Data Pipeline Flow

```mermaid
sequenceDiagram
    autonumber
    participant UI as Streamlit UI (pages/)
    participant PL as Pipeline (pipeline/generator.py)
    participant DA as Safety Analyzer (analysis/)
    participant LLM as Groq API (llm/groq_client.py)
    participant EV as Evaluator & Grounding (evaluation/)
    participant EX as Exporters (exporters/)

    UI->>PL: Request Section / Full Report Generation
    PL->>DA: Run Deterministic Safety Analysis
    DA-->>PL: Return Ground-Truth Evidence Dictionary
    PL->>PL: Scope Evidence JSON & Load Section Prompt
    PL->>LLM: Generate Narrative (Llama 3.3 70B)
    LLM-->>PL: Return Generated Narrative Text
    PL->>EV: Verify Numerical Grounding & Compute XAI Metrics
    EV-->>PL: Return Grounding Score & Attribution Map
    PL-->>UI: Display Generated Narrative in Review Workspace
    UI->>EX: Request PDF / DOCX / HTML Export
    EX-->>UI: Return Formatted Document Artifacts
```

---

## 3. Provider Abstraction Layer

```mermaid
classDiagram
    class BaseLLMProvider {
        +generate(prompt, system_instruction, evidence)
    }
    class GroqProvider {
        +generate(prompt, system_instruction, evidence)
    }
    class GeminiProvider {
        +generate(prompt, system_instruction, evidence)
    }
    class HuggingFaceProvider {
        +generate(prompt, system_instruction, evidence)
    }
    class OfflineFallbackProvider {
        +generate(prompt, system_instruction, evidence)
    }

    BaseLLMProvider <|-- GroqProvider
    BaseLLMProvider <|-- GeminiProvider
    BaseLLMProvider <|-- HuggingFaceProvider
    BaseLLMProvider <|-- OfflineFallbackProvider
```

---

## 4. Key Engineering Choices

- **No Framework Dependencies**: Built without LangChain, LangGraph, or AutoGen to avoid unnecessary abstraction layers and performance overhead.
- **Resilient Fallback**: Uses Groq API as the primary engine with a 1.2s delay between sections to stay within TPM limits, falling back automatically to the offline rule synthesizer if rate-limited.
- **Custom Document Rendering**: Markdown pipe tables are parsed into native ReportLab `Table` objects for PDF rendering and `python-docx` elements for Word rendering.
