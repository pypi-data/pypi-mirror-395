from pystac_client import Client
import planetary_computer as pc
import geopandas as gpd
from shapely.geometry import box

# Define your area of interest (bounding box) in WGS84
# Bounding box: [min_lon, min_lat, max_lon, max_lat]
aoi_bbox = [-76.72, 39.18, -76.52, 39.38]  # Small area over Baltimore, Maryland
aoi = box(*aoi_bbox)

# Load the STAC API for MPC
client = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")

# Search for HLS data within the bounding box and date range
search = client.search(
    collections=["hls"],
    bbox=aoi_bbox,
    datetime="2024-01-01/2024-11-01",
    limit=50,  # Adjust limit as needed
)

# Get matching items
items = list(search.items())
print(f"Found {len(items)} items.")
