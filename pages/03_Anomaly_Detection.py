"""
pages/03_Anomaly_Detection.py
Cost Anomaly Detection page for NeuroCore AI.
"""

import sys
import os
import streamlit as st
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data.generate_data import generate_cost_data
from models.anomaly_detection import detect_cost_anomalies
from utils.visualization import anomaly_chart

st.set_page_config(page_title="Anomaly Detection · NeuroCore AI", page_icon="⚠️", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    section[data-testid="stSidebar"] { background-color: #161b22; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("# ⚠️ Cost Anomaly Detection")
st.markdown("Isolation Forest model to identify unusual cost spikes in operational data.")
st.divider()

with st.sidebar:
    st.markdown("## ⚙️ Detection Settings")
    contamination = st.slider("Expected Anomaly Rate", 0.02, 0.20, 0.08, step=0.01)
    periods = st.slider("Data Points (days)", 60, 365, 180)
    st.divider()
    detect_btn = st.button("🔍 Detect Anomalies", use_container_width=True, type="primary")

# ── Load data & detect ────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_costs(p: int) -> pd.DataFrame:
    return generate_cost_data(periods=p)


if detect_btn or "anomaly_result" not in st.session_state:
    cost_df = load_costs(periods)
    with st.spinner("Running Isolation Forest…"):
        try:
            result_df, _, _ = detect_cost_anomalies(
                cost_df,
                feature_cols=["operational_cost", "marketing_cost", "hr_cost"],
                contamination=contamination,
            )
            st.session_state["anomaly_result"] = result_df
        except Exception as exc:
            st.error(f"Detection failed: {exc}")
            st.stop()

result_df = st.session_state.get("anomaly_result")

if result_df is not None:
    anomaly_count = result_df["is_anomaly"].sum()
    normal_count = (~result_df["is_anomaly"]).sum()

    # ── KPIs ─────────────────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", f"{len(result_df):,}")
    col2.metric("Anomalies Detected", f"{anomaly_count}")
    col3.metric("Normal Records", f"{normal_count:,}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chart ────────────────────────────────────────────────────────────────────
    fig = anomaly_chart(result_df)
    st.plotly_chart(fig, use_container_width=True)

    # ── Anomaly table ─────────────────────────────────────────────────────────────
    st.markdown("### 🚨 Flagged Anomalies")
    anomalies = result_df[result_df["is_anomaly"]].copy()
    anomalies["date"] = anomalies["date"].astype(str)
    for col in ["operational_cost", "marketing_cost", "hr_cost", "total_cost"]:
        anomalies[col] = anomalies[col].apply(lambda v: f"${v:,.0f}")
    st.dataframe(anomalies.drop(columns=["is_anomaly"]).reset_index(drop=True), use_container_width=True)
