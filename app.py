
# ============================================================
# MOVIEVERSE AI
# app.py
#
# 5 DATA APIs:
# 1. TMDB
# 2. OMDb
# 3. WatchMode
# 4. News API
# 5. Wikipedia
#
# RAG + Gemini
# ============================================================

import os
import sys
import json
import pandas as pd
from datetime import datetime, date

import streamlit as st


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

# ---------------- TMDB ----------------

try:
    from services.tmdb_service import search_movie as search_tmdb

    TMDB_IMPORT_ERROR = None

except Exception as e:
    search_tmdb = None
    TMDB_IMPORT_ERROR = str(e)


# ---------------- OMDb ----------------

try:
    from services.omdb_service import search_movie as search_omdb

    OMDB_IMPORT_ERROR = None

except Exception as e:
    search_omdb = None
    OMDB_IMPORT_ERROR = str(e)


# ---------------- WatchMode ----------------

try:
    from services.watchmode_service import search_title as search_watchmode

    WATCHMODE_IMPORT_ERROR = None

except Exception as e:
    search_watchmode = None
    WATCHMODE_IMPORT_ERROR = str(e)


# ---------------- News API ----------------

try:
    from services.news_service import get_movie_news

    NEWS_IMPORT_ERROR = None

except Exception as e:
    get_movie_news = None
    NEWS_IMPORT_ERROR = str(e)


# ---------------- Wikipedia ----------------

try:
    from services.wikipedia_service import search_movie as search_wikipedia

    WIKIPEDIA_IMPORT_ERROR = None

except Exception as e:
    search_wikipedia = None
    WIKIPEDIA_IMPORT_ERROR = str(e)


# ---------------- TMDB Discovery ----------------

try:
    from services.movie_discovery_service import discover_movies

    DISCOVERY_IMPORT_ERROR = None

except Exception as e:
    discover_movies = None
    DISCOVERY_IMPORT_ERROR = str(e)


# ---------------- RAG Context ----------------

try:
    from services.movie_context import build_movie_context

    CONTEXT_IMPORT_ERROR = None

except Exception as e:
    build_movie_context = None
    CONTEXT_IMPORT_ERROR = str(e)



# ---------------- Gemini ----------------

try:
    from services.gemini_service import generate_recommendation

    GEMINI_IMPORT_ERROR = None

except Exception as e:
    generate_recommendation = None
    GEMINI_IMPORT_ERROR = str(e)


# ---------------- FAISS Movie Retriever ----------------

try:
    from rag.retriever import build_rag_context

    FAISS_IMPORT_ERROR = None

