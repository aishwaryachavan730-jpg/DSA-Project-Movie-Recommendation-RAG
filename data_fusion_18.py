import os
import sys
import time
import pandas as pd

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# IMPORT YOUR EXISTING 5 API SERVICES
# ============================================================

from services.tmdb_service import search_movie as search_tmdb

from services.omdb_service import (
    search_movie as search_omdb
)

from services.watchmode_service import (
    search_title as search_watchmode,
    get_sources
)

from services.news_service import (
    get_movie_news
)

from services.wikipedia_service import (
    search_wikipedia
)


# ============================================================
# FILE PATHS
# ============================================================

INPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "DataSet",
    "TMDB_movie_dataset_v11.csv"
)

OUTPUT_CSV = os.path.join(
    PROJECT_ROOT,
    "DataSet",
    "MovieVerse_Fused_18_Columns.csv"
)

OUTPUT_EXCEL = os.path.join(
    PROJECT_ROOT,
    "MovieVerse_Fused_18_Columns.xlsx"
)


# ============================================================
# NUMBER OF MOVIES
# ============================================================
#
# IMPORTANT:
# Do NOT process 899,104 movies.
#
# For your assignment use 50 or 100 movies.
#
# Change this to 50 if required.
# ============================================================

MAX_MOVIES = 100


# ============================================================
# SAFE API CALL
# ============================================================

def safe_call(function, *args):

    try:

        result = function(*args)

        if result is None:

            return {
                "success": False,
                "error": "No data returned"
            }

        if isinstance(result, dict):

            return result

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        print(
            f"    API ERROR: {function.__name__}: {e}"
        )

        return {
            "success": False,
            "error": str(e)
        }


# ============================================================
# SAFE VALUE
# ============================================================

def get_value(data, key, default="Not Available"):

    if not isinstance(data, dict):
        return default

    value = data.get(key)

    if value is None:
        return default

    if isinstance(value, str) and not value.strip():
        return default

    return value


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(value):

    if value is None:
        return ""

    value = str(value)

    value = value.replace("\n", " ")
    value = value.replace("\r", " ")
    value = value.replace("\t", " ")

    return " ".join(value.split())


# ============================================================
# WATCHMODE DATA
# ============================================================

def get_watchmode_information(movie_title):

    result = safe_call(
        search_watchmode,
        movie_title
    )

    if not result.get("success"):

        return {
            "streaming_platforms": "Not Available",
            "streaming_region": "Not Available"
        }

    results = result.get(
        "results",
        []
    )

    if not results:

        return {
            "streaming_platforms": "Not Available",
            "streaming_region": "Not Available"
        }

    # --------------------------------------------------------
    # Select first/best result
    # --------------------------------------------------------

    best_match = results[0]

    watchmode_id = best_match.get("id")

    if not watchmode_id:

        return {
            "streaming_platforms": "Not Available",
            "streaming_region": "Not Available"
        }

    # --------------------------------------------------------
    # Get streaming sources
    # --------------------------------------------------------

    sources_result = safe_call(
        get_sources,
        watchmode_id
    )

    if not sources_result.get("success"):

        return {
            "streaming_platforms": "Not Available",
            "streaming_region": "Not Available"
        }

    sources = sources_result.get(
        "sources",
        []
    )

    if not sources:

        return {
            "streaming_platforms": "Not Available",
            "streaming_region": "Not Available"
        }

    platforms = []
    regions = []

    for source in sources:

        name = source.get(
            "name"
        )

        region = source.get(
            "region"
        )

        if name:

            platforms.append(
                str(name)
            )

        if region:

            regions.append(
                str(region)
            )

    platforms = list(
        dict.fromkeys(platforms)
    )

    regions = list(
        dict.fromkeys(regions)
    )

    return {

        "streaming_platforms":
            ", ".join(platforms)
            if platforms
            else "Not Available",

        "streaming_region":
            ", ".join(regions)
            if regions
            else "Not Available"
    }


# ============================================================
# NEWS API DATA
# ============================================================

def get_news_information(movie_title):

    result = safe_call(
        get_movie_news,
        movie_title
    )

    if not result.get("success"):

        return {
            "news_count": 0,
            "latest_news": "No recent news available."
        }

    articles = result.get(
        "articles",
        []
    )

    if not articles:

        return {
            "news_count": 0,
            "latest_news": "No recent news available."
        }

    news_titles = []

    for article in articles[:3]:

        title = article.get(
            "title"
        )

        if title:

            news_titles.append(
                clean_text(title)
            )

    return {

        "news_count": len(articles),

        "latest_news":
            " | ".join(news_titles)
            if news_titles
            else "No recent news available."
    }


# ============================================================
# WIKIPEDIA DATA
# ============================================================

