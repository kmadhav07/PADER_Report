"""
Object-Oriented Deterministic Safety Analysis Engine.

Author: Madhav Kumar
Module: analysis.safety_analyzer
"""

import os
from typing import Dict, Any, List
from collections import Counter
import pandas as pd
import numpy as np


class DemographicsAnalyzer:
    """Analyzes gender, age groups, and country distributions."""
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def analyze(self) -> Dict[str, Any]:
        sex_series = self.df['patient_patientsex'].astype(str).str.strip().str.lower()
        male = int(sex_series.isin(['male', 'm', '1']).sum())
        female = int(sex_series.isin(['female', 'f', '2']).sum())
        unknown_sex = len(self.df) - male - female

        ages = self.df['age_num'].dropna() if 'age_num' in self.df.columns else pd.Series(dtype=float)
        countries = self.df['occurcountry'].dropna().astype(str).str.strip().str.title().value_counts().to_dict()

        return {
            "sex": {"Male": male, "Female": female, "Unknown": unknown_sex},
            "age_groups": {
                "Pediatric (<18)": int((ages < 18).sum()),
                "Adult (18-64)": int(((ages >= 18) & (ages < 65)).sum()),
                "Elderly (65+)": int((ages >= 65).sum()),
                "Unknown": len(self.df) - len(ages)
            },
            "countries": countries
        }


class ReactionsAnalyzer:
    """Analyzes MedDRA Preferred Terms and seriousness criteria."""
    def __init__(self, raw_df: pd.DataFrame, case_df: pd.DataFrame):
        self.raw_df = raw_df
        self.case_df = case_df

    def analyze_reactions(self, top_n: int = 15) -> Dict[str, Any]:
        all_pts, serious_pts = [], []
        for _, r in self.raw_df.iterrows():
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

    def analyze_seriousness(self) -> Dict[str, int]:
        mapping = {
            "Hospitalization": 'seriousnesshospitalization',
            "Disabling": 'seriousnessdisabling',
            "Other Medically Important": 'seriousnessother',
            "Life-Threatening": 'seriousnesslifethreatening',
            "Death": 'seriousnessdeath',
            "Congenital Anomaly": 'seriousnesscongenitalanomali'
        }
        return {
            k: int(self.case_df[col].isin(['yes', '1', 'true']).sum())
            for k, col in mapping.items() if col in self.case_df.columns
        }


class DeterministicSafetyAnalyzer:
    """Master Object-Oriented Safety Analyzer."""
    def __init__(self, raw_df: pd.DataFrame):
        self.raw_df = raw_df
        self.case_df = raw_df.drop_duplicates(subset=['safetyreportid']).copy() if 'safetyreportid' in raw_df.columns else raw_df.copy()
        
        self.demographics_engine = DemographicsAnalyzer(self.case_df)
        self.reactions_engine = ReactionsAnalyzer(self.raw_df, self.case_df)

    def summary_metrics(self) -> Dict[str, Any]:
        total_cases = len(self.case_df)
        serious_count = int(self.case_df['serious'].isin(['serious', 'yes', '1', 'true']).sum())
        non_serious = total_cases - serious_count
        expedited = int(self.case_df['fulfillexpeditecriteria'].isin(['yes', '1', 'true']).sum())

        dates = self.raw_df['date_parsed'].dropna() if 'date_parsed' in self.raw_df.columns else pd.Series()
        start_date = dates.min().strftime('%Y-%m-%d') if not dates.empty else "2024-12-27"
        end_date = dates.max().strftime('%Y-%m-%d') if not dates.empty else "2025-12-26"

        return {
            "total_rows": len(self.raw_df),
            "total_cases": total_cases,
            "serious_cases": serious_count,
            "non_serious_cases": non_serious,
            "serious_percentage": round((serious_count / total_cases * 100), 2) if total_cases > 0 else 0.0,
            "expedited_15day_alert_cases": expedited,
            "reporting_period_start": start_date,
            "reporting_period_end": end_date,
            "product_name": "Bisoprolol",
            "application_number": "NDA 020186",
            "mah_holder": "Aurobindo Pharma USA, Inc."
        }

    def monthly_trends(self) -> Dict[str, int]:
        if 'date_parsed' in self.case_df.columns and not self.case_df['date_parsed'].dropna().empty:
            m = self.case_df.set_index('date_parsed').resample('ME').size()
            m.index = m.index.strftime('%Y-%m')
            return m.to_dict()
        return {}

    def analyze_all(self) -> Dict[str, Any]:
        rx_data = self.reactions_engine.analyze_reactions()
        outcomes = Counter()
        for _, r in self.raw_df.iterrows():
            out_str = str(r.get('patient_reaction_reactionoutcome', '')).strip().lower()
            if out_str and out_str != 'nan':
                for o in [x.strip() for x in out_str.split(',') if x.strip()]:
                    outcomes[o] += 1
        rx_data["outcomes"] = dict(outcomes)

        alerts_df = self.case_df[self.case_df['fulfillexpeditecriteria'].isin(['yes', '1', 'true'])].head(15)
        sample_alerts = [
            {
                "case_id": str(r.get('safetyreportid', '')),
                "country": str(r.get('occurcountry', '')).title(),
                "age": str(r.get('patient_patientonsetage', 'N/A')),
                "sex": str(r.get('patient_patientsex', 'N/A')).title(),
                "reaction": str(r.get('patient_reaction_reactionmeddrapt', 'N/A')),
                "seriousness": "Serious",
                "outcome": str(r.get('patient_reaction_reactionoutcome', 'Unknown')).title(),
                "receive_date": str(r.get('receivedate', 'N/A')),
                "reporter": str(r.get('primarysource_qualification', 'N/A')).title()
            }
            for _, r in alerts_df.iterrows()
        ]

        reporters = self.case_df['primarysource_qualification'].dropna().str.strip().str.title().value_counts().to_dict() if 'primarysource_qualification' in self.case_df.columns else {}

        return {
            "summary_stats": self.summary_metrics(),
            "seriousness_breakdown": self.reactions_engine.analyze_seriousness(),
            "demographics": self.demographics_engine.analyze(),
            "reaction_analysis": rx_data,
            "monthly_trends": self.monthly_trends(),
            "reporters": reporters,
            "sample_alerts": sample_alerts
        }