except Exception as e:
    build_rag_context = None
    FAISS_IMPORT_ERROR = str(e)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MovieVerse AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #0b1020;
        color: #f8fafc;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #374151;
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    h1, h2, h3, h4 {
        color: #ffffff !important;
    }

    p {
        color: #d1d5db;
    }

    .main-title {
        font-size: 48px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #9ca3af;
        margin-bottom: 25px;
    }

    .movie-card {
        background: #111827;
        border: 1px solid #374151;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
    }

    .api-card {
        background: #111827;
        border: 1px solid #374151;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.20);
    }

    .api-title {
        font-size: 21px;
        font-weight: 700;
        color: #ffffff;
    }

    .api-description {
        color: #9ca3af;
        margin-top: 5px;
    }

    [data-testid="stMetric"] {
        background: #111827;
        border: 1px solid #374151;
        padding: 18px;
        border-radius: 15px;
    }

    [data-testid="stMetricLabel"] {
        color: #9ca3af !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    .stTextInput input {
        background: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid #4b5563 !important;
        border-radius: 10px !important;
    }

    .stTextInput label {
        color: #ffffff !important;
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 700;
        min-height: 45px;
    }

    [data-testid="stExpander"] {
        background: #111827;
        border: 1px solid #374151;
        border-radius: 12px;
    }

    hr {
        border-color: #374151;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "search_result" not in st.session_state:
    st.session_state.search_result = ""

if "movie_data" not in st.session_state:
    st.session_state.movie_data = None

if "recommendation" not in st.session_state:
    st.session_state.recommendation = None


if "faiss_context" not in st.session_state:
    st.session_state.faiss_context = None

if "faiss_results" not in st.session_state:
    st.session_state.faiss_results = []


if "discovery_data" not in st.session_state:
    st.session_state.discovery_data = None

if "news_data" not in st.session_state:
    st.session_state.news_data = None


# ============================================================
# SAFE API CALL
# ============================================================

def safe_call(function, *args, **kwargs):

    if function is None:
        return {
            "success": False,
            "error": "Service could not be imported."
        }

    try:

        result = function(
            *args,
            **kwargs
        )

        if result is None:
            return {
                "success": False,
                "error": "API returned empty response."
            }

        if isinstance(result, dict):
            return result

        return {
            "success": True,
            "data": result
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }


# ============================================================
# NORMALIZE API RESULT
# ============================================================

def normalize_result(result):

    if result is None:
        return {
            "success": False,
            "error": "No result returned."
        }

    if not isinstance(result, dict):
        return {
            "success": True,
            "data": result
        }

    # Handle:
    #
    # {
    #     "success": True,
    #     "data": {...}
    # }

    if (
        "success" in result
        and "data" in result
        and isinstance(result["data"], dict)
    ):

        data = result["data"].copy()

        data["success"] = result.get(
            "success",
            True
        )

        if result.get("error"):
            data["error"] = result["error"]

        return data

    # If service returns normal data without success flag,
    # consider it successful.

    if "success" not in result:

        result = result.copy()
        result["success"] = True

    return result


# ============================================================
# POSTER URL
# ============================================================

def get_poster_url(poster_path):

    if not poster_path:
        return None

    poster_path = str(poster_path)

    if poster_path.startswith("http"):
        return poster_path

    return (
        "https://image.tmdb.org/t/p/w500"
        + poster_path
    )


# ============================================================
# FILTER RELEASED MOVIES
# ============================================================

def filter_released_movies(movies):

    today = date.today()

    filtered = []

    if not isinstance(movies, list):
        return filtered

    for movie in movies:

        if not isinstance(movie, dict):
            continue

        release_date = movie.get(
            "release_date",
            ""
        )

        if not release_date:
            continue

        try:

            release = datetime.strptime(
                release_date,
                "%Y-%m-%d"
            ).date()

            if release <= today:
                filtered.append(movie)

        except Exception:
            continue

    return filtered


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🎬 MovieVerse AI")

    st.caption(
        "LLM-Based Movie Recommendation System"
    )

    st.divider()

    menu = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "🔎 Movie Search",
            "🔥 Latest Movies",
            "📰 Movie News",
            "🤖 AI Recommendation",
            "📊 API Dashboard",
            "📄 JSON Result",
            "📈 ML Model Comparison",
        ]
    )

    st.divider()

    st.subheader("🔌 5 Data APIs")

    st.write("🎬 TMDB")
    st.write("⭐ OMDb")
    st.write("📺 WatchMode")
    st.write("📰 News API")
    st.write("📚 Wikipedia")

    st.divider()

    st.subheader("🤖 AI Layer")

    st.write("📖 RAG")
    st.write("✨ Gemini")

    st.divider()

    st.caption(
        "5 APIs + RAG + Gemini"
    )


# ============================================================
# HOME
# ============================================================

if menu == "🏠 Home":

    st.markdown(
        '<div class="main-title">🎬 MovieVerse AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitle">
        LLM-based movie recommendation system using
        five complementary data APIs, RAG and Gemini.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Data APIs",
            "5"
        )

    with col2:
        st.metric(
            "Architecture",
            "RAG"
        )

    with col3:
        st.metric(
            "LLM",
            "Gemini"
        )

    st.divider()

    st.subheader(
        "🎯 What can MovieVerse AI do?"
    )

    st.info(
        """
🎬 **TMDB** → Movie details, posters, ratings and release information

⭐ **OMDb** → IMDb rating, actors, director, genre and awards

📺 **WatchMode** → Streaming availability information

📰 **News API** → Recent movie-related news

📚 **Wikipedia** → Movie background and summary information

🤖 **RAG + Gemini** → Combines the collected information and generates an AI recommendation
"""
    )

    st.subheader(
        "🔎 Search a Movie"
    )

    home_query = st.text_input(
        "Enter movie name",
        placeholder="Example: Interstellar"
    )

    if st.button(
        "🔎 Search Movie",
        type="primary",
        use_container_width=True
    ):

        if not home_query.strip():

            st.warning(
                "Please enter a movie name."
            )

        else:

            st.session_state.search_result = (
                home_query.strip()
            )

            st.success(
                f"Movie selected: {home_query.strip()}"
            )

            st.info(
                "Open 'Movie Search' from the sidebar."
            )


# ============================================================
# MOVIE SEARCH
# ============================================================

