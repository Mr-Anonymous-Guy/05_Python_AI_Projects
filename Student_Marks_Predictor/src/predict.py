"""
predict.py — Inference engine for trained models.

Loads a saved model and uses it to predict student marks from
either interactive input or batch data (DataFrame / CSV).
"""

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.train import TrainingResult, load_model
from src.utils import MODELS_DIR


# ──────────────────────────────────────────────────────────────
# Model loading helper
# ──────────────────────────────────────────────────────────────


def load_predictor(
    model_path: Path | str = MODELS_DIR / "marks_predictor.pkl",
) -> TrainingResult:
    """
    Load the saved model from disk.

    Args:
        model_path: Path to the serialized model file.

    Returns:
        TrainingResult with the trained model.

    Raises:
        FileNotFoundError: If the model file doesn't exist.
    """
    return load_model(model_path)


# ──────────────────────────────────────────────────────────────
# Single prediction
# ──────────────────────────────────────────────────────────────


def predict_single(
    model: Any,
    features: dict[str, float],
) -> float:
    """
    Predict marks for a single student.

    Args:
        model: Fitted scikit-learn estimator.
        features: Dictionary mapping feature names to values.

    Returns:
        Predicted marks (float).

    Raises:
        ValueError: If features dictionary is empty or malformed.
    """
    if not features:
        raise ValueError("Features dictionary cannot be empty.")

    # Convert dict to DataFrame (single row)
    df = pd.DataFrame([features])

    # Predict
    prediction = model.predict(df)
    return float(prediction[0])


# ──────────────────────────────────────────────────────────────
# Batch prediction
# ──────────────────────────────────────────────────────────────


def predict_batch(
    model: Any,
    X: pd.DataFrame,
) -> np.ndarray:
    """
    Predict marks for multiple students.

    Args:
        model: Fitted scikit-learn estimator.
        X: Feature DataFrame (one row per student).

    Returns:
        Array of predicted marks.

    Raises:
        ValueError: If X is empty.
    """
    if X.empty:
        raise ValueError("Input DataFrame cannot be empty.")

    return model.predict(X)


# ──────────────────────────────────────────────────────────────
# Interactive prediction CLI
# ──────────────────────────────────────────────────────────────


def interactive_predict(
    result: TrainingResult,
    feature_names: list[str],
) -> None:
    """
    Prompt the user for feature values and display the prediction.

    Args:
        result: TrainingResult with the loaded model.
        feature_names: List of feature column names to prompt for.
    """
    print("\n" + "=" * 56)
    print(f"  🔮  Predict Student Marks — {result.model_name}")
    print("=" * 56)

    features: dict[str, float] = {}
    for name in feature_names:
        while True:
            try:
                value = float(input(f"  Enter {name}: "))
                features[name] = value
                break
            except ValueError:
                print(f"  ⚠️  Invalid input. Please enter a number.")
            except (EOFError, KeyboardInterrupt):
                print("\n\n  Cancelled.\n")
                return

    try:
        predicted_marks = predict_single(result.model, features)
        print("\n" + "─" * 56)
        print(f"  📊  Predicted Marks: {predicted_marks:.2f}")
        print("─" * 56)
        print(f"\n  Model: {result.model_name}")
        print(f"  R² Score: {result.r2:.4f}")
        print("=" * 56 + "\n")
    except Exception as exc:
        print(f"\n  ❌  Prediction failed: {exc}\n")
