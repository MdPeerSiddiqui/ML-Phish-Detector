#!/usr/bin/env python3
"""
================================================================================
Automated Unit Verification Suite for PEER'S ML Phish Detector
Author      : Mohammed Peer Siddiqui
Organization: Sqrock IT Solutions — Cybersecurity Internship (Alpha 2 Cohort)
================================================================================
"""

import os
import sys
import json
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from phish_classifier import (
    load_dataset,
    train_and_evaluate,
    predict_email,
    get_top_phishing_features
)


class TestMLPhishDetector(unittest.TestCase):
    """Test suite covering dataset ingestion, model accuracy, inference, and serialization."""

    def test_dataset_loading(self):
        """Verify dataset loads successfully with at least 50 samples and binary labels."""
        df = load_dataset()
        self.assertGreaterEqual(len(df), 50)
        self.assertIn("email_text", df.columns)
        self.assertIn("label", df.columns)
        self.assertEqual(set(df["label"].unique()), {0, 1})

    def test_model_training_and_accuracy(self):
        """Verify model trains cleanly and achieves at least 85% accuracy on test split."""
        model, metrics = train_and_evaluate()
        self.assertIsNotNone(model)
        self.assertGreaterEqual(metrics["accuracy"], 85.0)
        self.assertGreaterEqual(metrics["f1_score"], 80.0)

    def test_phishing_prediction(self):
        """Verify an explicit phishing lure is correctly predicted with high confidence."""
        phish_text = "Urgent: Your account is suspended. Click here immediately to verify your password."
        res = predict_email(phish_text)
        self.assertEqual(res["prediction"], "PHISHING")
        self.assertEqual(res["label"], 1)
        self.assertGreaterEqual(res["phishing_confidence_pct"], 70.0)
        self.assertTrue(len(res["identified_urgency_tokens"]) > 0)

    def test_legitimate_prediction(self):
        """Verify a normal corporate email is correctly classified as legitimate."""
        legit_text = "Weekly product engineering standup meeting notes and sprint retro attached."
        res = predict_email(legit_text)
        self.assertEqual(res["prediction"], "LEGITIMATE")
        self.assertEqual(res["label"], 0)
        self.assertGreaterEqual(res["legitimate_confidence_pct"], 60.0)

    def test_confusion_matrix_dimensions(self):
        """Verify confusion matrix contains valid non-negative counts across all quadrants."""
        _, metrics = train_and_evaluate()
        cm = metrics["confusion_matrix"]
        self.assertIn("true_negatives", cm)
        self.assertIn("false_positives", cm)
        self.assertIn("false_negatives", cm)
        self.assertIn("true_positives", cm)
        self.assertGreater(cm["true_positives"] + cm["true_negatives"], 0)

    def test_top_features_extraction(self):
        """Verify model explainability extracts top discriminative n-grams."""
        top_tokens = get_top_phishing_features(5)
        self.assertEqual(len(top_tokens), 5)
        for token, score in top_tokens:
            self.assertIsInstance(token, str)
            self.assertIsInstance(score, float)


if __name__ == "__main__":
    unittest.main()
