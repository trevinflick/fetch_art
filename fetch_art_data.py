import requests
import json
from datetime import date
import random

def fetch_random_art_data():
    # Step 1: Get the total number of artworks
    api_url = "https://api.artic.edu/api/v1/artworks"
    params = {"fields": "id", "limit": 1}  # We just need to know the total count
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    total_artworks = response.json()["pagination"]["total"]

    # Step 2: Generate a random artwork ID
    random_index = random.randint(1, total_artworks)

    # Step 3: Fetch the random artwork data
    params = {"fields": "id,title,image_id,artist_display,short_description", "limit": 1, "page": random_index}
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    data = response.json()["data"][0]  # Get the first (and only) item from data

    # Fetch and format the necessary fields
    art_id = data.get("id", "Unknown ID")
    image_url = f"https://www.artic.edu/iiif/2/{data['image_id']}/full/400,/0/default.jpg"
    description = data.get("short_description", "No description available")
    artist_display = data.get("artist_display", "No artist information available")
    title = data.get("title", "No title available")

    # Formatting artist name and additional details
    formatted_artist_info = format_artist_info(artist_display)
    
    return art_id, image_url, description, formatted_artist_info, title

def format_artist_info(artist_display):
    parts = artist_display.split(", ")
    if len(parts) >= 2:
        artist_name = parts[0]
        country = parts[1]
        years = ", ".join(parts[2:]) if len(parts) > 2 else ""
        # Insert a newline between artist name and the rest of the information
        return f"{artist_name}\n{country}, {years}"
    else:
        return artist_display

def save_art_data_to_file(filename="art_data.json"):
    # Fetch random art data
    art_id, image_url, description, artist_info, title = fetch_random_art_data()
    
    # Save data to a file
    art_data = {
        "id": art_id,
        "date": str(date.today()),  # Save the date to manage daily fetches
        "image_url": image_url,
        "description": description,
        "artist_info": artist_info,
        "title": title
    }

    with open(filename, "w") as file:
        json.dump(art_data, file, indent=4)

if __name__ == "__main__":
    save_art_data_to_file()
