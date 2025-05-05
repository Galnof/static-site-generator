import os
import shutil
from copy_static import copy_files_recursive
from generate_content import generate_pages_recursive

# Directory paths used throughout the program.
static_dir_path = "./static"
public_dir_path = "./public"
content_dir_path = "./content"
template_path = "./template.html"

def main():
    """
    Main entry point for the static site generator.
    
    This function:
    1. Cleans the public directory by removing it if it exists.
    2. Copies all static files to the public directory.
    3. Generates HTML pages from markdown content.
    """
    # Clean the public directory to start fresh.
    print("Deleting public directory...")
    if os.path.exists(public_dir_path):
        shutil.rmtree(public_dir_path)

    # Copy static assets (CSS, JS, images, etc.) to the public directory.
    print("Copying static files to public directory...")
    copy_files_recursive(static_dir_path, public_dir_path)

    # Convert markdown content to HTML pages using the template.
    print("Generating content...")
    generate_pages_recursive(content_dir_path, template_path, public_dir_path)

if __name__ == "__main__":
    main()
