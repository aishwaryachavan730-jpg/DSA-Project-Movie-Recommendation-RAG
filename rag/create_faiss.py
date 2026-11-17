import pandas as pd
import numpy as np
import faiss
import os

DATA_FILE = "DataSet/cleaned_movies.csv"
EMBEDDING_FILE = "DataSet/movie_embeddings.npy"
INDEX_FILE = "DataSet/movies.index"

print("=" * 60)
print("STEP 8.3 - CREATING FAISS VECTOR DATABASE")
print("=" * 60)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = pd.read_csv(DATA_FILE)

# ---------------------------------------------------------
# LOAD EMBEDDINGS
# ---------------------------------------------------------

embeddings = np.load(
    EMBEDDING_FILE
)

print("\nMovies:", len(df))
print("Embedding shape:", embeddings.shape)

# ---------------------------------------------------------
# CONVERT TO FLOAT32
# ---------------------------------------------------------

embeddings = embeddings.astype("float32")

# ---------------------------------------------------------
# NORMALIZE
# ---------------------------------------------------------

faiss.normalize_L2(embeddings)

# ---------------------------------------------------------
# CREATE FAISS INDEX
# ---------------------------------------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

# ---------------------------------------------------------
# ADD VECTORS
# ---------------------------------------------------------

index.add(embeddings)

print("\nFAISS index created.")
print("Number of vectors:", index.ntotal)
print("Vector dimension:", dimension)

# ---------------------------------------------------------
# SAVE INDEX
# ---------------------------------------------------------

faiss.write_index(
    index,
    INDEX_FILE
)

print("\nFAISS index saved to:")
print(INDEX_FILE)

print("=" * 60)
print("FAISS CREATION COMPLETED")
print("=" * 60)