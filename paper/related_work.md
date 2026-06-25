# Related Work

Phishing and spam detection have been extensively researched within the context of the English language. Techniques ranging from classical TF-IDF pipelines to modern transformer-based architectures (e.g., BERT, RoBERTa) have achieved near-perfect accuracy on English SMS Spam datasets.

However, research into Urdu NLP—and specifically Roman Urdu—remains significantly underdeveloped. While some prior works have explored sentiment analysis and generic text classification for Roman Urdu, the domain of cybersecurity threat detection remains largely unexplored. Code-switching (the fluid mixing of Urdu grammar with English vocabulary, represented in Latin script) introduces unique morphological and syntactic challenges that standard English NLP models fail to generalize against. 

Currently, there is a distinct gap in the literature regarding publicly available datasets and tailored models for phishing detection in Roman Urdu. This research addresses this gap by introducing the first labeled dataset for this task and evaluating the zero-shot multilingual capabilities of mBERT architectures against classical code-switched baselines.
