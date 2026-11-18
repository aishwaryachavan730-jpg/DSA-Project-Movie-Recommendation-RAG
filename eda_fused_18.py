# ============================================================
# MOVIEVERSE AI
# EDA ON 18-COLUMN FUSED DATASET
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# INPUT DATASET
# ============================================================

CSV_PATH = os.path.join(
    PROJECT_ROOT,
    "fused_data",
    "movie_fused_18_columns.csv"
)


# ============================================================
# OUTPUT DIRECTORY
# ============================================================

EDA_DIR = os.path.join(
    PROJECT_ROOT,
    "fused_data",
    "EDA"
)

os.makedirs(
    EDA_DIR,
    exist_ok=True
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("MOVIEVERSE AI - EDA ON 18-COLUMN FUSED DATASET")
print("=" * 70)


# ============================================================
# CHECK FILE
# ============================================================

if not os.path.exists(CSV_PATH):

    print("\nERROR: FUSED CSV FILE NOT FOUND")
    print("\nExpected file:")
    print(CSV_PATH)

    print("\nCheck your fused_data folder.")

    exit()


# ============================================================
# LOAD DATA
# ============================================================

print("\nLoading fused dataset...")

df = pd.read_csv(
    CSV_PATH
)


# ============================================================
# BASIC INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("1. DATASET INFORMATION")
print("=" * 70)

print(
    f"\nRows: {df.shape[0]}"
)

print(
    f"Columns: {df.shape[1]}"
)

print("\nColumn Names:")

for i, column in enumerate(
    df.columns,
    start=1
):

    print(
        f"{i}. {column}"
    )


# ============================================================
# FIRST FIVE ROWS
# ============================================================

print("\n" + "=" * 70)
print("2. FIRST FIVE ROWS")
print("=" * 70)

print(
    df.head()
)


# ============================================================
# DATA TYPES
# ============================================================

print("\n" + "=" * 70)
print("3. DATA TYPES")
print("=" * 70)

print(
    df.dtypes
)


# ============================================================
# MISSING VALUES
# ============================================================

print("\n" + "=" * 70)
print("4. MISSING VALUE ANALYSIS")
print("=" * 70)

missing = df.isnull().sum()

missing_percentage = (
    missing / len(df) * 100
)

missing_table = pd.DataFrame({

    "Column": df.columns,

    "Missing_Count": missing.values,

    "Missing_Percentage":
        missing_percentage.values

})

print(
    missing_table.to_string(
        index=False
    )
)


# ============================================================
# DUPLICATE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("5. DUPLICATE ANALYSIS")
print("=" * 70)

duplicates = df.duplicated().sum()

print(
    f"Duplicate rows: {duplicates}"
)


# ============================================================
# MOVIE TITLE PRIMARY KEY CHECK
# ============================================================

print("\n" + "=" * 70)
print("6. MOVIE TITLE KEY ANALYSIS")
print("=" * 70)

if "movie_title" in df.columns:

    unique_titles = (
        df["movie_title"]
        .nunique()
    )

    total_titles = len(df)

    print(
        f"Total movie records: {total_titles}"
    )

    print(
        f"Unique movie titles: {unique_titles}"
    )

    duplicate_titles = (
        total_titles -
        unique_titles
    )

    print(
        f"Duplicate movie titles: "
        f"{duplicate_titles}"
    )

else:

    print(
        "movie_title column not found."
    )


# ============================================================
# NUMERIC COLUMNS
# ============================================================

print("\n" + "=" * 70)
print("7. NUMERICAL COLUMN ANALYSIS")
print("=" * 70)

numeric_columns = (
    df.select_dtypes(
        include=np.number
    ).columns
)

print(
    "\nNumerical columns:"
)

for column in numeric_columns:

    print(
        f"- {column}"
    )


if len(numeric_columns) > 0:

    print(
        "\nStatistical Summary:"
    )

    print(
        df[numeric_columns]
        .describe()
    )


# ============================================================
# CATEGORICAL COLUMNS
# ============================================================

print("\n" + "=" * 70)
print("8. CATEGORICAL COLUMN ANALYSIS")
print("=" * 70)

categorical_columns = (
    df.select_dtypes(
        include=["object"]
    ).columns
)

for column in categorical_columns:

    print(
        f"\nColumn: {column}"
    )

    print(
        f"Unique values: "
        f"{df[column].nunique()}"
    )


# ============================================================
# TOP MOVIES BY RATING
# ============================================================

print("\n" + "=" * 70)
print("9. TOP MOVIES BY RATING")
print("=" * 70)

if "tmdb_rating" in df.columns:

    top_rating = (
        df[
            [
                "movie_title",
                "tmdb_rating"
            ]
        ]
        .dropna()
        .sort_values(
            "tmdb_rating",
            ascending=False
        )
        .head(10)
    )

    print(
        top_rating.to_string(
            index=False
        )
    )


# ============================================================
# TOP MOVIES BY POPULARITY
# ============================================================

print("\n" + "=" * 70)
print("10. TOP MOVIES BY POPULARITY")
print("=" * 70)

if "popularity" in df.columns:

    top_popularity = (
        df[
            [
                "movie_title",
                "popularity"
            ]
        ]
        .dropna()
        .sort_values(
            "popularity",
            ascending=False
        )
        .head(10)
    )

    print(
        top_popularity.to_string(
            index=False
        )
    )


# ============================================================
# RELEASE YEAR ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("11. RELEASE YEAR ANALYSIS")
print("=" * 70)

if "release_date" in df.columns:

    dates = pd.to_datetime(
        df["release_date"],
        errors="coerce"
    )

    release_year = (
        dates.dt.year
    )

    print(
        release_year
        .value_counts()
        .sort_index()
        .tail(20)
    )


# ============================================================
# RATING DISTRIBUTION
# ============================================================

if "tmdb_rating" in df.columns:

    plt.figure(
        figsize=(10, 6)
    )

    df["tmdb_rating"].dropna().plot(
        kind="hist",
        bins=20
    )

    plt.title(
        "TMDB Rating Distribution"
    )

    plt.xlabel(
        "TMDB Rating"
    )

    plt.ylabel(
        "Number of Movies"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            EDA_DIR,
            "01_tmdb_rating_distribution.png"
        )
    )

    plt.close()


