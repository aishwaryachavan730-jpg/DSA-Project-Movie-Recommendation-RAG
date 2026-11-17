import pandas as pd
import matplotlib.pyplot as plt
import os


# =========================================================
# STEP 7 — EXPLORATORY DATA ANALYSIS
# =========================================================

print("=" * 60)
print("STEP 7 - EXPLORATORY DATA ANALYSIS")
print("=" * 60)


# ---------------------------------------------------------
# 1. Load fused dataset
# ---------------------------------------------------------

INPUT_FILE = "DataSet/fused_movies.csv"

df = pd.read_csv(INPUT_FILE)

print("\nDataset loaded successfully!")


# ---------------------------------------------------------
# 2. Basic information
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("1. DATASET INFORMATION")
print("=" * 60)

print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

print("\nColumns:")
for column in df.columns:
    print("-", column)


# ---------------------------------------------------------
# 3. First 5 records
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("2. FIRST 5 MOVIES")
print("=" * 60)

print(df.head())


# ---------------------------------------------------------
# 4. Data types
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("3. DATA TYPES")
print("=" * 60)

print(df.dtypes)


# ---------------------------------------------------------
# 5. Missing values
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("4. MISSING VALUES")
print("=" * 60)

missing_values = df.isnull().sum()

print(missing_values)


# ---------------------------------------------------------
# 6. Duplicate records
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("5. DUPLICATE RECORDS")
print("=" * 60)

duplicates = df.duplicated().sum()

print("Duplicate records:", duplicates)


# ---------------------------------------------------------
# 7. Unique movie titles
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("6. UNIQUE MOVIES")
print("=" * 60)

unique_movies = df["title"].nunique()

print("Unique movie titles:", unique_movies)


# ---------------------------------------------------------
# 8. Rating statistics
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("7. TMDB RATING STATISTICS")
print("=" * 60)

rating = pd.to_numeric(
    df["tmdb_rating"],
    errors="coerce"
)

print(rating.describe())


# ---------------------------------------------------------
# 9. Average rating
# ---------------------------------------------------------

print("\nAverage TMDB rating:")

print(round(rating.mean(), 2))


# ---------------------------------------------------------
# 10. Highest rated movies
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("8. TOP RATED MOVIES")
print("=" * 60)

top_movies = df.copy()

top_movies["tmdb_rating"] = pd.to_numeric(
    top_movies["tmdb_rating"],
    errors="coerce"
)

top_movies = top_movies.sort_values(
    by="tmdb_rating",
    ascending=False
)

print(
    top_movies[
        ["title", "year", "tmdb_rating"]
    ].head(10)
)


# ---------------------------------------------------------
# 11. Movies by year
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("9. MOVIES BY YEAR")
print("=" * 60)

year_counts = df["year"].value_counts().sort_index()

print(year_counts)


# ---------------------------------------------------------
# 12. Genre analysis
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("10. GENRE ANALYSIS")
print("=" * 60)

genre_series = (
    df["genre"]
    .dropna()
    .astype(str)
    .str.split(",")
    .explode()
    .str.strip()
)

genre_counts = genre_series.value_counts()

print(genre_counts.head(10))


# ---------------------------------------------------------
# Create EDA output folder
# ---------------------------------------------------------

os.makedirs("eda/output", exist_ok=True)


# =========================================================
# GRAPH 1 — Rating Distribution
# =========================================================

plt.figure(figsize=(8, 5))

plt.hist(
    rating.dropna(),
    bins=10
)

plt.title("TMDB Movie Rating Distribution")
plt.xlabel("TMDB Rating")
plt.ylabel("Number of Movies")

plt.tight_layout()

plt.savefig(
    "eda/output/rating_distribution.png"
)

plt.show()


# =========================================================
# GRAPH 2 — Movies by Year
# =========================================================

plt.figure(figsize=(10, 5))

year_counts.plot(
    kind="bar"
)

plt.title("Movies by Year")
plt.xlabel("Year")
plt.ylabel("Number of Movies")

plt.tight_layout()

plt.savefig(
    "eda/output/movies_by_year.png"
)

plt.show()


# =========================================================
# GRAPH 3 — Top Genres
# =========================================================

top_genres = genre_counts.head(10)

plt.figure(figsize=(10, 5))

top_genres.plot(
    kind="bar"
)

plt.title("Top 10 Movie Genres")
plt.xlabel("Genre")
plt.ylabel("Number of Movies")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "eda/output/top_genres.png"
)

plt.show()


# =========================================================
# GRAPH 4 — Top Rated Movies
# =========================================================

top_10 = top_movies.head(10)

plt.figure(figsize=(10, 6))

plt.barh(
    top_10["title"],
    top_10["tmdb_rating"]
)

plt.title("Top 10 Rated Movies")

plt.xlabel("TMDB Rating")

plt.ylabel("Movie")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
    "eda/output/top_rated_movies.png"
)

plt.show()


# =========================================================
# Save EDA report
# =========================================================

report = {
    "total_movies": int(df.shape[0]),
    "total_columns": int(df.shape[1]),
    "unique_movies": int(unique_movies),
    "duplicate_records": int(duplicates),
    "average_tmdb_rating": round(float(rating.mean()), 2),
    "missing_values": missing_values.to_dict()
}

report_df = pd.DataFrame(
    list(report.items()),
    columns=["Metric", "Value"]
)

report_df.to_csv(
    "eda/output/eda_report.csv",
    index=False
)


print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nGenerated files:")

print("1. eda/output/rating_distribution.png")
print("2. eda/output/movies_by_year.png")
print("3. eda/output/top_genres.png")
print("4. eda/output/top_rated_movies.png")
print("5. eda/output/eda_report.csv")

print("\nNext phase:")
print("EDA → Data Cleaning → Embeddings → FAISS → RAG")