# ============================================================
# WIKIPEDIA SERVICE
# MovieVerse AI
# ============================================================

import requests
from urllib.parse import quote


# ============================================================
# WIKIPEDIA API
# ============================================================

WIKIPEDIA_API_URL = (
    "https://en.wikipedia.org/api/rest_v1/page/summary/"
)


# ============================================================
# SEARCH WIKIPEDIA
# ============================================================

def search_wikipedia(movie_title):
    """
    Search Wikipedia for a movie title.

    Parameters
    ----------
    movie_title : str
        Movie title to search.

    Returns
    -------
    dict
        Normalized Wikipedia movie information.
    """

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    if not movie_title:

        return {
            "success": False,
            "error": "Movie title is empty."
        }

    movie_title = str(movie_title).strip()

    if not movie_title:

        return {
            "success": False,
            "error": "Movie title is empty."
        }

    # --------------------------------------------------------
    # Create Wikipedia page URL
    # --------------------------------------------------------

    page_title = movie_title.replace(" ", "_")

    url = WIKIPEDIA_API_URL + quote(
        page_title,
        safe=""
    )

    # --------------------------------------------------------
    # Request
    # --------------------------------------------------------

    try:

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "MovieVerseAI/1.0"
            }
        )

        # ----------------------------------------------------
        # Successful response
        # ----------------------------------------------------

        if response.status_code == 200:

            data = response.json()

            content_urls = data.get(
                "content_urls",
                {}
            )

            desktop = content_urls.get(
                "desktop",
                {}
            )

            return {

                "success": True,

                "title": data.get(
                    "title",
                    movie_title
                ),

                "description": data.get(
                    "description",
                    ""
                ),

                "summary": data.get(
                    "extract",
                    ""
                ),

                "url": desktop.get(
                    "page",
                    ""
                ),

                "thumbnail": data.get(
                    "thumbnail",
                    {}
                ).get(
                    "source",
                    ""
                )
            }

        # ----------------------------------------------------
        # Page not found
        # ----------------------------------------------------

        if response.status_code == 404:

            return {

                "success": False,

                "title": movie_title,

                "error": (
                    "Wikipedia page not found."
                )
            }

        # ----------------------------------------------------
        # Other HTTP errors
        # ----------------------------------------------------

        return {

            "success": False,

            "title": movie_title,

            "error": (
                f"Wikipedia API HTTP "
                f"{response.status_code}"
            )
        }

    # --------------------------------------------------------
    # Exception
    # --------------------------------------------------------

    except requests.exceptions.Timeout:

        return {

            "success": False,

            "title": movie_title,

            "error": (
                "Wikipedia API request timed out."
            )
        }

    except requests.exceptions.RequestException as error:

        return {

            "success": False,

            "title": movie_title,

            "error": str(error)
        }

    except Exception as error:

        return {

            "success": False,

            "title": movie_title,

            "error": str(error)
        }


# ============================================================
# ALIASES
# ============================================================

def get_movie_wikipedia(movie_title):

    return search_wikipedia(movie_title)


def search_movie(movie_title):

    return search_wikipedia(movie_title)