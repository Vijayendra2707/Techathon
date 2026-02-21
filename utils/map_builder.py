import folium
from folium.plugins import HeatMap
import numpy as np
import pandas as pd

PUNE_CENTER = [18.5204, 73.8567]

GRADIENT = {
    "0.2": "blue",
    "0.4": "lime",
    "0.6": "yellow",
    "0.8": "orange",
    "1.0": "red"
}


# -----------------------------
# NORMALIZATION FUNCTION
# -----------------------------
def normalize(series):
    series = series.fillna(0)

    min_v = series.min()
    max_v = series.max()

    if max_v == min_v:
        return series * 0

    return ((series - min_v) / (max_v - min_v)).astype(float)


# -----------------------------
# MAP BUILDER
# -----------------------------
def build_map(df):

    # ---------- CLEAN DATA ----------
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["latitude", "longitude"])

    df["severity_weight"] = pd.to_numeric(
        df["severity_weight"], errors="coerce"
    ).fillna(0)

    df["risk_score"] = pd.to_numeric(
        df["risk_score"], errors="coerce"
    ).fillna(0)

    if "risk_prediction" in df.columns:
        df["risk_prediction"] = pd.to_numeric(
            df["risk_prediction"], errors="coerce"
        ).fillna(0)

    # ---------- CREATE MAP ----------
    m = folium.Map(
        location=PUNE_CENTER,
        zoom_start=12,
        tiles="cartodbpositron"
    )

    # ===============================
    # 1️⃣ Accident Density
    # ===============================
    accident_points = df[["latitude", "longitude"]].values.tolist()

    HeatMap(
        accident_points,
        name="Accident Density",
        radius=10,
        blur=18,
        min_opacity=0.3,
        gradient=GRADIENT,
        max_zoom=16
    ).add_to(m)

    # ===============================
    # 2️⃣ Severity Heatmap
    # ===============================
    df["severity_norm"] = normalize(df["severity_weight"])

    severity_data = [
        [row.latitude, row.longitude, float(row.severity_norm)]
        for _, row in df.iterrows()
    ]

    HeatMap(
        severity_data,
        name="Severity Intensity",
        radius=14,
        blur=22,
        gradient=GRADIENT,
        min_opacity=0.4
    ).add_to(m)

    # ===============================
    # 3️⃣ Risk Score Heatmap
    # ===============================
    df["risk_norm"] = normalize(df["risk_score"])

    risk_data = [
        [row.latitude, row.longitude, float(row.risk_norm)]
        for _, row in df.iterrows()
    ]

    HeatMap(
        risk_data,
        name="AI Risk Score",
        radius=18,
        blur=28,
        min_opacity=0.5,
        gradient=GRADIENT
    ).add_to(m)

    # ===============================
    # 4️⃣ AI Risk Prediction ⭐
    # ===============================
    if "risk_prediction" in df.columns:

        prediction_data = [
            [
                float(row.latitude),
                float(row.longitude),
                float(row.risk_prediction / 100)
            ]
            for _, row in df.iterrows()
        ]

        HeatMap(
            prediction_data,
            name="AI Risk Prediction",
            radius=20,
            blur=30,
            min_opacity=0.5,
            gradient=GRADIENT
        ).add_to(m)

    # ===============================
    # Layer Control
    # ===============================
    folium.LayerControl(collapsed=False).add_to(m)

    # ---------- LEGEND ----------
    legend = """
    <div style="
    position: fixed;
    bottom: 50px;
    right: 50px;
    width: 180px;
    background-color: white;
    z-index:9999;
    padding:10px;
    border:2px solid grey;">
    <b>Risk Intensity</b><br>
    🔵 Low<br>
    🟢 Moderate<br>
    🟡 Elevated<br>
    🟠 High<br>
    🔴 Critical
    </div>
    """

    m.get_root().html.add_child(folium.Element(legend))

    return m