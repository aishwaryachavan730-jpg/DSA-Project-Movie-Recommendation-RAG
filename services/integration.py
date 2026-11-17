# ============================================================
# MOVIEVERSE AI
# COMPLETE MULTI-API + RAG + GEMINI INTEGRATION
# ============================================================

import os
import sys
import json
import traceback


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# IMPORT SERVICES
# ============================================================

from services.tmdb_service import search_movie as search_tmdb
from services.movie_discovery_service import discover_movies
from services.omdb_service import search_movie as search_omdb
from services.watchmode_service import search_title as search_watchmode
from services.news_service import get_movie_news
from services.movie_context import build_movie_context
from services.gemini_service import generate_recommendation


# ============================================================
# HELPER - SAFE API CALL
# ============================================================

def safe_call(function, *args, **kwargs):
    """
    Safely execute an API/service function.

    If the service fails, return an empty dictionary
    instead of stopping the complete integration.
    """

    try:

        result = function(
            *args,
            **kwargs
        )

        if result is None:
            return {}

        return result

    except Exception as error:

        print()
        print("-" * 70)
        print(
            f"ERROR IN: {function.__name__}"
        )
        print(
            f"ERROR: {error}"
        )
        print("-" * 70)

        traceback.print_exc()

        return {}


# ============================================================
# HELPER - NORMALIZE RESULT
# ============================================================

def normalize_result(result):
    """
    Make sure API results are always dictionaries.
    """

    if result is None:
        return {}

    if isinstance(result, dict):
        return result

    return {
        "data": result
    }


# ============================================================
# MAIN MOVIE INTEGRATION
# ============================================================

