"""
Report Generation Pipeline Orchestrator.

Author: Madhav Kumar
Module: pipeline.generator
"""

import os
import yaml
import time
from typing import Dict, Any, List, Optional
from pipeline.loader import load_icsr_dataset
from pipeline.validator import validate_icsr_dataset
from pipeline.analyzer import run_deterministic_analysis
from pipeline.evidence import generate_evidence_with_versioning
from pipeline.prompt_builder import load_prompt_template, build_section_prompt
from llm.router import LLMRouter
from evaluation.grounding_checker import GroundingChecker
from config.settings import CONFIG_DIR


class ReportPipeline:
    """
    End-to-end report generation pipeline driven by YAML schema configurations.
    """
    def __init__(self, data_path: str, config_name: str = "pader_config.yaml", provider_type: str = "groq", api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.data_path = data_path
        self.config = self._load_yaml_config(config_name)
        self.df = load_icsr_dataset(data_path)
        self.validation = validate_icsr_dataset(self.df)
        self.raw_analysis = run_deterministic_analysis(self.df)
        
        self.model_name = model_name or "llama-3.3-70b-versatile"
        self.evidence_packet = generate_evidence_with_versioning(self.raw_analysis, data_path, self.model_name)
        
        self.router = LLMRouter(provider_type=provider_type, api_key=api_key, model_name=self.model_name)
        self.verifier = GroundingChecker(self.evidence_packet)
        
        self.sections_content: Dict[str, str] = {}
        self.section_approvals: Dict[str, bool] = {sec["id"]: False for sec in self.config.get("sections", [])}
        self.section_audits: Dict[str, Any] = {}

    def _load_yaml_config(self, filename: str) -> Dict[str, Any]:
        path = os.path.join(CONFIG_DIR, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {"report_type": "PADER", "sections": []}

    def generate_section(self, section_id: str, custom_instruction: str = "") -> str:
        """Generate a single section with rate limit retries."""
        sec_config = next((s for s in self.config.get("sections", []) if s["id"] == section_id), None)
        if not sec_config:
            raise ValueError(f"Unknown section id: {section_id}")

        req_keys = sec_config.get("requires_analysis", [])
        scoped_evidence = {k: self.evidence_packet[k] for k in req_keys if k in self.evidence_packet}
        if "metadata" in self.evidence_packet:
            scoped_evidence["metadata"] = self.evidence_packet["metadata"]

        system_instruction = load_prompt_template(sec_config.get("prompt_template", ""))
        user_prompt = build_section_prompt(sec_config["title"], custom_instruction)

        text = None
        for attempt in range(3):
            try:
                text = self.router.generate_section_text(
                    prompt=user_prompt,
                    system_instruction=system_instruction,
                    evidence_packet=scoped_evidence
                )
                break
            except Exception as e:
                print(f"[ReportPipeline Warning] Attempt {attempt+1} failed: {e}. Retrying in 2 seconds...")
                time.sleep(2.0)

        if not text:
            text = self.router.generate_section_text(user_prompt, system_instruction, scoped_evidence)

        self.sections_content[section_id] = text
        self.section_audits[section_id] = self.verifier.verify_section(section_id, text)
        return text

    def generate_full_report(self) -> Dict[str, str]:
        """Generate all sections configured in YAML schema with pacing."""
        for idx, sec in enumerate(self.config.get("sections", [])):
            if idx > 0:
                time.sleep(1.2)
            self.generate_section(sec["id"])
        return self.sections_content

    def update_section_text(self, section_id: str, new_text: str):
        """Update text during human review."""
        self.sections_content[section_id] = new_text
        self.section_audits[section_id] = self.verifier.verify_section(section_id, new_text)

    def set_section_approval(self, section_id: str, approved: bool):
        """Approve or flag section."""
        self.section_approvals[section_id] = approved

    def assemble_final_markdown(self) -> str:
        """Assemble markdown document."""
        stats = self.evidence_packet["summary_stats"]
        meta = self.evidence_packet.get("metadata", {})
        
        md = [
            f"# {self.config.get('full_name', 'Periodic Safety Report')}",
            f"**Drug Product**: {stats.get('product_name', 'Bisoprolol')}",
            f"**Application Identifier**: {stats.get('application_number', 'NDA 020186')}",
            f"**Reporting Period**: {stats.get('reporting_period_start')} to {stats.get('reporting_period_end')}",
            f"**Marketing Authorization Holder**: {stats.get('mah_holder')}",
            f"**Regulatory Framework**: {self.config.get('regulatory_framework', '21 CFR 314.80')}",
            f"**Dataset SHA-256 Hash**: `{meta.get('dataset_hash', 'N/A')}` | **Engine**: `{meta.get('model_used')}`\n",
            "---\n"
        ]

        for sec in self.config.get("sections", []):
            sid = sec["id"]
            title = sec["title"]
            text = self.sections_content.get(sid, "_Section narrative not generated._")
            status = "✅ Approved" if self.section_approvals.get(sid, False) else "⏳ Pending Sign-off"

            md.append(f"## {title}")
            md.append(f"*Status: {status}*\n")
            md.append(text)
            md.append("\n---\n")

        return "\n".join(md)
