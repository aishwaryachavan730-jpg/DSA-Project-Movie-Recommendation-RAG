import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATASET_PATH = os.path.join(
    PROJECT_ROOT,
    "fused_data",
    "movie_fused_18_columns.csv"
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "eda",
    "eda_outputs"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# LOAD DATASET
# ============================================================

print("=" * 70)
print("MOVIEVERSE AI - FUSED DATASET EDA")
print("=" * 70)

print("\nDataset path:")
print(DATASET_PATH)


if not os.path.exists(DATASET_PATH):

    raise FileNotFoundError(
        f"\nDataset not found:\n{DATASET_PATH}"
    )


df = pd.read_csv(
    DATASET_PATH
)


print("\nDataset loaded successfully.")

print(
    "Rows:",
    df.shape[0]
)

print(
    "Columns:",
    df.shape[1]
)


# ============================================================
# COLUMN INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("COLUMN NAMES")
print("=" * 70)

for i, column in enumerate(
    df.columns,
    start=1
):

    print(
        f"{i}. {column}"
    )


# ============================================================
# DATA TYPES
# ============================================================

print("\n" + "=" * 70)
print("DATA TYPES")
print("=" * 70)

print(
    df.dtypes
)


# ============================================================
# MISSING VALUES
# ============================================================

print("\n" + "=" * 70)
print("MISSING VALUE ANALYSIS")
print("=" * 70)

missing_count = df.isnull().sum()

missing_percentage = (
    missing_count /
    len(df)
) * 100


missing_df = pd.DataFrame({

    "Missing_Values":
        missing_count,

    "Missing_Percentage":
        missing_percentage.round(2)

})


missing_df = missing_df[
    missing_df["Missing_Values"] > 0
]


if len(missing_df) == 0:

    print(
        "No missing values found."
    )

else:

    print(
        missing_df.sort_values(
            "Missing_Values",
            ascending=False
        )
    )


missing_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "missing_values.csv"
    )
)


# ============================================================
# DUPLICATES
# ============================================================

print("\n" + "=" * 70)
print("DUPLICATE ANALYSIS")
print("=" * 70)

duplicate_count = df.duplicated().sum()

print(
    "Duplicate rows:",
    duplicate_count
)


# ============================================================
# UNIQUE VALUES
# ============================================================

print("\n" + "=" * 70)
print("UNIQUE VALUE ANALYSIS")
print("=" * 70)

for column in df.columns:

    print(
        f"{column}: {df[column].nunique(dropna=True)} unique values"
    )


# ============================================================
# NUMERICAL COLUMNS
# ============================================================

numeric_columns = df.select_dtypes(
    include=np.number
).columns.tolist()


print("\n" + "=" * 70)
print("NUMERICAL COLUMNS")
print("=" * 70)

print(
    numeric_columns
)


# ============================================================
# DESCRIPTIVE STATISTICS
# ============================================================

if len(numeric_columns) > 0:

    print("\n" + "=" * 70)
    print("DESCRIPTIVE STATISTICS")
    print("=" * 70)

    statistics = df[
        numeric_columns
    ].describe().T

    statistics["median"] = (
        df[numeric_columns]
        .median()
    )

    statistics = statistics[
        [
            "count",
            "mean",
            "median",
            "std",
            "min",
            "25%",
            "50%",
            "75%",
            "max"
        ]
    ]

    print(
        statistics
    )

    statistics.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "descriptive_statistics.csv"
        )
    )


# ============================================================
# FIND MOVIE TITLE COLUMN
# ============================================================

title_candidates = [

    "title",
    "movie_title",
    "Movie Title",
    "movie title",
    "Title"

]


title_column = None


for column in title_candidates:

    if column in df.columns:

        title_column = column

        break


print("\nMovie title column:")

print(
    title_column
)


# ============================================================
# FIND GENRE COLUMN
# ============================================================

genre_candidates = [

    "genre",
    "genres",
    "Genre",
    "Genres"

]


genre_column = None


for column in genre_candidates:

    if column in df.columns:

        genre_column = column

        break


