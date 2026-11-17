import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"


def discover_movies(region="IN", page=1):

    if not TMDB_API_KEY:
        return {
            "success": False,
            "error": "TMDB_API_KEY not found in .env"
        }

    url = f"{BASE_URL}/discover/movie"

    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "region": region,
        "sort_by": "primary_release_date.desc",
        "include_adult": False,
        "include_video": False,
        "page": page
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        movies = []

        for movie in data.get("results", []):

            movies.append({
                "id": movie.get("id"),
                "title": movie.get("title"),
                "release_date": movie.get("release_date"),
                "overview": movie.get("overview"),
                "rating": movie.get("vote_average"),
                "vote_count": movie.get("vote_count"),
                "poster_path": movie.get("poster_path")
            })

        return {
            "success": True,
            "page": data.get("page", page),
            "total_pages": data.get("total_pages", 0),
            "total_results": data.get("total_results", 0),
            "movies": movies
        }

    except requests.exceptions.RequestException as error:

        return {
            "success": False,
            "error": str(error)
        }


if __name__ == "__main__":

    print("=" * 70)
    print("TMDB MOVIE DISCOVERY API TEST")
    print("=" * 70)

    result = discover_movies(
        region="IN",
        page=1
    )

    print(result)