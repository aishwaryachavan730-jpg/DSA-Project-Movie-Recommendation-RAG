# ============================================================
# MOVIEVERSE AI
# DATA QUALITY ASSESSMENT
# 18-COLUMN FUSED DATASET
# ============================================================

import pandas as pd
import numpy as np
import os


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# INPUT FILE
# ============================================================

INPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "fused_data",
    "movie_fused_18_columns.csv"
)


# ============================================================
# OUTPUT FILES
# ============================================================

QUALITY_CSV = os.path.join(
    PROJECT_ROOT,
    "data_quality_report.csv"
)

QUALITY_EXCEL = os.path.join(
    PROJECT_ROOT,
    "data_quality_report.xlsx"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("MOVIEVERSE AI - DATA QUALITY ASSESSMENT")
print("=" * 70)


# ============================================================
# CHECK FILE
# ============================================================

if not os.path.exists(INPUT_FILE):

    print("\nERROR: FUSED CSV FILE NOT FOUND")

    print("\nExpected file:")
    print(INPUT_FILE)

    print(
        "\nPlease keep movie_fused_18_columns.csv "
        "inside the project root."
    )

    exit()


# ============================================================
# LOAD DATA
# ============================================================

print("\nLoading fused dataset...")

df = pd.read_csv(
    INPUT_FILE
)


# ============================================================
# BASIC INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("1. BASIC DATASET INFORMATION")
print("=" * 70)

print(
    f"\nRows    : {df.shape[0]}"
)

print(
    f"Columns : {df.shape[1]}"
)

print("\nColumns:")

for column in df.columns:

    print(
        f" - {column}"
    )


# ============================================================
# DATA TYPES
# ============================================================

print("\n" + "=" * 70)
print("2. DATA TYPES")
print("=" * 70)

print(
    df.dtypes
)


# ============================================================
# UNIQUE MOVIE TITLES
# ============================================================

print("\n" + "=" * 70)
print("3. UNIQUE MOVIE TITLES")
print("=" * 70)

unique_titles = df[
    "movie_title"
].nunique()

print(
    f"\nUnique movie titles: {unique_titles}"
)


# ============================================================
# DUPLICATE ROWS
# ============================================================

print("\n" + "=" * 70)
print("4. DUPLICATE ROW CHECK")
print("=" * 70)

duplicate_rows = df.duplicated().sum()

print(
    f"\nDuplicate rows: {duplicate_rows}"
)


# ============================================================
# DUPLICATE MOVIE TITLES
# ============================================================

print("\n" + "=" * 70)
print("5. DUPLICATE MOVIE TITLE CHECK")
print("=" * 70)

duplicate_titles = df[
    "movie_title"
].duplicated().sum()

print(
    f"\nDuplicate movie titles: {duplicate_titles}"
)


# ============================================================
# MISSING VALUES
# ============================================================

print("\n" + "=" * 70)
print("6. MISSING VALUE ANALYSIS")
print("=" * 70)

missing_count = df.isnull().sum()

missing_percentage = (
    df.isnull().mean() * 100
)


missing_report = pd.DataFrame({

    "column": df.columns,

    "missing_count":
        missing_count.values,

    "missing_percentage":
        missing_percentage.values

})


print(
    missing_report.to_string(
        index=False
    )
)


# ============================================================
# EMPTY STRING CHECK
# ============================================================

print("\n" + "=" * 70)
print("7. EMPTY STRING CHECK")
print("=" * 70)

empty_report = []

for column in df.columns:

    empty_count = (
        df[column]
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    empty_report.append({

        "column": column,

        "empty_string_count":
            empty_count
    })


empty_df = pd.DataFrame(
    empty_report
)

print(
    empty_df.to_string(
        index=False
    )
)


# ============================================================
# NUMERIC COLUMN ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("8. NUMERIC COLUMN ANALYSIS")
print("=" * 70)


numeric_columns = [
    "tmdb_rating",
    "vote_count",
    "popularity",
    "imdb_rating",
    "news_count"
]


numeric_report = []


for column in numeric_columns:

    if column not in df.columns:
        continue

    series = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    numeric_report.append({

        "column": column,

        "count": series.count(),

        "mean": series.mean(),

        "median": series.median(),

        "minimum": series.min(),

        "maximum": series.max(),

        "std": series.std(),

        "missing":
            series.isnull().sum()

    })


numeric_df = pd.DataFrame(
    numeric_report
)


print(
    numeric_df.to_string(
        index=False
    )
)


# ============================================================
# OUTLIER ANALYSIS - IQR
# ============================================================

print("\n" + "=" * 70)
print("9. OUTLIER ANALYSIS")
print("=" * 70)


outlier_report = []


for column in numeric_columns:

    if column not in df.columns:
        continue

    series = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()

    if len(series) == 0:
        continue

    Q1 = series.quantile(
        0.25
    )

    Q3 = series.quantile(
        0.75
    )

    IQR = Q3 - Q1

    lower_limit = Q1 - (
        1.5 * IQR
    )

    upper_limit = Q3 + (
        1.5 * IQR
    )

    outliers = series[
        (series < lower_limit)
        |
        (series > upper_limit)
    ]

    outlier_report.append({

        "column": column,

        "Q1": Q1,

        "Q3": Q3,

        "IQR": IQR,

        "lower_limit":
            lower_limit,

        "upper_limit":
            upper_limit,

        "outlier_count":
            len(outliers),

        "outlier_percentage":
            (
                len(outliers)
                /
                len(series)
                *
                100
            )

    })


outlier_df = pd.DataFrame(
    outlier_report
)


print(
    outlier_df.to_string(
        index=False
    )
)


# ============================================================
# TEXT COLUMN SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("10. TEXT COLUMN ANALYSIS")
print("=" * 70)


text_columns = [
    "movie_title",
    "genres",
    "director",
    "actors",
    "awards",
    "streaming_platforms",
    "streaming_region"
]


text_report = []


for column in text_columns:

    if column not in df.columns:
        continue

    text_report.append({

        "column": column,

        "unique_values":
            df[column].nunique(),

        "missing_values":
            df[column].isnull().sum(),

        "non_empty_values":
            (
                df[column]
                .astype(str)
                .str.strip()
                .ne("")
                .sum()
            )

    })


text_df = pd.DataFrame(
    text_report
)


print(
    text_df.to_string(
        index=False
    )
)


# ============================================================
# DATE VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("11. RELEASE DATE VALIDATION")
print("=" * 70)


if "release_date" in df.columns:

    release_dates = pd.to_datetime(
        df["release_date"],
        errors="coerce"
    )

    invalid_dates = (
        release_dates.isnull()
        &
        df["release_date"].notnull()
        &
        (
            df["release_date"]
            .astype(str)
            .str.strip()
            != ""
        )
    ).sum()

    valid_dates = (
        release_dates.notnull()
    ).sum()

    print(
        f"\nValid dates   : {valid_dates}"
    )

    print(
        f"Invalid dates : {invalid_dates}"
    )


# ============================================================
# RATING VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("12. RATING VALIDATION")
print("=" * 70)


if "tmdb_rating" in df.columns:

    tmdb_rating = pd.to_numeric(
        df["tmdb_rating"],
        errors="coerce"
    )

    invalid_tmdb = (
        (tmdb_rating < 0)
        |
        (tmdb_rating > 10)
    ).sum()

    print(
        f"\nInvalid TMDB ratings: "
        f"{invalid_tmdb}"
    )


if "imdb_rating" in df.columns:

    imdb_rating = pd.to_numeric(
        df["imdb_rating"],
        errors="coerce"
    )

    invalid_imdb = (
        (imdb_rating < 0)
        |
        (imdb_rating > 10)
    ).sum()

    print(
        f"Invalid IMDb ratings: "
        f"{invalid_imdb}"
    )


# ============================================================
# NEWS COUNT VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("13. NEWS COUNT VALIDATION")
print("=" * 70)


if "news_count" in df.columns:

    news_count = pd.to_numeric(
        df["news_count"],
        errors="coerce"
    )

    negative_news = (
        news_count < 0
    ).sum()

    print(
        f"\nNegative news counts: "
        f"{negative_news}"
    )


# ============================================================
# FUSION KEY VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("14. PRIMARY / FUSION KEY VALIDATION")
print("=" * 70)


if "movie_title" in df.columns:

    missing_titles = (
        df["movie_title"]
        .isnull()
        .sum()
    )

    blank_titles = (
        df["movie_title"]
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    print(
        f"\nMissing movie titles: "
        f"{missing_titles}"
    )

    print(
        f"Blank movie titles: "
        f"{blank_titles}"
    )

    print(
        "\nFusion key used: movie_title"
    )


# ============================================================
# OVERALL QUALITY SCORE
# ============================================================

print("\n" + "=" * 70)
print("15. OVERALL DATA QUALITY SUMMARY")
print("=" * 70)


total_cells = (
    df.shape[0] *
    df.shape[1]
)

missing_cells = (
    df.isnull().sum().sum()
)


if total_cells > 0:

    completeness = (
        1 -
        (
            missing_cells /
            total_cells
        )
    ) * 100

else:

    completeness = 0


print(
    f"\nTotal cells      : "
    f"{total_cells}"
)

print(
    f"Missing cells    : "
    f"{missing_cells}"
)

print(
    f"Completeness     : "
    f"{completeness:.2f}%"
)

print(
    f"Duplicate rows   : "
    f"{duplicate_rows}"
)

print(
    f"Duplicate titles : "
    f"{duplicate_titles}"
)


# ============================================================
# CREATE FINAL QUALITY REPORT
# ============================================================

quality_summary = pd.DataFrame({

    "Metric": [

        "Total Rows",

        "Total Columns",

        "Unique Movie Titles",

        "Duplicate Rows",

        "Duplicate Movie Titles",

        "Missing Cells",

        "Completeness Percentage",

        "Invalid TMDB Ratings",

        "Invalid IMDb Ratings",

        "Negative News Counts"

    ],

    "Value": [

        df.shape[0],

        df.shape[1],

        unique_titles,

        duplicate_rows,

        duplicate_titles,

        missing_cells,

        round(
            completeness,
            2
        ),

        (
            invalid_tmdb
            if "tmdb_rating"
            in df.columns
            else 0
        ),

        (
            invalid_imdb
            if "imdb_rating"
            in df.columns
            else 0
        ),

        (
            negative_news
            if "news_count"
            in df.columns
            else 0
        )

    ]

})


# ============================================================
# SAVE CSV
# ============================================================

quality_summary.to_csv(
    QUALITY_CSV,
    index=False
)


# ============================================================
# SAVE EXCEL
# ============================================================

with pd.ExcelWriter(
    QUALITY_EXCEL,
    engine="openpyxl"
) as writer:

    quality_summary.to_excel(
        writer,
        sheet_name="Summary",
        index=False
    )

    missing_report.to_excel(
        writer,
        sheet_name="Missing Values",
        index=False
    )

    numeric_df.to_excel(
        writer,
        sheet_name="Numeric Analysis",
        index=False
    )

    outlier_df.to_excel(
        writer,
        sheet_name="Outliers",
        index=False
    )

    text_df.to_excel(
        writer,
        sheet_name="Text Analysis",
        index=False
    )

    empty_df.to_excel(
        writer,
        sheet_name="Empty Strings",
        index=False
    )


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("DATA QUALITY ASSESSMENT COMPLETED")
print("=" * 70)

print(
    f"\nCSV report:"
)

print(
    QUALITY_CSV
)

print(
    f"\nExcel report:"
)

print(
    QUALITY_EXCEL
)

print(
    "\nNext step: EDA on the fused dataset."
)

print("=" * 70)