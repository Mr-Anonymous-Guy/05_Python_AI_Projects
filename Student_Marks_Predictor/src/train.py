"""
train.py — Model training pipeline with multiple algorithms.

Trains Linear Regression, Decision Tree, and Random Forest models,
then selects the best performer based on R² score and saves it to disk.
"""

import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

from src.utils import MODELS_DIR


# ──────────────────────────────────────────────────────────────
# Training result container
# ──────────────────────────────────────────────────────────────


@dataclass
class TrainingResult:
    """
    Encapsulates the result of training a single model.

    Attributes:
        model_name:  Human-readable model name.
        model:       The fitted scikit-learn estimator.
        mae:         Mean Absolute Error on test set.
        mse:         Mean Squared Error on test set.
        rmse:        Root Mean Squared Error on test set.
        r2:          R² (coefficient of determination) on test set.
    """

    model_name: str
    model: Any
    mae: float
    mse: float
    rmse: float
    r2: float

    def summary(self) -> str:
        """Return a formatted summary string."""
        return (
            f"\n  {self.model_name}\n"
            f"  {'─' * 40}\n"
            f"  MAE   : {self.mae:.4f}\n"
            f"  MSE   : {self.mse:.4f}\n"
            f"  RMSE  : {self.rmse:.4f}\n"
            f"  R²    : {self.r2:.4f}\n"
        )


# ──────────────────────────────────────────────────────────────
# Model factory
# ──────────────────────────────────────────────────────────────


def get_models() -> dict[str, Any]:
    """
    Return a dictionary of model name → instantiated estimator.

    Returns:
        Dictionary with keys "Linear Regression", "Decision Tree",
        and "Random Forest".
    """
    return {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(random_state=42, max_depth=10),
        "Random Forest": RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=10,
            n_jobs=-1,
        ),
    }


# ──────────────────────────────────────────────────────────────
# Training and evaluation
# ──────────────────────────────────────────────────────────────


def train_and_evaluate(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    model_name: str,
    model: Any,
) -> TrainingResult:
    """
    Train a single model and compute test-set metrics.

    Args:
        X_train: Training features.
        X_test:  Test features.
        y_train: Training target.
        y_test:  Test target.
        model_name: Display name for the model.
        model:   Instantiated scikit-learn estimator.

    Returns:
        TrainingResult with computed metrics.
    """
    # Fit
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Evaluate
    mae  = mean_absolute_error(y_test, y_pred)
    mse  = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    r2   = r2_score(y_test, y_pred)

    return TrainingResult(
        model_name=model_name,
        model=model,
        mae=mae,
        mse=mse,
        rmse=rmse,
        r2=r2,
    )


def train_all_models(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42,
) -> list[TrainingResult]:
    """
    Train all available models and return their results.

    Args:
        X: Feature DataFrame.
        y: Target Series.
        test_size: Fraction of data to reserve for testing.
        random_state: RNG seed for reproducibility.

    Returns:
        List of TrainingResult objects (one per model).
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    models = get_models()
    results: list[TrainingResult] = []

    for name, model in models.items():
        result = train_and_evaluate(
            X_train, X_test, y_train, y_test, name, model
        )
        results.append(result)

    return results


def select_best_model(results: list[TrainingResult]) -> TrainingResult:
    """
    Pick the model with the highest R² score.

    Args:
        results: List of TrainingResult objects.

    Returns:
        The TrainingResult with maximum R².

    Raises:
        ValueError: If results is empty.
    """
    if not results:
        raise ValueError("No training results to select from.")
    return max(results, key=lambda r: r.r2)


# ──────────────────────────────────────────────────────────────
# Model persistence
# ──────────────────────────────────────────────────────────────


def save_model(
    result: TrainingResult,
    filepath: Path | str,
) -> None:
    """
    Serialize a trained model and its metadata to disk.

    Args:
        result: TrainingResult containing the fitted model.
        filepath: Destination file path.

    Raises:
        OSError: If the file cannot be written.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "model_name": result.model_name,
        "model": result.model,
        "mae": result.mae,
        "mse": result.mse,
        "rmse": result.rmse,
        "r2": result.r2,
    }
    with path.open("wb") as f:
        pickle.dump(payload, f)


def load_model(filepath: Path | str) -> TrainingResult:
    """
    Load a serialized model from disk.

    Args:
        filepath: Path to the saved model file.

    Returns:
        Reconstructed TrainingResult.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        pickle.UnpicklingError: If the file is corrupt.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Model file not found: {path}")

    with path.open("rb") as f:
        payload = pickle.load(f)

    return TrainingResult(
        model_name=payload["model_name"],
        model=payload["model"],
        mae=payload["mae"],
        mse=payload["mse"],
        rmse=payload["rmse"],
        r2=payload["r2"],
    )


# ──────────────────────────────────────────────────────────────
# High-level pipeline
# ──────────────────────────────────────────────────────────────


def train_pipeline(
    X: pd.DataFrame,
    y: pd.Series,
    save_path: Path | str = MODELS_DIR / "marks_predictor.pkl",
) -> TrainingResult:
    """
    Full training pipeline: train all models, select best, and save.

    Args:
        X: Feature DataFrame.
        y: Target Series.
        save_path: Where to save the best model.

    Returns:
        The TrainingResult of the best model.
    """
    print("\n" + "=" * 56)
    print("  🤖  Training Models...")
    print("=" * 56)

    results = train_all_models(X, y)

    print("\n  📈  Model Performance:\n")
    for result in results:
        print(result.summary())

    best = select_best_model(results)
    print("=" * 56)
    print(f"  🏆  Best Model: {best.model_name}  (R² = {best.r2:.4f})")
    print("=" * 56)

    save_model(best, save_path)
    print(f"\n  💾  Model saved to: {Path(save_path).resolve()}\n")

    return best
