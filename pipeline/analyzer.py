"""
Deterministic Analysis Orchestrator.

Author: Madhav Kumar
Module: pipeline.analyzer
"""

from typing import Dict, Any
import pandas as pd
from analysis.safety_analyzer import DeterministicSafetyAnalyzer


def run_deterministic_analysis(raw_df: pd.DataFrame) -> Dict[str, Any]:
    """Execute all modular deterministic safety analyses using OOP analyzer."""
    analyzer = DeterministicSafetyAnalyzer(raw_df)
    return analyzer.analyze_all()
