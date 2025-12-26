import pandas as pd
import requests
import math
import os
import time
from tqdm import tqdm


INPUT_FILE = "train(1).xlsx"
OUTPUT_DIR = "house_images"
ZOOM_LEVEL = 18
MAX_RETRIES = 3
TIMEOUT = 15  

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
df = pd.read_excel(INPUT_FILE)
def latlon_to_tile(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return xtile, ytile

print(f"Starting download of {len(df)} images...")

for index, row in tqdm(df.iterrows(), total=len(df), desc="Fetching Images"):
    house_id = str(int(row['id']))
    file_path = os.path.join(OUTPUT_DIR, f"{house_id}.jpg")
    
    if os.path.exists(file_path):
        continue
        
    x, y = latlon_to_tile(row['lat'], row['long'], ZOOM_LEVEL)
    url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{ZOOM_LEVEL}/{y}/{x}"
    
    success = False
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=TIMEOUT)
            
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                success = True
                break 
            elif response.status_code == 404:
                break 
                
        except Exception:
            if attempt < MAX_RETRIES - 1:
                time.sleep(2)
            else:
                with open("failed_downloads.txt", "a") as f:
                    f.write(f"ID: {house_id}, Lat: {row['lat']}, Lon: {row['long']}\n")
    

    time.sleep(0.1)

print("Download process complete. Check 'house_images' folder.")