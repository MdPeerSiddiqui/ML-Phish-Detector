#!/usr/bin/env python3
"""
================================================================================
PEER'S ML PHISH DETECTOR v2.5 — Machine Learning Phishing Email Classifier
Author      : Mohammed Peer Siddiqui
Organization: Sqrock IT Solutions — Cybersecurity Internship (Alpha 2 Cohort)
Track       : Social Engineering Attack Simulations Using Python (Day 12)
Standard    : NIST SP 800-177 (Trustworthy Email) | MITRE ATT&CK T1566 (Phishing)
================================================================================
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from colorama import Fore, Style, init

init(autoreset=True)

BANNER = f"""
{Fore.CYAN}███╗   ███╗██╗         ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗
{Fore.CYAN}████╗ ████║██║         ██╔══██╗██║  ██║██║██╔════╝██║  ██║
{Fore.CYAN}██╔████╔██║██║         ██████╔╝███████║██║███████╗███████║
{Fore.BLUE}██║╚██╔╝██║██║         ██╔═══╝ ██╔══██║██║╚════██║██╔══██║
{Fore.BLUE}██║ ╚═╝ ██║███████╗    ██║     ██║  ██║██║███████║██║  ██║
{Fore.BLUE}╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝
{Fore.MAGENTA}  [+] MACHINE LEARNING PHISHING DETECTION ENGINE v2.5
{Fore.LIGHTBLACK_EX}  [+] Author: Mohammed Peer Siddiqui | Sqrock IT Solutions Alpha 2
  [+] Standard: NIST SP 800-177 | MITRE ATT&CK T1566 | Scikit-Learn NLP
==============================================================================={Style.RESET_ALL}"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
MODELS_DIR = os.path.join(BASE_DIR, "models")
REPORTS_DIR = os.path.join(BASE_DIR, "evaluation_reports")
DATASET_PATH = os.path.join(DATASETS_DIR, "phishing_dataset_50.csv")
MODEL_PATH = os.path.join(MODELS_DIR, "phish_model.joblib")
JSON_REPORT = os.path.join(REPORTS_DIR, "ml_evaluation_report.json")
TXT_REPORT = os.path.join(REPORTS_DIR, "ml_evaluation_report.txt")

URGENCY_KEYWORDS = [
    "verify", "suspended", "immediately", "urgent", "action required", 
    "overdue", "closure", "password expires", "critical alert", "breach", 
    "unauthorized", "wire transfer", "claim prize", "subpoena"
]


def ensure_directories():
    """Ensure output directories exist."""
    os.makedirs(DATASETS_DIR, exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)


