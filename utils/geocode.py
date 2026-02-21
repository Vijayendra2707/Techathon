import requests

TOMTOM_API_KEY = "RqquJidW1U0KJTewBahEPpLQIRMRmqjg"


def geocode_location(query: str):
    """
    Convert place name → latitude, longitude
    """

    url = "https://api.tomtom.com/search/2/geocode/.json"

    params = {
        "key": TOMTOM_API_KEY,
        "query": query,   # ✅ correct way
        "limit": 1
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("TomTom Error:", response.text)
        return None

    data = response.json()

    # Debug (you can remove later)
    print("Geocode response:", data)

    if "results" not in data or len(data["results"]) == 0:
        return None

    position = data["results"][0]["position"]

    return position["lat"], position["lon"]