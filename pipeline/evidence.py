"""
Evidence Packet & Versioning Generator.

Author: Madhav Kumar
Module: pipeline.evidence
"""

import hashlib
import json
import datetime
from typing import Dict, Any


def generate_evidence_with_versioning(analysis_results: Dict[str, Any], filepath: str, model_name: str) -> Dict[str, Any]:
    """Attach SHA-256 dataset hash, timestamp, and versioning metadata to evidence packet."""
    dataset_hash = "N/A"
    try:
        with open(filepath, "rb") as f:
            dataset_hash = hashlib.sha256(f.read()).hexdigest()[:12]
    except Exception:
        pass

    evidence = analysis_results.copy()
    evidence["metadata"] = {
        "dataset_hash": dataset_hash,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model_used": model_name,
        "temperature": 0.15,
        "prompt_version": "v1.0-FDA-PADER"
    }

    return evidence
