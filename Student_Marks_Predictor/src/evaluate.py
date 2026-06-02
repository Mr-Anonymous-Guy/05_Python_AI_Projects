"""
evaluate.py — Model evaluation and metrics reporting.

Computes MAE, MSE, RMSE, and R² for a model's predictions and
provides formatted reports for display or logging.
"""

from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ──────────────────────────────────────────────────────────────
# Evaluation metrics
# ──────────────────────────────────────────────────────────────


def compute_metrics(
    y_true: pd.Series | np.ndarray,
    y_pred: np.ndarray,
) -> dict[str, float]:
    """
    Compute regression evaluation metrics.

    Args:
        y_true: Ground truth values.
        y_pred: Model predictions.

    Returns:
        Dictionary with keys: "MAE", "MSE", "RMSE", "R2".
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)

    return {
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2,
    }


def display_metrics(metrics: dict[str, float]) -> str:
    """
    Format evaluation metrics as a pretty table string.

    Args:
        metrics: Dictionary from compute_metrics().

    Returns:
        Multi-line string ready to print.
    """
    lines = [
        "\n" + "=" * 56,
        "  📊  Evaluation Metrics",
        "=" * 56,
        f"  MAE (Mean Absolute Error)       : {metrics['MAE']:.4f}",
        f"  MSE (Mean Squared Error)        : {metrics['MSE']:.4f}",
        f"  RMSE (Root Mean Squared Error)  : {metrics['RMSE']:.4f}",
        f"  R² (Coefficient of Determination): {metrics['R2']:.4f}",
        "=" * 56,
    ]
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────
# Model evaluation wrapper
# ──────────────────────────────────────────────────────────────


def evaluate_model(
    model: Any,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict[str, float]:
    """
    Evaluate a trained model on a test set.

    Args:
        model: Fitted scikit-learn estimator.
        X_test: Test features.
        y_test: Test target values.

    Returns:
        Dictionary of computed metrics.
    """
    y_pred = model.predict(X_test)
    return compute_metrics(y_test, y_pred)
