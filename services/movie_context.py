import os
import sys

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
from services.omdb_service import search_movie as search_omdb
from services.watchmode_service import search_title as search_watchmode
from services.news_service import get_movie_news


# ============================================================
# BUILD MOVIE CONTEXT
# ============================================================

def build_movie_context(
    movie_title,
    tmdb_data=None,
    omdb_data=None,
    watchmode_data=None,
    news_data=None,
    wikipedia_data=None
):
    """
    Build one combined movie context from:

    1. TMDB
    2. OMDb / IMDb
    3. WatchMode
    4. News API
    5. Wikipedia

    The final context can be sent to Gemini.
    """

    context_parts = []

    # ========================================================
    # MOVIE TITLE
    # ========================================================

    context_parts.append(
        f"""
MOVIE TITLE:
{movie_title}
""".strip()
    )

    # ========================================================
    # TMDB
    # ========================================================

    if tmdb_data:

        context_parts.append(
            f"""
TMDB INFORMATION:

Title:
{tmdb_data.get("title", movie_title)}

Overview:
{tmdb_data.get("overview", "Not available")}

Release Date:
{tmdb_data.get("release_date", "Not available")}

TMDB Rating:
{tmdb_data.get("rating", "Not available")}

Vote Count:
{tmdb_data.get("vote_count", "Not available")}

TMDB ID:
{tmdb_data.get("tmdb_id", "Not available")}
""".strip()
        )

    else:

        context_parts.append(
            "TMDB INFORMATION:\nNot available."
        )

    # ========================================================
    # OMDb / IMDb
    # ========================================================

    if omdb_data:

        context_parts.append(
            f"""
OMDb / IMDb INFORMATION:

Title:
{omdb_data.get("title", movie_title)}

Year:
{omdb_data.get("year", "Not available")}

IMDb Rating:
{omdb_data.get("imdb_rating", "Not available")}

Director:
{omdb_data.get("director", "Not available")}

Actors:
{omdb_data.get("actors", "Not available")}

Awards:
{omdb_data.get("awards", "Not available")}

Plot:
{omdb_data.get("plot", "Not available")}

Genre:
{omdb_data.get("genre", "Not available")}

Runtime:
{omdb_data.get("runtime", "Not available")}

IMDb ID:
{omdb_data.get("imdb_id", "Not available")}
""".strip()
        )

    else:

        context_parts.append(
            "OMDb / IMDb INFORMATION:\nNot available."
        )

    # ========================================================
    # WATCHMODE
    # ========================================================

    if watchmode_data:

        sources = watchmode_data.get(
            "sources",
            []
        )

        results = watchmode_data.get(
            "results",
            []
        )

        context_parts.append(
            f"""
WATCHMODE STREAMING INFORMATION:

Title:
{watchmode_data.get("title", movie_title)}

Search Results Found:
{len(results)}

Streaming Sources Found:
{len(sources)}
""".strip()
        )

        # ----------------------------------------------------
        # STREAMING SOURCES
        # ----------------------------------------------------

        if sources:

            source_text = []

            for index, source in enumerate(
                sources,
                start=1
            ):

                source_text.append(
                    f"""
Streaming Source {index}

Service:
{source.get("name", "Unknown")}

Type:
{source.get("type", "Unknown")}

Region:
{source.get("region", "Unknown")}

Format:
{source.get("format", "Unknown")}

Price:
{source.get("price", "Not available")}

URL:
{source.get("web_url", "Not available")}
""".strip()
                )

            context_parts.append(
                "\n\n".join(source_text)
            )

        else:

            context_parts.append(
                "No streaming sources available."
            )

    else:

        context_parts.append(
            "WATCHMODE STREAMING INFORMATION:\nNot available."
        )

    # ========================================================
    # NEWS API
    # ========================================================

    if news_data:

        articles = news_data.get(
            "articles",
            []
        )

        context_parts.append(
            f"""
RECENT MOVIE-RELATED NEWS:

Articles Found:
{len(articles)}
""".strip()
        )

        if articles:

            for index, article in enumerate(
                articles,
                start=1
            ):

                context_parts.append(
                    f"""
Article {index}

Title:
{article.get("title", "Not available")}

Description:
{article.get("description", "Not available")}

Source:
{article.get("source", "Unknown")}

Published:
{article.get("published_at", "Unknown")}

URL:
{article.get("url", "Not available")}
""".strip()
                )

        else:

            context_parts.append(
                "No recent news articles available."
            )

    else:

        context_parts.append(
            "RECENT MOVIE-RELATED NEWS:\nNot available."
        )

    # ========================================================
    # WIKIPEDIA
    # ========================================================

    if wikipedia_data:

        context_parts.append(
            f"""
WIKIPEDIA INFORMATION:

Title:
{wikipedia_data.get("title", movie_title)}

Description:
{wikipedia_data.get("description", "Not available")}

Summary:
{wikipedia_data.get("summary", "Not available")}

URL:
{wikipedia_data.get("url", "Not available")}
""".strip()
        )

    else:

        context_parts.append(
            "WIKIPEDIA INFORMATION:\nNot available."
        )

    # ========================================================
    # FINAL CONTEXT
    # ========================================================

    final_context = "\n\n".join(
        context_parts
    )

    return final_context