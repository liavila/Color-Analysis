from bing_image_downloader import downloader
import pandas as pd
import os

# Read the CSV file into a DataFrame
data = pd.read_csv("Celebs and seasons.csv", header=None, names=["Celebrity", "Season"])

def download_images(celebrity, season, num_images=50):
    query = f"{celebrity} portrait"
    downloader.download(query, limit=num_images,  output_dir=f'season_images/{season}', adult_filter_off=True, force_replace=False, timeout=60)

# Ensure the directory for each season exists and download images
for season in data['Season'].unique():
    os.makedirs(f"season_images/{season}", exist_ok=True)

for index, row in data.iterrows():
    download_images(row['Celebrity'], row['Season'])

print("Download complete!")
