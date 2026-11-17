
import os
from functools import lru_cache

import pandas as pd
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


# ============================================================
# MOVIEVERSE AI - LAZY LOADED FAISS RETRIEVER
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
# CREATE MOVIE DOCUMENT
# ============================================================

def create_movie_text(row, columns):

    parts = []

    for column in columns:

        value = row[column]

        if pd.isna(value):
            continue

        value = str(value).strip()

        if value:
            parts.append(f"{column}: {value}")

    return "\n".join(parts)


# ============================================================
# LOAD DATASET, MODEL AND FAISS INDEX ONCE
# ============================================================

@lru_cache(maxsize=1)
def load_rag_resources():

    print("=" * 60)
    print("MOVIEVERSE AI - LOADING FAISS RESOURCES")
    print("=" * 60)

    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(
            f"Fused dataset not found: {DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH)

    if "movie_title" not in df.columns:
        raise ValueError(
            "Dataset must contain movie_title."
        )

    df = df.dropna(subset=["movie_title"]).reset_index(drop=True)

    print("Movies loaded:", len(df))

    documents = [
        create_movie_text(row, df.columns)
        for _, row in df.iterrows()
    ]

    print("Movie documents:", len(documents))

    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print("Generating embeddings...")

    embeddings = model.encode(
        documents,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    index = faiss.IndexFlatIP(
        embeddings.shape[1]
    )

    index.add(embeddings)

    print("FAISS index created.")
    print("FAISS vectors:", index.ntotal)
    print("Vector dimension:", index.d)

    return df, model, index


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

    # Search the complete index so we can exclude the searched movie
    search_count = len(df)

    similarities, indices = index.search(
        query_embedding,
        search_count
    )

    results = []

    # Normalize the searched title for comparison
    searched_title = query.strip().casefold()

    for similarity, movie_index in zip(
        similarities[0],
        indices[0]
    ):

        if movie_index < 0:
            continue

        movie = df.iloc[int(movie_index)].to_dict()

        movie_title = str(
            movie.get("movie_title", "")
        ).strip().casefold()

        # Exclude the exact searched movie
        if movie_title == searched_title:
            continue

        movie["_similarity_score"] = float(similarity)

        results.append(movie)

        # Stop after collecting the requested alternatives
        if len(results) >= top_k:
            break

    return results


# ============================================================
# BUILD RAG CONTEXT
# ============================================================

def build_rag_context(query, top_k=TOP_K):

    results = retrieve_movies(
        query,
        top_k
    )

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

    return "\n\n".join(context_parts), results


# ============================================================
# TEST RETRIEVER
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

        print("\n" + "=" * 60)
        print("USER QUERY:", query)
        print("=" * 60)

        results = retrieve_movies(
            query,
            TOP_K
        )

        if not results:
            print("No movies found.")
            continue

        for rank, movie in enumerate(results, start=1):

            print(
                f"\n{rank}. {movie.get('movie_title', 'Unknown')}"
            )

            print("Genre:", movie.get("genres", "N/A"))
            print("IMDb:", movie.get("imdb_rating", "N/A"))

            print(
                "Similarity:",
                f"{movie['_similarity_score']:.4f}"
            )
