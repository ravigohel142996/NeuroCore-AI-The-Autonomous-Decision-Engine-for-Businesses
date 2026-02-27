"""
pages/01_Revenue_Forecast.py
Revenue Forecast page for NeuroCore AI.
"""

import sys
import os
import streamlit as st
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data.generate_data import generate_revenue_data
from models.revenue_forecast import run_revenue_forecast
from utils.visualization import revenue_forecast_chart
from utils.theme import inject_css, section_header

st.set_page_config(page_title="Revenue Forecast · NeuroCore AI", page_icon="📈", layout="wide")
inject_css()

st.markdown("# 📈 Revenue Forecast")
st.markdown(
    '<p style="color:#C9D1D9;">Prophet-based 6-month revenue projection with confidence intervals.</p>',
    unsafe_allow_html=True,
)
st.divider()

# ── Controls ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Forecast Settings")
    forecast_periods = st.slider("Forecast Horizon (months)", 3, 12, 6)
    data_periods = st.slider("Historical Data (months)", 24, 60, 36)
    st.divider()
    run_btn = st.button("🚀 Run Forecast", use_container_width=True, type="primary")

# ── Load data ────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_revenue(periods: int) -> pd.DataFrame:
    return generate_revenue_data(periods=periods)


df = load_revenue(data_periods)

# ── Run forecast ─────────────────────────────────────────────────────────────────
if run_btn or "forecast_result" not in st.session_state:
    with st.spinner("Training Prophet model..."):
        try:
            forecast_df, metrics = run_revenue_forecast(df, forecast_periods)
            st.session_state["forecast_result"] = (forecast_df, metrics)
        except Exception as exc:
            st.error(f"Forecast failed: {exc}")
            st.stop()

forecast_df, metrics = st.session_state.get("forecast_result", (None, None))

if forecast_df is not None:
    # ── Metrics ─────────────────────────────────────────────────────────────────
    section_header("Forecast Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Last Actual Revenue", f"${metrics['last_actual_revenue']:,.0f}")
    col2.metric("Next Month Forecast", f"${metrics['next_month_forecast']:,.0f}")
    col3.metric("Forecast MAPE", f"{metrics['mape']:.2f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chart ────────────────────────────────────────────────────────────────────
    section_header("Revenue Forecast Chart")
    fig = revenue_forecast_chart(df, forecast_df, title="Revenue Forecast (6-Month Projection)")
    st.plotly_chart(fig, use_container_width=True)

    # ── Forecast table ────────────────────────────────────────────────────────────
    section_header("Forecast Detail")
    future = forecast_df[forecast_df["ds"] > df["ds"].max()][
        ["ds", "yhat", "yhat_lower", "yhat_upper"]
    ].copy()
    future.columns = ["Date", "Forecast", "Lower Bound", "Upper Bound"]
    future["Date"] = future["Date"].dt.strftime("%Y-%m")
    for col in ["Forecast", "Lower Bound", "Upper Bound"]:
        future[col] = future[col].apply(lambda v: f"${v:,.0f}")
    st.dataframe(future.reset_index(drop=True), use_container_width=True)
