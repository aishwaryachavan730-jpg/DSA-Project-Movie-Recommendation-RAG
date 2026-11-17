import pandas as pd
import os
import json


INPUT_FILE = "DataSet/TMDB_movie_dataset_v11.csv"
OUTPUT_FILE = "DataSet/fused_movies.csv"


def create_fused_record(row):

    return {
        "title": row.get("title", ""),
        "year": str(row.get("release_date", ""))[:4],
        "tmdb_rating": row.get("vote_average", ""),
        "imdb_rating": "",
        "genre": row.get("genres", ""),
        "overview": row.get("overview", ""),
        "director": "",
        "actors": "",
        "awards": "",
        "watchmode_data": json.dumps({}, ensure_ascii=False),
        "news_data": json.dumps({}, ensure_ascii=False)
    }


print("DATA FUSION - 50 MOVIES")
print("=" * 50)

# Load TMDB dataset
df = pd.read_csv(INPUT_FILE)

print(f"Original movies: {len(df)}")

# Remove movies without title
df = df.dropna(subset=["title"])

# Remove duplicate titles
df = df.drop_duplicates(subset=["title"])

# Select first 50 different movies
movies_50 = df.head(50)

records = []

for _, row in movies_50.iterrows():

    record = create_fused_record(row)

    records.append(record)


# Create output directory
os.makedirs("DataSet", exist_ok=True)

# Save fused dataset
fused_df = pd.DataFrame(records)

fused_df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)

print("=" * 50)
print("FUSED DATASET CREATED")
print(f"Number of movies: {len(fused_df)}")
print(f"Saved to: {OUTPUT_FILE}")
print("=" * 50)

print("\nFirst 10 movies:")
print(fused_df[["title", "year", "tmdb_rating"]].head(10))