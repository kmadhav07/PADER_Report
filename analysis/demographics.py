"""
Demographics Analysis Module.

Author: Madhav Kumar
Module: analysis.demographics
"""

from typing import Dict, Any
import pandas as pd
import numpy as np


def analyze_demographics(case_df: pd.DataFrame) -> Dict[str, Any]:
    """Compute gender, age group, and country distributions."""
    sex_series = case_df['patient_patientsex'].astype(str).str.strip().str.lower()
    male = int(sex_series.isin(['male', 'm', '1']).sum())
    female = int(sex_series.isin(['female', 'f', '2']).sum())
    unknown_sex = len(case_df) - male - female

    ages = case_df['age_num'].dropna() if 'age_num' in case_df.columns else pd.Series(dtype=float)
    pediatric = int((ages < 18).sum())
    adult = int(((ages >= 18) & (ages < 65)).sum())
    elderly = int((ages >= 65).sum())
    unknown_age = len(case_df) - len(ages)

    countries = case_df['occurcountry'].dropna().astype(str).str.strip().str.title().value_counts().to_dict()

    return {
        "sex": {"Male": male, "Female": female, "Unknown": unknown_sex},
        "age_groups": {
            "Pediatric (<18)": pediatric,
            "Adult (18-64)": adult,
            "Elderly (65+)": elderly,
            "Unknown": unknown_age
        },
        "countries": countries
    }
