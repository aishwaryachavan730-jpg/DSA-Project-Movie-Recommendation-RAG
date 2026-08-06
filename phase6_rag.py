import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Load metadata
print("Loading Metadata...")
movies = pd.read_csv("faiss_index/movie_metadata.csv")

# Load FAISS
print("Loading FAISS...")
index = faiss.read_index("faiss_index/movie_index.faiss")

print("Total Movies:", index.ntotal)

# Load embedding model
print("Loading Embedding Model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model Loaded Successfully")

# User Query
query = input("\nEnter Movie Preference:\n\n")

# Query Embedding
query_embedding = model.encode([query])

query_embedding = np.array(query_embedding).astype("float32")

# Search
distance, indices = index.search(query_embedding, 5)

print("\nRecommended Movies")
print("=" * 60)

for i in indices[0]:

    movie = movies.iloc[i]

    print("\nTitle :", movie["title"])
    print("Genre :", movie["genres"])
    print("Rating :", movie["vote_average"])
    print("Language :", movie["original_language"])

    print("\nOverview:")

    print(movie["overview"])

    print("-" * 60)