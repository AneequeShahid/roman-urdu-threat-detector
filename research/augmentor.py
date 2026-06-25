import pandas as pd
import random
import os

SYNONYMS = {
    "account": ["ac", "acount", "khata"],
    "password": ["pwd", "pass", "code", "pin"],
    "update": ["change", "modify", "verify", "theek"],
    "urgent": ["fori", "jaldi", "lazmi"],
    "winner": ["jeetne", "jeeta", "lucky"],
    "lucky draw": ["inaam", "lottery"],
    "money": ["paisa", "rupay", "cash"]
}

SCAM_PHRASES = [
    "abhi call karein",
    "link par click karein",
    "urgent reply karein",
    "kisi ko mat batana"
]

def augment_message(text):
    words = text.split()
    # Synonym replacement
    for i, word in enumerate(words):
        for k, v in SYNONYMS.items():
            if k in word.lower():
                if random.random() > 0.5:
                    words[i] = random.choice(v)
    
    # Random insertion
    if random.random() > 0.5:
        words.append(random.choice(SCAM_PHRASES))
        
    return " ".join(words)

def run_augmentation():
    train_path = "data/splits/train.csv"
    if not os.path.exists(train_path):
        raise FileNotFoundError(f"Training split not found at {train_path}")
        
    df = pd.read_csv(train_path)
    scam_df = df[df['label'] == 1]
    
    print(f"Original scam samples in train: {len(scam_df)}")
    
    augmented_rows = []
    # Generate 300 synthetic examples
    for _ in range(300):
        sample = scam_df.sample(n=1).iloc[0]
        aug_text = augment_message(sample['text'])
        augmented_rows.append({"text": aug_text, "label": 1})
        
    aug_df = pd.DataFrame(augmented_rows)
    
    # Combine
    final_df = pd.concat([df, aug_df]).sample(frac=1, random_state=42).reset_index(drop=True)
    
    os.makedirs("data/augmented", exist_ok=True)
    final_df.to_csv("data/augmented/augmented_train.csv", index=False)
    
    print(f"Augmented scam samples added: 300")
    print(f"Total training samples now: {len(final_df)}")
    
    return final_df

if __name__ == "__main__":
    run_augmentation()
