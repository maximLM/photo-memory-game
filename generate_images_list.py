import os
import json
from pathlib import Path

def generate_images_json():
    # Get the directory of this script
    script_dir = Path(__file__).parent
    
    # Path to photos directory
    photos_dir = script_dir / 'assets' / 'photos'
    
    # Check if directory exists
    if not photos_dir.exists():
        print(f"Creating directory: {photos_dir}")
        photos_dir.mkdir(parents=True)
        return
    
    # Get all jpg/jpeg files
    image_files = []
    for ext in ['.jpg', '.jpeg', '.JPG', '.JPEG']:
        image_files.extend(list(photos_dir.glob(f'*{ext}')))
    
    # Create GitHub raw URLs for images
    base_url = "https://raw.githubusercontent.com/maximLM/photo-memory-game/main/assets/photos"
    image_paths = [f"{base_url}/assets/photos/{file.name}" 
                  for file in image_files]
    
    # Save to images.json in the root directory
    json_path = script_dir / 'images.json'
    with open(json_path, 'w') as f:
        json.dump(image_paths, f, indent=2)
    
    print(f"Found {len(image_paths)} images:")
    for path in image_paths:
        print(f"  {path}")
    print(f"\nSaved to: {json_path}")

if __name__ == "__main__":
    generate_images_json() 