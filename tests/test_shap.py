"""
Unit Tests for SHAP Feature Importance Explainer.

Author: Madhav Kumar
Module: tests.test_shap
"""

import unittest
import os
from pipeline.loader import load_icsr_dataset
from evaluation.shap_explainer import SafetySHAPExplainer


class TestSafetySHAPExplainer(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "Bisoprolol_icsr_sample_1068rows.csv")
        self.df = load_icsr_dataset(self.data_path)
        self.explainer = SafetySHAPExplainer(self.df)

    def test_fit_and_explain(self):
        res = self.explainer.fit_and_explain()
        self.assertIn("model_accuracy", res)
        self.assertIn("feature_importance", res)
        self.assertIn("Patient Age", res["feature_importance"])
        self.assertGreater(res["model_accuracy"], 50.0)


if __name__ == "__main__":
    unittest.main()
