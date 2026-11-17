# ================================================================
# MOVIEVERSE AI
# STEP 2 - COMPLETE EDA ON 18-COLUMN FUSED DATASET
# ================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ================================================================
# 1. PATH CONFIGURATION
# ================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "fused_data" / "movie_fused_18_columns.csv"

REPORT_DIR = PROJECT_ROOT / "eda" / "reports"
CHART_DIR = PROJECT_ROOT / "eda" / "charts"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("MOVIEVERSE AI - COMPLETE EDA")
print("18-COLUMN FUSED MOVIE DATASET")
print("=" * 70)

# ================================================================
# 2. LOAD DATASET
# ================================================================

if not INPUT_FILE.exists():
    print("\nERROR: Fused CSV not found.")
    print("\nExpected location:")
    print(INPUT_FILE)
    raise SystemExit

df = pd.read_csv(INPUT_FILE)

print("\nDataset loaded successfully.")

# ================================================================
# 3. DATASET SHAPE
# ================================================================

print("\n" + "=" * 70)
print("1. DATASET SHAPE")
print("=" * 70)

print("Rows    :", df.shape[0])
print("Columns :", df.shape[1])

# ================================================================
# 4. COLUMN NAMES
# ================================================================

print("\n" + "=" * 70)
print("2. COLUMN NAMES")
print("=" * 70)

for i, column in enumerate(df.columns, 1):
    print(f"{i:02d}. {column}")

# ================================================================
# 5. DATA TYPES
# ================================================================

print("\n" + "=" * 70)
print("3. DATA TYPES")
print("=" * 70)

print(df.dtypes)

# ================================================================
# 6. FIRST FIVE RECORDS
# ================================================================

print("\n" + "=" * 70)
print("4. FIRST FIVE RECORDS")
print("=" * 70)

print(df.head().to_string())

# ================================================================
# 7. LAST FIVE RECORDS
# ================================================================

print("\n" + "=" * 70)
print("5. LAST FIVE RECORDS")
print("=" * 70)

print(df.tail().to_string())

# ================================================================
# 8. DUPLICATE MOVIE TITLES
# ================================================================

print("\n" + "=" * 70)
print("6. DUPLICATE MOVIE TITLES")
print("=" * 70)

duplicates = df["movie_title"].duplicated().sum()
unique_movies = df["movie_title"].nunique()

print("Duplicate movie titles:", duplicates)
print("Unique movie titles   :", unique_movies)

# ================================================================
# 9. MISSING VALUES
# ================================================================

print("\n" + "=" * 70)
print("7. MISSING VALUES")
print("=" * 70)

missing = pd.DataFrame({
    "Column": df.columns,
    "Missing_Count": df.isnull().sum().values,
    "Missing_Percentage": (
        df.isnull().mean().values * 100
    ).round(2)
})

print(missing.to_string(index=False))

missing.to_csv(
    REPORT_DIR / "missing_values_report.csv",
    index=False
)

# ================================================================
# 10. DATA COMPLETENESS
# ================================================================

print("\n" + "=" * 70)
print("8. DATA COMPLETENESS")
print("=" * 70)

total_cells = df.shape[0] * df.shape[1]
missing_cells = df.isnull().sum().sum()

completeness = (
    (total_cells - missing_cells) / total_cells
) * 100

print(f"Dataset completeness: {completeness:.2f}%")

# ================================================================
# 11. CREATE NUMERIC RUNTIME
# ================================================================

print("\n" + "=" * 70)
print("9. RUNTIME CONVERSION")
print("=" * 70)

# Convert values such as:
# "148 min" -> 148
# "169" -> 169

df["runtime_numeric"] = (
    df["runtime"]
    .astype(str)
    .str.extract(r"(\d+\.?\d*)")[0]
)

df["runtime_numeric"] = pd.to_numeric(
    df["runtime_numeric"],
    errors="coerce"
)

print(
    "Valid runtime values:",
    df["runtime_numeric"].notna().sum()
)

print(
    "Missing runtime values:",
    df["runtime_numeric"].isna().sum()
)

if df["runtime_numeric"].notna().sum() > 0:

    print(
        "Average runtime:",
        round(df["runtime_numeric"].mean(), 2),
        "minutes"
    )

    print(
        "Minimum runtime:",
        df["runtime_numeric"].min(),
        "minutes"
    )

    print(
        "Maximum runtime:",
        df["runtime_numeric"].max(),
        "minutes"
    )

# ================================================================
# 12. NUMERIC COLUMN SUMMARY
# ================================================================

