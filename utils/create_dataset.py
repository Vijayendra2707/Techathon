import pandas as pd

INPUT_FILE = "data/AccidentsBig.csv"
OUTPUT_FILE = "data/pune_cleaned_dataset.csv"

IMPORTANT_COLS = [
    "latitude","longitude","Accident_Severity","Date","Time",
    "Day_of_Week","Number_of_Vehicles","Number_of_Casualties",
    "Speed_limit","Weather_Conditions","Road_Surface_Conditions",
    "Light_Conditions","Road_Type","Junction_Detail",
    "Urban_or_Rural_Area"
]

LAT_MIN, LAT_MAX = 18.40, 18.70
LON_MIN, LON_MAX = 73.70, 74.05

CHUNK_SIZE = 50000  # load 50k rows at a time

print("Processing dataset in chunks...")

first_write = True

for chunk in pd.read_csv(
        INPUT_FILE,
        usecols=IMPORTANT_COLS,
        chunksize=CHUNK_SIZE,
        low_memory=True):

    # ---------------- CLEAN ----------------
    chunk = chunk.dropna(subset=[
        "latitude","longitude","Accident_Severity"
    ])

    # ---------------- FILTER PUNE ----------------
    chunk = chunk[
        (chunk["latitude"].between(LAT_MIN, LAT_MAX)) &
        (chunk["longitude"].between(LON_MIN, LON_MAX))
    ]

    # ---------------- APPEND TO FILE ----------------
    chunk.to_csv(
        OUTPUT_FILE,
        mode="w" if first_write else "a",
        header=first_write,
        index=False
    )

    first_write = False

print("✅ Pune dataset created successfully!")