
from pathlib import Path
import pandas as pd
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    balanced_accuracy_score
)

BASE_DIR = Path(__file__).resolve().parents[2]
RESULTS_DIR = BASE_DIR / "fused_data" / "ML_Results"

file_path = RESULTS_DIR / "classification_predictions.csv"
df = pd.read_csv(file_path)

actual = df["actual_rating_category"]

models = [
    "1_Naive_Bayes",
    "2_SVM",
    "3_Decision_Tree",
    "4_Random_Forest",
    "5_Logistic_Regression"
]

for model_name in models:
    if model_name not in df.columns:
        print(f"\nSkipping missing model: {model_name}")
        continue

    predicted = df[model_name]

    print("\n" + "=" * 55)
    print("MODEL:", model_name)
    print("=" * 55)

    print("\nConfusion Matrix (rows = actual, columns = predicted):")
    print(pd.DataFrame(
        confusion_matrix(
            actual, predicted, labels=["Low", "High"]
        ),
        index=["Actual Low", "Actual High"],
        columns=["Predicted Low", "Predicted High"]
    ))

    print("\nClassification Report:")
    print(classification_report(
        actual,
        predicted,
        labels=["Low", "High"],
        zero_division=0,
        digits=3
    ))

    print(
        "Balanced Accuracy:",
        round(balanced_accuracy_score(actual, predicted), 3)
    )

print("\nValidation completed.")