def get_wikipedia_information(movie_title):

    result = safe_call(
        search_wikipedia,
        movie_title
    )

    if not result.get("success"):

        return {

            "wikipedia_summary":
                "Wikipedia information not available.",

            "wikipedia_url":
                "Not Available"
        }

    return {

        "wikipedia_summary":
            clean_text(
                get_value(
                    result,
                    "summary",
                    "Wikipedia information not available."
                )
            ),

        "wikipedia_url":
            get_value(
                result,
                "url",
                "Not Available"
            )
    }


# ============================================================
# CREATE ONE FUSED MOVIE RECORD
# ============================================================

def create_fused_record(
    original_row,
    movie_title
):

    print(
        f"\n{'-' * 70}"
    )

    print(
        f"Movie: {movie_title}"
    )

    print(
        f"{'-' * 70}"
    )


    # ========================================================
    # 1. TMDB
    # ========================================================

    print("  TMDB...")

    tmdb = safe_call(
        search_tmdb,
        movie_title
    )


    # ========================================================
    # 2. OMDb
    # ========================================================

    print("  OMDb...")

    omdb = safe_call(
        search_omdb,
        movie_title
    )


    # ========================================================
    # 3. WATCHMODE
    # ========================================================

    print("  WatchMode...")

    watchmode = get_watchmode_information(
        movie_title
    )


    # ========================================================
    # 4. NEWS API
    # ========================================================

    print("  News API...")

    news = get_news_information(
        movie_title
    )


    # ========================================================
    # 5. WIKIPEDIA
    # ========================================================

    print("  Wikipedia...")

    wikipedia = get_wikipedia_information(
        movie_title
    )


    # ========================================================
    # CREATE EXACTLY 18 COLUMNS
    # ========================================================

    record = {

        # ----------------------------------------------------
        # PRIMARY / FUSION KEY
        # ----------------------------------------------------

        "movie_title":
            movie_title,


        # ----------------------------------------------------
        # TMDB
        # ----------------------------------------------------

        "overview":
            clean_text(
                get_value(
                    tmdb,
                    "overview",
                    original_row.get(
                        "overview",
                        "Not Available"
                    )
                )
            ),

        "genres":
            clean_text(
                get_value(
                    tmdb,
                    "genres",
                    original_row.get(
                        "genres",
                        "Not Available"
                    )
                )
            ),

        "release_date":
            get_value(
                tmdb,
                "release_date",
                original_row.get(
                    "release_date",
                    "Not Available"
                )
            ),

        "tmdb_rating":
            get_value(
                tmdb,
                "rating",
                original_row.get(
                    "vote_average",
                    "Not Available"
                )
            ),

        "vote_count":
            get_value(
                tmdb,
                "vote_count",
                original_row.get(
                    "vote_count",
                    "Not Available"
                )
            ),

        "popularity":
            get_value(
                tmdb,
                "popularity",
                original_row.get(
                    "popularity",
                    "Not Available"
                )
            ),


        # ----------------------------------------------------
        # OMDb / IMDb
        # ----------------------------------------------------

        "imdb_rating":
            get_value(
                omdb,
                "imdb_rating",
                "Not Available"
            ),

        "runtime":
            get_value(
                omdb,
                "runtime",
                "Not Available"
            ),

        "director":
            clean_text(
                get_value(
                    omdb,
                    "director",
                    "Not Available"
                )
            ),

        "actors":
            clean_text(
                get_value(
                    omdb,
                    "actors",
                    "Not Available"
                )
            ),

        "awards":
            clean_text(
                get_value(
                    omdb,
                    "awards",
                    "Not Available"
                )
            ),


        # ----------------------------------------------------
        # WATCHMODE
        # ----------------------------------------------------

        "streaming_platforms":
            watchmode[
                "streaming_platforms"
            ],

        "streaming_region":
            watchmode[
                "streaming_region"
            ],


        # ----------------------------------------------------
        # NEWS API
        # ----------------------------------------------------

        "news_count":
            news[
                "news_count"
            ],

        "latest_news":
            news[
                "latest_news"
            ],


        # ----------------------------------------------------
        # WIKIPEDIA
        # ----------------------------------------------------

        "wikipedia_summary":
            wikipedia[
                "wikipedia_summary"
            ],

        "wikipedia_url":
            wikipedia[
                "wikipedia_url"
            ]
    }


    return record


# ============================================================
# MAIN DATA FUSION
# ============================================================

