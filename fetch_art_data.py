import requests
import json
from datetime import date
import random
import time

def read_valid_art_ids(filename="valid_art_ids.txt"):
    """Read valid art IDs from a text file."""
    with open(filename, "r") as file:
        valid_ids = [line.strip() for line in file.readlines()]
    return valid_ids

def fetch_art_data_by_id(art_id, timeout=5):
    """Fetch the art data for a specific artwork ID."""
    api_url = f"https://api.artic.edu/api/v1/artworks/{art_id}"
    params = {"fields": "id,title,image_id,artist_display,short_description"}
    response = requests.get(api_url, params=params, timeout=timeout)
    response.raise_for_status()
    data = response.json()["data"]  # Get the artwork data

    # Fetch and format the necessary fields
    image_url = f"https://www.artic.edu/iiif/2/{data['image_id']}/full/400,/0/default.jpg"
    description = data.get("short_description", "No description available")
    artist_display = data.get("artist_display", "No artist information available")
    title = data.get("title", "No title available")

    # Formatting artist name and additional details
    formatted_artist_info = format_artist_info(artist_display)
    
    return art_id, image_url, description, formatted_artist_info, title

def format_artist_info(artist_display):
    """Format artist information."""
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
    try:
        # Read valid art IDs from file
        valid_art_ids = read_valid_art_ids()
        
        if not valid_art_ids:
            raise Exception("No valid art IDs found.")

        # Choose a random art ID from the valid art IDs
        art_id = random.choice(valid_art_ids)

        # Fetch art data for the selected ID
        art_id, image_url, description, artist_info, title = fetch_art_data_by_id(art_id)
        
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
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    save_art_data_to_file()
