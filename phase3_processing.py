# ==========================================
# Phase 3: Data Processing
# Movie Recommendation System using RAG
# ==========================================

import pandas as pd

# Load cleaned dataset
df = pd.read_csv("dataset/clean_movies.csv")

print("Dataset Loaded Successfully")
print("Original Shape:", df.shape)

# ------------------------------------------------
# Select only useful columns
# ------------------------------------------------
selected_columns = [
    "title",
    "overview",
    "genres",
    "vote_average",
    "release_date",
    "original_language",
    "popularity",
    "keywords"
]

df = df[selected_columns]

print("\nSelected Columns:")
print(df.columns)

print("\nShape After Selecting Columns:")
print(df.shape)

# ------------------------------------------------
# Check Missing Values
# ------------------------------------------------

print("\nMissing Values:")
print(df.isnull().sum())

# Fill missing values
df["overview"] = df["overview"].fillna("No overview available")
df["genres"] = df["genres"].fillna("Unknown")
df["keywords"] = df["keywords"].fillna("No keywords")
df["original_language"] = df["original_language"].fillna("Unknown")

# Remove rows where title is missing
df = df.dropna(subset=["title"])

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

print("\nShape After Cleaning:")
print(df.shape)

# ------------------------------------------------
# Create Combined Text
# ------------------------------------------------

df["combined_text"] = (
    "Title: " + df["title"].astype(str) +
    "\nGenre: " + df["genres"].astype(str) +
    "\nOverview: " + df["overview"].astype(str) +
    "\nLanguage: " + df["original_language"].astype(str) +
    "\nRating: " + df["vote_average"].astype(str) +
    "\nPopularity: " + df["popularity"].astype(str) +
    "\nKeywords: " + df["keywords"].astype(str)
)

print("\nCombined Text Example:\n")
print(df["combined_text"].iloc[0])

# ------------------------------------------------
# Save Processed Dataset
# ------------------------------------------------

df.to_csv("dataset/processed_movies.csv", index=False)

print("\nProcessed dataset saved successfully!")
print("Location: dataset/processed_movies.csv")
print("\nPhase 3 Completed Successfully!")