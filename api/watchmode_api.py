import os
import requests
from dotenv import load_dotenv

load_dotenv()

WATCHMODE_API_KEY = os.getenv("WATCHMODE_API_KEY")


def search_watchmode(movie_name):

    url = "https://api.watchmode.com/v1/search/"

    params = {
        "apiKey": WATCHMODE_API_KEY,
        "search_field": "name",
        "search_value": movie_name
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

    print("Watchmode Error:", response.status_code)
    print(response.text)

    return None