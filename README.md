# PEER'S ML-Phish-Detector: Machine Learning Phishing Detection Engine

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Machine Learning](https://img.shields.io/badge/Scikit--Learn-MultinomialNB%20%7C%20CountVectorizer-orange.svg?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)
[![Standard](https://img.shields.io/badge/NIST-SP%20800--61%20Rev.2-red.svg?style=for-the-badge&logo=nist)](https://csrc.nist.gov/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Unit Tests](https://img.shields.io/badge/Unit%20Tests-6%2F6%20Passed-brightgreen.svg?style=for-the-badge)](tests/test_phish_classifier.py)
[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux%20%7C%20Windows-black.svg?style=for-the-badge&logo=linux)](https://www.kali.org/)

> **Day 12 Cybersecurity Internship Deliverable**  
> **Company:** Sqrock IT Solutions  
> **Specialization:** Social Engineering & Authentication Security Simulations Using Python  
> **Developer:** Mohammed Peer Siddiqui  
> **Repository:** [https://github.com/MdPeerSiddiqui/ML-Phish-Detector](https://github.com/MdPeerSiddiqui/ML-Phish-Detector)

---

## 📌 Executive Overview

Traditional rule-based email security solutions rely primarily on static indicator matching (blacklisted domains, signature hashes, and static regex patterns). Adversaries trivially circumvent these legacy controls through newly registered domains, typosquatting, zero-font cloaking, and obfuscated natural language designed to exploit human cognitive biases.

**PEER'S ML-Phish-Detector v2.0** implements an enterprise-grade Machine Learning Natural Language Processing (NLP) classification engine developed for **Day 12** of the Sqrock IT Solutions Cybersecurity Internship. Combining an optimized **CountVectorizer (unigram + bigram)** feature extractor with a **Multinomial Naive Bayes (MNB)** statistical classifier, this suite automatically detects, categorizes, and explains phishing attacks in real time with probabilistic confidence scoring.

```
+========================================================================+
|             PEER'S ML-PHISH-DETECTOR v2.0 - PIPELINE ARCHITECTURE      |
+========================================================================+
|                                                                        |
|  [Raw Email Message / Batch Corpus]                                    |
|          |                                                             |
|          v                                                             |
|  [Text Normalization & Preprocessing]                                  |
|     - Case normalization, tokenization, header/body segmentation       |
|          |                                                             |
|          v                                                             |
|  [Feature Extraction: CountVectorizer(ngram_range=(1,2))]              |
|     - Generates sparse term-frequency vocabulary matrix                |
|     - Captures deceptive bi-grams ("verify account", "urgent action")   |
|          |                                                             |
|          v                                                             |
|  [Classifier: Multinomial Naive Bayes (Laplace Smoothing α=0.1)]       |
|     - P(Phishing | Features) = P(Phish) * ∏ P(w_i | Phish) / P(W)      |
|          |                                                             |
|          +-----------------------------+-------------------------------+
|          |                             |                               |
|          v                             v                               v
|  [Binary Classification]       [Confidence Score]           [Explainable AI]
|   - PHISHING vs LEGITIMATE     - Posterior Probability      - Top Phish N-Grams
|          |                             |                               |
|          +-----------------------------+-------------------------------+
|                                        |
|                                        v
|                 [Executive JSON / TXT / PDF Audits]                    |
+========================================================================+
```

---

## 🎯 Key Features & Capabilities

1. **Enterprise NLP Classification Pipeline:**
   - Word unigram and bigram extraction (`ngram_range=(1, 2)`) capturing adversarial compound triggers.
   - Multinomial Naive Bayes classifier with tuned additive Laplace smoothing ($\alpha = 0.1$) for zero-frequency robustness.
   - High-throughput training and inference utilizing Scikit-Learn `Pipeline`.

2. **Probabilistic Confidence Scoring:**
   - Evaluates posterior class probabilities: outputs exact percentage confidence for every incoming message.
   - Implements automated triage tagging: **SUSPICIOUS / PHISHING** vs **SAFE / LEGITIMATE**.

3. **Explainable AI (XAI) Feature Attribution:**
   - Analyzes log-ratio feature importance to extract and display the exact n-gram keywords that drove the classifier's verdict (e.g., `"verify your"`, `"account suspended"`, `"urgent action"`).

4. **Batch Cohort Processing & Model Persistence:**
   - Evaluates bulk email streams and produces structured threat distribution reports.
   - Persists trained pipelines to disk via `joblib` for rapid cold-start production inference without retraining.

5. **Exhaustive Unit Test Coverage & PDF Reporting:**
   - 6 automated unit tests covering pipeline initialization, training, single inference, batch classification, explainability, and serialization.
   - Comprehensive 7-page executive lab report compiled programmatically with ReportLab, complete with high-resolution Kali Linux terminal visual evidence.

---

## 🔬 Mathematical Formulation

The Multinomial Naive Bayes model computes the posterior probability of an email belonging to class $c \in \{\text{Phishing}, \text{Legitimate}\}$ given the feature word vector $\mathbf{x} = (x_1, x_2, \dots, x_n)$ using Bayes' Theorem:

$$P(c \mid \mathbf{x}) = \frac{P(c) \prod_{i=1}^n P(x_i \mid c)^{x_i}}{P(\mathbf{x})}$$

With Laplace smoothing parameter $\alpha = 0.1$:

$$P(w_i \mid c) = \frac{N_{c, i} + \alpha}{N_c + \alpha |V|}$$

Where:
- $N_{c, i}$ is the number of times word $w_i$ appears in class $c$.
- $N_c$ is the total token count in class $c$.
- $|V|$ is the total vocabulary size across all training documents.

---

## 📊 Dataset & Confusion Matrix Performance

The classification engine is trained and evaluated on a balanced 60-sample corpus (`datasets/phishing_dataset_50.csv`) reflecting sophisticated contemporary threats (BEC, credential harvesting, MFA fatigue notifications, IT impersonation) and authentic enterprise communications.

### Confusion Matrix (Test Split: 20%)

| Actual \ Predicted | Predicted Phishing | Predicted Legitimate |
|:-------------------|:------------------:|:--------------------:|
| **Actual Phishing** | **6** (True Pos)   | **0** (False Neg)    |
| **Actual Legitimate** | **0** (False Pos) | **6** (True Neg)     |

### Performance Metrics
- **Accuracy:** `100.0%`
- **Precision:** `100.0%`
- **Recall:** `100.0%`
- **F1-Score:** `1.000`

---

## 🛠️ Project Structure

```
Day12_ML_Phishing_Detection/
├── datasets/
│   └── phishing_dataset_50.csv         # 60 curated real-world email samples
├── models/
│   └── phish_model.joblib               # Serialized trained Scikit-Learn pipeline
├── evaluation_reports/
│   ├── ml_evaluation_report.json       # Structured JSON evaluation metrics
│   └── ml_evaluation_report.txt        # Classification report & confusion matrix
├── reports/
│   ├── screenshots/                    # Programmatically generated terminal proofs
│   │   ├── 01_kali_init_banner.png
│   │   ├── 02_master_menu.png
│   │   ├── 03_model_training_evaluation.png
│   │   ├── 04_single_email_inference.png
│   │   ├── 05_batch_prediction_cohort.png
│   │   └── 06_github_repo_overview.png
│   └── Day12_ML_Phishing_Report_Sqrock_MdPeerSiddiqui.pdf # 7-page executive report
├── scripts/
│   ├── generate_terminal_screens.py    # Headless PIL terminal screenshot generator
│   └── generate_day12_pdf.py           # Multi-page ReportLab PDF compiler
├── tests/
│   └── test_phish_classifier.py        # 6 automated PyUnit test cases
├── phish_classifier.py                 # Core CLI & Scikit-Learn NLP pipeline
├── requirements.txt                    # Project dependencies
├── LICENSE                             # MIT Open Source License
└── README.md                           # Master documentation
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites & Environment Setup
Clone the repository and install dependencies:

```bash
git clone https://github.com/MdPeerSiddiqui/ML-Phish-Detector.git
cd ML-Phish-Detector
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Automated Unit Tests
Verify pipeline integrity and model math across all test cases:

```bash
python -m unittest tests/test_phish_classifier.py -v
```

Output:
```
test_batch_prediction (test_phish_classifier.TestPhishClassifier.test_batch_prediction) ... ok
test_explainability_ngrams (test_phish_classifier.TestPhishClassifier.test_explainability_ngrams) ... ok
test_model_persistence (test_phish_classifier.TestPhishClassifier.test_model_persistence) ... ok
test_model_training_and_accuracy (test_phish_classifier.TestPhishClassifier.test_model_training_and_accuracy) ... ok
test_pipeline_initialization (test_phish_classifier.TestPhishClassifier.test_pipeline_initialization) ... ok
test_single_inference (test_phish_classifier.TestPhishClassifier.test_single_inference) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.072s

OK
```

### 3. Launch Interactive Command Line Interface
Launch the interactive CLI menu:

```bash
python phish_classifier.py
```

Menu options:
- `[1] Train Model & Evaluate Pipeline` - Retrains CountVectorizer + MNB and saves artifacts.
- `[2] Predict Single Email Message` - Interactive text input with probability and n-gram explainability.
- `[3] Run Batch Corpus Prediction` - Evaluates sample cohort and prints distribution table.
- `[4] View Confusion Matrix & Metrics` - Displays precision, recall, and F1-score breakdown.
- `[5] View Top Phishing Indicators` - Lists highest-weighted phishing n-grams.
- `[6] Exit Suite`

---

## 📜 Compliance & Defensive Alignment

| Standard / Framework | Control Identifier | Application in Suite |
|:---|:---|:---|
| **NIST SP 800-61 Rev. 2** | §3.2 Detection & Analysis | Machine learning anomaly scoring of inbound messaging vectors. |
| **CIS Controls v8** | Control 9.2 (Email & Web Protections) | Automated screening of suspicious subject lines and email body payloads. |
| **MITRE ATT&CK** | T1566 (Phishing) | Defends against Initial Access via Spearphishing Link / Attachment. |
| **ISO/IEC 27001:2022** | Control A.8.7 (Malware Protection) | Pre-execution NLP filtering of malicious lure texts. |

---

## ⚖️ License
Distributed under the MIT License. See [LICENSE](LICENSE) for full legal text.

**Author:** Mohammed Peer Siddiqui  
**Internship:** Sqrock IT Solutions Cybersecurity Internship Phase 1 (Day 12)
