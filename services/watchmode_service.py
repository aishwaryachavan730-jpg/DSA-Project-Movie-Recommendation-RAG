import os
import requests
from dotenv import load_dotenv

load_dotenv()

WATCHMODE_API_KEY = os.getenv("WATCHMODE_API_KEY")

BASE_URL = "https://api.watchmode.com/v1"


def search_title(title):

    if not WATCHMODE_API_KEY:
        return {
            "success": False,
            "error": "WATCHMODE_API_KEY not found"
        }

    url = f"{BASE_URL}/search/"

    params = {
        "apiKey": WATCHMODE_API_KEY,
        "search_value": title,
        "search_field": "name"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        return {
            "success": True,
            "title": title,
            "results": data.get("title_results", [])
        }

    except Exception as e:

        return {
            "success": False,
            "title": title,
            "error": str(e)
        }


def get_sources(title_id):

    if not WATCHMODE_API_KEY:
        return {
            "success": False,
            "error": "WATCHMODE_API_KEY not found"
        }

    url = f"{BASE_URL}/title/{title_id}/sources/"

    params = {
        "apiKey": WATCHMODE_API_KEY
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        return {
            "success": True,
            "sources": response.json()
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":

    result = search_title("Inception")

    print(result)