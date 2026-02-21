import requests

# ==============================
# PUT YOUR API KEY HERE
# ==============================
API_KEY = "RqquJidW1U0KJTewBahEPpLQIRMRmqjg"


def get_routes(start_lat, start_lon, end_lat, end_lon):

    url = f"https://api.tomtom.com/routing/1/calculateRoute/{start_lat},{start_lon}:{end_lat},{end_lon}/json"

    params = {
        "key": API_KEY,
        "traffic": "true",          # IMPORTANT → enables traffic
        "routeType": "fastest",
        "maxAlternatives": 2        # gives multiple routes
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error:", response.text)
        return None

    data = response.json()

    routes = []

    for i, route in enumerate(data["routes"]):

        summary = route["summary"]

        # Extract route coordinates
        points = [
            (p["latitude"], p["longitude"])
            for leg in route["legs"]
            for p in leg["points"]
        ]

        routes.append({
            "route_id": i,
            "distance_m": summary["lengthInMeters"],
            "time_sec": summary["travelTimeInSeconds"],
            "traffic_delay_sec": summary["trafficDelayInSeconds"],
            "points": points
        })

    return routes


# ==============================
# TEST RUN (PUNE EXAMPLE)
# ==============================

if __name__ == "__main__":

    # Example: Pune Railway Station → FC Road
    start = (18.5286, 73.8743)
    end = (18.5204, 73.8567)

    routes = get_routes(*start, *end)

    if routes:
        print("\nRoutes Found:", len(routes))

        for r in routes:
            print("\nRoute", r["route_id"])
            print("Distance:", r["distance_m"], "meters")
            print("Time:", r["time_sec"], "seconds")
            print("Traffic Delay:", r["traffic_delay_sec"], "seconds")
            print("Points:", len(r["points"]))