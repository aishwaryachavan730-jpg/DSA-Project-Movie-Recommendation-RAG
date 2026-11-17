
import os
import pandas as pd
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


# ============================================================
# MOVIEVERSE AI - FUSED DATASET RAG RETRIEVER
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATASET_PATH = os.path.join(
    PROJECT_ROOT,
    "fused_data",
    "movie_fused_18_columns.csv"
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K = 5


# ============================================================
# LOAD DATASET
# ============================================================

print("=" * 65)
print("MOVIEVERSE AI - FUSED DATASET RAG RETRIEVER")
print("=" * 65)

if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(
        f"Fused dataset not found: {DATASET_PATH}"
    )

df = pd.read_csv(DATASET_PATH)

if "movie_title" not in df.columns:
    raise ValueError(
        "Dataset must contain a movie_title column."
    )

print("Dataset loaded:", len(df), "movies")


# ============================================================
# CREATE MOVIE DOCUMENTS
# ============================================================

def create_movie_text(row):

    parts = []

    for column in df.columns:

        value = row[column]

        if pd.isna(value):
            continue

        value = str(value).strip()

        if value:
            parts.append(f"{column}: {value}")

    return "\n".join(parts)


documents = [
    create_movie_text(row)
    for _, row in df.iterrows()
]

print("Documents created:", len(documents))


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("\nLoading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded successfully.")


# ============================================================
# GENERATE EMBEDDINGS
# ============================================================

print("\nGenerating movie embeddings...")

embeddings = model.encode(
    documents,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)

embeddings = embeddings.astype("float32")


# ============================================================
# CREATE FAISS INDEX
# ============================================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

print("\nFAISS index created successfully.")
print("FAISS vectors:", index.ntotal)
print("Vector dimension:", index.d)


# ============================================================
# RETRIEVE MOVIES
# ============================================================

def retrieve_movies(query, top_k=5):

    if not query or not query.strip():
        return []

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    query_embedding = query_embedding.astype("float32")

    search_count = min(top_k, len(df))

    similarities, indices = index.search(
        query_embedding,
        search_count
    )

    results = []

    for similarity, movie_index in zip(
        similarities[0],
        indices[0]
    ):

        if movie_index < 0:
            continue

        movie = df.iloc[int(movie_index)].to_dict()

        movie["_similarity_score"] = float(similarity)

        results.append(movie)

    return results


# ============================================================
# BUILD RAG CONTEXT
# ============================================================

def build_rag_context(query, top_k=5):

    results = retrieve_movies(query, top_k)

    if not results:
        return "", []

    context_parts = []

    for rank, movie in enumerate(results, start=1):

        movie_details = []

        for key, value in movie.items():

            if key == "_similarity_score":
                continue

            if pd.isna(value):
                continue

            movie_details.append(
                f"{key}: {value}"
            )

        context_parts.append(
            f"MOVIE RESULT {rank}\n"
            f"Similarity: {movie['_similarity_score']:.4f}\n"
            + "\n".join(movie_details)
        )

    context = "\n\n".join(context_parts)

    return context, results


# ============================================================
# TEST FIVE QUERIES
# ============================================================

if __name__ == "__main__":

    test_queries = [
        "science fiction movie about space",
        "romantic love story movies",
        "action movies with superheroes",
        "movies directed by Christopher Nolan",
        "thriller movies with mystery"
    ]

    for query in test_queries:

        print("\n" + "=" * 65)
        print("USER QUERY:", query)
        print("=" * 65)

        results = retrieve_movies(query, TOP_K)

        if not results:
            print("No movies found.")
            continue

        for rank, movie in enumerate(results, start=1):

            print(
                f"\n{rank}. "
                f"{movie.get('movie_title', 'Unknown')}"
            )

            print(
                "   Genre:",
                movie.get("genres", "N/A")
            )

            print(
                "   TMDB Rating:",
                movie.get("tmdb_rating", "N/A")
            )

            print(
                "   IMDb Rating:",
                movie.get("imdb_rating", "N/A")
            )

            print(
                "   Similarity:",
                f"{movie['_similarity_score']:.4f}"
            )

            print(
                "   Director:",
                movie.get("director", "N/A")
            )

    print("\n" + "=" * 65)
    print("ALL FIVE RETRIEVAL TESTS COMPLETED")
    print("=" * 65)
