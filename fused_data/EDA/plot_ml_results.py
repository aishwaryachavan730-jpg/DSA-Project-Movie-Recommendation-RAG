
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[2]
RESULTS = BASE_DIR / "fused_data" / "ML_Results"
CHARTS = RESULTS / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

# Graph 1: Classification accuracy
classification = pd.read_csv(
    RESULTS / "classification_results.csv"
)
classification = classification.sort_values("Accuracy", ascending=False)

plt.figure(figsize=(10, 6))
plt.bar(classification["Algorithm"], classification["Accuracy"])
plt.title("Comparison of Classification Algorithms")
plt.xlabel("Algorithm")
plt.ylabel("Accuracy")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(CHARTS / "classification_accuracy.png", dpi=300)
plt.close()

# Graph 2: Regression MAE
regression = pd.read_csv(RESULTS / "regression_results.csv")
regression = regression.sort_values("MAE")

plt.figure(figsize=(9, 5))
plt.bar(regression["Algorithm"], regression["MAE"])
plt.title("Regression Models - Mean Absolute Error")
plt.xlabel("Algorithm")
plt.ylabel("MAE (IMDb rating points)")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(CHARTS / "regression_mae.png", dpi=300)
plt.close()

# Graph 3: Regression R-squared
plt.figure(figsize=(9, 5))
plt.bar(regression["Algorithm"], regression["R2_Score"])
plt.axhline(0, linewidth=1)
plt.title("Regression Models - R² Score")
plt.xlabel("Algorithm")
plt.ylabel("R² Score")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(CHARTS / "regression_r2.png", dpi=300)
plt.close()

print("Graphs saved in:", CHARTS)
