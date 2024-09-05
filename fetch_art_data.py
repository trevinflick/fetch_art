import requests
import json
from datetime import date
import random
import time
import os

def fetch_art_ids_from_file(filename="valid_art_ids.txt"):
    art_ids = []
    if os.path.exists(filename):
        with open(filename, "r") as file:
            art_ids = [line.strip() for line in file.readlines()]
    else:
        print(f"File {filename} does not exist.")
    return art_ids

def fetch_random_art_data(max_attempts=10, timeout=5):
    art_ids = fetch_art_ids_from_file()
    if not art_ids:
        raise Exception("No valid art IDs found.")
    
    # Pick a random art ID from the list
    art_id = random.choice(art_ids)
    api_url = f"https://api.artic.edu/api/v1/artworks/{art_id}"
    params = {"fields": "id,title,image_id,artist_display,short_description,alt_text"}  # Include alt_text in fields
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(api_url, params=params, timeout=timeout)
            response.raise_for_status()
            data = response.json()["data"]  # Get the artwork data

            if data and data.get('image_id') and data.get('short_description'):
                # Fetch and format the necessary fields
                image_url_small=f"https://www.artic.edu/iiif/2/{data['image_id']}/full/200,/0/default.jpg"
                image_url_medium = f"https://www.artic.edu/iiif/2/{data['image_id']}/full/400,/0/default.jpg"
                image_url_large=f"https://www.artic.edu/iiif/2/{data['image_id']}/full/600,/0/default.jpg"
                image_url_full=f"https://www.artic.edu/iiif/2/{data['image_id']}/full/843,/0/default.jpg"
                description = data.get("short_description", "No description available")
                artist_display = data.get("artist_display", "No artist information available")
                title = data.get("title", "No title available")
                image_id = data.get("image_id", "No image ID available")
                alt_text = data.get("alt_text", "No alternative text available")  # Get alt_text

                # Formatting artist name and additional details
                formatted_artist_info = format_artist_info(artist_display)
                
                return art_id, image_id, image_url_small, image_url_medium, image_url_large, image_url_full, description, formatted_artist_info, title, alt_text  # Include alt_text in return

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(1)  # Sleep for a short period to avoid overwhelming the API
    
    raise Exception("Failed to find an artwork with a non-null image_id after maximum attempts.")

def format_artist_info(artist_display):
    parts = artist_display.split(", ")
    if len(parts) >= 2:
        artist_name = parts[0]
        country = parts[1]
        years = ", ".join(parts[2:]) if len(parts) > 2 else ""
        return f"{artist_name}\n{country}, {years}"
    else:
        return artist_display

def save_art_data_to_file(filename="art_data.json"):
    try:
        # Fetch random art data
        art_id, image_id, image_url_small, image_url_medium, image_url_large, image_url_full, description, artist_info, title, alt_text = fetch_random_art_data()  # Include alt_text in fetch

        # Save data to a file
        art_data = {
            "id": art_id,
            "date": str(date.today()),  # Save the date to manage daily fetches,
            "image_id": image_id,
            "image_url_small": image_url_small,
            "image_url_medium": image_url_medium,
            "image_url_large": image_url_large,
            "image_url_full": image_url_full,
            "description": description,
            "artist_info": artist_info,
            "title": title,
            "alt_text": alt_text  # Save alt_text
        }

        with open(filename, "w") as file:
            json.dump(art_data, file, indent=4)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    save_art_data_to_file()
