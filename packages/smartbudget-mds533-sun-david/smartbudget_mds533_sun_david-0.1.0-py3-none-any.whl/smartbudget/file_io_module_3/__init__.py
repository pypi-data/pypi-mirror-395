"""
I/O subpackage for SmartBudget.

This module exposes the public interface of the I/O layer, grouping together
JSON serialization utilities and low-level file system operations. It provides
a clean and centralized access point for higher-level application modules.
"""

from .json_io import (
    save_to_json,
    load_from_json,
    append_to_json,
    clear_json
)

from .file_utils import (
    file_exists,
    delete_file,
    list_files
)

__all__ = [
    # JSON I/O
    "save_to_json",
    "load_from_json",
    "append_to_json",
    "clear_json",

    # File utilities
    "file_exists",
    "delete_file",
    "list_files",
]
