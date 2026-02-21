import numpy as np
import pandas as pd


# =====================================================
# FEATURE ENGINEERING
# =====================================================
def create_features(df):

    df = df.copy()

    # -----------------------
    # TIME FEATURES
    # -----------------------
    df["hour"] = (
        df["Time"]
        .astype(str)
        .str.split(":")
        .str[0]
        .astype(float)
        .fillna(12)
    )

    df["is_night"] = ((df["hour"] < 6) | (df["hour"] > 20)).astype(int)

    # -----------------------
    # WEATHER (robust)
    # -----------------------
    df["bad_weather"] = (
        df["Weather_Conditions"]
        .astype(str)
        .str.contains("Rain|Fog|Snow|Storm", case=False, na=False)
        .astype(int)
    )

    # -----------------------
    # LIGHT CONDITIONS
    # -----------------------
    df["dark"] = (
        df["Light_Conditions"]
        .astype(str)
        .str.contains("Dark", case=False, na=False)
        .astype(int)
    )

    # -----------------------
    # LOCATION BUCKETS ⭐⭐⭐
    # (MOST IMPORTANT FEATURE)
    # -----------------------
    df["lat_bucket"] = (df["latitude"] * 50).astype(int)
    df["lon_bucket"] = (df["longitude"] * 50).astype(int)

    # -----------------------
    # TARGET LABEL
    # -----------------------
    df["accident_label"] = 1

    return df


# =====================================================
# NEGATIVE SAMPLE GENERATION
# =====================================================
def generate_negative_samples(df, n_samples=None):

    # balance dataset automatically
    if n_samples is None:
        n_samples = len(df)

    lat_min, lat_max = df["latitude"].min(), df["latitude"].max()
    lon_min, lon_max = df["longitude"].min(), df["longitude"].max()

    safe = df.sample(n_samples, replace=True).copy()

    # random safe locations
    safe["latitude"] = np.random.uniform(lat_min, lat_max, n_samples)
    safe["longitude"] = np.random.uniform(lon_min, lon_max, n_samples)

    # safer assumptions
    safe["bad_weather"] = 0
    safe["dark"] = 0
    safe["is_night"] = 0

    # recompute spatial buckets
    safe["lat_bucket"] = (safe["latitude"] * 50).astype(int)
    safe["lon_bucket"] = (safe["longitude"] * 50).astype(int)

    safe["accident_label"] = 0

    return safe