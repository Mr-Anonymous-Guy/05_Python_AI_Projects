"""
test_pipeline.py — End-to-end tests for the ML pipeline.

Covers:
  - Data loading and validation
  - Model training and evaluation
  - Predictions (single and batch)
  - Model persistence (save/load)
"""

import sys
import os
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.evaluate import compute_metrics
from src.predict import predict_batch, predict_single
from src.train import (
    TrainingResult,
    get_models,
    load_model,
    save_model,
    select_best_model,
    train_all_models,
    train_and_evaluate,
)
from src.utils import (
    check_missing_values,
    handle_missing_values,
    load_dataset,
    split_features_target,
    validate_dataset,
)


class TestDataLoading(unittest.TestCase):
    """Tests for data loading and validation."""

    @classmethod
    def setUpClass(cls) -> None:
        """Create a temporary CSV file for testing."""
        cls.temp_dir = tempfile.mkdtemp()
        cls.csv_path = Path(cls.temp_dir) / "test_data.csv"

        # Sample dataset
        data = {
            "study_hours": [2.5, 3.0, 1.5, 4.0, 2.0],
            "attendance": [85, 90, 70, 95, 80],
            "assignments_completed": [8, 9, 5, 10, 7],
            "previous_marks": [72, 78, 65, 85, 70],
            "marks": [75, 82, 68, 88, 73],
        }
        pd.DataFrame(data).to_csv(cls.csv_path, index=False)

    def test_load_dataset_success(self) -> None:
        df = load_dataset(self.csv_path)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 5)

    def test_load_dataset_nonexistent_raises(self) -> None:
        with self.assertRaises(FileNotFoundError):
            load_dataset(Path(self.temp_dir) / "nonexistent.csv")

    def test_validate_dataset_valid(self) -> None:
        df = load_dataset(self.csv_path)
        required = ["study_hours", "attendance", "marks"]
        is_valid, missing = validate_dataset(df, required)
        self.assertTrue(is_valid)
        self.assertEqual(missing, [])

    def test_validate_dataset_missing_columns(self) -> None:
        df = load_dataset(self.csv_path)
        required = ["study_hours", "nonexistent_column"]
        is_valid, missing = validate_dataset(df, required)
        self.assertFalse(is_valid)
        self.assertIn("nonexistent_column", missing)

    def test_check_missing_values(self) -> None:
        df = load_dataset(self.csv_path)
        missing = check_missing_values(df)
        # Should be all zeros for this dataset
        self.assertTrue(all(v == 0 for v in missing.values()))

    def test_handle_missing_values_drop(self) -> None:
        df = pd.DataFrame({"a": [1, 2, None], "b": [4, None, 6]})
        result = handle_missing_values(df, strategy="drop")
        self.assertEqual(len(result), 1)

    def test_handle_missing_values_mean(self) -> None:
        df = pd.DataFrame({"a": [1.0, 2.0, None], "b": [4.0, None, 6.0]})
        result = handle_missing_values(df, strategy="mean")
        self.assertEqual(len(result), 3)
        self.assertFalse(result.isnull().any().any())

    def test_split_features_target(self) -> None:
        df = load_dataset(self.csv_path)
        X, y = split_features_target(df, "marks")
        self.assertEqual(len(X.columns), 4)
        self.assertNotIn("marks", X.columns)
        self.assertEqual(len(y), 5)


class TestModelTraining(unittest.TestCase):
    """Tests for model training and evaluation."""

    @classmethod
    def setUpClass(cls) -> None:
        """Prepare a simple dataset for training."""
        cls.X = pd.DataFrame({
            "study_hours": np.random.uniform(1, 5, 50),
            "attendance": np.random.uniform(60, 100, 50),
            "assignments_completed": np.random.randint(4, 11, 50),
            "previous_marks": np.random.uniform(55, 95, 50),
        })
        cls.y = pd.Series(
            cls.X["study_hours"] * 5 + cls.X["attendance"] * 0.3 + np.random.normal(0, 2, 50)
        )

    def test_get_models_returns_dict(self) -> None:
        models = get_models()
        self.assertIsInstance(models, dict)
        self.assertIn("Linear Regression", models)
        self.assertIn("Decision Tree", models)
        self.assertIn("Random Forest", models)

    def test_train_and_evaluate(self) -> None:
        from sklearn.linear_model import LinearRegression
        from sklearn.model_selection import train_test_split

        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )

        model = LinearRegression()
        result = train_and_evaluate(
            X_train, X_test, y_train, y_test, "Test Model", model
        )

        self.assertIsInstance(result, TrainingResult)
        self.assertEqual(result.model_name, "Test Model")
        self.assertGreaterEqual(result.r2, 0)
        self.assertGreaterEqual(result.mae, 0)

    def test_train_all_models(self) -> None:
        results = train_all_models(self.X, self.y)
        self.assertEqual(len(results), 3)
        self.assertTrue(all(isinstance(r, TrainingResult) for r in results))

    def test_select_best_model(self) -> None:
        results = train_all_models(self.X, self.y)
        best = select_best_model(results)
        self.assertIsInstance(best, TrainingResult)
        # Best model should have the highest R²
        self.assertEqual(best.r2, max(r.r2 for r in results))

    def test_select_best_model_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            select_best_model([])


