"""
Unit Tests for XAI & Quantitative Evaluation Engine.

Author: Madhav Kumar
Module: tests.test_evaluator
"""

import unittest
from evaluation.evaluator import XAIEvaluator


class TestXAIEvaluator(unittest.TestCase):
    def setUp(self):
        self.evidence = {
            "summary_stats": {
                "total_cases": 1024,
                "serious_cases": 1023,
                "expedited_15day_alert_cases": 1023
            }
        }
        self.evaluator = XAIEvaluator(self.evidence)

    def test_bleu_and_rouge(self):
        cand = "A total of 1024 unique ICSR cases were processed."
        ref = "During the period 1024 unique ICSR cases were processed."
        bleu = self.evaluator.compute_bleu(cand, ref)
        rouge = self.evaluator.compute_rouge_l(cand, ref)
        self.assertGreater(bleu, 0.0)
        self.assertGreater(rouge, 0.0)

    def test_xai_attribution(self):
        text = "A total of 1024 cases were processed. Serious cases were 1023."
        attributions = self.evaluator.build_xai_attribution_map(text)
        self.assertEqual(len(attributions), 2)
        self.assertTrue(attributions[0]["is_grounded"])
        self.assertEqual(attributions[0]["evidence_key"], "summary_stats.total_cases")


if __name__ == "__main__":
    unittest.main()
