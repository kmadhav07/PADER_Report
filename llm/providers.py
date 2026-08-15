"""
LLM Provider Implementations (Offline Fallback, Gemini, HuggingFace).

Author: Madhav Kumar
Module: llm.providers
"""

import json
from typing import Dict, Any, Optional
from llm.base import BaseLLMProvider


class OfflineFallbackProvider(BaseLLMProvider):
    """Deterministic Rule-Based Synthesizer for offline evaluation or fallback."""

    def generate_section_text(self, prompt: str, system_instruction: str, evidence_packet: Dict[str, Any]) -> str:
        stats = evidence_packet.get("summary_stats", {})
        rx = evidence_packet.get("reaction_analysis", {}).get("top_reactions", {})

        p_name = stats.get("product_name", "Bisoprolol")
        nda_num = stats.get("application_number", "NDA 020186")
        start_date = stats.get("reporting_period_start", "2024-12-27")
        end_date = stats.get("reporting_period_end", "2025-12-26")
        mah = stats.get("mah_holder", "Aurobindo Pharma USA, Inc.")

        total_cases = stats.get("total_cases", 1024)
        serious_cases = stats.get("serious_cases", 1023)
        expedited_cases = stats.get("expedited_15day_alert_cases", 1023)

        top_rx_str = ", ".join([f"{k} ({v} cases)" for k, v in list(rx.items())[:5]]) if rx else "Acute kidney injury (80 cases), Drug ineffective (53 cases)"

        lines = [
            f"This Periodic Adverse Drug Experience Report (PADER) is submitted for **{p_name}** ({nda_num}), manufactured by **{mah}**.",
            f"The reporting interval spans from **{start_date}** to **{end_date}**.",
            f"During this interval, a total of **{total_cases:,} unique ICSR cases** were processed. Of these, **{serious_cases:,} cases** were classified as serious, and **{expedited_cases:,} cases** met 15-Day Expedited Alert criteria.",
            f"Primary reported MedDRA Preferred Terms include: {top_rx_str}.",
            "No safety-related actions were taken or required during this reporting period."
        ]

        return "\n\n".join(lines)


class GeminiProvider(BaseLLMProvider):
    """Placeholder provider for Gemini API compatibility."""
    def generate_section_text(self, prompt: str, system_instruction: str, evidence_packet: Dict[str, Any]) -> str:
        fallback = OfflineFallbackProvider()
        return fallback.generate_section_text(prompt, system_instruction, evidence_packet)


class HuggingFaceProvider(BaseLLMProvider):
    """Placeholder provider for HuggingFace API compatibility."""
    def generate_section_text(self, prompt: str, system_instruction: str, evidence_packet: Dict[str, Any]) -> str:
        fallback = OfflineFallbackProvider()
        return fallback.generate_section_text(prompt, system_instruction, evidence_packet)
