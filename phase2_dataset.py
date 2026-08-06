import pandas as pd

# Load the dataset
df = pd.read_csv("dataset/TMDB_movie_dataset_v11.csv")

# Display first 5 rows
print("First 5 Rows:")
print(df.head())

# Display dataset shape
print("\nDataset Shape:")
print(df.shape)

# Display column names
print("\nColumns:")
print(df.columns)

# Display dataset information
print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

df = df.drop_duplicates()

print("\nDataset Shape After Removing Duplicates:")
print(df.shape)

df.to_csv("dataset/clean_movies.csv", index=False)

print("\nClean dataset saved successfully!")

