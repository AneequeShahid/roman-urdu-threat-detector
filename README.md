# Roman Urdu Threat Detector

## Research Question & Contribution
**Research Question:** "Can transformer-based models detect phishing and scam messages written in Roman Urdu and code-switched Roman Urdu/English text, and how do they compare against classical ML baselines?"

**Contribution:** 
1. First labeled Roman Urdu phishing/scam SMS dataset.
2. Benchmark comparison of mBERT (`paraphrase-multilingual-MiniLM-L12-v2`) vs classical ML on this specific task.
3. Publicly released dataset for the broader research community.

## Why Roman Urdu?
Roman Urdu (Urdu written in Latin script) is the primary mode of digital communication for millions of people in Pakistan and the diaspora across WhatsApp, SMS, and social media. Threat detection systems are overwhelmingly trained on English data and often fail completely against code-switched Roman Urdu text. This creates a massive vulnerability where scammers exploit the linguistic gap to target victims with fraudulent prize schemes, bank impersonations, and OTP theft.

## ASCII Architecture

```
Raw Messages → Cleaning → Augmentation
                              ↓
                  TF-IDF → Classical ML (SVM, RF, LR)
                  mBERT Embeddings → Fine-tuned BERT
                              ↓
                  Comparison → Paper Results → IEEE Access
```

## Dataset Statistics
- Target: Scam/Phishing (1) vs Legitimate (0)
- Original Dataset: 200 manually curated Roman Urdu messages
- Augmented Dataset: Expanded to 500+ messages using synonym replacement and random insertion
- Classes: Perfectly balanced

## Installation and Execution

1. Clone the repository and install requirements:
```bash
git clone https://github.com/AneequeShahid/roman-urdu-threat-detector.git
cd roman-urdu-threat-detector
pip install -r requirements.txt
```

2. Run the Full Experiment Pipeline:
```bash
python main.py
```
*Note: This will download the `paraphrase-multilingual-MiniLM-L12-v2` model from HuggingFace automatically on first run.*

3. Start the Live Detector UI:
```bash
uvicorn api.app:app --reload &
streamlit run ui/app.py
```

## How to Add Your Own Messages
To contribute to the dataset, simply append new messages to `data/raw/scam_messages.csv` following the format: `text,label` where `1` is a scam and `0` is legitimate. Re-run `main.py` to automatically update all features and models.

## Target Publication
This repository and its findings are prepared for submission to **IEEE Access**.