def run_movie_integration(movie_title):
    """
    Complete MovieVerse AI pipeline.

    Pipeline:

    Movie Title
        |
        +---- TMDB Movie Search
        |
        +---- TMDB Movie Discovery
        |
        +---- OMDb API
        |
        +---- WatchMode API
        |
        +---- News API
        |
        +---- Combined Movie Context
        |
        +---- Gemini LLM
        |
        +---- Final Recommendation
    """

    # ========================================================
    # VALIDATE MOVIE TITLE
    # ========================================================

    movie_title = str(
        movie_title
    ).strip()

    if not movie_title:

        raise ValueError(
            "Movie title cannot be empty."
        )


    # ========================================================
    # START
    # ========================================================

    print()
    print("=" * 70)
    print(
        "MOVIE RECOMMENDATION RAG - COMPLETE API INTEGRATION"
    )
    print("=" * 70)

    print()
    print(
        f"Selected Movie: {movie_title}"
    )


    # ========================================================
    # STEP 11.1 - TMDB MOVIE SEARCH
    # ========================================================

    print()
    print("=" * 70)
    print("STEP 11.1 - TMDB API")
    print("=" * 70)

    print()
    print(
        f"Searching TMDB for: {movie_title}"
    )

    tmdb_data = safe_call(
        search_tmdb,
        movie_title
    )

    tmdb_data = normalize_result(
        tmdb_data
    )

    print()
    print("TMDB Result:")
    print(tmdb_data)


    # ========================================================
    # STEP 11.2 - OMDb API
    # ========================================================

    print()
    print("=" * 70)
    print("STEP 11.2 - OMDb API")
    print("=" * 70)

    print()
    print(
        f"Searching OMDb for: {movie_title}"
    )

    omdb_data = safe_call(
        search_omdb,
        movie_title
    )

    omdb_data = normalize_result(
        omdb_data
    )

    print()
    print("OMDb Result:")
    print(omdb_data)


    # ========================================================
    # STEP 11.3 - WATCHMODE API
    # ========================================================

    print()
    print("=" * 70)
    print("STEP 11.3 - WATCHMODE API")
    print("=" * 70)

    print()
    print(
        f"Searching WatchMode for: {movie_title}"
    )

    watchmode_data = safe_call(
        search_watchmode,
        movie_title
    )

    watchmode_data = normalize_result(
        watchmode_data
    )

    print()
    print("WatchMode Result:")
    print(watchmode_data)


    # ========================================================
    # STEP 11.4 - MOVIE DISCOVERY API
    # ========================================================

    print()
    print("=" * 70)
    print("STEP 11.4 - MOVIE DISCOVERY API")
    print("=" * 70)

    print()
    print(
        "Discovering latest movies for India..."
    )

    discovery_data = safe_call(
        discover_movies,
        region="IN",
        page=1
    )

    discovery_data = normalize_result(
        discovery_data
    )

    print()
    print("Movie Discovery Result:")
    print(discovery_data)


    # ========================================================
    # DISPLAY DISCOVERY RESULTS
    # ========================================================

    if discovery_data.get("success"):

        print()
        print(
            "MOVIE DISCOVERY API SUCCESS"
        )

        # Support different possible result keys
        movies = discovery_data.get(
            "movies",
            discovery_data.get(
                "results",
                []
            )
        )

        if not isinstance(movies, list):
            movies = []

        print()
        print(
            f"Movies Found: {len(movies)}"
        )

        for index, movie in enumerate(
            movies,
            start=1
        ):

            if not isinstance(movie, dict):
                continue

            print()
            print("-" * 60)
            print(
                f"Movie {index}"
            )
            print("-" * 60)

            print(
                "Title:",
                movie.get(
                    "title",
                    movie.get(
                        "name",
                        "Not available"
                    )
                )
            )

            print(
                "Release Date:",
                movie.get(
                    "release_date",
                    "Not available"
                )
            )

            print(
                "Rating:",
                movie.get(
                    "rating",
                    movie.get(
                        "vote_average",
                        "Not available"
                    )
                )
            )

    else:

        print()
        print(
            "MOVIE DISCOVERY API DID NOT RETURN SUCCESS"
        )


    # ========================================================
    # STEP 11.5 - NEWS API
    # ========================================================

    print()
    print("=" * 70)
    print("STEP 11.5 - NEWS API + RAG")
    print("=" * 70)

    print()
    print(
        "Searching movie news..."
    )

    news_data = safe_call(
        get_movie_news,
        movie_title
    )

    news_data = normalize_result(
        news_data
    )

    print()
    print("News API Result:")
    print(news_data)


    # ========================================================
    # DISPLAY NEWS RESULTS
    # ========================================================

    if news_data.get("success"):

        articles = news_data.get(
            "articles",
            []
        )

        if not isinstance(articles, list):
            articles = []

        print()
        print(
            "NEWS API SUCCESS"
        )

        print(
            f"Movie: "
            f"{news_data.get('movie', movie_title)}"
        )

        print(
            f"Articles Found: "
            f"{len(articles)}"
        )

        for index, article in enumerate(
            articles,
            start=1
        ):

            if not isinstance(article, dict):
                continue

            print()
            print("-" * 60)
            print(
                f"Article {index}"
            )
            print("-" * 60)

            print(
                "Title:",
                article.get(
                    "title",
                    "Not available"
                )
            )

            print(
                "Description:",
                article.get(
                    "description",
                    "Not available"
                )
            )

            print(
                "Source:",
                article.get(
                    "source",
                    "Unknown"
                )
            )

            print(
                "Published:",
                article.get(
                    "published_at",
                    "Unknown"
                )
            )

            print(
                "URL:",
                article.get(
                    "url",
                    "Not available"
                )
            )

    else:

        print()
        print(
            "NEWS API DID NOT RETURN SUCCESS"
        )


    # ========================================================
    # STEP 11.6 - BUILD COMBINED MOVIE CONTEXT
    # ========================================================

    print()
    print("=" * 70)
    print(
        "STEP 11.6 - BUILD COMBINED MOVIE CONTEXT"
    )
    print("=" * 70)

    print()
    print(
        "Building combined movie context..."
    )


    movie_context = build_movie_context(
        movie_title=movie_title,
        tmdb_data=tmdb_data,
        omdb_data=omdb_data,
        watchmode_data=watchmode_data,
        news_data=news_data
    )


    # ========================================================
    # DISPLAY COMBINED CONTEXT
    # ========================================================

    print()
    print(
        "Combined Movie Context:"
    )

    print("=" * 70)

    print(movie_context)

    print("=" * 70)


    # ========================================================
    # STEP 11.7 - GEMINI LLM + RAG
    # ========================================================

    print()
    print("=" * 70)
    print(
        "STEP 11.7 - GEMINI LLM + RAG"
    )
    print("=" * 70)

    recommendation = None

    try:

        print()
        print(
            "Sending combined context to Gemini..."
        )


        # IMPORTANT:
        #
        # Your current gemini_service.py contains:
        #
        # def generate_recommendation(movie_context):
        #
        # Therefore we pass ONLY movie_context.

        recommendation = generate_recommendation(
            movie_context
        )


        print()
        print("=" * 70)
        print(
            "GEMINI RESPONSE"
        )
        print("=" * 70)

        print()

        print(
            recommendation
        )


    except Exception as error:

        print()
        print("=" * 70)
        print(
            "GEMINI RECOMMENDATION GENERATION FAILED"
        )
        print("=" * 70)

        print()
        print(
            f"Error: {error}"
        )

        traceback.print_exc()

        recommendation = {
            "success": False,
            "error": str(error)
        }


    # ========================================================
    # STEP 11.8 - FINAL RECOMMENDATION
    # ========================================================

    print()
    print("=" * 70)
    print(
        "FINAL MOVIE RECOMMENDATION"
    )
    print("=" * 70)

    print()

    if recommendation:

        print(
            recommendation
        )

    else:

        print(
            "No Gemini recommendation was generated."
        )


    # ========================================================
    # COMPLETE RESULT
    # ========================================================

    result = {

        "movie_title": movie_title,

        "tmdb": tmdb_data,

        "omdb": omdb_data,

        "watchmode": watchmode_data,

        "movie_discovery": discovery_data,

        "news": news_data,

        "movie_context": movie_context,

        "recommendation": recommendation
    }


    # ========================================================
    # RETURN RESULT
    # ========================================================

    return result


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print(
        "MOVIEVERSE AI"
    )
    print(
        "Gemini + RAG + Multi-API Integration"
    )
    print("=" * 70)


    # ========================================================
    # TEST MOVIE
    # ========================================================

    selected_movie = "Interstellar"

    print()
    print(
        f"Movie selected for testing: "
        f"{selected_movie}"
    )


    # ========================================================
    # RUN COMPLETE PIPELINE
    # ========================================================

    try:

        result = run_movie_integration(
            selected_movie
        )


        # ====================================================
        # SAVE RESULT TO JSON
        # ====================================================

        output_file = os.path.join(
            PROJECT_ROOT,
            "movie_integration_result.json"
        )


        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                result,
                file,
                indent=4,
                ensure_ascii=False,
                default=str
            )


        # ====================================================
        # SUCCESS MESSAGE
        # ====================================================

        print()
        print("=" * 70)
        print(
            "INTEGRATION COMPLETED"
        )
        print("=" * 70)

        print()

        print(
            "Result saved to:"
        )

        print(
            output_file
        )


    except Exception as error:

        print()
        print("=" * 70)
        print(
            "INTEGRATION FAILED"
        )
        print("=" * 70)

        print()

        print(
            f"Error: {error}"
        )

        traceback.print_exc()