elif menu == "🔎 Movie Search":

    st.title(
        "🔎 Movie Search"
    )

    st.write(
        "Search a movie across five complementary data APIs."
    )

    movie_query = st.text_input(
        "Enter movie title",
        value=st.session_state.search_result,
        placeholder="Example: Interstellar"
    )

    if st.button(
        "🔎 Search Movie",
        type="primary",
        use_container_width=True
    ):

        if not movie_query.strip():

            st.error(
                "Please enter a movie title."
            )

        else:

            movie_query = movie_query.strip()

            st.session_state.search_result = movie_query
            st.session_state.recommendation = None
            st.session_state.movie_context = None

            with st.spinner(
                "Collecting information from 5 APIs..."
            ):

                tmdb_data = normalize_result(
                    safe_call(
                        search_tmdb,
                        movie_query
                    )
                )

                omdb_data = normalize_result(
                    safe_call(
                        search_omdb,
                        movie_query
                    )
                )

                watchmode_data = normalize_result(
                    safe_call(
                        search_watchmode,
                        movie_query
                    )
                )

                news_data = normalize_result(
                    safe_call(
                        get_movie_news,
                        movie_query
                    )
                )

                wikipedia_data = normalize_result(
                    safe_call(
                        search_wikipedia,
                        movie_query
                    )
                )

            st.session_state.movie_data = {

                "movie_title": movie_query,

                "tmdb": tmdb_data,

                "omdb": omdb_data,

                "watchmode": watchmode_data,

                "news": news_data,

                "wikipedia": wikipedia_data
            }


    # ========================================================
    # DISPLAY RESULTS
    # ========================================================

    data = st.session_state.movie_data

    if data:

        movie_query = data["movie_title"]

        st.success(
            f"🎬 Results for: {movie_query}"
        )

        tmdb = data.get(
            "tmdb",
            {}
        )

        omdb = data.get(
            "omdb",
            {}
        )

        watchmode = data.get(
            "watchmode",
            {}
        )

        news = data.get(
            "news",
            {}
        )

        wikipedia = data.get(
            "wikipedia",
            {}
        )


        # ====================================================
        # API STATUS
        # ====================================================

        st.subheader(
            "🔌 API Connection Status"
        )

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:

            if tmdb.get("success"):
                st.success("🟢 TMDB")
            else:
                st.error("🔴 TMDB")

        with c2:

            if omdb.get("success"):
                st.success("🟢 OMDb")
            else:
                st.error("🔴 OMDb")

        with c3:

            if watchmode.get("success"):
                st.success("🟢 WatchMode")
            else:
                st.error("🔴 WatchMode")

        with c4:

            if news.get("success"):
                st.success("🟢 News API")
            else:
                st.error("🔴 News API")

        with c5:

            if wikipedia.get("success"):
                st.success("🟢 Wikipedia")
            else:
                st.error("🔴 Wikipedia")


        # ====================================================
        # TMDB
        # ====================================================

        st.divider()

        st.subheader(
            "🎬 TMDB — Movie Information"
        )

        if tmdb.get("success"):

            col1, col2 = st.columns(
                [1, 2]
            )

            with col1:

                poster_url = get_poster_url(
                    tmdb.get(
                        "poster_path"
                    )
                )

                if poster_url:

                    st.image(
                        poster_url,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "Poster not available."
                    )

            with col2:

                st.subheader(
                    tmdb.get(
                        "title",
                        movie_query
                    )
                )

                st.write(
                    f"📅 **Release Date:** "
                    f"{tmdb.get('release_date', 'N/A')}"
                )

                st.write(
                    f"⭐ **TMDB Rating:** "
                    f"{tmdb.get('rating', tmdb.get('vote_average', 'N/A'))}"
                )

                st.write(
                    f"👥 **Vote Count:** "
                    f"{tmdb.get('vote_count', 'N/A')}"
                )

                st.write(
                    f"🆔 **TMDB ID:** "
                    f"{tmdb.get('tmdb_id', tmdb.get('id', 'N/A'))}"
                )

                st.write(
                    "**Overview:**"
                )

                st.write(
                    tmdb.get(
                        "overview",
                        "No overview available."
                    )
                )

        else:

            st.error(
                f"TMDB error: "
                f"{tmdb.get('error', 'Unknown error')}"
            )


        # ====================================================
        # OMDb
        # ====================================================

        st.divider()

        st.subheader(
            "⭐ OMDb / IMDb"
        )

        if omdb.get("success"):

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "IMDb Rating",
                    omdb.get(
                        "imdb_rating",
                        "N/A"
                    )
                )

            with c2:

                st.metric(
                    "Year",
                    omdb.get(
                        "year",
                        "N/A"
                    )
                )

            with c3:

                st.metric(
                    "Runtime",
                    omdb.get(
                        "runtime",
                        "N/A"
                    )
                )

            st.write(
                f"🎬 **Director:** "
                f"{omdb.get('director', 'N/A')}"
            )

            st.write(
                f"👥 **Actors:** "
                f"{omdb.get('actors', 'N/A')}"
            )

            st.write(
                f"🎭 **Genre:** "
                f"{omdb.get('genre', 'N/A')}"
            )

            st.write(
                f"🏆 **Awards:** "
                f"{omdb.get('awards', 'N/A')}"
            )

            st.write(
                "**Plot:**"
            )

            st.write(
                omdb.get(
                    "plot",
                    "No plot available."
                )
            )

        else:

            st.error(
                f"OMDb error: "
                f"{omdb.get('error', 'Unknown error')}"
            )


        # ====================================================
        # WATCHMODE
        # ====================================================

        st.divider()

        st.subheader(
            "📺 WatchMode — Streaming"
        )

        if watchmode.get("success"):

            results = watchmode.get(
                "results",
                []
            )

            sources = watchmode.get(
                "sources",
                []
            )

            if not isinstance(results, list):
                results = []

            if not isinstance(sources, list):
                sources = []

            st.write(
                f"Search results: **{len(results)}**"
            )

            st.write(
                f"Streaming sources: **{len(sources)}**"
            )

            if sources:

                for source in sources[:10]:

                    if not isinstance(
                        source,
                        dict
                    ):
                        continue

                    st.write(
                        f"📺 **{source.get('name', 'Unknown')}**"
                    )

                    st.caption(
                        f"Type: {source.get('type', 'N/A')} | "
                        f"Region: {source.get('region', 'N/A')}"
                    )

                    if source.get("web_url"):

                        st.link_button(
                            "Watch / View",
                            source.get("web_url")
                        )

            elif results:

                for item in results[:10]:

                    if not isinstance(
                        item,
                        dict
                    ):
                        continue

                    st.write(
                        f"🎬 **{item.get('name', item.get('title', 'Unknown'))}** "
                        f"({item.get('year', 'N/A')})"
                    )

            else:

                st.info(
                    "No streaming information found."
                )

        else:

            st.error(
                f"WatchMode error: "
                f"{watchmode.get('error', 'Unknown error')}"
            )


        # ====================================================
        # NEWS API
        # ====================================================

        st.divider()

        st.subheader(
            "📰 News API — Recent News"
        )

        if news.get("success"):

            articles = news.get(
                "articles",
                []
            )

            if not isinstance(articles, list):
                articles = []

            if articles:

                for article in articles[:5]:

                    if not isinstance(
                        article,
                        dict
                    ):
                        continue

                    st.markdown(
                        f"### 📰 "
                        f"{article.get('title', 'Untitled')}"
                    )

                    st.write(
                        article.get(
                            "description",
                            "No description available."
                        )
                    )

                    st.caption(
                        f"{article.get('source', 'Unknown')} | "
                        f"{article.get('published_at', 'Unknown')}"
                    )

                    if article.get("url"):

                        st.link_button(
                            "Read Article",
                            article.get("url")
                        )

                    st.divider()

            else:

                st.info(
                    "No recent movie news found."
                )

        else:

            st.error(
                f"News API error: "
                f"{news.get('error', 'Unknown error')}"
            )


        # ====================================================
        # WIKIPEDIA
        # ====================================================

        st.divider()

        st.subheader(
            "📚 Wikipedia — Movie Background"
        )

        if wikipedia.get("success"):

            st.write(
                f"**Title:** "
                f"{wikipedia.get('title', movie_query)}"
            )

            description = wikipedia.get(
                "description"
            )

            if description:
                st.write(
                    f"**Description:** {description}"
                )

            st.write(
                wikipedia.get(
                    "summary",
                    "No Wikipedia summary available."
                )
            )

            if wikipedia.get("url"):

                st.link_button(
                    "📖 Open Wikipedia",
                    wikipedia.get("url")
                )

        else:

            st.error(
                f"Wikipedia error: "
                f"{wikipedia.get('error', 'Unknown error')}"
            )


        # ====================================================
        # RAW API DATA
        # ====================================================

        st.divider()

        st.subheader(
            "🔍 Raw API Responses"
        )

        with st.expander(
            "🎬 TMDB JSON"
        ):
            st.json(tmdb)

        with st.expander(
            "⭐ OMDb JSON"
        ):
            st.json(omdb)

        with st.expander(
            "📺 WatchMode JSON"
        ):
            st.json(watchmode)

        with st.expander(
            "📰 News API JSON"
        ):
            st.json(news)

        with st.expander(
            "📚 Wikipedia JSON"
        ):
            st.json(wikipedia)


