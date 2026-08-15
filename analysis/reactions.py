"""
Adverse Reactions & Seriousness Analysis Module.

Author: Madhav Kumar
Module: analysis.reactions
"""

from typing import Dict, Any
from collections import Counter
import pandas as pd


def analyze_reactions(raw_df: pd.DataFrame, top_n: int = 15) -> Dict[str, Any]:
    """Analyze MedDRA Preferred Terms and serious reactions."""
    all_pts = []
    serious_pts = []

    for _, r in raw_df.iterrows():
        pt_str = str(r.get('patient_reaction_reactionmeddrapt', ''))
        is_ser = str(r.get('serious', '')).strip().lower() in ['serious', 'yes', '1', 'true']

        if pt_str and pt_str.lower() != 'nan':
            for pt in [p.strip() for p in pt_str.split(',') if p.strip()]:
                all_pts.append(pt)
                if is_ser:
                    serious_pts.append(pt)

    return {
        "top_reactions": dict(Counter(all_pts).most_common(top_n)),
        "top_serious_reactions": dict(Counter(serious_pts).most_common(top_n)),
        "total_reaction_occurrences": len(all_pts)
    }


def analyze_seriousness(case_df: pd.DataFrame) -> Dict[str, int]:
    """Compute distribution of ICH E2A seriousness criteria."""
    mapping = {
        "Hospitalization": 'seriousnesshospitalization',
        "Disabling": 'seriousnessdisabling',
        "Other Medically Important": 'seriousnessother',
        "Life-Threatening": 'seriousnesslifethreatening',
        "Death": 'seriousnessdeath',
        "Congenital Anomaly": 'seriousnesscongenitalanomali'
    }
    return {
        k: int(case_df[col].isin(['yes', '1', 'true']).sum())
        for k, col in mapping.items() if col in case_df.columns
    }
