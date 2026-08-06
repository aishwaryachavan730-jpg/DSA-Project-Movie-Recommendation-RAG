import pandas as pd

# Load movie dataset
movies = pd.read_csv("faiss_index/movie_metadata.csv")


def chatbot(query):

    query = query.lower()

    # Horror Movies
    if "horror" in query:

        result = movies[
            movies["genres"].str.contains(
                "Horror",
                case=False,
                na=False
            )
        ]

        return result.head(10)

    # Comedy Movies
    elif "comedy" in query:

        result = movies[
            movies["genres"].str.contains(
                "Comedy",
                case=False,
                na=False
            )
        ]

        return result.head(10)

    # Action Movies
    elif "action" in query:

        result = movies[
            movies["genres"].str.contains(
                "Action",
                case=False,
                na=False
            )
        ]

        return result.head(10)

    # Romance Movies
    elif "romance" in query:

        result = movies[
            movies["genres"].str.contains(
                "Romance",
                case=False,
                na=False
            )
        ]

        return result.head(10)

    # Sci-Fi Movies
    elif "science fiction" in query or "sci-fi" in query:

        result = movies[
            movies["genres"].str.contains(
                "Science Fiction",
                case=False,
                na=False
            )
        ]

        return result.head(10)

    # Harry Potter Like Movies
    elif "harry potter" in query:

        result = movies[
            movies["genres"].str.contains(
                "Fantasy",
                case=False,
                na=False
            )
        ]

        return result.head(10)

    # Tom Cruise Movies
    elif "tom cruise" in query:

        result = movies[
            movies["overview"].str.contains(
                "Tom Cruise",
                case=False,
                na=False
            )
        ]

        return result.head(10)

    # Default
    else:

        return movies.sample(10)