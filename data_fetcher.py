import pandas as pd
import requests
import math
import os
import time
from tqdm import tqdm

# --- CONFIGURATION ---
INPUT_FILE = "train(1).xlsx"
OUTPUT_DIR = "house_images"
ZOOM_LEVEL = 18
MAX_RETRIES = 3
TIMEOUT = 15  # Seconds to wait for server response

# 1. Setup Folders
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 2. Load Dataset
df = pd.read_excel(INPUT_FILE)

# 3. Coordinate to Tile Logic
def latlon_to_tile(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return xtile, ytile

# 4. Download Loop
print(f"Starting download of {len(df)} images...")

for index, row in tqdm(df.iterrows(), total=len(df), desc="Fetching Images"):
    house_id = str(int(row['id']))
    file_path = os.path.join(OUTPUT_DIR, f"{house_id}.jpg")
    
    # Skip if already downloaded
    if os.path.exists(file_path):
        continue
        
    x, y = latlon_to_tile(row['lat'], row['long'], ZOOM_LEVEL)
    
    # Esri Satellite Tile Server
    url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{ZOOM_LEVEL}/{y}/{x}"
    
    # Retry Mechanism for Connection Timeouts
    success = False
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=TIMEOUT)
            
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                success = True
                break  # Exit retry loop on success
            elif response.status_code == 404:
                # No tile exists for this coordinate at this zoom
                break 
                
        except Exception:
            if attempt < MAX_RETRIES - 1:
                time.sleep(2) # Wait before retrying
            else:
                # Log failures to a text file for review later
                with open("failed_downloads.txt", "a") as f:
                    f.write(f"ID: {house_id}, Lat: {row['lat']}, Lon: {row['long']}\n")
    
    # Small pause to be polite to the server
    time.sleep(0.1)

print("Download process complete. Check 'house_images' folder.")