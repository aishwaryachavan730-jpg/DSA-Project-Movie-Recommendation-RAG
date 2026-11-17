# ============================================================
# MOVIEVERSE AI
# STEP E - EDA ON 18 COLUMN FUSED DATASET
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)

INPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "fused_data",
    "movie_fused_18_columns.csv"
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "EDA"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("MOVIEVERSE AI - EDA ON FUSED DATASET")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv(
    INPUT_FILE
)

print("\nDataset loaded successfully.")

print("\nFile:")
print(INPUT_FILE)

print("\nRows:", df.shape[0])
print("Columns:", df.shape[1])


# ============================================================
# STEP 1 - DISPLAY COLUMN NAMES
# ============================================================

print("\n" + "=" * 70)
print("STEP 1 - COLUMN INFORMATION")
print("=" * 70)

for i, column in enumerate(
    df.columns,
    start=1
):
    print(
        f"{i}. {column}"
    )


# ============================================================
# STEP 2 - DATA TYPES
# ============================================================

print("\n" + "=" * 70)
print("STEP 2 - DATA TYPES")
print("=" * 70)

print(
    df.dtypes
)


# Save data types

dtype_df = pd.DataFrame({
    "column": df.columns,
    "data_type": [
        str(dtype)
        for dtype in df.dtypes
    ]
})

dtype_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "eda_data_types.csv"
    ),
    index=False
)


# ============================================================
# STEP 3 - BASIC STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("STEP 3 - BASIC STATISTICS")
print("=" * 70)

print(
    df.describe(
        include="all"
    ).T
)

df.describe(
    include="all"
).T.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "eda_descriptive_statistics.csv"
    )
)


# ============================================================
# STEP 4 - MISSING VALUES
# ============================================================

print("\n" + "=" * 70)
print("STEP 4 - MISSING VALUES")
print("=" * 70)

missing = df.isnull().sum()

missing_percentage = (
    df.isnull().mean() * 100
)

missing_df = pd.DataFrame({
    "column": df.columns,
    "missing_count": missing.values,
    "missing_percentage": (
        missing_percentage.values
    )
})

print(
    missing_df
)

missing_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "eda_missing_values.csv"
    ),
    index=False
)


# ============================================================
# STEP 5 - DUPLICATE MOVIE TITLES
# ============================================================

print("\n" + "=" * 70)
print("STEP 5 - DUPLICATE MOVIE TITLES")
print("=" * 70)

if "movie_title" in df.columns:

    duplicate_count = (
        df["movie_title"]
        .duplicated()
        .sum()
    )

    print(
        "Duplicate movie titles:",
        duplicate_count
    )

else:

    print(
        "movie_title column not found."
    )


# ============================================================
# STEP 6 - UNIQUE MOVIES
# ============================================================

print("\n" + "=" * 70)
print("STEP 6 - UNIQUE MOVIES")
print("=" * 70)

if "movie_title" in df.columns:

    unique_movies = (
        df["movie_title"]
        .nunique()
    )

    print(
        "Unique movies:",
        unique_movies
    )


# ============================================================
# STEP 7 - NUMERIC COLUMNS
# ============================================================

print("\n" + "=" * 70)
print("STEP 7 - NUMERIC COLUMNS")
print("=" * 70)

numeric_columns = (
    df.select_dtypes(
        include=np.number
    ).columns
)

print(
    list(numeric_columns)
)


# ============================================================
# STEP 8 - NUMERIC SUMMARY
# ============================================================

if len(numeric_columns) > 0:

    print("\n" + "=" * 70)
    print("STEP 8 - NUMERIC SUMMARY")
    print("=" * 70)

    numeric_summary = df[
        numeric_columns
    ].describe().T

    print(
        numeric_summary
    )

    numeric_summary.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "eda_numeric_summary.csv"
        )
    )


# ============================================================
# STEP 9 - CATEGORICAL COLUMNS
# ============================================================

print("\n" + "=" * 70)
print("STEP 9 - CATEGORICAL COLUMNS")
print("=" * 70)

categorical_columns = (
    df.select_dtypes(
        include=["object"]
    ).columns
)

print(
    list(categorical_columns)
)


# ============================================================
# STEP 10 - RATING DISTRIBUTION
# ============================================================

rating_columns = [
    column
    for column in df.columns
    if "rating" in column.lower()
]

print("\n" + "=" * 70)
print("STEP 10 - RATING ANALYSIS")
print("=" * 70)

print(
    "Rating columns:",
    rating_columns
)

for column in rating_columns:

    values = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()

    if len(values) == 0:
        continue

    plt.figure(
        figsize=(10, 6)
    )

    sns.histplot(
        values,
        bins=20,
        kde=True
    )

    plt.title(
        f"Distribution of {column}"
    )

    plt.xlabel(
        column
    )

    plt.ylabel(
        "Number of Movies"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            f"rating_distribution_{column}.png"
        )
    )

    plt.close()


