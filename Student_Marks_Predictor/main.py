"""
main.py — CLI entry point for Student Marks Predictor.

Run with:
    python main.py
"""

import sys
from pathlib import Path

# ── path setup ──────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))

from src.evaluate import compute_metrics, display_metrics
from src.predict import interactive_predict, load_predictor, predict_batch
from src.train import train_all_models, train_pipeline
from src.utils import (
    DATA_DIR,
    MODELS_DIR,
    display_dataset_info,
    handle_missing_values,
    load_dataset,
    split_features_target,
    validate_dataset,
)
from src.visualize import (
    plot_actual_vs_predicted,
    plot_correlation_heatmap,
    plot_model_comparison,
    plot_residuals,
    plot_target_distribution,
)


# ──────────────────────────────────────────────────────────────
# Banner
# ──────────────────────────────────────────────────────────────

BANNER = r"""
╔══════════════════════════════════════════════════════╗
║         📚  STUDENT MARKS PREDICTOR  📈              ║
║              Machine Learning Project                ║
╚══════════════════════════════════════════════════════╝
"""


def print_banner() -> None:
    """Display the application banner."""
    print(BANNER)


def print_menu() -> None:
    """Display the main menu."""
    print("\n" + "=" * 56)
    print("  MAIN MENU")
    print("=" * 56)
    print("  [1]  Load & Explore Dataset")
    print("  [2]  Train Models")
    print("  [3]  Predict Marks (Interactive)")
    print("  [4]  Visualizations")
    print("  [5]  Evaluate Saved Model")
    print("=" * 56)
    print("  [Q]  Quit")
    print("=" * 56)


def get_input(prompt: str) -> str:
    """Safe input wrapper."""
    try:
        return input(prompt).strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\n\n  👋  Goodbye!\n")
        sys.exit(0)


# ──────────────────────────────────────────────────────────────
# Menu actions
# ──────────────────────────────────────────────────────────────


def action_load_and_explore() -> None:
    """Load the dataset and display summary statistics."""
    print("\n" + "=" * 56)
    print("  📂  Loading Dataset...")
    print("=" * 56)

    try:
        dataset_path = DATA_DIR / "students.csv"
        df = load_dataset(dataset_path)

        # Validate columns
        required_cols = ["study_hours", "attendance", "assignments_completed", "previous_marks", "marks"]
        is_valid, missing = validate_dataset(df, required_cols)

        if not is_valid:
            print(f"\n  ⚠️  Missing columns: {missing}\n")
            return

        # Handle missing values
        df = handle_missing_values(df, strategy="mean")

        # Display info
        print(display_dataset_info(df))

        get_input("\n  Press ENTER to continue...")

    except Exception as exc:
        print(f"\n  ❌  Error loading dataset: {exc}\n")


def action_train_models() -> None:
    """Train all models and save the best one."""
    print("\n" + "=" * 56)
    print("  🚀  Training Pipeline")
    print("=" * 56)

    try:
        dataset_path = DATA_DIR / "students.csv"
        df = load_dataset(dataset_path)
        df = handle_missing_values(df, strategy="mean")

        X, y = split_features_target(df, target_column="marks")

        # Train all models and select best
        best_result = train_pipeline(X, y)

        print(f"\n  ✅  Training complete!")
        print(f"  Best Model: {best_result.model_name}")
        print(f"  R² Score: {best_result.r2:.4f}\n")

        get_input("  Press ENTER to continue...")

    except Exception as exc:
        print(f"\n  ❌  Training failed: {exc}\n")


def action_predict_interactive() -> None:
    """Interactive prediction using the saved model."""
    try:
        model_path = MODELS_DIR / "marks_predictor.pkl"
        if not model_path.exists():
            print("\n  ⚠️  No trained model found. Please train a model first (Option 2).\n")
            return

        result = load_predictor(model_path)
        feature_names = ["study_hours", "attendance", "assignments_completed", "previous_marks"]

        interactive_predict(result, feature_names)

    except Exception as exc:
        print(f"\n  ❌  Prediction failed: {exc}\n")


def action_visualizations() -> None:
    """Generate and display visualizations."""
    print("\n" + "=" * 56)
    print("  📊  Visualizations")
    print("=" * 56)

    try:
        dataset_path = DATA_DIR / "students.csv"
        df = load_dataset(dataset_path)
        df = handle_missing_values(df, strategy="mean")

        X, y = split_features_target(df, target_column="marks")

        print("\n  Select visualization:")
        print("  [1]  Correlation Heatmap")
        print("  [2]  Target Distribution")
        print("  [3]  Actual vs Predicted (requires trained model)")
        print("  [4]  Model Comparison (requires training)")
        print("  [5]  Residual Plot (requires trained model)")

        choice = get_input("\n  Choose: ")

        if choice == "1":
            plot_correlation_heatmap(df)
        elif choice == "2":
            plot_target_distribution(y)
        elif choice == "3":
            model_path = MODELS_DIR / "marks_predictor.pkl"
            if not model_path.exists():
                print("\n  ⚠️  No trained model found.\n")
                return
            result = load_predictor(model_path)
            y_pred = predict_batch(result.model, X)
            plot_actual_vs_predicted(y, y_pred, result.model_name)
        elif choice == "4":
            results = train_all_models(X, y)
            plot_model_comparison(results)
        elif choice == "5":
            model_path = MODELS_DIR / "marks_predictor.pkl"
            if not model_path.exists():
                print("\n  ⚠️  No trained model found.\n")
                return
            result = load_predictor(model_path)
            y_pred = predict_batch(result.model, X)
            plot_residuals(y, y_pred, result.model_name)
        else:
            print("  ⚠️  Invalid choice.")

    except Exception as exc:
        print(f"\n  ❌  Visualization failed: {exc}\n")


def action_evaluate_model() -> None:
    """Evaluate the saved model on the full dataset."""
    print("\n" + "=" * 56)
    print("  📈  Model Evaluation")
    print("=" * 56)

    try:
        model_path = MODELS_DIR / "marks_predictor.pkl"
        if not model_path.exists():
            print("\n  ⚠️  No trained model found. Please train a model first (Option 2).\n")
            return

        result = load_predictor(model_path)

        dataset_path = DATA_DIR / "students.csv"
        df = load_dataset(dataset_path)
        df = handle_missing_values(df, strategy="mean")

        X, y = split_features_target(df, target_column="marks")
        y_pred = predict_batch(result.model, X)

        metrics = compute_metrics(y, y_pred)
        print(display_metrics(metrics))

        print(f"\n  Model: {result.model_name}")
        print(f"  Loaded from: {model_path.resolve()}\n")

        get_input("  Press ENTER to continue...")

    except Exception as exc:
        print(f"\n  ❌  Evaluation failed: {exc}\n")


# ──────────────────────────────────────────────────────────────
# Main loop
# ──────────────────────────────────────────────────────────────


def main() -> None:
    """Application entry point."""
    while True:
        print_banner()
        print_menu()

        choice = get_input("  Choose an option: ")

        if choice == "q":
            print("\n" + "=" * 56)
            print("  👋  Thank you for using Student Marks Predictor!")
            print("=" * 56 + "\n")
            sys.exit(0)

        elif choice == "1":
            action_load_and_explore()
        elif choice == "2":
            action_train_models()
        elif choice == "3":
            action_predict_interactive()
        elif choice == "4":
            action_visualizations()
        elif choice == "5":
            action_evaluate_model()
        else:
            print("\n  ⚠️  Invalid choice. Please try again.\n")
            get_input("  Press ENTER to continue...")


if __name__ == "__main__":
    main()
