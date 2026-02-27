"""
models/anomaly_detection.py
Cost anomaly detection module using Isolation Forest.
"""

import numpy as np
import pandas as pd
from typing import Tuple, List
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def detect_cost_anomalies(
    df: pd.DataFrame,
    feature_cols: List[str] = None,
    contamination: float = 0.08,
) -> Tuple[pd.DataFrame, IsolationForest, StandardScaler]:
    """
    Detect cost anomalies using Isolation Forest.

    Args:
        df: DataFrame containing cost features.
        feature_cols: Columns to use for anomaly detection.
                      Defaults to all numeric columns except 'date'.
        contamination: Expected proportion of anomalies in the dataset.

    Returns:
        Tuple of (result_df, trained_model, scaler).
        result_df has an added 'is_anomaly' boolean column.
    """
    if df.empty:
        raise ValueError("Input DataFrame must not be empty.")

    df = df.copy()

    # Default to all numeric columns, excluding date-like columns
    if feature_cols is None:
        feature_cols = [
            col
            for col in df.select_dtypes(include=[np.number]).columns.tolist()
            if col.lower() not in ("date", "timestamp", "index")
        ]

    if not feature_cols:
        raise ValueError("No numeric feature columns found for anomaly detection.")

    X = df[feature_cols].values

    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train Isolation Forest
    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=42,
        n_jobs=-1,
    )
    predictions = model.fit_predict(X_scaled)

    # Convert: Isolation Forest returns -1 for anomalies, 1 for normal
    df["is_anomaly"] = predictions == -1
    df["anomaly_score"] = model.score_samples(X_scaled).round(4)

    return df, model, scaler
