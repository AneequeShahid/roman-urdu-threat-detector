# Methodology

## Dataset Collection and Statistics
We generated a dataset of 200 synthetic Roman Urdu messages mimicking real-world text from Pakistani SMS and WhatsApp conversations. The dataset is perfectly balanced with 100 scam/phishing messages and 100 legitimate messages. Categories of scams include prize/lottery scams, bank fraud, job scams, impersonation, fake investments, and OTP theft. Legitimate examples reflect normal conversational topics, greetings, and queries.

## Annotation Guidelines
Messages were strictly labeled:
- `1` (Scam/Phishing): If the message exhibited malicious intent, requested sensitive information (OTP, PIN), directed to unverified links, or falsely promised monetary rewards.
- `0` (Legitimate): If the message represented routine conversation without deceptive intent.

## Augmentation Techniques
To address data scarcity and improve model generalization, we applied two specific data augmentation techniques:
1. **Synonym Replacement**: Replaced common code-switched English words (e.g., 'password', 'urgent', 'account') with their Roman Urdu or alternative English equivalents (e.g., 'code', 'fori', 'khata') based on a predefined dictionary.
2. **Random Insertion**: Injected common scam trigger phrases (e.g., 'abhi call karein', 'urgent reply karein') randomly into existing scam messages.
Through these techniques, the dataset was augmented to yield over 500 total messages.

## Model Architectures
- **Baseline Models**: We utilized TF-IDF vectorization (max features: 5000, n-gram range: 1-2, char_wb analyzer) followed by classical machine learning classifiers: Support Vector Machine (SVM), Random Forest (RF), and Logistic Regression (LR).
- **Deep Learning Model (mBERT)**: We leveraged `paraphrase-multilingual-MiniLM-L12-v2` via the sentence-transformers library to generate contextual embeddings of the Roman Urdu text. A Multi-Layer Perceptron (MLP) classification head was trained atop these embeddings to provide the final prediction.

## Evaluation Metrics
We evaluated all models across Accuracy, Precision, Recall, F1 Score, and ROC-AUC. Confusion matrices were generated to assess the False Positive and False Negative rates.

## Experimental Setup
The data was split temporally/stratified into 70% Train, 15% Validation, and 15% Test sets. All classical models and the mBERT classification head were tracked using MLflow. A fixed random state of 42 was maintained across all phases for absolute reproducibility.
