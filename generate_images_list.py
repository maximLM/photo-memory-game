import os
import json
import shutil
from pathlib import Path
import re

def clean_filename(filename):
    # Remove spaces and special characters, keep extension
    name, ext = os.path.splitext(filename)
    # Replace spaces and special chars with underscore, keep only alphanumeric
    clean_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    # Remove multiple underscores
    clean_name = re.sub(r'_+', '_', clean_name)
    # Remove leading/trailing underscores
    clean_name = clean_name.strip('_')
    print(f'before: {filename}, after: {clean_name}{ext.lower()}')
    return f"{clean_name}{ext.lower()}"


def convert_to_remote_url(path: Path, script_dir: Path) -> str:
    relative_path = str(path).replace(str(script_dir), '')
    return f"https://raw.githubusercontent.com/maximLM/photo-memory-game/main{relative_path}"



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
    
    # Clean filenames and collect image files
    image_files = []
    for ext in ['.jpg', '.jpeg', '.JPG', '.JPEG']:
        for file in photos_dir.glob(f'*{ext}'):
            clean_name = clean_filename(file.name)
            if clean_name != file.name:
                new_path = file.parent / clean_name
                print(f"Renaming: {file.name} -> {clean_name}")
                if new_path.exists():
                    base, ext = os.path.splitext(clean_name)
                    counter = 1
                    while new_path.exists():
                        new_path = file.parent / f"{base}_{counter}{ext}"
                        counter += 1
                shutil.move(str(file), str(new_path))
                image_files.append(new_path)
            else:
                image_files.append(file)

    # Create image paths (using local paths)
    
    image_paths = [convert_to_remote_url(path, script_dir) for path in image_files]
    # Save to images.json in the root directory
    json_path = script_dir / 'images.json'
    with open(json_path, 'w') as f:
        json.dump(image_paths, f, indent=2)
    
    print(f"\nFound {len(image_paths)} images:")
    for path in image_paths:
        print(f"  {path}")
    print(f"\nSaved to: {json_path}")

if __name__ == "__main__":
    generate_images_json() 