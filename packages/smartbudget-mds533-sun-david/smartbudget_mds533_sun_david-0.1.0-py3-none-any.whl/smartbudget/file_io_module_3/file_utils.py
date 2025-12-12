"""
General file utilities for SmartBudget.
All functions operate inside the 'files' directory.
"""

import os

# Directory where all files are stored
FILES_DIR = "files"


def ensure_files_dir():
    """Create the files/ directory if it does not exist."""
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)


def file_exists(filename):
    """Check whether a file exists in the files directory."""
    ensure_files_dir()
    return os.path.isfile(os.path.join(FILES_DIR, filename))


def delete_file(filename):
    """Delete a file inside the files directory."""
    ensure_files_dir()
    target = os.path.join(FILES_DIR, filename)
    if os.path.isfile(target):
        os.remove(target)
        return True
    return False


def list_files():
    """List files inside the files directory."""
    ensure_files_dir()
    return [f for f in os.listdir(FILES_DIR)
            if os.path.isfile(os.path.join(FILES_DIR, f))]