# ============================================================
# LATEST MOVIES
# ============================================================

elif menu == "🔥 Latest Movies":

    st.title(
        "🔥 Latest Movies"
    )

    st.write(
        "Discover recently released movies using TMDB Discovery."
    )

    region = st.selectbox(
        "Region",
        [
            "IN",
            "US",
            "GB",
            "CA",
            "AU"
        ]
    )

    page = st.number_input(
        "Page",
        min_value=1,
        max_value=10,
        value=1,
        step=1
    )

    if st.button(
        "🔥 Discover Latest Movies",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "Loading latest movies..."
        ):

            discovery = normalize_result(
                safe_call(
                    discover_movies,
                    region=region,
                    page=int(page)
                )
            )

        if discovery.get("success"):

            movies = discovery.get(
                "movies",
                discovery.get(
                    "results",
                    []
                )
            )

            movies = filter_released_movies(
                movies
            )

            discovery["movies"] = movies

        st.session_state.discovery_data = discovery


    discovery = st.session_state.discovery_data

    if discovery:

        if discovery.get("success"):

            movies = discovery.get(
                "movies",
                discovery.get(
                    "results",
                    []
                )
            )

            movies = movies[:20]

            if movies:

                st.success(
                    f"Showing {len(movies)} released movies."
                )

                for index in range(
                    0,
                    len(movies),
                    4
                ):

                    row = movies[
                        index:index + 4
                    ]

                    columns = st.columns(4)

                    for col, movie in zip(
                        columns,
                        row
                    ):

                        with col:

                            poster_url = get_poster_url(
                                movie.get(
                                    "poster_path"
                                )
                            )

                            if poster_url:

                                st.image(
                                    poster_url,
                                    use_container_width=True
                                )

                            else:

                                st.info(
                                    "No poster"
                                )

                            st.markdown(
                                f"**{movie.get('title', 'Unknown Movie')}**"
                            )

                            st.caption(
                                f"📅 {movie.get('release_date', 'N/A')}"
                            )

                            st.caption(
                                f"⭐ {movie.get('rating', movie.get('vote_average', 'N/A'))}"
                            )

                            with st.expander(
                                "Details"
                            ):

                                st.write(
                                    movie.get(
                                        "overview",
                                        "No overview available."
                                    )
                                )

            else:

                st.info(
                    "No released movies found."
                )

        else:

            st.error(
                discovery.get(
                    "error",
                    "TMDB Discovery failed."
                )
            )