print("\n" + "=" * 70)
print("10. NUMERIC COLUMN SUMMARY")
print("=" * 70)

numeric_columns = [
    "tmdb_rating",
    "vote_count",
    "popularity",
    "imdb_rating",
    "news_count",
    "runtime_numeric"
]

numeric_columns = [
    col for col in numeric_columns
    if col in df.columns
]

numeric_summary = df[numeric_columns].describe().T

print(numeric_summary.to_string())

numeric_summary.to_csv(
    REPORT_DIR / "numeric_summary.csv"
)

# ================================================================
# 13. UNIQUE VALUES
# ================================================================

print("\n" + "=" * 70)
print("11. UNIQUE VALUES")
print("=" * 70)

unique_data = []

for column in df.columns:

    unique_data.append({
        "Column": column,
        "Unique_Values": df[column].nunique(dropna=False),
        "Total_Values": len(df)
    })

unique_df = pd.DataFrame(unique_data)

print(unique_df.to_string(index=False))

unique_df.to_csv(
    REPORT_DIR / "unique_values_report.csv",
    index=False
)

# ================================================================
# 14. RATING ANALYSIS
# ================================================================

print("\n" + "=" * 70)
print("12. RATING ANALYSIS")
print("=" * 70)

for column in ["tmdb_rating", "imdb_rating"]:

    if column in df.columns:

        valid = df[column].dropna()

        print(f"\n{column}")
        print("Valid values:", len(valid))
        print("Average     :", round(valid.mean(), 2))
        print("Minimum     :", round(valid.min(), 2))
        print("Maximum     :", round(valid.max(), 2))
        print("Median      :", round(valid.median(), 2))

# ================================================================
# 15. TOP 10 MOVIES BY TMDB RATING
# ================================================================

print("\n" + "=" * 70)
print("13. TOP 10 MOVIES BY TMDB RATING")
print("=" * 70)

top_10 = (
    df[
        ["movie_title", "tmdb_rating"]
    ]
    .dropna()
    .sort_values(
        "tmdb_rating",
        ascending=False
    )
    .head(10)
)

print(top_10.to_string(index=False))

top_10.to_csv(
    REPORT_DIR / "top_10_movies.csv",
    index=False
)

# ================================================================
# 16. RELEASE YEAR ANALYSIS
# ================================================================

print("\n" + "=" * 70)
print("14. RELEASE YEAR ANALYSIS")
print("=" * 70)

df["release_year"] = pd.to_datetime(
    df["release_date"],
    errors="coerce"
).dt.year

valid_years = df["release_year"].dropna()

print("Earliest year:", int(valid_years.min()))
print("Latest year  :", int(valid_years.max()))

year_counts = (
    df["release_year"]
    .value_counts()
    .sort_index()
)

print("\nMovies by release year:")
print(year_counts.to_string())

# ================================================================
# GRAPH 1 - MOVIES BY RELEASE YEAR
# ================================================================

plt.figure(figsize=(12, 6))

year_counts.plot(
    kind="line",
    marker="o"
)

plt.title("Movies by Release Year")
plt.xlabel("Release Year")
plt.ylabel("Number of Movies")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    CHART_DIR / "01_movies_by_release_year.png",
    dpi=300
)

plt.close()

# ================================================================
# 17. RATING DISTRIBUTION
# ================================================================

# ================================================================
# GRAPH 2 - TMDB RATING DISTRIBUTION
# ================================================================

plt.figure(figsize=(10, 6))

plt.hist(
    df["tmdb_rating"].dropna(),
    bins=10,
    edgecolor="black"
)

plt.title("TMDB Rating Distribution")
plt.xlabel("TMDB Rating")
plt.ylabel("Number of Movies")
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "02_tmdb_rating_distribution.png",
    dpi=300
)

plt.close()

# ================================================================
# GRAPH 3 - IMDb RATING DISTRIBUTION
# ================================================================

plt.figure(figsize=(10, 6))

plt.hist(
    df["imdb_rating"].dropna(),
    bins=10,
    edgecolor="black"
)

plt.title("IMDb Rating Distribution")
plt.xlabel("IMDb Rating")
plt.ylabel("Number of Movies")
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "03_imdb_rating_distribution.png",
    dpi=300
)

plt.close()

# ================================================================
# GRAPH 4 - TMDB VS IMDb RATING
# ================================================================

plt.figure(figsize=(9, 6))

plt.scatter(
    df["tmdb_rating"],
    df["imdb_rating"],
    alpha=0.7
)

