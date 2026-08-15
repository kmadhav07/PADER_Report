"""
Unit Tests for Deterministic Safety Analytics Engine.

Author: Madhav Kumar
Module: tests.test_analysis
"""

import unittest
import os
from pipeline.loader import load_icsr_dataset
from analysis.safety_analyzer import DeterministicSafetyAnalyzer


class TestSafetyAnalytics(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "Bisoprolol_icsr_sample_1068rows.csv")
        self.df = load_icsr_dataset(self.data_path)
        self.analyzer = DeterministicSafetyAnalyzer(self.df)

    def test_summary_metrics(self):
        stats = self.analyzer.summary_metrics()
        self.assertEqual(stats["total_cases"], 1024)
        self.assertEqual(stats["total_rows"], 1068)
        self.assertEqual(stats["serious_cases"], 1024)
        self.assertEqual(stats["expedited_15day_alert_cases"], 1023)

    def test_seriousness_breakdown(self):
        seriousness = self.analyzer.reactions_engine.analyze_seriousness()
        self.assertIn("Hospitalization", seriousness)
        self.assertGreater(seriousness["Hospitalization"], 0)

    def test_reactions(self):
        rx = self.analyzer.reactions_engine.analyze_reactions()
        self.assertIn("Acute kidney injury", rx["top_reactions"])
        self.assertEqual(rx["top_reactions"]["Acute kidney injury"], 72)


if __name__ == "__main__":
    unittest.main()
