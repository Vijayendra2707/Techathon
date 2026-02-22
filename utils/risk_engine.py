import pandas as pd

# -------------------------------
# SEVERITY WEIGHT
# -------------------------------
def compute_severity_weight(df):

    df["severity_weight"] = df["Accident_Severity"].apply(
        lambda x: 3 if x == 3 else 2 if x == 2 else 1
    )

    return df


# -------------------------------
# RISK SCORE (0–100)
# -------------------------------
def compute_risk_score(df):

    weather_risk = {
        "Fine": 0,
        "Rain": 2,
        "Fog": 3
    }

    light_risk = {
        "Daylight": 0,
        "Darkness - lights lit": 2,
        "Darkness - no lighting": 3
    }

    surface_risk = {
        "Dry": 0,
        "Wet": 2
    }

    df["weather_score"] = df["Weather_Conditions"].map(weather_risk).fillna(1)
    df["light_score"] = df["Light_Conditions"].map(light_risk).fillna(1)
    df["surface_score"] = df["Road_Surface_Conditions"].map(surface_risk).fillna(1)

    df["risk_score"] = (
        df["severity_weight"] * 25 +
        df["Number_of_Casualties"] * 5 +
        df["Speed_limit"] * 0.25 +
        df["weather_score"] * 10 +
        df["light_score"] * 10 +
        df["surface_score"] * 10
    )

    # Normalize
    df["risk_score"] = (
        100 * (df["risk_score"] - df["risk_score"].min())
        / (df["risk_score"].max() - df["risk_score"].min())
    )

    return df