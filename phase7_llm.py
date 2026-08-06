import pandas as pd
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer
from transformers import pipeline

print("Loading Metadata...")
movies = pd.read_csv("faiss_index/movie_metadata.csv")

print("Loading FAISS...")
index = faiss.read_index("faiss_index/movie_index.faiss")

print("Loading Embedding Model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading LLM...")

generator = pipeline(
    task="text2text-generation",
    model="google/flan-t5-small"
)
query = input("\nEnter Movie Preference: ")

query_embedding = embedding_model.encode([query])
query_embedding = np.array(query_embedding).astype("float32")

distance, indices = index.search(query_embedding,5)

context=""

for i in indices[0]:

    movie=movies.iloc[i]

    context += f"""
Title: {movie['title']}
Genre: {movie['genres']}
Overview: {movie['overview']}
Rating: {movie['vote_average']}

"""

prompt=f"""
You are a movie recommendation assistant.

Context:

{context}

User Question:

{query}

Recommend the best movies with a short explanation.
"""

response = generator(
    prompt,
    max_new_tokens=250,
    temperature=0.7,
    do_sample=True
)

print("\n========== AI Recommendation ==========\n")
print(response[0]["generated_text"])