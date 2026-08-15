"""
Robust Dataset Loader & Cleaning Component.

Author: Madhav Kumar
Module: pipeline.loader
"""

import os
import pandas as pd
import numpy as np


def load_icsr_dataset(filepath: str) -> pd.DataFrame:
    """
    Load, clean, and normalize raw ICSR safety data.
    Defensive against missing columns, nulls, and schema variations.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset path invalid: {filepath}")

    df = pd.read_csv(filepath, low_memory=False)
    df.columns = [c.strip().lower() for c in df.columns]

    # Ensure safetyreportid exists; if missing, assign sequential IDs
    if 'safetyreportid' not in df.columns:
        df['safetyreportid'] = [f"CASE_{i+1:05d}" for i in range(len(df))]
    else:
        df['safetyreportid'] = df['safetyreportid'].ffill().astype(str)

    # Standardize boolean flags
    flag_cols = [
        'serious', 'seriousnessdeath', 'seriousnesslifethreatening',
        'seriousnesshospitalization', 'seriousnessdisabling',
        'seriousnesscongenitalanomali', 'seriousnessother', 'fulfillexpeditecriteria'
    ]
    for col in flag_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()
        else:
            df[col] = "no"

    # Normalize Age
    if 'patient_patientonsetage' in df.columns:
        df['age_num'] = pd.to_numeric(df['patient_patientonsetage'], errors='coerce')
    else:
        df['age_num'] = np.nan

    # Normalize Sex
    if 'patient_patientsex' not in df.columns:
        df['patient_patientsex'] = "Unknown"

    # Normalize Country
    if 'occurcountry' not in df.columns:
        df['occurcountry'] = "Unknown"

    # Normalize Date
    if 'receivedate' in df.columns:
        dates = df['receivedate'].astype(str).str.split('.').str[0]
        df['date_parsed'] = pd.to_datetime(dates, format='%Y%m%d', errors='coerce')
    else:
        df['date_parsed'] = pd.NaT

    return df
