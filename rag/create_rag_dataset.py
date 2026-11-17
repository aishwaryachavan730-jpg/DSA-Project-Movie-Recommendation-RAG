import os
import pandas as pd


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


INPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "fused_data",
    "movie_fused_18_columns.csv"
)


OUTPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "fused_data",
    "movie_rag_dataset.csv"
)


print("=" * 70)
print("CREATE RAG DATASET")
print("=" * 70)


df = pd.read_csv(
    INPUT_FILE
)


print(
    f"Original rows: {len(df)}"
)


# ------------------------------------------------------------
# Remove duplicate movie titles
# ------------------------------------------------------------

title_column = None


for column in [
    "movie_title",
    "title",
    "Movie Title"
]:

    if column in df.columns:

        title_column = column

        break


if title_column is None:

    raise ValueError(
        "Movie title column not found."
    )


df = df.drop_duplicates(
    subset=[title_column]
)


# ------------------------------------------------------------
# Remove rows without movie title
# ------------------------------------------------------------

df = df[
    df[title_column]
    .notna()
]


# ------------------------------------------------------------
# Keep useful records
# ------------------------------------------------------------

important_columns = [
    title_column
]


for column in df.columns:

    if column not in important_columns:

        if df[column].notna().sum() > 0:

            important_columns.append(
                column
            )


df = df[
    important_columns
]


# ------------------------------------------------------------
# Limit dataset for RAG
# ------------------------------------------------------------

MAX_MOVIES = 10000


if len(df) > MAX_MOVIES:

    df = df.head(
        MAX_MOVIES
    )


# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


print(
    f"\nRAG dataset created:"
)

print(
    OUTPUT_FILE
)

print(
    f"Rows: {len(df)}"
)

print(
    f"Columns: {len(df.columns)}"
)

print(
    "\nSUCCESS"
)