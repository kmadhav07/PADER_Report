"""
SHAP (SHapley Additive exPlanations) & ML Feature Importance Module.

Author: Madhav Kumar
Module: evaluation.shap_explainer
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import shap


class SafetySHAPExplainer:
    """
    Computes SHAP feature importance values for safety outcome risk prediction.
    Explains which patient factors (age, sex, country, adverse reaction) drive hospitalization risk.
    """
    def __init__(self, raw_df: pd.DataFrame):
        self.raw_df = raw_df.copy()
        self.model = None
        self.feature_names = []
        self.shap_values = None
        self.explainer = None
        self.X_encoded = None

    def prepare_features(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Preprocess ICSR attributes into machine learning feature matrix."""
        df = self.raw_df.copy()
        
        # Target variable: Hospitalization Risk (1 vs 0)
        if 'seriousnesshospitalization' in df.columns:
            df['target'] = df['seriousnesshospitalization'].astype(str).str.strip().str.lower().isin(['yes', '1', 'true']).astype(int)
        else:
            df['target'] = df['serious'].astype(str).str.strip().str.lower().isin(['serious', 'yes', '1', 'true']).astype(int)

        # Feature 1: Age
        if 'patient_patientonsetage' in df.columns:
            df['age_feat'] = pd.to_numeric(df['patient_patientonsetage'], errors='coerce').fillna(55.0)
        else:
            df['age_feat'] = 55.0

        # Feature 2: Sex
        le_sex = LabelEncoder()
        sex_col = df['patient_patientsex'].astype(str).str.strip().str.lower() if 'patient_patientsex' in df.columns else pd.Series(['unknown']*len(df))
        df['sex_feat'] = le_sex.fit_transform(sex_col)

        # Feature 3: Country
        le_country = LabelEncoder()
        country_col = df['occurcountry'].astype(str).str.strip().str.title() if 'occurcountry' in df.columns else pd.Series(['Unknown']*len(df))
        df['country_feat'] = le_country.fit_transform(country_col)

        # Feature 4: Primary Adverse Reaction
        le_rx = LabelEncoder()
        rx_col = df['patient_reaction_reactionmeddrapt'].astype(str).str.split(',').str[0].str.strip() if 'patient_reaction_reactionmeddrapt' in df.columns else pd.Series(['Unknown']*len(df))
        df['reaction_feat'] = le_rx.fit_transform(rx_col)

        X = df[['age_feat', 'sex_feat', 'country_feat', 'reaction_feat']].copy()
        y = df['target']
        self.feature_names = ['Patient Age', 'Patient Sex', 'Reporter Country', 'Adverse Event (PT)']
        X.columns = self.feature_names
        
        return X, y

    def fit_and_explain(self) -> Dict[str, Any]:
        """Fit Random Forest and compute SHAP values."""
        X, y = self.prepare_features()
        self.X_encoded = X

        # Train Random Forest Classifier
        self.model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
        self.model.fit(X, y)

        # Compute SHAP values
        self.explainer = shap.TreeExplainer(self.model)
        shap_vals = self.explainer.shap_values(X)

        if isinstance(shap_vals, list):
            vals = shap_vals[1] if len(shap_vals) > 1 else shap_vals[0]
        else:
            vals = shap_vals

        if len(vals.shape) == 3:
            vals = vals[:, :, 1]

        mean_abs_shap = np.abs(vals).mean(axis=0)

        feature_importance = dict(zip(self.feature_names, [round(float(v), 4) for v in mean_abs_shap]))
        
        # Accuracy score
        accuracy = round(float(self.model.score(X, y) * 100), 2)

        return {
            "model_accuracy": accuracy,
            "feature_importance": feature_importance,
            "shap_summary": feature_importance
        }