def main():

    print(
        "\n" + "=" * 70
    )

    print(
        "MOVIEVERSE AI - 18 COLUMN DATA FUSION"
    )

    print(
        "=" * 70
    )


    # ========================================================
    # CHECK INPUT FILE
    # ========================================================

    if not os.path.exists(INPUT_FILE):

        print(
            "\nERROR: INPUT FILE NOT FOUND"
        )

        print(
            f"\nExpected:"
        )

        print(
            INPUT_FILE
        )

        return


    print(
        f"\nDataset selected:"
    )

    print(
        INPUT_FILE
    )


    # ========================================================
    # LOAD DATASET
    # ========================================================

    print(
        "\nLoading original dataset..."
    )

    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )


    print(
        f"\nOriginal rows: {len(df)}"
    )

    print(
        f"Original columns: {len(df.columns)}"
    )


    print(
        "\nOriginal columns:"
    )

    for column in df.columns:

        print(
            f" - {column}"
        )


    # ========================================================
    # FIND TITLE COLUMN
    # ========================================================

    title_column = None

    for column in df.columns:

        if column.lower() == "title":

            title_column = column
            break


    if title_column is None:

        print(
            "\nERROR: title column not found."
        )

        return


    print(
        f"\nFusion source title column: "
        f"{title_column}"
    )


    # ========================================================
    # REMOVE EMPTY TITLES
    # ========================================================

    df = df[
        df[title_column]
        .notna()
    ].copy()


    # ========================================================
    # NORMALIZE TITLES
    # ========================================================

    df["movie_title"] = (
        df[title_column]
        .astype(str)
        .str.strip()
    )


    df = df[
        df["movie_title"] != ""
    ]


    # ========================================================
    # REMOVE DUPLICATE TITLES
    # ========================================================

    df = df.drop_duplicates(
        subset=["movie_title"],
        keep="first"
    )


    print(
        f"\nUnique movies: {len(df)}"
    )


    # ========================================================
    # LIMIT MOVIES
    # ========================================================

    df = df.head(
        MAX_MOVIES
    ).copy()


    print(
        f"Movies selected for fusion: "
        f"{len(df)}"
    )


    # ========================================================
    # FUSION
    # ========================================================

    fused_records = []

    total = len(df)


    for index, (_, row) in enumerate(
        df.iterrows(),
        start=1
    ):

        movie_title = str(
            row["movie_title"]
        ).strip()


        print(
            f"\n[{index}/{total}] "
            f"{movie_title}"
        )


        original_row = row.to_dict()


        record = create_fused_record(
            original_row,
            movie_title
        )


        fused_records.append(
            record
        )


        # ----------------------------------------------------
        # SMALL DELAY
        # ----------------------------------------------------

        time.sleep(0.3)


        # ----------------------------------------------------
        # SAVE PROGRESS
        # ----------------------------------------------------

        if index % 10 == 0:

            progress_df = pd.DataFrame(
                fused_records
            )

            progress_df.to_csv(
                OUTPUT_CSV,
                index=False,
                encoding="utf-8-sig"
            )

            print(
                f"\nProgress saved: "
                f"{index}/{total}"
            )


    # ========================================================
    # CREATE FINAL DATAFRAME
    # ========================================================

    fused_df = pd.DataFrame(
        fused_records
    )


    # ========================================================
    # FORCE EXACT COLUMN ORDER
    # ========================================================

    final_columns = [

        "movie_title",

        "overview",

        "genres",

        "release_date",

        "tmdb_rating",

        "vote_count",

        "popularity",

        "imdb_rating",

        "runtime",

        "director",

        "actors",

        "awards",

        "streaming_platforms",

        "streaming_region",

        "news_count",

        "latest_news",

        "wikipedia_summary",

        "wikipedia_url"
    ]


    fused_df = fused_df[
        final_columns
    ]


    # ========================================================
    # REMOVE DUPLICATE PRIMARY KEY
    # ========================================================

    fused_df = fused_df.drop_duplicates(
        subset=["movie_title"],
        keep="first"
    )


    # ========================================================
    # SAVE CSV
    # ========================================================

    fused_df.to_csv(
        OUTPUT_CSV,
        index=False,
        encoding="utf-8-sig"
    )


    # ========================================================
    # SAVE EXCEL
    # ========================================================

    fused_df.to_excel(
        OUTPUT_EXCEL,
        index=False,
        engine="openpyxl"
    )


    # ========================================================
    # FINAL REPORT
    # ========================================================

    print(
        "\n" + "=" * 70
    )

    print(
        "DATA FUSION COMPLETED SUCCESSFULLY"
    )

    print(
        "=" * 70
    )


    print(
        f"\nRows created: "
        f"{len(fused_df)}"
    )

    print(
        f"Columns created: "
        f"{len(fused_df.columns)}"
    )


    print(
        "\nFinal 18 columns:"
    )

    for number, column in enumerate(
        fused_df.columns,
        start=1
    ):

        print(
            f"{number:02d}. {column}"
        )


    print(
        "\nPrimary / Fusion Key:"
    )

    print(
        "movie_title"
    )


    print(
        "\nCSV file:"
    )

    print(
        OUTPUT_CSV
    )


    print(
        "\nExcel file:"
    )

    print(
        OUTPUT_EXCEL
    )


    print(
        "\n" + "=" * 70
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()