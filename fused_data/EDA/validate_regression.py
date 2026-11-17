
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE_DIR = Path(__file__).resolve().parents[2]
RESULTS_DIR = BASE_DIR / "fused_data" / "ML_Results"

file_path = RESULTS_DIR / "regression_predictions.csv"
df = pd.read_csv(file_path)

actual = df["actual_imdb_rating"]

models = [
    "6_Linear_Regression",
    "7_Multiple_Linear_Regression",
    "8_Polynomial_Regression"
]

for name in models:
    if name not in df.columns:
        print(f"\nSkipping missing model: {name}")
        continue

    predicted = df[name]

    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    r2 = r2_score(actual, predicted)

    print("\n" + "=" * 45)
    print("MODEL:", name)
    print("=" * 45)
    print(f"MAE:  {mae:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print(f"R2 Score: {r2:.3f}")

    comparison = pd.DataFrame({
        "Movie": df["movie_title"],
        "Actual IMDb Rating": actual,
        "Predicted IMDb Rating": predicted,
        "Absolute Error": abs(actual - predicted)
    })

    print("\nSample predictions:")
    print(comparison.head(5).round(3).to_string(index=False))

print("\nRegression validation completed.")
