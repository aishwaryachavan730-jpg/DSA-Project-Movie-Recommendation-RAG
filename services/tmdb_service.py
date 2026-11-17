# ============================================================
# TMDB SERVICE
# services/tmdb_service.py
# ============================================================

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")

BASE_URL = "https://api.themoviedb.org/3"


def _headers():
    """
    Prefer TMDB Bearer token if available.
    Otherwise use API key.
    """

    headers = {
        "accept": "application/json"
    }

    if TMDB_ACCESS_TOKEN:
        headers["Authorization"] = f"Bearer {TMDB_ACCESS_TOKEN}"

    return headers


def search_movie(movie_title):

    if not TMDB_API_KEY and not TMDB_ACCESS_TOKEN:
        return {
            "success": False,
            "error": "TMDB_API_KEY or TMDB_ACCESS_TOKEN is missing."
        }

    url = f"{BASE_URL}/search/movie"

    params = {
        "query": movie_title,
        "language": "en-US",
        "include_adult": "false"
    }

    # API key authentication only when Bearer token is unavailable
    if not TMDB_ACCESS_TOKEN:
        params["api_key"] = TMDB_API_KEY

    try:

        response = requests.get(
            url,
            headers=_headers(),
            params=params,
            timeout=(5, 20)
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        if not results:

            return {
                "success": False,
                "error": f"No TMDB movie found for '{movie_title}'.",
                "results": []
            }

        movie = results[0]

        return {
            "success": True,

            "tmdb_id": movie.get("id"),

            "title": movie.get(
                "title",
                movie_title
            ),

            "original_title": movie.get(
                "original_title",
                ""
            ),

            "overview": movie.get(
                "overview",
                ""
            ),

            "release_date": movie.get(
                "release_date",
                ""
            ),

            "poster_path": movie.get(
                "poster_path"
            ),

            "backdrop_path": movie.get(
                "backdrop_path"
            ),

            "rating": movie.get(
                "vote_average"
            ),

            "vote_average": movie.get(
                "vote_average"
            ),

            "vote_count": movie.get(
                "vote_count"
            ),

            "popularity": movie.get(
                "popularity"
            ),

            "original_language": movie.get(
                "original_language"
            ),

            "adult": movie.get(
                "adult",
                False
            ),

            "results": results
        }

    except requests.exceptions.ConnectTimeout:

        return {
            "success": False,
            "error": (
                "TMDB connection timed out. "
                "TMDB may be temporarily unreachable "
                "from your network."
            )
        }

    except requests.exceptions.ReadTimeout:

        return {
            "success": False,
            "error": (
                "TMDB server response timed out. "
                "Please try again."
            )
        }

    except requests.exceptions.ConnectionError as error:

        return {
            "success": False,
            "error": (
                "Could not connect to TMDB. "
                "Check your internet/VPN/firewall settings."
            )
        }

    except requests.exceptions.HTTPError as error:

        status_code = (
            error.response.status_code
            if error.response is not None
            else "unknown"
        )

        if status_code == 401:

            message = (
                "TMDB authentication failed. "
                "Check TMDB_API_KEY or TMDB_ACCESS_TOKEN."
            )

        elif status_code == 429:

            message = (
                "TMDB rate limit reached. "
                "Please wait and try again."
            )

        else:

            message = (
                f"TMDB HTTP error: {status_code}"
            )

        return {
            "success": False,
            "error": message
        }

    except Exception as error:

        return {
            "success": False,
            "error": f"TMDB unexpected error: {error}"
        }


def discover_movies(
    region="IN",
    page=1
):

    if not TMDB_API_KEY and not TMDB_ACCESS_TOKEN:

        return {
            "success": False,
            "error": "TMDB credentials are missing."
        }

    url = f"{BASE_URL}/discover/movie"

    params = {
        "language": "en-US",
        "region": region,
        "page": page,
        "sort_by": "popularity.desc",
        "include_adult": "false",
        "include_video": "false"
    }

    if not TMDB_ACCESS_TOKEN:
        params["api_key"] = TMDB_API_KEY

    try:

        response = requests.get(
            url,
            headers=_headers(),
            params=params,
            timeout=(5, 20)
        )

        response.raise_for_status()

        data = response.json()

        return {
            "success": True,
            "movies": data.get("results", []),
            "page": data.get("page", page),
            "total_pages": data.get(
                "total_pages",
                0
            ),
            "total_results": data.get(
                "total_results",
                0
            )
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "error": "TMDB Discovery request timed out."
        }

    except requests.exceptions.ConnectionError:

        return {
            "success": False,
            "error": (
                "Could not connect to TMDB Discovery."
            )
        }

    except requests.exceptions.HTTPError as error:

        status = (
            error.response.status_code
            if error.response
            else "unknown"
        )

        return {
            "success": False,
            "error": f"TMDB Discovery HTTP error: {status}"
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }