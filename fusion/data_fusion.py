import pandas as pd
import json
import os


def create_fused_movie_record(
    tmdb_data=None,
    omdb_data=None,
    watchmode_data=None,
    news_data=None
):
    tmdb_data = tmdb_data or {}
    omdb_data = omdb_data or {}
    watchmode_data = watchmode_data or {}
    news_data = news_data or {}

    record = {
        "title": (
            tmdb_data.get("title")
            or omdb_data.get("Title")
            or watchmode_data.get("name")
        ),

        "year": (
            tmdb_data.get("release_date", "")[:4]
            if tmdb_data.get("release_date")
            else omdb_data.get("Year")
        ),

        "tmdb_rating": tmdb_data.get("vote_average"),

        "imdb_rating": omdb_data.get("imdbRating"),

        "genre": (
            tmdb_data.get("genres")
            or omdb_data.get("Genre")
        ),

        "overview": (
            tmdb_data.get("overview")
            or omdb_data.get("Plot")
        ),

        "director": omdb_data.get("Director"),

        "actors": omdb_data.get("Actors"),

        "awards": omdb_data.get("Awards"),

        "watchmode_data": watchmode_data,

        "news_data": news_data
    }

    return record


def normalize_movie_record(record):

    return {
        "title": record.get("title"),
        "year": record.get("year"),
        "tmdb_rating": record.get("tmdb_rating"),
        "imdb_rating": record.get("imdb_rating"),
        "genre": record.get("genre"),
        "overview": record.get("overview"),
        "director": record.get("director"),
        "actors": record.get("actors"),
        "awards": record.get("awards"),

        "watchmode_data": json.dumps(
            record.get("watchmode_data", {}),
            ensure_ascii=False
        ),

        "news_data": json.dumps(
            record.get("news_data", {}),
            ensure_ascii=False
        )
    }


def save_fused_data(records):

    os.makedirs("DataSet", exist_ok=True)

    df = pd.DataFrame(records)

    output_file = "DataSet/fused_movies.csv"

    df.to_csv(
        output_file,
        index=False,
        encoding="utf-8"
    )

    print(f"Fused dataset saved to: {output_file}")
    print(f"Number of movies: {len(df)}")

    return df


# ==========================================
# TEST DATA FUSION
# ==========================================

if __name__ == "__main__":

    print("DATA FUSION SCRIPT STARTED")

    tmdb = {
        "title": "Inception",
        "release_date": "2010-07-15",
        "vote_average": 8.3,
        "genres": "Action, Adventure, Science Fiction",
        "overview": "A thief who steals corporate secrets through dream-sharing technology."
    }

    omdb = {
        "Title": "Inception",
        "Year": "2010",
        "Genre": "Action, Adventure, Sci-Fi",
        "Director": "Christopher Nolan",
        "Actors": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page",
        "imdbRating": "8.8",
        "Awards": "Won 4 Oscars"
    }

    watchmode = {
        "title_results": [
            {
                "name": "Inception",
                "type": "movie"
            }
        ]
    }

    news = {
        "articles": [
            {
                "title": "Latest news about Inception",
                "source": "Example News"
            }
        ]
    }

    fused = create_fused_movie_record(
        tmdb_data=tmdb,
        omdb_data=omdb,
        watchmode_data=watchmode,
        news_data=news
    )

    normalized = normalize_movie_record(fused)

    save_fused_data([normalized])