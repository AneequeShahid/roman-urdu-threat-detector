import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve

def evaluate_models():
    os.makedirs("results/figures", exist_ok=True)
    
    with open("results/metrics/baseline_metrics.json", "r") as f:
        baselines = json.load(f)
        
    with open("results/metrics/bert_metrics.json", "r") as f:
        bert = json.load(f)
        
    all_metrics = {**baselines, **bert}
    
    # Save combined
    with open("results/metrics/metrics.json", "w") as f:
        json.dump(all_metrics, f, indent=4)
        
    df = pd.DataFrame(all_metrics).T
    print("\n--- Model Comparison ---")
    print(df[['accuracy', 'f1', 'roc_auc']])
    
    # 1. Bar Chart
    df[['accuracy', 'f1']].plot(kind='bar', figsize=(10, 6))
    plt.title('Accuracy and F1 Score Comparison')
    plt.ylabel('Score')
    plt.tight_layout()
    plt.savefig('results/figures/metrics_comparison.png', dpi=300)
    plt.close()
    
    # 2. Confusion Matrices
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    for idx, (name, metrics) in enumerate(all_metrics.items()):
        if idx < 4:
            cm = np.array(metrics['confusion_matrix'])
            sns.heatmap(cm, annot=True, fmt='d', ax=axes[idx], cmap='Blues')
            axes[idx].set_title(f'{name} Confusion Matrix')
    plt.tight_layout()
    plt.savefig('results/figures/confusion_matrices.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    evaluate_models()
