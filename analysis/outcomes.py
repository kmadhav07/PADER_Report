"""
Outcomes Analysis Module.

Author: Madhav Kumar
Module: analysis.outcomes
"""

from typing import Dict, Any
from collections import Counter
import pandas as pd


def analyze_outcomes(raw_df: pd.DataFrame) -> Dict[str, int]:
    """Compute distribution of event outcomes."""
    outcomes = Counter()
    for _, r in raw_df.iterrows():
        out_str = str(r.get('patient_reaction_reactionoutcome', '')).strip().lower()
        if out_str and out_str != 'nan':
            for o in [x.strip() for x in out_str.split(',') if x.strip()]:
                outcomes[o] += 1
    return dict(outcomes)
