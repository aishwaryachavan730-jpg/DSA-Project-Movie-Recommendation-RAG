def detect_movie_query(query):

    query = query.lower().strip()

    language_map = {
        "marathi": "mr",
        "hindi": "hi",
        "tamil": "ta",
        "telugu": "te",
        "malayalam": "ml",
        "kannada": "kn",
        "bengali": "bn",
        "punjabi": "pa"
    }

    latest_keywords = [
        "latest",
        "new",
        "recent",
        "newest",
        "upcoming"
    ]

    is_latest = any(
        word in query
        for word in latest_keywords
    )

    detected_language = None

    for language_name, language_code in language_map.items():

        if language_name in query:
            detected_language = language_code
            break

    return {
        "is_latest": is_latest,
        "language": detected_language,
        "region": "IN"
    }