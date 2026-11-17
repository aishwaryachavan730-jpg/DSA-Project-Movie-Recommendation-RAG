import pandas as pd
import os

INPUT_FILE = "DataSet/fused_movies.csv"
OUTPUT_FILE = "DataSet/cleaned_movies.csv"

print("=" * 60)
print("STEP 8.1 - DATA CLEANING")
print("=" * 60)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print(f"\nOriginal rows: {len(df)}")
print(f"Original columns: {len(df.columns)}")

# ---------------------------------------------------------
# REMOVE DUPLICATES
# ---------------------------------------------------------

before = len(df)

df = df.drop_duplicates(subset=["title"])

after = len(df)

print(f"\nDuplicate movies removed: {before - after}")

# ---------------------------------------------------------
# CLEAN TEXT COLUMNS
# ---------------------------------------------------------

text_columns = [
    "title",
    "genre",
    "overview",
    "director",
    "actors",
    "awards",
    "watchmode_data",
    "news_data"
]

for column in text_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

# ---------------------------------------------------------
# CLEAN NUMERIC COLUMNS
# ---------------------------------------------------------

numeric_columns = [
    "year",
    "tmdb_rating",
    "imdb_rating"
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

# ---------------------------------------------------------
# HANDLE MISSING VALUES
# ---------------------------------------------------------

# Keep missing IMDb rating as 0
# because one movie does not have valid OMDb data.

df["imdb_rating"] = df["imdb_rating"].fillna(0)

# Missing TMDB rating
df["tmdb_rating"] = df["tmdb_rating"].fillna(0)

# Missing year
df["year"] = df["year"].fillna(0).astype(int)

# ---------------------------------------------------------
# CREATE SEARCH TEXT
# ---------------------------------------------------------

df["movie_text"] = (
    "Title: " + df["title"] +
    ". Year: " + df["year"].astype(str) +
    ". Genre: " + df["genre"] +
    ". Overview: " + df["overview"] +
    ". Director: " + df["director"] +
    ". Actors: " + df["actors"] +
    ". Awards: " + df["awards"] +
    ". TMDB Rating: " + df["tmdb_rating"].astype(str) +
    ". IMDb Rating: " + df["imdb_rating"].astype(str)
)

# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

os.makedirs("DataSet", exist_ok=True)

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED")
print("=" * 60)

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print(f"\nSaved to:")
print(OUTPUT_FILE)

print("\nColumns:")
for column in df.columns:
    print("-", column)

print("\nFirst movie text:")
print(df["movie_text"].iloc[0])