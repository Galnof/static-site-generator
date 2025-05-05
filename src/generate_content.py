import os
from block_markdown_to_html import markdown_to_html_node

def generate_pages_recursive(content_dir_path, template_path, dest_dir_path):
    """
    Recursively generates HTML pages from markdown files.
    
    Args:
        `content_dir_path` (str): Path to the directory containing markdown content.
        `template_path` (str): Path to the HTML template file.
        `dest_dir_path` (str): Path to the destination directory for generated HTML files.
        
    Raises:
        `ValueError`: If the content directory path is invalid.
    
    Side effects:
        - Uses `generate_page` to generate directories and file for `dest_html_path`.
    """
    # Validate content directory exists. 
    if not os.path.exists(content_dir_path):
        raise ValueError("Invalid content path.")
    
    # Get all entries in the content directory.
    path_entries = os.listdir(content_dir_path)
    
    for entry in path_entries:
        # Create full paths for source and destination.
        content_path = os.path.join(content_dir_path, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(content_path):
            # If it's a markdown file, convert to HTML.
            if content_path.endswith(".md"):
                # Change extension from .md to .html.
                dest_html_path = dest_path[:-3] + ".html"
                # Generate the HTML page.
                generate_page(content_path, template_path, dest_html_path)
        elif os.path.isdir(content_path):
            # If it's a directory, process it recursively.
            generate_pages_recursive(content_path, template_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    """
    Generate an HTML page from a markdown file using a template.
    
    Args:
        `from_path` (str): Path to the markdown file to convert.
        `template_path` (str): Path to the HTML template file.
        `dest_path` (str): Path where the generated HTML file will be saved.
    
    Side effects:
        - Creates directories in `dest_path` if they don't exist.
        - Writes generated HTML to `dest_path`.
        - Prints status message to console.
    """
    # Log the generation process.
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read and store the markdown content.
    with open(from_path) as file:
        from_doc = file.read()

    # Read and store the HTML template.
    with open(template_path) as file:
        template_doc = file.read()
    
    # Extract the title from the markdown content.
    title = extract_title(from_doc)
    
    # Convert markdown to HTML.
    content = markdown_to_html_node(from_doc).to_html()
    
    # Replace placeholders in the template with content and title.
    new_template = template_doc.replace("{{ Title }}", title).replace("{{ Content }}", content)
    
    # Ensure the destination directory exists, then make directories as needed.
    dest_dir_name = os.path.dirname(dest_path)
    if dest_dir_name != "":
        os.makedirs(dest_dir_name, exist_ok=True)
    
    # Write the final HTML to the destination file.
    with open(dest_path, "w") as file:
        file.write(new_template)

def extract_title(markdown):
    """
    Extract the h1 header from a `markdown` string and return it as the title.
    
    Args:
        `markdown` (str): The `markdown` content to extract the title from.
        
    Returns:
        str: The text of the h1 header without the '# ' prefix.
        
    Raises:
        `ValueError`: If no h1 header is found in the `markdown`.
    """
    # Split the markdown into separate lines.
    lines = markdown.split("\n")

    # Check each line for an h1 header. (starts with '# ')
    for line in lines:
        if line.startswith("# "):
            # Remove the '# ' prefix and any leading/trailing whitespace.
            title = line[2:].strip()
            return title
    
    # If no h1 header is found, raise an error.
    raise ValueError("No title found in markdown.")