# ============================================================
# MOVIE NEWS
# ============================================================

elif menu == "📰 Movie News":

    st.title(
        "📰 Movie News"
    )

    query = st.text_input(
        "Movie / topic",
        placeholder="Example: Interstellar"
    )

    if st.button(
        "📰 Search News",
        type="primary",
        use_container_width=True
    ):

        if not query.strip():

            st.warning(
                "Please enter a movie or topic."
            )

        else:

            with st.spinner(
                "Searching News API..."
            ):

                news = normalize_result(
                    safe_call(
                        get_movie_news,
                        query.strip()
                    )
                )

            st.session_state.news_data = news


    news = st.session_state.news_data

    if news:

        if news.get("success"):

            articles = news.get(
                "articles",
                []
            )

            if not isinstance(articles, list):
                articles = []

            if articles:

                st.success(
                    f"{len(articles)} articles found."
                )

                for article in articles:

                    if not isinstance(
                        article,
                        dict
                    ):
                        continue

                    st.markdown(
                        f"### 📰 "
                        f"{article.get('title', 'Untitled')}"
                    )

                    st.write(
                        article.get(
                            "description",
                            "No description available."
                        )
                    )

                    st.caption(
                        f"Source: "
                        f"{article.get('source', 'Unknown')}"
                    )

                    if article.get("url"):

                        st.link_button(
                            "Read More",
                            article.get("url")
                        )

                    st.divider()

            else:

                st.info(
                    "No recent articles found."
                )

        else:

            st.error(
                news.get(
                    "error",
                    "News API failed."
                )
            )


# ============================================================
# AI RECOMMENDATION
# ============================================================

elif menu == "🤖 AI Recommendation":

    st.title(
        "🤖 AI Movie Recommendation"
    )

    st.write(
        "5 APIs → RAG Context → Gemini LLM → Recommendation"
    )

    recommendation_movie = st.text_input(
        "Enter movie title",
        placeholder="Example: Interstellar"
    )

    if st.button(
        "✨ Generate AI Recommendation",
        type="primary",
        use_container_width=True
    ):

        if not recommendation_movie.strip():

            st.warning(
                "Please enter a movie title."
            )

        elif build_movie_context is None:

            st.error(
                "movie_context.py could not be loaded."
            )

            st.code(
                CONTEXT_IMPORT_ERROR
            )

        elif generate_recommendation is None:

            st.error(
                "gemini_service.py could not be loaded."
            )

            st.code(
                GEMINI_IMPORT_ERROR
            )

        else:

            recommendation_movie = (
                recommendation_movie.strip()
            )

            with st.spinner(
                "Collecting data from 5 APIs..."
            ):

                tmdb = normalize_result(
                    safe_call(
                        search_tmdb,
                        recommendation_movie
                    )
                )

                omdb = normalize_result(
                    safe_call(
                        search_omdb,
                        recommendation_movie
                    )
                )

                watchmode = normalize_result(
                    safe_call(
                        search_watchmode,
                        recommendation_movie
                    )
                )

                news = normalize_result(
                    safe_call(
                        get_movie_news,
                        recommendation_movie
                    )
                )

                wikipedia = normalize_result(
                    safe_call(
                        search_wikipedia,
                        recommendation_movie
                    )
                )


            # ==================================================
            # BUILD RAG CONTEXT
            # ==================================================

            try:

                context = build_movie_context(

                    movie_title=recommendation_movie,

                    tmdb_data=tmdb,

                    omdb_data=omdb,

                    watchmode_data=watchmode,

                    news_data=news,

                    wikipedia_data=wikipedia
                )




                # ==================================================
                # FAISS MOVIE RETRIEVAL
                # ==================================================

                faiss_context = ""
                faiss_results = []

                if build_rag_context is not None:

                    try:

                        with st.spinner(
                            "Searching similar movies using FAISS..."
                        ):

                            faiss_context, faiss_results = (
                                build_rag_context(
                                    recommendation_movie,
                                    top_k=5
                                )
                            )

                        st.session_state.faiss_context = faiss_context
                        st.session_state.faiss_results = faiss_results

                    except Exception as error:

                        st.warning(
                            f"FAISS retrieval failed: {error}"
                        )

                else:

                    st.warning(
                        "FAISS retriever is unavailable: "
                        + str(FAISS_IMPORT_ERROR)
                    )

                    
                # Combine five API sources and FAISS results

                api_context = context

                context = (
                    "=== REQUESTED MOVIE: FIVE API DATA ===\n\n"
                    + api_context
                    + "\n\n"
                    "=== SIMILAR MOVIES: FAISS RETRIEVAL ===\n\n"
                    + (
                        faiss_context
                        if faiss_context
                        else "No similar movies were retrieved."
                    )
                )

            except Exception as error:

                context = ""

                st.error(
                    f"RAG context creation failed: {error}"
                )


            # ==================================================
            # DISPLAY API COLLECTION STATUS
            # ==================================================

            if context:

                st.success(
                    "📚 RAG context created successfully."
                )

                with st.expander(
                    "🔍 View collected API data"
                ):

                    st.write(
                        "🎬 TMDB:",
                        "Available" if tmdb.get("success")
                        else "Unavailable"
                    )

                    st.write(
                        "⭐ OMDb:",
                        "Available" if omdb.get("success")
                        else "Unavailable"
                    )

                    st.write(
                        "📺 WatchMode:",
                        "Available" if watchmode.get("success")
                        else "Unavailable"
                    )

                    st.write(
                        "📰 News API:",
                        "Available" if news.get("success")
                        else "Unavailable"
                    )

                    st.write(
                        "📚 Wikipedia:",
                        "Available" if wikipedia.get("success")
                        else "Unavailable"
                    )


            # ==================================================
            # GEMINI
            # ==================================================

            if context:

                with st.spinner(
                    "Gemini is generating recommendation..."
                ):

                    try:

                        result = generate_recommendation(

                            user_query=recommendation_movie,

                            movie_context=context
                        )

                        if isinstance(
                            result,
                            dict
                        ):

                            if result.get("success"):

                                response = result.get(
                                    "response",
                                    result.get(
                                        "recommendation",
                                        ""
                                    )
                                )

                                st.session_state.recommendation = (
                                    response
                                )

                                st.session_state.movie_context = (
                                    context
                                )

                            else:

                                st.error(
                                    result.get(
                                        "error",
                                        "Gemini failed."
                                    )
                                )

                        else:

                            st.session_state.recommendation = (
                                str(result)
                            )

                            st.session_state.movie_context = (
                                context
                            )

                    except Exception as error:

                        st.error(
                            f"Gemini error: {error}"
                        )

            else:

                st.error(
                    "RAG context could not be created."
                )


    # ========================================================
    # DISPLAY FAISS RESULTS
    # ========================================================

    if st.session_state.faiss_results:

        with st.expander(
            "🎯 View FAISS Similar Movie Results"
        ):

            for rank, movie in enumerate(
                st.session_state.faiss_results,
                start=1
            ):

                st.markdown(
                    f"**{rank}. {movie.get('movie_title', 'Unknown')}**"
                )

                st.write(
                    "Genre:",
                    movie.get("genres", "N/A")
                )

                st.write(
                    "Similarity:",
                    f"{movie.get('_similarity_score', 0):.4f}"
                )

                st.divider()


    # ========================================================
    # DISPLAY RECOMMENDATION
    # ========================================================

    if st.session_state.recommendation:

        st.divider()

        st.subheader(
            "🎬 AI Recommendation"
        )

        st.markdown(
            st.session_state.recommendation
        )

        with st.expander(
            "📚 View RAG Retrieved Context"
        ):

            st.text(
                st.session_state.movie_context
            )


# ============================================================
# API DASHBOARD
# ============================================================

