import pandas as pd
from sklearn.model_selection import train_test_split
import os

def load_and_split_data():
    raw_path = "data/raw/scam_messages.csv"
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Dataset not found at {raw_path}")
        
    df = pd.read_csv(raw_path)
    
    # Basic cleaning
    df['text'] = df['text'].str.lower()
    df['text'] = df['text'].str.strip()
    df['text'] = df['text'].str.replace(r'\s+', ' ', regex=True)
    
    # Drop empty rows
    df = df.dropna(subset=['text', 'label'])
    
    # Train val test split
    X = df['text']
    y = df['label']
    
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)
    
    print("\n--- Dataset Distribution ---")
    print(f"Total rows: {len(df)}")
    print(f"Scam (1): {len(df[df['label'] == 1])}")
    print(f"Legitimate (0): {len(df[df['label'] == 0])}")
    print(f"\nSplits - Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
    
    # Save splits
    os.makedirs("data/splits", exist_ok=True)
    
    train_df = pd.DataFrame({'text': X_train, 'label': y_train})
    val_df = pd.DataFrame({'text': X_val, 'label': y_val})
    test_df = pd.DataFrame({'text': X_test, 'label': y_test})
    
    train_df.to_csv("data/splits/train.csv", index=False)
    val_df.to_csv("data/splits/val.csv", index=False)
    test_df.to_csv("data/splits/test.csv", index=False)
    
    return train_df, val_df, test_df

if __name__ == "__main__":
    load_and_split_data()
