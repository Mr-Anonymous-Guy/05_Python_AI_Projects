"""
utils.py — Data loading, validation, and preprocessing utilities.

Handles CSV I/O, missing value detection, and basic data quality checks.
All functions are pure (no global state) for testability.
"""

import os
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import pandas as pd


# ──────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR     = PROJECT_ROOT / "data"
MODELS_DIR   = PROJECT_ROOT / "models"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)


# ──────────────────────────────────────────────────────────────
# Data loading
# ──────────────────────────────────────────────────────────────


def load_dataset(filepath: Path | str) -> pd.DataFrame:
    """
    Load a CSV dataset into a pandas DataFrame.

    Args:
        filepath: Path to the CSV file.

    Returns:
        Loaded DataFrame.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        pd.errors.EmptyDataError: If the CSV is empty.
        pd.errors.ParserError: If the CSV is malformed.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"Dataset is empty: {path}")

    return df


def validate_dataset(
    df: pd.DataFrame,
    required_columns: list[str],
) -> Tuple[bool, list[str]]:
    """
    Validate that a DataFrame contains the expected columns.

    Args:
        df: DataFrame to validate.
        required_columns: List of column names that must be present.

    Returns:
        Tuple of (is_valid: bool, missing_columns: list[str]).
    """
    missing = [col for col in required_columns if col not in df.columns]
    return len(missing) == 0, missing


def check_missing_values(df: pd.DataFrame) -> dict[str, int]:
    """
    Count missing values per column.

    Args:
        df: Input DataFrame.

    Returns:
        Dictionary mapping column names to missing-value counts.
    """
    return df.isnull().sum().to_dict()


def handle_missing_values(
    df: pd.DataFrame,
    strategy: str = "drop",
) -> pd.DataFrame:
    """
    Handle missing values in a DataFrame.

    Args:
        df: Input DataFrame.
        strategy: One of "drop" (remove rows with NaNs) or
                 "mean" (fill numeric columns with column mean).

    Returns:
        DataFrame with missing values handled.

    Raises:
        ValueError: If strategy is not recognized.
    """
    if strategy == "drop":
        return df.dropna()
    elif strategy == "mean":
        # Fill numeric columns with mean
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        return df
    else:
        raise ValueError(f"Unknown strategy: {strategy!r}")


# ──────────────────────────────────────────────────────────────
# Display helpers
# ──────────────────────────────────────────────────────────────


def display_dataset_info(df: pd.DataFrame) -> str:
    """
    Return a formatted string summarising the dataset.

    Args:
        df: Input DataFrame.

    Returns:
        Multi-line summary string.
    """
    lines = [
        "\n" + "=" * 56,
        "  📊  Dataset Summary",
        "=" * 56,
        f"  Rows       : {len(df)}",
        f"  Columns    : {len(df.columns)}",
        f"  Memory     : {df.memory_usage(deep=True).sum() / 1024:.2f} KB",
        "=" * 56,
        "\n  Column Details:",
    ]
    for col in df.columns:
        dtype = df[col].dtype
        missing = df[col].isnull().sum()
        lines.append(f"    • {col:<20} {dtype}  (missing: {missing})")

    lines += [
        "=" * 56,
        "\n  Statistical Summary:",
        str(df.describe()),
        "=" * 56,
    ]
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────
# Train/test splitting
# ──────────────────────────────────────────────────────────────


def split_features_target(
    df: pd.DataFrame,
    target_column: str,
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Split a DataFrame into features (X) and target (y).

    Args:
        df: Full dataset.
        target_column: Name of the column to predict.

    Returns:
        (X, y) where X is feature DataFrame, y is target Series.

    Raises:
        KeyError: If target_column is not in df.
    """
    if target_column not in df.columns:
        raise KeyError(f"Target column {target_column!r} not found in DataFrame")

    X = df.drop(columns=[target_column])
    y = df[target_column]
    return X, y
