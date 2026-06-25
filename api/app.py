from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Roman Urdu Threat Detector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model_name = os.getenv("MODEL_NAME", "paraphrase-multilingual-MiniLM-L12-v2")
embedder = None
classifier = None

@app.on_event("startup")
async def load_models():
    global embedder, classifier
    try:
        embedder = SentenceTransformer(model_name)
        with open("models/finetuned_bert/classifier.pkl", "rb") as f:
            classifier = pickle.load(f)
    except Exception as e:
        print(f"Warning: Models not loaded. {e}")

class PredictRequest(BaseModel):
    text: str

@app.post("/predict")
async def predict(req: PredictRequest):
    if embedder is None or classifier is None:
        return {"error": "Models not loaded"}
        
    emb = embedder.encode([req.text])
    pred = classifier.predict(emb)[0]
    prob = classifier.predict_proba(emb)[0][1]
    
    return {
        "prediction": "scam" if pred == 1 else "legitimate",
        "confidence": float(prob if pred == 1 else 1 - prob)
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
