"""
Static Site Generator

This script generates a static website from markdown content using HTML templates.
It copies static assets and converts markdown files to HTML pages, supporting both
local development and GitHub Pages deployment via a configurable base path.

Usage:
    python3 main.py [basepath]
    
    where [basepath] is the optional root URL path (defaults to '/' if not provided)
"""

import os
import shutil
import sys
from copy_static import copy_files_recursive
from generate_content import generate_pages_recursive

# Directory paths used throughout the program.
static_dir_path = "./static"
docs_dir_path = "./docs"
content_dir_path = "./content"
template_path = "./template.html"

def main():
    """
    Main entry point for the static site generator.
    
    This function:
    1. Cleans the docs directory by removing it if it exists.
    2. Copies all static files to the docs directory.
    3. Determines the base path from command line arguments
    4. Generates HTML pages from markdown content.
    """
    # Clean the docs directory to start fresh.
    print("Deleting docs directory...")
    if os.path.exists(docs_dir_path):
        shutil.rmtree(docs_dir_path)

    # Copy static assets (CSS, JS, images, etc.) to the docs directory.
    print("Copying static files to docs directory...")
    copy_files_recursive(static_dir_path, docs_dir_path)

    # Determine the base path from command line arguments
    # For local development: '/'
    # For GitHub Pages: '/REPO_NAME/'
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    # Convert markdown content to HTML pages using the template.
    print("Generating content...")
    generate_pages_recursive(content_dir_path, template_path, docs_dir_path, basepath)

if __name__ == "__main__":
    main()
