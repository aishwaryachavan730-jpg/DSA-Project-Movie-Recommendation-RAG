import os
import sys
import pandas as pd


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# IMPORT SERVICES
# ============================================================

from services.tmdb_service import search_movie as search_tmdb
from services.omdb_service import search_movie as search_omdb
from services.watchmode_service import search_title as search_watchmode
from services.news_service import get_movie_news
from services.wikipedia_service import search_wikipedia


# ============================================================
# SAFE API CALL
# ============================================================

def safe_call(function, *args, **kwargs):

    try:

        result = function(
            *args,
            **kwargs
        )

        if result is None:
            return {}

        if isinstance(result, dict):

            return result

        return {
            "data": result
        }

    except Exception as error:

        print(
            f"API Error: {error}"
        )

        return {}


# ============================================================
# NORMALIZE RESULT
# ============================================================

def normalize_result(result):

    if not isinstance(
        result,
        dict
    ):
        return {}

    # Case:
    # {"success": True, "data": {...}}

    if (
        "data" in result
        and isinstance(
            result["data"],
            dict
        )
    ):

        data = result["data"].copy()

        if "success" in result:
            data["success"] = result["success"]

        return data

    return result


# ============================================================
# WATCHMODE DATA
# ============================================================

def extract_watchmode_data(
    watchmode
):

    platforms = []
    regions = []
    types = []

    sources = watchmode.get(
        "sources",
        []
    )

    if not isinstance(
        sources,
        list
    ):
        sources = []

    for source in sources:

        if not isinstance(
            source,
            dict
        ):
            continue

        name = source.get(
            "name"
        )

        region = source.get(
            "region"
        )

        source_type = source.get(
            "type"
        )

        if name:
            platforms.append(
                str(name)
            )

        if region:
            regions.append(
                str(region)
            )

        if source_type:
            types.append(
                str(source_type)
            )

    return {

        "streaming_platform": ", ".join(
            sorted(
                set(platforms)
            )
        ),

        "streaming_region": ", ".join(
            sorted(
                set(regions)
            )
        ),

        "streaming_type": ", ".join(
            sorted(
                set(types)
            )
        )
    }


# ============================================================
# NEWS DATA
# ============================================================

def extract_news_data(
    news
):

    articles = news.get(
        "articles",
        []
    )

    if not isinstance(
        articles,
        list
    ):
        articles = []

    news_count = len(
        articles
    )

    latest_news_title = ""

    if articles:

        first_article = articles[0]

        if isinstance(
            first_article,
            dict
        ):

            latest_news_title = (
                first_article.get(
                    "title",
                    ""
                )
            )

    return {

        "news_count": news_count,

        "latest_news_title":
            latest_news_title
    }


# ============================================================
# WIKIPEDIA DATA
# ============================================================

def extract_wikipedia_data(
    wikipedia
):

    return {

        "wikipedia_description":
            wikipedia.get(
                "description",
                ""
            ),

        "wikipedia_summary":
            wikipedia.get(
                "summary",
                ""
            )
    }


# ============================================================
# CREATE ONE FUSED RECORD
# ============================================================

