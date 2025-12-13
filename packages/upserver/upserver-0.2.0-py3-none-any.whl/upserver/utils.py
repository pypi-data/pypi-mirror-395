"""
Utility functions for the upserver package.
"""

import os
import shutil
import platform
from pathlib import Path
import unicodedata


def sanitize_filename(filename):
    """
    Sanitize a filename by removing quotes and preventing path traversal.
    Also checks for null bytes, reserved device names (Windows), excessive length,
    hidden files (starting with dot), and normalizes Unicode to NFC.

    Args:
        filename (str): Original filename

    Returns:
        str: Sanitized filename
    """
    # Remove spaces, quotes and any directory components
    name = os.path.basename(filename.strip().strip("'\""))

    # Normalize Unicode to NFC
    name = unicodedata.normalize("NFC", name)

    # Remove null bytes
    name = name.replace("\x00", "")

    # Reserved device names on Windows (case-insensitive, with or without extension)
    reserved_names = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }
    name_no_ext, ext = os.path.splitext(name)
    if name_no_ext.upper() in reserved_names:
        name_no_ext = f"_{name_no_ext}"
        name = name_no_ext + ext

    # Prevent hidden files (starting with dot)
    if name.startswith("."):
        name = name.lstrip(".")
        if not name:
            name = "file"

    # Limit filename length (255 bytes is a common max)
    max_len = 255
    # Truncate if necessary, preserving extension
    if len(name.encode("utf-8")) > max_len:
        # Try to preserve extension
        name_no_ext, ext = os.path.splitext(name)
        _ = max_len - len(ext.encode("utf-8"))  # noqa: F841
        # Truncate name_no_ext to fit
        while len((name_no_ext + ext).encode("utf-8")) > max_len and name_no_ext:
            name_no_ext = name_no_ext[:-1]
        name = name_no_ext + ext
        if not name_no_ext:
            name = "file" + ext

    # Fallback if name is empty
    if not name:
        name = "file"

    return name


def get_disk_space(path):
    """
    Get disk space information in a cross-platform way.
    Works on both Windows and Linux.

    Args:
        path (str): Path to check disk space for

    Returns:
        tuple: (total_gb, used_gb, free_gb)
    """
    try:
        # Using shutil.disk_usage which works on both Windows and Linux
        total, used, free = shutil.disk_usage(path)

        # Convert to GB
        total_gb = total / (1024**3)
        used_gb = used / (1024**3)
        free_gb = free / (1024**3)

        return total_gb, used_gb, free_gb

    except Exception as e:
        print(f"⚠️  Error getting disk space information: {e}")
        # Default values in case of error
        return 0.0, 0.0, 0.0


def format_file_size(size_bytes):
    """
    Format file size in human readable format.

    Args:
        size_bytes (int): Size in bytes

    Returns:
        str: Formatted size string
    """
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.2f} {size_names[i]}"


def ensure_directory_exists(directory):
    """
    Ensure that a directory exists, create if it doesn't.

    Args:
        directory (str or Path): Directory path

    Returns:
        Path: Path object for the directory
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_system_info():
    """
    Get system information for logging purposes.

    Returns:
        dict: System information
    """
    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }
