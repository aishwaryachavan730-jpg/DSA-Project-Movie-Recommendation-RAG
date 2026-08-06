import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

# Load processed dataset
df = pd.read_csv("dataset/processed_movies.csv")

print("Dataset Loaded Successfully")
print(df.shape)

# Use a sample for development
df = df.head(10000)

# Load embedding model
print("Loading Embedding Model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model Loaded Successfully")

# Prepare text
texts = df["combined_text"].tolist()

# Generate embeddings
print("Generating Embeddings...")

embeddings = model.encode(
    texts,
    show_progress_bar=True,
    batch_size=64,
    convert_to_numpy=True
)

print("Embeddings Generated Successfully")

print("Embedding Shape:")
print(embeddings.shape)

# Save embeddings
np.save("dataset/movie_embeddings.npy", embeddings)

print("Embeddings Saved Successfully")