plt.title("TMDB Rating vs IMDb Rating")
plt.xlabel("TMDB Rating")
plt.ylabel("IMDb Rating")
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "04_tmdb_vs_imdb_rating.png",
    dpi=300
)

plt.close()

# ================================================================
# 18. VOTE COUNT ANALYSIS
# ================================================================

print("\n" + "=" * 70)
print("15. VOTE COUNT ANALYSIS")
print("=" * 70)

print("Average votes:",
      round(df["vote_count"].mean(), 2))

print("Minimum votes:",
      df["vote_count"].min())

print("Maximum votes:",
      df["vote_count"].max())

# ================================================================
# GRAPH 5 - TOP 10 MOVIES BY VOTE COUNT
# ================================================================

top_votes = (
    df[
        ["movie_title", "vote_count"]
    ]
    .sort_values(
        "vote_count",
        ascending=False
    )
    .head(10)
)

plt.figure(figsize=(12, 7))

plt.barh(
    top_votes["movie_title"][::-1],
    top_votes["vote_count"][::-1]
)

plt.title("Top 10 Movies by Vote Count")
plt.xlabel("Vote Count")
plt.ylabel("Movie")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "05_top_10_vote_count.png",
    dpi=300
)

plt.close()

# ================================================================
# 19. POPULARITY ANALYSIS
# ================================================================

print("\n" + "=" * 70)
print("16. POPULARITY ANALYSIS")
print("=" * 70)

print("Average popularity:",
      round(df["popularity"].mean(), 2))

print("Minimum popularity:",
      round(df["popularity"].min(), 2))

print("Maximum popularity:",
      round(df["popularity"].max(), 2))

# ================================================================
# GRAPH 6 - POPULARITY DISTRIBUTION
# ================================================================

plt.figure(figsize=(10, 6))

plt.hist(
    df["popularity"].dropna(),
    bins=15,
    edgecolor="black"
)

plt.title("Movie Popularity Distribution")
plt.xlabel("Popularity")
plt.ylabel("Number of Movies")
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "06_popularity_distribution.png",
    dpi=300
)

plt.close()

# ================================================================
# 20. GENRE ANALYSIS
# ================================================================

print("\n" + "=" * 70)
print("17. GENRE ANALYSIS")
print("=" * 70)

genre_series = (
    df["genres"]
    .fillna("")
    .astype(str)
    .str.split(",")
    .explode()
    .str.strip()
)

genre_counts = (
    genre_series[
        genre_series != ""
    ]
    .value_counts()
)

print("\nAll genres:")
print(genre_counts.to_string())

genre_counts.to_csv(
    REPORT_DIR / "genre_counts.csv"
)

# ================================================================
# GRAPH 7 - TOP 10 GENRES
# ================================================================

top_genres = genre_counts.head(10)

plt.figure(figsize=(10, 6))

plt.bar(
    top_genres.index,
    top_genres.values
)

plt.title("Top 10 Movie Genres")
plt.xlabel("Genre")
plt.ylabel("Number of Movies")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "07_top_10_genres.png",
    dpi=300
)

plt.close()

# ================================================================
# 21. STREAMING PLATFORM ANALYSIS
# ================================================================

print("\n" + "=" * 70)
print("18. STREAMING PLATFORM ANALYSIS")
print("=" * 70)

platform_series = (
    df["streaming_platforms"]
    .fillna("")
    .astype(str)
    .str.split(",")
    .explode()
    .str.strip()
)

platform_counts = (
    platform_series[
        platform_series != ""
    ]
    .value_counts()
)

print(platform_counts.to_string())

# ================================================================
# GRAPH 8 - STREAMING PLATFORMS
# ================================================================

if len(platform_counts) > 0:

    top_platforms = platform_counts.head(10)

    plt.figure(figsize=(10, 6))

    plt.bar(
        top_platforms.index,
        top_platforms.values
    )

    plt.title("Top Streaming Platforms")
    plt.xlabel("Streaming Platform")
    plt.ylabel("Number of Movies")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    plt.savefig(
        CHART_DIR / "08_streaming_platforms.png",
        dpi=300
    )

    plt.close()

# ================================================================
# 22. STREAMING REGION ANALYSIS
# ================================================================

print("\n" + "=" * 70)
print("19. STREAMING REGION ANALYSIS")
print("=" * 70)

region_counts = (
    df["streaming_region"]
    .fillna("Unknown")
    .astype(str)
    .value_counts()
)

print(region_counts.to_string())

