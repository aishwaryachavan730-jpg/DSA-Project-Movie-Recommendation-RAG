import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

# ============================================================
# STEP 1 — LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

INPUT_FILE = "DataSet/fused_movies.csv"
OUTPUT_FILE = "DataSet/fused_movies.csv"
TMDB_FILE = "DataSet/TMDB_movie_dataset_v11.csv"

print("=" * 70)
print("FIXING 50-MOVIE FUSED DATASET")
print("=" * 70)

if not OMDB_API_KEY:
    raise ValueError(
        "OMDB_API_KEY not found in .env file"
    )

print("OMDb API key found.")


# ============================================================
# STEP 2 — LOAD CURRENT FUSED DATASET
# ============================================================

print("\nLoading fused dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Current movies: {len(df)}")

if len(df) != 50:
    print(
        f"WARNING: Expected 50 movies, but found {len(df)} movies."
    )


# ============================================================
# STEP 3 — LOAD ORIGINAL TMDB DATASET
# ============================================================

print("\nLoading original TMDB dataset...")

tmdb = pd.read_csv(
    TMDB_FILE,
    usecols=lambda c: c in [
        "title",
        "release_date",
        "imdb_id"
    ]
)

print(f"TMDB records loaded: {len(tmdb)}")


# ============================================================
# STEP 4 — CLEAN TMDB TITLES
# ============================================================

df["title"] = df["title"].astype(str).str.strip()

tmdb["title"] = (
    tmdb["title"]
    .astype(str)
    .str.strip()
)

# Remove duplicate titles
tmdb = tmdb.drop_duplicates(
    subset=["title"],
    keep="first"
)


# ============================================================
# STEP 5 — MERGE TMDB RELEASE DATE
# ============================================================

df = df.merge(
    tmdb,
    on="title",
    how="left",
    suffixes=("", "_tmdb")
)

print("\nTMDB release dates matched.")


# ============================================================
# STEP 6 — FIX YEAR
# ============================================================

df["year"] = pd.to_datetime(
    df["release_date"],
    errors="coerce"
).dt.year

print("\nCorrected years:")
print("-" * 70)

print(
    df[
        ["title", "year"]
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# STEP 7 — OMDb API FUNCTION
# ============================================================

def get_omdb_movie(title, year):

    url = "https://www.omdbapi.com/"

    params = {
        "apikey": OMDB_API_KEY,
        "t": title,
        "y": int(year) if pd.notna(year) else "",
        "type": "movie",
        "plot": "full"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if data.get("Response") == "True":

            return data

        print(
            f"  OMDb did not find: {title} ({year})"
        )

    except requests.exceptions.RequestException as e:

        print(
            f"  OMDb request error for {title}: {e}"
        )

    except Exception as e:

        print(
            f"  OMDb error for {title}: {e}"
        )

    return {}


# ============================================================
# STEP 8 — FETCH OMDb DATA
# ============================================================

omdb_results = []

print("\n")
print("=" * 70)
print("FETCHING OMDb INFORMATION")
print("=" * 70)

for index, row in df.iterrows():

    title = row["title"]
    year = row["year"]

    print(
        f"[{index + 1}/{len(df)}] {title} ({year})"
    )

    data = get_omdb_movie(
        title,
        year
    )

    omdb_results.append(data)

    # Small delay to avoid excessive requests
    time.sleep(0.3)


# ============================================================
# STEP 9 — EXTRACT OMDb FIELDS
# ============================================================

df["imdb_rating"] = [
    data.get("imdbRating")
    if data
    else None
    for data in omdb_results
]

df["director"] = [
    data.get("Director")
    if data
    else None
    for data in omdb_results
]

df["actors"] = [
    data.get("Actors")
    if data
    else None
    for data in omdb_results
]

df["awards"] = [
    data.get("Awards")
    if data
    else None
    for data in omdb_results
]


# ============================================================
# STEP 10 — CONVERT IMDb RATING TO NUMBER
# ============================================================

df["imdb_rating"] = pd.to_numeric(
    df["imdb_rating"],
    errors="coerce"
)


# ============================================================
# STEP 11 — CLEAN EMPTY VALUES
# ============================================================

# Convert empty strings to NaN
df = df.replace(
    r"^\s*$",
    pd.NA,
    regex=True
)


# ============================================================
# STEP 12 — REMOVE TEMPORARY TMDB COLUMNS
# ============================================================

df.drop(
    columns=[
        "release_date",
        "imdb_id"
    ],
    errors="ignore",
    inplace=True
)


# ============================================================
# STEP 13 — SAVE FIXED DATASET
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)


# ============================================================
# STEP 14 — FINAL REPORT
# ============================================================

print("\n")
print("=" * 70)
print("DATASET FIXED SUCCESSFULLY")
print("=" * 70)

print(f"Movies: {len(df)}")
print(f"Output: {OUTPUT_FILE}")


# ============================================================
# STEP 15 — MISSING VALUES
# ============================================================

print("\nMissing values:")

print(
    df[
        [
            "year",
            "imdb_rating",
            "director",
            "actors",
            "awards"
        ]
    ].isnull().sum()
)


# ============================================================
# STEP 16 — SHOW PROBLEMATIC RECORDS
# ============================================================

print("\nMovies with missing OMDb information:")

missing_rows = df[
    df[
        [
            "imdb_rating",
            "director",
            "actors",
            "awards"
        ]
    ].isnull().any(axis=1)
]

if len(missing_rows) == 0:

    print("None — all OMDb fields are available.")

else:

    print(
        missing_rows[
            [
                "title",
                "year",
                "imdb_rating",
                "director",
                "actors",
                "awards"
            ]
        ]
        .to_string(index=False)
    )


# ============================================================
# STEP 17 — SHOW FIRST 10 MOVIES
# ============================================================

print("\nFirst 10 movies:")

print(
    df[
        [
            "title",
            "year",
            "tmdb_rating",
            "imdb_rating",
            "director"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# STEP 18 — VERIFY SPECIAL MOVIES
# ============================================================

print("\n")
print("=" * 70)
print("VERIFYING PREVIOUSLY PROBLEMATIC MOVIES")
print("=" * 70)

check_titles = [
    "Harry Potter and the Philosopher's Stone",
    "Se7en"
]

check = df[
    df["title"].isin(check_titles)
]

if len(check) > 0:

    print(
        check[
            [
                "title",
                "year",
                "imdb_rating",
                "director",
                "actors",
                "awards"
            ]
        ]
        .to_string(index=False)
    )


# ============================================================
# FINISHED
# ============================================================

print("\n")
print("=" * 70)
print("STEP COMPLETED")
print("=" * 70)

print("""
Your 50-movie fused dataset has been updated.

Next:
1. Verify missing values
2. Re-run EDA
3. Data Cleaning
4. Generate embeddings
5. Build FAISS index
6. Connect RAG
""")