# ============================================================
# STEP 11 - VOTE COUNT ANALYSIS
# ============================================================

vote_columns = [
    column
    for column in df.columns
    if "vote" in column.lower()
]

print("\n" + "=" * 70)
print("STEP 11 - VOTE COUNT ANALYSIS")
print("=" * 70)

print(
    "Vote columns:",
    vote_columns
)

for column in vote_columns:

    values = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()

    if len(values) == 0:
        continue

    plt.figure(
        figsize=(10, 6)
    )

    sns.histplot(
        values,
        bins=30
    )

    plt.title(
        f"Distribution of {column}"
    )

    plt.xlabel(
        column
    )

    plt.ylabel(
        "Number of Movies"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            f"vote_distribution_{column}.png"
        )
    )

    plt.close()


# ============================================================
# STEP 12 - RELEASE YEAR ANALYSIS
# ============================================================

release_columns = [
    column
    for column in df.columns
    if "release" in column.lower()
    and "date" in column.lower()
]

print("\n" + "=" * 70)
print("STEP 12 - RELEASE YEAR ANALYSIS")
print("=" * 70)

print(
    "Release date columns:",
    release_columns
)

if release_columns:

    column = release_columns[0]

    dates = pd.to_datetime(
        df[column],
        errors="coerce"
    )

    years = (
        dates
        .dt.year
        .dropna()
    )

    if len(years) > 0:

        year_counts = (
            years
            .value_counts()
            .sort_index()
        )

        print(
            year_counts.tail(20)
        )

        plt.figure(
            figsize=(12, 6)
        )

        year_counts.plot()

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
                OUTPUT_DIR,
                "movies_by_release_year.png"
            )
        )

        plt.close()


# ============================================================
# STEP 13 - TOP MOVIES BY RATING
# ============================================================

print("\n" + "=" * 70)
print("STEP 13 - TOP MOVIES BY RATING")
print("=" * 70)

if "movie_title" in df.columns:

    rating_candidates = [
        column
        for column in df.columns
        if "rating" in column.lower()
    ]

    for column in rating_candidates:

        temp = df[
            [
                "movie_title",
                column
            ]
        ].copy()

        temp[column] = pd.to_numeric(
            temp[column],
            errors="coerce"
        )

        temp = (
            temp
            .dropna()
            .sort_values(
                column,
                ascending=False
            )
            .head(10)
        )

        if len(temp) > 0:

            print(
                f"\nTop movies by {column}:"
            )

            print(
                temp.to_string(
                    index=False
                )
            )

            plt.figure(
                figsize=(10, 6)
            )

            sns.barplot(
                data=temp,
                x=column,
                y="movie_title"
            )

            plt.title(
                f"Top 10 Movies by {column}"
            )

            plt.xlabel(
                column
            )

            plt.ylabel(
                "Movie"
            )

            plt.tight_layout()

            safe_name = (
                column
                .replace("/", "_")
                .replace(" ", "_")
            )

            plt.savefig(
                os.path.join(
                    OUTPUT_DIR,
                    f"top_10_{safe_name}.png"
                )
            )

            plt.close()


# ============================================================
# STEP 14 - CORRELATION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("STEP 14 - CORRELATION ANALYSIS")
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
            OUTPUT_DIR,
            "eda_correlation_matrix.csv"
        )
    )

    plt.figure(
        figsize=(12, 8)
    )

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )

    plt.title(
        "Correlation Between Numeric Movie Features"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "correlation_heatmap.png"
        )
    )

    plt.close()


# ============================================================
# STEP 15 - DATASET PROFILE
# ============================================================

print("\n" + "=" * 70)
print("STEP 15 - DATASET PROFILE")
print("=" * 70)

profile = {
    "total_rows": len(df),
    "total_columns": len(df.columns),
    "unique_movies": (
        df["movie_title"].nunique()
        if "movie_title" in df.columns
        else "N/A"
    ),
    "duplicate_rows": (
        df.duplicated().sum()
    ),
    "total_missing_values": (
        df.isnull().sum().sum()
    )
}

profile_df = pd.DataFrame(
    [
        profile
    ]
)

print(
    profile_df
)

profile_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "eda_dataset_profile.csv"
    ),
    index=False
)


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 70)

print(
    "\nEDA reports and graphs saved in:"
)

print(
    OUTPUT_DIR
)

print("\nGenerated files:")

for file in sorted(
    os.listdir(OUTPUT_DIR)
):

    print(
        " -",
        file
    )

print(
    "\nNext step: Interpret EDA findings and identify new insights "
    "introduced by API data fusion."
)