elif menu == "📊 API Dashboard":

    st.title(
        "📊 API Integration Dashboard"
    )

    st.write(
        "MovieVerse AI integrates five complementary external data APIs."
    )

    st.divider()


    # ========================================================
    # TMDB
    # ========================================================

    st.subheader(
        "🎬 TMDB"
    )

    st.write(
        "Provides movie title, poster, overview, release date, "
        "ratings, vote count and movie ID."
    )

    if search_tmdb is not None:

        st.success(
            "🟢 TMDB service imported successfully."
        )

    else:

        st.error(
            f"🔴 TMDB import failed: {TMDB_IMPORT_ERROR}"
        )


    # ========================================================
    # OMDb
    # ========================================================

    st.divider()

    st.subheader(
        "⭐ OMDb"
    )

    st.write(
        "Provides IMDb rating, year, runtime, director, "
        "actors, genre, awards and plot."
    )

    if search_omdb is not None:

        st.success(
            "🟢 OMDb service imported successfully."
        )

    else:

        st.error(
            f"🔴 OMDb import failed: {OMDB_IMPORT_ERROR}"
        )


    # ========================================================
    # WATCHMODE
    # ========================================================

    st.divider()

    st.subheader(
        "📺 WatchMode"
    )

    st.write(
        "Provides movie/TV title and streaming availability information."
    )

    if search_watchmode is not None:

        st.success(
            "🟢 WatchMode service imported successfully."
        )

    else:

        st.error(
            f"🔴 WatchMode import failed: "
            f"{WATCHMODE_IMPORT_ERROR}"
        )


    # ========================================================
    # NEWS API
    # ========================================================

    st.divider()

    st.subheader(
        "📰 News API"
    )

    st.write(
        "Provides recent movie-related news articles."
    )

    if get_movie_news is not None:

        st.success(
            "🟢 News API service imported successfully."
        )

    else:

        st.error(
            f"🔴 News API import failed: "
            f"{NEWS_IMPORT_ERROR}"
        )


    # ========================================================
    # WIKIPEDIA
    # ========================================================

    st.divider()

    st.subheader(
        "📚 Wikipedia"
    )

    st.write(
        "Provides movie background, summary and reference information."
    )

    if search_wikipedia is not None:

        st.success(
            "🟢 Wikipedia service imported successfully."
        )

    else:

        st.error(
            f"🔴 Wikipedia import failed: "
            f"{WIKIPEDIA_IMPORT_ERROR}"
        )


    # ========================================================
    # DISCOVERY
    # ========================================================

    st.divider()

    st.subheader(
        "🔥 TMDB Discovery"
    )

    st.write(
        "Used for discovering latest and recently released movies."
    )

    if discover_movies is not None:

        st.success(
            "🟢 TMDB Discovery service imported successfully."
        )

    else:

        st.error(
            f"🔴 Discovery import failed: "
            f"{DISCOVERY_IMPORT_ERROR}"
        )


    # ========================================================
    # RAG
    # ========================================================

    st.divider()

    st.subheader(
        "📚 RAG Context"
    )

    st.write(
        "Combines information retrieved from the five data sources "
        "into one context for Gemini."
    )

    if build_movie_context is not None:

        st.success(
            "🟢 RAG context service imported successfully."
        )

    else:

        st.error(
            f"🔴 RAG import failed: "
            f"{CONTEXT_IMPORT_ERROR}"
        )


    # ========================================================
    # GEMINI
    # ========================================================

    st.divider()

    st.subheader(
        "🤖 Gemini LLM"
    )

    st.write(
        "Generates AI-powered recommendations from the RAG context."
    )

    if generate_recommendation is not None:

        st.success(
            "🟢 Gemini service imported successfully."
        )

    else:

        st.error(
            f"🔴 Gemini import failed: "
            f"{GEMINI_IMPORT_ERROR}"
        )


    # ========================================================
    # DATA FLOW
    # ========================================================

    st.divider()

    st.subheader(
        "🔄 MovieVerse AI Data Flow"
    )

    st.info(
        """
User enters movie name

↓

🎬 TMDB
Movie details + poster + rating

+

⭐ OMDb
IMDb + actors + director + awards

+

📺 WatchMode
Streaming information

+

📰 News API
Recent movie news

+

📚 Wikipedia
Background + summary

↓

📚 RAG Context

↓

🤖 Gemini LLM

↓

✨ AI Movie Recommendation
"""
    )



# ============================================================
# ML MODEL COMPARISON
# ============================================================

