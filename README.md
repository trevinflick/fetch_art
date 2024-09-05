# Fetch Art Data

This Python script fetches random artwork information from the Art Institute of Chicago's public API. It retrieves metadata such as the artwork title, image, artist details, description, and alternative text. The script saves the fetched data into a JSON file, allowing it to manage daily art fetches for integration into other projects or use in apps.

## Features

    - **Fetch random artwork**: Retrieves data for a randomly selected artwork from a list of valid IDs.
    - **Robust API handling**: Includes retries in case of failed API requests, ensuring reliable data fetching.
    - **Formatted artist information**: Displays artist details including name, country, and life dates (if available) in a readable format.
    - **Daily data saving**: Stores fetched artwork data into a art_data.json file, including the current date to enable managing daily fetches.
    - **Image and alternative text**: Fetches the artwork image URL and alt text for accessibility.

## Requirements

To use this script, you need:

    - Python 3.x
    - Required libraries: `requests`, `json`, `os`, `random`, `time`, `datetime`

Install the required libraries by running:
```bash
pip install requests
```

## How It Works

    1. **Valid Art IDs**: The script reads a list of valid artwork IDs from a text file (valid_art_ids.txt). Each ID corresponds to an artwork in the Art Institute of Chicago's collection.

    2. **Fetching Artwork Data**: The script sends an HTTP request to the API to fetch a random artwork's metadata, including the title, artist, image, description, and alt text.

    3. **Retries and Timeout**: If a request fails or does not return a valid image or description, the script retries up to 10 times before giving up.

    4. **Saving Data**: The fetched data is saved in a JSON file (art_data.json), which includes:
        Artwork ID
        Fetch date
        Image URL
        Description
        Artist information
        Title
        Alt text

## File Structure

    - valid_art_ids.txt: A file containing the list of valid artwork IDs (one ID per line).
    - art_data.json: Output file where the fetched artwork data is stored in JSON format.