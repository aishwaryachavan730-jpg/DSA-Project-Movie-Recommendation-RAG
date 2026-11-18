import os
import pandas as pd


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

OUTPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "fused_data",
    "movie_rag_context.csv"
)


# ============================================================
# CHECK FILE
# ============================================================

if not os.path.exists(INPUT_FILE):

    print("=" * 70)
    print("ERROR: FUSED CSV NOT FOUND")
    print("=" * 70)

    print(INPUT_FILE)

    raise SystemExit


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("MOVIEVERSE AI - RAG DATA PREPARATION")
print("=" * 70)

df = pd.read_csv(
    INPUT_FILE,
    low_memory=False
)

print()
print("Input file:")
print(INPUT_FILE)

print()
print("Rows:", len(df))
print("Columns:", len(df.columns))

print()
print("Columns:")
for column in df.columns:
    print(" -", column)


# ============================================================
# CHECK MOVIE TITLE
# ============================================================

if "movie_title" not in df.columns:

    if "title" in df.columns:

        df["movie_title"] = df["title"]

    else:

        raise ValueError(
            "movie_title or title column not found."
        )


# ============================================================
# REMOVE EMPTY TITLES
# ============================================================

df["movie_title"] = (
    df["movie_title"]
    .fillna("")
    .astype(str)
    .str.strip()
)

df = df[
    df["movie_title"] != ""
].copy()


# ============================================================
# REMOVE DUPLICATE MOVIES
# ============================================================

df = df.drop_duplicates(
    subset=["movie_title"]
)


# ============================================================
# SELECT USEFUL INFORMATION
# ============================================================

possible_columns = [

    "movie_title",

    "title",

    "overview",

    "release_date",

    "vote_average",

    "vote_count",

    "rating",

    "imdb_rating",

    "year",

    "runtime",

    "director",

    "actors",

    "genre",

    "genres",

    "awards",

    "plot",

    "streaming_services",

    "streaming_sources",

    "news",

    "news_title",

    "news_description",

    "wikipedia_summary",

    "wikipedia_description",

    "wikipedia_url"
]


available_columns = []

for column in possible_columns:

    if column in df.columns:

        if column not in available_columns:

            available_columns.append(column)


# ============================================================
# CREATE RAG DATASET
# ============================================================

rag_df = df[
    available_columns
].copy()


# ============================================================
# CREATE TEXT CONTEXT
# ============================================================

def safe_value(row, column):

    if column not in row.index:

        return "Not available"

    value = row[column]

    if pd.isna(value):

        return "Not available"

    value = str(value).strip()

    if not value:

        return "Not available"

    return value


def create_context(row):

    title = safe_value(
        row,
        "movie_title"
    )

    context = f"""
MOVIE TITLE:
{title}

TMDB INFORMATION:
Overview: {safe_value(row, "overview")}
Release Date: {safe_value(row, "release_date")}
TMDB Rating: {safe_value(row, "vote_average")}
Vote Count: {safe_value(row, "vote_count")}

OMDb / IMDb INFORMATION:
IMDb Rating: {safe_value(row, "imdb_rating")}
Year: {safe_value(row, "year")}
Runtime: {safe_value(row, "runtime")}
Director: {safe_value(row, "director")}
Actors: {safe_value(row, "actors")}
Genre: {safe_value(row, "genre")}
Awards: {safe_value(row, "awards")}
Plot: {safe_value(row, "plot")}

WATCHMODE INFORMATION:
Streaming Services: {safe_value(row, "streaming_services")}
Streaming Sources: {safe_value(row, "streaming_sources")}

NEWS API INFORMATION:
News: {safe_value(row, "news")}
News Title: {safe_value(row, "news_title")}
News Description: {safe_value(row, "news_description")}

WIKIPEDIA INFORMATION:
Description: {safe_value(row, "wikipedia_description")}
Summary: {safe_value(row, "wikipedia_summary")}
Wikipedia URL: {safe_value(row, "wikipedia_url")}
""".strip()

    return context


rag_df["rag_context"] = rag_df.apply(
    create_context,
    axis=1
)


# ============================================================
# SAVE
# ============================================================

rag_df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# RESULT
# ============================================================

print()
print("=" * 70)
print("RAG DATA PREPARATION COMPLETED")
print("=" * 70)

print()
print("RAG rows:", len(rag_df))
print("RAG columns:", len(rag_df.columns))

print()
print("Output:")
print(OUTPUT_FILE)

print()
print("Sample RAG context:")
print("-" * 70)

if len(rag_df) > 0:

    print(
        rag_df.iloc[0]["rag_context"]
    )

print()
print("=" * 70)