
from pathlib import Path
import re

import numpy as np
import pandas as pd

from sklearn.model_selection import StratifiedKFold, KFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score

# 1. Paths and dataset
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "fused_data" / "movie_fused_18_columns.csv"
OUTPUT_DIR = BASE_DIR / "fused_data" / "ML_Results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE)

numeric_features = [
    "tmdb_rating",
    "vote_count",
    "popularity",
    "runtime_minutes",
    "news_count",
]

# Create runtime_minutes if it is missing
if "runtime_minutes" not in df.columns:
    def convert_runtime(value):
        if pd.isna(value):
            return np.nan
        text = str(value).lower().strip()
        hours = re.search(r"(\d+)\s*h", text)
        minutes = re.search(r"(\d+)\s*m", text)

        if hours or minutes:
            h = int(hours.group(1)) if hours else 0
            m = int(minutes.group(1)) if minutes else 0
            return h * 60 + m

        number = re.search(r"\d+", text)
        return float(number.group()) if number else np.nan

    df["runtime_minutes"] = df["runtime"].apply(convert_runtime)

for col in numeric_features + ["imdb_rating"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

data = df.dropna(subset=["imdb_rating"]).copy()
X = data[numeric_features]
y_reg = data["imdb_rating"]
y_class = np.where(y_reg >= 7.0, "High", "Low")

print("Movies evaluated:", len(data))
print("Rating classes:", pd.Series(y_class).value_counts().to_dict())

# 2. Classification models
def classification_pipeline(model, scale=False):
    steps = [("imputer", SimpleImputer(strategy="median"))]
    if scale:
        steps.append(("scaler", StandardScaler()))
    steps.append(("model", model))
    return Pipeline(steps)

classifiers = {
    "Naive Bayes": classification_pipeline(GaussianNB()),
    "SVM": classification_pipeline(SVC(kernel="rbf"), scale=True),
    "Decision Tree": classification_pipeline(
        DecisionTreeClassifier(max_depth=4, random_state=42)
    ),
    "Random Forest": classification_pipeline(
        RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight="balanced",
        )
    ),
    "Logistic Regression": classification_pipeline(
        LogisticRegression(max_iter=2000), scale=True
    ),
}

classification_cv = StratifiedKFold(
    n_splits=5, shuffle=True, random_state=42
)

# "High" is the positive class
scoring = {
    "accuracy": "accuracy",
    "precision": make_scorer(
        precision_score, pos_label="High", zero_division=0
    ),
    "recall": make_scorer(
        recall_score, pos_label="High", zero_division=0
    ),
    "f1": make_scorer(
        f1_score, pos_label="High", zero_division=0
    ),
}

classification_rows = []

for name, model in classifiers.items():
    scores = cross_validate(
        model,
        X,
        y_class,
        cv=classification_cv,
        scoring=scoring,
        n_jobs=-1,
        error_score="raise",
    )

    classification_rows.append({
        "Algorithm": name,
        "Accuracy_Mean": scores["test_accuracy"].mean(),
        "Accuracy_SD": scores["test_accuracy"].std(),
        "Precision_Mean": scores["test_precision"].mean(),
        "Recall_Mean": scores["test_recall"].mean(),
        "F1_Mean": scores["test_f1"].mean(),
    })

classification_results = pd.DataFrame(classification_rows)

# 3. Regression models
regression_models = {
    "Linear Regression": (
        ["tmdb_rating"],
        Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("model", LinearRegression()),
        ]),
    ),
    "Multiple Linear Regression": (
        numeric_features,
        Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("model", LinearRegression()),
        ]),
    ),
    "Polynomial Regression": (
        ["tmdb_rating"],
        Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("poly", PolynomialFeatures(degree=2, include_bias=False)),
            ("model", LinearRegression()),
        ]),
    ),
}

regression_cv = KFold(n_splits=5, shuffle=True, random_state=42)
regression_rows = []

for name, (features, model) in regression_models.items():
    scores = cross_validate(
        model,
        X[features],
        y_reg,
        cv=regression_cv,
        scoring={
            "mae": "neg_mean_absolute_error",
            "mse": "neg_mean_squared_error",
            "r2": "r2",
        },
        n_jobs=-1,
        error_score="raise",
    )

    mae = -scores["test_mae"]
    rmse = np.sqrt(-scores["test_mse"])

    regression_rows.append({
        "Algorithm": name,
        "MAE_Mean": mae.mean(),
        "MAE_SD": mae.std(),
        "RMSE_Mean": rmse.mean(),
        "RMSE_SD": rmse.std(),
        "R2_Mean": scores["test_r2"].mean(),
        "R2_SD": scores["test_r2"].std(),
    })

regression_results = pd.DataFrame(regression_rows)

# 4. Save new results without overwriting original ML result files
classification_file = OUTPUT_DIR / "classification_cross_validation.csv"
regression_file = OUTPUT_DIR / "regression_cross_validation.csv"
excel_file = OUTPUT_DIR / "cross_validation_results.xlsx"

classification_results.to_csv(classification_file, index=False)
regression_results.to_csv(regression_file, index=False)

with pd.ExcelWriter(excel_file) as writer:
    classification_results.to_excel(
        writer, sheet_name="Classification CV", index=False
    )
    regression_results.to_excel(
        writer, sheet_name="Regression CV", index=False
    )

print("\n--- CLASSIFICATION: 5-FOLD CROSS-VALIDATION ---")
print(classification_results.round(3).to_string(index=False))

print("\n--- REGRESSION: 5-FOLD CROSS-VALIDATION ---")
print(regression_results.round(3).to_string(index=False))

print("\nNew results saved in:", OUTPUT_DIR)
print("Existing result files were not overwritten.")