print(
    "Genre column:",
    genre_column
)


# ============================================================
# GENRE ANALYSIS
# ============================================================

if genre_column is not None:

    print("\n" + "=" * 70)
    print("GENRE ANALYSIS")
    print("=" * 70)


    genre_series = (
        df[genre_column]
        .dropna()
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
    )


    genre_counts = (
        genre_series
        .value_counts()
        .head(15)
    )


    print(
        genre_counts
    )


    genre_counts.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "top_genres.csv"
        )
    )


    plt.figure(
        figsize=(10, 6)
    )

    genre_counts.sort_values().plot(
        kind="barh"
    )

    plt.title(
        "Top 15 Movie Genres"
    )

    plt.xlabel(
        "Number of Movies"
    )

    plt.ylabel(
        "Genre"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "genre_distribution.png"
        ),
        dpi=300
    )

    plt.close()


# ============================================================
# NUMERICAL DISTRIBUTION
# ============================================================

for column in numeric_columns:

    values = df[column].dropna()

    if len(values) == 0:

        continue


    plt.figure(
        figsize=(8, 5)
    )

    plt.hist(
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
        "Frequency"
    )

    plt.tight_layout()

    safe_name = (
        str(column)
        .replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
    )


    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            f"hist_{safe_name}.png"
        ),
        dpi=300
    )

    plt.close()


# ============================================================
# BOXPLOTS
# ============================================================

for column in numeric_columns:

    values = df[column].dropna()

    if len(values) == 0:

        continue


    plt.figure(
        figsize=(8, 5)
    )

    plt.boxplot(
        values
    )

    plt.title(
        f"Boxplot of {column}"
    )

    plt.ylabel(
        column
    )

    plt.tight_layout()


    safe_name = (
        str(column)
        .replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
    )


    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            f"box_{safe_name}.png"
        ),
        dpi=300
    )

    plt.close()


# ============================================================
# CORRELATION
# ============================================================

if len(numeric_columns) >= 2:

    print("\n" + "=" * 70)
    print("CORRELATION ANALYSIS")
    print("=" * 70)


    correlation = df[
        numeric_columns
    ].corr()


    print(
        correlation.round(4)
    )


    correlation.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "correlation_matrix.csv"
        )
    )


    plt.figure(
        figsize=(12, 10)
    )


    plt.imshow(
        correlation,
        interpolation="nearest"
    )


    plt.colorbar()


    plt.xticks(
        range(len(correlation.columns)),
        correlation.columns,
        rotation=90
    )


    plt.yticks(
        range(len(correlation.columns)),
        correlation.columns
    )


    plt.title(
        "Movie Dataset Correlation Heatmap"
    )


    plt.tight_layout()


    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "correlation_heatmap.png"
        ),
        dpi=300
    )


    plt.close()


# ============================================================
# TOP MOVIES BY NUMERICAL FEATURES
# ============================================================

if title_column is not None:

    for column in numeric_columns:

        top_movies = (
            df[
                [title_column, column]
            ]
            .dropna()
            .sort_values(
                column,
                ascending=False
            )
            .head(15)
        )


        if len(top_movies) == 0:

            continue


        safe_name = (
            str(column)
            .replace("/", "_")
            .replace("\\", "_")
            .replace(" ", "_")
        )


        top_movies.to_csv(
            os.path.join(
                OUTPUT_DIR,
                f"top_movies_{safe_name}.csv"
            ),
            index=False
        )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 70)

print(
    "\nRows:",
    df.shape[0]
)

print(
    "Columns:",
    df.shape[1]
)

print(
    "Duplicate rows:",
    duplicate_count
)

print(
    "Numerical columns:",
    len(numeric_columns)
)

print(
    "\nEDA output folder:"
)

print(
    OUTPUT_DIR
)

print(
    "\nGenerated files:"
)

if os.path.exists(OUTPUT_DIR):

    for file in os.listdir(
        OUTPUT_DIR
    ):

        print(
            " -",
            file
        )