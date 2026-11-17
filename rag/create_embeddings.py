import pandas as pd
import numpy as np
import os

from sentence_transformers import SentenceTransformer

INPUT_FILE = "DataSet/cleaned_movies.csv"
EMBEDDING_FILE = "DataSet/movie_embeddings.npy"

print("=" * 60)
print("STEP 8.2 - GENERATING MOVIE EMBEDDINGS")
print("=" * 60)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print(f"\nMovies loaded: {len(df)}")

# ---------------------------------------------------------
# LOAD EMBEDDING MODEL
# ---------------------------------------------------------

print("\nLoading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded successfully.")

# ---------------------------------------------------------
# GET MOVIE TEXT
# ---------------------------------------------------------

texts = df["movie_text"].fillna("").tolist()

print(f"\nGenerating embeddings for {len(texts)} movies...")

# ---------------------------------------------------------
# CREATE EMBEDDINGS
# ---------------------------------------------------------

embeddings = model.encode(
    texts,
    show_progress_bar=True,
    convert_to_numpy=True
)

print("\nEmbedding generation completed.")

print("Embedding shape:", embeddings.shape)

# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

np.save(
    EMBEDDING_FILE,
    embeddings
)

print("\nEmbeddings saved to:")
print(EMBEDDING_FILE)

print("=" * 60)
print("EMBEDDINGS COMPLETED")
print("=" * 60)