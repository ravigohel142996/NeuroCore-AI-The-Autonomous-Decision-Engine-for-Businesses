"""
pages/05_Optimization.py
Profit Optimization page for NeuroCore AI using scipy.optimize.
"""

import sys
import os
import streamlit as st
import plotly.graph_objects as go

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.optimization import optimize_profit
from utils.visualization import risk_gauge

st.set_page_config(page_title="Profit Optimization · NeuroCore AI", page_icon="💰", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    section[data-testid="stSidebar"] { background-color: #161b22; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("# 💰 Profit Optimization")
st.markdown(
    "SciPy SLSQP optimizer finds the optimal marketing spend, pricing, and hiring mix "
    "to maximize profit within your budget and risk constraints."
)
st.divider()

# ── Inputs ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📥 Optimization Parameters")
    base_revenue = st.number_input("Base Annual Revenue ($)", value=10_000_000, step=500_000)
    base_cost = st.number_input("Base Annual Cost ($)", value=7_000_000, step=500_000)
    budget_limit = st.number_input("Additional Budget Limit ($)", value=1_000_000, step=100_000)
    risk_threshold = st.slider("Max Risk Score", 10, 80, 50)
    st.divider()
    optimize_btn = st.button("⚡ Optimize", use_container_width=True, type="primary")

# ── Run optimization ──────────────────────────────────────────────────────────
if optimize_btn or "opt_result" not in st.session_state:
    with st.spinner("Running SLSQP optimizer…"):
        try:
            result = optimize_profit(
                base_revenue=base_revenue,
                base_cost=base_cost,
                budget_limit=budget_limit,
                risk_threshold=risk_threshold,
            )
            st.session_state["opt_result"] = result
        except Exception as exc:
            st.error(f"Optimization failed: {exc}")
            st.stop()

result = st.session_state.get("opt_result", {})

if result:
    status_icon = "✅" if result["optimizer_success"] else "⚠️"
    st.markdown(f"**Optimizer Status:** {status_icon} {result['optimizer_message']}")

    st.markdown("### 🎯 Optimal Decision Variables")
    col1, col2, col3 = st.columns(3)
    col1.metric("Marketing Increase", f"{result['optimized_marketing_increase_pct']:.1f}%")
    col2.metric("Price Change", f"{result['optimized_price_change_pct']:.1f}%")
    col3.metric("New Hires", f"{result['optimized_hiring_count']}")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### 💹 Projected Outcome")
    col4, col5, col6 = st.columns(3)
    col4.metric("Projected Revenue", f"${result['projected_revenue']:,.0f}")
    col5.metric("Projected Cost", f"${result['projected_cost']:,.0f}")
    col6.metric("Projected Profit", f"${result['projected_profit']:,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    col_gauge, col_bar = st.columns([1, 2])

    with col_gauge:
        st.markdown("### ⚡ Optimized Risk Score")
        fig_risk = risk_gauge(result["risk_score"])
        st.plotly_chart(fig_risk, use_container_width=True)

    with col_bar:
        st.markdown("### 📊 Base vs Optimized Profit")
        base_profit = base_revenue - base_cost
        fig_compare = go.Figure(
            go.Bar(
                x=["Base Profit", "Optimized Profit"],
                y=[base_profit, result["projected_profit"]],
                marker=dict(color=["#374151", "#7c3aed"]),
                text=[f"${base_profit:,.0f}", f"${result['projected_profit']:,.0f}"],
                textposition="outside",
            )
        )
        fig_compare.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            font=dict(color="#e0e0e0"),
            yaxis_title="Profit (USD)",
            height=300,
            margin=dict(l=40, r=20, t=20, b=40),
        )
        st.plotly_chart(fig_compare, use_container_width=True)

    # ── Interpretation ────────────────────────────────────────────────────────
    profit_improvement = result["projected_profit"] - base_profit
    if profit_improvement > 0:
        st.success(
            f"✅ Optimization identifies a **${profit_improvement:,.0f}** profit improvement "
            f"with a risk score of **{result['risk_score']:.0f}/100** — within your threshold of {risk_threshold}."
        )
    else:
        st.warning(
            "⚠️ Optimization could not identify a profitable configuration within the given constraints. "
            "Consider increasing the budget limit or relaxing the risk threshold."
        )
