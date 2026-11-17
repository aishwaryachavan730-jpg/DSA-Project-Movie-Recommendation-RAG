from api.tmdb_api import search_movie as tmdb_search
from api.omdb_api import get_movie_details as omdb_details
from api.watchmode_api import search_movie as watchmode_search
from api.watchmode_api import get_sources as watchmode_sources
from api.news_api import search_movie_news


def get_movie_information(title, year=None):

    result = {
        "title": title,
        "tmdb": {},
        "omdb": {},
        "watchmode": {},
        "news": []
    }

    # --------------------------------------------------
    # TMDB
    # --------------------------------------------------

    try:

        tmdb_data = tmdb_search(title)

        result["tmdb"] = tmdb_data

    except Exception as e:

        result["tmdb"] = {
            "error": str(e)
        }

    # --------------------------------------------------
    # OMDb
    # --------------------------------------------------

    try:

        omdb_data = omdb_details(title, year)

        result["omdb"] = omdb_data

    except Exception as e:

        result["omdb"] = {
            "error": str(e)
        }

    # --------------------------------------------------
    # WATCHMODE
    # --------------------------------------------------

    try:

        watchmode_data = watchmode_search(title)

        if watchmode_data:

            watchmode_id = watchmode_data.get("id")

            if watchmode_id:

                sources = watchmode_sources(watchmode_id)

                watchmode_data["sources"] = sources

        result["watchmode"] = watchmode_data

    except Exception as e:

        result["watchmode"] = {
            "error": str(e)
        }

    # --------------------------------------------------
    # NEWS
    # --------------------------------------------------

    try:

        news_data = search_movie_news(title)

        result["news"] = news_data

    except Exception as e:

        result["news"] = {
            "error": str(e)
        }

    return result