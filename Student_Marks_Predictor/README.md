# 📚 Student Marks Predictor 📈

A production-grade machine learning system for predicting student exam marks using scikit-learn.  
Part of the **05_Python_AI_Projects** repository — the first ML engineering project.

---

## What You'll Learn

| Concept | Implementation |
|---|---|
| Data Processing | pandas DataFrames, missing-value handling, train/test splits |
| Machine Learning | Linear Regression, Decision Trees, Random Forest |
| Regression Metrics | MAE, MSE, RMSE, R² scoring |
| Model Persistence | pickle serialization for production deployment |
| Visualization | matplotlib + seaborn: heatmaps, scatter plots, residuals |
| Modular ML Design | Separation of train/predict/evaluate/visualize |

---

## Features

### Dataset Management
- **Load CSV** — pandas-based data ingestion with validation
- **Missing values** — drop or impute (mean-fill for numeric columns)
- **Statistics** — `.describe()`, correlation matrix, column dtypes

### Machine Learning
Three regression algorithms trained and compared automatically:

| Model | Hyperparameters |
|---|---|
| Linear Regression | Default (OLS) |
| Decision Tree | `max_depth=10`, `random_state=42` |
| Random Forest | `n_estimators=100`, `max_depth=10`, `n_jobs=-1` |

The **best model** (highest R²) is automatically selected and saved.

### Evaluation Metrics
- **MAE** — Mean Absolute Error (average prediction error in marks)
- **MSE** — Mean Squared Error (penalizes large errors)
- **RMSE** — Root MSE (in same units as target)
- **R²** — Coefficient of determination (0 = baseline, 1 = perfect)

### Predictions
- **Interactive mode** — CLI prompts for student features
- **Batch mode** — predict from CSV or DataFrame

### Visualizations
Publication-quality charts using matplotlib + seaborn:

1. **Correlation Heatmap** — feature relationships
2. **Actual vs Predicted** — scatter with diagonal reference line
3. **Model Comparison** — R² bar chart across all models
4. **Residual Plot** — error distribution analysis
5. **Target Distribution** — histogram + KDE of marks

---

## Project Structure

```
Student_Marks_Predictor/
├── data/
│   └── students.csv         # Sample dataset (100 rows, 5 features)
│
├── models/
│   └── marks_predictor.pkl  # Saved best model (auto-generated)
│
├── src/
│   ├── __init__.py
│   ├── utils.py             # Data loading, validation, preprocessing
│   ├── train.py             # Training pipeline + model persistence
│   ├── predict.py           # Inference engine (single + batch)
│   ├── evaluate.py          # Metrics computation and reporting
│   └── visualize.py         # All matplotlib/seaborn charts
│
├── tests/
│   ├── __init__.py
│   └── test_pipeline.py     # 30+ unit tests
│
├── main.py                  # Interactive CLI application
├── requirements.txt
├── run.sh                   # Linux / macOS launcher
├── run.bat                  # Windows launcher
├── .gitignore
└── README.md
```

---

## Quick Start

### Prerequisites
- Python **3.8+**
- pip (Python package manager)

### Install dependencies

```bash
pip install -r requirements.txt
```

Core packages:
- `numpy` — numerical computing
- `pandas` — data manipulation
- `scikit-learn` — ML algorithms and metrics
- `matplotlib` + `seaborn` — visualization

### Run the app

**Linux / macOS**
```bash
chmod +x run.sh
./run.sh
```

**Windows**
```bat
run.bat
```

**Direct**
```bash
python main.py
```

---

## Usage Guide

### 1. Load & Explore Dataset

Displays:
- Row/column counts
- Memory usage
- Column dtypes and missing-value counts
- Statistical summary (`.describe()`)

### 2. Train Models

Trains all three models, compares their performance, saves the best:

```
🤖  Training Models...

  Linear Regression
  ────────────────────────────────────────
  MAE   : 1.2345
  MSE   : 2.4567
  RMSE  : 1.5674
  R²    : 0.9876

  Decision Tree
  ────────────────────────────────────────
  MAE   : 1.3456
  MSE   : 2.6789
  RMSE  : 1.6367
  R²    : 0.9850

  Random Forest
  ────────────────────────────────────────
  MAE   : 1.1234
  MSE   : 2.2345
  RMSE  : 1.4948
  R²    : 0.9890

🏆  Best Model: Random Forest  (R² = 0.9890)
💾  Model saved to: models/marks_predictor.pkl
```

### 3. Predict Marks (Interactive)

Prompts for:
- `study_hours` (hours spent studying per day)
- `attendance` (% attendance)
- `assignments_completed` (number completed)
- `previous_marks` (marks from previous exam)

Returns predicted marks with model confidence (R²).

### 4. Visualizations

**Correlation Heatmap**
Shows relationships between all numeric features.

