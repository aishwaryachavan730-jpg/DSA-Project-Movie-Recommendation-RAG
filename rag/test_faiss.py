import pandas as pd
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

DATA_FILE = "DataSet/cleaned_movies.csv"
EMBEDDING_FILE = "DataSet/movie_embeddings.npy"
INDEX_FILE = "DataSet/movies.index"

print("=" * 60)
print("FAISS SEARCH TEST")
print("=" * 60)

# Load dataset
df = pd.read_csv(DATA_FILE)

# Load model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# Load FAISS
index = faiss.read_index(
    INDEX_FILE
)

# User query
query = "science fiction movie about space"

print("\nQuery:")
print(query)

# Create query embedding
query_embedding = model.encode(
    [query],
    convert_to_numpy=True
).astype("float32")

# Normalize
faiss.normalize_L2(query_embedding)

# Search
distances, indices = index.search(
    query_embedding,
    5
)

print("\nTop 5 recommendations:")
print("-" * 60)

for rank, idx in enumerate(indices[0], start=1):

    movie = df.iloc[idx]

    print(
        f"{rank}. {movie['title']} "
        f"({movie['year']}) "
        f"- similarity: {distances[0][rank-1]:.4f}"
    )

print("\nFAISS SEARCH COMPLETED")