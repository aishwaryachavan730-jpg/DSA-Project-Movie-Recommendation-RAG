from tmdb_api import search_movie
from omdb_api import get_movie_details
from watchmode_api import search_movie as watchmode_search
from news_api import search_movie_news


TITLE = "Inception"
YEAR = 2010


print("=" * 60)
print("STEP 10 - API TEST")
print("=" * 60)


# --------------------------------------------------
# TMDB
# --------------------------------------------------

print("\n1. TMDB API")
print("-" * 40)

try:

    tmdb = search_movie(TITLE)

    print("Title:", tmdb.get("title"))
    print("TMDB Rating:", tmdb.get("tmdb_rating"))
    print("Release Date:", tmdb.get("release_date"))
    print("Poster:", tmdb.get("poster_path"))

except Exception as e:

    print("TMDB ERROR:", e)


# --------------------------------------------------
# OMDb
# --------------------------------------------------

print("\n2. OMDb API")
print("-" * 40)

try:

    omdb = get_movie_details(TITLE, YEAR)

    print("IMDb ID:", omdb.get("imdb_id"))
    print("IMDb Rating:", omdb.get("imdb_rating"))
    print("Director:", omdb.get("director"))
    print("Actors:", omdb.get("actors"))
    print("Awards:", omdb.get("awards"))

except Exception as e:

    print("OMDb ERROR:", e)


# --------------------------------------------------
# Watchmode
# --------------------------------------------------

print("\n3. WATCHMODE API")
print("-" * 40)

try:

    watchmode = watchmode_search(TITLE)

    print("Watchmode result:")
    print(watchmode)

except Exception as e:

    print("WATCHMODE ERROR:", e)


# --------------------------------------------------
# News
# --------------------------------------------------

print("\n4. NEWS API")
print("-" * 40)

try:

    news = search_movie_news(TITLE)

    print("Number of articles:", len(news))

    for article in news[:3]:

        print(
            "-",
            article.get("title")
        )

except Exception as e:

    print("NEWS ERROR:", e)


print("\n" + "=" * 60)
print("API TEST COMPLETED")
print("=" * 60)