"""
utils/strategy_simulator.py
Business strategy simulation engine for NeuroCore AI.
"""

from typing import Dict


def simulate_strategy(
    base_revenue: float,
    base_cost: float,
    marketing_increase_percent: float = 0.0,
    price_change_percent: float = 0.0,
    employee_hiring_count: int = 0,
    retention_investment: float = 0.0,
    avg_employee_cost: float = 60_000.0,
    churn_rate: float = 0.15,
) -> Dict:
    """
    Simulate the financial and risk impact of business strategy decisions.

    Args:
        base_revenue: Current annual revenue in USD.
        base_cost: Current annual cost in USD.
        marketing_increase_percent: Percentage increase in marketing spend.
        price_change_percent: Percentage change in product pricing.
        employee_hiring_count: Number of new employees to hire.
        retention_investment: Additional investment in customer retention (USD).
        avg_employee_cost: Average annual cost per new employee.
        churn_rate: Current customer churn rate (0–1).

    Returns:
        Dictionary with projected revenue, cost, profit, ROI, and risk score.
    """
    # --- Revenue Impact ---
    # Marketing lift: 1% marketing increase → ~0.5% revenue lift (diminishing returns)
    marketing_revenue_lift = base_revenue * (marketing_increase_percent / 100) * 0.5

    # Pricing impact: direct multiplier on existing revenue
    pricing_revenue_impact = base_revenue * (price_change_percent / 100)

    # Retention impact: reduces churn; $1 retention spend recovers ~$3 in revenue
    retention_revenue_lift = retention_investment * 3 * churn_rate

    projected_revenue = (
        base_revenue
        + marketing_revenue_lift
        + pricing_revenue_impact
        + retention_revenue_lift
    )

    # --- Cost Impact ---
    marketing_cost_increase = base_cost * (marketing_increase_percent / 100)
    hiring_cost = employee_hiring_count * avg_employee_cost

    projected_cost = base_cost + marketing_cost_increase + hiring_cost + retention_investment

    # --- Profit & ROI ---
    base_profit = base_revenue - base_cost
    projected_profit = projected_revenue - projected_cost
    incremental_investment = projected_cost - base_cost

    roi = (
        ((projected_profit - base_profit) / incremental_investment * 100)
        if incremental_investment > 0
        else 0.0
    )

    # --- Risk Score (0–100) ---
    # Higher marketing spend, aggressive pricing, and large hiring increase risk
    risk_score = min(
        100,
        abs(marketing_increase_percent) * 0.4
        + abs(price_change_percent) * 1.2
        + employee_hiring_count * 0.3
        + (retention_investment / 10_000) * 0.5,
    )

    return {
        "base_revenue": round(base_revenue, 2),
        "base_cost": round(base_cost, 2),
        "base_profit": round(base_profit, 2),
        "projected_revenue": round(projected_revenue, 2),
        "projected_cost": round(projected_cost, 2),
        "projected_profit": round(projected_profit, 2),
        "revenue_delta": round(projected_revenue - base_revenue, 2),
        "cost_delta": round(projected_cost - base_cost, 2),
        "profit_delta": round(projected_profit - base_profit, 2),
        "roi_percent": round(roi, 2),
        "risk_score": round(risk_score, 1),
    }
