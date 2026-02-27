"""
utils/visualization.py
Reusable Plotly chart helpers for NeuroCore AI Streamlit pages.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Optional

from utils.theme import COLORS, plotly_layout


# ── Shared theme ────────────────────────────────────────────────────────────────
def _layout_defaults(**overrides) -> dict:
    return plotly_layout(**overrides)


def revenue_forecast_chart(
    historical_df: pd.DataFrame,
    forecast_df: pd.DataFrame,
    title: str = "Revenue Forecast",
) -> go.Figure:
    """
    Plot historical revenue with Prophet forecast and confidence interval.

    Args:
        historical_df: DataFrame with 'ds' and 'y' columns (historical data).
        forecast_df: Prophet forecast DataFrame with 'ds', 'yhat', 'yhat_lower', 'yhat_upper'.
        title: Chart title.

    Returns:
        Plotly Figure.
    """
    future_forecast = forecast_df[forecast_df["ds"] > historical_df["ds"].max()]

    fig = go.Figure()

    # Confidence interval band
    fig.add_trace(
        go.Scatter(
            x=pd.concat([future_forecast["ds"], future_forecast["ds"][::-1]]),
            y=pd.concat([future_forecast["yhat_upper"], future_forecast["yhat_lower"][::-1]]),
            fill="toself",
            fillcolor="rgba(0,212,255,0.10)",
            line=dict(color="rgba(255,255,255,0)"),
            name="Confidence Interval",
            showlegend=True,
        )
    )

    # Historical line
    fig.add_trace(
        go.Scatter(
            x=historical_df["ds"],
            y=historical_df["y"],
            mode="lines+markers",
            name="Historical Revenue",
            line=dict(color=COLORS["accent"], width=2),
            marker=dict(size=5),
        )
    )

    # Forecast line
    fig.add_trace(
        go.Scatter(
            x=future_forecast["ds"],
            y=future_forecast["yhat"],
            mode="lines+markers",
            name="Forecast",
            line=dict(color=COLORS["success"], width=2, dash="dash"),
            marker=dict(size=6, symbol="diamond"),
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Revenue (USD)",
        **_layout_defaults(),
    )
    return fig


def confusion_matrix_chart(cm: list, title: str = "Confusion Matrix") -> go.Figure:
    """
    Render a confusion matrix heatmap.

    Args:
        cm: 2x2 confusion matrix as nested list.
        title: Chart title.

    Returns:
        Plotly Figure.
    """
    labels = ["Not Churned", "Churned"]
    fig = px.imshow(
        cm,
        labels=dict(x="Predicted", y="Actual", color="Count"),
        x=labels,
        y=labels,
        color_continuous_scale="Blues",
        text_auto=True,
        title=title,
    )
    fig.update_layout(**_layout_defaults())
    return fig


def feature_importance_chart(
    importances: dict, title: str = "Feature Importances"
) -> go.Figure:
    """
    Horizontal bar chart of Random Forest feature importances.

    Args:
        importances: Dict mapping feature name → importance score.
        title: Chart title.

    Returns:
        Plotly Figure.
    """
    sorted_items = sorted(importances.items(), key=lambda x: x[1])
    features, scores = zip(*sorted_items) if sorted_items else ([], [])

    fig = go.Figure(
        go.Bar(
            x=list(scores),
            y=list(features),
            orientation="h",
            marker=dict(
                color=COLORS["accent"],
                opacity=0.85,
            ),
        )
    )
    fig.update_layout(
        title=title,
        xaxis_title="Importance Score",
        yaxis_title="Feature",
        **_layout_defaults(),
    )
    return fig


def anomaly_chart(df: pd.DataFrame, title: str = "Cost Anomaly Detection") -> go.Figure:
    """
    Plot total cost over time, highlighting anomalous points.

    Args:
        df: DataFrame with 'date', 'total_cost', and 'is_anomaly' columns.
        title: Chart title.

    Returns:
        Plotly Figure.
    """
    normal = df[~df["is_anomaly"]]
    anomalies = df[df["is_anomaly"]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=normal["date"],
            y=normal["total_cost"],
            mode="lines+markers",
            name="Normal",
            line=dict(color=COLORS["accent"], width=1.5),
            marker=dict(size=4),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=anomalies["date"],
            y=anomalies["total_cost"],
            mode="markers",
            name="Anomaly",
            marker=dict(color=COLORS["danger"], size=10, symbol="x"),
        )
    )
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Total Cost (USD)",
        **_layout_defaults(),
    )
    return fig


def risk_gauge(risk_score: float, title: str = "Business Risk Score") -> go.Figure:
    """
    Render a gauge chart for the business risk score.

    Args:
        risk_score: Risk score 0–100.
        title: Chart title.

    Returns:
        Plotly Figure.
    """
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=risk_score,
            title={"text": title, "font": {"color": COLORS["text"], "size": 14}},
            number={"font": {"color": COLORS["text"], "size": 36}},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickcolor": COLORS["text_muted"],
                    "tickfont": {"color": COLORS["text_muted"], "size": 11},
                },
                "bar": {"color": _risk_color(risk_score)},
                "bgcolor": COLORS["card_bg"],
                "bordercolor": COLORS["border"],
                "steps": [
                    {"range": [0, 20],  "color": "#0B2B1E"},
                    {"range": [20, 40], "color": "#1A2E0A"},
                    {"range": [40, 65], "color": "#2B1A08"},
                    {"range": [65, 100],"color": "#2B0808"},
                ],
                "threshold": {
                    "line": {"color": COLORS["text"], "width": 3},
                    "thickness": 0.75,
                    "value": risk_score,
                },
            },
        )
    )
    fig.update_layout(
        paper_bgcolor=COLORS["bg"],
        font=dict(color=COLORS["text_sec"]),
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig


def _risk_color(score: float) -> str:
    if score < 20:
        return COLORS["success"]
    if score < 40:
        return COLORS["warning"]
    if score < 65:
        return "#FF8C00"
    return COLORS["danger"]
