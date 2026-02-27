"""
models/revenue_forecast.py
Revenue forecasting module using Facebook Prophet.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict


def compute_mape(actual: pd.Series, predicted: pd.Series) -> float:
    """
    Compute Mean Absolute Percentage Error (MAPE).

    Args:
        actual: Series of actual values.
        predicted: Series of predicted values.

    Returns:
        MAPE as a float (0–100 scale).
    """
    mask = actual != 0
    return float(np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask])) * 100)


def run_revenue_forecast(
    df: pd.DataFrame, forecast_periods: int = 6
) -> Tuple[pd.DataFrame, Dict]:
    """
    Train a Prophet model and generate a revenue forecast.

    Args:
        df: DataFrame with columns ['ds', 'y'] (date and revenue).
        forecast_periods: Number of future months to predict.

    Returns:
        Tuple of (forecast_df, metrics_dict).
        forecast_df contains Prophet output columns.
        metrics_dict includes MAPE and last known revenue.
    """
    try:
        # Import here to avoid top-level import issues in constrained environments
        from prophet import Prophet  # type: ignore
    except ImportError as exc:
        raise ImportError(
            "Facebook Prophet is required. Install it via: pip install prophet"
        ) from exc

    if df.empty or "ds" not in df.columns or "y" not in df.columns:
        raise ValueError("Input DataFrame must contain 'ds' and 'y' columns.")

    df = df.copy()
    df["ds"] = pd.to_datetime(df["ds"])

    # Train Prophet model with weekly/yearly seasonality disabled for monthly data
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
        changepoint_prior_scale=0.05,
    )
    model.fit(df)

    # Build future dataframe and predict
    future = model.make_future_dataframe(periods=forecast_periods, freq="MS")
    forecast = model.predict(future)

    # Calculate in-sample MAPE on the training portion
    train_predictions = forecast[forecast["ds"].isin(df["ds"])]["yhat"]
    mape = compute_mape(df["y"].values, train_predictions.values)

    metrics = {
        "mape": round(mape, 2),
        "last_actual_revenue": round(float(df["y"].iloc[-1]), 2),
        "next_month_forecast": round(
            float(forecast[forecast["ds"] > df["ds"].max()]["yhat"].iloc[0]), 2
        ),
    }

    return forecast, metrics
