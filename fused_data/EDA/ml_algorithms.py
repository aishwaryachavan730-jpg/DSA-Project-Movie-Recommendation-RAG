
import re
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# --------------------------------------------------
# 1. PATHS
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_FILE = BASE_DIR / "fused_data" / "movie_fused_18_columns.csv"
OUTPUT_DIR = BASE_DIR / "fused_data" / "ML_Results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. LOAD DATASET
# --------------------------------------------------
df = pd.read_csv(DATA_FILE)

print("Dataset loaded successfully.")
print("Original dataset shape:", df.shape)

# --------------------------------------------------
# 3. CLEAN AND PREPARE DATA
# --------------------------------------------------
def convert_runtime(value):
    """Convert values such as '120 min' or '2h 10m' to minutes."""
    if pd.isna(value):
        return np.nan

    text = str(value).lower().strip()

    # Example: 2h 10m
    hours = re.search(r"(\d+)\s*h", text)
    minutes = re.search(r"(\d+)\s*m", text)

    if hours or minutes:
        h = int(hours.group(1)) if hours else 0
        m = int(minutes.group(1)) if minutes else 0
        return h * 60 + m

    # Example: 120
    number = re.search(r"\d+", text)
    return float(number.group()) if number else np.nan


if "runtime_minutes" not in df.columns:
    df["runtime_minutes"] = df["runtime"].apply(convert_runtime)
else:
    df["runtime_minutes"] = pd.to_numeric(
        df["runtime_minutes"], errors="coerce"
    )

numeric_features = [
    "tmdb_rating",
    "vote_count",
    "popularity",
    "runtime_minutes",
    "news_count"
]

for col in numeric_features + ["imdb_rating"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Models require a known target value.
model_df = df.dropna(subset=["imdb_rating"]).copy()

# Classification target: High >= 7, Low < 7.
model_df["rating_category"] = np.where(
    model_df["imdb_rating"] >= 7.0, "High", "Low"
)

# Do not use imdb_rating as an input feature because it
# determines both the regression target and the category.
X = model_df[numeric_features]
y_class = model_df["rating_category"]
y_reg = model_df["imdb_rating"]

# Use the same split for fair comparisons.
train_idx, test_idx = train_test_split(
    model_df.index,
    test_size=0.20,
    random_state=42,
    stratify=y_class
)

X_train, X_test = X.loc[train_idx], X.loc[test_idx]
yc_train, yc_test = y_class.loc[train_idx], y_class.loc[test_idx]
yr_train, yr_test = y_reg.loc[train_idx], y_reg.loc[test_idx]

# --------------------------------------------------
# 4. CLASSIFICATION MODELS: ALGORITHMS 1-5
# --------------------------------------------------
def classification_pipeline(model, scale=False):
    steps = [("imputer", SimpleImputer(strategy="median"))]

    if scale:
        steps.append(("scaler", StandardScaler()))

    steps.append(("model", model))
    return Pipeline(steps)


classifiers = {
    "1_Naive_Bayes": classification_pipeline(GaussianNB()),
    "2_SVM": classification_pipeline(SVC(kernel="rbf"), scale=True),
    "3_Decision_Tree": classification_pipeline(
        DecisionTreeClassifier(max_depth=4, random_state=42)
    ),
    "4_Random_Forest": classification_pipeline(
        RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight="balanced"
        )
    ),
    "5_Logistic_Regression": classification_pipeline(
        LogisticRegression(max_iter=2000), scale=True
    )
}

classification_results = []
prediction_output = pd.DataFrame({
    "movie_title": model_df.loc[test_idx, "movie_title"].values,
    "actual_rating_category": yc_test.values
})

for name, model in classifiers.items():
    model.fit(X_train, yc_train)
    predictions = model.predict(X_test)

    classification_results.append({
        "Algorithm": name,
        "Accuracy": accuracy_score(yc_test, predictions),
        "Precision": precision_score(
            yc_test, predictions, pos_label="High", zero_division=0
        ),
        "Recall": recall_score(
            yc_test, predictions, pos_label="High", zero_division=0
        ),
        "F1_Score": f1_score(
            yc_test, predictions, pos_label="High", zero_division=0
        )
    })

    prediction_output[name] = predictions
    print(f"{name} completed.")

# --------------------------------------------------
# 5. REGRESSION MODELS: ALGORITHMS 6-8
# --------------------------------------------------
regression_models = {
    # 6. Simple Linear Regression
    "6_Linear_Regression": (
        ["tmdb_rating"],
        Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("model", LinearRegression())
        ])
    ),

    # 7. Multiple Linear Regression
    "7_Multiple_Linear_Regression": (
        numeric_features,
        Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("model", LinearRegression())
        ])
    ),

    # 8. Polynomial Regression (degree 2)
    "8_Polynomial_Regression": (
        ["tmdb_rating"],
        Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("poly", PolynomialFeatures(degree=2, include_bias=False)),
            ("model", LinearRegression())
        ])
    )
}

regression_results = []
regression_predictions = pd.DataFrame({
    "movie_title": model_df.loc[test_idx, "movie_title"].values,
    "actual_imdb_rating": yr_test.values
})

for name, (features, model) in regression_models.items():
    model.fit(X_train[features], yr_train)
    predictions = model.predict(X_test[features])

    regression_results.append({
        "Algorithm": name,
        "MAE": mean_absolute_error(yr_test, predictions),
        "RMSE": np.sqrt(mean_squared_error(yr_test, predictions)),
        "R2_Score": r2_score(yr_test, predictions)
    })

    regression_predictions[name] = predictions
    print(f"{name} completed.")

# --------------------------------------------------
# 6. SAVE RESULTS
# --------------------------------------------------
classification_table = pd.DataFrame(classification_results)
regression_table = pd.DataFrame(regression_results)

classification_table.to_csv(
    OUTPUT_DIR / "classification_results.csv", index=False
)
regression_table.to_csv(
    OUTPUT_DIR / "regression_results.csv", index=False
)
prediction_output.to_csv(
    OUTPUT_DIR / "classification_predictions.csv", index=False
)
regression_predictions.to_csv(
    OUTPUT_DIR / "regression_predictions.csv", index=False
)

with pd.ExcelWriter(OUTPUT_DIR / "all_algorithm_results.xlsx") as writer:
    classification_table.to_excel(
        writer, sheet_name="Classification", index=False
    )
    regression_table.to_excel(
        writer, sheet_name="Regression", index=False
    )
    prediction_output.to_excel(
        writer, sheet_name="Class Predictions", index=False
    )
    regression_predictions.to_excel(
        writer, sheet_name="Rating Predictions", index=False
    )

print("\n--- CLASSIFICATION RESULTS ---")
print(classification_table.round(3).to_string(index=False))

print("\n--- REGRESSION RESULTS ---")
print(regression_table.round(3).to_string(index=False))

print("\nResults saved to:", OUTPUT_DIR)