# ================================================================
# GRAPH 9 - STREAMING REGION
# ================================================================

plt.figure(figsize=(10, 6))

region_counts.plot(
    kind="bar"
)

plt.title("Movies by Streaming Region")
plt.xlabel("Region")
plt.ylabel("Number of Movies")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "09_streaming_regions.png",
    dpi=300
)

plt.close()

# ================================================================
# 23. NEWS ANALYSIS
# ================================================================

print("\n" + "=" * 70)
print("20. NEWS ANALYSIS")
print("=" * 70)

print("Average news count:",
      round(df["news_count"].mean(), 2))

print("Movies with news:",
      (df["news_count"] > 0).sum())

print("Movies without news:",
      (df["news_count"] == 0).sum())

# ================================================================
# GRAPH 10 - NEWS COUNT
# ================================================================

news_counts = df["news_count"].value_counts().sort_index()

plt.figure(figsize=(8, 5))

plt.bar(
    news_counts.index.astype(str),
    news_counts.values
)

plt.title("Distribution of News Count")
plt.xlabel("Number of News Articles")
plt.ylabel("Number of Movies")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "10_news_count.png",
    dpi=300
)

plt.close()

# ================================================================
# 24. RUNTIME DISTRIBUTION
# ================================================================

# ================================================================
# GRAPH 11 - RUNTIME DISTRIBUTION
# ================================================================

if df["runtime_numeric"].notna().sum() > 0:

    plt.figure(figsize=(10, 6))

    plt.hist(
        df["runtime_numeric"].dropna(),
        bins=10,
        edgecolor="black"
    )

    plt.title("Movie Runtime Distribution")
    plt.xlabel("Runtime (Minutes)")
    plt.ylabel("Number of Movies")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        CHART_DIR / "11_runtime_distribution.png",
        dpi=300
    )

    plt.close()

# ================================================================
# 25. CORRELATION ANALYSIS
# ================================================================

print("\n" + "=" * 70)
print("21. CORRELATION ANALYSIS")
print("=" * 70)

correlation_columns = [
    "tmdb_rating",
    "vote_count",
    "popularity",
    "imdb_rating",
    "news_count",
    "runtime_numeric"
]

correlation_columns = [
    col for col in correlation_columns
    if col in df.columns
]

correlation = df[
    correlation_columns
].corr()

print(correlation.round(3).to_string())

correlation.to_csv(
    REPORT_DIR / "correlation_matrix.csv"
)

# ================================================================
# GRAPH 12 - RATING VS POPULARITY
# ================================================================

plt.figure(figsize=(9, 6))

plt.scatter(
    df["tmdb_rating"],
    df["popularity"],
    alpha=0.7
)

plt.title("TMDB Rating vs Popularity")
plt.xlabel("TMDB Rating")
plt.ylabel("Popularity")
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "12_rating_vs_popularity.png",
    dpi=300
)

plt.close()

# ================================================================
# 26. API DATA COVERAGE
# ================================================================

print("\n" + "=" * 70)
print("22. API DATA COVERAGE")
print("=" * 70)

api_columns = {
    "TMDB": [
        "tmdb_rating",
        "vote_count",
        "popularity"
    ],

    "OMDb": [
        "imdb_rating",
        "runtime",
        "director",
        "actors",
        "awards"
    ],

    "WatchMode": [
        "streaming_platforms",
        "streaming_region"
    ],

    "News API": [
        "news_count",
        "latest_news"
    ],

    "Wikipedia": [
        "wikipedia_summary",
        "wikipedia_url"
    ]
}

coverage_rows = []

for api, columns in api_columns.items():

    for column in columns:

        if column in df.columns:

            non_empty = df[column].notna().sum()

            # Treat empty strings as missing
            non_empty = (
                df[column]
                .astype(str)
                .str.strip()
                .replace("nan", "")
                .ne("")
                .sum()
            )

            coverage = (
                non_empty / len(df)
            ) * 100

            coverage_rows.append({
                "API": api,
                "Column": column,
                "Non_Empty": non_empty,
                "Coverage_Percentage": round(
                    coverage,
                    2
                )
            })

coverage_df = pd.DataFrame(
    coverage_rows
)

print(
    coverage_df.to_string(index=False)
)

coverage_df.to_csv(
    REPORT_DIR / "api_coverage.csv",
    index=False
)

# ================================================================
# 27. TEXT DATA STATISTICS
# ================================================================

print("\n" + "=" * 70)
print("23. TEXT DATA ANALYSIS")
print("=" * 70)