**Actual vs Predicted**
Scatter plot with diagonal reference line — points on the line = perfect predictions.

**Model Comparison**
Bar chart of R² scores for all three models.

**Residual Plot**
Plots prediction errors against predicted values — helps detect bias.

**Target Distribution**
Histogram + KDE curve showing the distribution of student marks.

### 5. Evaluate Saved Model

Loads the saved model and computes metrics on the full dataset.

---

## Running Tests

```bash
# pytest (recommended)
pip install pytest
python -m pytest tests/ -v

# Built-in unittest — zero dependencies
python -m unittest discover tests/ -v
```

Expected output:
```
test_check_missing_values                  PASSED
test_compute_metrics                       PASSED
test_compute_metrics_perfect_prediction    PASSED
test_get_models_returns_dict               PASSED
test_handle_missing_values_drop            PASSED
test_handle_missing_values_mean            PASSED
test_load_dataset_nonexistent_raises       PASSED
test_load_dataset_success                  PASSED
test_load_model_nonexistent_raises         PASSED
test_predict_batch                         PASSED
test_predict_batch_empty_raises            PASSED
test_predict_single                        PASSED
test_predict_single_empty_raises           PASSED
test_save_and_load_model                   PASSED
test_select_best_model                     PASSED
test_select_best_model_empty_raises        PASSED
test_split_features_target                 PASSED
test_train_all_models                      PASSED
test_train_and_evaluate                    PASSED
test_validate_dataset_missing_columns      PASSED
test_validate_dataset_valid                PASSED

21 passed
```

---

## Sample Dataset

**`data/students.csv`** contains 100 synthetic student records:

| Feature | Description | Range |
|---|---|---|
| `study_hours` | Daily study hours | 1.0 – 5.0 |
| `attendance` | Attendance percentage | 60 – 100 |
| `assignments_completed` | Number of assignments | 4 – 10 |
| `previous_marks` | Marks from previous exam | 55 – 95 |
| **`marks`** | **Target variable** | 60 – 96 |

The dataset is synthetically generated with a strong linear relationship, ensuring high R² scores for pedagogical clarity.

---

## Architecture Notes

### Module responsibilities

| Module | Purpose |
|---|---|
| `utils.py` | Pure data I/O — no ML logic |
| `train.py` | Training loop, model selection, persistence |
| `predict.py` | Inference only — no training code |
| `evaluate.py` | Metrics computation — reusable across train/test |
| `visualize.py` | All matplotlib/seaborn code isolated here |
| `main.py` | Orchestration — menu-driven CLI |

### Why three models?

- **Linear Regression** — baseline; assumes linear relationships
- **Decision Tree** — captures non-linear patterns; prone to overfitting
- **Random Forest** — ensemble of trees; usually best out-of-the-box

The pipeline trains all three and picks the winner based on **R² score** (proportion of variance explained).

### Model persistence

The trained model is serialized to `models/marks_predictor.pkl` using Python's `pickle` module. This allows:
- **Deployment** — load the model in production without retraining
- **Reproducibility** — same predictions on same input
- **Metadata** — model name, metrics, and hyperparameters stored together

---

## Example Terminal Output

```
╔══════════════════════════════════════════════════════╗
║         📚  STUDENT MARKS PREDICTOR  📈              ║
║              Machine Learning Project                ║
╚══════════════════════════════════════════════════════╝

========================================================
  MAIN MENU
========================================================
  [1]  Load & Explore Dataset
  [2]  Train Models
  [3]  Predict Marks (Interactive)
  [4]  Visualizations
  [5]  Evaluate Saved Model
========================================================
  [Q]  Quit
========================================================
  Choose an option: 3

========================================================
  🔮  Predict Student Marks — Random Forest
========================================================
  Enter study_hours: 3.5
  Enter attendance: 92
  Enter assignments_completed: 9
  Enter previous_marks: 80

────────────────────────────────────────────────────────
  📊  Predicted Marks: 84.23
────────────────────────────────────────────────────────

  Model: Random Forest
  R² Score: 0.9890
========================================================
```

---

## Extending the Project

### Add more features
Edit `students.csv` to include columns like:
- `sleep_hours`
- `extracurricular_hours`
- `socioeconomic_score`

The pipeline will automatically use all features except `marks`.

### Try other algorithms
In `train.py`, add to the `get_models()` dictionary:
```python
from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor

"SVR": SVR(),
"Gradient Boosting": GradientBoostingRegressor(),
```

### Hyperparameter tuning
Replace manual params with `GridSearchCV`:
```python
from sklearn.model_selection import GridSearchCV

param_grid = {"n_estimators": [50, 100, 200], "max_depth": [5, 10, 15]}
grid = GridSearchCV(RandomForestRegressor(), param_grid, cv=5)
grid.fit(X_train, y_train)
best_model = grid.best_estimator_
```

---

## License

MIT — free to use, modify, and learn from.
