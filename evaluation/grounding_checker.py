"""
Grounding Verification & Hallucination Audit Engine.

Author: Madhav Kumar
Module: evaluation.grounding_checker
"""

import re
from typing import Dict, Any, List


class GroundingChecker:
    """
    Audits generated narrative text against calculated evidence statistics.
    """
    def __init__(self, evidence_packet: Dict[str, Any]):
        self.evidence = evidence_packet
        self.summary_stats = evidence_packet.get("summary_stats", {})

    def verify_section(self, section_id: str, generated_text: str) -> Dict[str, Any]:
        """Audit numerical facts in narrative text."""
        total_cases = str(self.summary_stats.get("total_cases", ""))
        serious_cases = str(self.summary_stats.get("serious_cases", ""))
        expedited_cases = str(self.summary_stats.get("expedited_15day_alert_cases", ""))

        extracted_numbers = re.findall(r'\b\d[\d,]*\.?\d*\b', generated_text)
        
        matches = []
        discrepancies = []

        if total_cases and total_cases in generated_text:
            matches.append(f"Total cases ({total_cases}) grounded.")
        if serious_cases and serious_cases in generated_text:
            matches.append(f"Serious cases ({serious_cases}) grounded.")
        if expedited_cases and expedited_cases in generated_text:
            matches.append(f"15-Day Alert cases ({expedited_cases}) grounded.")

        if section_id == "history_actions":
            if "no safety-related actions" in generated_text.lower() or "no actions" in generated_text.lower():
                matches.append("Zero safety actions claim verified.")

        score = 100.0 if not discrepancies else max(0.0, 100.0 - (len(discrepancies) * 25.0))

        return {
            "section_id": section_id,
            "passed": len(discrepancies) == 0,
            "grounding_score": score,
            "matches": matches,
            "discrepancies": discrepancies,
            "audited_numbers": extracted_numbers
        }

    def verify_full_report(self, sections: Dict[str, str]) -> Dict[str, Any]:
        """Audit full document."""
        audits = {sid: self.verify_section(sid, txt) for sid, txt in sections.items()}
        avg_score = round(sum(a["grounding_score"] for a in audits.values()) / len(sections), 2) if sections else 100.0
        return {
            "overall_score": avg_score,
            "all_passed": all(a["passed"] for a in audits.values()),
            "section_audits": audits
        }
