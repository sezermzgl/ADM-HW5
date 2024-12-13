import pandas as pd
import requests
import time


def get_coordinates(city_name, airport_code):
    url = "https://nominatim.openstreetmap.org/search"
    headers = {
        "User-Agent": "GeoCoordinateFinder (sezermzgl@gmail.com)"  # Replace with your app name and email
    }
    query = f"{city_name} airport {airport_code}"
    params = {"q": query, "format": "json", "limit": 1}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error with query '{query}': {e}")
        return None, None