# ============================================================
# POPULARITY DISTRIBUTION
# ============================================================

if "popularity" in df.columns:

    plt.figure(
        figsize=(10, 6)
    )

    df["popularity"].dropna().plot(
        kind="hist",
        bins=30
    )

    plt.title(
        "Movie Popularity Distribution"
    )

    plt.xlabel(
        "Popularity"
    )

    plt.ylabel(
        "Number of Movies"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            EDA_DIR,
            "02_popularity_distribution.png"
        )
    )

    plt.close()


# ============================================================
# TOP 10 MOVIES BY RATING
# ============================================================

if (
    "movie_title" in df.columns
    and
    "tmdb_rating" in df.columns
):

    top10 = (
        df[
            [
                "movie_title",
                "tmdb_rating"
            ]
        ]
        .dropna()
        .sort_values(
            "tmdb_rating",
            ascending=False
        )
        .head(10)
    )

    plt.figure(
        figsize=(12, 6)
    )

    plt.bar(
        top10["movie_title"],
        top10["tmdb_rating"]
    )

    plt.title(
        "Top 10 Movies by TMDB Rating"
    )

    plt.xlabel(
        "Movie"
    )

    plt.ylabel(
        "TMDB Rating"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            EDA_DIR,
            "03_top_10_movies_rating.png"
        )
    )

    plt.close()


# ============================================================
# RELEASE YEAR TREND
# ============================================================

if "release_date" in df.columns:

    dates = pd.to_datetime(
        df["release_date"],
        errors="coerce"
    )

    years = dates.dt.year

    year_counts = (
        years
        .dropna()
        .value_counts()
        .sort_index()
    )

    plt.figure(
        figsize=(12, 6)
    )

    year_counts.plot(
        kind="line"
    )

    plt.title(
        "Movies Released by Year"
    )

    plt.xlabel(
        "Release Year"
    )

    plt.ylabel(
        "Number of Movies"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            EDA_DIR,
            "04_movies_by_year.png"
        )
    )

    plt.close()


# ============================================================
# RATING VS POPULARITY
# ============================================================

if (
    "tmdb_rating" in df.columns
    and
    "popularity" in df.columns
):

    plot_data = df[
        [
            "tmdb_rating",
            "popularity"
        ]
    ].dropna()

    plt.figure(
        figsize=(10, 6)
    )

    plt.scatter(
        plot_data["tmdb_rating"],
        plot_data["popularity"],
        alpha=0.5
    )

    plt.title(
        "TMDB Rating vs Movie Popularity"
    )

    plt.xlabel(
        "TMDB Rating"
    )

    plt.ylabel(
        "Popularity"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            EDA_DIR,
            "05_rating_vs_popularity.png"
        )
    )

    plt.close()


# ============================================================
# API COVERAGE
# ============================================================

print("\n" + "=" * 70)
print("12. API DATA COVERAGE")
print("=" * 70)

possible_api_columns = {

    "TMDB": [
        "tmdb_rating",
        "tmdb_vote_count"
    ],

    "OMDb": [
        "imdb_rating",
        "director",
        "genre"
    ],

    "WatchMode": [
        "streaming_sources"
    ],

    "News API": [
        "news_count"
    ],

    "Wikipedia": [
        "wikipedia_summary"
    ]
}


for api, columns in possible_api_columns.items():

    available = [
        column
        for column in columns
        if column in df.columns
    ]

    if available:

        print(
            f"\n{api}:"
        )

        for column in available:

            non_null = (
                df[column]
                .notna()
                .sum()
            )

            coverage = (
                non_null /
                len(df) *
                100
            )

            print(
                f"  {column}: "
                f"{non_null} records "
                f"({coverage:.2f}%)"
            )


# ============================================================
# CORRELATION
# ============================================================

print("\n" + "=" * 70)
print("13. CORRELATION ANALYSIS")
print("=" * 70)

if len(numeric_columns) >= 2:

    correlation = (
        df[numeric_columns]
        .corr()
    )

    print(
        correlation
    )

    correlation.to_csv(
        os.path.join(
            EDA_DIR,
            "correlation_matrix.csv"
        )
    )


# ============================================================
# SAVE MISSING VALUE REPORT
# ============================================================

missing_table.to_csv(
    os.path.join(
        EDA_DIR,
        "missing_value_report.csv"
    ),
    index=False
)


# ============================================================
# SAVE STATISTICS
# ============================================================

if len(numeric_columns) > 0:

    df[numeric_columns].describe().to_csv(
        os.path.join(
            EDA_DIR,
            "statistical_summary.csv"
        )
    )


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 70)

print(
    "\nEDA output folder:"
)

print(
    EDA_DIR
)

print(
    "\nGenerated files:"
)

if os.path.exists(EDA_DIR):

    for filename in os.listdir(
        EDA_DIR
    ):

        print(
            f" - {filename}"
        )

print(
    "\nNext step: Analyze EDA findings "
    "and prepare interpretations for the assignment."
)

print("=" * 70)