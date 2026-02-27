"""
utils/optimization.py
Profit optimization engine using scipy.optimize for NeuroCore AI.
"""

import numpy as np
from typing import Dict
from scipy.optimize import minimize


def optimize_profit(
    base_revenue: float,
    base_cost: float,
    budget_limit: float,
    risk_threshold: float = 50.0,
) -> Dict:
    """
    Optimize marketing spend, pricing, and hiring to maximize profit.

    Decision variables:
        x[0] = marketing_increase_percent  (0 – 50%)
        x[1] = price_change_percent        (-10% to +15%)
        x[2] = employee_hiring_count       (0 – 50)

    Args:
        base_revenue: Current annual revenue in USD.
        base_cost: Current annual cost in USD.
        budget_limit: Maximum additional spend allowed (USD).
        risk_threshold: Maximum acceptable risk score (0–100).

    Returns:
        Dictionary with optimized variable values and projected financials.
    """

    def _profit_objective(x: np.ndarray) -> float:
        """Negative profit (minimization target)."""
        mktg_pct, price_pct, hires = x
        avg_emp_cost = 60_000.0

        revenue = (
            base_revenue
            + base_revenue * (mktg_pct / 100) * 0.5
            + base_revenue * (price_pct / 100)
        )
        cost = (
            base_cost
            + base_cost * (mktg_pct / 100)
            + hires * avg_emp_cost
        )
        return -(revenue - cost)

    def _risk_constraint(x: np.ndarray) -> float:
        """Risk score must stay at or below risk_threshold."""
        mktg_pct, price_pct, hires = x
        risk = (
            abs(mktg_pct) * 0.4
            + abs(price_pct) * 1.2
            + hires * 0.3
        )
        return risk_threshold - risk  # >= 0

    def _budget_constraint(x: np.ndarray) -> float:
        """Additional spend must not exceed budget_limit."""
        mktg_pct, _price_pct, hires = x
        avg_emp_cost = 60_000.0
        additional_spend = base_cost * (mktg_pct / 100) + hires * avg_emp_cost
        return budget_limit - additional_spend  # >= 0

    # Initial guess: small positive values
    x0 = np.array([5.0, 2.0, 2.0])

    bounds = [(0, 50), (-10, 15), (0, 50)]
    constraints = [
        {"type": "ineq", "fun": _risk_constraint},
        {"type": "ineq", "fun": _budget_constraint},
    ]

    result = minimize(
        _profit_objective,
        x0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"ftol": 1e-6, "maxiter": 500},
    )

    if not result.success:
        # Return a safe fallback if optimizer fails
        opt_mktg, opt_price, opt_hires = x0
    else:
        opt_mktg, opt_price, opt_hires = result.x

    # Compute final projected figures using optimized variables
    avg_emp_cost = 60_000.0
    opt_revenue = (
        base_revenue
        + base_revenue * (opt_mktg / 100) * 0.5
        + base_revenue * (opt_price / 100)
    )
    opt_cost = base_cost + base_cost * (opt_mktg / 100) + opt_hires * avg_emp_cost
    opt_profit = opt_revenue - opt_cost
    opt_risk = min(100, abs(opt_mktg) * 0.4 + abs(opt_price) * 1.2 + opt_hires * 0.3)

    return {
        "optimized_marketing_increase_pct": round(float(opt_mktg), 2),
        "optimized_price_change_pct": round(float(opt_price), 2),
        "optimized_hiring_count": int(round(float(opt_hires))),
        "projected_revenue": round(float(opt_revenue), 2),
        "projected_cost": round(float(opt_cost), 2),
        "projected_profit": round(float(opt_profit), 2),
        "risk_score": round(float(opt_risk), 1),
        "optimizer_success": bool(result.success),
        "optimizer_message": result.message if hasattr(result, "message") else "",
    }