class TestModelPersistence(unittest.TestCase):
    """Tests for saving and loading models."""

    def test_save_and_load_model(self) -> None:
        from sklearn.linear_model import LinearRegression

        # Create a dummy model
        model = LinearRegression()
        X_dummy = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        y_dummy = pd.Series([7, 8, 9])
        model.fit(X_dummy, y_dummy)

        result = TrainingResult(
            model_name="Test Model",
            model=model,
            mae=1.0,
            mse=2.0,
            rmse=1.414,
            r2=0.95,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            save_path = Path(tmpdir) / "test_model.pkl"
            save_model(result, save_path)

            # Load and verify
            loaded = load_model(save_path)
            self.assertEqual(loaded.model_name, "Test Model")
            self.assertEqual(loaded.r2, 0.95)

            # Test prediction consistency
            test_X = pd.DataFrame({"a": [10], "b": [20]})
            pred_original = model.predict(test_X)
            pred_loaded = loaded.model.predict(test_X)
            np.testing.assert_array_almost_equal(pred_original, pred_loaded)

    def test_load_model_nonexistent_raises(self) -> None:
        with self.assertRaises(FileNotFoundError):
            load_model(Path("nonexistent_model.pkl"))


class TestPredictions(unittest.TestCase):
    """Tests for prediction functions."""

    @classmethod
    def setUpClass(cls) -> None:
        """Train a simple model for prediction tests."""
        from sklearn.linear_model import LinearRegression

        cls.X = pd.DataFrame({
            "study_hours": [2.5, 3.0, 4.0],
            "attendance": [85, 90, 95],
            "assignments_completed": [8, 9, 10],
            "previous_marks": [72, 78, 85],
        })
        cls.y = pd.Series([75, 82, 88])

        cls.model = LinearRegression()
        cls.model.fit(cls.X, cls.y)

    def test_predict_single(self) -> None:
        features = {
            "study_hours": 3.5,
            "attendance": 92,
            "assignments_completed": 9,
            "previous_marks": 80,
        }
        result = predict_single(self.model, features)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

    def test_predict_single_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            predict_single(self.model, {})

    def test_predict_batch(self) -> None:
        predictions = predict_batch(self.model, self.X)
        self.assertEqual(len(predictions), 3)
        self.assertTrue(all(isinstance(p, (float, np.floating)) for p in predictions))

    def test_predict_batch_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            predict_batch(self.model, pd.DataFrame())


class TestEvaluation(unittest.TestCase):
    """Tests for evaluation metrics."""

    def test_compute_metrics(self) -> None:
        y_true = np.array([75, 82, 68, 88, 73])
        y_pred = np.array([76, 81, 70, 87, 72])

        metrics = compute_metrics(y_true, y_pred)

        self.assertIn("MAE", metrics)
        self.assertIn("MSE", metrics)
        self.assertIn("RMSE", metrics)
        self.assertIn("R2", metrics)

        self.assertGreater(metrics["MAE"], 0)
        self.assertGreater(metrics["R2"], 0)

    def test_compute_metrics_perfect_prediction(self) -> None:
        y_true = np.array([75, 82, 68, 88, 73])
        y_pred = y_true.copy()

        metrics = compute_metrics(y_true, y_pred)

        self.assertAlmostEqual(metrics["MAE"], 0.0)
        self.assertAlmostEqual(metrics["MSE"], 0.0)
        self.assertAlmostEqual(metrics["RMSE"], 0.0)
        self.assertAlmostEqual(metrics["R2"], 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
