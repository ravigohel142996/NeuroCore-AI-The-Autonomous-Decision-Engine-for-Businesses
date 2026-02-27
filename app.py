"""
app.py
NeuroCore AI – Autonomous Business Decision Engine
Executive Dashboard (main entry point).
"""

import streamlit as st
import pandas as pd
import sys
import os

# Allow imports from project root
sys.path.insert(0, os.path.dirname(__file__))

from data.generate_data import generate_revenue_data, generate_churn_data, generate_cost_data
from utils.insights import generate_executive_insights
from utils.visualization import risk_gauge

# ── Page configuration ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeuroCore AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Dark theme overrides ─────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Main background */
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #161b22; }
    /* KPI card style */
    .kpi-card {
        background: linear-gradient(135deg, #1f2937, #111827);
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
    }
    .kpi-title { font-size: 0.85rem; color: #9ca3af; letter-spacing: 0.05em; text-transform: uppercase; }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #f9fafb; margin: 6px 0; }
    .kpi-delta-pos { color: #34d399; font-size: 0.9rem; }
    .kpi-delta-neg { color: #f87171; font-size: 0.9rem; }
    /* Section header */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #7c3aed;
        border-left: 4px solid #7c3aed;
        padding-left: 10px;
        margin: 18px 0 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://img.icons8.com/fluency/96/artificial-intelligence.png",
        width=64,
    )
    st.markdown("## 🧠 NeuroCore AI")
    st.markdown("**Autonomous Business Decision Engine**")
    st.divider()
    st.markdown("### Navigation")
    st.page_link("app.py", label="📊 Executive Dashboard", icon="🏠")
    st.page_link("pages/01_Revenue_Forecast.py", label="📈 Revenue Forecast")
    st.page_link("pages/02_Churn_Prediction.py", label="🔁 Churn Prediction")
    st.page_link("pages/03_Anomaly_Detection.py", label="⚠️ Anomaly Detection")
    st.page_link("pages/04_Strategy_Simulator.py", label="🧩 Strategy Simulator")
    st.page_link("pages/05_Optimization.py", label="💰 Profit Optimization")
    st.divider()
    st.caption("v1.0.0 · Enterprise Edition")

# ── Page header ──────────────────────────────────────────────────────────────────
st.markdown("# 🧠 NeuroCore AI")
st.markdown("### Autonomous Business Decision Engine — Executive Dashboard")
st.divider()

# ── Load synthetic data ───────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    revenue_df = generate_revenue_data()
    churn_df = generate_churn_data()
    cost_df = generate_cost_data()
    return revenue_df, churn_df, cost_df


revenue_df, churn_df, cost_df = load_data()

# ── KPI derivation ────────────────────────────────────────────────────────────────
last_revenue = revenue_df["y"].iloc[-1]
prev_revenue = revenue_df["y"].iloc[-2]
revenue_delta_pct = (last_revenue - prev_revenue) / prev_revenue * 100

churn_rate = churn_df["churn"].mean()
total_customers = len(churn_df)
churned = churn_df["churn"].sum()

avg_monthly_cost = cost_df["total_cost"].mean()
cost_std = cost_df["total_cost"].std()

revenue_trend = "up" if revenue_delta_pct > 1 else ("down" if revenue_delta_pct < -1 else "stable")

# ── KPI Cards ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    delta_class = "kpi-delta-pos" if revenue_delta_pct >= 0 else "kpi-delta-neg"
    delta_symbol = "▲" if revenue_delta_pct >= 0 else "▼"
    st.markdown(
        f"""<div class="kpi-card">
            <div class="kpi-title">Monthly Revenue</div>
            <div class="kpi-value">${last_revenue/1e6:.2f}M</div>
            <div class="{delta_class}">{delta_symbol} {abs(revenue_delta_pct):.1f}% MoM</div>
        </div>""",
        unsafe_allow_html=True,
    )

with col2:
    churn_class = "kpi-delta-neg" if churn_rate > 0.15 else "kpi-delta-pos"
    st.markdown(
        f"""<div class="kpi-card">
            <div class="kpi-title">Churn Rate</div>
            <div class="kpi-value">{churn_rate:.1%}</div>
            <div class="{churn_class}">{churned:,} of {total_customers:,} customers</div>
        </div>""",
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""<div class="kpi-card">
            <div class="kpi-title">Avg Monthly Cost</div>
            <div class="kpi-value">${avg_monthly_cost/1e3:.1f}K</div>
            <div class="kpi-delta-pos">σ = ${cost_std/1e3:.1f}K</div>
        </div>""",
        unsafe_allow_html=True,
    )

with col4:
    profit = last_revenue - avg_monthly_cost
    profit_class = "kpi-delta-pos" if profit > 0 else "kpi-delta-neg"
    st.markdown(
        f"""<div class="kpi-card">
            <div class="kpi-title">Est. Monthly Profit</div>
            <div class="kpi-value">${profit/1e3:.1f}K</div>
            <div class="{profit_class}">Revenue – Avg Cost</div>
        </div>""",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Revenue trend sparkline ────────────────────────────────────────────────────────
import plotly.graph_objects as go

st.markdown('<div class="section-header">Revenue Trend (Last 36 Months)</div>', unsafe_allow_html=True)
fig_trend = go.Figure()
fig_trend.add_trace(
    go.Scatter(
        x=revenue_df["ds"],
        y=revenue_df["y"],
        fill="tozeroy",
        fillcolor="rgba(99, 102, 241, 0.15)",
        line=dict(color="#6366f1", width=2),
        name="Revenue",
    )
)
fig_trend.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font=dict(color="#e0e0e0"),
    height=250,
    margin=dict(l=40, r=20, t=20, b=40),
    showlegend=False,
    xaxis_title="Date",
    yaxis_title="Revenue (USD)",
)
st.plotly_chart(fig_trend, use_container_width=True)

# ── Risk Gauge & Insights ─────────────────────────────────────────────────────────
col_gauge, col_insights = st.columns([1, 2])

with col_gauge:
    st.markdown('<div class="section-header">Business Risk Score</div>', unsafe_allow_html=True)
    risk_score = min(100, churn_rate * 100 * 0.5 + (cost_std / avg_monthly_cost) * 50)
    fig_risk = risk_gauge(risk_score)
    st.plotly_chart(fig_risk, use_container_width=True)

with col_insights:
    st.markdown('<div class="section-header">Executive AI Insights</div>', unsafe_allow_html=True)
    anomaly_count = int(len(cost_df) * 0.08)  # approximate 8% contamination
    insights_result = generate_executive_insights(
        revenue_trend=revenue_trend,
        churn_rate=churn_rate,
        anomaly_count=anomaly_count,
        risk_score=risk_score,
    )
    st.info(insights_result["executive_summary"])

    if insights_result["action_items"]:
        st.markdown("**📋 Recommended Actions:**")
        for item in insights_result["action_items"]:
            st.markdown(f"- {item}")

st.divider()
st.caption("NeuroCore AI · Powered by Prophet, Scikit-learn & SciPy · Enterprise Edition")
