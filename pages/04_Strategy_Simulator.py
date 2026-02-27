"""
pages/04_Strategy_Simulator.py
Business Strategy Simulator page for NeuroCore AI.
"""

import sys
import os
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.strategy_simulator import simulate_strategy
from utils.visualization import risk_gauge
from utils.theme import inject_css, section_header

st.set_page_config(page_title="Strategy Simulator · NeuroCore AI", page_icon="🧩", layout="wide")
inject_css()

st.markdown("# 🧩 Strategy Simulator")
st.markdown(
    '<p style="color:#C9D1D9;">Model the financial impact of key business decisions before committing resources.</p>',
    unsafe_allow_html=True,
)
st.divider()

# ── Inputs ────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📥 Strategy Inputs")
    base_revenue = st.number_input("Base Annual Revenue ($)", value=10_000_000, step=500_000)
    base_cost = st.number_input("Base Annual Cost ($)", value=7_000_000, step=500_000)
    churn_rate = st.slider("Current Churn Rate", 0.01, 0.40, 0.15, step=0.01, format="%.2f")
    st.divider()
    marketing_pct = st.slider("Marketing Increase (%)", 0, 50, 10)
    price_pct = st.slider("Price Change (%)", -10, 20, 5)
    hiring = st.slider("New Hires", 0, 50, 5)
    retention_inv = st.number_input("Retention Investment ($)", value=100_000, step=10_000)
    st.divider()
    simulate_btn = st.button("▶️ Run Simulation", use_container_width=True, type="primary")

# ── Run simulation ────────────────────────────────────────────────────────────────
if simulate_btn or "sim_result" not in st.session_state:
    result = simulate_strategy(
        base_revenue=base_revenue,
        base_cost=base_cost,
        marketing_increase_percent=marketing_pct,
        price_change_percent=price_pct,
        employee_hiring_count=hiring,
        retention_investment=retention_inv,
        churn_rate=churn_rate,
    )
    st.session_state["sim_result"] = result

result = st.session_state.get("sim_result", {})

if result:
    # ── Financial summary ─────────────────────────────────────────────────────────
    section_header("Projected Financials")
    col1, col2, col3 = st.columns(3)

    rev_delta = result["revenue_delta"]
    cost_delta = result["cost_delta"]
    profit_delta = result["profit_delta"]

    col1.metric(
        "Projected Revenue",
        f"${result['projected_revenue']:,.0f}",
        delta=f"${rev_delta:+,.0f}",
        delta_color="normal",
    )
    col2.metric(
        "Projected Cost",
        f"${result['projected_cost']:,.0f}",
        delta=f"${cost_delta:+,.0f}",
        delta_color="inverse",
    )
    col3.metric(
        "Projected Profit",
        f"${result['projected_profit']:,.0f}",
        delta=f"${profit_delta:+,.0f}",
        delta_color="normal",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col_roi, col_gauge = st.columns([1, 1])

    with col_roi:
        section_header("ROI Analysis")
        st.markdown(
            f"""
            | Metric | Value |
            |--------|-------|
            | Base Profit | ${result['base_profit']:,.0f} |
            | Projected Profit | ${result['projected_profit']:,.0f} |
            | Profit Delta | ${result['profit_delta']:+,.0f} |
            | ROI on Incremental Investment | **{result['roi_percent']:.1f}%** |
            """
        )

    with col_gauge:
        section_header("Business Risk Score")
        fig_risk = risk_gauge(result["risk_score"])
        st.plotly_chart(fig_risk, use_container_width=True)

    # ── Interpretation ────────────────────────────────────────────────────────────
    section_header("Simulation Interpretation")
    if result["roi_percent"] > 20:
        st.success(
            f"✅ Strong ROI of **{result['roi_percent']:.1f}%**. "
            "This strategy delivers above-threshold returns. Recommend proceeding."
        )
    elif result["roi_percent"] > 0:
        st.warning(
            f"⚠️ Moderate ROI of **{result['roi_percent']:.1f}%**. "
            "Returns are positive but below the 20% benchmark. Consider refining the strategy."
        )
    else:
        st.error(
            f"❌ Negative ROI of **{result['roi_percent']:.1f}%**. "
            "This configuration results in a net loss. Revisit cost and investment assumptions."
        )

    risk = result["risk_score"]
    if risk >= 65:
        st.error(f"🔴 Risk Score {risk:.0f}/100 — Critical. Immediate risk mitigation required.")
    elif risk >= 40:
        st.warning(f"🟡 Risk Score {risk:.0f}/100 — Elevated. Monitor closely.")
    else:
        st.success(f"🟢 Risk Score {risk:.0f}/100 — Acceptable risk level.")
