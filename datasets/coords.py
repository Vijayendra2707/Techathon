# -------------------------------
# SafePath AI - Pune Dataset Generator
# -------------------------------

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# -------------------------------
# Pune Boundary (ONLY Pune region)
# -------------------------------
PUNE_BOUNDARY = {
    "lat_min": 18.40,
    "lat_max": 18.70,
    "lon_min": 73.70,
    "lon_max": 74.05
}

# -------------------------------
# Major Pune Traffic Hubs
# -------------------------------
PUNE_HUBS = [
    ("Shivajinagar", 18.5308, 73.8475),
    ("Hinjewadi", 18.5912, 73.7389),
    ("Wakad", 18.5995, 73.7620),
    ("Baner", 18.5590, 73.7868),
    ("Hadapsar", 18.5089, 73.9260),
    ("Swargate", 18.5018, 73.8636),
    ("Viman Nagar", 18.5679, 73.9143)
]

# -------------------------------
# Possible Conditions
# -------------------------------
weather_types = ["Clear", "Rain", "Fog"]
road_types = ["Highway", "City Road", "Intersection"]
road_conditions = ["Dry", "Wet"]
vehicle_types = ["Car", "Bike", "Truck", "Bus"]

# -------------------------------
# Random datetime generator
# -------------------------------
def random_datetime():
    start = datetime(2023, 1, 1)
    end = datetime(2024, 1, 1)
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

# -------------------------------
# Generate Accident Records
# -------------------------------
records = []
accident_id = 1

for hub, lat, lon in PUNE_HUBS:

    for _ in range(400):   # accidents per hub

        latitude = lat + np.random.normal(0, 0.01)
        longitude = lon + np.random.normal(0, 0.01)

        dt = random_datetime()
        hour = dt.hour

        weather = np.random.choice(weather_types, p=[0.6, 0.3, 0.1])

        visibility = np.random.uniform(0.5, 1.0)
        if weather == "Fog":
            visibility *= 0.5

        traffic_level = np.random.randint(1, 6)

        severity = np.random.choice([1, 2, 3], p=[0.5, 0.35, 0.15])

        lighting = "Night" if hour < 6 or hour > 19 else "Daylight"

        records.append([
            accident_id,
            latitude,
            longitude,
            dt,
            hour,
            dt.weekday(),
            severity,
            weather,
            np.random.choice(road_types),
            visibility,
            traffic_level,
            np.random.choice(road_conditions),
            lighting,
            np.random.choice([0, 1]),  # junction
            np.random.choice([40, 60, 80]),
            np.random.choice(vehicle_types),
            hub
        ])

        accident_id += 1

# -------------------------------
# Add random scattered accidents
# -------------------------------
for _ in range(150):

    dt = random_datetime()

    records.append([
        accident_id,
        np.random.uniform(PUNE_BOUNDARY["lat_min"], PUNE_BOUNDARY["lat_max"]),
        np.random.uniform(PUNE_BOUNDARY["lon_min"], PUNE_BOUNDARY["lon_max"]),
        dt,
        dt.hour,
        dt.weekday(),
        random.choice([1, 2, 3]),
        random.choice(weather_types),
        random.choice(road_types),
        np.random.uniform(0.4, 1.0),
        random.randint(1, 5),
        random.choice(road_conditions),
        random.choice(["Daylight", "Night"]),
        random.choice([0, 1]),
        random.choice([40, 60, 80]),
        random.choice(vehicle_types),
        "Random"
    ])

    accident_id += 1

# -------------------------------
# Create DataFrame
# -------------------------------
columns = [
    "accident_id",
    "latitude",
    "longitude",
    "datetime",
    "hour",
    "day_of_week",
    "severity",
    "weather",
    "road_type",
    "visibility",
    "traffic_level",
    "road_condition",
    "lighting",
    "junction",
    "speed_limit",
    "vehicle_type",
    "area_name"
]

df = pd.DataFrame(records, columns=columns)

# -------------------------------
# Save Dataset
# -------------------------------
output_path = "./datasets/pune_accidents.csv"
df.to_csv(output_path, index=False)

print("✅ Dataset created successfully!")
print("Saved at:", output_path)
print("Total records:", len(df))