"""
models/churn_prediction.py
Customer churn prediction pipeline using Random Forest Classifier.
"""

import joblib
import numpy as np
import pandas as pd
from typing import Dict, Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


def preprocess_churn_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Preprocess churn dataset: handle missing values and encode categoricals.

    Args:
        df: Raw churn DataFrame.

    Returns:
        Tuple of (feature_df, label_series).
    """
    df = df.copy()

    # Fill missing numeric values with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    # Encode categorical columns
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))

    # Separate features and target
    if "churn" not in df.columns:
        raise ValueError("Dataset must contain a 'churn' target column.")

    X = df.drop(columns=["churn"])
    y = df["churn"]
    return X, y


def train_churn_model(
    df: pd.DataFrame, model_path: str = "churn_model.pkl"
) -> Tuple[RandomForestClassifier, Dict]:
    """
    Train a Random Forest Classifier for churn prediction.

    Args:
        df: Churn dataset including a 'churn' label column.
        model_path: File path to persist the trained model.

    Returns:
        Tuple of (trained_model, evaluation_metrics_dict).
    """
    X, y = preprocess_churn_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    # Evaluate on test set
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "roc_auc": round(float(roc_auc_score(y_test, y_proba)), 4),
        "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "feature_importances": dict(
            zip(X.columns.tolist(), model.feature_importances_.round(4).tolist())
        ),
    }

    # Persist trained model
    joblib.dump(model, model_path)

    return model, metrics


def predict_churn(
    model: RandomForestClassifier, df: pd.DataFrame
) -> pd.DataFrame:
    """
    Run churn prediction on new data.

    Args:
        model: Trained RandomForestClassifier.
        df: Feature DataFrame (without 'churn' column).

    Returns:
        DataFrame with added 'churn_probability' and 'churn_prediction' columns.
    """
    df = df.copy()
    # Remove target column if present
    df.drop(columns=["churn"], errors="ignore", inplace=True)

    # Encode categoricals
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))

    df["churn_probability"] = model.predict_proba(df)[:, 1].round(4)
    df["churn_prediction"] = (df["churn_probability"] >= 0.5).astype(int)
    return df