elif menu == "📈 ML Model Comparison":

    st.title("📈 ML Model Comparison")
    st.write(
        "Compare classification and regression algorithms "
        "used in the MovieVerse AI project."
    )

    ML_RESULTS_DIR = os.path.join(
        PROJECT_ROOT,
        "fused_data",
        "ML_Results"
    )

    # Load classification and regression results
    classification_file = os.path.join(
        ML_RESULTS_DIR,
        "classification_results.csv"
    )
    regression_file = os.path.join(
        ML_RESULTS_DIR,
        "regression_results.csv"
    )

    if (
        os.path.exists(classification_file)
        and os.path.exists(regression_file)
    ):

        classification_df = pd.read_csv(classification_file)
        regression_df = pd.read_csv(regression_file)

        st.subheader("1. Classification Algorithms")
        st.caption(
            "Task: Classify movies as High IMDb rating (≥ 7) "
            "or Low IMDb rating (< 7)."
        )

        classification_display = classification_df.copy()
        for col in ["Accuracy", "Precision", "Recall", "F1_Score"]:
            if col in classification_display.columns:
                classification_display[col] = (
                    classification_display[col].map(
                        lambda x: f"{x:.3f}"
                    )
                )

        st.dataframe(
            classification_display,
            use_container_width=True,
            hide_index=True
        )

        best_classifier = classification_df.loc[
            classification_df["Accuracy"].idxmax()
        ]

        st.success(
            f"Highest test accuracy: {best_classifier['Algorithm']} "
            f"({best_classifier['Accuracy']:.1%})"
        )

        st.subheader("2. Classification Accuracy Chart")

        accuracy_chart = os.path.join(
            ML_RESULTS_DIR,
            "charts",
            "classification_accuracy.png"
        )

        if os.path.exists(accuracy_chart):
            st.image(
                accuracy_chart,
                caption="Classification algorithm accuracy comparison",
                use_container_width=True
            )
        else:
            st.info("Classification accuracy chart was not found.")

        with st.expander("Understand classification metrics"):
            st.markdown(
                """
                - **Accuracy:** Percentage of all predictions that are correct.
                - **Precision:** Of the movies predicted as High, how many are actually High?
                - **Recall:** Of the actual High-rated movies, how many were identified?
                - **F1-score:** Balance between Precision and Recall.
                """
            )

        st.divider()

        st.subheader("3. Regression Algorithms")
        st.caption(
            "Task: Predict a movie's IMDb rating using numeric features."
        )

        regression_display = regression_df.copy()
        for col in ["MAE", "RMSE", "R2_Score"]:
            if col in regression_display.columns:
                regression_display[col] = (
                    regression_display[col].map(
                        lambda x: f"{x:.3f}"
                    )
                )

        st.dataframe(
            regression_display,
            use_container_width=True,
            hide_index=True
        )

        best_regressor = regression_df.loc[
            regression_df["MAE"].idxmin()
        ]

        st.success(
            f"Lowest test MAE: {best_regressor['Algorithm']} "
            f"({best_regressor['MAE']:.3f})"
        )

        st.subheader("4. Regression Performance Charts")

        chart_col1, chart_col2 = st.columns(2)

        mae_chart = os.path.join(
            ML_RESULTS_DIR,
            "charts",
            "regression_mae.png"
        )
        r2_chart = os.path.join(
            ML_RESULTS_DIR,
            "charts",
            "regression_r2.png"
        )

        with chart_col1:
            st.markdown("**Mean Absolute Error (MAE)**")
            if os.path.exists(mae_chart):
                st.image(mae_chart, use_container_width=True)
            else:
                st.info("MAE chart was not found.")

        with chart_col2:
            st.markdown("**R² Score**")
            if os.path.exists(r2_chart):
                st.image(r2_chart, use_container_width=True)
            else:
                st.info("R² chart was not found.")

        with st.expander("Understand regression metrics"):
            st.markdown(
                """
                - **MAE:** Average absolute difference between actual and predicted ratings. Lower is better.
                - **RMSE:** Error measure that penalizes larger errors more strongly. Lower is better.
                - **R² Score:** Indicates how well the model explains rating variation. Closer to 1 is generally better.
                """
            )

        st.divider()

        st.subheader("5. Project Conclusion")
        st.markdown(
            """
            - Random Forest achieved the highest classification accuracy
              in the current test split.
            - Polynomial Regression achieved the lowest MAE and highest
              R² score among the tested regression models.
            - The results are based on a small dataset, so further
              cross-validation is needed before concluding that these
              models will perform equally well on new movies.
            """
        )

    else:
        st.error(
            "ML result files are missing. Please check the "
            "fused_data/ML_Results folder."
        )


# ============================================================
# JSON RESULT
# ============================================================

elif menu == "📄 JSON Result":

    st.title(
        "📄 Movie Integration JSON"
    )

    json_file = os.path.join(
        PROJECT_ROOT,
        "movie_integration_result.json"
    )

    if os.path.exists(json_file):

        try:

            with open(
                json_file,
                "r",
                encoding="utf-8"
            ) as file:

                json_data = json.load(
                    file
                )

            st.success(
                "JSON integration result loaded."
            )

            st.json(
                json_data
            )

            json_string = json.dumps(
                json_data,
                indent=4,
                ensure_ascii=False,
                default=str
            )

            st.download_button(
                "⬇️ Download JSON",
                data=json_string,
                file_name="movie_integration_result.json",
                mime="application/json",
                use_container_width=True
            )

        except Exception as error:

            st.error(
                f"Could not read JSON file: {error}"
            )

    else:

        st.info(
            "movie_integration_result.json "
            "has not been generated yet."
        )


# ============================================================
# END OF APP
# ============================================================
