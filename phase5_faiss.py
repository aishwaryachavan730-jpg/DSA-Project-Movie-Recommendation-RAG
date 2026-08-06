import pandas as pd
import numpy as np
import faiss
import os

print("Loading Dataset...")
df = pd.read_csv("dataset/processed_movies.csv")

print("Loading Embeddings...")
embeddings = np.load("dataset/movie_embeddings.npy")

embeddings = embeddings.astype("float32")

dimension = embeddings.shape[1]

print("Embedding Dimension:", dimension)

index = faiss.IndexFlatL2(dimension)

print("Adding Embeddings...")

index.add(embeddings)

print("Total Vectors:", index.ntotal)

os.makedirs("faiss_index", exist_ok=True)

faiss.write_index(
    index,
    "faiss_index/movie_index.faiss"
)

df.to_csv(
    "faiss_index/movie_metadata.csv",
    index=False
)

print("\nFAISS Saved Successfully")

query = embeddings[0].reshape(1, -1)

distance, indices = index.search(query, 5)

print("\nNearest Movies")

for i in indices[0]:
    print(df.iloc[i]["title"])