text_columns = [
    "overview",
    "actors",
    "director",
    "awards",
    "latest_news",
    "wikipedia_summary"
]

text_statistics = []

for column in text_columns:

    if column in df.columns:

        lengths = (
            df[column]
            .fillna("")
            .astype(str)
            .str.len()
        )

        text_statistics.append({
            "Column": column,
            "Average_Characters": round(
                lengths.mean(),
                2
            ),
            "Minimum_Characters": lengths.min(),
            "Maximum_Characters": lengths.max()
        })

text_stats_df = pd.DataFrame(
    text_statistics
)

print(
    text_stats_df.to_string(index=False)
)

text_stats_df.to_csv(
    REPORT_DIR / "text_statistics.csv",
    index=False
)

# ================================================================
# 28. CREATE CLEAN DATASET
# ================================================================

print("\n" + "=" * 70)
print("24. CLEAN DATASET")
print("=" * 70)

clean_df = df.copy()

# Fill text columns
text_fill_columns = [
    "overview",
    "genres",
    "director",
    "actors",
    "awards",
    "streaming_platforms",
    "streaming_region",
    "latest_news",
    "wikipedia_summary",
    "wikipedia_url"
]

for column in text_fill_columns:

    if column in clean_df.columns:

        clean_df[column] = (
            clean_df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

# Numeric missing values
for column in [
    "tmdb_rating",
    "vote_count",
    "popularity",
    "imdb_rating",
    "news_count",
    "runtime_numeric"
]:

    if column in clean_df.columns:

        clean_df[column] = pd.to_numeric(
            clean_df[column],
            errors="coerce"
        )

# ================================================================
# 29. CREATE MOVIE TEXT FOR RAG
# ================================================================

def create_movie_text(row):

    return f"""
Movie Title: {row.get('movie_title', '')}

Overview: {row.get('overview', '')}

Genres: {row.get('genres', '')}

Release Date: {row.get('release_date', '')}

TMDB Rating: {row.get('tmdb_rating', '')}

IMDb Rating: {row.get('imdb_rating', '')}

Vote Count: {row.get('vote_count', '')}

Popularity: {row.get('popularity', '')}

Runtime: {row.get('runtime_numeric', '')} minutes

Director: {row.get('director', '')}

Actors: {row.get('actors', '')}

Awards: {row.get('awards', '')}

Streaming Platforms: {row.get('streaming_platforms', '')}

Streaming Region: {row.get('streaming_region', '')}

News Count: {row.get('news_count', '')}

Latest News: {row.get('latest_news', '')}

Wikipedia Summary: {row.get('wikipedia_summary', '')}
""".strip()


clean_df["movie_text"] = clean_df.apply(
    create_movie_text,
    axis=1
)

# ================================================================
# 30. SAVE CLEAN DATASET
# ================================================================

clean_file = (
    REPORT_DIR /
    "eda_clean_dataset.csv"
)

clean_df.to_csv(
    clean_file,
    index=False
)

print("\nClean dataset saved at:")
print(clean_file)

# ================================================================
# 31. SAVE CLEAN EXCEL
# ================================================================

excel_file = (
    REPORT_DIR /
    "eda_clean_dataset.xlsx"
)

clean_df.to_excel(
    excel_file,
    index=False
)

print("\nClean Excel saved at:")
print(excel_file)

# ================================================================
# 32. FINAL SUMMARY
# ================================================================

print("\n" + "=" * 70)
print("EDA COMPLETE")
print("=" * 70)

print("\nDataset:")
print("  Movies              :", len(clean_df))
print("  Original columns   :", 18)
print("  Final columns      :", len(clean_df.columns))
print("  Duplicate titles   :", duplicates)
print(
    "  Dataset completeness:",
    f"{completeness:.2f}%"
)

print("\nGenerated charts:")
print("  01_movies_by_release_year.png")
print("  02_tmdb_rating_distribution.png")
print("  03_imdb_rating_distribution.png")
print("  04_tmdb_vs_imdb_rating.png")
print("  05_top_10_vote_count.png")
print("  06_popularity_distribution.png")
print("  07_top_10_genres.png")
print("  08_streaming_platforms.png")
print("  09_streaming_regions.png")
print("  10_news_count.png")
print("  11_runtime_distribution.png")
print("  12_rating_vs_popularity.png")

print("\nReports folder:")
print(REPORT_DIR)

print("\nCharts folder:")
print(CHART_DIR)

print("\n" + "=" * 70)
print("READY FOR TEXT PREPARATION + RAG")
print("=" * 70)