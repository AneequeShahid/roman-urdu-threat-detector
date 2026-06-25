import streamlit as st
import requests
import json
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Roman Urdu Threat Detector", layout="wide")

st.title("Roman Urdu Threat Detector")
st.write("Detecting scams and phishing attempts in Roman Urdu and code-switched text.")

tab1, tab2, tab3 = st.tabs(["Live Detector", "Model Comparison", "Dataset Explorer"])

with tab1:
    st.header("Live Detection")
    text_input = st.text_area("Paste a message here (Roman Urdu / English):")
    if st.button("Predict"):
        if text_input:
            try:
                res = requests.post("http://localhost:8000/predict", json={"text": text_input})
                if res.status_code == 200:
                    data = res.json()
                    pred = data["prediction"]
                    conf = data["confidence"]
                    if pred == "scam":
                        st.error(f"⚠️ SCAM DETECTED (Confidence: {conf*100:.2f}%)")
                    else:
                        st.success(f"✅ LEGITIMATE (Confidence: {conf*100:.2f}%)")
                else:
                    st.warning("API error")
            except:
                st.warning("Ensure the FastAPI backend is running on port 8000.")

with tab2:
    st.header("Model Evaluation")
    metrics_file = "results/metrics/metrics.json"
    if os.path.exists(metrics_file):
        with open(metrics_file) as f:
            metrics = json.load(f)
        df = pd.DataFrame(metrics).T
        st.dataframe(df[['accuracy', 'f1', 'roc_auc']])
        
        img_path = "results/figures/metrics_comparison.png"
        if os.path.exists(img_path):
            st.image(img_path)
            
        cm_path = "results/figures/confusion_matrices.png"
        if os.path.exists(cm_path):
            st.image(cm_path)
    else:
        st.write("Run the experiment pipeline first to generate metrics.")

with tab3:
    st.header("Dataset Overview")
    data_path = "data/raw/scam_messages.csv"
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        st.write(f"Total Raw Messages: {len(df)}")
        st.dataframe(df.sample(min(20, len(df))))
    else:
        st.write("Raw data not found.")
