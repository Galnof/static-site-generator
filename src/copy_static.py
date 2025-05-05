import os
import shutil

def copy_files_recursive(source_dir_path, dest_dir_path):
    """
    Recursively copies all files and directories from a source directory to a destination directory.

    This function ensures that:
    1. The destination directory is created if it does not exist.
    2. Files are copied directly, while subdirectories are handled recursively.

    Args:
        `source_dir_path` (str): The source directory path from where files and directories are copied.
        `dest_dir_path` (str): The destination directory path where files and directories are copied to.

    Raises:
        `ValueError`: If the source directory does not exist.
    
    Side effects:
        - Creates directories in `dest_dir_path` if they don't exist.
        - Copies static files to `dest_path`.
        - Prints status message to console.
    """
    # Raise error if the source directory does not exist.
    if not os.path.exists(source_dir_path):
        raise ValueError("Invalid source path.")
    
    # Create the destination directory if it does not exist.
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    # Get a list of all files and directories in the source directory.
    path_entries = os.listdir(source_dir_path)

    for entry in path_entries:
        # Create full paths for the current source and corresponding destination entry.
        from_path = os.path.join(source_dir_path, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        # Check if path is a file, then copy files directly.
        if os.path.isfile(from_path):
            print(f"Copied file: {from_path} -> {dest_path}")
            shutil.copy(from_path, dest_path)
        else:
            # Recursively copy the content of subdirectories if not a file.
            copy_files_recursive(from_path, dest_path)
