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
    
    # Dictionary to store images by folder
    images_by_folder = {}
    
    for ext in ['.jpg', '.jpeg', '.JPG', '.JPEG']:
        for file in photos_dir.rglob(f'*{ext}'):
            clean_name = clean_filename(file.name)
            folder_name = file.parent.name
            
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
                path_to_add = new_path
            else:
                path_to_add = file
            
            # Add to folder dictionary
            if folder_name not in images_by_folder:
                images_by_folder[folder_name] = []
            images_by_folder[folder_name].append(convert_to_remote_url(path_to_add, script_dir))
    
    # Save to images.json in the root directory
    json_path = script_dir / 'images.json'
    with open(json_path, 'w') as f:
        json.dump(images_by_folder, f, indent=2)
    
    print(f"\nFound images in {len(images_by_folder)} folders:")
    for folder, paths in images_by_folder.items():
        print(f"\n{folder}: {len(paths)} images")
        for path in paths:
            print(f"  {path}")
    print(f"\nSaved to: {json_path}")

if __name__ == "__main__":
    generate_images_json() 