def create_fused_record(
    movie_title
):

    print(
        f"\nCollecting data for: "
        f"{movie_title}"
    )

    # ========================================================
    # TMDB
    # ========================================================

    print(
        "1/5 Calling TMDB..."
    )

    tmdb = normalize_result(
        safe_call(
            search_tmdb,
            movie_title
        )
    )

    # ========================================================
    # OMDb
    # ========================================================

    print(
        "2/5 Calling OMDb..."
    )

    omdb = normalize_result(
        safe_call(
            search_omdb,
            movie_title
        )
    )

    # ========================================================
    # WatchMode
    # ========================================================

    print(
        "3/5 Calling WatchMode..."
    )

    watchmode = normalize_result(
        safe_call(
            search_watchmode,
            movie_title
        )
    )

    # ========================================================
    # News API
    # ========================================================

    print(
        "4/5 Calling News API..."
    )

    news = normalize_result(
        safe_call(
            get_movie_news,
            movie_title
        )
    )

    # ========================================================
    # Wikipedia
    # ========================================================

    print(
        "5/5 Calling Wikipedia..."
    )

    wikipedia = normalize_result(
        safe_call(
            search_wikipedia,
            movie_title
        )
    )

    # ========================================================
    # EXTRACT WATCHMODE
    # ========================================================

    watchmode_info = (
        extract_watchmode_data(
            watchmode
        )
    )

    # ========================================================
    # EXTRACT NEWS
    # ========================================================

    news_info = (
        extract_news_data(
            news
        )
    )

    # ========================================================
    # EXTRACT WIKIPEDIA
    # ========================================================

    wikipedia_info = (
        extract_wikipedia_data(
            wikipedia
        )
    )

    # ========================================================
    # CREATE MASTER RECORD
    # ========================================================

    record = {

        # ----------------------------------------------------
        # 1-6 TMDB
        # ----------------------------------------------------

        "movie_id":
            tmdb.get(
                "tmdb_id",
                tmdb.get(
                    "id",
                    ""
                )
            ),

        "movie_title":
            tmdb.get(
                "title",
                movie_title
            ),

        "release_date":
            tmdb.get(
                "release_date",
                ""
            ),

        "tmdb_rating":
            tmdb.get(
                "rating",
                tmdb.get(
                    "vote_average",
                    ""
                )
            ),

        "vote_count":
            tmdb.get(
                "vote_count",
                ""
            ),

        "overview":
            tmdb.get(
                "overview",
                ""
            ),

        # ----------------------------------------------------
        # 7-13 OMDb
        # ----------------------------------------------------

        "imdb_id":
            omdb.get(
                "imdb_id",
                ""
            ),

        "imdb_rating":
            omdb.get(
                "imdb_rating",
                ""
            ),

        "runtime":
            omdb.get(
                "runtime",
                ""
            ),

        "genre":
            omdb.get(
                "genre",
                ""
            ),

        "director":
            omdb.get(
                "director",
                ""
            ),

        "actors":
            omdb.get(
                "actors",
                ""
            ),

        "awards":
            omdb.get(
                "awards",
                ""
            ),

        # ----------------------------------------------------
        # 14-16 WatchMode
        # ----------------------------------------------------

        "streaming_platform":
            watchmode_info[
                "streaming_platform"
            ],

        "streaming_region":
            watchmode_info[
                "streaming_region"
            ],

        "streaming_type":
            watchmode_info[
                "streaming_type"
            ],

        # ----------------------------------------------------
        # 17-18 News API
        # ----------------------------------------------------

        "news_count":
            news_info[
                "news_count"
            ],

        "latest_news_title":
            news_info[
                "latest_news_title"
            ],

        # ----------------------------------------------------
        # 19-20 Wikipedia
        # ----------------------------------------------------

        "wikipedia_description":
            wikipedia_info[
                "wikipedia_description"
            ],

        "wikipedia_summary":
            wikipedia_info[
                "wikipedia_summary"
            ]
    }

    return record


# ============================================================
# MAIN FUSION FUNCTION
# ============================================================

def create_fused_dataset(
    movie_titles
):

    records = []

    for movie_title in movie_titles:

        movie_title = (
            movie_title.strip()
        )

        if not movie_title:
            continue

        try:

            record = create_fused_record(
                movie_title
            )

            records.append(
                record
            )

        except Exception as error:

            print(
                f"Failed for "
                f"{movie_title}: {error}"
            )

    # ========================================================
    # CREATE DATAFRAME
    # ========================================================

    df = pd.DataFrame(
        records
    )

    # ========================================================
    # REMOVE DUPLICATE MOVIES
    # ========================================================

    if not df.empty:

        df = df.drop_duplicates(
            subset=[
                "movie_title"
            ]
        )

    # ========================================================
    # SAVE EXCEL
    # ========================================================

    output_file = os.path.join(
        PROJECT_ROOT,
        "MovieVerse_Fused_Data.xlsx"
    )

    df.to_excel(
        output_file,
        index=False
    )

    print(
        "\n======================================"
    )

    print(
        "DATA FUSION COMPLETED"
    )

    print(
        "======================================"
    )

    print(
        f"Rows    : {len(df)}"
    )

    print(
        f"Columns : {len(df.columns)}"
    )

    print(
        f"File    : {output_file}"
    )

    print(
        "\nColumns:"
    )

    for number, column in enumerate(
        df.columns,
        start=1
    ):

        print(
            f"{number}. {column}"
        )

    return df


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":

    movies = [

        "Interstellar",

        "Inception",

        "The Dark Knight",

        "Avatar",

        "Titanic",

        "The Matrix",

        "Avengers: Endgame",

        "Jurassic Park",

        "Oppenheimer",

        "Dune"

    ]

    create_fused_dataset(
        movies
    )