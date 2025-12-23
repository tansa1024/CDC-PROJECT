import requests
import math
import os

# House coordinates from your dataset
lat = 47.4632
lon = -122.187
zoom = 18  # Zoom 18 or 19 is best for individual houses

def latlon_to_tile(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return x, y

x, y = latlon_to_tile(lat, lon, zoom)

# ESRI Satellite Tile Server - High Resolution
url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{y}/{x}"

# Headers are important to avoid being blocked as a bot
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open("house_satellite.jpg", "wb") as f:
        f.write(response.content)
    print("Satellite image saved!")
else:
    print(f"Error: {response.status_code}")


