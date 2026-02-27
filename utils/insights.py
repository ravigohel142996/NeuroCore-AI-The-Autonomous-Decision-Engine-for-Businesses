"""
utils/insights.py
Rule-based executive AI insight generator for NeuroCore AI.
"""

from typing import Dict, List


def generate_executive_insights(
    revenue_trend: str,
    churn_rate: float,
    anomaly_count: int,
    risk_score: float,
    forecast_mape: float = None,
    projected_profit_delta: float = None,
) -> Dict:
    """
    Generate board-level executive insights based on business KPIs.

    Args:
        revenue_trend: "up", "down", or "stable".
        churn_rate: Current customer churn rate as a decimal (e.g., 0.15 = 15%).
        anomaly_count: Number of detected cost anomalies.
        risk_score: Business risk score (0–100).
        forecast_mape: Revenue forecast MAPE (optional).
        projected_profit_delta: Change in projected profit vs baseline (optional).

    Returns:
        Dictionary containing a structured executive summary and action items.
    """
    insights: List[str] = []
    action_items: List[str] = []
    risk_level = _classify_risk(risk_score)
    churn_level = _classify_churn(churn_rate)

    # --- Revenue Commentary ---
    if revenue_trend == "up":
        insights.append(
            "Revenue trajectory is positive, reflecting healthy market demand "
            "and effective go-to-market execution."
        )
    elif revenue_trend == "down":
        insights.append(
            "Revenue is exhibiting a downward trend. Immediate investigation into "
            "pricing strategy, sales pipeline health, and competitive positioning is warranted."
        )
        action_items.append("Conduct urgent revenue recovery review with Sales & Marketing leadership.")
    else:
        insights.append(
            "Revenue performance remains stable. Consider growth initiatives to "
            "capitalize on market opportunities and drive above-benchmark returns."
        )
        action_items.append("Identify and evaluate new revenue stream opportunities.")

    # --- Churn Commentary ---
    if churn_level == "critical":
        insights.append(
            f"Customer churn rate stands at {churn_rate:.1%}, which is critically high. "
            "This poses a material risk to recurring revenue and customer lifetime value."
        )
        action_items.append(
            "Initiate emergency churn reduction program: targeted retention campaigns, "
            "proactive customer success outreach, and product feedback loops."
        )
    elif churn_level == "elevated":
        insights.append(
            f"Churn rate of {churn_rate:.1%} is above industry benchmarks. "
            "Retention investment should be prioritized in the next budget cycle."
        )
        action_items.append("Launch structured customer retention program with measurable KPIs.")
    else:
        insights.append(
            f"Customer churn is well-controlled at {churn_rate:.1%}, demonstrating "
            "strong customer satisfaction and loyalty program effectiveness."
        )

    # --- Anomaly Commentary ---
    if anomaly_count > 10:
        insights.append(
            f"{anomaly_count} cost anomalies detected in operational expenditure. "
            "This level of irregularity may indicate process inefficiencies, "
            "procurement issues, or potential financial risk."
        )
        action_items.append(
            "Engage Finance and Operations teams to investigate cost anomalies "
            "and implement cost governance controls."
        )
    elif anomaly_count > 3:
        insights.append(
            f"{anomaly_count} moderate cost anomalies identified. "
            "Targeted review of flagged cost centres is recommended."
        )
        action_items.append("Schedule cost anomaly review with Finance team.")
    else:
        insights.append(
            "Cost structure is operating within normal parameters. "
            "Expenditure discipline is commendable."
        )

    # --- Risk Commentary ---
    insights.append(
        f"Overall business risk score is {risk_score:.0f}/100 ({risk_level}). "
        + _risk_commentary(risk_level)
    )
    if risk_level in ("High", "Critical"):
        action_items.append(
            "Convene Risk Committee to review and mitigate elevated business risk exposure."
        )

    # --- Forecast Accuracy ---
    if forecast_mape is not None:
        if forecast_mape < 5:
            insights.append(
                f"Revenue forecast model achieves high accuracy with MAPE of {forecast_mape:.2f}%. "
                "Leadership can rely on forecast outputs with confidence."
            )
        elif forecast_mape < 10:
            insights.append(
                f"Revenue forecast MAPE of {forecast_mape:.2f}% is acceptable. "
                "Periodic model recalibration is advisable."
            )
        else:
            insights.append(
                f"Forecast MAPE of {forecast_mape:.2f}% indicates high uncertainty. "
                "Model retraining with more recent data is strongly recommended."
            )

    # --- Profit Delta ---
    if projected_profit_delta is not None:
        if projected_profit_delta > 0:
            insights.append(
                f"Strategic initiatives are projected to deliver ${projected_profit_delta:,.0f} "
                "in incremental profit — a positive signal for shareholder value creation."
            )
        else:
            insights.append(
                f"Current strategic plan projects a profit shortfall of "
                f"${abs(projected_profit_delta):,.0f}. Recalibration of investment allocation is advised."
            )

    executive_summary = " ".join(insights)

    return {
        "executive_summary": executive_summary,
        "action_items": action_items,
        "risk_level": risk_level,
        "churn_level": churn_level,
        "key_metrics": {
            "risk_score": risk_score,
            "churn_rate_pct": round(churn_rate * 100, 2),
            "anomaly_count": anomaly_count,
            "revenue_trend": revenue_trend,
        },
    }


# --- Helper functions ---

def _classify_risk(score: float) -> str:
    if score < 20:
        return "Low"
    if score < 40:
        return "Moderate"
    if score < 65:
        return "High"
    return "Critical"


def _classify_churn(rate: float) -> str:
    if rate < 0.05:
        return "healthy"
    if rate < 0.15:
        return "elevated"
    return "critical"


def _risk_commentary(level: str) -> str:
    comments = {
        "Low": "The business is operating in a stable risk environment.",
        "Moderate": "Moderate risk warrants proactive monitoring and contingency planning.",
        "High": "Elevated risk requires immediate strategic attention and mitigation measures.",
        "Critical": "Critical risk levels demand urgent executive intervention.",
    }
    return comments.get(level, "")
