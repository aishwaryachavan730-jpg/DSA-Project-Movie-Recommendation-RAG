import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ============================================================
# PART A - LOAD AND INSPECT FUSED DATASET
# ============================================================

FILE_PATH = r"E:\LLM Project\MAJOR Project\Movie-Recommendation-RAG\fused_data\movie_fused_18_columns.csv"

# Create output folders
CHART_DIR = r"E:\LLM Project\MAJOR Project\Movie-Recommendation-RAG\fused_data\EDA\charts"
RESULT_DIR = r"E:\LLM Project\MAJOR Project\Movie-Recommendation-RAG\fused_data\EDA\results"

os.makedirs(CHART_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

# Load dataset
df = pd.read_csv(FILE_PATH)

print("=" * 70)
print("NEW FUSED MOVIE DATASET - EDA")
print("=" * 70)

# Dataset shape
print("\n1. Dataset Shape:")
print(df.shape)

# Columns
print("\n2. Columns:")
for i, col in enumerate(df.columns, 1):
    print(f"{i}. {col}")

# First five rows
print("\n3. First 5 Rows:")
print(df.head())

# Data types
print("\n4. Data Types:")
print(df.dtypes)

# Missing values
print("\n5. Missing Values:")
print(df.isnull().sum())

# Duplicate records
print("\n6. Duplicate Records:")
print(df.duplicated().sum())

# ============================================================
# DATA CLEANING FOR EDA
# ============================================================

# Convert release_date to datetime
df["release_date"] = pd.to_datetime(
    df["release_date"],
    errors="coerce"
)

# Extract release year
df["release_year"] = df["release_date"].dt.year

print("\nRelease Year:")
print(df["release_year"].head())

import re

# ============================================================
# STEP A2 - CONVERT RUNTIME INTO MINUTES
# ============================================================

def convert_runtime(value):

    if pd.isna(value):
        return np.nan

    value = str(value).strip().lower()

    # Example: 135 minutes
    match = re.search(r"(\d+(?:\.\d+)?)\s*minutes?", value)
    if match:
        return float(match.group(1))

    # Example: 135 min
    match = re.search(r"(\d+(?:\.\d+)?)\s*min", value)
    if match:
        return float(match.group(1))

    # Example: 2h 15m
    match = re.search(r"(\d+)\s*h(?:ours?)?\s*(\d+)?\s*m?", value)

    if match:
        hours = float(match.group(1))
        minutes = float(match.group(2)) if match.group(2) else 0

        return hours * 60 + minutes

    # Example: 2h
    match = re.search(r"(\d+(?:\.\d+)?)\s*h(?:ours?)?", value)

    if match:
        return float(match.group(1)) * 60

    # Example: 135
    match = re.fullmatch(r"\d+(?:\.\d+)?", value)

    if match:
        return float(value)

    return np.nan


df["runtime_minutes"] = df["runtime"].apply(convert_runtime)

print("\nRuntime Conversion:")
print(df[["runtime", "runtime_minutes"]].head(20))

numeric_columns = [
    "tmdb_rating",
    "vote_count",
    "popularity",
    "imdb_rating",
    "runtime_minutes",
    "news_count",
    "release_year"
]

print("\n" + "=" * 70)
print("NUMERICAL VARIABLES FOR EDA")
print("=" * 70)

print(numeric_columns)

print("\nNumerical Data:")
print(df[numeric_columns].head())

# ============================================================
# PART B - UNIVARIATE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("PART B - UNIVARIATE ANALYSIS")
print("=" * 70)

statistics = df[numeric_columns].describe().T

print("\nDESCRIPTIVE STATISTICS:")
print(statistics)

# Save results
statistics.to_csv(
    os.path.join(
        RESULT_DIR,
        "descriptive_statistics.csv"
    )
)

print("\nDescriptive statistics saved.")

# ============================================================
# PART B - HISTOGRAMS
# ============================================================

print("\n" + "=" * 70)
print("GENERATING HISTOGRAMS")
print("=" * 70)

for column in numeric_columns:

    plt.figure(figsize=(8, 5))

    sns.histplot(
        data=df,
        x=column,
        bins=15,
        kde=True
    )

    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Number of Movies")

    plt.tight_layout()

    # Save histogram
    output_path = os.path.join(
        CHART_DIR,
        f"{column}_histogram.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    print(f"Saved: {output_path}")

    plt.show()
    plt.close()

print("\nAll histograms generated successfully.")

# ============================================================
# PART B - BOXPLOTS
# ============================================================

print("\n" + "=" * 70)
print("GENERATING BOXPLOTS")
print("=" * 70)

for column in numeric_columns:

    # Create figure
    plt.figure(figsize=(8, 5))

    # Create boxplot
    sns.boxplot(
        x=df[column].dropna()
    )

    # Title and labels
    plt.title(f"Boxplot of {column}")
    plt.xlabel(column)

    # Adjust layout
    plt.tight_layout()

    # Output file path
    output_path = os.path.join(
        CHART_DIR,
        f"{column}_boxplot.png"
    )

    # Save image
    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    print(f"Saved: {output_path}")

    # Display
    plt.show()

    # Close figure
    plt.close()

print("\nAll 7 boxplots generated successfully.")

# ============================================================
# PART B - TOP 10 GENRES BAR CHART
# ============================================================

print("\n" + "=" * 70)
print("GENERATING TOP 10 GENRES BAR CHART")
print("=" * 70)

# Get genre values
genre_series = (
    df["genres"]
    .dropna()
    .astype(str)
    .str.split(",")
    .explode()
    .str.strip()
)

# Count each genre
genre_counts = genre_series.value_counts().head(10)

print("\nTop 10 Genres:")
print(genre_counts)

# Create bar chart
plt.figure(figsize=(10, 6))

genre_counts.plot(kind="bar")

plt.title("Top 10 Movie Genres in Fused Dataset")
plt.xlabel("Genre")
plt.ylabel("Number of Movies")

plt.xticks(rotation=45, ha="right")

plt.tight_layout()

# Save chart
output_path = os.path.join(
    CHART_DIR,
    "top_10_genres.png"
)

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

print(f"\nSaved: {output_path}")

# Display chart
plt.show()

plt.close()

print("\nTop 10 genres bar chart generated successfully.")

# ============================================================
# PART C - BIVARIATE ANALYSIS
# C1. TMDB RATING VS IMDb RATING
# ============================================================

print("\n" + "=" * 70)
print("PART C - BIVARIATE ANALYSIS")
print("=" * 70)

print("\nGenerating TMDB Rating vs IMDb Rating...")

# Remove missing IMDb ratings
rating_data = df[
    ["tmdb_rating", "imdb_rating"]
].dropna()

plt.figure(figsize=(8, 6))

sns.scatterplot(
    data=rating_data,
    x="tmdb_rating",
    y="imdb_rating",
    s=70
)

plt.title("TMDB Rating vs IMDb Rating")
plt.xlabel("TMDB Rating")
plt.ylabel("IMDb Rating")

plt.tight_layout()

output_path = os.path.join(
    CHART_DIR,
    "tmdb_vs_imdb_rating.png"
)

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

print(f"Saved: {output_path}")

plt.show()
plt.close()

# ============================================================
# C2. TMDB RATING VS VOTE COUNT
# ============================================================

print("\nGenerating TMDB Rating vs Vote Count...")

vote_data = df[
    ["tmdb_rating", "vote_count"]
].dropna()

plt.figure(figsize=(8, 6))

sns.scatterplot(
    data=vote_data,
    x="vote_count",
    y="tmdb_rating",
    s=70
)

plt.title("TMDB Rating vs Vote Count")
plt.xlabel("Vote Count")
plt.ylabel("TMDB Rating")

plt.tight_layout()

output_path = os.path.join(
    CHART_DIR,
    "tmdb_rating_vs_vote_count.png"
)

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

print(f"Saved: {output_path}")

plt.show()
plt.close()

# ============================================================
# C3. POPULARITY VS TMDB RATING
# ============================================================

print("\nGenerating Popularity vs TMDB Rating...")

popularity_data = df[
    ["popularity", "tmdb_rating"]
].dropna()

plt.figure(figsize=(8, 6))

sns.scatterplot(
    data=popularity_data,
    x="popularity",
    y="tmdb_rating",
    s=70
)

plt.title("Movie Popularity vs TMDB Rating")
plt.xlabel("Popularity")
plt.ylabel("TMDB Rating")

plt.tight_layout()

output_path = os.path.join(
    CHART_DIR,
    "popularity_vs_tmdb_rating.png"
)

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

print(f"Saved: {output_path}")

plt.show()
plt.close()

# ============================================================
# C4. CORRELATION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("CORRELATION ANALYSIS")
print("=" * 70)

correlation_columns = [
    "tmdb_rating",
    "vote_count",
    "popularity",
    "imdb_rating",
    "runtime_minutes",
    "news_count"
]

correlation = df[correlation_columns].corr()

print("\nCorrelation Matrix:")
print(correlation.round(3))

# Save correlation matrix
correlation_path = os.path.join(
    RESULT_DIR,
    "correlation_matrix.csv"
)

correlation.to_csv(correlation_path)

print(f"\nCorrelation matrix saved: {correlation_path}")

# ============================================================
# IMPORTANT CORRELATIONS
# ============================================================

print("\nImportant Relationships:")

print(
    "TMDB Rating vs IMDb Rating:",
    round(
        df["tmdb_rating"].corr(df["imdb_rating"]),
        3
    )
)

print(
    "TMDB Rating vs Vote Count:",
    round(
        df["tmdb_rating"].corr(df["vote_count"]),
        3
    )
)

print(
    "TMDB Rating vs Popularity:",
    round(
        df["tmdb_rating"].corr(df["popularity"]),
        3
    )
)

print(
    "Popularity vs Vote Count:",
    round(
        df["popularity"].corr(df["vote_count"]),
        3
    )
)

# ============================================================
# PART D - MULTIVARIATE ANALYSIS
# CORRELATION HEATMAP
# ============================================================

print("\n" + "=" * 70)
print("PART D - MULTIVARIATE ANALYSIS")
print("=" * 70)

print("\nGenerating Correlation Heatmap...")

# Numerical variables for multivariate analysis
heatmap_columns = [
    "tmdb_rating",
    "vote_count",
    "popularity",
    "imdb_rating",
    "runtime_minutes",
    "news_count"
]

# Calculate correlation
correlation = df[heatmap_columns].corr()

print("\nCorrelation Matrix:")
print(correlation.round(2))

# Create heatmap
plt.figure(figsize=(10, 8))

sns.heatmap(
    correlation,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=0.5,
    square=True
)

plt.title("Correlation Heatmap of Fused Movie Dataset")

plt.tight_layout()

# Save heatmap
output_path = os.path.join(
    CHART_DIR,
    "correlation_heatmap.png"
)

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

print(f"\nSaved: {output_path}")

# Display
plt.show()

plt.close()

print("\nCorrelation heatmap generated successfully.")

# ============================================================
# PART E - FINDINGS AND INTERPRETATION
# ============================================================

print("\n" + "=" * 70)
print("PART E - FINDINGS AND INTERPRETATION")
print("=" * 70)

# ------------------------------------------------------------
# 1. Dataset Overview
# ------------------------------------------------------------

print("\n1. DATASET OVERVIEW")
print("-" * 50)

print("Dataset: movie_fused_18_columns.csv")
print("Number of records:", len(df))
print("Number of original columns:", 18)

# ------------------------------------------------------------
# 2. Missing Values
# ------------------------------------------------------------

print("\n2. MISSING VALUE FINDINGS")
print("-" * 50)

missing_values = df.isnull().sum()
missing_values = missing_values[missing_values > 0]

if len(missing_values) == 0:
    print("No missing values were found.")
else:
    print(missing_values)

# ------------------------------------------------------------
# 3. Duplicate Records
# ------------------------------------------------------------

print("\n3. DUPLICATE RECORD FINDINGS")
print("-" * 50)

duplicates = df.duplicated().sum()

print("Duplicate records:", duplicates)

if duplicates == 0:
    print("No duplicate records were found.")
else:
    print("Duplicate records are present and should be reviewed.")

# ------------------------------------------------------------
# 4. Descriptive Statistics
# ------------------------------------------------------------

print("\n4. DESCRIPTIVE STATISTICS FINDINGS")
print("-" * 50)

for column in numeric_columns:

    print(f"\n{column}")

    print("Mean:", round(df[column].mean(), 2))
    print("Median:", round(df[column].median(), 2))
    print("Minimum:", round(df[column].min(), 2))
    print("Maximum:", round(df[column].max(), 2))

# ------------------------------------------------------------
# 5. Highest Rated Movies
# ------------------------------------------------------------

print("\n5. HIGHEST RATED MOVIES")
print("-" * 50)

top_rated = df[
    ["movie_title", "tmdb_rating", "imdb_rating"]
].sort_values(
    by="tmdb_rating",
    ascending=False
).head(10)

print(top_rated.to_string(index=False))

# ------------------------------------------------------------
# 6. Most Popular Movies
# ------------------------------------------------------------

print("\n6. MOST POPULAR MOVIES")
print("-" * 50)

top_popular = df[
    ["movie_title", "popularity", "tmdb_rating"]
].sort_values(
    by="popularity",
    ascending=False
).head(10)

print(top_popular.to_string(index=False))

# ------------------------------------------------------------
# 7. Most Voted Movies
# ------------------------------------------------------------

print("\n7. MOST VOTED MOVIES")
print("-" * 50)

top_voted = df[
    ["movie_title", "vote_count", "tmdb_rating"]
].sort_values(
    by="vote_count",
    ascending=False
).head(10)

print(top_voted.to_string(index=False))

# ------------------------------------------------------------
# 8. Top Genres
# ------------------------------------------------------------

print("\n8. TOP MOVIE GENRES")
print("-" * 50)

print(genre_counts)

# ------------------------------------------------------------
# 9. Correlation Findings
# ------------------------------------------------------------

print("\n9. CORRELATION FINDINGS")
print("-" * 50)

print(correlation.round(3))

# Remove diagonal values
corr_pairs = correlation.copy()

for i in range(len(corr_pairs.columns)):
    corr_pairs.iloc[i, i] = np.nan

# Find strongest positive correlation
positive_pair = corr_pairs.stack().idxmax()
positive_value = corr_pairs.stack().max()

# Find strongest negative correlation
negative_pair = corr_pairs.stack().idxmin()
negative_value = corr_pairs.stack().min()

print("\nStrongest positive relationship:")
print(
    positive_pair[0],
    "<->",
    positive_pair[1],
    "=",
    round(positive_value, 3)
)

print("\nStrongest negative relationship:")
print(
    negative_pair[0],
    "<->",
    negative_pair[1],
    "=",
    round(negative_value, 3)
)

# ------------------------------------------------------------
# 10. Final EDA Summary
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("FINAL EDA SUMMARY")
print("=" * 70)

print("""
The EDA was performed on the newly fused movie dataset.

The analysis included:
1. Dataset inspection and preprocessing.
2. Univariate analysis using descriptive statistics,
   histograms, boxplots and a genre bar chart.
3. Bivariate analysis using scatter plots and correlation analysis.
4. Multivariate analysis using a correlation heatmap.

The analysis provides an understanding of movie ratings,
popularity, vote counts, runtime, news coverage and genre
distribution.

These findings can be used as a foundation for the
Movie Recommendation RAG system.
""")

print("=" * 70)
print("PART E COMPLETED SUCCESSFULLY")
print("=" * 70)

