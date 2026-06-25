from research import dataset, augmentor, features, baseline_models, bert_model, evaluator
import os

def run_experiment():
    print("=" * 50)
    print("Starting Roman Urdu Threat Detector Pipeline")
    print("=" * 50)
    
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
    
    print("\n[Step 1/6] Loading and Splitting Data...")
    dataset.load_and_split_data()
    
    print("\n[Step 2/6] Augmenting Data...")
    augmentor.run_augmentation()
    
    print("\n[Step 3/6] Extracting Features...")
    features.extract_features()
    
    print("\n[Step 4/6] Training Baseline Models...")
    baseline_models.train_baselines()
    
    print("\n[Step 5/6] Fine-tuning mBERT...")
    bert_model.train_bert()
    
    print("\n[Step 6/6] Evaluating Models...")
    evaluator.evaluate_models()
    
    print("\nPipeline Complete! Results saved to results/ directory.")

if __name__ == "__main__":
    run_experiment()
