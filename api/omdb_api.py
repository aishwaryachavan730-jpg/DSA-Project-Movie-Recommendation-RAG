import os
import requests
from dotenv import load_dotenv

load_dotenv()


def search_omdb(movie_name):
    url = "https://www.omdbapi.com/"

    api_key = os.getenv("OMDB_API_KEY")

    params = {
        "apikey": api_key,
        "t": movie_name
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        if data.get("Response") == "True":
            return data

        print("OMDb Error:", data.get("Error"))

    else:
        print("HTTP Error:", response.status_code)

    return None