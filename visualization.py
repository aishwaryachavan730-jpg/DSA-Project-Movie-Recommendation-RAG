
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# MOVIEVERSE AI - DATA VISUALIZATION
# ==========================================

FILE_PATH = "fused_data/movie_fused_18_columns.csv"
OUTPUT_DIR = "fused_data/visualizations"

os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")

# Load dataset
df = pd.read_csv(FILE_PATH)

print("=" * 50)
print("MOVIEVERSE AI - VISUALIZATION")
print("=" * 50)

print("Dataset shape:", df.shape)
print("\nMissing values:")
print(df.isnull().sum())


# Convert numerical columns safely
numeric_columns = [
    "tmdb_rating",
    "imdb_rating",
    "vote_count",
    "popularity",
    "news_count"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Extract runtime in minutes (e.g. "148 min" -> 148)
df["runtime_minutes"] = pd.to_numeric(
    df["runtime"].astype(str).str.extract(r"(\d+)", expand=False),
    errors="coerce"
)

print("\nValid runtime values:", df["runtime_minutes"].notna().sum())
print("Missing runtime values:", df["runtime_minutes"].isna().sum())

# ==========================================
# GRAPH 1: IMDb RATING DISTRIBUTION
# ==========================================

plt.figure(figsize=(9, 5))

sns.histplot(
    data=df,
    x="imdb_rating",
    bins=15,
    kde=True
)

plt.title("Distribution of IMDb Ratings")
plt.xlabel("IMDb Rating")
plt.ylabel("Number of Movies")

plt.tight_layout()
plt.savefig(
    f"{OUTPUT_DIR}/01_imdb_rating_distribution.png",
    dpi=300
)
plt.close()



# ==========================================
# GRAPH 2: RUNTIME BOXPLOT
# ==========================================

plt.figure(figsize=(9, 5))

sns.boxplot(
    x=df["runtime_minutes"].dropna()
)

plt.title("Movie Runtime Distribution")
plt.xlabel("Runtime (Minutes)")

plt.tight_layout()
plt.savefig(
    f"{OUTPUT_DIR}/02_runtime_boxplot.png",
    dpi=300
)
plt.close()


# ==========================================
# GRAPH 3: TMDB VS IMDb RATING
# ==========================================

plt.figure(figsize=(9, 5))

sns.regplot(
    data=df,
    x="tmdb_rating",
    y="imdb_rating",
    scatter_kws={"alpha": 0.7}
)

plt.title("TMDB Rating vs IMDb Rating")
plt.xlabel("TMDB Rating")
plt.ylabel("IMDb Rating")

plt.tight_layout()
plt.savefig(
    f"{OUTPUT_DIR}/03_tmdb_vs_imdb.png",
    dpi=300
)
plt.close()


# ==========================================
# GRAPH 4: VOTE COUNT VS POPULARITY
# ==========================================

plt.figure(figsize=(9, 5))

sns.scatterplot(
    data=df,
    x="vote_count",
    y="popularity"
)

plt.title("TMDB Vote Count vs Movie Popularity")
plt.xlabel("Vote Count")
plt.ylabel("Popularity")

plt.tight_layout()
plt.savefig(
    f"{OUTPUT_DIR}/04_votes_vs_popularity.png",
    dpi=300
)
plt.close()


# ==========================================
# GRAPH 5: CORRELATION HEATMAP
# ==========================================

numeric_df = df.select_dtypes(include="number").drop(
    columns=["runtime_minutes"],
    errors="ignore"
)

numeric_df["runtime_minutes"] = df["runtime_minutes"]

plt.figure(figsize=(12, 8))

correlation = numeric_df.corr()

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)

plt.title("Correlation Heatmap - Fused Movie Dataset")

plt.tight_layout()
plt.savefig(
    f"{OUTPUT_DIR}/05_correlation_heatmap.png",
    dpi=300
)
plt.close()


# ==========================================
# GRAPH 6: API FUSION INSIGHT
# VOTE COUNT VS NEWS COUNT
# ==========================================

plt.figure(figsize=(9, 5))

sns.regplot(
    data=df,
    x="vote_count",
    y="news_count",
    scatter_kws={"alpha": 0.7}
)

plt.title("API Fusion Insight: Vote Count vs News Count")
plt.xlabel("TMDB Vote Count")
plt.ylabel("News Articles Count")

plt.tight_layout()
plt.savefig(
    f"{OUTPUT_DIR}/06_api_fusion_insight.png",
    dpi=300
)
plt.close()


# ==========================================
# FINAL OUTPUT
# ==========================================

print("\nAll six visualization files generated.")

print("\nSaved files:")

for file in sorted(os.listdir(OUTPUT_DIR)):
    if file.endswith(".png"):
        print(file)

print("\nOutput folder:", OUTPUT_DIR)
