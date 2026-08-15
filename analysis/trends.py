"""
Time-Series Trends Analysis Module.

Author: Madhav Kumar
Module: analysis.trends
"""

from typing import Dict, Any
import pandas as pd


def analyze_monthly_trends(case_df: pd.DataFrame) -> Dict[str, int]:
    """Calculate monthly ICSR case submission trends."""
    if 'date_parsed' in case_df.columns and not case_df['date_parsed'].dropna().empty:
        m = case_df.set_index('date_parsed').resample('ME').size()
        m.index = m.index.strftime('%Y-%m')
        return m.to_dict()
    return {}
