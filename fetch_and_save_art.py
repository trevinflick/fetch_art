import requests
import json
from datetime import datetime

def fetch_art_data(artwork_id=27992):
    api_url = f"https://api.artic.edu/api/v1/artworks/{artwork_id}"
    params = {"fields": "title,image_id,artist_display,short_description"}
    response = requests.get(api_url, params=params)
    response.raise_for_status()  # Check for request errors
    data = response.json()["data"]  # Get the artwork data

    image_url = f"https://www.artic.edu/iiif/2/{data['image_id']}/full/400,/0/default.jpg"
    description = data.get("short_description", "No description available")
    artist_display = data.get("artist_display", "No artist information available")
    title = data.get("title", "No title available")

    return image_url, description, artist_display, title

def save_art_data():
    image_url, description, artist_display, title = fetch_art_data()
    art_data = {
        "image_url": image_url,
        "description": description,
        "artist_display": artist_display,
        "title": title,
        "fetched_at": datetime.now().isoformat()
    }
    with open("art_data.json", "w") as f:
        json.dump(art_data, f)

if __name__ == "__main__":
    save_art_data()
