import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

BASE_URL = "https://newsapi.org/v2/everything"


def get_movie_news(title):

    if not NEWS_API_KEY:
        return {
            "success": False,
            "error": "NEWS_API_KEY not found"
        }

    params = {
        "apiKey": NEWS_API_KEY,
        "q": title,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5
    }

    try:

        response = requests.get(
            BASE_URL,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        articles = []

        for article in data.get("articles", []):

            articles.append({
                "title": article.get("title"),
                "description": article.get("description"),
                "url": article.get("url"),
                "published_at": article.get(
                    "publishedAt"
                ),
                "source": (
                    article.get("source", {})
                    .get("name")
                )
            })

        return {
            "success": True,
            "movie": title,
            "articles": articles
        }

    except Exception as e:

        return {
            "success": False,
            "movie": title,
            "error": str(e)
        }


if __name__ == "__main__":

    result = get_movie_news("Inception")

    print(result)
    