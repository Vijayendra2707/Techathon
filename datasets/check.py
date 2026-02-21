import pandas as pd

df = pd.read_csv("AccidentsBig.csv", nrows=5)

important_cols = [
    "latitude",
    "longitude",
    "Accident_Severity",
    "Date",
    "Time",
    "Day_of_Week",
    "Number_of_Vehicles",
    "Number_of_Casualties",
    "Speed_limit",
    "Weather_Conditions",
    "Road_Surface_Conditions",
    "Light_Conditions",
    "Road_Type",
    "Junction_Detail",
    "Urban_or_Rural_Area"
]

print(df[important_cols].isnull().sum())