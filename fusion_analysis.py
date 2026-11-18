
import pandas as pd
import os

# Load the fused dataset
file_path = "fused_data/movie_fused_18_columns.csv"
df = pd.read_csv(file_path)

# Create output folder
output_dir = "fused_data/analysis"
os.makedirs(output_dir, exist_ok=True)

# Calculate missing values
missing = pd.DataFrame({
    "Column": df.columns,
    "Missing_Count": df.isnull().sum().values,
    "Missing_Percentage": (
        df.isnull().mean().values * 100
    ).round(2)
})

# Count duplicate movie titles
duplicates = df.duplicated(
    subset=["movie_title"]
).sum()

# Display data-quality information
print("=" * 50)
print("MOVIEVERSE AI - DATA QUALITY ANALYSIS")
print("=" * 50)

print("\nDataset shape:", df.shape)

print("\nMissing value report:")
print(missing.to_string(index=False))

print("\nDuplicate movie titles:", duplicates)

print("\nNumerical summary:")
print(df.describe().round(2).to_string())

# Save missing-value report
missing.to_csv(
    f"{output_dir}/missing_values_report.csv",
    index=False
)

# Save numerical summary
df.describe().round(2).to_csv(
    f"{output_dir}/numerical_summary.csv"
)

print("\nReports saved successfully in:", output_dir)