# ============================================================
# MOVIEVERSE AI
# GEMINI SERVICE
# STEP 16 - GEMINI + RAG RECOMMENDATION
# ============================================================

import os

from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ============================================================
# GEMINI MODEL
# ============================================================

MODEL_NAME = "gemini-3.5-flash"


# ============================================================
# CREATE GEMINI CLIENT
# ============================================================

client = None

if GEMINI_API_KEY:

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


# ============================================================
# GENERATE MOVIE RECOMMENDATION
# ============================================================

def generate_recommendation(
    user_query,
    movie_context
):
    """
    Generate a movie recommendation using Gemini.

    Parameters
    ----------
    user_query : str
        Movie title or movie-related query.

    movie_context : str
        Combined information retrieved from:
        - TMDB
        - OMDb
        - WatchMode
        - News API
        - Movie discovery
        - RAG context

    Returns
    -------
    dict
        Recommendation result.
    """

    # ========================================================
    # CHECK API KEY
    # ========================================================

    if not GEMINI_API_KEY:

        return {
            "success": False,
            "model": MODEL_NAME,
            "error": (
                "GEMINI_API_KEY not found. "
                "Please add GEMINI_API_KEY to your .env file."
            )
        }


    # ========================================================
    # VALIDATE USER QUERY
    # ========================================================

    if user_query is None:

        return {
            "success": False,
            "model": MODEL_NAME,
            "error": "Movie query is empty."
        }


    user_query = str(
        user_query
    ).strip()


    if not user_query:

        return {
            "success": False,
            "model": MODEL_NAME,
            "error": "Movie query is empty."
        }


    # ========================================================
    # VALIDATE MOVIE CONTEXT
    # ========================================================

    if movie_context is None:

        return {
            "success": False,
            "model": MODEL_NAME,
            "error": "Movie context is empty."
        }


    movie_context = str(
        movie_context
    ).strip()


    if not movie_context:

        return {
            "success": False,
            "model": MODEL_NAME,
            "error": "Movie context is empty."
        }


    # ========================================================
    # BUILD GEMINI PROMPT
    # ========================================================

    prompt = f"""
You are MovieVerse AI, an intelligent movie recommendation
assistant.

The user searched for:

{user_query}

You have received movie information from multiple APIs
and a RAG-based context-building pipeline.

Use ONLY the retrieved context provided below.

IMPORTANT RULES:

1. Do not invent movie information.
2. Do not invent ratings.
3. Do not invent actors.
4. Do not invent directors.
5. Do not invent awards.
6. Do not invent streaming platforms.
7. Do not invent news.
8. Do not treat unrelated news as movie news.
9. If information is unavailable, write:
   "Information not available."
10. Clearly separate movie information from recent news.
11. Base the final recommendation on the retrieved context.
12. Keep the response clear and suitable for a movie
    recommendation application.

============================================================
USER QUERY
============================================================

{user_query}

============================================================
RETRIEVED MOVIE CONTEXT
============================================================

{movie_context}

============================================================
END RETRIEVED MOVIE CONTEXT
============================================================

Generate the response using the following structure:

# 🎬 Movie Recommendation

## 1. Recommended Movie

Give the movie title and year.

## 2. Why This Movie Matches

Explain why the movie is worth watching using only
the retrieved information.

## 3. Genre

Give the available genres.

## 4. Ratings

Show available TMDB and IMDb ratings.

## 5. Director and Main Actors

Show the available director and actors.

## 6. Awards

Show available awards.

## 7. Where to Watch

Show available streaming information.

If streaming information is unavailable, write:

"Information not available."

## 8. Recent Movie News

Show only relevant retrieved movie news.

If no relevant movie news is available, write:

"Information not available."

## 9. Final Recommendation

Give a short recommendation based only on the
retrieved movie information.

Do not add unsupported information.
"""


    # ========================================================
    # CALL GEMINI
    # ========================================================

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )


        # ====================================================
        # EXTRACT RESPONSE TEXT
        # ====================================================

        response_text = getattr(
            response,
            "text",
            None
        )


        if not response_text:

            return {
                "success": False,
                "model": MODEL_NAME,
                "error": "Gemini returned an empty response."
            }


        # ====================================================
        # SUCCESS
        # ====================================================

        return {
            "success": True,
            "model": MODEL_NAME,
            "response": response_text.strip()
        }


    # ========================================================
    # GEMINI ERROR
    # ========================================================

    except Exception as error:

        return {
            "success": False,
            "model": MODEL_NAME,
            "error": str(error)
        }


# ============================================================
# DIRECT GEMINI TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("MOVIEVERSE AI - GEMINI API TEST")
    print("=" * 70)


    # ========================================================
    # TEST MOVIE
    # ========================================================

    test_movie = "Interstellar"


    # ========================================================
    # TEST CONTEXT
    # ========================================================

    test_context = """
MOVIE TITLE:
Interstellar

YEAR:
2014

GENRE:
Adventure, Drama, Sci-Fi

TMDB RATING:
8.484

IMDb RATING:
8.7

DIRECTOR:
Christopher Nolan

ACTORS:
Matthew McConaughey,
Anne Hathaway,
Jessica Chastain

AWARDS:
Won 1 Oscar.
45 wins & 148 nominations total

PLOT:
When Earth becomes uninhabitable in the future,
a farmer and ex-NASA pilot, Joseph Cooper,
is tasked to pilot a spacecraft with a team
of researchers to find a new planet for humans.

RUNTIME:
169 min

STREAMING:
Information not available.

RECENT MOVIE NEWS:
Information not available.
"""


    # ========================================================
    # DISPLAY TEST INFORMATION
    # ========================================================

    print()
    print(
        f"Testing movie: {test_movie}"
    )

    print()
    print(
        f"Gemini model: {MODEL_NAME}"
    )


    # ========================================================
    # CALL GEMINI
    # ========================================================

    result = generate_recommendation(
        user_query=test_movie,
        movie_context=test_context
    )


    # ========================================================
    # DISPLAY RESULT
    # ========================================================

    print()
    print("=" * 70)
    print("GEMINI TEST RESULT")
    print("=" * 70)


    if result.get("success"):

        print()
        print("GEMINI API SUCCESS")

        print()
        print(
            result.get(
                "response",
                "No response."
            )
        )

    else:

        print()
        print("GEMINI API FAILED")

        print()
        print(
            "Error:",
            result.get(
                "error",
                "Unknown error."
            )
        )


    print()
    print("=" * 70)