import json
import os

# Path to the directory containing JSON files
json_dir = '~/artic-api-data/json/artworks'
valid_art_ids = []

# Iterate over the JSON files in the directory
for filename in os.listdir(json_dir):
    if filename.endswith('.json'):
        file_path = os.path.join(json_dir, filename)
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)

                # Check if the JSON file contains an artwork with both a non-null image_id and short_description
                image_id = data.get('image_id')
                short_description = data.get('short_description')

                # Debug: Print the fields being checked
                print(f"Image ID: {image_id}, Short Description: {short_description}")

                if image_id and short_description:  # Ensure both are not null or empty
                    valid_art_ids.append(data['id'])
                    print(f"Valid artwork found: ID {data['id']}")
            
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {filename}: {e}")

# Save valid art IDs to a text file
output_file = 'valid_art_ids.txt'
with open(output_file, 'w') as file:
    for art_id in valid_art_ids:
        file.write(f"{art_id}\n")

print(f"Saved {len(valid_art_ids)} valid art IDs to {output_file}.")