def load_dataset(csv_path=DATASET_PATH):
    """Loads labeled email dataset."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at {csv_path}")
    df = pd.read_csv(csv_path)
    return df


def build_pipeline():
    """Constructs CountVectorizer + Multinomial Naive Bayes pipeline (Syllabus Standard)."""
    return Pipeline([
        ('vec', CountVectorizer(ngram_range=(1, 2))),
        ('nb', MultinomialNB(alpha=0.1))
    ])


def train_and_evaluate(csv_path=DATASET_PATH, test_size=0.2, random_state=1):
    """
    Trains the ML model on labeled email dataset and computes
    confusion matrix, accuracy, precision, recall, and F1-score.
    """
    ensure_directories()
    df = load_dataset(csv_path)

    X = df["email_text"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    # Predictions
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    # Metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    # Save trained model
    joblib.dump(pipeline, MODEL_PATH)

    metrics = {
        "dataset_total_samples": len(df),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "accuracy": round(acc * 100, 2),
        "precision": round(prec * 100, 2),
        "recall": round(rec * 100, 2),
        "f1_score": round(f1 * 100, 2),
        "confusion_matrix": {
            "true_negatives": int(cm[0][0]),
            "false_positives": int(cm[0][1]),
            "false_negatives": int(cm[1][0]),
            "true_positives": int(cm[1][1])
        },
        "model_architecture": "TF-IDF (1-2 ngrams) + Multinomial Naive Bayes (alpha=0.1)"
    }

    # Save to JSON
    with open(JSON_REPORT, "w", encoding="utf-8") as jf:
        json.dump(metrics, jf, indent=2)

    # Save to TXT
    with open(TXT_REPORT, "w", encoding="utf-8") as tf:
        tf.write("===============================================================================\n")
        tf.write("       SQROCK IT SOLUTIONS - ML PHISHING DETECTOR EVALUATION REPORT            \n")
        tf.write("===============================================================================\n")
        tf.write(f"Total Dataset Samples : {metrics['dataset_total_samples']}\n")
        tf.write(f"Training Samples      : {metrics['train_samples']} | Testing: {metrics['test_samples']}\n")
        tf.write(f"Model Accuracy        : {metrics['accuracy']}%\n")
        tf.write(f"Precision             : {metrics['precision']}%\n")
        tf.write(f"Recall                : {metrics['recall']}%\n")
        tf.write(f"F1-Score              : {metrics['f1_score']}%\n")
        tf.write("Confusion Matrix:\n")
        tf.write(f"  [TN: {cm[0][0]:<3} | FP: {cm[0][1]:<3}]\n")
        tf.write(f"  [FN: {cm[1][0]:<3} | TP: {cm[1][1]:<3}]\n")
        tf.write("===============================================================================\n")

    return pipeline, metrics


def load_trained_model():
    """Loads existing trained model from disk or trains a new one."""
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    pipeline, _ = train_and_evaluate()
    return pipeline


def predict_email(email_text, model=None):
    """
    Classifies a single email string and returns predicted label,
    confidence probability, and identified urgency features.
    """
    if model is None:
        model = load_trained_model()

    pred = model.predict([email_text])[0]
    prob = model.predict_proba([email_text])[0]
    phish_prob = round(prob[1] * 100, 2)
    legit_prob = round(prob[0] * 100, 2)

    text_lower = email_text.lower()
    matched_urgency = [w for w in URGENCY_KEYWORDS if w in text_lower]

    return {
        "email_text": email_text,
        "prediction": "PHISHING" if pred == 1 else "LEGITIMATE",
        "label": int(pred),
        "phishing_confidence_pct": phish_prob,
        "legitimate_confidence_pct": legit_prob,
        "risk_tier": "CRITICAL" if phish_prob >= 80 else ("HIGH" if phish_prob >= 50 else "LOW"),
        "identified_urgency_tokens": matched_urgency
    }


def get_top_phishing_features(n=10):
    """Extracts top predictive phishing tokens from trained Naive Bayes log probabilities."""
    model = load_trained_model()
    vectorizer = model.named_steps['vec']
    nb = model.named_steps['nb']

    feature_names = np.array(vectorizer.get_feature_names_out())
    # Log probability of features given phishing class (class 1)
    phish_log_prob = nb.feature_log_prob_[1]
    top_indices = np.argsort(phish_log_prob)[-n:][::-1]

    top_features = []
    for idx in top_indices:
        top_features.append((feature_names[idx], round(float(phish_log_prob[idx]), 3)))
    return top_features


# ==============================================================================
# INTERACTIVE CLI PRESENTATION
# ==============================================================================

def print_menu():
    print(f"\n{Fore.LIGHTBLACK_EX}--- [ PEER'S ML PHISH DETECTOR CONTROL CONSOLE ] ---{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}[1]{Fore.WHITE} Train & Evaluate ML Model (Confusion Matrix & Accuracy Report)")
    print(f"  {Fore.CYAN}[2]{Fore.WHITE} Classify Custom Email Text (Single Inference with Probability)")
    print(f"  {Fore.CYAN}[3]{Fore.WHITE} Batch Predict Test Cohort (5 Diverse Validation Emails)")
    print(f"  {Fore.CYAN}[4]{Fore.WHITE} Inspect Most Discriminative Phishing N-Grams (NLP Explainability)")
    print(f"  {Fore.CYAN}[5]{Fore.WHITE} Export Model Artifacts & Evaluation Metrics (JSON / TXT)")
    print(f"  {Fore.CYAN}[6]{Fore.WHITE} Display Enterprise Email Gateway & NLP Blueprint")
    print(f"  {Fore.CYAN}[7]{Fore.RED} Exit Suite")


def interactive_cli():
    print(BANNER)
    ensure_directories()
    model = None

    while True:
        print_menu()
        choice = input(f"\n{Fore.GREEN}sqrock@phish-ml{Fore.WHITE}:{Fore.BLUE}~/classifier{Fore.WHITE}$ ").strip()

        if choice == "1":
            print(f"\n{Fore.YELLOW}[*] Training Naive Bayes NLP Classifier on {DATASET_PATH}...{Style.RESET_ALL}")
            model, metrics = train_and_evaluate()
            cm = metrics["confusion_matrix"]
            print(f"{Fore.GREEN}[+] Model Training & Validation Complete!{Style.RESET_ALL}")
            print(f"  • Architecture    : {metrics['model_architecture']}")
            print(f"  • Dataset Volume  : {metrics['dataset_total_samples']} Samples ({metrics['train_samples']} Train / {metrics['test_samples']} Test)")
            print(f"  • Accuracy        : {Fore.GREEN}{metrics['accuracy']}%{Style.RESET_ALL}")
            print(f"  • Precision       : {Fore.GREEN}{metrics['precision']}%{Style.RESET_ALL}")
            print(f"  • Recall          : {Fore.GREEN}{metrics['recall']}%{Style.RESET_ALL}")
            print(f"  • F1-Score        : {Fore.GREEN}{metrics['f1_score']}%{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}--- [ Confusion Matrix (2x2) ] ---{Style.RESET_ALL}")
            print(f"  True Negatives  (Legitimate Correct) : {Fore.GREEN}{cm['true_negatives']}{Style.RESET_ALL}")
            print(f"  False Positives (Legit flagged Phish): {Fore.RED}{cm['false_positives']}{Style.RESET_ALL}")
            print(f"  False Negatives (Phish slipped past) : {Fore.RED}{cm['false_negatives']}{Style.RESET_ALL}")
            print(f"  True Positives  (Phishing Correct)   : {Fore.GREEN}{cm['true_positives']}{Style.RESET_ALL}")

        elif choice == "2":
            print(f"\n{Fore.YELLOW}[*] Single Email Inference Engine:{Style.RESET_ALL}")
            sample = input("Enter Email Text to classify: ").strip()
            if not sample:
                sample = "URGENT: Your corporate payroll deposit failed. Click here to update banking details immediately."
                print(f"Using default sample: '{sample}'")
            res = predict_email(sample, model)
            col = Fore.RED if res["prediction"] == "PHISHING" else Fore.GREEN
            print(f"\n{Fore.GREEN}[+] Classification Result:{Style.RESET_ALL}")
            print(f"  • Verdict           : {col}{res['prediction']}{Style.RESET_ALL} ({res['risk_tier']} TIER)")
            print(f"  • Phishing Confidence: {res['phishing_confidence_pct']}%")
            print(f"  • Legit Confidence   : {res['legitimate_confidence_pct']}%")
            if res["identified_urgency_tokens"]:
                print(f"  • Urgency Tokens    : {Fore.YELLOW}{', '.join(res['identified_urgency_tokens'])}{Style.RESET_ALL}")

        elif choice == "3":
            cohort = [
                "Verify your Microsoft 365 credentials immediately to avoid suspension.",
                "Hey team, here are the meeting notes and action items from yesterday's sync.",
                "Urgent action required: Wire $25,000 to new vendor acquisition account.",
                "Attached is the monthly AWS cloud cost allocation invoice for Q3.",
                "Package delivery held at warehouse. Click here to confirm shipping address."
            ]
            print(f"\n{Fore.YELLOW}[*] Running Batch Inference across 5 Unlabeled Test Vectors:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'#':<3} {'Predicted':<12} {'Confidence':<12} {'Email Text Preview'}{Style.RESET_ALL}")
            print("-" * 88)
            for i, email in enumerate(cohort, 1):
                res = predict_email(email, model)
                col = Fore.RED if res["prediction"] == "PHISHING" else Fore.GREEN
                print(f"{i:<3} {col}{res['prediction']:<12}{Style.RESET_ALL} {res['phishing_confidence_pct']:<5}%      {email[:50]}...")
            print("-" * 88)

        elif choice == "4":
            print(f"\n{Fore.YELLOW}[*] Top 10 Most Discriminative Phishing N-Grams (Model Explainability):{Style.RESET_ALL}")
            top_tokens = get_top_phishing_features(10)
            for rank, (tok, score) in enumerate(top_tokens, 1):
                print(f"  {rank:>2}. {Fore.CYAN}{tok:<20}{Fore.WHITE} Log-Probability: {score}")

        elif choice == "5":
            _, metrics = train_and_evaluate()
            print(f"\n{Fore.GREEN}[+] Exported model evaluation reports to:{Style.RESET_ALL}")
            print(f"  • JSON Report : {JSON_REPORT}")
            print(f"  • TXT Briefing: {TXT_REPORT}")
            print(f"  • Model File  : {MODEL_PATH}")

        elif choice == "6":
            print(f"\n{Fore.CYAN}==============================================================================={Style.RESET_ALL}")
            print(f"{Fore.GREEN}        ENTERPRISE EMAIL GATEWAY & NLP DEFENSE BLUEPRINT                       {Style.RESET_ALL}")
            print(f"{Fore.CYAN}==============================================================================={Style.RESET_ALL}")
            print(f"""
{Fore.YELLOW}1. Multi-Stage Pipeline Integration:{Fore.WHITE}
   - Deploy ML text classifiers directly at the Secure Email Gateway (SEG) tier.
   - Combine NLP scoring with DMARC, DKIM, and SPF cryptographic sender verification.

{Fore.YELLOW}2. Feature Engineering & Signal Synthesis:{Fore.WHITE}
   - Correlate TF-IDF text features with sender domain age, URL entropy, and homoglyphs.
   - Analyze email headers for mismatching Display Name vs Envelope From addresses.

{Fore.YELLOW}3. Automated Quarantine & Feedback Loops:{Fore.WHITE}
   - Emails with Phishing Confidence >= 80% route directly to SOC Quarantine.
   - User-reported false positives and false negatives continuously retrain the model.
""")

        elif choice == "7":
            print(f"\n{Fore.CYAN}[+] Exiting PEER'S ML Phish Detector. Pipeline active.{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}[-] Invalid option. Please select 1 through 7.{Style.RESET_ALL}")


if __name__ == "__main__":
    interactive_cli()
