"""
data/generate_data.py
Generates synthetic business datasets for NeuroCore AI demonstration.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def generate_revenue_data(periods: int = 36, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic monthly revenue time-series data.

    Args:
        periods: Number of months of historical data.
        seed: Random seed for reproducibility.

    Returns:
        DataFrame with columns ['ds', 'y'] compatible with Prophet.
    """
    np.random.seed(seed)
    start_date = datetime(2021, 1, 1)
    dates = [start_date + timedelta(days=30 * i) for i in range(periods)]

    # Base trend + seasonality + noise
    trend = np.linspace(500_000, 900_000, periods)
    seasonality = 50_000 * np.sin(np.linspace(0, 4 * np.pi, periods))
    noise = np.random.normal(0, 20_000, periods)

    revenue = trend + seasonality + noise
    return pd.DataFrame({"ds": dates, "y": revenue})


def generate_churn_data(n_samples: int = 2000, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic customer churn dataset.

    Args:
        n_samples: Number of customer records.
        seed: Random seed for reproducibility.

    Returns:
        DataFrame with customer features and a binary 'churn' label.
    """
    np.random.seed(seed)

    tenure = np.random.randint(1, 72, n_samples)
    monthly_charges = np.random.uniform(20, 120, n_samples)
    total_charges = tenure * monthly_charges + np.random.normal(0, 50, n_samples)
    num_products = np.random.randint(1, 6, n_samples)
    support_calls = np.random.randint(0, 10, n_samples)
    contract_type = np.random.choice(
        ["Month-to-Month", "One Year", "Two Year"], n_samples, p=[0.5, 0.3, 0.2]
    )
    payment_method = np.random.choice(
        ["Electronic check", "Mailed check", "Bank transfer", "Credit card"],
        n_samples,
    )

    # Churn probability influenced by tenure, charges, and support calls
    churn_prob = (
        0.4 * (1 / (tenure + 1))
        + 0.3 * (monthly_charges / 120)
        + 0.2 * (support_calls / 10)
        - 0.1 * (num_products / 5)
    )
    churn_prob = np.clip(churn_prob, 0.05, 0.95)
    churn = (np.random.rand(n_samples) < churn_prob).astype(int)

    return pd.DataFrame(
        {
            "tenure": tenure,
            "monthly_charges": monthly_charges.round(2),
            "total_charges": total_charges.round(2),
            "num_products": num_products,
            "support_calls": support_calls,
            "contract_type": contract_type,
            "payment_method": payment_method,
            "churn": churn,
        }
    )


def generate_cost_data(periods: int = 180, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic daily cost data with injected anomalies.

    Args:
        periods: Number of daily records.
        seed: Random seed for reproducibility.

    Returns:
        DataFrame with cost features for anomaly detection.
    """
    np.random.seed(seed)
    dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(periods)]

    operational_cost = np.random.normal(10_000, 800, periods)
    marketing_cost = np.random.normal(5_000, 400, periods)
    hr_cost = np.random.normal(20_000, 1_000, periods)

    # Inject anomalies at random positions
    anomaly_indices = np.random.choice(periods, size=15, replace=False)
    operational_cost[anomaly_indices] += np.random.uniform(8_000, 20_000, 15)
    marketing_cost[anomaly_indices] += np.random.uniform(3_000, 10_000, 15)

    return pd.DataFrame(
        {
            "date": dates,
            "operational_cost": operational_cost.round(2),
            "marketing_cost": marketing_cost.round(2),
            "hr_cost": hr_cost.round(2),
            "total_cost": (operational_cost + marketing_cost + hr_cost).round(2),
        }
    )
