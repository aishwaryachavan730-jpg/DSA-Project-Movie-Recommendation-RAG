from tmdb_service import search_movie
from omdb_service import get_movie
from watchmode_service import search_title
from news_service import get_movie_news
from gemini_service import generate_recommendation


print("=" * 70)
print("STEP 10 - TESTING ALL 5 APIs")
print("=" * 70)


movie = "Inception"
year = 2010


# ---------------------------------------------------------
# 1. TMDB
# ---------------------------------------------------------

print("\n[1/5] TMDB API")
print("-" * 70)

tmdb_result = search_movie(movie)

print(tmdb_result)


# ---------------------------------------------------------
# 2. OMDb
# ---------------------------------------------------------

print("\n[2/5] OMDb API")
print("-" * 70)

omdb_result = get_movie(
    movie,
    year
)

print(omdb_result)


# ---------------------------------------------------------
# 3. Watchmode
# ---------------------------------------------------------

print("\n[3/5] WATCHMODE API")
print("-" * 70)

watchmode_result = search_title(movie)

print(watchmode_result)


# ---------------------------------------------------------
# 4. News API
# ---------------------------------------------------------

print("\n[4/5] NEWS API")
print("-" * 70)

news_result = get_movie_news(movie)

print(news_result)


# ---------------------------------------------------------
# 5. Gemini
# ---------------------------------------------------------

print("\n[5/5] GEMINI API")
print("-" * 70)

context = f"""
Movie: {movie}

TMDB:
{tmdb_result}

OMDb:
{omdb_result}

Watchmode:
{watchmode_result}

News:
{news_result}
"""

gemini_result = generate_recommendation(
    f"Tell me about {movie}",
    context
)

print(gemini_result)


print("\n" + "=" * 70)
print("ALL 5 API TESTS COMPLETED")
print("=" * 70)