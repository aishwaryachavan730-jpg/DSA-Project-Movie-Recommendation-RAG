import os
import requests
from dotenv import load_dotenv

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

BASE_URL = "https://www.omdbapi.com/"


def search_movie(title):

    if not OMDB_API_KEY:
        return {
            "success": False,
            "error": "OMDB_API_KEY not found"
        }

    params = {
        "apikey": OMDB_API_KEY,
        "t": title,
        "type": "movie"
    }

    try:

        response = requests.get(
            BASE_URL,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if data.get("Response") != "True":

            return {
                "success": False,
                "title": title,
                "error": data.get(
                    "Error",
                    "Movie not found"
                )
            }

        return {
            "success": True,
            "title": data.get("Title"),
            "year": data.get("Year"),
            "imdb_rating": data.get("imdbRating"),
            "director": data.get("Director"),
            "actors": data.get("Actors"),
            "awards": data.get("Awards"),
            "plot": data.get("Plot"),
            "genre": data.get("Genre"),
            "runtime": data.get("Runtime"),
            "imdb_id": data.get("imdbID")
        }

    except Exception as e:

        return {
            "success": False,
            "title": title,
            "error": str(e)
        }


if __name__ == "__main__":

    result = search_movie("Interstellar")

    print(result)