import pickle
import os
import mlflow
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from tqdm import tqdm

def train_baselines():
    with open("data/splits/tfidf_features.pkl", "rb") as f:
        X_train, X_val, X_test, y_train, y_val, y_test = pickle.load(f)
        
    y_train = np.array(y_train).copy()
    y_test = np.array(y_test).copy()
        
    models = {
        "SVM": SVC(probability=True, random_state=42),
        "RandomForest": RandomForestClassifier(random_state=42),
        "LogisticRegression": LogisticRegression(random_state=42)
    }
    
    mlflow.set_experiment("roman-urdu-threat-detection")
    
    best_model = None
    best_f1 = 0
    metrics_dict = {}
    
    for name, model in tqdm(models.items(), desc="Training Baselines"):
        with mlflow.start_run(run_name=f"Baseline_{name}", nested=True):
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            probs = model.predict_proba(X_test)[:, 1]
            
            acc = accuracy_score(y_test, preds)
            prec = precision_score(y_test, preds)
            rec = recall_score(y_test, preds)
            f1 = f1_score(y_test, preds)
            roc = roc_auc_score(y_test, probs)
            cm = confusion_matrix(y_test, preds)
            
            mlflow.log_metrics({
                "accuracy": acc,
                "precision": prec,
                "recall": rec,
                "f1": f1,
                "roc_auc": roc
            })
            
            metrics_dict[name] = {
                "accuracy": acc,
                "precision": prec,
                "recall": rec,
                "f1": f1,
                "roc_auc": roc,
                "confusion_matrix": cm.tolist()
            }
            
            if f1 > best_f1:
                best_f1 = f1
                best_model = model
                
            with open(f"models/{name}.pkl", "wb") as f:
                pickle.dump(model, f)
                
    with open("models/best_baseline.pkl", "wb") as f:
        pickle.dump(best_model, f)
        
    import json
    os.makedirs("results/metrics", exist_ok=True)
    with open("results/metrics/baseline_metrics.json", "w") as f:
        json.dump(metrics_dict, f, indent=4)
        
    print(f"Baseline training complete. Best F1: {best_f1:.4f}")

if __name__ == "__main__":
    train_baselines()
