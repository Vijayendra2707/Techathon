import requests

TOMTOM_API_KEY = "RqquJidW1U0KJTewBahEPpLQIRMRmqjg"


def get_routes(start_lat, start_lon, end_lat, end_lon):

    url = f"https://api.tomtom.com/routing/1/calculateRoute/{start_lat},{start_lon}:{end_lat},{end_lon}/json"

    params = {
        "key": TOMTOM_API_KEY,
        "traffic": "true",
        "routeType": "fastest",
        "maxAlternatives": 2
    }

    response = requests.get(url, params=params)
    data = response.json()

    routes = []

    for i, route in enumerate(data["routes"]):

        points = [
            (p["latitude"], p["longitude"])
            for leg in route["legs"]
            for p in leg["points"]
        ]

        summary = route["summary"]

        routes.append({
            "route_id": i,
            "points": points,
            "time_sec": summary["travelTimeInSeconds"],
            "distance": summary["lengthInMeters"]
        })

    return routes   