import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

BASE_URL = "https://newsapi.org/v2/everything"


def search_movie_news(movie_name):
    params = {
        "q": movie_name,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=10
    )

    if response.status_code != 200:
        raise Exception(
            f"News API Error: {response.status_code} - {response.text}"
        )

    return response.json()