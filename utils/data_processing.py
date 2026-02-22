import pandas as pd

IMPORTANT_COLS = [
    "latitude","longitude","Accident_Severity","Date","Time",
    "Day_of_Week","Number_of_Vehicles","Number_of_Casualties",
    "Speed_limit","Weather_Conditions","Road_Surface_Conditions",
    "Light_Conditions","Road_Type","Junction_Detail",
    "Urban_or_Rural_Area"
]

# Pune Bounding Box
LAT_MIN, LAT_MAX = 18.40, 18.70
LON_MIN, LON_MAX = 73.70, 74.05


def load_data(path="data/pune_cleaned_dataset.csv"):
    df = pd.read_csv(path)
    ROAD_TYPE_MAP = {
    1: "Roundabout",
    2: "One way street",
    3: "Dual carriageway",
    6: "Single carriageway",
    7: "Slip road",
    9: "Unknown"
}

    df["Road_Type"] = df["Road_Type"].map(ROAD_TYPE_MAP).fillna("Unknown")
    df = df[IMPORTANT_COLS]
    df = df.dropna(subset=["latitude","longitude"])

    df["Accident_Severity"] = pd.to_numeric(
        df["Accident_Severity"], errors="coerce"
    )

    # Filter Pune region
    df = df[
        (df["latitude"] >= LAT_MIN) &
        (df["latitude"] <= LAT_MAX) &
        (df["longitude"] >= LON_MIN) &
        (df["longitude"] <= LON_MAX)
    ]

    return df