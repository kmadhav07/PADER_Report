"""
Dataset Validation Layer.

Author: Madhav Kumar
Module: pipeline.validator
"""

from typing import Dict, Any
import pandas as pd


def validate_icsr_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """Audit input dataset for completeness, missing fields, and unexpected values."""
    required_cols = ['safetyreportid', 'serious', 'receivedate', 'patient_reaction_reactionmeddrapt']
    missing_cols = [c for c in required_cols if c not in df.columns]

    total_rows = len(df)
    unique_cases = df['safetyreportid'].nunique() if 'safetyreportid' in df.columns else total_rows
    duplicates = total_rows - unique_cases

    null_counts = {col: int(df[col].isnull().sum()) for col in df.columns[:15]}

    return {
        "valid": len(missing_cols) == 0,
        "missing_required_columns": missing_cols,
        "total_rows": total_rows,
        "unique_cases": unique_cases,
        "duplicate_rows": duplicates,
        "missing_value_audit": null_counts
    }
