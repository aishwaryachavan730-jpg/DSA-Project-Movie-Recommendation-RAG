import os
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer

# ============================================================
# STEP 9 - RAG RETRIEVAL PIPELINE
# ============================================================

print("=" * 60)
print("STEP 9 - RAG RETRIEVAL PIPELINE")
print("=" * 60)

# ------------------------------------------------------------
# FILE PATHS
# ------------------------------------------------------------

CSV_FILE = "DataSet/cleaned_movies.csv"
INDEX_FILE = "DataSet/movies.index"

# ------------------------------------------------------------
# LOAD DATASET
# ------------------------------------------------------------

print("\nLoading movie dataset...")

df = pd.read_csv(CSV_FILE)

print(f"Movies loaded: {len(df)}")

# ------------------------------------------------------------
# LOAD FAISS INDEX
# ------------------------------------------------------------

print("\nLoading FAISS index...")

index = faiss.read_index(INDEX_FILE)

print(f"FAISS vectors: {index.ntotal}")
print(f"Vector dimension: {index.d}")

# ------------------------------------------------------------
# LOAD EMBEDDING MODEL
# ------------------------------------------------------------

print("\nLoading embedding model...")

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded successfully.")

# ------------------------------------------------------------
# RETRIEVAL FUNCTION
# ------------------------------------------------------------

def retrieve_movies(query, top_k=5):

    print("\n" + "=" * 60)
    print(f"USER QUERY: {query}")
    print("=" * 60)

    # Convert query into embedding
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    # Search FAISS
    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for rank, (idx, score) in enumerate(
        zip(indices[0], distances[0]),
        start=1
    ):

        if idx == -1:
            continue

        movie = df.iloc[idx]

        results.append({
            "rank": rank,
            "title": movie["title"],
            "year": movie["year"],
            "genre": movie["genre"],
            "overview": movie["overview"],
            "director": movie["director"],
            "actors": movie["actors"],
            "tmdb_rating": movie["tmdb_rating"],
            "imdb_rating": movie["imdb_rating"],
            "similarity": float(score)
        })

    return results


# ------------------------------------------------------------
# DISPLAY RESULTS
# ------------------------------------------------------------

def display_results(results):

    print("\nTop Recommendations:")
    print("-" * 60)

    for movie in results:

        print(
            f"{movie['rank']}. "
            f"{movie['title']} "
            f"({int(movie['year'])})"
        )

        print(
            f"   Genre: {movie['genre']}"
        )

        print(
            f"   TMDB: {movie['tmdb_rating']}"
        )

        print(
            f"   IMDb: {movie['imdb_rating']}"
        )

        print(
            f"   Similarity: "
            f"{movie['similarity']:.4f}"
        )

        print(
            f"   Director: "
            f"{movie['director']}"
        )

        print()


# ------------------------------------------------------------
# TEST QUERIES
# ------------------------------------------------------------

queries = [
    "science fiction movie about space",
    "superhero action movie",
    "crime thriller with a serial killer",
    "movie about dreams and mind",
    "fantasy adventure movie"
]

for query in queries:

    results = retrieve_movies(
        query,
        top_k=5
    )

    display_results(results)


# ------------------------------------------------------------
# INTERACTIVE MODE
# ------------------------------------------------------------

print("=" * 60)
print("INTERACTIVE MOVIE RETRIEVAL")
print("=" * 60)

print("Type 'exit' to stop.")

while True:

    query = input("\nEnter your movie request: ")

    if query.lower().strip() == "exit":
        print("\nRAG retrieval stopped.")
        break

    if not query.strip():
        print("Please enter a movie request.")
        continue

    results = retrieve_movies(
        query,
        top_k=5
    )

    display_results(results)


print("=" * 60)
print("STEP 9 COMPLETED")
print("=" * 60)