from fastapi import FastAPI, Request
import pandas as pd
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from utils.geocode import geocode_location
from utils.routing import get_routes
from utils.route_risk import compute_route_risk
from fastapi.responses import JSONResponse
import os
from utils.dashboard_data import create_dashboard_metrics
from utils.data_processing import load_data
from utils.risk_engine import compute_severity_weight, compute_risk_score
from utils.feature_engineering import (
    create_features,
    generate_negative_samples
)
from utils.ml_model import train_model
from utils.map_builder import build_map
from utils.heatmap import build_severity_heatmap

app = FastAPI(title="SafePath AI")

templates = Jinja2Templates(directory="templates")

heatmap_cache = None
# -------------------------------
# LOAD DATA ON STARTUP (ONLY ONCE)
# -------------------------------
@app.on_event("startup")
def startup_loader():

    
    global model, heatmap_cache

    print("Preparing ML system...")

    df = load_data()

    df = create_features(df)

    # 🔥 BUILD HEATMAP HERE
    heatmap_cache = build_severity_heatmap(df)

    negative_df = generate_negative_samples(df)

    full_df = pd.concat([df, negative_df])

    model = train_model(full_df)

    print("System Ready ✅")
    # ---------------------------------
# Create ML risk prediction column
# ---------------------------------
    from utils.ml_model import FEATURES

    X = df[FEATURES]

    df["risk_probability"] = model.predict_proba(X)[:,1]

# Convert to 0–100 score
    df["risk_score"] = (df["risk_probability"] * 100).round(2)
    app.state.df = df
    app.state.model = model

    print("ML Model Ready ✅")# -------------------------------
# HOME PAGE
# -------------------------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    df = app.state.df

    metrics, day_counts, risk_bins, road_risk = \
        create_dashboard_metrics(df)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "metrics": metrics,
            "day_counts": day_counts,
            "risk_bins": risk_bins,
            "road_risk": road_risk,
        },
    )

# -------------------------------
# MAP ENDPOINT
# -------------------------------
@app.get("/map")
def get_map():
    return FileResponse("outputs/pune_map.html")

# -------------------------------
# ROUTE FINDER API
# -------------------------------
@app.post("/routes")
async def find_routes(data: dict):

    df_global = app.state.df

    # ✅ start location from browser GPS
    start_lat = float(data["start_lat"])
    start_lon = float(data["start_lon"])

    destination = data["destination"]

    coords = geocode_location(destination)

    if coords is None:
        return {"error": "Location not found"}

    end_lat, end_lon = coords

    routes = get_routes(start_lat, start_lon, end_lat, end_lon)

    model = app.state.model

    for r in routes:
        r["risk_score"] = compute_route_risk(
        r["points"],
        model
    )

    fastest = min(routes, key=lambda r: r["time_sec"])
    safest = min(routes, key=lambda r: r["risk_score"])

    selected_routes = [
        {**fastest, "type": "fastest"}
    ]

    if safest["route_id"] != fastest["route_id"]:
        selected_routes.append(
            {**safest, "type": "safest"}
        )

    return {"routes": selected_routes}

@app.get("/heatmap-data")
def get_heatmap():
    return {"data": heatmap_cache}