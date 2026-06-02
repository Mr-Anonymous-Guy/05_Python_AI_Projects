"""
visualize.py — Data and model visualization tools.

Creates publication-quality charts using matplotlib and seaborn:
  - Correlation heatmaps
  - Actual vs Predicted scatter plots
  - Model performance comparisons
  - Residual plots
"""

from pathlib import Path
from typing import Any, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import mean_absolute_error, r2_score

from src.train import TrainingResult


# ──────────────────────────────────────────────────────────────
# Style configuration
# ──────────────────────────────────────────────────────────────

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["font.size"] = 10


# ──────────────────────────────────────────────────────────────
# Correlation heatmap
# ──────────────────────────────────────────────────────────────


def plot_correlation_heatmap(
    df: pd.DataFrame,
    save_path: Optional[Path | str] = None,
) -> None:
    """
    Display a correlation heatmap for all numeric columns.

    Args:
        df: Input DataFrame.
        save_path: If provided, save the figure to this path.
    """
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8},
    )
    plt.title("Feature Correlation Heatmap", fontsize=14, fontweight="bold")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"  💾  Heatmap saved to: {Path(save_path).resolve()}")

    plt.show()


# ──────────────────────────────────────────────────────────────
# Actual vs Predicted
# ──────────────────────────────────────────────────────────────


def plot_actual_vs_predicted(
    y_true: pd.Series | np.ndarray,
    y_pred: np.ndarray,
    model_name: str = "Model",
    save_path: Optional[Path | str] = None,
) -> None:
    """
    Scatter plot of actual vs predicted values with a diagonal line.

    Args:
        y_true: Ground truth values.
        y_pred: Model predictions.
        model_name: Display name for the chart title.
        save_path: If provided, save the figure to this path.
    """
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    plt.figure(figsize=(8, 8))
    plt.scatter(y_true, y_pred, alpha=0.6, edgecolors="k", s=50)

    # Diagonal reference line
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], "r--", lw=2, label="Perfect Prediction")

    plt.xlabel("Actual Marks", fontsize=12, fontweight="bold")
    plt.ylabel("Predicted Marks", fontsize=12, fontweight="bold")
    plt.title(
        f"Actual vs Predicted — {model_name}\nMAE: {mae:.2f}  |  R²: {r2:.4f}",
        fontsize=14,
        fontweight="bold",
    )
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"  💾  Chart saved to: {Path(save_path).resolve()}")

    plt.show()


# ──────────────────────────────────────────────────────────────
# Model comparison bar chart
# ──────────────────────────────────────────────────────────────


def plot_model_comparison(
    results: list[TrainingResult],
    save_path: Optional[Path | str] = None,
) -> None:
    """
    Bar chart comparing R² scores across multiple models.

    Args:
        results: List of TrainingResult objects.
        save_path: If provided, save the figure to this path.
    """
    names = [r.model_name for r in results]
    r2_scores = [r.r2 for r in results]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, r2_scores, color=["#3498db", "#e74c3c", "#2ecc71"], edgecolor="black")

    # Annotate bars with values
    for bar, score in zip(bars, r2_scores):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.01,
            f"{score:.4f}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )

    plt.ylabel("R² Score", fontsize=12, fontweight="bold")
    plt.title("Model Performance Comparison", fontsize=14, fontweight="bold")
    plt.ylim(0, 1.0)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"  💾  Comparison chart saved to: {Path(save_path).resolve()}")

    plt.show()


# ──────────────────────────────────────────────────────────────
# Residual plot
# ──────────────────────────────────────────────────────────────


def plot_residuals(
    y_true: pd.Series | np.ndarray,
    y_pred: np.ndarray,
    model_name: str = "Model",
    save_path: Optional[Path | str] = None,
) -> None:
    """
    Plot residuals (prediction errors) against predicted values.

    Args:
        y_true: Ground truth values.
        y_pred: Model predictions.
        model_name: Display name for the chart title.
        save_path: If provided, save the figure to this path.
    """
    residuals = np.array(y_true) - y_pred

    plt.figure(figsize=(10, 6))
    plt.scatter(y_pred, residuals, alpha=0.6, edgecolors="k", s=50)
    plt.axhline(0, color="red", linestyle="--", lw=2, label="Zero Error")

    plt.xlabel("Predicted Marks", fontsize=12, fontweight="bold")
    plt.ylabel("Residuals (Actual - Predicted)", fontsize=12, fontweight="bold")
    plt.title(f"Residual Plot — {model_name}", fontsize=14, fontweight="bold")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"  💾  Residual plot saved to: {Path(save_path).resolve()}")

    plt.show()


# ──────────────────────────────────────────────────────────────
# Distribution plots
# ──────────────────────────────────────────────────────────────


def plot_target_distribution(
    y: pd.Series,
    save_path: Optional[Path | str] = None,
) -> None:
    """
    Plot histogram and KDE of the target variable.

    Args:
        y: Target Series.
        save_path: If provided, save the figure to this path.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(y, kde=True, bins=30, color="steelblue", edgecolor="black")

    plt.xlabel("Marks", fontsize=12, fontweight="bold")
    plt.ylabel("Frequency", fontsize=12, fontweight="bold")
    plt.title("Target Variable Distribution", fontsize=14, fontweight="bold")
    plt.grid(alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"  💾  Distribution plot saved to: {Path(save_path).resolve()}")

    plt.show()
