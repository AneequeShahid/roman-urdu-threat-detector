import pandas as pd
import numpy as np
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "paraphrase-multilingual-MiniLM-L12-v2")

def extract_features():
    train_df = pd.read_csv("data/augmented/augmented_train.csv")
    val_df = pd.read_csv("data/splits/val.csv")
    test_df = pd.read_csv("data/splits/test.csv")
    
    print("Extracting TF-IDF Features...")
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), analyzer='char_wb')
    
    X_train_tfidf = vectorizer.fit_transform(train_df['text'])
    X_val_tfidf = vectorizer.transform(val_df['text'])
    X_test_tfidf = vectorizer.transform(test_df['text'])
    
    os.makedirs("models", exist_ok=True)
    with open("models/tfidf_vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
        
    with open("data/splits/tfidf_features.pkl", "wb") as f:
        pickle.dump((X_train_tfidf, X_val_tfidf, X_test_tfidf, train_df['label'], val_df['label'], test_df['label']), f)
        
    print(f"Extracting mBERT Embeddings using {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)
    
    X_train_emb = model.encode(train_df['text'].tolist(), show_progress_bar=True)
    X_val_emb = model.encode(val_df['text'].tolist(), show_progress_bar=True)
    X_test_emb = model.encode(test_df['text'].tolist(), show_progress_bar=True)
    
    np.save("data/splits/X_train_emb.npy", X_train_emb)
    np.save("data/splits/X_val_emb.npy", X_val_emb)
    np.save("data/splits/X_test_emb.npy", X_test_emb)
    
    print("Feature extraction complete.")

if __name__ == "__main__":
    extract_features()
