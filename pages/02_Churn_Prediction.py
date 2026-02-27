"""
pages/02_Churn_Prediction.py
Customer Churn Prediction page for NeuroCore AI.
"""

import sys
import os
import streamlit as st
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data.generate_data import generate_churn_data
from models.churn_prediction import train_churn_model
from utils.visualization import confusion_matrix_chart, feature_importance_chart

st.set_page_config(page_title="Churn Prediction · NeuroCore AI", page_icon="🔁", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    section[data-testid="stSidebar"] { background-color: #161b22; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("# 🔁 Customer Churn Prediction")
st.markdown("Random Forest classifier trained on synthetic customer data.")
st.divider()

with st.sidebar:
    st.markdown("## ⚙️ Model Settings")
    n_samples = st.slider("Training Samples", 500, 5000, 2000, step=500)
    st.divider()
    train_btn = st.button("🚀 Train Model", use_container_width=True, type="primary")

# ── Load & train ─────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_churn(n: int) -> pd.DataFrame:
    return generate_churn_data(n_samples=n)


if train_btn or "churn_result" not in st.session_state:
    df = load_churn(n_samples)
    with st.spinner("Training Random Forest…"):
        try:
            model, metrics = train_churn_model(df, model_path="/tmp/churn_model.pkl")
            st.session_state["churn_result"] = metrics
            st.session_state["churn_data"] = df
        except Exception as exc:
            st.error(f"Training failed: {exc}")
            st.stop()

metrics = st.session_state.get("churn_result")
df = st.session_state.get("churn_data")

if metrics:
    # ── Metrics ─────────────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("ROC-AUC", f"{metrics['roc_auc']:.4f}")
    col2.metric("Precision", f"{metrics['precision']:.4f}")
    col3.metric("Recall", f"{metrics['recall']:.4f}")
    col4.metric("F1 Score", f"{metrics['f1']:.4f}")

    st.markdown("<br>", unsafe_allow_html=True)

    col_cm, col_fi = st.columns(2)

    with col_cm:
        fig_cm = confusion_matrix_chart(metrics["confusion_matrix"])
        st.plotly_chart(fig_cm, use_container_width=True)

    with col_fi:
        fig_fi = feature_importance_chart(metrics["feature_importances"])
        st.plotly_chart(fig_fi, use_container_width=True)

    # ── Dataset preview ──────────────────────────────────────────────────────────
    st.markdown("### 📋 Dataset Sample")
    st.dataframe(df.head(20), use_container_width=True)
