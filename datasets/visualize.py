# ----------------------------------
# SafePath AI - Pune Map Visualization
# ----------------------------------

import pandas as pd
import folium
from folium.plugins import HeatMap

# -------------------------
# Load Dataset
# -------------------------
df = pd.read_csv("./datasets/pune_accidents.csv")

# -------------------------
# Create Base Map (Pune Center)
# -------------------------
pune_map = folium.Map(
    location=[18.5204, 73.8567],   # Pune center
    zoom_start=12,
    tiles="OpenStreetMap"
)

# -------------------------
# Add Accident Markers
# -------------------------
for _, row in df.iterrows():

    if row["severity"] == 1:
        color = "green"
    elif row["severity"] == 2:
        color = "orange"
    else:
        color = "red"

    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=3,
        color=color,
        fill=True,
        fill_opacity=0.7,
        popup=f"""
        Severity: {row['severity']}<br>
        Weather: {row['weather']}<br>
        Area: {row['area_name']}
        """
    ).add_to(pune_map)

# -------------------------
# Create Heatmap Layer
# -------------------------
heat_data = df[["latitude", "longitude"]].values.tolist()

HeatMap(heat_data, radius=10).add_to(pune_map)

# -------------------------
# Save Map
# -------------------------
output_file = "pune_accident_map.html"
pune_map.save(output_file)

print("✅ Map created successfully!")
print("Open:", output_file)